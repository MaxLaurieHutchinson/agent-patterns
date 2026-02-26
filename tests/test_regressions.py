import importlib.util
import pathlib
import sys
import tempfile
import threading
import types
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def _ensure_lang_stubs():
    """Install lightweight stubs for optional LangChain/LangGraph deps."""
    try:
        import langgraph.graph  # type: ignore  # noqa: F401
    except ImportError:
        langgraph_pkg = types.ModuleType("langgraph")
        graph_mod = types.ModuleType("langgraph.graph")
        end_sentinel = "__END__"

        class StateGraph:
            def __init__(self, _state_type):
                self._nodes = {}
                self._entry = None
                self._edges = {}
                self._conditional_edges = {}

            def add_node(self, name, func):
                self._nodes[name] = func

            def set_entry_point(self, name):
                self._entry = name

            def add_edge(self, source, target):
                self._edges[source] = target

            def add_conditional_edges(self, source, route_fn, mapping):
                self._conditional_edges[source] = (route_fn, mapping)

            def compile(self):
                nodes = self._nodes
                entry = self._entry
                edges = self._edges
                conditional_edges = self._conditional_edges

                class CompiledGraph:
                    def invoke(self, state):
                        current = entry
                        safety_counter = 0

                        while current != end_sentinel:
                            if current not in nodes:
                                raise RuntimeError(f"Unknown node '{current}'")

                            safety_counter += 1
                            if safety_counter > 1000:
                                raise RuntimeError("Graph execution exceeded max steps")

                            state = nodes[current](state)

                            if current in conditional_edges:
                                route_fn, mapping = conditional_edges[current]
                                route = route_fn(state)
                                current = mapping[route]
                            else:
                                if current not in edges:
                                    raise RuntimeError(
                                        f"No outgoing edge defined for node '{current}'"
                                    )
                                current = edges[current]

                        return state

                return CompiledGraph()

        graph_mod.StateGraph = StateGraph
        graph_mod.END = end_sentinel
        sys.modules["langgraph"] = langgraph_pkg
        sys.modules["langgraph.graph"] = graph_mod

    try:
        import langchain_core.messages  # type: ignore  # noqa: F401
    except ImportError:
        langchain_pkg = types.ModuleType("langchain_core")
        messages_mod = types.ModuleType("langchain_core.messages")
        models_mod = types.ModuleType("langchain_core.language_models")
        tools_mod = types.ModuleType("langchain_core.tools")

        class BaseMessage:
            def __init__(self, content):
                self.content = content

        class HumanMessage(BaseMessage):
            pass

        class AIMessage(BaseMessage):
            pass

        class SystemMessage(BaseMessage):
            pass

        class BaseChatModel:
            pass

        class BaseTool:
            name = "tool"
            description = ""

            def invoke(self, _args):
                raise NotImplementedError

        messages_mod.BaseMessage = BaseMessage
        messages_mod.HumanMessage = HumanMessage
        messages_mod.AIMessage = AIMessage
        messages_mod.SystemMessage = SystemMessage
        models_mod.BaseChatModel = BaseChatModel
        tools_mod.BaseTool = BaseTool

        sys.modules["langchain_core"] = langchain_pkg
        sys.modules["langchain_core.messages"] = messages_mod
        sys.modules["langchain_core.language_models"] = models_mod
        sys.modules["langchain_core.tools"] = tools_mod


def _load_module(relative_path: str, module_name: str, with_lang_stubs: bool = False):
    if with_lang_stubs:
        _ensure_lang_stubs()

    module_path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class _LLMResponse:
    def __init__(self, content: str):
        self.content = content


class _PlannerLLM:
    def __init__(self, plan_text: str):
        self.plan_text = plan_text

    def invoke(self, _messages):
        return _LLMResponse(self.plan_text)


class _ExecutorLLM:
    def __init__(self, fail_step: bool = False):
        self.fail_step = fail_step

    def invoke(self, messages):
        prompt = messages[0].content if messages else ""

        if "Execute this step:" in prompt:
            if self.fail_step:
                raise RuntimeError("executor boom")
            return _LLMResponse("step completed")

        if "Based on the completed steps" in prompt:
            return _LLMResponse("final synthesized answer")

        return _LLMResponse("ok")


