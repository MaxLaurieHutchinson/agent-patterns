# Router + Delegation (Plain Language)

## What It Is
A front-door router chooses which specialist should handle each request.

## When To Use
- You have multiple specialists.
- Different tasks need different prompts/tools.

## When Not To Use
- One specialist handles all tasks well.
- Routing overhead exceeds benefit.

## Inputs
- User query
- Routing rules or classifier
- Specialist registry

## Outputs
- Chosen specialist
- Specialist response

## Workflow
1. Classify task intent.
2. Select specialist.
3. Delegate request with context.
4. Return result and routing metadata.

## Failure Modes
- Misrouting from weak intent rules.
- Missing specialist for chosen intent.

## Safety Guardrails
- Always define fallback specialist.
- Log route decisions for auditing.

## Minimal Example
"Draft a launch post" routes to writer agent, not research or coding agent.

## Evaluation Checklist
- [ ] Correct routing on representative tasks.
- [ ] Fallback activates on unknown intents.
- [ ] Route decision is observable.
