"""
Bayesian reasoning implementation.
"""

from typing import Dict


class BayesUpdater:
    @staticmethod
    def update(prior, likelihood):
        if isinstance(prior, dict):
            return BayesUpdater._update_distribution(prior, likelihood)
        return BayesUpdater._update_scalar(prior, likelihood)

    @staticmethod
    def _update_scalar(prior: float, likelihood) -> float:
        if isinstance(likelihood, dict):
            p_e_given_h = likelihood.get("p_e_given_h")
            p_e_given_not_h = likelihood.get("p_e_given_not_h")
        else:
            p_e_given_h, p_e_given_not_h = likelihood

        numerator = p_e_given_h * prior
        denominator = numerator + p_e_given_not_h * (1.0 - prior)
        if denominator == 0:
            return 0.0
        return numerator / denominator

    @staticmethod
    def _update_distribution(prior: Dict[str, float], likelihood: Dict[str, float]) -> Dict[str, float]:
        unnormalized = {k: prior[k] * likelihood.get(k, 0.0) for k in prior}
        total = sum(unnormalized.values())
        if total == 0:
            return {k: 0.0 for k in prior}
        return {k: v / total for k, v in unnormalized.items()}
