# Markov Models (Plain Language)

## What It Is
Uses transition matrices to sample next state and compute stationary distribution.

## When To Use
- When you need state transitions with probabilities.

## When Not To Use
- When you need a different decision model

## Inputs
- transition matrix
- current state

## Outputs
- next state
- stationary distribution

## Workflow
1. Sample next state
2. Iterate to estimate steady state

## Minimal Example
Weather transitions: sunny -> rainy.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected
