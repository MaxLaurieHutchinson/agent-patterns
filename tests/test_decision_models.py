import unittest
import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_impl(slug: str):
    module_path = REPO_ROOT / slug / "implementation.py"
    spec = importlib.util.spec_from_file_location(f"{slug}_impl", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


ooda_impl = load_impl("ooda-loop")
bdi_impl = load_impl("bdi-agent")
bayes_impl = load_impl("bayesian-reasoning")
logreg_impl = load_impl("logistic-regression")
markov_impl = load_impl("markov-models")
risk_impl = load_impl("risk-scoring")
mdp_impl = load_impl("mdp-pomdp")
bandit_impl = load_impl("bandits-explore-exploit")
eu_impl = load_impl("expected-utility")
rules_impl = load_impl("decision-trees-rules")
mcts_impl = load_impl("monte-carlo-tree-search")
ensemble_impl = load_impl("ensemble-voting")
abstain_impl = load_impl("calibration-abstain")
knap_impl = load_impl("constraint-optimization")
causal_impl = load_impl("causal-reasoning")
fsm_impl = load_impl("state-machines")


class OODATests(unittest.TestCase):
    def test_ooda_loop(self):
        counter = {"n": 0}

        def observe():
            return counter["n"]

        def orient(obs, _ctx):
            return obs + 1

        def decide(ori, _ctx):
            return "act" if ori < 3 else "stop"

        def act(decision, _ctx):
            counter["n"] += 1
            return decision

        loop = ooda_impl.OODALoop(max_iters=3)
        result = loop.run(observe, orient, decide, act)
        self.assertEqual(len(result.steps), 3)
        self.assertEqual(result.final_decision, "stop")

    def test_ooda_zero_iters(self):
        loop = ooda_impl.OODALoop(max_iters=5)
        result = loop.run(lambda: None, lambda *_: None, lambda *_: None, lambda *_: None, max_iters=0)
        self.assertEqual(result.steps, [])
        self.assertIsNone(result.final_decision)


class BDITests(unittest.TestCase):
    def test_bdi_intention(self):
        def belief_updater(beliefs, percepts):
            out = dict(beliefs)
            out.update(percepts)
            return out

        def desire_generator(beliefs):
            desires = [bdi_impl.Desire("idle", 1)]
            if beliefs.get("urgent"):
                desires.append(bdi_impl.Desire("handle_urgent", 5))
            return desires

        agent = bdi_impl.BDIAgent(belief_updater, desire_generator)
        intention = agent.step({"urgent": True})
        self.assertEqual(intention.name, "handle_urgent")

    def test_bdi_no_desires(self):
        agent = bdi_impl.BDIAgent(lambda b, p: b, lambda _: [])
        self.assertIsNone(agent.step({}))
        self.assertEqual(agent.intentions, [])


class BayesTests(unittest.TestCase):
    def test_bayes_scalar(self):
        posterior = bayes_impl.BayesUpdater.update(0.5, (0.9, 0.1))
        self.assertAlmostEqual(posterior, 0.9 / (0.9 + 0.1), places=6)

    def test_bayes_distribution(self):
        prior = {"a": 0.2, "b": 0.8}
        likelihood = {"a": 0.5, "b": 0.25}
        posterior = bayes_impl.BayesUpdater.update(prior, likelihood)
        self.assertAlmostEqual(sum(posterior.values()), 1.0, places=6)

    def test_bayes_zero_denominator(self):
        posterior = bayes_impl.BayesUpdater.update(0.5, (0.0, 0.0))
        self.assertEqual(posterior, 0.0)

    def test_bayes_zero_distribution(self):
        prior = {"a": 0.2, "b": 0.8}
        likelihood = {"a": 0.0, "b": 0.0}
        posterior = bayes_impl.BayesUpdater.update(prior, likelihood)
        self.assertEqual(posterior, {"a": 0.0, "b": 0.0})


class LogisticRegressionTests(unittest.TestCase):
    def test_logistic_regression(self):
        X = [[0.0], [1.0], [2.0], [3.0]]
        y = [0, 0, 1, 1]
        model = logreg_impl.LogisticRegression().fit(X, y, lr=0.2, epochs=500)
        preds = model.predict(X)
        self.assertEqual(preds, y)

    def test_logistic_probabilities(self):
        X = [[0.0], [1.0]]
        y = [0, 1]
        model = logreg_impl.LogisticRegression().fit(X, y, lr=0.5, epochs=200)
        probs = model.predict_proba(X)
        for p in probs:
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)


