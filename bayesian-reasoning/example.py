"""
Bayesian reasoning example: diagnostic test.
"""

from implementation import BayesUpdater


def main():
    prior = 0.01
    likelihood = (0.95, 0.10)  # sensitivity, false positive rate
    posterior = BayesUpdater.update(prior, likelihood)
    print("posterior=", round(posterior, 4))


if __name__ == "__main__":
    main()
