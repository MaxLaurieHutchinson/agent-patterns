# AGENT_SPEC

## Name
plan_and_execute

## Purpose
Decompose a complex task into steps and execute them reliably.

## Inputs
- `task` (string, required)
- `execution_strategy` (string, optional): `sequential|parallel|dynamic`
- `max_replans` (integer, optional)

## Outputs
- `plan` (object)
- `results` (map step_id -> result)
- `final_answer` (string)

## Preconditions
- Planner and executor LLMs are available.
- Tool registry is initialized if tools are used.

## Procedure
1. Build initial plan from task.
2. Execute next eligible step(s) based on strategy.
3. Persist per-step status/result/error.
4. If failures exist and replans remain, enter replan node.
5. Finalize response from accumulated results.

## Safety Rules
- Reject unresolved dependency graphs.
- Bound replan count.
- Mark failed steps without aborting whole state machine when possible.

## Failure Handling
- Step exceptions become `FAILED` status with error text.
- If finalization happens with failures, return explicit incomplete summary.

## Telemetry
- step success/failure counts
- replan count
- execution strategy used

## Example I/O Contract
```json
{
  "input": {"task": "Research X and summarize"},
  "output": {"final_answer": "...", "results": {"step_1": "..."}},
  "status": "ok"
}
```
