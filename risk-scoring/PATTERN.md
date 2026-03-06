# Risk Scoring (Plain Language)

## What It Is
Scores inputs and assigns low/medium/high risk bands.

## When To Use
- When you need weighted scoring with thresholds.

## When Not To Use
- When you need a different decision model

## Inputs
- feature dict
- weights
- thresholds

## Outputs
- risk score
- risk band

## Workflow
1. Compute weighted sum
2. Assign band by thresholds

## Minimal Example
Transaction risk labeling.

## Evaluation Checklist
- [ ] Produces expected output
- [ ] Handles invalid input safely
- [ ] Is deterministic where expected

## Common Pitfalls
- Using thresholds without calibration data
- Ignoring missing or sparse features
- Treating the score as a probability

## Further Reading
- See [DECISION_MODEL_READINGS.md](../DECISION_MODEL_READINGS.md#risk-scoring)
