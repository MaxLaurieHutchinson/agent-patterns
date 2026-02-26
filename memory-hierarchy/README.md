# Memory Hierarchy Pattern

The Memory Hierarchy pattern implements a multi-layered memory system for agents: working memory (current context), episodic memory (past experiences), and semantic memory (general knowledge).

## Core Concept

```
Working (short-term) -> Episodic (experience) -> Semantic (facts/knowledge)
```

## Memory Types

### Working Memory
- **Scope:** Current session/conversation
- **Lifetime:** Ephemeral
- **Access:** Immediate
- **Size:** Bounded by configured message count

### Episodic Memory
- **Scope:** Past interactions and outcomes
- **Lifetime:** Persistent in process/runtime store
- **Access:** Embedding similarity or keyword fallback
- **Use:** User preferences, prior conversations, historical context

### Semantic Memory
- **Scope:** Structured facts and relationships
- **Lifetime:** Persistent in process/runtime store
- **Access:** Key/query lookup
- **Use:** Known facts, domain knowledge, relationship graphs

## When to Use

### ✅ Use Memory Hierarchy When:
- Long-running agents with user relationships
- Need to learn from past interactions
- Complex tasks needing cross-session context
- Personal assistant-style behavior
- Knowledge-intensive applications

### ❌ Don't Use When:
- Stateless, one-shot tasks
- Strict no-persistence privacy requirements
- Memory overhead is not justified

## Key Benefits

1. **Contextual Awareness** - Preserve relevant context
2. **Personalization** - Learn user preferences over time
3. **Continuity** - Span sessions with remembered state
4. **Learning** - Improve from prior outcomes
5. **Efficiency** - Retrieve instead of recompute

## This Repository's Implementation

- Core implementation: `implementation.py`
- Demo script: `example.py`
- Working memory: bounded deque of recent messages + goals/context
- Episodic memory: scored retrieval using embedding or keyword overlap
- Semantic memory: fact store + simple entity relationship queries

### Current Tradeoffs

- Semantic `query()` currently uses simple key-based matching.
- Episodic embeddings are optional; without an embedding model it falls back to keyword matching.
- Storage is in-memory in this reference implementation (no external DB by default).

## Related Patterns

- **ReAct Loop** - Can retrieve memory during reasoning
- **Observer Pattern** - Memory updates can emit events
- **Multi-Agent Debate** - Shared semantic memory across agents
