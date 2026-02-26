# Plan-and-Execute Pattern

The Plan-and-Execute pattern separates planning from execution. A planner breaks down complex tasks into subtasks, and an executor (often another agent) carries out each step.

## Core Concept

```
Complex Task -> Planner -> [Subtask 1, Subtask 2, ...] -> Executor -> Results
```

Two main components:
1. **Planner** - Analyzes the task and creates a structured plan
2. **Executor** - Executes each step, potentially using ReAct or other patterns

## When to Use

### ✅ Use Plan-and-Execute When:
- Task has clear, separable subtasks
- Need to parallelize independent steps
- Want to optimize the plan before execution
- Complex multi-step workflows (research, data processing)
- Cost optimization (cheaper model for execution)

### ❌ Don't Use When:
- Task is highly dynamic (plan becomes obsolete quickly)
- Need real-time streaming responses
- Simple tasks where planning overhead isn't worth it
- Tasks requiring constant replanning

## Key Benefits

1. **Modularity** - Separate planning logic from execution
2. **Optimization** - Review and optimize plan before execution
3. **Parallelization** - Execute independent steps concurrently
4. **Cost Control** - Use cheaper models for execution
5. **Observability** - Clear view of what's happening

## This Repository's Implementation

- Core implementation: `implementation.py`
- Demo script: `example.py`
- Strategies: `sequential`, `parallel`, and `dynamic`
- Graph flow: `plan -> execute -> (execute|replan|finalize)`

### Current Tradeoffs

- Plan parsing expects a constrained text format from the planner model.
- Dynamic replanning is intentionally lightweight and increments replan attempts, but does not fully rebuild plan steps.
- Tool execution in `_execute_single_step` is model-driven (not full autonomous tool routing).

## Architecture Variants

### Sequential Execution
Execute steps one at a time in dependency order.

### Parallel Execution
Execute independent steps concurrently.

### Dynamic Replanning
Replan if execution reveals new information.

### Hierarchical Planning
Plan -> Sub-plans -> Execution (recursive)

## Related Patterns

- **ReAct Loop** - Good executor for individual steps
- **Multi-Agent Debate** - Can review and improve plans
- **Memory Hierarchy** - Store plans and execution history
- **Observer Pattern** - Monitor plan execution progress
