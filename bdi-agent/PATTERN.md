# BDI Agent (Plain Language)

## What It Is
Maintains beliefs, generates desires, and commits to intentions deterministically.

## When To Use
- When you need beliefs, desires, intentions for goal-driven agents.

## When Not To Use
- When you need a different decision model

## Inputs
- percepts
- belief store
- desire generators

## Outputs
- current intention
- updated beliefs

## Workflow
1. Update beliefs
2. Generate desires
3. Select intention
4. Execute intention

## Minimal Example
Assistant chooses to schedule a meeting based on inbox signals.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected
