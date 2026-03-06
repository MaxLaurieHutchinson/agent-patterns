# Expected Utility

Computes expected utility over outcomes and selects max.

## Core Concept

Choose option with highest expected value.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Assumes utilities are comparable
- Depends on probability quality

## When To Use
- You can enumerate outcomes and probabilities
- Utilities are on a common scale
- You want a transparent decision rule

## When Not To Use
- Preferences are non-linear or inconsistent
- Outcomes are not independent
- Utilities are hard to quantify

## Failure Modes
- Miscalibrated probabilities dominating choice
- Utility scales that hide important tradeoffs
- Ignoring constraints or risk appetite

## Variants
- Multi-attribute utility
- Prospect theory (loss aversion)
- Risk-adjusted utility

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#expected-utility)
