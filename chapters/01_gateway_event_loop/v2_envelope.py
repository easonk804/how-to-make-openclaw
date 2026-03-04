from __future__ import annotations


def build_envelope(channel: str, user: str, text: str) -> dict[str, object]:
    return {
        "id": f"{channel}:{user}:001",
        "channel": channel,
        "user": user,
        "payload": {"text": text},
        "meta": {"version": 2},
    }


def classify_intent(text: str) -> str:
    lowered = text.lower()
    if "create" in lowered or "创建" in text:
        return "create_file"
    if "read" in lowered or "读取" in text:
        return "read_file"
    return "reply"


def handle_envelope(envelope: dict[str, object]) -> dict[str, object]:
    payload = envelope.get("payload", {})
    text = payload.get("text", "") if isinstance(payload, dict) else ""
    intent = classify_intent(str(text))
    return {
        "id": envelope.get("id", "unknown"),
        "intent": intent,
        "result": f"handled:{intent}",
    }


def main() -> None:
    env = build_envelope("telegram", "u1", "please create file")
    print(handle_envelope(env))


if __name__ == "__main__":
    main()
