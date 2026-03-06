# Decision Trees / Rules (Plain Language)

## What It Is
Evaluates ordered rules with first-match wins.

## When To Use
- When you need rule-based decisions.

## When Not To Use
- When you need a different decision model

## Inputs
- rules
- input record

## Outputs
- matched rule
- decision

## Workflow
1. Iterate rules
2. Return first match

## Minimal Example
Support ticket routing.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected
