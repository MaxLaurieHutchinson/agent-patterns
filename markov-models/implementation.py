"""
Markov model implementation.
"""

import random


class MarkovChain:
    def __init__(self, transitions: dict[str, dict[str, float]], rng: random.Random | None = None):
        self.transitions = transitions
        self.states = list(transitions.keys())
        self.rng = rng or random.Random()
        self._normalize()

    def _normalize(self):
        for state, probs in self.transitions.items():
            total = sum(probs.values())
            if total == 0:
                continue
            for k in list(probs.keys()):
                probs[k] = probs[k] / total

    def next_state(self, state: str) -> str:
        probs = self.transitions[state]
        r = self.rng.random()
        cumulative = 0.0
        for next_state, p in probs.items():
            cumulative += p
            if r <= cumulative:
                return next_state
        return next(iter(probs))

    def stationary_distribution(self, tol: float = 1e-6, max_iter: int = 1000) -> dict[str, float]:
        n = len(self.states)
        dist = {s: 1.0 / n for s in self.states}

        for _ in range(max_iter):
            new_dist = {s: 0.0 for s in self.states}
            for s in self.states:
                for ns, p in self.transitions[s].items():
                    new_dist[ns] += dist[s] * p
            delta = sum(abs(new_dist[s] - dist[s]) for s in self.states)
            dist = new_dist
            if delta < tol:
                break
        return dist
