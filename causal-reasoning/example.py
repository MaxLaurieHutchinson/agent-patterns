"""
Causal reasoning example.
"""

from implementation import SCM


def main():
    equations = {
        "sales": lambda v: v.get("ads", 0) * 2 + 1,
    }
    scm = SCM(equations, order=["sales"])
    result = scm.counterfactual({"ads": 3}, {"ads": 5})
    print(result)


if __name__ == "__main__":
    main()
