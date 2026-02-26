# AGENT_SPEC

## Name
checkpoint_resume

## Purpose
Persist workflow progress and resume safely after interruption.

## Inputs
- `task_id` (string, required)
- `steps` (array of callables, required)
- `checkpoint_path` (string, required)

## Outputs
- `status` (string): `in_progress|completed|failed`
- `last_step_index` (integer)
- `data` (object)

## Preconditions
- Checkpoint directory is writable.
- Steps are deterministic or idempotent where possible.

## Procedure
1. Load checkpoint if present.
2. Determine next step index.
3. Execute step and update state.
4. Save checkpoint after each step.
5. Mark completed when final step succeeds.

## Safety Rules
- Never discard existing checkpoint without explicit request.
- Use atomic file replace on writes.

## Failure Handling
- On step failure, save failure state and error context.
- Return resumable state for later retry.

## Telemetry
- resume count
- checkpoint write count
- failed step index
