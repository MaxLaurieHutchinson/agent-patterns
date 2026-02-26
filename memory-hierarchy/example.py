"""
Memory Hierarchy Example
Demonstrates the three-tier memory system.
"""

import os
from datetime import datetime, timedelta
from implementation import (
    MemoryHierarchy, WorkingMemory, EpisodicMemory, 
    SemanticMemory, MemoryEntry
)


def demo_working_memory():
    """Demonstrate working memory."""
    print("\n" + "="*60)
    print("WORKING MEMORY DEMO")
    print("="*60)
    
    from langchain_core.messages import HumanMessage, AIMessage
    
    working = WorkingMemory(max_messages=5)
    
    # Simulate a conversation
    print("\n📝 Adding messages to working memory...")
    messages = [
        ("user", "Hi, I need help with Python"),
        ("assistant", "I'd be happy to help! What specifically?"),
        ("user", "How do I use decorators?"),
        ("assistant", "Decorators are functions that modify other functions..."),
        ("user", "Can you show an example?"),
        ("assistant", "Here's a simple example..."),
        ("user", "Thanks, that helps!"),
    ]
    
    for role, content in messages:
        msg = HumanMessage(content=content) if role == "user" else AIMessage(content=content)
        working.add_message(msg)
        print(f"   {role}: {content[:50]}...")
    
    print(f"\n📊 Working memory size: {len(working.messages)} (max: {working.max_messages})")
    print(f"   Oldest messages automatically removed")
    
    # Add goals and context
    working.set_goal("Teach Python decorators")
    working.update_context("topic", "Python decorators")
    working.update_context("skill_level", "beginner")
    
    print("\n🎯 Active Goals:", working.current_goals)
    print("📋 Active Context:", working.active_context)
    
    print("\n📄 Working Memory Context String:")
    print("-"*60)
    print(working.to_string())


def demo_episodic_memory():
    """Demonstrate episodic memory."""
    print("\n" + "="*60)
    print("EPISODIC MEMORY DEMO")
    print("="*60)
    
    episodic = EpisodicMemory()
    
    # Store some experiences
    print("\n💾 Storing experiences...")
    experiences = [
        ("User prefers concise answers", {"session_id": "s1", "topic": "preferences"}),
        ("Discussed Python decorators on Tuesday", {"session_id": "s1", "topic": "python"}),
        ("User is learning web development", {"session_id": "s2", "topic": "career"}),
        ("Showed examples of Flask routes", {"session_id": "s2", "topic": "flask"}),
        ("User likes visual explanations", {"session_id": "s1", "topic": "preferences"}),
    ]
    
    for content, meta in experiences:
        episodic.store(content, source="conversation", metadata=meta, importance=0.8)
        print(f"   Stored: {content}")
    
    # Retrieve relevant memories
    print("\n🔍 Retrieving memories for query 'Python':")
    results = episodic.retrieve("Python", k=3)
    for i, mem in enumerate(results, 1):
        print(f"   {i}. {mem.content} (importance: {mem.importance})")
    
    print("\n🔍 Retrieving memories for query 'user preferences':")
    results = episodic.retrieve("user preferences", k=3)
    for i, mem in enumerate(results, 1):
        print(f"   {i}. {mem.content}")


def demo_semantic_memory():
    """Demonstrate semantic memory."""
    print("\n" + "="*60)
    print("SEMANTIC MEMORY DEMO")
    print("="*60)
    
    semantic = SemanticMemory()
    
    # Add facts
    print("\n🧠 Adding facts to semantic memory...")
    facts = [
        ("user.name", "Alice", "user_profile", 1.0),
        ("user.expertise", "Python, JavaScript", "user_profile", 0.9),
        ("project.website_redesign.status", "In Progress", "project_tracking", 1.0),
        ("project.website_redesign.deadline", "2024-03-15", "project_tracking", 1.0),
        ("company.tech_stack", "Python, React, PostgreSQL", "company_info", 0.95),
    ]
    
    for key, value, source, confidence in facts:
        semantic.add_fact(key, value, source=source, confidence=confidence)
        print(f"   {key} = {value}")
    
    # Add relationships
    semantic.add_relationship("user", "works_on", "project.website_redesign")
    semantic.add_relationship("project.website_redesign", "uses", "company.tech_stack")
    
    # Query facts
    print("\n🔍 Querying facts for 'project':")
    results = semantic.query("project")
    for fact in results:
        print(f"   - {fact['key']}: {fact['value']}")
    
    print("\n🔗 Relationships from 'user':")
    related = semantic.query_relationship("user")
    for target in related:
        print(f"   - user works_on {target}")
    
    print("\n📄 Semantic Memory Context:")
    print("-"*60)
    print(semantic.to_context_string())


