"""
BDI Agent example: choose next action.
"""

from implementation import BDIAgent, Desire


def belief_updater(beliefs, percepts):
    beliefs = dict(beliefs)
    beliefs.update(percepts)
    return beliefs


def desire_generator(beliefs):
    desires = []
    if beliefs.get("inbox_unread", 0) > 0:
        desires.append(Desire(name="process_inbox", priority=2))
    if beliefs.get("meeting_soon"):
        desires.append(Desire(name="prepare_meeting", priority=3))
    desires.append(Desire(name="idle", priority=1))
    return desires


def main():
    agent = BDIAgent(belief_updater, desire_generator)
    intention = agent.step({"inbox_unread": 5, "meeting_soon": True})
    print("intention=", intention)


if __name__ == "__main__":
    main()
