# Calibration / Abstain (Plain Language)

## What It Is
Applies thresholding to decide or abstain.

## When To Use
- When you need refuse low-confidence decisions.

## When Not To Use
- When you need a different decision model

## Inputs
- score
- threshold

## Outputs
- label or abstain

## Workflow
1. Compare score to threshold
2. Return label or abstain

## Minimal Example
Reject low-confidence classifications.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected

## Common Pitfalls
- Setting thresholds without calibration data
- Ignoring the abstain rate in evaluation
- Using a single threshold across segments

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#calibration-abstain)