def demo_full_hierarchy():
    """Demonstrate the complete memory hierarchy."""
    print("\n" + "="*60)
    print("FULL MEMORY HIERARCHY DEMO")
    print("="*60)
    
    # Create hierarchy
    memory = MemoryHierarchy(working_memory_size=10)
    
    # Simulate previous interactions
    print("\n💾 Simulating previous session...")
    memory.episodic.store(
        "User is working on website redesign project",
        source="conversation",
        metadata={"session_id": "prev_session"},
        importance=0.9
    )
    memory.episodic.store(
        "User prefers detailed technical explanations",
        source="conversation",
        metadata={"session_id": "prev_session"},
        importance=0.8
    )
    
    # Add semantic knowledge
    memory.semantic.add_fact("user.role", "Frontend Developer", confidence=0.9)
    memory.semantic.add_fact("project.website.stack", "React, Node.js", confidence=1.0)
    
    # Current session
    print("\n📝 Current session interaction...")
    user_msg = "What's the best way to handle state in React?"
    assistant_msg = "For React state management, you have several options..."
    
    memory.store_interaction(user_msg, assistant_msg, session_id="current_session")
    memory.working.set_goal("Teach React state management")
    
    # Retrieve context
    print("\n🔍 Assembling context for query 'React state':")
    context = memory.assemble_context("React state")
    print("-"*60)
    print(context)
    
    # Learn from interaction
    memory.learn_fact("user.interest", "React state management", confidence=0.8)
    
    print("\n✅ Learned new fact:")
    print(f"   user.interest = {memory.semantic.get_fact('user.interest')}")


def demo_memory_consolidation():
    """Demonstrate memory consolidation."""
    print("\n" + "="*60)
    print("MEMORY CONSOLIDATION DEMO")
    print("="*60)
    
    episodic = EpisodicMemory()
    
    # Add old and new memories
    print("\n💾 Adding memories from different times...")
    
    old_time = datetime.now() - timedelta(days=60)
    new_time = datetime.now()
    
    # Old memory
    old_mem = MemoryEntry(
        content="Old project discussion",
        timestamp=old_time,
        source="conversation",
        importance=0.5
    )
    episodic.memories.append(old_mem)
    
    # Recent memories
    for i in range(3):
        new_mem = MemoryEntry(
            content=f"Recent discussion {i+1}",
            timestamp=new_time - timedelta(hours=i),
            source="conversation",
            importance=0.8
        )
        episodic.memories.append(new_mem)
    
    print(f"   Total memories: {len(episodic.memories)}")
    print(f"   Oldest: {old_mem.timestamp}")
    
    # Consolidate (remove old)
    print("\n🧹 Consolidating (removing memories > 30 days)...")
    episodic.forget_old(days=30)
    print(f"   Remaining memories: {len(episodic.memories)}")
    
    # Show recency scoring
    print("\n📊 Recency scores:")
    for mem in episodic.memories:
        score = episodic._recency_score(mem.timestamp)
        print(f"   {mem.content}: {score:.3f}")


def main():
    """Run all memory hierarchy demos."""
    print("\n" + "="*60)
    print("MEMORY HIERARCHY PATTERN DEMONSTRATION")
    print("="*60)
    
    demo_working_memory()
    demo_episodic_memory()
    demo_semantic_memory()
    demo_full_hierarchy()
    demo_memory_consolidation()
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)
    
    print("""
📝 Key Concepts Demonstrated:

1. WORKING MEMORY
   - Short-term context (last N messages)
   - Active goals and context
   - Fast, ephemeral access

2. EPISODIC MEMORY  
   - Long-term experiences
   - Similarity-based retrieval
   - Importance weighting
   - Recency scoring

3. SEMANTIC MEMORY
   - Structured facts and knowledge
   - Entity relationships
   - Confidence tracking

4. MEMORY HIERARCHY
   - Combines all three tiers
   - Context assembly for LLM
   - Learning from interactions
   - Automatic consolidation
""")


if __name__ == "__main__":
    main()
