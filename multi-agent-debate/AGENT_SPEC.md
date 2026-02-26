# AGENT_SPEC

## Name
multi_agent_debate

## Purpose
Improve answer quality through role-based multi-agent critique and synthesis.

## Inputs
- `query` (string, required)
- `agents` (array, required): role, prompt, model
- `max_rounds` (integer, optional)
- `cost_limit` (number, optional)

## Outputs
- `debate_history` (array)
- `consensus_reached` (boolean)
- `final_answer` (string)

## Preconditions
- At least one speaking agent exists.
- Synthesis role exists or fallback is defined.

## Procedure
1. Initialize round state and transcript.
2. Run one round of speaking agents.
3. Update cost estimate.
4. Evaluate consensus/termination conditions.
5. Synthesize and optionally judge final answer.

## Safety Rules
- Enforce `max_rounds` and `cost_limit`.
- Keep prompts scoped to task context.
- Persist transcript for traceability.

## Failure Handling
- If no judge role is present, fallback to synthesized answer.
- If synthesis role missing, fallback to first available agent.

## Telemetry
- rounds completed
- agent turn count
- estimated cost
- consensus flag

## Example I/O Contract
```json
{
  "input": {"query": "Should we cache this endpoint?"},
  "output": {"final_answer": "...", "consensus_reached": false},
  "status": "ok"
}
```
