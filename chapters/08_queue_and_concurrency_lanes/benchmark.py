"""
Benchmark script for Chapter 08: Queue and Concurrency Lanes

Run with: python chapters/08_queue_and_concurrency_lanes/benchmark.py
"""

from __future__ import annotations

import asyncio
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


v3 = _load_local_module("v3_lane_concurrency.py", "benchmark_v3")
run_with_lanes = v3.run_with_lanes


async def benchmark_concurrent_tasks(
    task_counts: list[int],
    lane_limits: list[int],
    global_limits: list[int],
) -> dict[str, list[dict]]:
    results: dict[str, list[dict]] = {
        "by_task_count": [],
        "by_lane_limit": [],
        "by_global_limit": [],
    }

    # Benchmark varying task counts
    for count in task_counts:
        tasks = [(f"task-{i}", f"lane-{i % 3}") for i in range(count)]
        start = time.perf_counter()
        await run_with_lanes(tasks, lane_limit=1, global_limit=4)
        elapsed = time.perf_counter() - start
        results["by_task_count"].append({
            "count": count,
            "elapsed_ms": round(elapsed * 1000, 2),
        })

    # Benchmark varying lane limits
    base_tasks = [(f"t{i}", f"l{i % 3}") for i in range(12)]
    for lane_limit in lane_limits:
        start = time.perf_counter()
        await run_with_lanes(base_tasks, lane_limit=lane_limit, global_limit=6)
        elapsed = time.perf_counter() - start
        results["by_lane_limit"].append({
            "lane_limit": lane_limit,
            "elapsed_ms": round(elapsed * 1000, 2),
        })

    # Benchmark varying global limits
    for global_limit in global_limits:
        start = time.perf_counter()
        await run_with_lanes(base_tasks, lane_limit=1, global_limit=global_limit)
        elapsed = time.perf_counter() - start
        results["by_global_limit"].append({
            "global_limit": global_limit,
            "elapsed_ms": round(elapsed * 1000, 2),
        })

    return results


def print_report(results: dict[str, list[dict]]) -> None:
    print("=" * 50)
    print("Chapter 08 Benchmark Report")
    print("=" * 50)

    print("\n[Task Count Scaling]")
    for r in results["by_task_count"]:
        print(f"  Tasks: {r['count']:3d} | Time: {r['elapsed_ms']:6.2f} ms")

    print("\n[Lane Limit Scaling]")
    for r in results["by_lane_limit"]:
        print(f"  Lane Limit: {r['lane_limit']} | Time: {r['elapsed_ms']:6.2f} ms")

    print("\n[Global Limit Scaling]")
    for r in results["by_global_limit"]:
        print(f"  Global Limit: {r['global_limit']} | Time: {r['elapsed_ms']:6.2f} ms")

    print("\n" + "=" * 50)


async def main() -> None:
    results = await benchmark_concurrent_tasks(
        task_counts=[6, 12, 24],
        lane_limits=[1, 2, 4],
        global_limits=[2, 4, 6],
    )
    print_report(results)


if __name__ == "__main__":
    asyncio.run(main())
