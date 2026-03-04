from pathlib import Path
import importlib.util


def _load_local_module(module_filename: str, alias: str):
    path = Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {module_filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v1_hardcoded_knowledge = _load_local_module("v1_hardcoded_knowledge.py", "chapter06_v1_hardcoded_knowledge")
v2_keyword_memory = _load_local_module("v2_keyword_memory.py", "chapter06_v2_keyword_memory")
v3_vector_retrieval = _load_local_module("v3_vector_retrieval.py", "chapter06_v3_vector_retrieval")


answer_hardcoded = v1_hardcoded_knowledge.answer_hardcoded
load_memory_lines = v2_keyword_memory.load_memory_lines
keyword_search = v2_keyword_memory.keyword_search
load_sample_docs = v3_vector_retrieval.load_sample_docs
build_index = v3_vector_retrieval.build_index
answer_with_retrieval = v3_vector_retrieval.answer_with_retrieval
search_with_fallback = v3_vector_retrieval.search_with_fallback
provider_health = v3_vector_retrieval.provider_health


def test_v1_hardcoded_hit() -> None:
    out = answer_hardcoded("tell me about session")
    assert "session" in out.lower()


def test_v2_keyword_search_has_hits() -> None:
    lines = load_memory_lines()
    hits = keyword_search("session policy", lines)
    assert len(hits) >= 1


def test_v3_retrieval_answer_shape() -> None:
    docs = load_sample_docs()
    index = build_index(docs)
    out = answer_with_retrieval("session isolation", index)
    assert out.startswith("Retrieved:")


def test_v3_fallback_attempts_shape() -> None:
    docs = load_sample_docs()
    index = build_index(docs)
    result = search_with_fallback("session isolation", index, provider_order=["local-index", "memory-lines"])
    assert result["ok"] is True
    assert result["provider_used"] == "local-index"
    attempts = result["attempts"]
    assert isinstance(attempts, list)
    assert attempts[0]["provider"] == "local-index"
    assert attempts[0]["ok"] is True


def test_v3_provider_health_updates() -> None:
    provider_health.clear()
    docs = load_sample_docs()
    index = build_index(docs)
    _ = search_with_fallback("session isolation", index, provider_order=["local-index"])
    assert provider_health["local-index"]["total"] >= 1
    assert provider_health["local-index"]["success"] >= 1
