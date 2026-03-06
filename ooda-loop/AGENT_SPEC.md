# AGENT_SPEC

## Name
ooda_loop

## Purpose
A deterministic decision loop that continuously updates context and acts.

## Inputs
- observe function
- orient function
- decide function
- act function

## Outputs
- decision trace
- final decision

## Procedure
1. Observe environment
2. Orient with context
3. Decide action
4. Act and repeat

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
