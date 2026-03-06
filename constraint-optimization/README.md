# Constraint Optimization

Greedy knapsack heuristic for capacity constraints.

## Core Concept

Choose items under constraints.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Not optimal
- Heuristic only

## When To Use
- You need a fast, simple approximation
- Items have positive weights and values
- Capacity constraints are hard limits

## When Not To Use
- You need optimal solutions
- Negative or zero weights appear
- The problem has complex dependencies

## Failure Modes
- Greedy ratio yields suboptimal picks
- Invalid weights cause undefined ratios
- Over-reliance on a single heuristic

## Variants
- Dynamic programming knapsack
- Branch-and-bound search
- Integer programming solvers

## Further Reading
- [Kellerer, Pferschy, Pisinger: Knapsack Problems](https://link.springer.com/book/10.1007/978-3-540-24777-7)
