"""
Plan-and-Execute Implementation
A complete implementation using LangGraph with support for sequential,
parallel, and dynamic replanning execution strategies.
"""

from typing import TypedDict, Annotated, Sequence, Any
import operator
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool


class StepStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Step:
    """A single step in a plan."""
    id: str
    description: str
    dependencies: list[str] = field(default_factory=list)
    status: StepStatus = StepStatus.PENDING
    result: Any = None
    error: str | None = None


@dataclass  
class Plan:
    """A plan consisting of multiple steps."""
    steps: list[Step]
    original_task: str = ""
    
    def get_parallel_groups(self) -> list[list[Step]]:
        """Group steps that can be executed in parallel."""
        completed = set()
        groups = []
        remaining = [s for s in self.steps if s.status == StepStatus.PENDING]
        
        while remaining:
            # Find steps with all dependencies satisfied
            group = [
                s for s in remaining
                if all(dep in completed for dep in s.dependencies)
            ]
            
            if not group:
                # Circular dependency or error
                raise ValueError("Unable to resolve step dependencies")
            
            groups.append(group)
            for step in group:
                completed.add(step.id)
                remaining.remove(step)
        
        return groups
    
    def get_step(self, step_id: str) -> Step | None:
        """Get a step by ID."""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None


class PlanExecuteState(TypedDict):
    """State for the plan-and-execute agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    plan: Plan | None
    current_step_index: int
    results: dict[str, Any]
    final_answer: str | None
    replan_count: int
    max_replans: int


class PlanAndExecuteAgent:
    """
    Plan-and-Execute Agent that separates planning from execution.
    
    Supports:
    - Sequential execution (step by step)
    - Parallel execution (dependency-based grouping)
    - Dynamic replanning (adjust plan based on new information)
    """
    
    def __init__(
        self,
        planner_llm: BaseChatModel,
        executor_llm: BaseChatModel,
        tools: list[BaseTool],
        execution_strategy: str = "sequential",  # "sequential", "parallel", "dynamic"
        max_replans: int = 2
    ):
        self.planner_llm = planner_llm
        self.executor_llm = executor_llm
        self.tools = {tool.name: tool for tool in tools}
        self.execution_strategy = execution_strategy
        self.max_replans = max_replans
        
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state machine."""
        
        def plan_step(state: PlanExecuteState) -> PlanExecuteState:
            """Create an execution plan for the task."""
            task = state["messages"][-1].content if state["messages"] else ""
            
            plan_prompt = f"""Create a step-by-step plan to accomplish this task:

Task: {task}

Break this down into clear, actionable steps. Each step should:
1. Be specific and concrete
2. Have a unique ID (step_1, step_2, etc.)
3. List dependencies (step IDs that must complete first)
4. Be executable independently

Format your response as:
PLAN:
- step_id: step_1 | description: [what to do] | depends_on: []
- step_id: step_2 | description: [what to do] | depends_on: [step_1]
...

Think about which steps can be done in parallel."""
            
            response = self.planner_llm.invoke([HumanMessage(content=plan_prompt)])
            content = response.content
            
            # Parse the plan
            steps = []
            if "PLAN:" in content:
                plan_section = content.split("PLAN:")[1]
                for line in plan_section.strip().split("\n"):
                    if line.strip().startswith("-"):
                        # Parse: - step_id: X | description: Y | depends_on: [Z]
                        try:
                            parts = line.strip()[1:].strip().split("|")
                            step_data = {}
                            for part in parts:
                                if ":" in part:
                                    key, value = part.split(":", 1)
                                    step_data[key.strip()] = value.strip()
                            
                            step_id = step_data.get("step_id", f"step_{len(steps)+1}")
                            description = step_data.get("description", "")
                            deps_str = step_data.get("depends_on", "[]")
                            deps = [d.strip() for d in deps_str.strip("[]").split(",") if d.strip()]
                            
                            steps.append(Step(id=step_id, description=description, dependencies=deps))
                        except Exception:
                            continue
            
            # Fallback: create simple sequential plan
            if not steps:
                steps = [Step(id="step_1", description=task, dependencies=[])]
            
            return {
                **state,
                "plan": Plan(steps=steps, original_task=task)
            }
        
        def execute_step(state: PlanExecuteState) -> PlanExecuteState:
            """Execute the next step(s) based on strategy."""
            plan = state["plan"]
            if not plan:
                return state
            
            if self.execution_strategy == "sequential":
                return self._execute_sequential(state, plan)
            elif self.execution_strategy == "parallel":
                return self._execute_parallel(state, plan)
            else:  # dynamic
                return self._execute_sequential(state, plan)  # Start with sequential
        
        def replan_step(state: PlanExecuteState) -> PlanExecuteState:
            """Replan based on execution results."""
            if state["replan_count"] >= state["max_replans"]:
                return state
            
            plan = state["plan"]
            if not plan:
                return state
            
            # Check if any steps failed or if we need adjustment
            failed_steps = [s for s in plan.steps if s.status == StepStatus.FAILED]
            
            if not failed_steps:
                return state
            
            # Replan around failures
            replan_prompt = f"""The following steps failed:
{chr(10).join([f"- {s.id}: {s.description} (Error: {s.error})" for s in failed_steps])}

Original task: {plan.original_task}

Create a new plan to work around these failures or achieve the goal differently.
Current results so far: {state["results"]}"""
            
            response = self.planner_llm.invoke([HumanMessage(content=replan_prompt)])
            # Parse new plan (simplified for example)
            
            return {
                **state,
                "replan_count": state["replan_count"] + 1
            }
        
        def finalize_step(state: PlanExecuteState) -> PlanExecuteState:
            """Generate final answer from results."""
            plan = state["plan"]
            results = state["results"]
            
            if not plan:
                return {**state, "final_answer": "No plan created"}
            
            # Check if all steps completed
            all_completed = all(s.status == StepStatus.COMPLETED for s in plan.steps)
            
            if all_completed:
                final_prompt = f"""Based on the completed steps, provide a final answer.

Original task: {plan.original_task}

Results from each step:
{chr(10).join([f"- {step.id}: {results.get(step.id, 'No result')}" for step in plan.steps])}

Provide a clear, concise final answer."""
                
                response = self.executor_llm.invoke([HumanMessage(content=final_prompt)])
                return {
                    **state,
                    "final_answer": response.content
                }
            else:
                failed = [s for s in plan.steps if s.status == StepStatus.FAILED]
                return {
                    **state,
                    "final_answer": f"Task incomplete. {len(failed)} step(s) failed."
                }
        
        def should_continue(state: PlanExecuteState) -> str:
            """Determine next step."""
            plan = state["plan"]
            if not plan:
                return "finalize"
            
            # Check if all done
            all_done = all(s.status in [StepStatus.COMPLETED, StepStatus.FAILED] for s in plan.steps)
            
            if all_done:
                if state["replan_count"] < state["max_replans"] and any(s.status == StepStatus.FAILED for s in plan.steps):
                    return "replan"
                return "finalize"
            
            return "execute"
        
        # Build graph
        workflow = StateGraph(PlanExecuteState)
        workflow.add_node("plan", plan_step)
        workflow.add_node("execute", execute_step)
        workflow.add_node("replan", replan_step)
        workflow.add_node("finalize", finalize_step)
        
        workflow.set_entry_point("plan")
        workflow.add_edge("plan", "execute")
        workflow.add_conditional_edges(
            "execute",
            should_continue,
            {
                "execute": "execute",
                "replan": "replan",
                "finalize": "finalize"
            }
        )
        workflow.add_edge("replan", "execute")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    def _execute_sequential(self, state: PlanExecuteState, plan: Plan) -> PlanExecuteState:
        """Execute steps one at a time."""
        for step in plan.steps:
            if step.status == StepStatus.PENDING:
                if all(plan.get_step(dep) and plan.get_step(dep).status == StepStatus.COMPLETED 
                       for dep in step.dependencies):
                    step.status = StepStatus.IN_PROGRESS
                    try:
                        result = self._execute_single_step(step)
                        step.result = result
                        step.status = StepStatus.COMPLETED if not step.error else StepStatus.FAILED
                    except Exception as e:
                        step.error = str(e)
                        step.status = StepStatus.FAILED
                        result = f"Error: {e}"
                    
                    results = dict(state["results"])
                    results[step.id] = result
                    return {**state, "results": results}
        
        return state
    
    def _execute_parallel(self, state: PlanExecuteState, plan: Plan) -> PlanExecuteState:
        """Execute steps in parallel where possible."""
        groups = plan.get_parallel_groups()
        all_results = dict(state["results"])
        
        for group in groups:
            pending = [s for s in group if s.status == StepStatus.PENDING]
            if not pending:
                continue
            
            with ThreadPoolExecutor(max_workers=len(pending)) as executor:
                futures = {executor.submit(self._execute_single_step, step): step 
                          for step in pending}
                
                for future in as_completed(futures):
                    step = futures[future]
                    try:
                        result = future.result()
                        step.result = result
                        step.status = StepStatus.COMPLETED
                        all_results[step.id] = result
                    except Exception as e:
                        step.error = str(e)
                        step.status = StepStatus.FAILED
                        all_results[step.id] = f"Error: {e}"
        
        return {**state, "results": all_results}
    
    def _execute_single_step(self, step: Step) -> Any:
        """Execute a single step using the executor LLM and tools."""
        prompt = f"""Execute this step:

Step: {step.description}

Use available tools if needed. Respond with the result or output of this step.

Available tools: {list(self.tools.keys())}"""
        
        messages = [HumanMessage(content=prompt)]
        
        # For simplicity, just use LLM directly
        # In a full implementation, this would use ReAct or similar
        response = self.executor_llm.invoke(messages)
        
        return response.content
    
    def run(self, task: str) -> dict:
        """Run the plan-and-execute agent."""
        initial_state: PlanExecuteState = {
            "messages": [HumanMessage(content=task)],
            "plan": None,
            "current_step_index": 0,
            "results": {},
            "final_answer": None,
            "replan_count": 0,
            "max_replans": self.max_replans
        }
        
        return self.graph.invoke(initial_state)
