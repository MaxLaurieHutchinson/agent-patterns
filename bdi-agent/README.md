# BDI Agent

Maintains beliefs, generates desires, and commits to intentions deterministically.

## Core Concept

Beliefs, desires, intentions for goal-driven agents.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Needs clear priority rules
- Intentions can become stale

## When To Use
- You need explicit belief, desire, and intention separation
- Goals and priorities change based on new percepts
- You want transparent intention selection

## When Not To Use
- Behavior is purely reactive and stateless
- Continuous control dominates decision-making
- You need learned policies over large state spaces

## Failure Modes
- Stale beliefs leading to wrong intentions
- Desire conflicts without a clear tie-breaker
- Intention thrashing across steps

## Variants
- Commitment strategies for persistent intentions
- Utility-based intention selection

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#bdi-agent)
