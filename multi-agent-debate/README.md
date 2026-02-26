# Multi-Agent Debate Pattern

The Multi-Agent Debate pattern uses multiple specialized agents that discuss a problem, propose solutions, critique each other's ideas, and reach a consensus or best answer.

## Core Concept

```
Problem -> Agent A proposes -> Agent B critiques -> Agent C synthesizes
                    |              |                |
              Consensus / Best Answer / Refined Solution
```

Multiple agents with different roles/perspectives collaborate:
- **Proposer** - Suggests solutions
- **Critic** - Identifies flaws and improvements
- **Synthesizer** - Combines best ideas
- **Judge** - Makes final decisions

## When to Use

### ✅ Use Multi-Agent Debate When:
- Complex decisions requiring diverse perspectives
- Creative tasks (brainstorming, writing)
- Code review and analysis
- Ethical considerations
- Need for higher quality through critique
- Different expertise domains needed

### ❌ Don't Use When:
- Simple, straightforward tasks
- Cost-sensitive applications (multiple LLM calls)
- Speed is critical
- Task doesn't benefit from multiple viewpoints

## Key Benefits

1. **Higher Quality** - Multiple perspectives catch issues
2. **Self-Correction** - Agents critique each other
3. **Creativity** - Diverse approaches to problems
4. **Robustness** - Less likely to miss important considerations
5. **Explainability** - Clear reasoning process visible

## This Repository's Implementation

- Core implementation: `implementation.py`
- Demo script: `example.py`
- Role model: proposer, critic, expert, synthesizer, judge
- Termination checks: consensus heuristic, max rounds, and cost limit

### Current Tradeoffs

- Consensus detection uses a simple keyword-based heuristic.
- Cost tracking is intentionally approximate for readability.
- Synthesis and judging are single-pass calls rather than multi-criteria voting.

## Related Patterns

- **Plan-and-Execute** - Debate can review/improve plans
- **Observer Pattern** - Agents can coordinate through events
- **Memory Hierarchy** - Store debate history for future reference
- **ReAct Loop** - Individual agents can use ReAct internally
