from __future__ import annotations


KNOWLEDGE = {
    "session": "OpenClaw supports configurable session scoping.",
    "queue": "OpenClaw uses queue lanes for controlled concurrency.",
    "sandbox": "OpenClaw enforces sandbox boundaries for safe tool execution.",
}


def answer_hardcoded(query: str) -> str:
    lowered = query.lower()
    for key, value in KNOWLEDGE.items():
        if key in lowered:
            return value
    return "No hardcoded memory hit."


def main() -> None:
    print(answer_hardcoded("How does session work?"))


if __name__ == "__main__":
    main()
