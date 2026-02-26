# Reflection + Verifier (Plain Language)

## What It Is
An answer quality loop where one component produces an answer and another checks it.

## When To Use
- Correctness matters.
- You can define explicit acceptance checks.
- You need a lightweight self-correction loop.

## When Not To Use
- Open-ended creative tasks without objective checks.
- Ultra-low latency workflows.

## Inputs
- Task/query
- Solver
- Verifier
- Retry limit

## Outputs
- Final answer
- Verification report
- Attempt history

## Workflow
1. Solver creates draft.
2. Verifier evaluates draft.
3. If failed, provide feedback to solver.
4. Repeat until pass or max attempts.

## Failure Modes
- Verifier is too weak or inconsistent.
- Solver ignores feedback.

## Safety Guardrails
- Cap attempts.
- Keep verifier independent from solver prompt where possible.

## Minimal Example
Solver says "2+2=5". Verifier rejects and asks to recompute. Solver revises to "4".

## Evaluation Checklist
- [ ] Verifier catches known bad outputs.
- [ ] Feedback improves next draft.
- [ ] Loop stops at max attempts.
