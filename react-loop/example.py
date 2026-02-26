"""
ReAct Loop Example
Demonstrates using the ReAct pattern for a calculation task.
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

# Import the ReAct implementation
from implementation import ReActAgent, ReActState


# Define some simple tools for demonstration
class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression to evaluate")


class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Evaluates mathematical expressions. Use for calculations."
    args_schema: type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """Evaluate the expression."""
        try:
            # Safe evaluation - only allow basic math
            allowed = set("0123456789+-*/.() ")
            if not all(c in allowed for c in expression):
                return "Error: Invalid characters in expression"
            result = eval(expression)
            return f"{result}"
        except Exception as e:
            return f"Error: {e}"


class SearchInput(BaseModel):
    query: str = Field(description="Search query")


class SearchTool(BaseTool):
    """Mock search tool for demonstration."""
    name: str = "search"
    description: str = "Searches for information. Use for factual queries."
    args_schema: type[BaseModel] = SearchInput
    
    def _run(self, query: str) -> str:
        """Mock search results."""
        knowledge = {
            "population of france": "68 million",
            "capital of japan": "Tokyo",
            "speed of light": "299,792,458 m/s"
        }
        for key, value in knowledge.items():
            if key in query.lower():
                return value
        return f"No results found for '{query}'"


def print_execution_trace(result: dict):
    """Pretty print the ReAct execution trace."""
    print("\n" + "="*60)
    print("ReAct Execution Trace")
    print("="*60)
    
    thoughts = result.get("thoughts", [])
    actions = result.get("actions", [])
    observations = result.get("observations", [])
    
    for i, thought in enumerate(thoughts):
        print(f"\n🤔 Step {i+1}:")
        print(f"   Thought: {thought}")
        
        if i < len(actions):
            action = actions[i]
            print(f"   Action: {action['tool']}{action['args']}")
        
        if i < len(observations):
            print(f"   Observation: {observations[i]}")
    
    print(f"\n✅ Final Answer: {result.get('final_answer', 'No answer generated')}")
    print("="*60)


def main():
    """Run the ReAct example."""
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable")
        print("   Using mock mode for demonstration...\n")
        demo_without_llm()
        return
    
    # Initialize LLM and tools
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [CalculatorTool(), SearchTool()]
    
    # Create ReAct agent
    agent = ReActAgent(
        llm=llm,
        tools=tools,
        max_iterations=5
    )
    
    # Example queries
    queries = [
        "What is 123 * 456?",
        "Calculate (100 + 50) * 2, then add 25",
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        result = agent.run(query)
        print_execution_trace(result)


def demo_without_llm():
    """Demonstrate ReAct pattern without requiring LLM."""
    print("\n🎮 Mock ReAct Demonstration\n")
    
    # Simulate a ReAct trace manually
    mock_result = {
        "thoughts": [
            "I need to calculate 123 * 456",
            "The calculator returned 56088, which is the final answer"
        ],
        "actions": [
            {"tool": "calculator", "args": {"expression": "123 * 456"}}
        ],
        "observations": [
            "56088",
        ],
        "final_answer": "123 * 456 = 56088"
    }
    
    print_execution_trace(mock_result)
    
    print("\n📝 How to use with real LLM:\n")
    print("""
    from langchain_openai import ChatOpenAI
    from implementation import ReActAgent
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    tools = [CalculatorTool(), SearchTool()]
    
    agent = ReActAgent(llm=llm, tools=tools)
    result = agent.run("What is 123 * 456?")
    
    print(result["final_answer"])
    """)


if __name__ == "__main__":
    main()
