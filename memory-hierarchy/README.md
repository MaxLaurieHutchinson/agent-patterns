# Memory Hierarchy Pattern

The Memory Hierarchy pattern implements a multi-layered memory system for agents: working memory (current context), episodic memory (past experiences), and semantic memory (general knowledge).

## Core Concept

```
┌─────────────────────────────────────────────────────────────┐
│                    Memory Hierarchy                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ WORKING MEMORY (Immediate)                          │   │
│  │ - Current conversation context                      │   │
│  │ - Active goals and tasks                            │   │
│  │ - Recent observations                               │   │
│  │ Size: Limited (last N messages)                     │   │
│  └────────────────────┬────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ EPISODIC MEMORY (Personal History)                  │   │
│  │ - Past conversations                                │   │
│  │ - Previous task outcomes                            │   │
│  │ - User preferences learned                          │   │
│  │ Retrieval: Similarity search on embeddings          │   │
│  └────────────────────┬────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SEMANTIC MEMORY (General Knowledge)                 │   │
│  │ - Facts and concepts                                │   │
│  │ - Procedures and rules                              │   │
│  │ - Domain knowledge                                  │   │
│  │ Storage: Vector DB, Knowledge Graph                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Memory Types

### Working Memory
- **Scope:** Current session/conversation
- **Lifetime:** Ephemeral (session duration)
- **Access:** Immediate (O(1))
- **Size:** Limited (context window constraints)

### Episodic Memory  
- **Scope:** Personal experiences with user
- **Lifetime:** Persistent
- **Access:** Similarity search
- **Use:** "Last time we talked about...", "You prefer..."

### Semantic Memory
- **Scope:** General facts and knowledge
- **Lifetime:** Persistent
- **Access:** Query/search
- **Use:** "The capital of France is...", "To deploy X, you should..."

## When to Use

### ✅ Use Memory Hierarchy When:
- Long-running agents with user relationships
- Need to learn from past interactions
- Complex tasks requiring context from previous sessions
- Personal assistants
- Knowledge-intensive applications

### ❌ Don't Use When:
- Stateless, one-shot tasks
- Strict privacy requirements (no persistence)
- Memory overhead not justified

## Key Benefits

1. **Contextual Awareness** - Remember important context
2. **Personalization** - Learn user preferences
3. **Continuity** - Conversations span sessions
4. **Learning** - Improve from past experiences
5. **Efficiency** - Retrieve relevant info instead of recomputing

## Related Patterns

- **ReAct Loop** - Can query memory during reasoning
- **Observer Pattern** - Memory changes trigger events
- **Multi-Agent Debate** - Agents share common semantic memory
