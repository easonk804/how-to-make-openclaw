"""
Benchmark script for Chapter 10: Security Sandbox Pairing

Run with: python chapters/10_security_sandbox_pairing/benchmark.py
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


v3 = _load_local_module("v3_sandbox_audit.py", "benchmark_v3")
enforce = v3.enforce
clear_audit = v3.clear_audit
list_audit = v3.list_audit


def benchmark_security(
    command_counts: list[int],
    whitelist_sizes: list[int],
) -> dict[str, list[dict]]:
    results: dict[str, list[dict]] = {
        "dangerous_detection": [],
        "whitelist_check": [],
        "audit_logging": [],
        "audit_retrieval": [],
        "decision_accuracy": [],
    }

    # Benchmark dangerous command detection
    dangerous_commands = [
        ("rm -rf /tmp/data", True, "sandbox_dangerous_pattern"),
        ("del /f C:\\Windows", True, "sandbox_dangerous_pattern"),
        ("format C:", True, "sandbox_dangerous_pattern"),
        ("echo hello", False, "sandbox_ok"),
        ("ls -la", False, "sandbox_ok"),
        ("pwd", False, "sandbox_ok"),
    ]
    
    for cmd, should_block, expected_reason in dangerous_commands:
        times = []
        for _ in range(100):
            start = time.perf_counter()
            decision, record = enforce(cmd)
            times.append(time.perf_counter() - start)
        
        avg_time = sum(times) / len(times)
        correct = (decision == "blocked") == should_block and record.reason.startswith(expected_reason.split(":")[0])
        
        results["dangerous_detection"].append({
            "command": cmd[:25],
            "decision": decision,
            "expected_block": should_block,
            "reason": record.reason[:30],
            "correct": correct,
            "avg_elapsed_ms": round(avg_time * 1000, 4),
        })

    # Benchmark whitelist checking with varying whitelist sizes
    for size in whitelist_sizes:
        whitelist = [f"cmd_{i}" for i in range(size)]
        test_cmd = "cmd_unknown"
        
        times = []
        for _ in range(50):
            start = time.perf_counter()
            decision, _ = enforce(test_cmd, whitelist)
            times.append(time.perf_counter() - start)
        
        avg_time = sum(times) / len(times)
        results["whitelist_check"].append({
            "whitelist_size": size,
            "command": test_cmd,
            "decision": decision,
            "avg_elapsed_ms": round(avg_time * 1000, 4),
        })

    # Benchmark audit logging
    clear_audit()
    for count in command_counts:
        clear_audit()
        
        start = time.perf_counter()
        for i in range(count):
            enforce(f"echo test_{i}")
        elapsed = time.perf_counter() - start
        
        results["audit_logging"].append({
            "command_count": count,
            "elapsed_ms": round(elapsed * 1000, 3),
            "avg_per_command_ms": round(elapsed * 1000 / count, 4),
            "audit_size": len(list_audit(limit=count * 2)),
        })

    # Benchmark audit retrieval
    clear_audit()
    for i in range(100):
        enforce(f"echo test_{i}")
    
    for limit in [10, 50, 100, 200]:
        times = []
        for _ in range(20):
            start = time.perf_counter()
            records = list_audit(limit=limit)
            times.append(time.perf_counter() - start)
        
        avg_time = sum(times) / len(times)
        results["audit_retrieval"].append({
            "requested_limit": limit,
            "records_returned": len(list_audit(limit=limit)),
            "avg_elapsed_ms": round(avg_time * 1000, 4),
        })

    # Decision accuracy test
    accuracy_tests = [
        ("rm -rf /", "blocked", "sandbox_dangerous_pattern"),
        ("echo hello", "allowed", "sandbox_ok"),
        ("pwd", "allowed", "sandbox_ok"),
        ("curl http://example.com", "blocked", "whitelist_block"),
        ("", "blocked", "command_required"),
    ]
    
    for cmd, expected_decision, expected_reason_prefix in accuracy_tests:
        decision, record = enforce(cmd)
        correct = decision == expected_decision and record.reason.startswith(expected_reason_prefix)
        
        results["decision_accuracy"].append({
            "command": cmd[:20] or "<empty>",
            "decision": decision,
            "expected": expected_decision,
            "reason": record.reason[:25],
            "correct": correct,
        })

    return results


def print_report(results: dict[str, list[dict]]) -> None:
    print("=" * 70)
    print("Chapter 10 Benchmark Report: Security Sandbox Pairing")
    print("=" * 70)

    print("\n[Dangerous Command Detection]")
    print(f"{'Command':>25} | {'Decision':>10} | {'Correct':>8} | {'Avg (ms)':>10}")
    print("-" * 70)
    for r in results["dangerous_detection"]:
        correct = "✓" if r['correct'] else "✗"
        print(f"{r['command']:>25} | {r['decision']:>10} | {correct:>8} | {r['avg_elapsed_ms']:>10.4f}")

    print("\n[Whitelist Check Performance]")
    print(f"{'Whitelist Size':>15} | {'Command':>15} | {'Decision':>10} | {'Avg (ms)':>10}")
    print("-" * 70)
    for r in results["whitelist_check"]:
        print(f"{r['whitelist_size']:>15} | {r['command']:>15} | {r['decision']:>10} | {r['avg_elapsed_ms']:>10.4f}")

    print("\n[Audit Logging Performance]")
    print(f"{'Commands':>10} | {'Total (ms)':>12} | {'Avg (ms)':>10} | {'Audit Size':>12}")
    print("-" * 70)
    for r in results["audit_logging"]:
        print(f"{r['command_count']:>10} | {r['elapsed_ms']:>12.3f} | {r['avg_per_command_ms']:>10.4f} | {r['audit_size']:>12}")

    print("\n[Audit Retrieval Performance]")
    print(f"{'Limit':>10} | {'Returned':>10} | {'Avg (ms)':>10}")
    print("-" * 70)
    for r in results["audit_retrieval"]:
        print(f"{r['requested_limit']:>10} | {r['records_returned']:>10} | {r['avg_elapsed_ms']:>10.4f}")

    print("\n[Decision Accuracy]")
    print(f"{'Command':>20} | {'Decision':>10} | {'Expected':>10} | {'Correct':>8}")
    print("-" * 70)
    for r in results["decision_accuracy"]:
        correct = "✓" if r['correct'] else "✗"
        print(f"{r['command']:>20} | {r['decision']:>10} | {r['expected']:>10} | {correct:>8}")

    print("\n" + "=" * 70)


def main() -> None:
    results = benchmark_security(
        command_counts=[10, 50, 100, 200],
        whitelist_sizes=[5, 10, 20, 50],
    )
    print_report(results)


if __name__ == "__main__":
    main()
