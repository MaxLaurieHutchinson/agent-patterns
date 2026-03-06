# Bayesian Reasoning

Uses Bayes rule to update probabilities for hypotheses.

## Core Concept

Update beliefs with evidence.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Requires valid priors
- Sensitive to likelihood estimates

## When To Use
- You need to update beliefs as evidence arrives
- You want explicit uncertainty tracking
- You can articulate priors and likelihoods

## When Not To Use
- Priors or likelihoods are unavailable or untrusted
- Simple threshold rules are sufficient
- You need purely frequentist estimates

## Failure Modes
- Overconfident priors dominating evidence
- Likelihoods that do not match reality
- Numerical collapse when evidence is near zero

## Variants
- Conjugate priors for closed-form updates
- Hierarchical models for shared structure
- Approximate inference (sampling or variational)

## Further Reading
- [E. T. Jaynes, Probability Theory: The Logic of Science](https://bayes.wustl.edu/etj/prob/book.pdf)
- [Gelman et al., Bayesian Data Analysis](https://sites.stat.columbia.edu/gelman/book/)
