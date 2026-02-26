"""
Memory Hierarchy Implementation
Implements a three-tier memory system: working, episodic, and semantic memory.
"""

from typing import TypedDict, Annotated, Sequence, Any, Optional
import operator
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import hashlib
import json

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.embeddings import Embeddings


@dataclass
class MemoryEntry:
    """A single memory entry."""
    content: str
    timestamp: datetime
    source: str
    metadata: dict = field(default_factory=dict)
    embedding: Optional[list[float]] = None
    importance: float = 1.0  # 0.0 - 1.0
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "metadata": self.metadata,
            "importance": self.importance
        }


class WorkingMemory:
    """
    Short-term memory for current context.
    Limited size, fast access, ephemeral.
    """
    
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages: deque[BaseMessage] = deque(maxlen=max_messages)
        self.current_goals: list[str] = []
        self.active_context: dict[str, Any] = {}
    
    def add_message(self, message: BaseMessage):
        """Add a message to working memory."""
        self.messages.append(message)
    
    def get_context(self, n: Optional[int] = None) -> list[BaseMessage]:
        """Get recent messages."""
        if n is None:
            return list(self.messages)
        return list(self.messages)[-n:]
    
    def set_goal(self, goal: str):
        """Set an active goal."""
        if goal not in self.current_goals:
            self.current_goals.append(goal)
    
    def clear_goal(self, goal: str):
        """Clear a goal."""
        if goal in self.current_goals:
            self.current_goals.remove(goal)
    
    def update_context(self, key: str, value: Any):
        """Update active context."""
        self.active_context[key] = value
    
    def clear(self):
        """Clear working memory."""
        self.messages.clear()
        self.current_goals.clear()
        self.active_context.clear()
    
    def to_string(self) -> str:
        """Convert to string for LLM context."""
        parts = []
        
        if self.current_goals:
            parts.append(f"Active Goals: {', '.join(self.current_goals)}")
        
        if self.active_context:
            parts.append(f"Context: {json.dumps(self.active_context)}")
        
        parts.append("Recent Messages:")
        for msg in self.messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            parts.append(f"  {role}: {msg.content[:100]}...")
        
        return "\n".join(parts)


class EpisodicMemory:
    """
    Long-term memory for experiences.
    Stores interactions, events, learned preferences.
    """
    
    def __init__(self, embedding_model: Optional[Embeddings] = None):
        self.embedding_model = embedding_model
        self.memories: list[MemoryEntry] = []
        self.session_memories: dict[str, list[MemoryEntry]] = {}
    
    def store(self, content: str, source: str = "unknown", 
              metadata: Optional[dict] = None,
              importance: float = 1.0) -> MemoryEntry:
        """Store a new episodic memory."""
        entry = MemoryEntry(
            content=content,
            timestamp=datetime.now(),
            source=source,
            metadata=metadata or {},
            importance=importance
        )
        
        # Generate embedding if model available
        if self.embedding_model:
            try:
                entry.embedding = self.embedding_model.embed_query(content)
            except Exception:
                pass
        
        self.memories.append(entry)
        
        # Also store in session
        session_id = metadata.get("session_id", "default") if metadata else "default"
        if session_id not in self.session_memories:
            self.session_memories[session_id] = []
        self.session_memories[session_id].append(entry)
        
        return entry
    
    def retrieve(self, query: str, k: int = 5, 
                 min_similarity: float = 0.7) -> list[MemoryEntry]:
        """Retrieve similar memories using embedding similarity."""
        if not self.embedding_model or not self.memories:
            # Fallback: keyword matching
            return self._keyword_retrieve(query, k)
        
        try:
            query_embedding = self.embedding_model.embed_query(query)
        except Exception:
            return self._keyword_retrieve(query, k)
        
        # Calculate similarities
        scored = []
        for memory in self.memories:
            if memory.embedding:
                similarity = self._cosine_similarity(query_embedding, memory.embedding)
                if similarity >= min_similarity:
                    # Weight by importance and recency
                    recency_boost = self._recency_score(memory.timestamp)
                    final_score = similarity * memory.importance * recency_boost
                    scored.append((final_score, memory))
        
        # Return top k
        scored.sort(reverse=True, key=lambda x: x[0])
        return [m for _, m in scored[:k]]
    
    def _keyword_retrieve(self, query: str, k: int) -> list[MemoryEntry]:
        """Simple keyword-based retrieval fallback."""
        keywords = set(query.lower().split())
        scored = []
        
        for memory in self.memories:
            memory_words = set(memory.content.lower().split())
            overlap = len(keywords & memory_words)
            if overlap > 0:
                recency = self._recency_score(memory.timestamp)
                scored.append((overlap * memory.importance * recency, memory))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        return [m for _, m in scored[:k]]
    
    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
    
    def _recency_score(self, timestamp: datetime) -> float:
        """Calculate recency boost (0.0 - 1.0)."""
        age_hours = (datetime.now() - timestamp).total_seconds() / 3600
        # Exponential decay: 1.0 at 0 hours, ~0.37 at 24 hours
        import math
        return math.exp(-age_hours / 24)
    
    def get_session_history(self, session_id: str) -> list[MemoryEntry]:
        """Get all memories from a specific session."""
        return self.session_memories.get(session_id, [])
    
    def forget_old(self, days: int = 30):
        """Remove memories older than specified days."""
        cutoff = datetime.now().timestamp() - (days * 24 * 3600)
        self.memories = [
            m for m in self.memories 
            if m.timestamp.timestamp() > cutoff
        ]


