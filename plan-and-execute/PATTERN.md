# Plan-and-Execute (Plain Language)

## What It Is
The agent first creates a plan, then executes steps from that plan. This separates strategy from execution.

## When To Use
- Tasks have clear substeps.
- Some steps can run in parallel.
- You want progress visibility.

## When Not To Use
- The task changes every second.
- Planning cost is higher than execution cost.

## Inputs
- High-level task
- Available tools/models
- Execution strategy (sequential, parallel, dynamic)

## Outputs
- Plan with step statuses
- Step results
- Final synthesized answer

## Workflow
1. Planner generates structured steps with dependencies.
2. Executor runs eligible steps.
3. Capture outputs/errors for each step.
4. Replan when needed (dynamic mode).
5. Synthesize final answer from completed work.

## Failure Modes
- Plan parser cannot parse model output.
- Dependency graph has cycles.
- A step fails repeatedly.

## Safety Guardrails
- Validate dependencies before execution.
- Mark failures explicitly, do not hide them.
- Limit replans and total execution loops.

## Minimal Example
Task: "Write blog post outline"
1. Plan: research topic -> draft sections -> finalize outline.
2. Execute each step.
3. Return consolidated outline.

## Evaluation Checklist
- [ ] Produces valid step graph.
- [ ] Correctly handles step failures.
- [ ] Respects dependency ordering.
- [ ] Returns final answer or explicit incomplete status.
