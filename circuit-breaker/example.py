"""
Circuit Breaker Example
Demonstrates using circuit breaker to protect LLM calls.
"""

import os
import time
from langchain_openai import ChatOpenAI
from implementation import (
    CircuitBreaker, CircuitConfig, CircuitState, 
    CircuitBreakerOpen, circuit_breaker
)


def demo_basic_usage():
    """Demonstrate basic circuit breaker usage."""
    print("\n" + "="*60)
    print("Basic Circuit Breaker Demo")
    print("="*60)
    
    # Create a circuit breaker with lenient settings for demo
    config = CircuitConfig(
        failure_threshold=3,
        success_threshold=2,
        timeout_duration=5.0,  # 5 seconds for demo
        cost_budget=1.0
    )
    
    breaker = CircuitBreaker("demo", config)
    
    # Simulate some successful calls
    print("\n✅ Simulating successful calls...")
    for i in range(5):
        try:
            # Simulate a function call
            result = breaker.call(lambda: f"Success {i+1}")
            print(f"   Call {i+1}: {result}")
            breaker.record_success()
        except Exception as e:
            print(f"   Call {i+1}: Error - {e}")
    
    print(f"\n   State: {breaker.get_state().name}")
    print(f"   Success count: {breaker.success_count}")
    
    # Now simulate failures
    print("\n❌ Simulating failures...")
    for i in range(5):
        try:
            breaker.record_failure()
            print(f"   Failure {i+1}: Recorded")
        except CircuitBreakerOpen as e:
            print(f"   Failure {i+1}: Circuit opened - {e}")
            break
    
    print(f"\n   State: {breaker.get_state().name}")
    print(f"   Failure count: {breaker.failure_count}")
    
    # Try to call while open
    print("\n🚫 Trying to call while circuit is open...")
    try:
        result = breaker.call(lambda: "Should not execute")
        print(f"   Result: {result}")
    except CircuitBreakerOpen as e:
        print(f"   Rejected: {e}")
    
    # Wait for timeout
    print(f"\n⏳ Waiting {config.timeout_duration}s for half-open...")
    time.sleep(config.timeout_duration)
    
    # Try again (should enter half-open)
    print("\n🔄 Trying to call (should enter half-open)...")
    try:
        result = breaker.call(lambda: "Test success")
        print(f"   Result: {result}")
        breaker.record_success()
        print(f"   State: {breaker.get_state().name}")
    except Exception as e:
        print(f"   Error: {e}")


def demo_cost_protection():
    """Demonstrate cost budget protection."""
    print("\n" + "="*60)
    print("Cost Protection Demo")
    print("="*60)
    
    config = CircuitConfig(
        cost_budget=0.10,  # $0.10 budget
        cost_window_seconds=60.0
    )
    
    breaker = CircuitBreaker("cost_demo", config)
    
    # Simulate calls with costs
    print("\n💰 Simulating calls with costs...")
    costs = [0.02, 0.03, 0.02, 0.03, 0.05]  # Will exceed $0.10 on 5th call
    
    for i, cost in enumerate(costs):
        try:
            # Check budget before call
            result = breaker.call(
                lambda c=cost: f"Call completed (cost: ${c})",
                cost_estimate=cost
            )
            breaker.record_cost(cost)
            print(f"   Call {i+1}: ${cost:.2f} - {result}")
        except CircuitBreakerOpen as e:
            print(f"   Call {i+1}: ${cost:.2f} - REJECTED (budget exceeded)")
            print(f"   Error: {e}")
    
    metrics = breaker.get_metrics()
    print(f"\n   Total cost: ${metrics['total_cost']:.2f}")
    print(f"   Window cost: ${metrics['current_window_cost']:.2f}")
    print(f"   Budget: ${metrics['cost_budget']:.2f}")


def demo_decorator():
    """Demonstrate using circuit breaker as a decorator."""
    print("\n" + "="*60)
    print("Decorator Demo")
    print("="*60)
    
    @circuit_breaker("my_service", CircuitConfig(
        failure_threshold=2,
        timeout_duration=3.0
    ))
    def unreliable_service(fail: bool = False):
        """A simulated unreliable service."""
        if fail:
            raise Exception("Service failed!")
        return "Service succeeded!"
    
    # Successful calls
    print("\n✅ Successful calls...")
    for i in range(3):
        try:
            result = unreliable_service(fail=False)
            print(f"   Call {i+1}: {result}")
        except Exception as e:
            print(f"   Call {i+1}: {e}")
    
    # Failed calls
    print("\n❌ Failed calls...")
    for i in range(3):
        try:
            result = unreliable_service(fail=True)
            print(f"   Call {i+1}: {result}")
        except CircuitBreakerOpen as e:
            print(f"   Call {i+1}: Circuit breaker open - {e}")
        except Exception as e:
            unreliable_service.circuit_breaker.record_failure()
            print(f"   Call {i+1}: Service error - {e}")
    
    # Check state
    state = unreliable_service.circuit_breaker.get_state()
    print(f"\n   Circuit state: {state.name}")
    
    # Check metrics
    metrics = unreliable_service.circuit_breaker.get_metrics()
    print(f"   Total calls: {metrics['total_calls']}")
    print(f"   Failed: {metrics['failed_calls']}")
    print(f"   Rejected: {metrics['rejected_calls']}")