class MarkovTests(unittest.TestCase):
    def test_markov_stationary(self):
        transitions = {
            "a": {"a": 1.0},
            "b": {"a": 1.0},
        }
        chain = markov_impl.MarkovChain(transitions)
        dist = chain.stationary_distribution()
        self.assertAlmostEqual(dist["a"], 1.0, places=6)

    def test_markov_normalization(self):
        transitions = {"a": {"a": 2.0, "b": 2.0}, "b": {"a": 1.0, "b": 1.0}}
        chain = markov_impl.MarkovChain(transitions)
        self.assertAlmostEqual(sum(chain.transitions["a"].values()), 1.0, places=6)


class RiskScoreTests(unittest.TestCase):
    def test_risk_scoring(self):
        scorer = risk_impl.RiskScorer({"x": 1.0}, [(0.3, "low"), (0.7, "mid"), (1.0, "high")])
        score = scorer.score({"x": 0.2})
        self.assertEqual(score.band, "low")

    def test_risk_scoring_upper_band(self):
        scorer = risk_impl.RiskScorer({"x": 1.0}, [(0.3, "low"), (0.7, "mid"), (1.0, "high")])
        score = scorer.score({"x": 0.95})
        self.assertEqual(score.band, "high")

    def test_risk_scoring_empty_thresholds(self):
        with self.assertRaises(ValueError):
            risk_impl.RiskScorer({"x": 1.0}, [])


class MDPTests(unittest.TestCase):
    def test_value_iteration(self):
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
        mdp = mdp_impl.MDP(states, actions, transitions, rewards, gamma=0.9)
        result = mdp.value_iteration()
        self.assertGreater(result.values["s2"], 0)
        self.assertEqual(result.policy["s1"], "a")

    def test_pomdp_belief_update(self):
        states = ["s1", "s2"]
        actions = ["a"]
        observations = ["o1"]
        transitions = {
            ("s1", "a"): [(1.0, "s2")],
            ("s2", "a"): [(1.0, "s2")],
        }
        observation_model = {
            ("s2", "a", "o1"): 1.0,
            ("s1", "a", "o1"): 0.0,
        }
        pomdp = mdp_impl.POMDP(states, actions, observations, transitions, observation_model)
        belief = {"s1": 1.0, "s2": 0.0}
        updated = pomdp.update_belief(belief, "a", "o1")
        self.assertAlmostEqual(updated["s2"], 1.0, places=6)

    def test_pomdp_zero_belief(self):
        states = ["s1"]
        actions = ["a"]
        observations = ["o1"]
        pomdp = mdp_impl.POMDP(states, actions, observations, transitions={}, observation_model={})
        updated = pomdp.update_belief({"s1": 1.0}, "a", "o1")
        self.assertEqual(updated, {"s1": 0.0})


class BanditTests(unittest.TestCase):
    def test_bandit_select(self):
        eg = bandit_impl.EpsilonGreedy(n_arms=2, epsilon=0.0)
        eg.update(0, 1.0)
        eg.update(1, 0.0)
        self.assertEqual(eg.select_arm(), 0)

    def test_ucb1_untried(self):
        ucb = bandit_impl.UCB1(n_arms=3)
        self.assertEqual(ucb.select_arm(), 0)


class ExpectedUtilityTests(unittest.TestCase):
    def test_expected_utility(self):
        options = [
            {"name": "A", "outcomes": [(1.0, 2.0)]},
            {"name": "B", "outcomes": [(1.0, 3.0)]},
        ]
        best = eu_impl.ExpectedUtility.choose(options)
        self.assertEqual(best["name"], "B")

    def test_expected_utility_value(self):
        option = {"outcomes": [(0.5, 2.0), (0.5, 0.0)]}
        self.assertAlmostEqual(eu_impl.ExpectedUtility.expected_utility(option), 1.0, places=6)


class RuleEngineTests(unittest.TestCase):
    def test_rule_engine(self):
        rules = [
            rules_impl.Rule("high", lambda x: x.get("p") == "high", "fast"),
            rules_impl.Rule("default", lambda x: True, "slow"),
        ]
        engine = rules_impl.RuleEngine(rules)
        self.assertEqual(engine.evaluate({"p": "high"}), "fast")

    def test_rule_engine_default(self):
        engine = rules_impl.RuleEngine([], default="fallback")
        self.assertEqual(engine.evaluate({"p": "none"}), "fallback")


