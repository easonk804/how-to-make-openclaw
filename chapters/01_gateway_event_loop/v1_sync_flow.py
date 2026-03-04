from __future__ import annotations


def decide_action(text: str) -> tuple[str, str]:
    lowered = text.lower()
    if "create" in lowered or "创建" in text:
        return "create_file", "demo.txt"
    if "read" in lowered or "读取" in text:
        return "read_file", "demo.txt"
    return "reply", "-"


def handle_sync(text: str) -> dict[str, str]:
    action, target = decide_action(text)
    if action == "create_file":
        egress = f"created:{target}"
    elif action == "read_file":
        egress = f"content:{target}=<mock>"
    else:
        egress = f"reply:{text}"

    return {
        "ingress": text,
        "action": action,
        "target": target,
        "egress": egress,
    }


def main() -> None:
    out = handle_sync("请创建一个演示文件")
    print(out)


if __name__ == "__main__":
    main()
