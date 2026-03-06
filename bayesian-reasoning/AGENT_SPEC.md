# AGENT_SPEC

## Name
bayesian_reasoning

## Purpose
Uses Bayes rule to update probabilities for hypotheses.

## Inputs
- priors
- likelihoods
- evidence

## Outputs
- posterior distribution

## Procedure
1. Compute unnormalized posteriors
2. Normalize to sum to 1

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
