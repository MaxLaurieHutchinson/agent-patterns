"""
Router + Delegation example.
"""

from implementation import RouterDelegation


def coding_agent(query: str, _context: dict):
    return f"[coding_agent] Plan for: {query}"


def research_agent(query: str, _context: dict):
    return f"[research_agent] Sources for: {query}"


def writer_agent(query: str, _context: dict):
    return f"[writer_agent] Draft for: {query}"


def general_agent(query: str, _context: dict):
    return f"[general_agent] Generic response for: {query}"


def main():
    router = RouterDelegation(fallback_agent="general_agent")

    router.add_route("coding", ["code", "bug", "python", "refactor"], "coding_agent")
    router.add_route("research", ["research", "sources", "compare", "analyze"], "research_agent")
    router.add_route("writing", ["write", "draft", "post", "article"], "writer_agent")

    router.register_handler("coding_agent", coding_agent)
    router.register_handler("research_agent", research_agent)
    router.register_handler("writer_agent", writer_agent)
    router.register_handler("general_agent", general_agent)

    queries = [
        "Refactor this python function",
        "Research model latency benchmarks",
        "Draft a launch post",
        "Hello there",
    ]

    for q in queries:
        out = router.delegate(q)
        print(f"query={q}")
        print(f"  intent={out.intent} agent={out.selected_agent} success={out.success}")
        print(f"  result={out.result or out.error}")


if __name__ == "__main__":
    main()
