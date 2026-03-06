# AGENT_SPEC

## Name
ensemble_voting

## Purpose
Aggregates predictions via majority or weighted voting.

## Inputs
- predictions
- weights

## Outputs
- ensemble decision

## Procedure
1. Count votes
2. Apply weights
3. Return decision

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
