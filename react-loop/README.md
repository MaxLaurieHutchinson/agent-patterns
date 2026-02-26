# ReAct Loop Pattern

The ReAct (Reasoning + Acting) pattern is a fundamental agent architecture where the LLM interleaves reasoning steps (thoughts) with action steps (tool calls). This creates a transparent, step-by-step problem-solving process.

## Core Concept

```
Thought → Action → Observation → Thought → Action → ... → Answer
```

The agent:
1. **Thinks** about the current state and what to do next
2. **Acts** by calling a tool or function
3. **Observes** the result
4. Repeats until the task is complete

## When to Use

### ✅ Use ReAct When:
- Task requires step-by-step reasoning
- Need transparent decision-making (debuggable)
- Using external tools (calculator, search, APIs)
- Interactive problem-solving
- The LLM needs to verify intermediate results

### ❌ Don't Use When:
- Simple, single-step tasks (overhead not worth it)
- Need maximum speed (streaming with reasoning adds latency)
- Task is purely creative/generative without verification needs

## Key Benefits

1. **Transparency** - See exactly how the agent is thinking
2. **Debuggability** - Easy to trace where things went wrong
3. **Tool Integration** - Natural fit for tool-using agents
4. **Self-Correction** - Agent can notice and fix its own mistakes

## Variations

- **Zero-shot ReAct** - No examples provided, LLM reasons from scratch
- **Few-shot ReAct** - Examples of reasoning chains provided
- **Reflexion** - Adds self-evaluation after each step

## Related Patterns

- **Plan-and-Execute** - ReAct can be the executor for each plan step
- **Tool Use (MCP)** - ReAct naturally integrates with tool systems
- **Memory Hierarchy** - ReAct can store reasoning traces in episodic memory
