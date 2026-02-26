"""
Plan-and-Execute Example
Demonstrates using the plan-and-execute pattern for a research task.
"""

import os
from langchain_openai import ChatOpenAI
from implementation import PlanAndExecuteAgent


def print_plan_execution(result: dict):
    """Pretty print the plan and execution results."""
    print("\n" + "="*60)
    print("Plan & Execution Results")
    print("="*60)
    
    plan = result.get("plan")
    if plan:
        print(f"\n📋 Original Task: {plan.original_task}")
        print(f"\n📊 Plan Steps:")
        for step in plan.steps:
            status_icon = "✅" if step.status.value == "completed" else "❌" if step.status.value == "failed" else "⏳"
            print(f"   {status_icon} {step.id}: {step.description}")
            if step.dependencies:
                print(f"      Depends on: {', '.join(step.dependencies)}")
    
    print(f"\n📈 Results:")
    for step_id, res in result.get("results", {}).items():
        print(f"   {step_id}: {res[:100]}..." if len(str(res)) > 100 else f"   {step_id}: {res}")
    
    print(f"\n✅ Final Answer:\n{result.get('final_answer', 'No answer')}")
    print("="*60)


def main():
    """Run the plan-and-execute example."""
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable")
        print("   Running in demo mode...\n")
        demo_without_llm()
        return
    
    # Initialize LLMs
    # Use GPT-4 for planning (better reasoning)
    # Use GPT-3.5 for execution (cheaper)
    planner_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    executor_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Example tasks
    tasks = [
        "Write a short blog post about the benefits of exercise",
        "Create a plan to learn Python programming from scratch",
    ]
    
    # Test sequential execution
    print("\n" + "="*60)
    print("SEQUENTIAL EXECUTION")
    print("="*60)
    
    agent = PlanAndExecuteAgent(
        planner_llm=planner_llm,
        executor_llm=executor_llm,
        tools=[],
        execution_strategy="sequential"
    )
    
    result = agent.run(tasks[0])
    print_plan_execution(result)
    
    # Test parallel execution
    print("\n" + "="*60)
    print("PARALLEL EXECUTION")
    print("="*60)
    
    agent_parallel = PlanAndExecuteAgent(
        planner_llm=planner_llm,
        executor_llm=executor_llm,
        tools=[],
        execution_strategy="parallel"
    )
    
    result = agent_parallel.run(tasks[1])
    print_plan_execution(result)


def demo_without_llm():
    """Demonstrate the pattern without requiring LLM."""
    print("\n🎮 Mock Plan-and-Execute Demonstration\n")
    
    # Simulate a plan and execution
    mock_result = {
        "plan": type('Plan', (), {
            'original_task': 'Write a blog post about exercise',
            'steps': [
                type('Step', (), {'id': 'step_1', 'description': 'Research exercise benefits', 'status': type('Status', (), {'value': 'completed'}), 'dependencies': []}),
                type('Step', (), {'id': 'step_2', 'description': 'Outline blog structure', 'status': type('Status', (), {'value': 'completed'}), 'dependencies': ['step_1']}),
                type('Step', (), {'id': 'step_3', 'description': 'Write introduction', 'status': type('Status', (), {'value': 'completed'}), 'dependencies': ['step_2']}),
                type('Step', (), {'id': 'step_4', 'description': 'Write main content', 'status': type('Status', (), {'value': 'completed'}), 'dependencies': ['step_2']}),
                type('Step', (), {'id': 'step_5', 'description': 'Write conclusion', 'status': type('Status', (), {'value': 'completed'}), 'dependencies': ['step_3', 'step_4']}),
            ]
        })(),
        "results": {
            "step_1": "Research complete: 10 benefits identified",
            "step_2": "Outline: Intro, 3 main sections, conclusion",
            "step_3": "Introduction written (150 words)",
            "step_4": "Main content written (400 words)",
            "step_5": "Conclusion written (100 words)"
        },
        "final_answer": "Blog post complete: 650 words covering 10 benefits of exercise with introduction, three main sections, and conclusion."
    }
    
    print_plan_execution(mock_result)
    
    print("\n📝 How to use with real LLM:\n")
    print("""
    from langchain_openai import ChatOpenAI
    from implementation import PlanAndExecuteAgent
    
    planner_llm = ChatOpenAI(model="gpt-4o-mini")
    executor_llm = ChatOpenAI(model="gpt-4o-mini")
    
    agent = PlanAndExecuteAgent(
        planner_llm=planner_llm,
        executor_llm=executor_llm,
        tools=[],
        execution_strategy="parallel"
    )
    
    result = agent.run("Write a blog post about exercise")
    print(result["final_answer"])
    """)
    
    print("\n🎯 Key Benefits Demonstrated:")
    print("   1. Planner creates structured approach")
    print("   2. Steps 3 & 4 can run in parallel (both depend on step_2)")
    print("   3. Step 5 waits for both 3 & 4 to complete")
    print("   4. Clear visibility into progress")


if __name__ == "__main__":
    main()
