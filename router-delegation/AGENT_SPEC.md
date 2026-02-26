# AGENT_SPEC

## Name
router_delegation

## Purpose
Route tasks to the most appropriate specialist and execute them.

## Inputs
- `query` (string, required)
- `context` (object, optional)

## Outputs
- `selected_agent` (string)
- `intent` (string)
- `result` (any)

## Preconditions
- Specialist handlers are registered.
- Router has rules or classifier.

## Procedure
1. Infer intent from query.
2. Choose target agent by intent.
3. Delegate query/context to selected handler.
4. Return structured result with route metadata.

## Safety Rules
- If no route matches, use default fallback agent.
- Never drop a request silently.

## Failure Handling
- If specialist fails, return structured error with agent name.

## Telemetry
- route distribution by intent
- fallback rate
- per-agent success/failure
