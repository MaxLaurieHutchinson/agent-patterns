"""
Multi-Agent Debate Implementation
Implements a multi-agent debate system with configurable agents,
debate rounds, and termination conditions.
"""

from typing import TypedDict, Annotated, Sequence, Any, Callable
import operator
from dataclasses import dataclass, field
from enum import Enum

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseChatModel


class AgentRole(Enum):
    PROPOSER = "proposer"
    CRITIC = "critic"
    EXPERT = "expert"
    SYNTHESIZER = "synthesizer"
    JUDGE = "judge"


@dataclass
class DebateAgent:
    """Configuration for a debate participant."""
    name: str
    role: AgentRole
    system_prompt: str
    llm: BaseChatModel
    priority: int = 0  # Higher = speaks earlier
    
    def generate_response(self, context: list[BaseMessage]) -> str:
        """Generate a response given the debate context."""
        messages = [SystemMessage(content=self.system_prompt)] + list(context)
        response = self.llm.invoke(messages)
        return response.content


@dataclass
class DebateMessage:
    """A single message in the debate."""
    agent_name: str
    role: AgentRole
    content: str
    round_num: int


class DebateState(TypedDict):
    """State for the multi-agent debate."""
    original_query: str
    messages: Annotated[Sequence[BaseMessage], operator.add]
    debate_history: list[DebateMessage]
    current_round: int
    max_rounds: int
    agent_responses: dict[str, str]
    final_answer: str | None
    consensus_reached: bool
    cost_estimate: float


class MultiAgentDebate:
    """
    Multi-Agent Debate system.
    
    Manages multiple agents debating a problem, tracking context,
    and determining when to terminate with a final answer.
    """
    
    def __init__(
        self,
        agents: list[DebateAgent],
        max_rounds: int = 3,
        cost_limit: float = 1.0,  # Estimated cost in $
        consensus_threshold: float = 0.8
    ):
        self.agents = sorted(agents, key=lambda a: -a.priority)
        self.max_rounds = max_rounds
        self.cost_limit = cost_limit
        self.consensus_threshold = consensus_threshold
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the debate state machine."""
        
        def initialize(state: DebateState) -> DebateState:
            """Set up the initial debate state."""
            return {
                **state,
                "current_round": 1,
                "debate_history": [],
                "agent_responses": {},
                "consensus_reached": False,
                "cost_estimate": 0.0
            }
        
        def run_round(state: DebateState) -> DebateState:
            """Execute one round of debate."""
            debate_history = list(state["debate_history"])
            responses = dict(state["agent_responses"])
            cost = state["cost_estimate"]
            
            # Build context for this round
            context: list[BaseMessage] = [
                HumanMessage(content=f"Original question: {state['original_query']}")
            ]
            
            # Add debate history
            for msg in debate_history:
                context.append(AIMessage(
                    content=f"[{msg.agent_name} - {msg.role.value}]: {msg.content}"
                ))
            
            # Each agent responds
            for agent in self.agents:
                # Skip synthesizer and judge until final round
                if agent.role in [AgentRole.SYNTHESIZER, AgentRole.JUDGE]:
                    continue
                
                # Check cost limit
                if cost >= self.cost_limit:
                    break
                
                response = agent.generate_response(context)
                
                debate_msg = DebateMessage(
                    agent_name=agent.name,
                    role=agent.role,
                    content=response,
                    round_num=state["current_round"]
                )
                debate_history.append(debate_msg)
                responses[agent.name] = response
                
                # Estimate cost (rough approximation)
                cost += 0.002  # ~1000 tokens
                
                # Update context for next agent
                context.append(AIMessage(
                    content=f"[{agent.name}]: {response}"
                ))
            
            return {
                **state,
                "debate_history": debate_history,
                "agent_responses": responses,
                "cost_estimate": cost
            }
        
        def check_consensus(state: DebateState) -> DebateState:
            """Check if agents have reached consensus."""
            # Simple heuristic: look for agreement indicators
            # In practice, could use embeddings or LLM-based evaluation
            
            recent_responses = [
                msg.content for msg in state["debate_history"]
                if msg.round_num == state["current_round"]
            ]
            
            # Check for agreement words
            agreement_indicators = ["agree", "concur", "yes", "correct", "optimal", "best"]
            agreement_count = sum(
                1 for resp in recent_responses
                for indicator in agreement_indicators
                if indicator in resp.lower()
            )
            
            consensus = agreement_count >= len(recent_responses) * 0.5
            
            return {
                **state,
                "consensus_reached": consensus
            }
        
        def synthesize(state: DebateState) -> DebateState:
            """Synthesize all viewpoints into a coherent answer."""
            # Find synthesizer agent
            synthesizer = next(
                (a for a in self.agents if a.role == AgentRole.SYNTHESIZER),
                None
            )
            
            if not synthesizer:
                # Use first available agent
                synthesizer = self.agents[0]
            
            # Build synthesis prompt
            debate_summary = "\n\n".join([
                f"{msg.agent_name} ({msg.role.value}): {msg.content}"
                for msg in state["debate_history"]
            ])
            
            prompt = f"""Based on the following debate, synthesize a comprehensive answer:

