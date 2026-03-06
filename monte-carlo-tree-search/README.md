# Monte Carlo Tree Search

UCT-based selection with random rollouts.

## Core Concept

Search via stochastic rollouts.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Non-deterministic
- Needs many rollouts

## When To Use
- Search space is large and exact search is expensive
- You can simulate outcomes cheaply
- You need anytime performance (more iterations improve quality)

## When Not To Use
- Exact solutions are available and fast
- Rollouts are too expensive to simulate
- You need strict determinism

## Failure Modes
- Poor rollout policy yields weak guidance
- Too few iterations causes unstable choices
- Rollouts that never terminate (use max depth)

## Variants
- UCT with domain heuristics
- Progressive widening for large branching
- Neural-guided rollouts

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#monte-carlo-tree-search)
