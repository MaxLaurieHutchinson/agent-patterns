# Circuit Breaker Architecture

## State Machine

```mermaid
stateDiagram-v2
    [*] --> CLOSED : Initialize
    CLOSED --> CLOSED : Success
    CLOSED --> OPEN : Failure threshold reached
    CLOSED --> OPEN : Cost threshold exceeded
    
    OPEN --> OPEN : Reject requests
    OPEN --> HALF_OPEN : Timeout expires
    
    HALF_OPEN --> CLOSED : Success threshold reached
    HALF_OPEN --> OPEN : Failure during test
    
    CLOSED --> [*] : Shutdown
    OPEN --> [*] : Shutdown
    HALF_OPEN --> [*] : Shutdown
```

## Component Diagram

```mermaid
classDiagram
    class CircuitBreaker {
        +state: CircuitState
        +failure_count: int
        +success_count: int
        +last_failure_time: float
        +config: CircuitConfig
        +call(func, *args, **kwargs)
        +record_success()
        +record_failure()
        +record_cost(amount)
        +get_state()
    }
    
    class CircuitConfig {
        +failure_threshold: int
        +success_threshold: int
        +timeout_duration: float
        +cost_threshold: float
        +rate_limit: int
        +half_open_max_calls: int
    }
    
    class CircuitState {
        <<enumeration>>
        CLOSED
        OPEN
        HALF_OPEN
    }
    
    class LLMWrapper {
        +circuit_breaker: CircuitBreaker
        +invoke(prompt)
        +fallback_strategy
    }
    
    class Metrics {
        +total_calls: int
        +rejected_calls: int
        +total_cost: float
        +avg_latency: float
        +get_stats()
    }
    
    CircuitBreaker --> CircuitConfig : uses
    CircuitBreaker --> CircuitState : tracks
    LLMWrapper --> CircuitBreaker : protects
    CircuitBreaker --> Metrics : updates
```

## Request Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Request Flow                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Request                                                    │
│     │                                                       │
│     ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Check Circuit State                                  │   │
│  │                                                      │   │
│  │ State = CLOSED? ──Yes──▶ Execute Request            │   │
│  │    │                                                 │   │
│  │    No                                                │   │
│  │    │                                                 │   │
│  │ State = HALF_OPEN? ──Yes──▶ Allow Limited           │   │
│  │    │                       Requests                  │   │
│  │    No                                                 │   │
│  │    │                                                 │   │
│  │ State = OPEN? ──Yes──▶ Reject Immediately           │   │
│  │                      Return Fallback / Error         │   │
│  └────────────────────┬────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Execute LLM Call                                     │   │
│  │                                                      │   │
│  │ Success? ──Yes──▶ Record Success                    │   │
│  │    │                        │                       │   │
│  │    │                        ▼                       │   │
│  │    │                 Check Success Threshold        │   │
│  │    │                 Reached? ──Yes──▶ Close Circuit│   │
│  │    │                                              │   │
│  │    No                                             │   │
│  │    │                                              │   │
│  │    ▼                                              │   │
│  │ Record Failure                                    │   │
│  │    │                                              │   │
│  │    ▼                                              │   │
│  │ Check Failure Threshold                           │   │
│  │ Reached? ──Yes──▶ Open Circuit                    │   │
│  │    │                        │                       │   │
│  │    No                        ▼                       │   │
│  │                    Start Timeout Timer              │   │
│  │                    Reject Future Requests           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Cost Protection Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 Cost Protection Mechanism                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Request                                                    │
│     │                                                       │
│     ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Check Cost Budget                                    │   │
│  │                                                      │   │
│  │ Current Cost: $45.50                                │   │
│  │ Budget Limit: $50.00                                │   │
│  │                                                      │   │
│  │ Estimate Request Cost: $2.00                        │   │
│  │                                                      │   │
│  │ $45.50 + $2.00 = $47.50 < $50.00 ──▶ ALLOW         │   │
│  │                                                      │   │
│  │ Would exceed? ──Yes──▶ REJECT                       │   │
│  │    │                           │                     │   │
│  │    │                           ▼                     │   │
│  │    │                   Return Quota Exceeded Error   │   │
│  │    │                                                   │   │
│  │    ▼                                                   │   │
│  │ Execute Request                                        │   │
│  │    │                                                   │   │
│  │    ▼                                                   │   │
│  │ Record Actual Cost: $1.85                              │   │
│  │ Update Running Total: $47.35                           │   │
│  │                                                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Time Window: Rolling 1-hour window                         │
│  Reset: Costs expire after window                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
