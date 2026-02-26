# Multi-Agent Debate Architecture

## System Overview

```mermaid
graph TB
    A[Problem/Query] --> B[Debate Orchestrator]
    B --> C[Agent 1: Proposer]
    B --> D[Agent 2: Critic]
    B --> E[Agent 3: Expert]
    B --> F[Agent 4: Synthesizer]
    
    C --> G[Shared Context]
    D --> G
    E --> G
    F --> G
    
    G --> H[Debate History]
    H --> B
    
    B --> I{Termination?}
    I -->|No| B
    I -->|Yes| J[Final Answer]
    J --> K[Output]
```

## Debate Flow

```mermaid
sequenceDiagram
    participant U as User
    participant O as Orchestrator
    participant P as Proposer
    participant C as Critic
    participant S as Synthesizer
    participant J as Judge
    
    U->>O: Submit problem
    O->>P: Request proposal
    P->>O: Solution A
    O->>C: Request critique
    C->>O: Issues identified
    O->>P: Revise with feedback
    P->>O: Solution B
    O->>E: Expert analysis
    E->>O: Technical review
    O->>S: Synthesize solutions
    S->>O: Combined approach
    O->>J: Final decision
    J->>O: Best answer
    O->>U: Return result
```

## State Machine

```mermaid
stateDiagram-v2
    [*] --> Initialization : Start debate
    Initialization --> RoundStart : Agents ready
    RoundStart --> AgentTurn : Select agent
    AgentTurn --> RoundComplete : Agent responds
    RoundComplete --> RoundStart : Next round
    RoundComplete --> Evaluation : Max rounds reached
    RoundComplete --> Evaluation : Early consensus
    Evaluation --> RoundStart : Needs more discussion
    Evaluation --> Finalization : Consensus reached
    Finalization --> [*] : Return answer
```

## Agent Interactions

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Agent Debate                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Round 1                                                        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │Proposer  │───▶│ Critic   │───▶│ Expert   │                  │
│  │"Use X"   │    │"X fails   │    │"Agreed,  │                  │
│  │          │    │ when Y"  │    │ try Z"   │                  │
│  └──────────┘    └──────────┘    └────┬─────┘                  │
│                                        │                        │
│                                        ▼                        │
│                               ┌──────────────┐                 │
│                               │ Shared Context│                 │
│                               │ - X suggested │                 │
│                               │ - Y is issue  │                 │
│                               │ - Z proposed  │                 │
│                               └──────┬───────┘                 │
│                                      │                          │
│  Round 2                             ▼                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │Proposer  │◀───│ Critic   │◀───│ Expert   │                  │
│  │"Z + W"   │    │"Better,  │    │"Z is     │                  │
│  │(revised) │    │ but..."  │    │ optimal" │                  │
│  └────┬─────┘    └──────────┘    └──────────┘                  │
│       │                                                         │
│       ▼                                                         │
│  ┌──────────┐                                                  │
│  │Synthesizer│                                                  │
│  │"Combine  │                                                  │
│  │ Z and W" │                                                  │
│  └────┬─────┘                                                  │
│       │                                                         │
│       ▼                                                         │
│  ┌──────────┐                                                  │
│  │  Judge   │                                                  │
│  │"Final:   │                                                  │
│  │ Use Z+W" │                                                  │
│  └──────────┘                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Message Flow

```
User Query
    │
    ▼
┌─────────────────────────────────────┐
│ Initialize Debate                   │
│ - Define agents                     │
│ - Set roles                         │
│ - Create shared context             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Round 1                             │
│ ┌───────────────────────────────┐   │
│ │ Proposer: "I suggest using    │   │
│ │ the Strategy pattern..."      │   │
│ └───────────────────────────────┘   │
│              │                      │
│              ▼                      │
│ ┌───────────────────────────────┐   │
│ │ Critic: "Strategy pattern has │   │
│ │ overhead. Consider factory."  │   │
│ └───────────────────────────────┘   │
│              │                      │
│              ▼                      │
│ ┌───────────────────────────────┐   │
│ │ Expert: "For this use case,   │   │
│ │ strategy is actually fine."   │   │
│ └───────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Check Termination                   │
│ - Rounds completed?                 │
│ - Consensus reached?                │
│ - Max cost exceeded?                │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌──────────┐      ┌──────────────┐
│ Continue │      │  Finalize    │
│ Debate   │      │              │
│          │      │ Synthesize   │
│ Round 2  │      │ all views    │
└──────────┘      │ Judge decides│
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Final Answer │
                  └──────────────┘
```
