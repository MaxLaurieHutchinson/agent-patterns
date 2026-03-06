"""
MDP/POMDP example.
"""

from implementation import MDP, POMDP


def main():
    states = ["s1", "s2"]
    actions = ["a"]
    transitions = {
        ("s1", "a"): [(1.0, "s2")],
        ("s2", "a"): [(1.0, "s2")],
    }
    rewards = {
        ("s1", "a", "s2"): 1.0,
        ("s2", "a", "s2"): 0.5,
    }

    mdp = MDP(states, actions, transitions, rewards, gamma=0.9)
    result = mdp.value_iteration()
    print("values=", result.values)
    print("policy=", result.policy)

    observations = ["o1"]
    observation_model = {
        ("s2", "a", "o1"): 1.0,
        ("s1", "a", "o1"): 0.0,
    }
    pomdp = POMDP(states, actions, observations, transitions, observation_model)
    belief = {"s1": 1.0, "s2": 0.0}
    updated = pomdp.update_belief(belief, "a", "o1")
    print("belief=", updated)


if __name__ == "__main__":
    main()
