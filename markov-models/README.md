# Markov Models

Uses transition matrices to sample next state and compute stationary distribution.

## Core Concept

State transitions with probabilities.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Requires normalized probabilities
- Assumes Markov property

## When To Use
- State transitions are approximately memoryless
- You can estimate transition probabilities
- You need a simple stochastic sequence model

## When Not To Use
- Long-range history matters
- Dynamics are highly non-stationary
- You need continuous or high-dimensional states

## Failure Modes
- Poor estimates for rare transitions
- Transition rows that do not sum to 1
- Absorbing states introduced unintentionally

## Variants
- Higher-order Markov chains
- Hidden Markov Models (HMMs)
- Time-inhomogeneous transitions

## Further Reading
- [Grinstead & Snell, Introduction to Probability (Markov chains)](https://math.dartmouth.edu/~prob/prob/prob.pdf)
