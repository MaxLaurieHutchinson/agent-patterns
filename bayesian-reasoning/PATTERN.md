# Bayesian Reasoning (Plain Language)

## What It Is
Uses Bayes rule to update probabilities for hypotheses.

## When To Use
- When you need update beliefs with evidence.

## When Not To Use
- When you need a different decision model

## Inputs
- priors
- likelihoods
- evidence

## Outputs
- posterior distribution

## Workflow
1. Compute unnormalized posteriors
2. Normalize to sum to 1

## Minimal Example
Diagnostic test with sensitivity/specificity.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected

## Common Pitfalls
- Using priors that are not justified
- Forgetting to normalize distributions
- Treating likelihoods as certainties

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#bayesian-reasoning)
