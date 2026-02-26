"""
ReAct Loop Implementation
A clean implementation of the Reasoning + Acting pattern using LangGraph.
"""

from typing import TypedDict, Annotated, Sequence, Callable, Any
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool


class ReActState(TypedDict):
    """State for the ReAct agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    thoughts: list[str]
    actions: list[dict]
    observations: list[str]
    final_answer: str | None
    step_count: int


class ReActAgent:
    """
    ReAct Agent implementing the Reasoning + Acting loop.
    
    The agent interleaves:
    1. Thought - reasoning about what to do
    2. Action - executing a tool
    3. Observation - processing the result
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        tools: list[BaseTool],
        max_iterations: int = 10,
        system_prompt: str | None = None
    ):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations
        
        # Default system prompt for ReAct behavior
        self.system_prompt = system_prompt or """You are a helpful assistant that solves problems step by step.

For each step, you MUST follow this format:

Thought: [Your reasoning about what to do next]
Action: [Tool name]([param1]=[value1], [param2]=[value2])
Observation: [This will be provided by the system]

Available tools:
{tools}

When you have the final answer, respond with:
Final Answer: [Your answer]

Always think step by step. Be thorough in your reasoning."""
        
        # Build the state graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state machine."""
        
        # Define nodes
        def think(state: ReActState) -> ReActState:
            """Generate a thought about what to do next."""
            messages = list(state["messages"])
            
            # Format tool descriptions
            tool_desc = "\n".join([
                f"- {name}: {tool.description}"
                for name, tool in self.tools.items()
            ])
            
            # Add system prompt with tool info
            if not any(isinstance(m, SystemMessage) for m in messages):
                system_msg = SystemMessage(
                    content=self.system_prompt.format(tools=tool_desc)
                )
                messages = [system_msg] + messages
            
            # Get LLM response
            response = self.llm.invoke(messages)
            content = response.content
            
            # Parse thought
            thought = ""
            if "Thought:" in content:
                thought = content.split("Thought:")[1].split("Action:")[0].strip()
            elif "Final Answer:" not in content:
                thought = content.strip()
            
            return {
                **state,
                "messages": messages + [AIMessage(content=content)],
                "thoughts": state["thoughts"] + [thought] if thought else state["thoughts"],
                "step_count": state["step_count"] + 1
            }
        
        def act(state: ReActState) -> ReActState:
            """Execute the action specified by the LLM."""
            last_message = state["messages"][-1].content
            
            # Check if we have a final answer
            if "Final Answer:" in last_message:
                answer = last_message.split("Final Answer:")[1].strip()
                return {
                    **state,
                    "final_answer": answer
                }
            
            # Parse action
            action_str = ""
            if "Action:" in last_message:
                action_part = last_message.split("Action:")[1]
                if "Observation:" in action_part:
                    action_str = action_part.split("Observation:")[0].strip()
                else:
                    action_str = action_part.strip()
            
            if not action_str:
                return {
                    **state,
                    "observations": state["observations"] + ["No action specified"]
                }
            
            # Parse tool name and arguments
            # Format: tool_name(param1=value1, param2=value2)
            try:
                tool_name = action_str.split("(")[0].strip()
                args_str = action_str.split("(")[1].rstrip(")")
                
                # Parse arguments
                args = {}
                if args_str:
                    for arg in args_str.split(","):
                        if "=" in arg:
                            key, value = arg.split("=", 1)
                            args[key.strip()] = value.strip().strip('"\'')
                
                # Execute tool
                if tool_name in self.tools:
                    tool = self.tools[tool_name]
                    result = tool.invoke(args)
                    observation = str(result)
                else:
                    observation = f"Error: Tool '{tool_name}' not found"
                
                return {
                    **state,
                    "actions": state["actions"] + [{"tool": tool_name, "args": args}],
                    "observations": state["observations"] + [observation],
                }
            except Exception as e:
                return {
                    **state,
                    "observations": state["observations"] + [f"Error executing action: {e}"]
                }
        
        def observe(state: ReActState) -> ReActState:
            """Add observation to messages for next iteration."""
            if state["observations"]:
                last_obs = state["observations"][-1]
                obs_message = HumanMessage(content=f"Observation: {last_obs}")
                return {
                    **state,
                    "messages": list(state["messages"]) + [obs_message]
                }
            return state
        
        # Define routing logic
        def should_continue(state: ReActState) -> str:
            """Determine if we should continue or end."""
            if state["final_answer"] is not None:
                return "end"
            if state["step_count"] >= self.max_iterations:
                return "end"
            return "continue"
        
        # Build graph
        workflow = StateGraph(ReActState)
        
        # Add nodes
        workflow.add_node("think", think)
        workflow.add_node("act", act)
        workflow.add_node("observe", observe)
        
        # Add edges
        workflow.set_entry_point("think")
        workflow.add_edge("think", "act")
        workflow.add_edge("act", "observe")
        workflow.add_conditional_edges(
            "observe",
            should_continue,
            {
                "continue": "think",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def run(self, query: str) -> dict:
        """Run the ReAct agent on a query."""
        initial_state: ReActState = {
            "messages": [HumanMessage(content=query)],
            "thoughts": [],
            "actions": [],
            "observations": [],
            "final_answer": None,
            "step_count": 0
        }
        
        result = self.graph.invoke(initial_state)
        return result
    
    def stream(self, query: str):
        """Stream the ReAct execution steps."""
        initial_state: ReActState = {
            "messages": [HumanMessage(content=query)],
            "thoughts": [],
            "actions": [],
            "observations": [],
            "final_answer": None,
            "step_count": 0
        }
        
        for event in self.graph.stream(initial_state):
            yield event
