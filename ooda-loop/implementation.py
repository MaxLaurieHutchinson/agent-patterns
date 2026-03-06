"""
OODA Loop implementation.
"""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class OODAStep:
    observation: Any
    orientation: Any
    decision: Any
    action: Any


@dataclass
class OODAResult:
    steps: list[OODAStep]
    final_decision: Any


class OODALoop:
    def __init__(self, max_iters: int = 10):
        self.max_iters = max_iters

    def run(
        self,
        observe: Callable[[], Any],
        orient: Callable[[Any, dict], Any],
        decide: Callable[[Any, dict], Any],
        act: Callable[[Any, dict], Any],
        max_iters: int | None = None,
    ) -> OODAResult:
        limit = max_iters if max_iters is not None else self.max_iters
        steps: list[OODAStep] = []
        context: dict = {}

        for _ in range(limit):
            observation = observe()
            orientation = orient(observation, context)
            decision = decide(orientation, context)
            action = act(decision, context)
            steps.append(OODAStep(observation, orientation, decision, action))
            context = {
                "observation": observation,
                "orientation": orientation,
                "decision": decision,
                "action": action,
            }

        final_decision = steps[-1].decision if steps else None
        return OODAResult(steps=steps, final_decision=final_decision)
