# AGENT_SPEC

## Name
causal_reasoning

## Purpose
Simple structural causal model with do-interventions.

## Inputs
- structural equations
- intervention

## Outputs
- intervention outcome
- counterfactual

## Procedure
1. Apply do()
2. Recompute downstream

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
