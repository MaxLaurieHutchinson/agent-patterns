# Calibration / Abstain

Applies thresholding to decide or abstain.

## Core Concept

Refuse low-confidence decisions.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Requires calibration
- May abstain too often

## When To Use
- You can measure confidence scores
- The cost of wrong answers is high
- You have a fallback path for abstains

## When Not To Use
- You must always return a decision
- Confidence scores are uncalibrated
- Abstains create unacceptable latency

## Failure Modes
- Thresholds tuned on outdated data
- Distribution shift causing under/over abstain
- Treating scores as calibrated probabilities

## Variants
- Temperature scaling before thresholding
- Selective classification with coverage targets
- Conformal prediction for abstain sets

## Further Reading
- [Guo et al., On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html)
- [Fumera et al., Classification with Rejection](https://proceedings.mlr.press/v119/fumera20a.html)
