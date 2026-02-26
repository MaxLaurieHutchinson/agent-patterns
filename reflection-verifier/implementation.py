"""
Reflection + Verifier implementation.
"""

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class VerificationResult:
    passed: bool
    feedback: str = ""


@dataclass
class ReflectionRun:
    query: str
    final_answer: str
    passed: bool
    attempts: int
    history: list[dict] = field(default_factory=list)


class ReflectionVerifier:
    def __init__(
        self,
        solver: Callable[[str, str], str],
        verifier: Callable[[str, str], VerificationResult],
        max_attempts: int = 3,
    ):
        self.solver = solver
        self.verifier = verifier
        self.max_attempts = max_attempts

    def run(self, query: str) -> ReflectionRun:
        feedback = ""
        last_answer = ""
        history: list[dict] = []

        for attempt in range(1, self.max_attempts + 1):
            draft = self.solver(query, feedback)
            verdict = self.verifier(query, draft)
            history.append(
                {
                    "attempt": attempt,
                    "draft": draft,
                    "passed": verdict.passed,
                    "feedback": verdict.feedback,
                }
            )

            last_answer = draft
            if verdict.passed:
                return ReflectionRun(
                    query=query,
                    final_answer=draft,
                    passed=True,
                    attempts=attempt,
                    history=history,
                )

            feedback = verdict.feedback

        return ReflectionRun(
            query=query,
            final_answer=last_answer,
            passed=False,
            attempts=self.max_attempts,
            history=history,
        )
