# MDP / POMDP (Plain Language)

## What It Is
Value iteration for MDP and belief updates for POMDP.

## When To Use
- When you need decision-making under uncertainty.

## When Not To Use
- When you need a different decision model

## Inputs
- states
- actions
- transitions
- rewards

## Outputs
- value function
- policy
- belief

## Workflow
1. Value iteration
2. Policy extraction
3. Belief update

## Minimal Example
Grid navigation with noisy sensors.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected

## Common Pitfalls
- Modeling an MDP when the system is partially observable
- Using poorly estimated transitions
- Ignoring belief normalization

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#mdp-pomdp)