class SemanticMemory:
    """
    Structured knowledge storage.
    Facts, concepts, and relationships.
    """
    
    def __init__(self):
        self.facts: dict[str, Any] = {}
        self.relationships: dict[str, list[tuple[str, str]]] = {}
        # entity -> [(relation, target), ...]
    
    def add_fact(self, key: str, value: Any, 
                 source: str = "inferred", confidence: float = 1.0):
        """Add a factual knowledge."""
        self.facts[key] = {
            "value": value,
            "source": source,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_fact(self, key: str) -> Optional[Any]:
        """Retrieve a fact."""
        fact = self.facts.get(key)
        return fact["value"] if fact else None
    
    def add_relationship(self, entity1: str, relation: str, entity2: str):
        """Add a relationship between entities."""
        if entity1 not in self.relationships:
            self.relationships[entity1] = []
        self.relationships[entity1].append((relation, entity2))
    
    def query_relationship(self, entity: str, 
                          relation: Optional[str] = None) -> list[str]:
        """Query relationships for an entity."""
        rels = self.relationships.get(entity, [])
        if relation:
            return [target for rel, target in rels if rel == relation]
        return [target for _, target in rels]
    
    def query(self, query_str: str) -> list[dict]:
        """Query semantic memory."""
        results = []
        query_lower = query_str.lower()
        
        # Simple keyword matching on keys
        for key, data in self.facts.items():
            if query_lower in key.lower():
                results.append({
                    "key": key,
                    **data
                })
        
        return results
    
    def to_context_string(self, relevant_keys: Optional[list[str]] = None) -> str:
        """Convert to context string for LLM."""
        if relevant_keys:
            facts = {k: self.facts[k] for k in relevant_keys if k in self.facts}
        else:
            facts = self.facts
        
        parts = ["Known Facts:"]
        for key, data in facts.items():
            parts.append(f"  - {key}: {data['value']} (confidence: {data['confidence']})")
        
        return "\n".join(parts)


class MemoryHierarchyState(TypedDict):
    """State for memory hierarchy."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    context_assembled: str
    response: Optional[str]


class MemoryHierarchy:
    """
    Three-tier memory system for agents.
    
    Combines working (short-term), episodic (experiences), 
    and semantic (knowledge) memory for comprehensive context.
    """
    
    def __init__(
        self,
        embedding_model: Optional[Embeddings] = None,
        working_memory_size: int = 20,
        episodic_retrieval_k: int = 5
    ):
        self.working = WorkingMemory(max_messages=working_memory_size)
        self.episodic = EpisodicMemory(embedding_model=embedding_model)
        self.semantic = SemanticMemory()
        self.episodic_k = episodic_retrieval_k
    
    def retrieve_context(self, query: str, 
                         include_working: bool = True,
                         include_episodic: bool = True,
                         include_semantic: bool = True) -> dict:
        """Retrieve relevant context from all memory tiers."""
        context = {
            "working": None,
            "episodic": [],
            "semantic": []
        }
        
        if include_working:
            context["working"] = self.working.to_string()
        
        if include_episodic:
            context["episodic"] = self.episodic.retrieve(query, k=self.episodic_k)
        
        if include_semantic:
            context["semantic"] = self.semantic.query(query)
        
        return context
    
    def assemble_context(self, query: str, 
                         max_tokens: int = 2000) -> str:
        """Assemble context from all memory tiers for LLM."""
        context_parts = []
        
        # Add working memory
        working_str = self.working.to_string()
        if working_str:
            context_parts.append("## Current Context\n" + working_str)
        
        # Add episodic memories
        episodic_memories = self.episodic.retrieve(query, k=self.episodic_k)
        if episodic_memories:
            context_parts.append("## Relevant Past Experiences")
            for mem in episodic_memories:
                date_str = mem.timestamp.strftime("%Y-%m-%d")
                context_parts.append(f"- [{date_str}] {mem.content}")
        
        # Add semantic knowledge
        semantic_facts = self.semantic.query(query)
        if semantic_facts:
            context_parts.append("## Relevant Knowledge")
            for fact in semantic_facts:
                context_parts.append(f"- {fact['key']}: {fact['value']}")
        
        return "\n\n".join(context_parts)
    
    def store_interaction(self, user_message: str, 
                         assistant_response: str,
                         session_id: str = "default",
                         metadata: Optional[dict] = None):
        """Store a complete interaction across memory tiers."""
        # Update working memory
        self.working.add_message(HumanMessage(content=user_message))
        self.working.add_message(AIMessage(content=assistant_response))
        
        # Store in episodic memory
        combined = f"User: {user_message}\nAssistant: {assistant_response}"
        meta = {"session_id": session_id, **(metadata or {})}
        self.episodic.store(combined, source="conversation", metadata=meta)
    
    def learn_fact(self, key: str, value: Any, 
                   source: str = "conversation",
                   confidence: float = 0.8):
        """Learn a new fact into semantic memory."""
        self.semantic.add_fact(key, value, source=source, confidence=confidence)
    
    def clear_working_memory(self):
        """Clear only working memory (keep episodic/semantic)."""
        self.working.clear()
