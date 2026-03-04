"""
Benchmark script for Chapter 06: Workspace Memory and Search

Run with: python chapters/06_workspace_memory_and_search/benchmark.py
"""

from __future__ import annotations

import time
from pathlib import Path
import importlib.util
import sys


def _load_local_module(module_filename: str, alias: str):
    path = Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {module_filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


v3 = _load_local_module("v3_vector_retrieval.py", "benchmark_v3")
load_sample_docs = v3.load_sample_docs
build_index = v3.build_index
retrieve_top_k = v3.retrieve_top_k
answer_with_retrieval = v3.answer_with_retrieval
search_with_fallback = v3.search_with_fallback


def benchmark_memory_search(
    doc_counts: list[int],
    top_k_values: list[int],
    query_counts: int = 10,
) -> dict[str, list[dict]]:
    results: dict[str, list[dict]] = {
        "index_building": [],
        "query_by_doc_count": [],
        "query_by_top_k": [],
        "fallback_chain": [],
    }

    # Benchmark index building with varying doc counts
    base_docs = load_sample_docs()
    for count in doc_counts:
        # Replicate docs to reach target count
        replicated = []
        for i in range(count):
            doc = base_docs[i % len(base_docs)]
            replicated.append({"id": f"d{i}", "text": f"{doc['text']} variant {i}"})
        
        start = time.perf_counter()
        index = build_index(replicated)
        elapsed = time.perf_counter() - start
        results["index_building"].append({
            "doc_count": count,
            "elapsed_ms": round(elapsed * 1000, 3),
            "index_size": len(index),
        })

    # Benchmark queries with varying doc counts
    for count in doc_counts:
        replicated = []
        for i in range(count):
            doc = base_docs[i % len(base_docs)]
            replicated.append({"id": f"d{i}", "text": f"{doc['text']} variant {i}"})
        index = build_index(replicated)
        
        query_times = []
        for _ in range(query_counts):
            start = time.perf_counter()
            answer_with_retrieval("session isolation policy", index)
            query_times.append(time.perf_counter() - start)
        
        avg_time = sum(query_times) / len(query_times)
        results["query_by_doc_count"].append({
            "doc_count": count,
            "queries": query_counts,
            "avg_elapsed_ms": round(avg_time * 1000, 3),
            "total_elapsed_ms": round(sum(query_times) * 1000, 3),
        })

    # Benchmark varying top_k values
    docs = load_sample_docs()
    index = build_index(docs)
    for top_k in top_k_values:
        query_times = []
        for _ in range(query_counts):
            start = time.perf_counter()
            retrieve_top_k("session queue sandbox", index, top_k)
            query_times.append(time.perf_counter() - start)
        
        avg_time = sum(query_times) / len(query_times)
        results["query_by_top_k"].append({
            "top_k": top_k,
            "avg_elapsed_ms": round(avg_time * 1000, 3),
        })

    # Benchmark fallback chain
    docs = load_sample_docs()
    index = build_index(docs)
    fallback_scenarios = [
        (["local-index"], "single provider"),
        (["local-index", "memory-lines"], "two providers"),
        (["memory-lines", "local-index"], "reversed order"),
    ]
    for provider_order, scenario in fallback_scenarios:
        start = time.perf_counter()
        result = search_with_fallback("sandbox security", index, provider_order, top_k=2)
        elapsed = time.perf_counter() - start
        results["fallback_chain"].append({
            "scenario": scenario,
            "provider_order": provider_order,
            "elapsed_ms": round(elapsed * 1000, 3),
            "provider_used": result.get("provider_used"),
            "attempts": len(result.get("attempts", [])),
        })

    return results


def print_report(results: dict[str, list[dict]]) -> None:
    print("=" * 70)
    print("Chapter 06 Benchmark Report: Workspace Memory and Search")
    print("=" * 70)

    print("\n[Index Building Performance]")
    print(f"{'Doc Count':>12} | {'Time (ms)':>12} | {'Index Size':>12}")
    print("-" * 70)
    for r in results["index_building"]:
        print(f"{r['doc_count']:>12} | {r['elapsed_ms']:>12.3f} | {r['index_size']:>12}")

    print("\n[Query Performance by Document Count]")
    print(f"{'Doc Count':>12} | {'Queries':>10} | {'Avg (ms)':>12} | {'Total (ms)':>12}")
    print("-" * 70)
    for r in results["query_by_doc_count"]:
        print(f"{r['doc_count']:>12} | {r['queries']:>10} | {r['avg_elapsed_ms']:>12.3f} | {r['total_elapsed_ms']:>12.3f}")

    print("\n[Query Performance by Top-K]")
    print(f"{'Top-K':>12} | {'Avg Time (ms)':>15}")
    print("-" * 70)
    for r in results["query_by_top_k"]:
        print(f"{r['top_k']:>12} | {r['avg_elapsed_ms']:>15.3f}")

    print("\n[Provider Fallback Chain]")
    print(f"{'Scenario':>25} | {'Time (ms)':>12} | {'Provider':>15} | {'Attempts':>10}")
    print("-" * 70)
    for r in results["fallback_chain"]:
        print(f"{r['scenario']:>25} | {r['elapsed_ms']:>12.3f} | {r['provider_used']:>15} | {r['attempts']:>10}")

    print("\n" + "=" * 70)


def main() -> None:
    results = benchmark_memory_search(
        doc_counts=[3, 10, 30, 100],
        top_k_values=[1, 2, 3, 5],
        query_counts=20,
    )
    print_report(results)


if __name__ == "__main__":
    main()
