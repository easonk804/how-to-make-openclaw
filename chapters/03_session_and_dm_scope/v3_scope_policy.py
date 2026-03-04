from __future__ import annotations


def build_session_key(channel: str, user: str, is_dm: bool, policy: str) -> str:
    if policy == "main":
        return "main"

    if policy == "per-peer":
        if is_dm:
            return f"peer:{user}"
        return "main"

    if policy == "per-channel-peer":
        return f"{channel}:{user}"

    raise ValueError(f"unknown policy: {policy}")


def route_session(envelope: dict[str, object], policy: str) -> dict[str, str]:
    channel = str(envelope.get("channel", "unknown"))
    user = str(envelope.get("user", "unknown"))
    is_dm = bool(envelope.get("is_dm", False))

    key = build_session_key(channel, user, is_dm, policy)
    return {
        "policy": policy,
        "session_key": key,
    }


def main() -> None:
    env = {"channel": "telegram", "user": "alice", "is_dm": True}
    print(route_session(env, policy="per-peer"))
    print(route_session(env, policy="per-channel-peer"))


if __name__ == "__main__":
    main()
