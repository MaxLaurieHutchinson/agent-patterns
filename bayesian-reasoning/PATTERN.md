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
- [E. T. Jaynes, Probability Theory: The Logic of Science](https://bayes.wustl.edu/etj/prob/book.pdf)
- [Gelman et al., Bayesian Data Analysis](https://sites.stat.columbia.edu/gelman/book/)
