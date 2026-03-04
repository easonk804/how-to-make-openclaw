from __future__ import annotations


BINDINGS = {
    "build ui": "frontend_agent",
    "implement api": "backend_agent",
    "write test": "qa_agent",
}


def route_task(task: str, bindings: dict[str, str] | None = None) -> str:
    return route_task_with_match(task, bindings)["agent"]


def route_task_with_match(task: str, bindings: dict[str, str] | None = None) -> dict[str, str]:
    use_bindings = bindings or BINDINGS
    for keyword, agent in use_bindings.items():
        if keyword in task:
            return {
                "agent": agent,
                "matched_by": keyword,
            }
    return {
        "agent": "generalist_agent",
        "matched_by": "default",
    }


def run_centralized(tasks: list[str]) -> list[str]:
    logs: list[str] = []
    for task in tasks:
        agent = route_task(task)
        logs.append(f"routed:{task}->{agent}")
    return logs


def main() -> None:
    print(run_centralized(["build ui", "implement api", "unknown"] ))


if __name__ == "__main__":
    main()
