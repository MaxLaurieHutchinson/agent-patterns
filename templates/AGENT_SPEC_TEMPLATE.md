# AGENT_SPEC

## Name
pattern_name

## Purpose
One sentence objective for an autonomous runtime.

## Inputs
- `input_name`: type, required/optional, description

## Outputs
- `output_name`: type, description

## Preconditions
- Required environment assumptions
- Required tools/dependencies

## Procedure
1. Validate inputs.
2. Execute core steps in order.
3. Apply safety checks before side effects.
4. Return structured result.

## Safety Rules
- Never perform destructive actions without explicit authorization.
- Reject malformed or out-of-policy actions.
- Enforce scope boundaries (files, network, or APIs).

## Failure Handling
- Define retry policy.
- Define fallback behavior.
- Return explicit error states.

## Telemetry
- Emit key metrics and status transitions.
- Include correlation identifiers where possible.

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
