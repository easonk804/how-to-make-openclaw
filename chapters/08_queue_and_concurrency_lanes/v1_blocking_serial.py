from __future__ import annotations


def run_blocking(tasks: list[tuple[str, int]]) -> list[str]:
    results: list[str] = []
    for name, duration_ms in tasks:
        results.append(f"run:{name}:{duration_ms}ms")
    return results


def main() -> None:
    print(run_blocking([("A", 10), ("B", 20)]))


if __name__ == "__main__":
    main()
