from __future__ import annotations


def run_with_fixed_retry(simulated_errors: list[str], max_retries: int = 3) -> tuple[str, list[str]]:
    logs: list[str] = []

    for attempt in range(max_retries + 1):
        logs.append(f"attempt:{attempt}")
        if attempt < len(simulated_errors):
            logs.append(f"error:{simulated_errors[attempt]}")
            continue
        logs.append("success")
        return "success", logs

    logs.append("exhausted")
    return "failed", logs


def main() -> None:
    print(run_with_fixed_retry(["timeout", "timeout"], max_retries=2))


if __name__ == "__main__":
    main()
