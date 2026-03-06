# State Machines

Finite state machine with explicit transition table.

## Core Concept

Explicit transitions and handlers.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Needs full transition coverage
- Can grow large

## When To Use
- Workflows have clear, discrete states
- You need explicit control over transitions
- You want deterministic behavior

## When Not To Use
- State space is continuous or very large
- Transitions are highly stochastic
- You need adaptive policies over time

## Failure Modes
- Missing transitions for edge events
- State explosion as features grow
- Hidden state stored outside the machine

## Variants
- Hierarchical state machines
- Statecharts with concurrency
- Event-driven reducers

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#state-machines)
