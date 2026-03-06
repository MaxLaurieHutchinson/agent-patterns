"""
Expected utility implementation.
"""


class ExpectedUtility:
    @staticmethod
    def choose(options: list[dict]) -> dict:
        best = None
        best_score = None
        for option in options:
            score = ExpectedUtility.expected_utility(option)
            if best_score is None or score > best_score:
                best_score = score
                best = dict(option)
                best["expected_utility"] = score
        return best

    @staticmethod
    def expected_utility(option: dict) -> float:
        total = 0.0
        for prob, utility in option.get("outcomes", []):
            total += prob * utility
        return total
