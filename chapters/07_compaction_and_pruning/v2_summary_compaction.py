from __future__ import annotations


def compact_with_summary(messages: list[str], keep_last: int = 3) -> dict[str, object]:
    if len(messages) <= keep_last:
        return {"summary": "", "working": list(messages)}

    old = messages[:-keep_last]
    summary = f"summary:{'; '.join(old[:3])}"
    return {
        "summary": summary,
        "working": messages[-keep_last:],
    }


def build_prompt(compacted: dict[str, object]) -> str:
    summary = str(compacted.get("summary", ""))
    working = compacted.get("working", [])
    if not isinstance(working, list):
        working = []
    return f"{summary}\nworking:{' | '.join(str(x) for x in working)}"


def main() -> None:
    msgs = [f"turn{i}" for i in range(1, 7)]
    compacted = compact_with_summary(msgs, keep_last=2)
    print(build_prompt(compacted))


if __name__ == "__main__":
    main()
