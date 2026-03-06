"""
State machine example.
"""

from implementation import FiniteStateMachine


def main():
    fsm = FiniteStateMachine("start")
    fsm.add_transition("start", "next", "review")
    fsm.add_transition("review", "approve", "done", handler=lambda _: "approved")

    print(fsm.transition("next"))
    print(fsm.transition("approve"))


if __name__ == "__main__":
    main()
