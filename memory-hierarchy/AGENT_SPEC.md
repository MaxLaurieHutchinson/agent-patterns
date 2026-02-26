# AGENT_SPEC

## Name
memory_hierarchy

## Purpose
Store and retrieve multi-tier context for higher quality agent responses.

## Inputs
- `interaction` (object, optional): user + assistant turn
- `query` (string, optional): retrieval query
- `session_id` (string, optional)

## Outputs
- `context` (string)
- `episodic_results` (array)
- `semantic_results` (array)

## Preconditions
- Memory stores are initialized.
- Embedding model is optional.

## Procedure
1. Add new interaction to working memory.
2. Persist combined interaction to episodic memory.
3. Query episodic memory by similarity or keyword fallback.
4. Query semantic memory by key lookup strategy.
5. Return assembled context for model consumption.

## Safety Rules
- Avoid storing secrets unless explicitly required.
- Support memory clearing and age-based pruning.
- Preserve source/confidence metadata for facts.

## Failure Handling
- If embedding lookup fails, fallback to keyword retrieval.
- If no memories are relevant, return empty sections safely.

## Telemetry
- working memory size
- episodic item count
- retrieval result counts

## Example I/O Contract
```json
{
  "input": {"query": "React state"},
  "output": {"context": "...", "episodic_results": []},
  "status": "ok"
}
```
