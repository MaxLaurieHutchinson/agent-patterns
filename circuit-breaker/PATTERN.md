# Circuit Breaker (Plain Language)

## What It Is
A reliability guard that stops calling a failing dependency for a cooldown period, then probes recovery.

## When To Use
- External APIs fail intermittently.
- You need spend and rate protection.
- You need fail-fast behavior.

## When Not To Use
- Prototype scripts where complexity is unnecessary.
- Flows where every call must be attempted.

## Inputs
- Protected function call
- Threshold configuration
- Optional fallback function

## Outputs
- Function result or rejection error
- Metrics and state transitions

## Workflow
1. Check budget/rate and state.
2. In `OPEN`, reject or fallback.
3. In `HALF_OPEN`, allow limited probes.
4. Record success/failure and transition state.

## Failure Modes
- Thresholds tuned too strict or too loose.
- Missing cost recording causes budget drift.
- Fallback path quality is poor.

## Safety Guardrails
- Enforce rate limits and cost windows.
- Keep call metrics thread-safe.
- Use clear fallback semantics.

## Minimal Example
- After 3 failures, circuit opens.
- Calls are rejected for 60 seconds.
- One successful probe in half-open can close circuit (per threshold config).

## Evaluation Checklist
- [ ] Opens at failure threshold.
- [ ] Rejects while open.
- [ ] Recovers through half-open probes.
- [ ] Tracks call metrics accurately.
