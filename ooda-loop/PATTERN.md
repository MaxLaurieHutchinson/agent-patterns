# OODA Loop (Plain Language)

## What It Is
A deterministic decision loop that continuously updates context and acts.

## When To Use
- When you need observe, orient, decide, act in a tight decision cycle.

## When Not To Use
- When you need a different decision model

## Inputs
- observe function
- orient function
- decide function
- act function

## Outputs
- decision trace
- final decision

## Workflow
1. Observe environment
2. Orient with context
3. Decide action
4. Act and repeat

## Minimal Example
Incident response loop that stabilizes a service.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected

## Common Pitfalls
- Treating orientation as optional
- Looping without a stopping condition
- Using stale observations to decide

## Further Reading
- [John Boyd, A Discourse on Winning and Losing](https://www.airuniversity.af.edu/Portals/10/AUPress/Books/B_0151_Boyd_Discourse_Winning_Losing.PDF)
