"""
OODA Loop example: basic incident response loop.
"""

from implementation import OODALoop


def main():
    signal = {"errors": 5, "latency_ms": 900}

    def observe():
        return dict(signal)

    def orient(observation, _context):
        if observation["errors"] > 0:
            return "degraded"
        return "healthy"

    def decide(orientation, _context):
        return "throttle" if orientation == "degraded" else "noop"

    def act(decision, _context):
        if decision == "throttle":
            signal["errors"] = max(0, signal["errors"] - 2)
        return f"action={decision}"

    loop = OODALoop(max_iters=3)
    result = loop.run(observe, orient, decide, act)

    print("final_decision=", result.final_decision)
    for step in result.steps:
        print(step)


if __name__ == "__main__":
    main()
