# Causal Reasoning (Plain Language)

## What It Is
Simple structural causal model with do-interventions.

## When To Use
- When you need interventions and counterfactuals.

## When Not To Use
- When you need a different decision model

## Inputs
- structural equations
- intervention

## Outputs
- intervention outcome
- counterfactual

## Workflow
1. Apply do()
2. Recompute downstream

## Minimal Example
Marketing lift vs baseline.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected

## Common Pitfalls
- Using causal claims without identifying assumptions
- Ignoring confounders and selection bias
- Confusing interventions with observations

## Further Reading
- [Pearl, Causality: Models, Reasoning, and Inference](https://www.cambridge.org/core/books/causality/36D1FE3B15B411C627E8FA3A48C7B0A9)
- [Pearl, Causality (online materials)](https://bayes.cs.ucla.edu/BOOK-2K/)
