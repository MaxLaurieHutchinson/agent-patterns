"""
Markov models example: weather transitions.
"""

from implementation import MarkovChain


def main():
    transitions = {
        "sunny": {"sunny": 0.7, "rain": 0.3},
        "rain": {"sunny": 0.4, "rain": 0.6},
    }
    chain = MarkovChain(transitions)
    print("next=", chain.next_state("sunny"))
    print("stationary=", chain.stationary_distribution())


if __name__ == "__main__":
    main()
