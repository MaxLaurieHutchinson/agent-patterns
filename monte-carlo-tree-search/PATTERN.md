# Monte Carlo Tree Search (Plain Language)

## What It Is
UCT-based selection with random rollouts.

## When To Use
- When you need search via stochastic rollouts.

## When Not To Use
- When you need a different decision model

## Inputs
- root state
- iterations

## Outputs
- best action

## Workflow
1. Select
2. Expand
3. Simulate
4. Backpropagate

## Minimal Example
Take-away game.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected
