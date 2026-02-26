"""
Router + Delegation implementation.
Routes tasks to specialist handlers using simple intent rules.
"""

from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class RouteDecision:
    intent: str
    agent_name: str


@dataclass
class DelegationResult:
    intent: str
    selected_agent: str
    success: bool
    result: Any = None
    error: str | None = None


class RouterDelegation:
    def __init__(self, fallback_agent: str = "general"):
        self.fallback_agent = fallback_agent
        self.intent_rules: list[tuple[str, set[str], str]] = []
        self.handlers: dict[str, Callable[[str, dict], Any]] = {}

    def add_route(self, intent: str, keywords: list[str], agent_name: str):
        self.intent_rules.append((intent, set(k.lower() for k in keywords), agent_name))

    def register_handler(self, agent_name: str, handler: Callable[[str, dict], Any]):
        self.handlers[agent_name] = handler

    def infer_intent(self, query: str) -> RouteDecision:
        words = set(query.lower().split())
        best_score = 0
        best_decision = RouteDecision(intent="general", agent_name=self.fallback_agent)

        for intent, keywords, agent_name in self.intent_rules:
            score = len(words & keywords)
            if score > best_score:
                best_score = score
                best_decision = RouteDecision(intent=intent, agent_name=agent_name)

        return best_decision

    def delegate(self, query: str, context: dict | None = None) -> DelegationResult:
        ctx = context or {}
        decision = self.infer_intent(query)
        handler = self.handlers.get(decision.agent_name)

        if handler is None:
            return DelegationResult(
                intent=decision.intent,
                selected_agent=decision.agent_name,
                success=False,
                error=f"No handler registered for '{decision.agent_name}'",
            )

        try:
            result = handler(query, ctx)
            return DelegationResult(
                intent=decision.intent,
                selected_agent=decision.agent_name,
                success=True,
                result=result,
            )
        except Exception as e:
            return DelegationResult(
                intent=decision.intent,
                selected_agent=decision.agent_name,
                success=False,
                error=str(e),
            )
