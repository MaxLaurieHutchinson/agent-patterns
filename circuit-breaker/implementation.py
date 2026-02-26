"""
Circuit Breaker Implementation
Production-ready circuit breaker for LLM calls with cost protection,
rate limiting, and automatic recovery detection.
"""

from typing import Callable, Any, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum, auto
from threading import Lock
import time
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = auto()      # Normal operation
    OPEN = auto()        # Failing fast
    HALF_OPEN = auto()   # Testing recovery


@dataclass
class CircuitConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5           # Failures before opening
    success_threshold: int = 3           # Successes to close from half-open
    timeout_duration: float = 60.0       # Seconds before half-open
    
    # Cost protection
    cost_budget: float = 10.0            # Max $ per window
    cost_window_seconds: float = 3600.0  # 1 hour window
    
    # Rate limiting
    rate_limit_per_second: int = 10
    
    # Half-open settings
    half_open_max_calls: int = 3
    
    # Fallback
    fallback_function: Optional[Callable] = None


@dataclass
class CallMetrics:
    """Metrics for circuit breaker monitoring."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0
    total_cost: float = 0.0
    current_window_cost: float = 0.0
    last_call_time: float = 0.0
    state_changes: list[tuple[float, str]] = field(default_factory=list)


class CircuitBreakerOpen(Exception):
    """Exception raised when circuit breaker is open."""
    pass


class CircuitBreaker:
    """
    Circuit breaker for protecting LLM calls.
    
    States:
    - CLOSED: Normal operation, all requests pass through
    - OPEN: Failing fast, requests rejected immediately
    - HALF_OPEN: Testing if service has recovered
    """
    
    def __init__(self, name: str, config: Optional[CircuitConfig] = None):
        self.name = name
        self.config = config or CircuitConfig()
        self.state = CircuitState.CLOSED
        
        # Counters
        self.failure_count = 0
        self.success_count = 0
        self.half_open_calls = 0
        
        # Timing
        self.last_failure_time = 0.0
        self.last_state_change = time.time()
        
        # Cost tracking (rolling window)
        self._cost_window: list[tuple[float, float]] = []  # (timestamp, cost)
        
        # Rate limiting
        self._call_times: list[float] = []
        
        # Metrics
        self.metrics = CallMetrics()
        
        # Thread safety
        self._lock = Lock()
        
        logger.info(f"Circuit breaker '{name}' initialized in {self.state.name} state")
    
    def call(self, func: Callable[..., T], *args, 
             cost_estimate: float = 0.0, **kwargs) -> T:
        """
        Execute a function with circuit breaker protection.
        
        Args:
            func: Function to call (typically LLM invocation)
            *args: Positional arguments for func
            cost_estimate: Estimated cost of this call
            **kwargs: Keyword arguments for func
            
        Returns:
            Result from func
            
        Raises:
            CircuitBreakerOpen: If circuit is open
            Exception: Any exception from func (recorded as failure)
        """
        with self._lock:
            # Check cost budget
            self._clean_expired_costs()
            if not self._check_cost_budget(cost_estimate):
                self.metrics.rejected_calls += 1
                logger.warning(f"Circuit '{self.name}': Cost budget exceeded")
                raise CircuitBreakerOpen("Cost budget exceeded for time window")
            
            # Check rate limit
            if not self._check_rate_limit():
                self.metrics.rejected_calls += 1
                logger.warning(f"Circuit '{self.name}': Rate limit exceeded")
                raise CircuitBreakerOpen("Rate limit exceeded")
            
            # Check circuit state
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self._transition_to(CircuitState.HALF_OPEN)
                    self.half_open_calls = 0
                else:
                    self.metrics.rejected_calls += 1
                    logger.info(f"Circuit '{self.name}': Rejecting call (OPEN)")
                    
                    # Try fallback
                    if self.config.fallback_function:
                        return self.config.fallback_function(*args, **kwargs)
                    raise CircuitBreakerOpen(
                        f"Circuit '{self.name}' is OPEN. "
                        f"Try again after {self._time_until_half_open():.0f}s"
                    )
            
            elif self.state == CircuitState.HALF_OPEN:
                if self.half_open_calls >= self.config.half_open_max_calls:
                    self.metrics.rejected_calls += 1
                    raise CircuitBreakerOpen(
                        "Circuit HALF-OPEN: max test calls reached"
                    )
                self.half_open_calls += 1

            self.metrics.total_calls += 1
            self.metrics.last_call_time = time.time()
        
        # Execute the call (outside lock to allow concurrency)
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception:
            self.record_failure()
            raise
    
    def record_success(self):
        """Record a successful call."""
        with self._lock:
            self.metrics.successful_calls += 1
            self.success_count += 1
            
            if self.state == CircuitState.HALF_OPEN:
                if self.success_count >= self.config.success_threshold:
                    logger.info(f"Circuit '{self.name}': Success threshold reached, closing")
                    self._transition_to(CircuitState.CLOSED)
            
            # Reset failure count on success
            self.failure_count = 0
    
    def record_failure(self, cost: float = 0.0):
        """Record a failed call."""
        with self._lock:
            self.metrics.failed_calls += 1
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            # Track cost
            if cost > 0:
                self._add_cost(cost)
            
            if self.state == CircuitState.HALF_OPEN:
                # Failure in half-open immediately opens circuit
                logger.warning(f"Circuit '{self.name}': Failure in HALF-OPEN, opening")
                self._transition_to(CircuitState.OPEN)
            elif self.state == CircuitState.CLOSED:
                if self.failure_count >= self.config.failure_threshold:
                    logger.warning(
                        f"Circuit '{self.name}': Failure threshold reached ({self.failure_count}), opening"
                    )
                    self._transition_to(CircuitState.OPEN)
    
    def record_cost(self, cost: float):
        """Record the cost of a call."""
        with self._lock:
            self._add_cost(cost)
    
    def _add_cost(self, cost: float):
        """Add cost to tracking window."""
        now = time.time()
        self._cost_window.append((now, cost))
        self.metrics.total_cost += cost
        self._clean_expired_costs()
        self.metrics.current_window_cost = sum(c for _, c in self._cost_window)
    
    def _clean_expired_costs(self):
        """Remove costs outside the time window."""
        now = time.time()
        cutoff = now - self.config.cost_window_seconds
        self._cost_window = [(t, c) for t, c in self._cost_window if t > cutoff]
    
    def _check_cost_budget(self, estimated_cost: float) -> bool:
        """Check if call would exceed cost budget."""
        current_window_cost = sum(c for _, c in self._cost_window)
        return (current_window_cost + estimated_cost) <= self.config.cost_budget
    
    def _check_rate_limit(self) -> bool:
        """Check if call would exceed rate limit."""
        now = time.time()
        cutoff = now - 1.0  # 1 second window
        self._call_times = [t for t in self._call_times if t > cutoff]
        
        if len(self._call_times) >= self.config.rate_limit_per_second:
            return False
        
        self._call_times.append(now)
        return True
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to try half-open."""
        return (time.time() - self.last_failure_time) >= self.config.timeout_duration
    
    def _time_until_half_open(self) -> float:
        """Get time remaining until half-open state."""
        if self.state != CircuitState.OPEN:
            return 0.0
        elapsed = time.time() - self.last_failure_time
        return max(0.0, self.config.timeout_duration - elapsed)
    
    def _transition_to(self, new_state: CircuitState):
        """Transition to a new state."""
        old_state = self.state
        self.state = new_state
        self.last_state_change = time.time()
        
        # Reset counters on transition
        if new_state == CircuitState.CLOSED:
            self.failure_count = 0
            self.success_count = 0
        elif new_state == CircuitState.OPEN:
            self.success_count = 0
        elif new_state == CircuitState.HALF_OPEN:
            self.success_count = 0
            self.half_open_calls = 0
        
        self.metrics.state_changes.append((time.time(), f"{old_state.name} -> {new_state.name}"))
        logger.info(f"Circuit '{self.name}': {old_state.name} -> {new_state.name}")
    
    def get_state(self) -> CircuitState:
        """Get current circuit state."""
        with self._lock:
            return self.state
    
    def get_metrics(self) -> dict:
        """Get current metrics."""
        with self._lock:
            self._clean_expired_costs()
            return {
                "circuit_name": self.name,
                "state": self.state.name,
                "failure_count": self.failure_count,
                "success_count": self.success_count,
                "total_calls": self.metrics.total_calls,
                "successful_calls": self.metrics.successful_calls,
                "failed_calls": self.metrics.failed_calls,
                "rejected_calls": self.metrics.rejected_calls,
                "total_cost": self.metrics.total_cost,
                "current_window_cost": sum(c for _, c in self._cost_window),
                "cost_budget": self.config.cost_budget,
                "state_changes": self.metrics.state_changes[-10:]  # Last 10
            }
    
    def reset(self):
        """Manually reset the circuit breaker to CLOSED."""
        with self._lock:
            self._transition_to(CircuitState.CLOSED)
            logger.info(f"Circuit '{self.name}': Manually reset")


def circuit_breaker(name: str, config: Optional[CircuitConfig] = None):
    """
    Decorator to apply circuit breaker to a function.
    
    Usage:
        @circuit_breaker("my_llm", CircuitConfig(failure_threshold=3))
        def call_llm(prompt):
            return llm.invoke(prompt)
    """
    breaker = CircuitBreaker(name, config)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, cost_estimate: float = 0.0, **kwargs) -> T:
            return breaker.call(func, *args, cost_estimate=cost_estimate, **kwargs)
        
        # Attach breaker for manual control
        wrapper.circuit_breaker = breaker
        return wrapper
    
    return decorator
