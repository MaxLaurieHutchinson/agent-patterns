"""
MCTS example: take-away game.
"""

from implementation import MCTS


class TakeAwayState:
    def __init__(self, remaining: int, player: int = 1):
        self.remaining = remaining
        self.player = player

    def get_actions(self):
        return [1, 2] if self.remaining >= 2 else [1]

    def next_state(self, action):
        return TakeAwayState(self.remaining - action, -self.player)

    def is_terminal(self):
        return self.remaining <= 0

    def evaluate(self):
        # If terminal, previous player made the last move.
        return 1.0 if self.player == -1 else 0.0


def main():
    mcts = MCTS()
    action = mcts.search(TakeAwayState(3), iters=50)
    print("best_action=", action)


if __name__ == "__main__":
    main()
