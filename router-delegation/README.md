# Router + Delegation Pattern

The Router + Delegation pattern selects the best specialist agent for an incoming task, then delegates execution to that specialist.

## Core Concept

```
Task -> Router -> Specialist Agent -> Result
```

## Why This Pattern

- Avoids sending all tasks to one generalist.
- Makes behavior easier to reason about.
- Supports scaling with new specialists over time.

## This Repository's Starter

- `implementation.py` provides a rule-based router and delegation runtime.
- `example.py` demonstrates routing for coding, research, and writing tasks.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs

- Basic routing uses keyword rules, not semantic embeddings.
- Delegation runtime is in-process and synchronous by default.
