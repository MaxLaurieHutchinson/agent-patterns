# AGENT_SPEC

## Name
bdi_agent

## Purpose
Maintains beliefs, generates desires, and commits to intentions deterministically.

## Inputs
- percepts
- belief store
- desire generators

## Outputs
- current intention
- updated beliefs

## Procedure
1. Update beliefs
2. Generate desires
3. Select intention
4. Execute intention

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
