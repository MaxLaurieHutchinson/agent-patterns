"""
Causal reasoning implementation with simple structural equations.
"""

from dataclasses import dataclass


@dataclass
class CausalResult:
    baseline: dict
    intervention: dict
    counterfactual: dict


class SCM:
    def __init__(self, equations: dict[str, callable], order: list[str]):
        self.equations = equations
        self.order = order

    def _compute(self, variables: dict) -> dict:
        values = dict(variables)
        for name in self.order:
            if name in self.equations and name not in variables:
                values[name] = self.equations[name](values)
        return values

    def do(self, intervention: dict, baseline: dict | None = None) -> dict:
        base = dict(baseline or {})
        base.update(intervention)
        return self._compute(base)

    def counterfactual(self, baseline: dict, intervention: dict) -> CausalResult:
        base = self._compute(dict(baseline))
        intervened = self.do(intervention, baseline=baseline)
        return CausalResult(baseline=base, intervention=intervention, counterfactual=intervened)
