"""
Risk scoring implementation.
"""

from dataclasses import dataclass


@dataclass
class RiskResult:
    score: float
    band: str


class RiskScorer:
    def __init__(self, weights: dict[str, float], thresholds: list[tuple[float, str]]):
        self.weights = weights
        self.thresholds = sorted(thresholds, key=lambda t: t[0])

    def score(self, features: dict[str, float]) -> RiskResult:
        score = 0.0
        for key, weight in self.weights.items():
            score += weight * features.get(key, 0.0)

        band = self.thresholds[-1][1]
        for threshold, label in self.thresholds:
            if score <= threshold:
                band = label
                break

        return RiskResult(score=score, band=band)
