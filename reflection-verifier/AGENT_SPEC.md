# AGENT_SPEC

## Name
reflection_verifier

## Purpose
Improve output quality by iterating draft generation with independent verification.

## Inputs
- `query` (string, required)
- `max_attempts` (integer, optional)

## Outputs
- `final_answer` (string)
- `passed` (boolean)
- `attempts` (array)

## Preconditions
- Solver callable is available.
- Verifier callable returns deterministic pass/fail and feedback.

## Procedure
1. Generate draft with current feedback context.
2. Run verifier on draft.
3. If pass, return result.
4. If fail, append feedback and retry.
5. Return best-effort result after max attempts.

## Safety Rules
- Enforce maximum attempts.
- Keep feedback short and actionable.

## Failure Handling
- If solver or verifier throws, return structured failure state.

## Telemetry
- attempts used
- pass/fail rate
- common failure reasons
