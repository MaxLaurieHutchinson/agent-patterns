# Checkpoint + Resume (Plain Language)

## What It Is
A reliability pattern that writes progress to disk after each step and resumes later from that saved state.

## When To Use
- Long-running multi-step tasks.
- Jobs that can be interrupted by crashes/restarts.
- Systems that require deterministic recovery.

## When Not To Use
- Very short tasks.
- Workflows where full rerun is cheaper than checkpoint logic.

## Inputs
- Task id
- Ordered step list
- Checkpoint storage path

## Outputs
- Final result
- Persisted checkpoint history

## Workflow
1. Load existing checkpoint.
2. Start from next incomplete step.
3. Execute step.
4. Save checkpoint.
5. Continue until done.

## Failure Modes
- Corrupt checkpoint file.
- Non-idempotent steps causing duplicate side effects.

## Safety Guardrails
- Use atomic checkpoint writes.
- Prefer idempotent step design.
- Include task id and step index in every checkpoint.

## Minimal Example
Three steps run. Process stops after step 2. On restart, execution resumes at step 3.

## Evaluation Checklist
- [ ] Resumes from correct step index.
- [ ] Handles missing checkpoints safely.
- [ ] Does not rerun completed steps by default.
