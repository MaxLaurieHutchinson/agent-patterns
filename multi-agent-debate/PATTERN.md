# Multi-Agent Debate (Plain Language)

## What It Is
Multiple agents with different roles discuss the same problem, then synthesize a stronger final answer.

## When To Use
- You want multiple perspectives.
- You need structured critique before deciding.
- Quality matters more than minimal cost.

## When Not To Use
- The task is simple.
- You have strict latency or budget limits.

## Inputs
- Original question
- Agent roster and role prompts
- Max rounds and cost limit

## Outputs
- Debate transcript
- Consensus status
- Final answer

## Workflow
1. Initialize debate state.
2. Run speaking round for proposer/critic/expert roles.
3. Check consensus or stopping conditions.
4. Synthesize discussion.
5. Optional judge step for final decision.

## Failure Modes
- Poor role prompts produce repetitive responses.
- Consensus heuristic triggers too early/late.
- Cost estimate underestimates actual provider cost.

## Safety Guardrails
- Limit rounds and estimated spend.
- Keep role prompts bounded and non-harmful.
- Preserve transcript for auditability.

## Minimal Example
Question: "Monolith or microservices for MVP?"
- Proposer suggests modular monolith.
- Critic identifies scaling tradeoffs.
- Expert adds migration strategy.
- Synthesizer returns final recommendation.

## Evaluation Checklist
- [ ] Distinct role contributions.
- [ ] Clear stopping condition.
- [ ] Final answer uses debate evidence.
- [ ] Cost/round limits enforced.
