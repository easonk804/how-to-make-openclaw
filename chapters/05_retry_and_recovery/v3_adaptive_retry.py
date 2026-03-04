from __future__ import annotations


def _classify(error: str) -> str:
    lowered = error.lower()
    if "timeout" in lowered or "network" in lowered or "429" in lowered:
        return "transient"
    if "permission" in lowered or "auth" in lowered or "401" in lowered or "403" in lowered:
        return "fatal"
    if "5xx" in lowered or "500" in lowered or "502" in lowered or "503" in lowered or "504" in lowered:
        return "transient"
    if "4xx" in lowered or "400" in lowered or "404" in lowered:
        return "fatal"
    return "unknown"


def run_with_adaptive_retry(simulated_errors: list[str], max_retries: int = 4) -> tuple[str, list[dict[str, str]]]:
    logs: list[dict[str, str]] = []

    attempt = 0
    while attempt <= max_retries:
        logs.append({"event": "attempt", "value": str(attempt)})

        if attempt < len(simulated_errors):
            error = simulated_errors[attempt]
            category = _classify(error)
            logs.append({"event": "error", "value": error})
            logs.append({"event": "category", "value": category})

            if category == "fatal":
                logs.append({"event": "decision", "value": "stop"})
                return "failed", logs

            if attempt >= max_retries:
                logs.append({"event": "decision", "value": "exhausted"})
                return "failed", logs

            backoff_ms = min(1000 * (2**attempt), 8000)
            logs.append({"event": "retry_delay_ms", "value": str(backoff_ms)})
            logs.append({"event": "decision", "value": "retry"})

            attempt += 1
            continue

        logs.append({"event": "decision", "value": "success"})
        return "success", logs

    logs.append({"event": "decision", "value": "exhausted"})
    return "failed", logs


def main() -> None:
    status, logs = run_with_adaptive_retry(["network timeout", "network timeout"], max_retries=3)
    print(status)
    print(logs)


if __name__ == "__main__":
    main()
