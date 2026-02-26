# Tool Use (MCP Style) (Plain Language)

## What It Is
A standardized tool layer where an agent discovers tools, validates arguments, executes calls, and returns structured results.

## When To Use
- You have multiple external tools.
- You want a common interface for tool calling.
- You need validation and consistent error handling.

## When Not To Use
- You only need one direct function call.
- Dynamic discovery is unnecessary.

## Inputs
- Tool name
- Parameter payload
- Tool registry manifest

## Outputs
- Structured tool result (`success`, `data/error`, timing)

## Workflow
1. Register tools with schemas.
2. Expose manifest to the model.
3. Parse requested tool call.
4. Validate parameters against schema.
5. Execute tool and return structured result.

## Failure Modes
- Invalid parameter types.
- Unknown tool name.
- Unsafe filesystem/path usage.

## Safety Guardrails
- Validate required fields and types.
- Restrict filesystem scope to a configured base path.
- Return explicit errors rather than silent failures.

## Minimal Example
- Model returns: `TOOL_CALL: calculator(expression="15*4")`
- Registry executes and returns `{result: 60}`
- Agent converts tool output to response context.

## Evaluation Checklist
- [ ] Unknown tools fail cleanly.
- [ ] Validation catches bad arguments.
- [ ] Filesystem access is scoped.
- [ ] Tool results are structured and parseable.
