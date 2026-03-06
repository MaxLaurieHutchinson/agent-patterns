"""
Calibration and abstain policy.
"""


class AbstainPolicy:
    def __init__(self, threshold: float, abstain_label: str = "abstain"):
        self.threshold = threshold
        self.abstain_label = abstain_label

    def apply(self, score: float, label: str = "positive") -> str:
        if score >= self.threshold:
            return label
        return self.abstain_label
