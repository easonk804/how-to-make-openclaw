from __future__ import annotations


def route_adapter(channel: str) -> str:
    name = channel.lower()
    if name == "telegram":
        return "telegram_adapter"
    if name == "discord":
        return "discord_adapter"
    if name == "webchat":
        return "webchat_adapter"
    return "default_adapter"


def dispatch_message(channel: str, text: str) -> str:
    adapter = route_adapter(channel)
    return f"{adapter}:handled:{text}"


def main() -> None:
    print(dispatch_message("telegram", "hello"))


if __name__ == "__main__":
    main()
