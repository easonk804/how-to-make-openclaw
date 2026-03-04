"""
Benchmark script for Chapter 09: Multi-Agent Routing

Run with: python chapters/09_multi_agent_routing/benchmark.py
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


v2 = _load_local_module("v2_central_router.py", "benchmark_v2")
v3 = _load_local_module("v3_isolated_routing.py", "benchmark_v3")
route_task = v2.route_task
route_task_with_match = v2.route_task_with_match
run_centralized = v2.run_centralized
route_with_isolation = v3.route_with_isolation


def benchmark_routing(
    task_counts: list[int],
    binding_counts: list[int],
) -> dict[str, list[dict]]:
    results: dict[str, list[dict]] = {
        "single_routing": [],
        "batch_routing": [],
        "binding_lookup": [],
        "isolation_checks": [],
        "routing_accuracy": [],
    }

    # Benchmark single task routing
    test_tasks = [
        ("build ui components", "frontend_agent"),
        ("implement api endpoints", "backend_agent"),
        ("write unit tests", "qa_agent"),
        ("unknown task", "generalist_agent"),
    ]
    for task, expected in test_tasks:
        times = []
        for _ in range(100):
            start = time.perf_counter()
            agent = route_task(task)
            times.append(time.perf_counter() - start)
        
        avg_time = sum(times) / len(times)
        results["single_routing"].append({
            "task": task[:30],
            "routed_to": agent,
            "expected": expected,
            "correct": agent == expected,
            "avg_elapsed_ms": round(avg_time * 1000, 4),
        })

    # Benchmark batch routing with varying task counts
    base_tasks = [
        "build ui",
        "implement api",
        "write tests",
        "deploy service",
        "fix bug",
        "update docs",
    ]
    for count in task_counts:
        tasks = [base_tasks[i % len(base_tasks)] for i in range(count)]
        
        start = time.perf_counter()
        logs = run_centralized(tasks)
        elapsed = time.perf_counter() - start
        
        results["batch_routing"].append({
            "task_count": count,
            "logs_generated": len(logs),
            "elapsed_ms": round(elapsed * 1000, 3),
            "avg_per_task_ms": round(elapsed * 1000 / count, 4),
        })

    # Benchmark binding lookup with varying binding counts
    for count in binding_counts:
        # Create custom bindings
        bindings = {f"keyword_{i}": f"agent_{i % 5}" for i in range(count)}
        
        lookup_times = []
        for i in range(100):
            test_task = f"test keyword_{i % count} task"
            start = time.perf_counter()
            result = route_task_with_match(test_task, bindings)
            lookup_times.append(time.perf_counter() - start)
        
        avg_time = sum(lookup_times) / len(lookup_times)
        results["binding_lookup"].append({
            "binding_count": count,
            "lookups": 100,
            "avg_elapsed_ms": round(avg_time * 1000, 4),
        })

    # Benchmark isolation checks
    auth_states = ["allowed", "denied", "pending"]
    intents = ["frontend", "backend", "unknown"]
    for auth in auth_states:
        for intent in intents:
            times = []
            for _ in range(50):
                start = time.perf_counter()
                result = route_with_isolation("ws1", "alice", auth, intent)
                times.append(time.perf_counter() - start)
            
            avg_time = sum(times) / len(times)
            results["isolation_checks"].append({
                "auth": auth,
                "intent": intent,
                "status": result["status"],
                "avg_elapsed_ms": round(avg_time * 1000, 4),
            })

    # Routing accuracy test
    accuracy_tests = [
        ("build react ui", "frontend_agent", "build ui"),
        ("implement rest api", "backend_agent", "implement api"),
        ("write jest tests", "qa_agent", "write test"),
        ("random task", "generalist_agent", "default"),
    ]
    for task, expected_agent, expected_match in accuracy_tests:
        result = route_task_with_match(task)
        results["routing_accuracy"].append({
            "task": task,
            "routed_to": result["agent"],
            "matched_by": result["matched_by"],
            "expected_agent": expected_agent,
            "expected_match": expected_match,
            "agent_correct": result["agent"] == expected_agent,
            "match_correct": result["matched_by"] == expected_match,
        })

    return results


def print_report(results: dict[str, list[dict]]) -> None:
    print("=" * 70)
    print("Chapter 09 Benchmark Report: Multi-Agent Routing")
    print("=" * 70)

    print("\n[Single Task Routing Performance]")
    print(f"{'Task':>30} | {'Routed To':>15} | {'Correct':>8} | {'Avg (ms)':>10}")
    print("-" * 70)
    for r in results["single_routing"]:
        correct = "✓" if r['correct'] else "✗"
        print(f"{r['task']:>30} | {r['routed_to']:>15} | {correct:>8} | {r['avg_elapsed_ms']:>10.4f}")

    print("\n[Batch Routing Performance]")
    print(f"{'Tasks':>10} | {'Logs':>8} | {'Total (ms)':>12} | {'Avg/Task (ms)':>15}")
    print("-" * 70)
    for r in results["batch_routing"]:
        print(f"{r['task_count']:>10} | {r['logs_generated']:>8} | {r['elapsed_ms']:>12.3f} | {r['avg_per_task_ms']:>15.4f}")

    print("\n[Binding Lookup Performance]")
    print(f"{'Bindings':>12} | {'Lookups':>10} | {'Avg (ms)':>12}")
    print("-" * 70)
    for r in results["binding_lookup"]:
        print(f"{r['binding_count']:>12} | {r['lookups']:>10} | {r['avg_elapsed_ms']:>12.4f}")

    print("\n[Isolation Check Performance]")
    print(f"{'Auth':>10} | {'Intent':>12} | {'Status':>10} | {'Avg (ms)':>10}")
    print("-" * 70)
    for r in results["isolation_checks"]:
        print(f"{r['auth']:>10} | {r['intent']:>12} | {r['status']:>10} | {r['avg_elapsed_ms']:>10.4f}")

    print("\n[Routing Accuracy]")
    print(f"{'Task':>20} | {'Routed':>15} | {'Match':>12} | {'Correct':>8}")
    print("-" * 70)
    for r in results["routing_accuracy"]:
        correct = "✓" if r['agent_correct'] and r['match_correct'] else "✗"
        print(f"{r['task']:>20} | {r['routed_to']:>15} | {r['matched_by']:>12} | {correct:>8}")

    print("\n" + "=" * 70)


def main() -> None:
    results = benchmark_routing(
        task_counts=[10, 50, 100, 200],
        binding_counts=[10, 50, 100, 500],
    )
    print_report(results)


if __name__ == "__main__":
    main()
