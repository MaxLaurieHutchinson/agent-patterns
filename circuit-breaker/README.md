# Circuit Breaker Pattern

The Circuit Breaker pattern prevents cascading failures by stopping requests when error rates or costs exceed thresholds. Essential for production LLM systems.

## Core Concept

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  CLOSED │────▶│  OPEN   │────▶│ HALF-OPEN│
│ (normal)│     │ (failing)│     │ (testing)│
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     │ Failure       │ Timeout       │ Success
     │ threshold     │ expires       │ threshold
     ▼               ▼               ▼
  Open circuit    Try test      Close circuit
```

The circuit has three states:
- **CLOSED** - Normal operation, requests pass through
- **OPEN** - Failing fast, requests rejected immediately
- **HALF-OPEN** - Testing if service recovered

## When to Use

### ✅ Use Circuit Breaker When:
- Production systems with external LLM calls
- Cost-sensitive applications
- High-availability requirements
- Preventing cascading failures
- Protecting against rate limits
- Handling intermittent API issues

### ❌ Don't Use When:
- Prototypes or internal tools
- Systems where every request must be attempted
- No external dependencies

## Key Benefits

1. **Fail Fast** - Don't waste time on failing calls
2. **Cost Control** - Stop expensive LLM calls when failing
3. **System Resilience** - Prevent cascading failures
4. **Graceful Degradation** - Can fallback to alternatives
5. **Recovery Detection** - Automatically test recovery

## Thresholds and Configuration

- **Failure Threshold** - Number of failures before opening
- **Success Threshold** - Successes needed to close from half-open
- **Timeout Duration** - How long to stay open before testing
- **Cost Threshold** - Maximum spend per time window
- **Rate Limit** - Maximum requests per second

## Related Patterns

- **Retry Pattern** - Often combined with circuit breaker
- **Fallback Pattern** - Alternative when circuit is open
- **Bulkhead Pattern** - Isolate different failure domains
- **Observer Pattern** - Monitor circuit state changes
