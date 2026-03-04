from __future__ import annotations

import math
from collections import Counter


provider_health: dict[str, dict[str, int]] = {}


def _tokenize(text: str) -> list[str]:
    return [token.strip(".,:;!?()[]{}\"'").lower() for token in text.split() if token.strip()]


def _embed(text: str) -> dict[str, float]:
    counts = Counter(_tokenize(text))
    return {k: float(v) for k, v in counts.items()}


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def _record_provider(provider: str, ok: bool) -> None:
    row = provider_health.setdefault(provider, {"total": 0, "success": 0, "error": 0})
    row["total"] += 1
    if ok:
        row["success"] += 1
    else:
        row["error"] += 1


def load_sample_docs() -> list[dict[str, str]]:
    return [
        {"id": "d1", "text": "Session policy controls whether context is shared or isolated."},
        {"id": "d2", "text": "Queue lanes limit concurrency and protect provider stability."},
        {"id": "d3", "text": "Sandbox and pairing improve security in DM workflows."},
    ]


def build_index(docs: list[dict[str, str]]) -> list[tuple[dict[str, str], dict[str, float]]]:
    return [(doc, _embed(doc["text"])) for doc in docs]


def retrieve_top_k(query: str, index: list[tuple[dict[str, str], dict[str, float]]], top_k: int = 2) -> list[dict[str, str]]:
    q = _embed(query)
    scored: list[tuple[float, dict[str, str]]] = []
    for doc, vec in index:
        scored.append((_cosine(q, vec), doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def _keyword_fallback(query: str, index: list[tuple[dict[str, str], dict[str, float]]], top_k: int = 2) -> list[dict[str, str]]:
    tokens = [t for t in _tokenize(query) if t]
    scored: list[tuple[int, dict[str, str]]] = []
    for doc, _ in index:
        text = doc["text"].lower()
        score = sum(1 for token in tokens if token in text)
        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda row: row[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def search_with_fallback(
    query: str,
    index: list[tuple[dict[str, str], dict[str, float]]],
    provider_order: list[str] | None = None,
    top_k: int = 1,
) -> dict[str, object]:
    order = provider_order or ["local-index", "memory-lines"]
    attempts: list[dict[str, object]] = []

    for provider in order:
        if provider == "local-index":
            hits = retrieve_top_k(query, index, top_k=top_k)
        elif provider == "memory-lines":
            hits = _keyword_fallback(query, index, top_k=top_k)
        else:
            hits = []
            attempts.append({"provider": provider, "ok": False, "count": 0, "error": "unsupported provider"})
            _record_provider(provider, False)
            continue

        ok = len(hits) > 0
        attempts.append({"provider": provider, "ok": ok, "count": len(hits)})
        _record_provider(provider, ok)
        if ok:
            return {
                "ok": True,
                "provider_used": provider,
                "attempts": attempts,
                "hits": hits,
            }

    return {
        "ok": False,
        "provider_used": None,
        "attempts": attempts,
        "hits": [],
        "error": "all providers failed",
    }


def answer_with_retrieval(query: str, index: list[tuple[dict[str, str], dict[str, float]]]) -> str:
    result = search_with_fallback(query, index, top_k=1)
    hits = result["hits"]
    if not isinstance(hits, list) or not hits:
        return "No retrieval hit."
    first = hits[0]
    if not isinstance(first, dict):
        return "No retrieval hit."
    return f"Retrieved: {first['text']}"


def main() -> None:
    docs = load_sample_docs()
    index = build_index(docs)
    print(answer_with_retrieval("How does session isolation work?", index))


if __name__ == "__main__":
    main()
