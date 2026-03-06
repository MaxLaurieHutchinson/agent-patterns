"""
Ensemble voting implementation.
"""

from collections import Counter


class Ensemble:
    @staticmethod
    def majority_vote(preds: list) -> object:
        counts = Counter(preds)
        return counts.most_common(1)[0][0]

    @staticmethod
    def weighted_vote(preds: list, weights: list[float]) -> object:
        totals = {}
        for pred, weight in zip(preds, weights):
            totals[pred] = totals.get(pred, 0.0) + weight
        return max(totals.items(), key=lambda kv: kv[1])[0]