class PlanExecuteRegressionTests(unittest.TestCase):
    def setUp(self):
        self.module = _load_module(
            "plan-and-execute/implementation.py",
            "plan_execute_impl",
            with_lang_stubs=True,
        )

    def test_agent_builds_and_runs_plan(self):
        planner = _PlannerLLM(
            "PLAN:\n- step_id: step_1 | description: Do thing | depends_on: []"
        )
        executor = _ExecutorLLM(fail_step=False)
        agent = self.module.PlanAndExecuteAgent(
            planner_llm=planner,
            executor_llm=executor,
            tools=[],
            execution_strategy="sequential",
            max_replans=0,
        )

        result = agent.run("Test task")

        self.assertEqual(result["final_answer"], "final synthesized answer")
        self.assertEqual(result["results"]["step_1"], "step completed")
        self.assertEqual(result["plan"].steps[0].status, self.module.StepStatus.COMPLETED)

    def test_sequential_execution_marks_failed_step(self):
        planner = _PlannerLLM(
            "PLAN:\n- step_id: step_1 | description: Fail step | depends_on: []"
        )
        executor = _ExecutorLLM(fail_step=True)
        agent = self.module.PlanAndExecuteAgent(
            planner_llm=planner,
            executor_llm=executor,
            tools=[],
            execution_strategy="sequential",
            max_replans=0,
        )

        result = agent.run("Task with failure")
        failed_step = result["plan"].steps[0]

        self.assertEqual(failed_step.status, self.module.StepStatus.FAILED)
        self.assertIn("executor boom", failed_step.error)
        self.assertEqual(result["final_answer"], "Task incomplete. 1 step(s) failed.")
        self.assertEqual(result["results"]["step_1"], "Error: executor boom")


class ObserverPatternRegressionTests(unittest.TestCase):
    def setUp(self):
        self.module = _load_module(
            "observer-pattern/implementation.py",
            "observer_impl",
        )

    def test_single_level_wildcard_does_not_match_deeper_topics(self):
        bus = self.module.EventBus()
        self.assertTrue(bus._topic_matches("task.*", "task.created"))
        self.assertFalse(bus._topic_matches("task.*", "task.created.high"))

    def test_publish_respects_single_level_wildcard(self):
        bus = self.module.EventBus()
        seen_topics = []

        def handler(event):
            seen_topics.append(event.topic)

        bus.subscribe("task.*", handler)
        bus.publish_simple("task.created", {"ok": True})
        bus.publish_simple("task.created.high", {"ok": True})

        self.assertEqual(seen_topics, ["task.created"])


class FileSystemToolRegressionTests(unittest.TestCase):
    def setUp(self):
        self.module = _load_module(
            "tool-use-mcp/implementation.py",
            "mcp_impl",
        )

    def test_filesystem_tool_blocks_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = pathlib.Path(tmp_dir)
            sandbox_dir = root / "sandbox"
            sandbox_dir.mkdir()

            inside_file = sandbox_dir / "inside.txt"
            inside_file.write_text("inside", encoding="utf-8")
            (root / "outside.txt").write_text("outside", encoding="utf-8")

            registry = self.module.MCPRegistry()
            registry.register(self.module.FileSystemTool(base_path=str(sandbox_dir)))

            allowed = registry.execute(
                "filesystem",
                {"operation": "read", "path": "inside.txt"},
            )
            self.assertTrue(allowed.success)
            self.assertEqual(allowed.data["content"], "inside")

            blocked = registry.execute(
                "filesystem",
                {"operation": "read", "path": "../outside.txt"},
            )
            self.assertFalse(blocked.success)
            self.assertIn("base path", (blocked.error or "").lower())


class CircuitBreakerRegressionTests(unittest.TestCase):
    def setUp(self):
        self.module = _load_module(
            "circuit-breaker/implementation.py",
            "circuit_impl",
        )

    def test_total_calls_matches_successful_calls_under_concurrency(self):
        config = self.module.CircuitConfig(
            failure_threshold=1_000_000,
            rate_limit_per_second=1_000_000,
        )
        breaker = self.module.CircuitBreaker("concurrency_test", config)

        threads = []
        errors = []
        thread_count = 20
        calls_per_thread = 200

        def worker():
            for _ in range(calls_per_thread):
                try:
                    breaker.call(lambda: "ok")
                except Exception as exc:  # pragma: no cover - should not happen
                    errors.append(exc)

        for _ in range(thread_count):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.assertEqual(errors, [])
        metrics = breaker.get_metrics()
        expected_calls = thread_count * calls_per_thread
        self.assertEqual(metrics["total_calls"], expected_calls)
        self.assertEqual(metrics["successful_calls"], expected_calls)


if __name__ == "__main__":
    unittest.main()
