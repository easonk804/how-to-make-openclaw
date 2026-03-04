from __future__ import annotations


def run_single_agent(task: str) -> dict[str, str]:
    return {
        "agent": "generalist",
        "task": task,
        "result": f"generalist handled: {task}",
    }


def main() -> None:
    print(run_single_agent("build ui"))


if __name__ == "__main__":
    main()
