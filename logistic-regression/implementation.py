"""
Logistic regression implementation (stdlib-only).
"""

import math


class LogisticRegression:
    def __init__(self):
        self.weights: list[float] = []

    @staticmethod
    def _sigmoid(z: float) -> float:
        if z >= 0:
            ez = math.exp(-z)
            return 1.0 / (1.0 + ez)
        ez = math.exp(z)
        return ez / (1.0 + ez)

    def fit(self, X: list[list[float]], y: list[int], lr: float = 0.1, epochs: int = 1000):
        if not X:
            return self
        n_features = len(X[0])
        self.weights = [0.0] * (n_features + 1)  # bias + weights

        for _ in range(epochs):
            grad = [0.0] * (n_features + 1)
            for xi, yi in zip(X, y):
                z = self.weights[0]
                for j in range(n_features):
                    z += self.weights[j + 1] * xi[j]
                pred = self._sigmoid(z)
                error = pred - yi
                grad[0] += error
                for j in range(n_features):
                    grad[j + 1] += error * xi[j]

            for j in range(n_features + 1):
                self.weights[j] -= lr * grad[j] / len(X)

        return self

    def predict_proba(self, X: list[list[float]]) -> list[float]:
        probs = []
        for xi in X:
            z = self.weights[0]
            for j in range(len(xi)):
                z += self.weights[j + 1] * xi[j]
            probs.append(self._sigmoid(z))
        return probs

    def predict(self, X: list[list[float]], threshold: float = 0.5) -> list[int]:
        return [1 if p >= threshold else 0 for p in self.predict_proba(X)]
