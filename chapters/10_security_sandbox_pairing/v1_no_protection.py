from __future__ import annotations


def execute_without_guard(command: str) -> dict[str, str]:
    return {
        "decision": "allowed",
        "command": command,
        "note": "no protection enabled",
    }


def main() -> None:
    print(execute_without_guard("rm -rf /tmp/demo"))


if __name__ == "__main__":
    main()
