"""
Greedy knapsack example.
"""

from implementation import Item, GreedyKnapsack


def main():
    items = [
        Item("A", value=10, weight=2),
        Item("B", value=6, weight=2),
        Item("C", value=8, weight=4),
    ]
    selected, total_value, total_weight = GreedyKnapsack.solve(items, capacity=4)
    print([i.name for i in selected], total_value, total_weight)


if __name__ == "__main__":
    main()
