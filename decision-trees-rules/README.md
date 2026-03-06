# Decision Trees / Rules

Evaluates ordered rules with first-match wins.

## Core Concept

Rule-based decisions.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Brittle rules
- Needs maintenance

## When To Use
- You need transparent, auditable decisions
- Inputs map to clear, discrete outcomes
- Order of rules is meaningful

## When Not To Use
- You need probabilistic outputs
- Rules change frequently without governance
- The decision boundary is highly complex

## Failure Modes
- Rule conflicts or unexpected overlaps
- Order dependence hiding better matches
- Rule sprawl over time

## Variants
- Decision trees (CART, ID3)
- Rule lists with scoring
- Decision tables

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#decision-trees-rules)
