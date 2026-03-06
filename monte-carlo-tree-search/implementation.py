"""
Monte Carlo Tree Search implementation.
"""

import math
import random


class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = {}
        self.visits = 0
        self.value = 0.0
        self.untried_actions = list(state.get_actions())

    def is_fully_expanded(self) -> bool:
        return len(self.untried_actions) == 0

    def best_child(self, c_param: float = 1.4):
        best_score = None
        best_child = None
        for child in self.children.values():
            exploitation = child.value / (child.visits or 1)
            exploration = c_param * math.sqrt(math.log(self.visits + 1) / (child.visits or 1))
            score = exploitation + exploration
            if best_score is None or score > best_score:
                best_score = score
                best_child = child
        return best_child


class MCTS:
    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()

    def search(self, root_state, iters: int = 100) -> object:
        root = MCTSNode(root_state)

        for _ in range(iters):
            node = root
            state = root_state

            # Selection
            while node.is_fully_expanded() and node.children:
                node = node.best_child()
                state = state.next_state(node.action)

            # Expansion
            if node.untried_actions:
                action = node.untried_actions.pop()
                next_state = state.next_state(action)
                child = MCTSNode(next_state, parent=node, action=action)
                node.children[action] = child
                node = child
                state = next_state

            # Simulation
            reward = self._rollout(state)

            # Backpropagation
            while node is not None:
                node.visits += 1
                node.value += reward
                node = node.parent

        if not root.children:
            return None
        return max(root.children.values(), key=lambda c: c.visits).action

    def _rollout(self, state) -> float:
        current = state
        while not current.is_terminal():
            actions = current.get_actions()
            action = self.rng.choice(actions)
            current = current.next_state(action)
        return current.evaluate()
