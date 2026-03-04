from __future__ import annotations

from pathlib import Path


def load_memory_lines() -> list[str]:
    memory_file = Path(__file__).resolve().parent / "MEMORY.md"
    if not memory_file.exists():
        return []
    return [line.strip() for line in memory_file.read_text(encoding="utf-8").splitlines() if line.strip()]


def keyword_search(query: str, memory_lines: list[str], top_k: int = 2) -> list[str]:
    tokens = [token for token in query.lower().split() if token]
    scored: list[tuple[int, str]] = []

    for line in memory_lines:
        lowered = line.lower()
        score = sum(1 for token in tokens if token in lowered)
        if score > 0:
            scored.append((score, line))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [line for _, line in scored[:top_k]]


def answer_with_keyword_memory(query: str) -> str:
    lines = load_memory_lines()
    hits = keyword_search(query, lines)
    if not hits:
        return "No memory result found."
    return f"Top memory: {hits[0]}"


def main() -> None:
    print(answer_with_keyword_memory("session key policy"))


if __name__ == "__main__":
    main()
