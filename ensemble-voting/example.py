"""
Ensemble voting example.
"""

from implementation import Ensemble


def main():
    preds = ["A", "A", "B"]
    print("majority=", Ensemble.majority_vote(preds))
    print("weighted=", Ensemble.weighted_vote(preds, [0.2, 0.4, 0.9]))


if __name__ == "__main__":
    main()
