# Reflection + Verifier Pattern

Reflection + Verifier adds a quality loop: generate a draft answer, verify it independently, and revise until it passes or retry limits are reached.

## Core Concept

```
Draft -> Verify -> (Pass -> Return) or (Fail -> Reflect and Revise)
```

## Why This Pattern

- Reduces obvious reasoning mistakes.
- Makes correctness checks explicit.
- Improves reliability for factual or constrained outputs.

## This Repository's Starter

- `implementation.py` provides a small reflection-verification loop.
- `example.py` shows a first-fail then corrected-pass flow.
