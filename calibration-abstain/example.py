"""
Calibration/abstain example.
"""

from implementation import AbstainPolicy


def main():
    policy = AbstainPolicy(threshold=0.7)
    print(policy.apply(0.8, label="approve"))
    print(policy.apply(0.4, label="approve"))


if __name__ == "__main__":
    main()
