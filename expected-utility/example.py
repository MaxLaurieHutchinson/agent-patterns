"""
Expected utility example.
"""

from implementation import ExpectedUtility


def main():
    options = [
        {"name": "A", "outcomes": [(0.8, 10), (0.2, -5)]},
        {"name": "B", "outcomes": [(0.5, 12), (0.5, 0)]},
    ]
    best = ExpectedUtility.choose(options)
    print(best)


if __name__ == "__main__":
    main()
