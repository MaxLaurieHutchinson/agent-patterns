# State Machines (Plain Language)

## What It Is
Finite state machine with explicit transition table.

## When To Use
- When you need explicit transitions and handlers.

## When Not To Use
- When you need a different decision model

## Inputs
- current state
- event

## Outputs
- next state
- handler outputs

## Workflow
1. Lookup transition
2. Execute handler
3. Update state

## Minimal Example
Onboarding flow states.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected

## Common Pitfalls
- Forgetting default transitions
- Storing implicit state outside the FSM
- Letting state counts grow without pruning

## Further Reading
- [Harel, Statecharts: A Visual Formalism for Complex Systems](https://www.wisdom.weizmann.ac.il/~harel/SCANNED.PAPERS/Statecharts.pdf)
