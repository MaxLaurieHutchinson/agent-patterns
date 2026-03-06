# Causal Reasoning

Simple structural causal model with do-interventions.

## Core Concept

Interventions and counterfactuals.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Simplified linear model
- Requires model assumptions

## When To Use
- You need to reason about interventions
- Counterfactuals matter for decision-making
- You can articulate causal structure

## When Not To Use
- You only need predictive associations
- Causal assumptions are unknown or disputed
- Data quality is too low for causal inference

## Failure Modes
- Wrong causal graph leads to wrong conclusions
- Unobserved confounders bias effects
- Treating correlations as causation

## Variants
- DAG-based causal inference
- Instrumental variable analysis
- Do-calculus with multiple interventions

## Further Reading
- [Pearl, Causality: Models, Reasoning, and Inference](https://www.cambridge.org/core/books/causality/36D1FE3B15B411C627E8FA3A48C7B0A9)
- [Pearl, Causality (online materials)](https://bayes.cs.ucla.edu/BOOK-2K/)
