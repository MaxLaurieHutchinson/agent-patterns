"""
Multi-Agent Debate Example
Demonstrates using multiple agents to debate a design decision.
"""

import os
from langchain_openai import ChatOpenAI
from implementation import MultiAgentDebate, DebateAgent, AgentRole


def print_debate_result(result: dict):
    """Pretty print the debate results."""
    print("\n" + "="*70)
    print("Multi-Agent Debate Results")
    print("="*70)
    
    print(f"\n🎯 Original Question: {result.get('original_query', 'N/A')}")
    print(f"📊 Rounds Completed: {result.get('current_round', 0)}")
    print(f"💰 Estimated Cost: ${result.get('cost_estimate', 0):.3f}")
    print(f"✅ Consensus Reached: {result.get('consensus_reached', False)}")
    
    print(f"\n📝 Debate Transcript:")
    print("-"*70)
    
    for msg in result.get("debate_history", []):
        role_icon = {
            AgentRole.PROPOSER: "💡",
            AgentRole.CRITIC: "🔍",
            AgentRole.EXPERT: "🎓",
            AgentRole.SYNTHESIZER: "🔄",
            AgentRole.JUDGE: "⚖️"
        }.get(msg.role, "🤖")
        
        print(f"\n{role_icon} Round {msg.round_num} - {msg.agent_name} ({msg.role.value}):")
        print(f"   {msg.content[:200]}..." if len(msg.content) > 200 else f"   {msg.content}")
    
    print("\n" + "-"*70)
    print(f"🏆 FINAL ANSWER:\n{result.get('final_answer', 'No answer generated')}")
    print("="*70)


def main():
    """Run the multi-agent debate example."""
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable")
        print("   Running in demo mode...\n")
        demo_without_llm()
        return
    
    # Create agents with different roles
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    agents = [
        DebateAgent(
            name="Alice",
            role=AgentRole.PROPOSER,
            system_prompt="""You are a creative problem solver who proposes innovative solutions.
Focus on suggesting practical, implementable ideas. Be bold but reasonable.""",
            llm=llm,
            priority=3
        ),
        DebateAgent(
            name="Bob",
            role=AgentRole.CRITIC,
            system_prompt="""You are a critical thinker who identifies flaws and edge cases.
Challenge assumptions and point out potential problems. Be constructive but thorough.""",
            llm=llm,
            priority=2
        ),
        DebateAgent(
            name="Carol",
            role=AgentRole.EXPERT,
            system_prompt="""You are a technical expert with deep domain knowledge.
Provide authoritative guidance on best practices and technical feasibility.""",
            llm=llm,
            priority=1
        ),
        DebateAgent(
            name="Diana",
            role=AgentRole.SYNTHESIZER,
            system_prompt="""You excel at combining multiple viewpoints into coherent solutions.
Find common ground and integrate the best ideas from all perspectives.""",
            llm=llm,
            priority=0
        ),
        DebateAgent(
            name="Edward",
            role=AgentRole.JUDGE,
            system_prompt="""You make final decisions based on all presented arguments.
Be fair, balanced, and provide clear reasoning for your judgment.""",
            llm=llm,
            priority=0
        )
    ]
    
    # Example debate topics
    topics = [
        "What is the best architecture for a real-time chat application?",
        "Should we use microservices or a monolith for a startup's MVP?",
    ]
    
    # Run debates
    debate = MultiAgentDebate(
        agents=agents,
        max_rounds=2,
        cost_limit=0.5
    )
    
    for topic in topics:
        print(f"\n🚀 Starting debate on: {topic}")
        result = debate.run(topic)
        print_debate_result(result)


def demo_without_llm():
    """Demonstrate the pattern without requiring LLM."""
    print("\n🎮 Mock Multi-Agent Debate Demonstration\n")
    
    # Simulate a debate
    from implementation import DebateMessage
    
    mock_result = {
        "original_query": "Should we use microservices or monolith?",
        "current_round": 2,
        "cost_estimate": 0.05,
        "consensus_reached": True,
        "debate_history": [
            DebateMessage(
                agent_name="Alice",
                role=AgentRole.PROPOSER,
                content="I propose starting with a modular monolith. It gives us clear boundaries while avoiding operational complexity.",
                round_num=1
            ),
            DebateMessage(
                agent_name="Bob",
                role=AgentRole.CRITIC,
                content="A monolith could become unmanageable. However, you're right about operational complexity. Maybe we need a middle ground?",
                round_num=1
            ),
            DebateMessage(
                agent_name="Carol",
                role=AgentRole.EXPERT,
                content="From a technical perspective, modular monoliths are gaining popularity. They allow migration to microservices later.",
                round_num=1
            ),
            DebateMessage(
                agent_name="Alice",
                role=AgentRole.PROPOSER,
                content="Exactly! We can design service boundaries now but deploy as one unit. When we need to scale independently, we extract services.",
                round_num=2
            ),
            DebateMessage(
                agent_name="Bob",
                role=AgentRole.CRITIC,
                content="That addresses my concerns. The modular approach gives us flexibility without premature optimization.",
                round_num=2
            ),
            DebateMessage(
                agent_name="Diana",
                role=AgentRole.SYNTHESIZER,
                content="Combining these views: Start modular monolith with clear service boundaries. Plan for future extraction but don't pay microservices tax yet.",
                round_num=2
            ),
        ],
        "final_answer": "Use a modular monolith architecture. Design internal APIs as if they were services, but deploy as single unit. This provides clean boundaries while avoiding operational complexity. Migrate to microservices only when specific scaling needs emerge."
    }
    
    print_debate_result(mock_result)
    
    print("\n📝 How to use with real LLM:\n")
    print("""
    from langchain_openai import ChatOpenAI
    from implementation import MultiAgentDebate, DebateAgent, AgentRole
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    agents = [
        DebateAgent(
            name="Alice",
            role=AgentRole.PROPOSER,
            system_prompt="You propose creative solutions...",
            llm=llm
        ),
        DebateAgent(
            name="Bob",
            role=AgentRole.CRITIC,
            system_prompt="You identify flaws and edge cases...",
            llm=llm
        ),
        # ... more agents
    ]
    
    debate = MultiAgentDebate(agents=agents, max_rounds=3)
    result = debate.run("What architecture should we use?")
    print(result["final_answer"])
    """)
    
    print("\n🎯 Key Benefits Demonstrated:")
    print("   1. Multiple perspectives (Proposer, Critic, Expert)")
    print("   2. Iterative refinement through debate rounds")
    print("   3. Synthesis of best ideas")
    print("   4. Final authoritative judgment")
    print("   5. Cost tracking and limits")


if __name__ == "__main__":
    main()
