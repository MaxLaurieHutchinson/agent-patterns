# Agent Patterns Catalog

A practical reference library of agentic design patterns with Python implementations and runnable demos.

## Repository Structure

- `react-loop/` - Reasoning + acting loop with tool calls
- `plan-and-execute/` - Planning/execution state machine with multiple strategies
- `multi-agent-debate/` - Multi-role collaborative reasoning
- `circuit-breaker/` - Reliability guard for LLM/tool calls
- `memory-hierarchy/` - Working, episodic, and semantic memory layers
- `observer-pattern/` - Event bus and pub/sub coordination model
- `tool-use-mcp/` - MCP-style tool registry + execution adapter

## Quick Decision Matrix

| Pattern | Use When | Don't Use When | Complexity | Best For |
|---------|----------|----------------|------------|----------|
| **ReAct Loop** | Tasks requiring reasoning + action cycles | Simple, single-step tasks | Low | Interactive problem-solving, tool use |
| **Plan-and-Execute** | Complex, multi-step tasks with clear subgoals | Real-time, streaming tasks | Medium | Research, data processing workflows |
| **Multi-Agent Debate** | Need diverse perspectives, complex decisions | Simple tasks, cost-sensitive | High | Creative tasks, ethical decisions, review |
| **Circuit Breaker** | Production systems with external LLM calls | Prototypes, internal tools | Low | Reliability, cost control |
| **Memory Hierarchy** | Long-running agents with learning | Stateless, one-shot tasks | Medium | Personal assistants, knowledge agents |
| **Observer Pattern** | Event-driven coordination, reactive systems | Simple linear workflows | Medium | Real-time monitoring, multi-agent systems |
| **Tool Use (MCP)** | Integrating external tools/resources | No external dependencies | Medium | Tool-augmented agents |

## Pattern Summaries

### 1. ReAct Loop
**Reasoning + Acting cycles**

The ReAct pattern interleaves reasoning (thought) and action steps. The agent thinks about what to do, performs an action (like calling a tool), observes the result, and repeats until the task is complete.

- **When to use:** Interactive problem-solving, tool-using agents, tasks requiring step-by-step reasoning
- **Key benefit:** Transparent decision-making process, easy to debug
- **See:** [/react-loop/README.md](./react-loop/README.md)

### 2. Plan-and-Execute
**Decomposition + execution**

Breaks complex tasks into a plan of subtasks, then executes them sequentially or in parallel. Often uses a planner LLM and an executor LLM/agent.

- **When to use:** Multi-step workflows, research tasks, data processing pipelines
- **Key benefit:** Structured approach to complex problems, parallelization opportunities
- **See:** [/plan-and-execute/README.md](./plan-and-execute/README.md)

### 3. Multi-Agent Debate
**Multiple agents discussing solution**

Multiple specialized agents discuss a problem, propose solutions, critique each other's ideas, and reach a consensus or best answer.

- **When to use:** Complex decisions requiring diverse perspectives, creative tasks, code review
- **Key benefit:** Higher quality outputs through collaboration and critique
- **See:** [/multi-agent-debate/README.md](./multi-agent-debate/README.md)

### 4. Circuit Breaker
**Fail fast for LLM failures**

Prevents cascading failures by stopping requests when error rates or costs exceed thresholds. Essential for production systems.

- **When to use:** Production agents, cost-sensitive applications, high-availability systems
- **Key benefit:** System resilience, cost control
- **See:** [/circuit-breaker/README.md](./circuit-breaker/README.md)

### 5. Memory Hierarchy
**Working + episodic + semantic memory**

Implements a multi-layered memory system: working memory (current context), episodic memory (past experiences), and semantic memory (general knowledge).

- **When to use:** Long-running agents, learning systems, personal assistants
- **Key benefit:** Contextual awareness, learning from experience
- **See:** [/memory-hierarchy/README.md](./memory-hierarchy/README.md)

### 6. Observer Pattern
**Event-driven agent coordination**

Agents subscribe to events and react to changes. Enables loose coupling and reactive behavior in multi-agent systems.

- **When to use:** Real-time systems, event-driven workflows, multi-agent coordination
- **Key benefit:** Loose coupling, reactive responses
- **See:** [/observer-pattern/README.md](./observer-pattern/README.md)

### 7. Tool Use (MCP)
**Model Context Protocol integration**

Standardized way for LLMs to discover and use external tools following the Model Context Protocol specification.

- **When to use:** Tool-augmented agents, API integrations, resource access
- **Key benefit:** Standardized tool interface, dynamic tool discovery
- **See:** [/tool-use-mcp/README.md](./tool-use-mcp/README.md)

## Choosing the Right Pattern

### For Simple Tasks
Start with **ReAct Loop** - it's the foundation of most agent systems.

### For Complex Workflows
Combine **Plan-and-Execute** with **ReAct** - plan the approach, then use ReAct for each subtask.

### For Production Systems
Always add **Circuit Breaker** for reliability.

### For Learning Agents
Implement **Memory Hierarchy** to maintain context across sessions.

### For Multi-Agent Systems
Use **Observer Pattern** for coordination and **Multi-Agent Debate** for quality.

## Video Content Recommendations

These patterns are particularly visual and educational for video content:

1. **Multi-Agent Debate** - Great for showing agents "talking" to each other
2. **ReAct Loop** - Clear step-by-step visualization of reasoning
3. **Memory Hierarchy** - Visual memory layers and retrieval
4. **Plan-and-Execute** - Flowchart-style plan visualization
5. **Circuit Breaker** - State machine transitions (Closed/Open/Half-Open)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running Examples

Each pattern includes a runnable example:

```bash
cd react-loop
python example.py
```

Some examples require `OPENAI_API_KEY`. If unset, most demos fall back to mock mode.

## Running Tests

```bash
python3.11 -m unittest discover -s tests -v
```

## Notes on Scope

- This repo is a reference implementation, not a complete production framework.
- Several patterns intentionally keep simple heuristics for readability (for example consensus detection and plan parsing).
- Security-sensitive components are guarded where appropriate (for example filesystem tool paths are constrained to a configured base directory).

## Contributing

Add new patterns following the same structure:
1. `README.md` - Concept explanation
2. `diagram.md` - Architecture diagram
3. `implementation.py` - Core implementation
4. `example.py` - Usage example
