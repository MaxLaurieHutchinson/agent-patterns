# Plan-and-Execute Architecture

## System Overview

```mermaid
graph TD
    A[Complex Task] --> B[Planner LLM]
    B --> C[Plan: List of Steps]
    C --> D{Execution Strategy}
    D -->|Sequential| E[Step-by-Step Executor]
    D -->|Parallel| F[Parallel Executor]
    D -->|Dynamic| G[Replanning Executor]
    E --> H[Results Aggregator]
    F --> H
    G --> H
    H --> I[Final Answer]
```

## State Machine

```mermaid
stateDiagram-v2
    [*] --> Planning : Receive task
    Planning --> PlanReady : Plan created
    PlanReady --> Executing : Start execution
    Executing --> Executing : Complete step
    Executing --> Replanning : Need adjustment
    Replanning --> PlanReady : Update plan
    Executing --> Complete : All steps done
    Complete --> [*] : Return result
```

## Component Diagram

```mermaid
classDiagram
    class Planner {
        +llm: BaseChatModel
        +create_plan(task, context)
        +validate_plan(plan)
    }
    
    class Plan {
        +steps: List[Step]
        +dependencies: Dict
        +estimated_cost: float
        +add_step(step)
        +get_parallel_groups()
    }
    
    class Step {
        +id: str
        +description: str
        +dependencies: List[str]
        +status: Status
        +result: Any
    }
    
    class Executor {
        +llm: BaseChatModel
        +tools: List[Tool]
        +execute_step(step)
        +execute_parallel(steps)
    }
    
    class ReplanningController {
        +should_replan(context)
        +update_plan(plan, new_info)
    }
    
    Planner --> Plan : creates
    Plan --> Step : contains
    Executor --> Step : executes
    ReplanningController --> Plan : modifies
```

## Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     Plan & Execute Flow                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Input: "Summarize the latest AI papers from arXiv"         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ PLANNER                                              │   │
│  │ 1. Search for recent AI papers on arXiv             │   │
│  │ 2. Download top 5 papers                             │   │
│  │ 3. Extract key findings from each paper              │   │
│  │ 4. Synthesize into summary                           │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ PARALLEL GROUPS                                       │   │
│  │ Group 1: [Step 1] → [Step 2]                         │   │
│  │ Group 2: [Step 3 - Paper 1]                          │   │
│  │          [Step 3 - Paper 2]  (parallel)              │   │
│  │          [Step 3 - Paper 3]                          │   │
│  │ Group 3: [Step 4] (depends on Group 2)               │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ EXECUTOR                                             │   │
│  │ Executing Group 1... ✓                               │   │
│  │ Executing Group 2... ✓ (5 parallel)                  │   │
│  │ Executing Group 3... ✓                               │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ RESULTS                                              │   │
│  │ Summary: [Combined findings from all papers]         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Execution Strategies

### Sequential
```
Step 1 → Step 2 → Step 3 → Step 4
  │        │        │        │
  ▼        ▼        ▼        ▼
Result 1  Result 2 Result 3 Result 4
```

### Parallel (by dependency groups)
```
Group 1: [Step 1, Step 2] (no deps)
            │
            ▼
Group 2: [Step 3, Step 4, Step 5] (depend on 1 & 2)
            │
            ▼
Group 3: [Step 6] (depends on 3,4,5)
```

### Dynamic Replanning
```
Execute Step 1 → Discover new info → Replan remaining steps
                                          │
                                          ▼
                               Update Step 3 & 4
                                          │
                                          ▼
                                Continue execution
```
