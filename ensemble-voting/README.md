# Ensemble Voting

Aggregates predictions via majority or weighted voting.

## Core Concept

Combine multiple weak models.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Depends on base model quality
- Weights require tuning

## When To Use
- You have multiple models with complementary errors
- You need a simple way to improve robustness
- Interpretability is still important

## When Not To Use
- All models are highly correlated
- You need calibrated probabilities, not just labels
- The base models are unstable

## Failure Modes
- Tie-breaking bias in close votes
- Overweighting a weak model
- Overfitting when weights are tuned on small data

## Variants
- Bagging and boosting
- Stacking with a meta-learner
- Soft voting on probabilities

## Further Reading
- [Dietterich, Ensemble Methods in Machine Learning](https://link.springer.com/chapter/10.1007/3-540-45014-9_1)
