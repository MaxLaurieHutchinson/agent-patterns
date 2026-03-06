# Ensemble Voting (Plain Language)

## What It Is
Aggregates predictions via majority or weighted voting.

## When To Use
- When you need combine multiple weak models.

## When Not To Use
- When you need a different decision model

## Inputs
- predictions
- weights

## Outputs
- ensemble decision

## Workflow
1. Count votes
2. Apply weights
3. Return decision

## Minimal Example
Combine three classifiers.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected
