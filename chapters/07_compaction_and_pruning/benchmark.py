"""
Benchmark script for Chapter 07: Compaction and Pruning

Run with: python chapters/07_compaction_and_pruning/benchmark.py
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


v3 = _load_local_module("v3_compaction_pruning.py", "benchmark_v3")
Memory = v3.Memory
compact_memory = v3.compact_memory
prune_tool_results = v3.prune_tool_results
memory_prompt = v3.memory_prompt


def benchmark_compaction(
    memory_sizes: list[int],
    working_limits: list[int],
    token_budgets: list[int],
) -> dict[str, list[dict]]:
    results: dict[str, list[dict]] = {
        "compaction_by_size": [],
        "compaction_by_limit": [],
        "token_budget_pruning": [],
        "pruning_by_tool_limit": [],
        "prompt_building": [],
    }

    # Benchmark compaction with varying memory sizes
    for size in memory_sizes:
        working = [f"message_{i}" for i in range(size)]
        mem = Memory(working=working, tool_results=[])
        
        start = time.perf_counter()
        compact_memory(mem, working_limit=10)
        elapsed = time.perf_counter() - start
        
        results["compaction_by_size"].append({
            "original_size": size,
            "after_compact": len(mem.working),
            "summary_length": len(mem.summary),
            "elapsed_ms": round(elapsed * 1000, 3),
        })

    # Benchmark compaction with varying working limits
    base_size = 50
    for limit in working_limits:
        working = [f"msg_{i}" for i in range(base_size)]
        mem = Memory(working=working, tool_results=[])
        
        start = time.perf_counter()
        compact_memory(mem, working_limit=limit)
        elapsed = time.perf_counter() - start
        
        results["compaction_by_limit"].append({
            "working_limit": limit,
            "original_size": base_size,
            "after_compact": len(mem.working),
            "elapsed_ms": round(elapsed * 1000, 3),
        })

    # Benchmark token budget pruning
    for budget in token_budgets:
        working = ["short", "medium length message", "this is a longer message with more tokens"]
        mem = Memory(working=working, tool_results=[])
        
        start = time.perf_counter()
        compact_memory(mem, working_limit=10, max_tokens=budget)
        elapsed = time.perf_counter() - start
        
        estimated_tokens = sum(len(w) for w in mem.working)
        results["token_budget_pruning"].append({
            "token_budget": budget,
            "working_count": len(mem.working),
            "estimated_tokens": estimated_tokens,
            "within_budget": estimated_tokens <= budget,
            "elapsed_ms": round(elapsed * 1000, 3),
        })

    # Benchmark tool result pruning
    tool_counts = [5, 10, 20, 50]
    for count in tool_counts:
        tools = [f"tool_result_{i}" for i in range(count)]
        mem = Memory(working=[], tool_results=tools)
        
        start = time.perf_counter()
        prune_tool_results(mem, tool_limit=5)
        elapsed = time.perf_counter() - start
        
        results["pruning_by_tool_limit"].append({
            "original_tools": count,
            "after_prune": len(mem.tool_results),
            "elapsed_ms": round(elapsed * 1000, 3),
        })

    # Benchmark prompt building
    prompt_sizes = [10, 50, 100, 200]
    for size in prompt_sizes:
        working = [f"line_{i}" for i in range(size)]
        tools = [f"tool_{i}" for i in range(min(size // 5, 10))]
        mem = Memory(working=working, tool_results=tools)
        compact_memory(mem, working_limit=20)
        prune_tool_results(mem, tool_limit=5)
        
        start = time.perf_counter()
        prompt = memory_prompt(mem)
        elapsed = time.perf_counter() - start
        
        results["prompt_building"].append({
            "working_size": len(mem.working),
            "tool_size": len(mem.tool_results),
            "prompt_length": len(prompt),
            "elapsed_ms": round(elapsed * 1000, 3),
        })

    return results


def print_report(results: dict[str, list[dict]]) -> None:
    print("=" * 70)
    print("Chapter 07 Benchmark Report: Compaction and Pruning")
    print("=" * 70)

    print("\n[Compaction by Memory Size]")
    print(f"{'Original':>12} | {'After':>10} | {'Summary Len':>12} | {'Time (ms)':>12}")
    print("-" * 70)
    for r in results["compaction_by_size"]:
        print(f"{r['original_size']:>12} | {r['after_compact']:>10} | {r['summary_length']:>12} | {r['elapsed_ms']:>12.3f}")

    print("\n[Compaction by Working Limit]")
    print(f"{'Limit':>10} | {'Original':>12} | {'After':>10} | {'Time (ms)':>12}")
    print("-" * 70)
    for r in results["compaction_by_limit"]:
        print(f"{r['working_limit']:>10} | {r['original_size']:>12} | {r['after_compact']:>10} | {r['elapsed_ms']:>12.3f}")

    print("\n[Token Budget Pruning]")
    print(f"{'Budget':>10} | {'Working':>10} | {'Est. Tokens':>12} | {'Within':>8} | {'Time (ms)':>12}")
    print("-" * 70)
    for r in results["token_budget_pruning"]:
        within = "✓" if r['within_budget'] else "✗"
        print(f"{r['token_budget']:>10} | {r['working_count']:>10} | {r['estimated_tokens']:>12} | {within:>8} | {r['elapsed_ms']:>12.3f}")

    print("\n[Tool Result Pruning]")
    print(f"{'Original':>12} | {'After':>10} | {'Time (ms)':>12}")
    print("-" * 70)
    for r in results["pruning_by_tool_limit"]:
        print(f"{r['original_tools']:>12} | {r['after_prune']:>10} | {r['elapsed_ms']:>12.3f}")

    print("\n[Prompt Building Performance]")
    print(f"{'Working':>10} | {'Tools':>8} | {'Prompt Len':>12} | {'Time (ms)':>12}")
    print("-" * 70)
    for r in results["prompt_building"]:
        print(f"{r['working_size']:>10} | {r['tool_size']:>8} | {r['prompt_length']:>12} | {r['elapsed_ms']:>12.3f}")

    print("\n" + "=" * 70)


def main() -> None:
    results = benchmark_compaction(
        memory_sizes=[10, 50, 100, 200],
        working_limits=[5, 10, 20, 50],
        token_budgets=[100, 200, 500, 1000],
    )
    print_report(results)


if __name__ == "__main__":
    main()
