from __future__ import annotations


def reason_steps(problem: str) -> list[str]:
    steps = ["Inspect error type", "Identify missing package"]
    if "requests" in problem:
        steps.append("Suggest installation command")
    else:
        steps.append("Suggest dependency check")
    return steps


def reason_and_answer(problem: str) -> tuple[list[str], str]:
    steps = reason_steps(problem)
    if "requests" in problem:
        final = "Run: pip install requests"
    else:
        final = "Verify project dependencies and reinstall."
    return steps, final


def main() -> None:
    steps, final = reason_and_answer("ModuleNotFoundError: No module named 'requests'")
    print(steps)
    print(final)


if __name__ == "__main__":
    main()
