# Logistic Regression (Plain Language)

## What It Is
Trains a binary classifier using gradient descent (stdlib only).

## When To Use
- When you need simple probabilistic classifier.

## When Not To Use
- When you need a different decision model

## Inputs
- X features
- y labels
- learning rate
- epochs

## Outputs
- model weights
- predicted probabilities

## Workflow
1. Initialize weights
2. Gradient descent updates
3. Predict via sigmoid

## Minimal Example
Toy spam classifier.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected

## Common Pitfalls
- Skipping feature scaling
- Training with too few epochs
- Using a fixed threshold when costs are asymmetric

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#logistic-regression)
