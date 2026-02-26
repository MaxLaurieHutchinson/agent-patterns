# AGENT_SPEC

## Name
circuit_breaker

## Purpose
Protect dependent calls with fail-fast state transitions, budget controls, and optional fallback.

## Inputs
- `callable` (function, required)
- `args/kwargs` (optional)
- `cost_estimate` (number, optional)
- `config` (object, required)

## Outputs
- `result` (any) or `CircuitBreakerOpen` error
- `metrics` (object)

## Preconditions
- Configuration thresholds are valid.
- Optional fallback is callable and side-effect safe.

## Procedure
1. Acquire lock and evaluate budget/rate/state.
2. Reject or fallback if blocked.
3. Count attempted call.
4. Execute protected callable outside lock.
5. Record success/failure and transition state.

## Safety Rules
- Keep state transitions under lock.
- Enforce explicit rate and budget limits.
- Never bypass open-state checks.

## Failure Handling
- Raise `CircuitBreakerOpen` for blocked calls.
- On callable exception, record failure then re-raise.
- Expose metrics for operational debugging.

## Telemetry
- total/success/failed/rejected calls
- current state and transition history
- window cost and budget

## Example I/O Contract
```json
{
  "input": {"cost_estimate": 0.01},
  "output": {"state": "CLOSED", "result": "ok"},
  "status": "ok"
}
```
