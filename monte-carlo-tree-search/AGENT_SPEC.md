# AGENT_SPEC

## Name
monte_carlo_tree_search

## Purpose
UCT-based selection with random rollouts.

## Inputs
- root state
- iterations

## Outputs
- best action

## Procedure
1. Select
2. Expand
3. Simulate
4. Backpropagate

## Example I/O Contract
```json
{
  "input": {},
  "output": {},
  "status": "ok"
}
```
