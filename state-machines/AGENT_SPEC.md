# AGENT_SPEC

## Name
state_machines

## Purpose
Finite state machine with explicit transition table.

## Inputs
- current state
- event

## Outputs
- next state
- handler outputs

## Procedure
1. Lookup transition
2. Execute handler
3. Update state

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
