# Logistic Regression

Trains a binary classifier using gradient descent (stdlib only).

## Core Concept

Simple probabilistic classifier.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Not optimized for large datasets
- No regularization by default

## When To Use
- You need a simple, interpretable binary classifier
- Probabilities are useful for ranking or thresholding
- Data is small to medium and mostly linearly separable

## When Not To Use
- Decision boundary is highly non-linear
- You need multi-class without extensions
- Strong regularization is required for stability

## Failure Modes
- Feature scaling issues leading to slow convergence
- Class imbalance causing biased predictions
- Perfect separation driving weights to extremes

## Variants
- L1/L2 regularized logistic regression
- Multinomial (softmax) regression
- Stochastic gradient descent

## Further Reading
- [Hastie, Tibshirani, Friedman: The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/)
