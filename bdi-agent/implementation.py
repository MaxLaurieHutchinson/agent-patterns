"""
BDI Agent implementation.
"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class Desire:
    name: str
    priority: int


class BDIAgent:
    def __init__(
        self,
        belief_updater: Callable[[dict, dict], dict],
        desire_generator: Callable[[dict], list[Desire]],
        intention_selector: Callable[[list[Desire]], Desire] | None = None,
    ):
        self.beliefs: dict = {}
        self.intentions: list[Desire] = []
        self._belief_updater = belief_updater
        self._desire_generator = desire_generator
        self._intention_selector = intention_selector

    def step(self, percepts: dict) -> Desire | None:
        self.beliefs = self._belief_updater(self.beliefs, percepts)
        desires = self._desire_generator(self.beliefs)
        if not desires:
            self.intentions = []
            return None

        if self._intention_selector:
            intention = self._intention_selector(desires)
        else:
            intention = max(desires, key=lambda d: d.priority)

        self.intentions = [intention]
        return intention
