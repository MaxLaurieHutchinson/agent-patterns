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
- [Von Neumann & Morgenstern, Theory of Games and Economic Behavior](https://press.princeton.edu/books/hardcover/9780691130613/theory-of-games-and-economic-behavior)
- [Expected Utility Theory (Cambridge Elements)](https://www.cambridge.org/core/elements/expected-utility-theory/0568AA577C9CF77F402491BCEFA1AA9D)
