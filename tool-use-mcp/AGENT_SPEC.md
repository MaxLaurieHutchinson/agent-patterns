# AGENT_SPEC

## Name
mcp_tool_registry

## Purpose
Provide a schema-driven, safe execution path for model-initiated tool calls.

## Inputs
- `tool_name` (string)
- `parameters` (object)
- `tool_call_string` (optional string form)

## Outputs
- `ToolResult` object: `call_id`, `success`, `data/error`, `duration_ms`

## Preconditions
- Tool is registered.
- Tool schema is available.

## Procedure
1. Resolve tool by name.
2. Validate input parameters.
3. Execute tool implementation.
4. Catch execution exceptions and wrap as structured error.
5. Append call/result to history.

## Safety Rules
- Reject unknown tools.
- Enforce schema validation.
- For filesystem operations, block path traversal outside `base_path`.

## Failure Handling
- Validation failures return `success=false` with clear reason.
- Execution errors return `success=false` and preserve `call_id`.

## Telemetry
- call duration
- success/failure rate
- per-tool usage

## Example I/O Contract
```json
{
  "input": {"tool_name": "search", "parameters": {"query": "python"}},
  "output": {"success": true, "data": {"results": ["..."]}},
  "status": "ok"
}
```