class MCTSTests(unittest.TestCase):
    def test_mcts_action(self):
        class State:
            def __init__(self, remaining):
                self.remaining = remaining

            def get_actions(self):
                return [1] if self.remaining == 1 else [1, 2]

            def next_state(self, action):
                return State(self.remaining - action)

            def is_terminal(self):
                return self.remaining <= 0

            def evaluate(self):
                return 1.0

        mcts = mcts_impl.MCTS()
        action = mcts.search(State(2), iters=10)
        self.assertIn(action, [1, 2])

    def test_mcts_rollout_max_depth(self):
        class LoopState:
            def get_actions(self):
                return [1]

            def next_state(self, action):
                return self

            def is_terminal(self):
                return False

            def evaluate(self):
                return 0.0

        mcts = mcts_impl.MCTS(max_depth=3)
        action = mcts.search(LoopState(), iters=1)
        self.assertEqual(action, 1)

    def test_mcts_no_actions(self):
        class TerminalState:
            def get_actions(self):
                return []

            def next_state(self, action):
                return self

            def is_terminal(self):
                return True

            def evaluate(self):
                return 0.0

        mcts = mcts_impl.MCTS()
        self.assertIsNone(mcts.search(TerminalState(), iters=1))


class EnsembleTests(unittest.TestCase):
    def test_ensemble_votes(self):
        preds = ["A", "A", "B"]
        self.assertEqual(ensemble_impl.Ensemble.majority_vote(preds), "A")
        self.assertEqual(ensemble_impl.Ensemble.weighted_vote(preds, [0.1, 0.1, 1.0]), "B")

    def test_ensemble_weighted_tie(self):
        preds = ["A", "B"]
        result = ensemble_impl.Ensemble.weighted_vote(preds, [0.5, 0.5])
        self.assertIn(result, {"A", "B"})


class AbstainTests(unittest.TestCase):
    def test_abstain(self):
        policy = abstain_impl.AbstainPolicy(threshold=0.7)
        self.assertEqual(policy.apply(0.5, label="ok"), "abstain")
        self.assertEqual(policy.apply(0.9, label="ok"), "ok")

    def test_abstain_custom_label(self):
        policy = abstain_impl.AbstainPolicy(threshold=0.9, abstain_label="hold")
        self.assertEqual(policy.apply(0.2, label="yes"), "hold")


class KnapsackTests(unittest.TestCase):
    def test_knapsack(self):
        items = [
            knap_impl.Item("A", value=10, weight=2),
            knap_impl.Item("B", value=6, weight=2),
            knap_impl.Item("C", value=8, weight=4),
        ]
        selected, total_value, total_weight = knap_impl.GreedyKnapsack.solve(items, capacity=4)
        self.assertLessEqual(total_weight, 4)
        self.assertGreater(total_value, 0)

    def test_knapsack_invalid_weight(self):
        items = [knap_impl.Item("A", value=10, weight=0)]
        with self.assertRaises(ValueError):
            knap_impl.GreedyKnapsack.solve(items, capacity=4)

    def test_knapsack_negative_capacity(self):
        items = [knap_impl.Item("A", value=10, weight=1)]
        with self.assertRaises(ValueError):
            knap_impl.GreedyKnapsack.solve(items, capacity=-1)


class CausalTests(unittest.TestCase):
    def test_causal(self):
        equations = {"y": lambda v: v.get("x", 0) * 2}
        scm = causal_impl.SCM(equations, order=["y"])
        result = scm.counterfactual({"x": 1}, {"x": 2})
        self.assertEqual(result.baseline["y"], 2)
        self.assertEqual(result.counterfactual["y"], 4)

    def test_causal_do(self):
        equations = {"y": lambda v: v.get("x", 0) + 1}
        scm = causal_impl.SCM(equations, order=["y"])
        outcome = scm.do({"x": 3})
        self.assertEqual(outcome["y"], 4)


class StateMachineTests(unittest.TestCase):
    def test_state_machine(self):
        fsm = fsm_impl.FiniteStateMachine("start")
        fsm.add_transition("start", "next", "done", handler=lambda _: "ok")
        prev, state, output = fsm.transition("next")
        self.assertEqual(prev, "start")
        self.assertEqual(state, "done")
        self.assertEqual(output, "ok")

    def test_state_machine_invalid(self):
        fsm = fsm_impl.FiniteStateMachine("start")
        with self.assertRaises(ValueError):
            fsm.transition("missing")


if __name__ == "__main__":
    unittest.main()
