"""
Reflection + Verifier example.
"""

from implementation import ReflectionVerifier, VerificationResult


def solver(query: str, feedback: str) -> str:
    if "2 + 2" in query and "incorrect" not in feedback.lower():
        return "The answer is 5."
    if "2 + 2" in query:
        return "The answer is 4."
    return "Draft response."


def verifier(query: str, draft: str) -> VerificationResult:
    if "2 + 2" in query and "4" not in draft:
        return VerificationResult(passed=False, feedback="Incorrect arithmetic. Recompute 2 + 2.")
    return VerificationResult(passed=True)


def main():
    rv = ReflectionVerifier(solver=solver, verifier=verifier, max_attempts=3)
    run = rv.run("What is 2 + 2?")

    print(f"passed={run.passed} attempts={run.attempts}")
    for item in run.history:
        print(item)
    print("final_answer=", run.final_answer)


if __name__ == "__main__":
    main()
