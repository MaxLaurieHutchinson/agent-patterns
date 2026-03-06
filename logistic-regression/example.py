"""
Logistic regression example: toy dataset.
"""

from implementation import LogisticRegression


def main():
    X = [[0.0], [1.0], [2.0], [3.0]]
    y = [0, 0, 1, 1]

    model = LogisticRegression().fit(X, y, lr=0.2, epochs=500)
    preds = model.predict(X)
    print("preds=", preds)


if __name__ == "__main__":
    main()