def demo_llm_protection():
    """Demonstrate protecting actual LLM calls."""
    print("\n" + "="*60)
    print("LLM Protection Demo")
    print("="*60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY to run LLM demo")
        print("   Showing configuration example...\n")
        
        print("""
    Usage with LangChain:
    
    from langchain_openai import ChatOpenAI
    from circuit_breaker import CircuitBreaker, CircuitConfig
    
    # Configure circuit breaker
    breaker = CircuitBreaker("openai", CircuitConfig(
        failure_threshold=3,
        success_threshold=2,
        timeout_duration=60.0,
        cost_budget=5.0,  # $5 per hour
        rate_limit_per_second=5
    ))
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    # Protected call
    try:
        result = breaker.call(
            lambda: llm.invoke("Hello!"),
            cost_estimate=0.01
        )
        breaker.record_cost(0.01)  # Actual cost
        print(result.content)
    except CircuitBreakerOpen:
        print("Circuit open - using fallback")
        # Use cheaper model or cached response
    """)
        return
    
    # Real LLM demo
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    breaker = CircuitBreaker("openai_demo", CircuitConfig(
        failure_threshold=3,
        cost_budget=0.50,
        rate_limit_per_second=2
    ))
    
    print("\n🤖 Making protected LLM calls...")
    prompts = [
        "Say 'Hello' in 5 words",
        "What is 2+2?",
        "Name a color",
        "Count to 3",
    ]
    
    for prompt in prompts:
        try:
            result = breaker.call(
                lambda p=prompt: llm.invoke(p),
                cost_estimate=0.01
            )
            breaker.record_success()
            print(f"   ✅ '{prompt[:30]}...' -> {result.content[:50]}...")
        except CircuitBreakerOpen as e:
            print(f"   ❌ '{prompt[:30]}...' -> Circuit open")
        except Exception as e:
            breaker.record_failure(cost=0.01)
            print(f"   ❌ '{prompt[:30]}...' -> Error: {e}")
    
    # Print metrics
    metrics = breaker.get_metrics()
    print(f"\n📊 Metrics:")
    print(f"   State: {metrics['state']}")
    print(f"   Total calls: {metrics['total_calls']}")
    print(f"   Successful: {metrics['successful_calls']}")
    print(f"   Cost: ${metrics['current_window_cost']:.3f} / ${metrics['cost_budget']:.2f}")


def demo_fallback():
    """Demonstrate fallback functionality."""
    print("\n" + "="*60)
    print("Fallback Demo")
    print("="*60)
    
    def expensive_llm_call(prompt: str) -> str:
        """Simulate expensive LLM call."""
        raise Exception("API unavailable")
    
    def cheap_fallback(prompt: str) -> str:
        """Cheap fallback when circuit is open."""
        return f"[FALLBACK] Cached/generic response for: {prompt[:30]}..."
    
    config = CircuitConfig(
        failure_threshold=1,
        timeout_duration=10.0,
        fallback_function=cheap_fallback
    )
    
    breaker = CircuitBreaker("fallback_demo", config)
    
    print("\n🔄 Testing with fallback...")
    
    # First call fails
    try:
        result = breaker.call(expensive_llm_call, "Test prompt")
        print(f"   Result: {result}")
    except Exception as e:
        breaker.record_failure()
        print(f"   First call: Failed and recorded")
    
    # Second call should trigger fallback
    print(f"\n   Circuit state: {breaker.get_state().name}")
    print("   Second call (should use fallback):")
    
    try:
        result = breaker.call(expensive_llm_call, "Test prompt 2")
        print(f"   Result: {result}")
    except CircuitBreakerOpen:
        print("   Circuit breaker triggered fallback")


def main():
    """Run all circuit breaker demos."""
    print("\n" + "="*60)
    print("CIRCUIT BREAKER PATTERN DEMONSTRATION")
    print("="*60)
    
    demo_basic_usage()
    demo_cost_protection()
    demo_decorator()
    demo_fallback()
    demo_llm_protection()
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)


if __name__ == "__main__":
    main()
