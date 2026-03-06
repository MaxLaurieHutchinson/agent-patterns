"""
Rule engine example.
"""

from implementation import Rule, RuleEngine


def main():
    rules = [
        Rule("urgent", lambda x: x.get("priority") == "high", "fast_lane"),
        Rule("billing", lambda x: x.get("topic") == "billing", "billing_team"),
    ]
    engine = RuleEngine(rules, default="general")
    print(engine.evaluate({"priority": "high"}))
    print(engine.evaluate({"topic": "billing"}))
    print(engine.evaluate({"topic": "other"}))


if __name__ == "__main__":
    main()
