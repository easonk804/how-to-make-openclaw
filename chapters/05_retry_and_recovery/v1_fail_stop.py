from __future__ import annotations


def run_once(simulated_error: str | None = None) -> tuple[str, list[str]]:
    logs: list[str] = ["start"]
    if simulated_error:
        logs.append(f"error:{simulated_error}")
        logs.append("stop")
        return "failed", logs

    logs.append("success")
    return "success", logs


def main() -> None:
    print(run_once("timeout"))


if __name__ == "__main__":
    main()
