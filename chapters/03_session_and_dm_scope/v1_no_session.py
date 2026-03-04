from __future__ import annotations


def handle_without_session(text: str) -> dict[str, str]:
    return {
        "session_key": "ephemeral",
        "reply": f"stateless:{text}",
    }


def main() -> None:
    print(handle_without_session("hello"))


if __name__ == "__main__":
    main()
