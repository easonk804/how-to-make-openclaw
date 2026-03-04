from __future__ import annotations

from dataclasses import dataclass, field
import math


@dataclass
class Memory:
    working: list[str] = field(default_factory=list)
    summary: list[str] = field(default_factory=list)
    tool_results: list[str] = field(default_factory=list)


def estimate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def prune_working_messages(
    working: list[str],
    max_messages: int,
    max_tokens: int | None = None,
) -> list[str]:
    out = working[-max_messages:] if max_messages > 0 else []
    if max_tokens is None or max_tokens <= 0:
        return out

    total = 0
    trimmed: list[str] = []
    for msg in reversed(out):
        total += estimate_tokens(msg)
        if total > max_tokens and trimmed:
            break
        trimmed.insert(0, msg)
    return trimmed


def compact_memory(memory: Memory, working_limit: int = 3, max_tokens: int | None = None) -> None:
    before = list(memory.working)
    after = prune_working_messages(before, max_messages=working_limit, max_tokens=max_tokens)
    if len(after) == len(before):
        return

    removed = before[: len(before) - len(after)]
    if removed:
        memory.summary.append(f"compact:{' ; '.join(removed)}")
    memory.working = after


def prune_tool_results(memory: Memory, tool_limit: int = 2) -> None:
    if len(memory.tool_results) <= tool_limit:
        return
    memory.tool_results = memory.tool_results[-tool_limit:]


def memory_prompt(memory: Memory) -> str:
    summary = "\n".join(memory.summary)
    working = "\n".join(memory.working)
    tools = "\n".join(memory.tool_results)
    return f"[summary]\n{summary}\n[working]\n{working}\n[tools]\n{tools}"


def main() -> None:
    mem = Memory(
        working=["u:hello", "a:hi", "u:need summary", "a:ok"],
        tool_results=["tool:a", "tool:b", "tool:c"],
    )
    compact_memory(mem, working_limit=2)
    prune_tool_results(mem, tool_limit=2)
    print(memory_prompt(mem))


if __name__ == "__main__":
    main()
