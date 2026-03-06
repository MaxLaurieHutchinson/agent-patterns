"""
Finite state machine implementation.
"""

from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Transition:
    next_state: str
    handler: Callable[[Any], Any] | None = None


class FiniteStateMachine:
    def __init__(self, initial_state: str):
        self.state = initial_state
        self.transitions: dict[tuple[str, str], Transition] = {}

    def add_transition(self, state: str, event: str, next_state: str, handler: Callable[[Any], Any] | None = None):
        self.transitions[(state, event)] = Transition(next_state=next_state, handler=handler)

    def transition(self, event: str, payload: Any | None = None):
        key = (self.state, event)
        if key not in self.transitions:
            raise ValueError(f"No transition for state={self.state}, event={event}")
        transition = self.transitions[key]
        output = transition.handler(payload) if transition.handler else None
        prev = self.state
        self.state = transition.next_state
        return prev, self.state, output
