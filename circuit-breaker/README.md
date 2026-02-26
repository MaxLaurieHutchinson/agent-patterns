# Circuit Breaker Pattern

The Circuit Breaker pattern prevents cascading failures by stopping requests when error rates or costs exceed thresholds. It is especially useful for production LLM and tool-calling systems.

## Core Concept

```
CLOSED -> OPEN -> HALF-OPEN -> CLOSED
```

The circuit has three states:
- **CLOSED** - Normal operation, requests pass through
- **OPEN** - Failing fast, requests rejected immediately
- **HALF-OPEN** - Testing whether the dependency recovered

## When to Use

### ✅ Use Circuit Breaker When:
- Production systems with external LLM calls
- Cost-sensitive applications
- High-availability requirements
- Preventing cascading failures
- Protecting against provider rate limits
- Handling intermittent API issues

### ❌ Don't Use When:
- Prototypes or internal tools
- Systems where every request must be attempted
- No external dependencies

## Key Benefits

1. **Fail Fast** - Avoid repeated expensive failures
2. **Cost Control** - Enforce budget windows
3. **System Resilience** - Reduce blast radius of dependency outages
4. **Graceful Degradation** - Fallback behavior when open
5. **Recovery Detection** - Half-open probing for restoration

## This Repository's Implementation

- Core implementation: `implementation.py`
- Demo script: `example.py`
- Includes failure thresholds, timeouts, rate limiting, and cost windows
- Tracks state transitions and call metrics

### Current Notes

- Success/failure counts are tracked internally; `call()` already records success/failure outcomes.
- `record_cost()` is explicit so actual known cost can be added after a call.
- Fallback behavior is optional via `fallback_function` in `CircuitConfig`.

## Related Patterns

- **Retry Pattern** - Often paired with circuit breaker
- **Fallback Pattern** - Alternative path while open
- **Bulkhead Pattern** - Isolate different failure domains
- **Observer Pattern** - Publish circuit state changes
