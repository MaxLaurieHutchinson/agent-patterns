# Constraint Optimization (Plain Language)

## What It Is
Greedy knapsack heuristic for capacity constraints.

## When To Use
- When you need choose items under constraints.

## When Not To Use
- When you need a different decision model

## Inputs
- items
- capacity

## Outputs
- selected items
- total value

## Workflow
1. Sort by ratio
2. Select until capacity

## Minimal Example
Budgeted resource allocation.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected
