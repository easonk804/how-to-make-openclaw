from __future__ import annotations


def _simulate_tool(action: str) -> str:
    if action == "pip_install_requests":
        return "ok:installed requests"
    return "failed:unknown action"


def react_solve(problem: str) -> tuple[list[dict[str, str]], str]:
    trace: list[dict[str, str]] = []

    trace.append({"type": "thought", "content": f"Analyze problem: {problem}"})

    if "requests" in problem:
        action = "pip_install_requests"
        trace.append({"type": "action", "tool": "shell", "command": "pip install requests"})
        observation = _simulate_tool(action)
        trace.append({"type": "observation", "content": observation})
        final = "Dependency fixed: requests installed."
    else:
        trace.append({"type": "action", "tool": "log_inspector", "command": "inspect logs"})
        observation = _simulate_tool("unknown")
        trace.append({"type": "observation", "content": observation})
        final = "Need deeper diagnostics from logs."

    trace.append({"type": "final", "content": final})
    return trace, final


def main() -> None:
    trace, final = react_solve("ModuleNotFoundError: No module named 'requests'")
    print(trace)
    print(final)


if __name__ == "__main__":
    main()
