"""
Checkpoint + Resume implementation.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Callable
import json
import os
import tempfile


@dataclass
class CheckpointState:
    task_id: str
    status: str
    step_index: int
    data: dict[str, Any]
    updated_at: str
    error: str | None = None


class CheckpointStore:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> CheckpointState | None:
        if not os.path.exists(self.path):
            return None

        with open(self.path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return CheckpointState(**raw)

    def save(self, state: CheckpointState):
        parent = os.path.dirname(self.path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        with tempfile.NamedTemporaryFile("w", delete=False, dir=parent or None, encoding="utf-8") as tmp:
            json.dump(asdict(state), tmp, indent=2)
            tmp_path = tmp.name

        os.replace(tmp_path, self.path)


class ResumableRunner:
    def __init__(self, task_id: str, steps: list[Callable[[dict[str, Any]], dict[str, Any]]], store: CheckpointStore):
        self.task_id = task_id
        self.steps = steps
        self.store = store

    def run(self, initial_data: dict[str, Any] | None = None) -> CheckpointState:
        state = self.store.load()
        if state is None:
            state = CheckpointState(
                task_id=self.task_id,
                status="in_progress",
                step_index=0,
                data=initial_data or {},
                updated_at=datetime.utcnow().isoformat(),
            )

        if state.status == "completed":
            return state

        while state.step_index < len(self.steps):
            step_fn = self.steps[state.step_index]
            try:
                state.data = step_fn(state.data)
                state.step_index += 1
                state.status = "completed" if state.step_index == len(self.steps) else "in_progress"
                state.error = None
            except Exception as e:
                state.status = "failed"
                state.error = str(e)
                state.updated_at = datetime.utcnow().isoformat()
                self.store.save(state)
                return state

            state.updated_at = datetime.utcnow().isoformat()
            self.store.save(state)

        return state
