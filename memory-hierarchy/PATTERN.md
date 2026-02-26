# Memory Hierarchy (Plain Language)

## What It Is
A layered memory model for agents: short-term working memory, episodic memory of past interactions, and semantic memory of facts.

## When To Use
- Conversations span sessions.
- Personalization matters.
- Retrieval of prior context improves output quality.

## When Not To Use
- Strict stateless processing.
- High privacy constraints that disallow persistence.

## Inputs
- New user/assistant messages
- Retrieval query
- Optional embedding model

## Outputs
- Assembled context
- Stored interactions/facts
- Retrieved memories

## Workflow
1. Store current turn in working and episodic memory.
2. Query episodic and semantic memory for relevant items.
3. Assemble context string for downstream reasoning.
4. Optionally learn new facts.

## Failure Modes
- Low retrieval quality from weak embeddings/keywords.
- Memory growth without pruning.
- Stale facts with outdated confidence.

## Safety Guardrails
- Minimize sensitive data retention.
- Allow selective forgetting and pruning.
- Track confidence/source for facts.

## Minimal Example
- Store: "User prefers concise answers"
- Later query: "How should I answer?"
- Retrieve preference and adapt response style.

## Evaluation Checklist
- [ ] Recovers relevant context.
- [ ] Keeps working memory bounded.
- [ ] Supports forgetting/pruning.
- [ ] Distinguishes episodic vs semantic content.
