# Risk Scoring

Scores inputs and assigns low/medium/high risk bands.

## Core Concept

Weighted scoring with thresholds.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Heuristic thresholds
- Requires calibration

## When To Use
- You need quick, explainable risk tiers
- A weighted scorecard is acceptable
- Outputs must be easy to audit

## When Not To Use
- Non-linear interactions dominate outcomes
- Thresholds cannot be reliably calibrated
- You need fully probabilistic estimates

## Failure Modes
- Stale weights after distribution shifts
- Thresholds tuned on small or biased samples
- Missing features treated as zero

## Variants
- Scorecards with binned features
- Logistic-regression-based scores
- Calibrated probability outputs

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#risk-scoring)
