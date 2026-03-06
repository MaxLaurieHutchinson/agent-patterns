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

## Common Pitfalls
- Treating a heuristic as optimal
- Allowing zero or negative weights
- Ignoring alternative heuristics for skewed data

## Further Reading
- [Kellerer, Pferschy, Pisinger: Knapsack Problems](https://link.springer.com/book/10.1007/978-3-540-24777-7)
