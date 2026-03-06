"""
MDP and POMDP implementations.
"""

from dataclasses import dataclass


@dataclass
class ValueIterationResult:
    values: dict
    policy: dict


class MDP:
    def __init__(self, states, actions, transitions, rewards, gamma: float = 0.9):
        self.states = states
        self.actions = actions
        self.transitions = transitions  # (state, action) -> list[(prob, next_state)]
        self.rewards = rewards  # (state, action, next_state) -> reward
        self.gamma = gamma

    def value_iteration(self, tol: float = 1e-6, max_iter: int = 1000) -> ValueIterationResult:
        values = {s: 0.0 for s in self.states}
        policy = {s: None for s in self.states}

        for _ in range(max_iter):
            delta = 0.0
            for state in self.states:
                best_value = None
                best_action = None
                for action in self.actions:
                    total = 0.0
                    for prob, next_state in self.transitions.get((state, action), []):
                        reward = self.rewards.get((state, action, next_state), 0.0)
                        total += prob * (reward + self.gamma * values[next_state])
                    if best_value is None or total > best_value:
                        best_value = total
                        best_action = action
                if best_value is None:
                    best_value = 0.0
                delta = max(delta, abs(best_value - values[state]))
                values[state] = best_value
                policy[state] = best_action
            if delta < tol:
                break

        return ValueIterationResult(values=values, policy=policy)


class POMDP:
    def __init__(self, states, actions, observations, transitions, observation_model):
        self.states = states
        self.actions = actions
        self.observations = observations
        self.transitions = transitions  # (state, action) -> list[(prob, next_state)]
        self.observation_model = observation_model  # (next_state, action, obs) -> prob

    def update_belief(self, belief: dict, action, observation) -> dict:
        new_belief = {s: 0.0 for s in self.states}
        for prev_state, prev_prob in belief.items():
            for prob, next_state in self.transitions.get((prev_state, action), []):
                obs_prob = self.observation_model.get((next_state, action, observation), 0.0)
                new_belief[next_state] += prev_prob * prob * obs_prob

        total = sum(new_belief.values())
        if total == 0:
            return {s: 0.0 for s in self.states}
        return {s: v / total for s, v in new_belief.items()}
