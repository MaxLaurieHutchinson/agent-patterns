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
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#causal-reasoning)
