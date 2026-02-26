# ReAct Loop (Plain Language)

## What It Is
ReAct is a loop where an agent alternates between thinking, taking an action, and reading the result of that action.

## When To Use
- You need tool calls during reasoning.
- You want a visible chain of decisions.
- You need iterative correction.

## When Not To Use
- The task is one-shot and simple.
- You need minimum latency.

## Inputs
- User request
- Tool catalog
- Current state/history

## Outputs
- Final answer
- Optional trace (thought/action/observation)

## Workflow
1. Generate next reasoning step.
2. Select a tool action or final answer.
3. Execute action and capture observation.
4. Repeat until complete or max iterations.

## Failure Modes
- Invalid tool call format.
- Tool output not parseable.
- Loop reaches max iterations without answer.

## Safety Guardrails
- Validate tool arguments.
- Restrict unsafe tools.
- Stop after configured iteration limit.

## Minimal Example
Question: "What is 123 * 456?"
1. Thought: "I should use calculator."
2. Action: `calculator(expression="123 * 456")`
3. Observation: `56088`
4. Final answer: `56088`

## Evaluation Checklist
- [ ] Produces correct final answer.
- [ ] Uses tools only when needed.
- [ ] Handles bad tool output safely.
- [ ] Stops within configured limits.
