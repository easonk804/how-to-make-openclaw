from __future__ import annotations


DEFAULT_RULES = [
    {"when": {"channel": "telegram"}, "adapter": "telegram_adapter"},
    {"when": {"channel": "discord"}, "adapter": "discord_adapter"},
    {"when": {"channel": "webchat"}, "adapter": "webchat_adapter"},
]


def choose_adapter(envelope: dict[str, str], rules: list[dict[str, object]] | None = None) -> str:
    use_rules = rules or DEFAULT_RULES
    for rule in use_rules:
        when = rule.get("when", {})
        if not isinstance(when, dict):
            continue
        if all(envelope.get(k) == v for k, v in when.items()):
            return str(rule.get("adapter", "default_adapter"))
    return "default_adapter"


def dispatch_with_rules(envelope: dict[str, str]) -> str:
    adapter = choose_adapter(envelope)
    return f"{adapter}:handled:{envelope.get('text', '')}"


def main() -> None:
    env = {"channel": "discord", "text": "ping"}
    print(dispatch_with_rules(env))


if __name__ == "__main__":
    main()
