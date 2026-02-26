```mermaid
flowchart TD
    A[Query] --> B[Solver Draft]
    B --> C[Verifier]
    C -->|pass| D[Final Answer]
    C -->|fail + feedback| E[Reflection/Revision]
    E --> B
```
