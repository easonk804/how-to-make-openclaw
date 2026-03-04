from __future__ import annotations


def _intent_from_text(text: str) -> str:
    lowered = text.lower()
    if "create" in lowered or "创建" in text:
        return "create_file"
    if "read" in lowered or "读取" in text:
        return "read_file"
    return "reply"


def lifecycle_for_message(text: str, channel: str = "cli", user: str = "u1") -> list[dict[str, str]]:
    intent = _intent_from_text(text)
    return [
        {"type": "lifecycle_start", "channel": channel, "user": user},
        {"type": "ingress", "text": text},
        {"type": "act", "intent": intent},
        {"type": "egress", "message": f"done:{intent}"},
        {"type": "lifecycle_end", "status": "ok"},
    ]


def run_gateway_loop(inputs: list[str], channel: str = "cli", user: str = "u1") -> list[dict[str, object]]:
    outputs: list[dict[str, object]] = []
    for text in inputs:
        events = lifecycle_for_message(text, channel=channel, user=user)
        outputs.append({"message": text, "events": events, "final": events[-2]["message"]})
    return outputs


def main() -> None:
    out = run_gateway_loop(["create a file", "read file"])
    print(out)


if __name__ == "__main__":
    main()
