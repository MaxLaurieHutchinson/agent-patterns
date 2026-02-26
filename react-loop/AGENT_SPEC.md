# AGENT_SPEC

## Name
react_loop

## Purpose
Solve tasks by interleaving reasoning with tool actions.

## Inputs
- `query` (string, required): user task.
- `tools` (array, required): callable tool definitions.
- `max_iterations` (integer, optional): loop limit.

## Outputs
- `final_answer` (string or null)
- `thoughts` (array of strings)
- `actions` (array of objects)
- `observations` (array of strings)

## Preconditions
- Tools are registered and callable.
- LLM can follow the response format.

## Procedure
1. Build prompt with tool descriptions.
2. Ask model for next `Thought` and `Action` or `Final Answer`.
3. If action exists, parse and execute tool call.
4. Add observation to context.
5. Repeat until final answer or max iterations.

## Safety Rules
- Reject unknown tools.
- Bound loop by `max_iterations`.
- Sanitize parsed arguments before tool invoke.

## Failure Handling
- On parse failure, append error observation and continue.
- On tool failure, append error observation and continue.
- If no final answer after limit, return partial trace.

## Telemetry
- `step_count`
- tool call count
- tool error count

## Example I/O Contract
```json
{
  "input": {"query": "What is 2+2?"},
  "output": {"final_answer": "4", "actions": [{"tool": "calculator", "args": {"expression": "2+2"}}]},
  "status": "ok"
}
```
