# OODA Loop

A deterministic decision loop that continuously updates context and acts.

## Core Concept

Observe, orient, decide, act in a tight decision cycle.

## This Repository's Starter

- `implementation.py` provides a minimal stdlib-only implementation.
- `example.py` demonstrates a small, deterministic demo.
- `PATTERN.md` and `AGENT_SPEC.md` provide plain-language and machine-readable guidance.

## Tradeoffs
- Requires well-defined stage functions
- Fast loops can amplify bad signals

## When To Use
- You need rapid observe-orient-decide-act cycles
- Decisions improve with frequent feedback
- You want a shared loop structure across teams

## When Not To Use
- Decisions are one-shot or batch only
- Observation latency dominates the loop
- The environment is effectively static

## Failure Modes
- Skipping orientation and acting on raw signals
- Repeating the loop without new observations
- Over-optimizing for speed at the expense of accuracy

## Variants
- Time-boxed loops with explicit stop criteria
- Nested loops at tactical and strategic levels

## Further Reading
- [John Boyd, A Discourse on Winning and Losing](https://www.airuniversity.af.edu/Portals/10/AUPress/Books/B_0151_Boyd_Discourse_Winning_Losing.PDF)