Original Question: {state['original_query']}

Debate Transcript:
{debate_summary}

Please provide a well-reasoned final answer that incorporates the best insights from all participants."""
            
            synthesis = synthesizer.llm.invoke([
                SystemMessage(content=synthesizer.system_prompt),
                HumanMessage(content=prompt)
            ])
            
            debate_history = list(state["debate_history"])
            debate_history.append(DebateMessage(
                agent_name=synthesizer.name,
                role=AgentRole.SYNTHESIZER,
                content=synthesis.content,
                round_num=state["current_round"]
            ))
            
            return {
                **state,
                "debate_history": debate_history
            }
        
        def judge(state: DebateState) -> DebateState:
            """Make final judgment/decision."""
            judge_agent = next(
                (a for a in self.agents if a.role == AgentRole.JUDGE),
                None
            )
            
            if not judge_agent:
                # Use synthesis as final answer
                synthesis_msg = [m for m in state["debate_history"] if m.role == AgentRole.SYNTHESIZER]
                if synthesis_msg:
                    return {
                        **state,
                        "final_answer": synthesis_msg[-1].content
                    }
                # Fallback to last response
                return {
                    **state,
                    "final_answer": state["debate_history"][-1].content if state["debate_history"] else "No answer"
                }
            
            # Build judgment prompt
            context = [
                HumanMessage(content=f"Based on the debate about: {state['original_query']}"),
                HumanMessage(content="Provide the definitive final answer.")
            ]
            
            for msg in state["debate_history"]:
                context.append(AIMessage(
                    content=f"[{msg.agent_name}]: {msg.content}"
                ))
            
            judgment = judge_agent.generate_response(context)
            
            return {
                **state,
                "final_answer": judgment
            }
        
        def should_continue(state: DebateState) -> str:
            """Determine if debate should continue."""
            # Check termination conditions
            if state["consensus_reached"]:
                return "finalize"
            
            if state["current_round"] >= self.max_rounds:
                return "finalize"
            
            if state["cost_estimate"] >= self.cost_limit:
                return "finalize"
            
            return "continue"
        
        def next_round(state: DebateState) -> DebateState:
            """Increment round counter."""
            return {
                **state,
                "current_round": state["current_round"] + 1
            }
        
        # Build graph
        workflow = StateGraph(DebateState)
        workflow.add_node("initialize", initialize)
        workflow.add_node("run_round", run_round)
        workflow.add_node("check_consensus", check_consensus)
        workflow.add_node("synthesize", synthesize)
        workflow.add_node("judge", judge)
        workflow.add_node("next_round", next_round)
        
        workflow.set_entry_point("initialize")
        workflow.add_edge("initialize", "run_round")
        workflow.add_edge("run_round", "check_consensus")
        workflow.add_conditional_edges(
            "check_consensus",
            should_continue,
            {
                "continue": "next_round",
                "finalize": "synthesize"
            }
        )
        workflow.add_edge("next_round", "run_round")
        workflow.add_edge("synthesize", "judge")
        workflow.add_edge("judge", END)
        
        return workflow.compile()
    
    def run(self, query: str) -> dict:
        """Run the multi-agent debate."""
        initial_state: DebateState = {
            "original_query": query,
            "messages": [HumanMessage(content=query)],
            "debate_history": [],
            "current_round": 0,
            "max_rounds": self.max_rounds,
            "agent_responses": {},
            "final_answer": None,
            "consensus_reached": False,
            "cost_estimate": 0.0
        }
        
        return self.graph.invoke(initial_state)
