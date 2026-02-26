# Memory Hierarchy Architecture

## System Overview

```mermaid
graph TB
    A[User Input] --> B[Memory Manager]
    B --> C[Working Memory]
    B --> D[Episodic Memory]
    B --> E[Semantic Memory]
    
    C --> F[LLM Context]
    D --> F
    E --> F
    
    F --> G[LLM Response]
    G --> H[Memory Update]
    H --> C
    H --> D
    H --> E
    
    I[Embeddings Model] --> D
    I --> E
    
    J[Vector Database] --> D
    K[Knowledge Graph] --> E
```

## Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant MM as Memory Manager
    participant WM as Working Memory
    participant EM as Episodic Memory
    participant SM as Semantic Memory
    participant LLM as LLM
    
    U->>MM: New message
    MM->>WM: Check recent context
    MM->>EM: Retrieve similar experiences
    MM->>SM: Query relevant knowledge
    
    WM-->>MM: Last 5 messages
    EM-->>MM: 3 similar conversations
    SM-->>MM: 2 relevant facts
    
    MM->>LLM: Assemble context
    LLM->>MM: Generate response
    
    MM->>WM: Update context
    MM->>EM: Store interaction
    MM->>SM: Extract new facts
    
    MM->>U: Return response
```

## Component Architecture

```mermaid
classDiagram
    class MemoryManager {
        +working_memory: WorkingMemory
        +episodic_memory: EpisodicMemory
        +semantic_memory: SemanticMemory
        +retrieve_context(query, config)
        +store_interaction(interaction)
        +consolidate_memories()
    }
    
    class WorkingMemory {
        +messages: List[Message]
        +max_size: int
        +add_message(msg)
        +get_context(n)
        +clear()
    }
    
    class EpisodicMemory {
        +vector_store: VectorStore
        +embedding_model: Embeddings
        +store(experience)
        +retrieve(query, k)
        +forget_old(threshold)
    }
    
    class SemanticMemory {
        +knowledge_graph: Graph
        +facts_db: Database
        +add_fact(fact, source)
        +query_fact(query)
        +infer_relation(entity1, entity2)
    }
    
    class MemoryConfig {
        +working_memory_size: int
        +episodic_retrieval_k: int
        +consolidation_threshold: float
    }
    
    MemoryManager --> WorkingMemory : manages
    MemoryManager --> EpisodicMemory : manages
    MemoryManager --> SemanticMemory : manages
    MemoryManager --> MemoryConfig : uses
```

## Memory Retrieval Flow

```
┌──────────────────────────────────────────────────────────────┐
│                   Memory Retrieval                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Input: "What's the status of my project?"                  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. WORKING MEMORY RETRIEVAL                            │  │
│  │                                                        │  │
│  │ Recent messages:                                       │  │
│  │ - User: "Check project status"                        │  │
│  │ - Assistant: "Which project?"                         │  │
│  │ - User: "The website redesign"                        │  │
│  │                                                        │  │
│  │ Retrieved: "Website redesign project"                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│                            ▼                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 2. EPISODIC MEMORY RETRIEVAL                           │  │
│  │                                                        │  │
│  │ Query: "website redesign project"                     │  │
│  │ Embedding: [0.23, -0.45, 0.89, ...]                   │  │
│  │                                                        │  │
│  │ Similar experiences:                                   │  │
│  │ - "Last week discussed website timeline" (0.92)       │  │
│  │ - "User prefers weekly updates" (0.78)                │  │
│  │ - "Previous project: mobile app" (0.65)               │  │
│  │                                                        │  │
│  │ Retrieved: Timeline discussion, update preference     │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│                            ▼                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 3. SEMANTIC MEMORY RETRIEVAL                           │  │
│  │                                                        │  │
│  │ Query: "website redesign status tracking"             │  │
│  │                                                        │  │
│  │ Knowledge facts:                                       │  │
│  │ - Website redesign: Status = In Progress              │  │
│  │ - Website redesign: Deadline = 2024-03-15             │  │
│  │ - Project status tracking uses Jira                   │  │
│  │                                                        │  │
│  │ Retrieved: Current status, deadline, tools used       │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│                            ▼                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 4. CONTEXT ASSEMBLY                                    │  │
│  │                                                        │  │
│  │ [Working Memory]                                       │  │
│  │ The user is asking about the website redesign project │  │
│  │ they mentioned previously.                            │  │
│  │                                                        │  │
│  │ [Episodic Memory]                                     │  │
│  │ Previously, we discussed the timeline for this        │  │
│  │ project. The user prefers weekly status updates.      │  │
│  │                                                        │  │
│  │ [Semantic Memory]                                     │  │
│  │ Project: Website Redesign                             │  │
│  │ Status: In Progress                                   │  │
│  │ Deadline: March 15, 2024                              │  │
│  │ Tracking: Jira board                                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Memory Storage Flow

```
New Interaction
       │
       ▼
┌─────────────────────────────────────┐
│ 1. Store in Working Memory          │
│    - Add to message history         │
│    - Trim if exceeds limit          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Store in Episodic Memory         │
│    - Create embedding               │
│    - Store with timestamp           │
│    - Tag with session/user          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Extract Semantic Knowledge       │
│    - Identify facts learned         │
│    - Update knowledge graph         │
│    - Link to existing facts         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Consolidation (Periodic)         │
│    - Summarize old episodes         │
│    - Prune redundant memories       │
│    - Reinforce important facts      │
└─────────────────────────────────────┘
```
