# MDP / POMDP

Value iteration for MDP and belief updates for POMDP.

## Core Concept

Decision-making under uncertainty.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Small state spaces only
- Simplified belief update

## When To Use
- Sequential decision-making with known dynamics
- You can define rewards and transitions
- Partial observability can be modeled with beliefs

## When Not To Use
- State space is huge or continuous
- Dynamics are unknown or changing rapidly
- Real-time constraints prevent iteration

## Failure Modes
- State explosion and slow convergence
- Inaccurate transition or observation models
- Belief collapse to incorrect states

## Variants
- Policy iteration or Q-learning
- Point-based value iteration for POMDPs
- Particle-filter belief updates

## Further Reading
- [Sutton & Barto, Reinforcement Learning (2nd ed.)](http://incompleteideas.net/book/bookdraft2016sep.pdf)
- [Kaelbling, Littman, Cassandra, Planning in POMDPs](https://people.csail.mit.edu/lpk/papers/aij98.pdf)
