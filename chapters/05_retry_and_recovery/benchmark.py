"""
Benchmark script for Chapter 05: Retry and Recovery

Run with: python chapters/05_retry_and_recovery/benchmark.py
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


v3 = _load_local_module("v3_adaptive_retry.py", "benchmark_v3")
run_with_adaptive_retry = v3.run_with_adaptive_retry


def benchmark_retry_policies(
    error_counts: list[int],
    max_retries_list: list[int],
) -> dict[str, list[dict]]:
    results: dict[str, list[dict]] = {
        "by_error_count": [],
        "by_max_retries": [],
        "error_classification": [],
    }

    # Benchmark varying error counts
    for count in error_counts:
        errors = ["network timeout"] * count
        start = time.perf_counter()
        status, logs = run_with_adaptive_retry(errors, max_retries=max(count, 3))
        elapsed = time.perf_counter() - start
        results["by_error_count"].append({
            "error_count": count,
            "elapsed_ms": round(elapsed * 1000, 3),
            "status": status,
            "log_entries": len(logs),
        })

    # Benchmark varying max retry limits
    base_errors = ["network timeout", "network timeout", "timeout"]
    for max_retry in max_retries_list:
        start = time.perf_counter()
        status, logs = run_with_adaptive_retry(base_errors, max_retries=max_retry)
        elapsed = time.perf_counter() - start
        results["by_max_retries"].append({
            "max_retries": max_retry,
            "elapsed_ms": round(elapsed * 1000, 3),
            "status": status,
        })

    # Benchmark error classification
    error_types = [
        (["network timeout"], "transient"),
        (["permission denied"], "fatal"),
        (["401 unauthorized"], "fatal"),
        (["500 server error"], "transient"),
    ]
    for errors, expected_category in error_types:
        start = time.perf_counter()
        _, logs = run_with_adaptive_retry(errors, max_retries=2)
        elapsed = time.perf_counter() - start
        # Find classification in logs
        category = "unknown"
        for log in logs:
            if log.get("event") == "category":
                category = log.get("value", "unknown")
                break
        results["error_classification"].append({
            "error": errors[0],
            "classified": category,
            "expected": expected_category,
            "match": category == expected_category,
            "elapsed_ms": round(elapsed * 1000, 3),
        })

    return results


def print_report(results: dict[str, list[dict]]) -> None:
    print("=" * 60)
    print("Chapter 05 Benchmark Report: Retry and Recovery")
    print("=" * 60)

    print("\n[Error Count Scaling]")
    print(f"{'Errors':>10} | {'Time (ms)':>10} | {'Status':>10} | {'Log Entries':>12}")
    print("-" * 60)
    for r in results["by_error_count"]:
        print(f"{r['error_count']:>10} | {r['elapsed_ms']:>10.3f} | {r['status']:>10} | {r['log_entries']:>12}")

    print("\n[Max Retries Scaling]")
    print(f"{'Max Retries':>12} | {'Time (ms)':>10} | {'Status':>10}")
    print("-" * 60)
    for r in results["by_max_retries"]:
        print(f"{r['max_retries']:>12} | {r['elapsed_ms']:>10.3f} | {r['status']:>10}")

    print("\n[Error Classification Accuracy]")
    print(f"{'Error':>20} | {'Classified':>12} | {'Expected':>10} | {'Match':>6}")
    print("-" * 60)
    for r in results["error_classification"]:
        match_str = "✓" if r["match"] else "✗"
        print(f"{r['error']:>20} | {r['classified']:>12} | {r['expected']:>10} | {match_str:>6}")

    print("\n" + "=" * 60)


def main() -> None:
    results = benchmark_retry_policies(
        error_counts=[1, 3, 5, 10],
        max_retries_list=[2, 4, 6, 8],
    )
    print_report(results)


if __name__ == "__main__":
    main()
