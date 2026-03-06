"""
Risk scoring example.
"""

from implementation import RiskScorer


def main():
    weights = {"amount": 0.6, "velocity": 0.4}
    thresholds = [(0.3, "low"), (0.7, "medium"), (1.0, "high")]
    scorer = RiskScorer(weights, thresholds)
    result = scorer.score({"amount": 0.7, "velocity": 0.5})
    print(result)


if __name__ == "__main__":
    main()
