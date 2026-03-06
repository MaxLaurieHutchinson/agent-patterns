"""
Rule-based decision engine.
"""

from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Rule:
    name: str
    predicate: Callable[[dict], bool]
    decision: Any


class RuleEngine:
    def __init__(self, rules: list[Rule], default: Any = None):
        self.rules = rules
        self.default = default

    def evaluate(self, inputs: dict) -> Any:
        for rule in self.rules:
            if rule.predicate(inputs):
                return rule.decision
        return self.default
