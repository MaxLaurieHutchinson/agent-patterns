# AGENT_SPEC

## Name
risk_scoring

## Purpose
Scores inputs and assigns low/medium/high risk bands.

## Inputs
- feature dict
- weights
- thresholds

## Outputs
- risk score
- risk band

## Procedure
1. Compute weighted sum
2. Assign band by thresholds

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
