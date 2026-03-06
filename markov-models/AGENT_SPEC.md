# AGENT_SPEC

## Name
markov_models

## Purpose
Uses transition matrices to sample next state and compute stationary distribution.

## Inputs
- transition matrix
- current state

## Outputs
- next state
- stationary distribution

## Procedure
1. Sample next state
2. Iterate to estimate steady state

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
