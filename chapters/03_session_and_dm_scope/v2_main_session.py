from __future__ import annotations


class SessionStore:
    def __init__(self) -> None:
        self._messages: dict[str, list[str]] = {}

    def append(self, key: str, message: str) -> None:
        self._messages.setdefault(key, []).append(message)

    def history(self, key: str) -> list[str]:
        return list(self._messages.get(key, []))


def main_session_key(workspace: str, agent: str) -> str:
    return f"{workspace}:{agent}:main"


def handle_with_main_session(store: SessionStore, text: str, workspace: str = "demo", agent: str = "openclaw") -> dict[str, object]:
    key = main_session_key(workspace, agent)
    store.append(key, f"user:{text}")
    store.append(key, f"assistant:ack:{text}")
    return {
        "session_key": key,
        "history_size": len(store.history(key)),
    }


def main() -> None:
    store = SessionStore()
    print(handle_with_main_session(store, "hello"))


if __name__ == "__main__":
    main()
