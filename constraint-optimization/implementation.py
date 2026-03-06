"""
Constraint optimization: greedy knapsack.
"""

from dataclasses import dataclass


@dataclass
class Item:
    name: str
    value: float
    weight: float


class GreedyKnapsack:
    @staticmethod
    def solve(items: list[Item], capacity: float):
        items_sorted = sorted(items, key=lambda i: i.value / i.weight, reverse=True)
        selected = []
        total_value = 0.0
        total_weight = 0.0

        for item in items_sorted:
            if total_weight + item.weight <= capacity:
                selected.append(item)
                total_weight += item.weight
                total_value += item.value

        return selected, total_value, total_weight
