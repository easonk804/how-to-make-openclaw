from __future__ import annotations


def direct_answer(problem: str) -> str:
    if "ModuleNotFoundError" in problem and "requests" in problem:
        return "Install dependency: pip install requests"
    return "Use logs to diagnose the issue."


def main() -> None:
    print(direct_answer("ModuleNotFoundError: No module named 'requests'"))


if __name__ == "__main__":
    main()
