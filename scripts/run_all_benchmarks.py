"""
Master Benchmark Runner for How-to-Make-OpenClaw

Runs all chapter benchmarks and generates a comprehensive report.

Usage:
    python scripts/run_all_benchmarks.py
    python scripts/run_all_benchmarks.py --chapters 05,06,07
    python scripts/run_all_benchmarks.py --format json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


CHAPTER_BENCHMARKS = {
    "05": "chapters/05_retry_and_recovery/benchmark.py",
    "06": "chapters/06_workspace_memory_and_search/benchmark.py",
    "07": "chapters/07_compaction_and_pruning/benchmark.py",
    "08": "chapters/08_queue_and_concurrency_lanes/benchmark.py",
    "09": "chapters/09_multi_agent_routing/benchmark.py",
    "10": "chapters/10_security_sandbox_pairing/benchmark.py",
}


def run_benchmark(chapter: str, script_path: str) -> dict[str, Any]:
    """Run a single chapter benchmark and return results."""
    root = Path(__file__).resolve().parents[1]
    full_path = root / script_path
    
    if not full_path.exists():
        return {
            "chapter": chapter,
            "status": "skipped",
            "error": f"Benchmark script not found: {script_path}",
        }
    
    try:
        result = subprocess.run(
            [sys.executable, str(full_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=root,
        )
        
        return {
            "chapter": chapter,
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout,
            "stderr": result.stderr if result.stderr else None,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "chapter": chapter,
            "status": "timeout",
            "error": "Benchmark exceeded 60 second timeout",
        }
    except Exception as e:
        return {
            "chapter": chapter,
            "status": "error",
            "error": str(e),
        }


def print_summary(results: list[dict[str, Any]]) -> None:
    """Print a summary of all benchmark results."""
    print("\n" + "=" * 70)
    print("MASTER BENCHMARK REPORT")
    print("=" * 70)
    
    total = len(results)
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    errors = sum(1 for r in results if r["status"] not in ("success", "failed", "skipped"))
    
    print(f"\nTotal benchmarks: {total}")
    print(f"  ✓ Success: {success}")
    print(f"  ✗ Failed: {failed}")
    print(f"  ○ Skipped: {skipped}")
    print(f"  ! Errors: {errors}")
    
    print("\nChapter Details:")
    print("-" * 70)
    
    for result in results:
        chapter = result["chapter"]
        status = result["status"]
        
        if status == "success":
            icon = "✓"
        elif status == "failed":
            icon = "✗"
        elif status == "skipped":
            icon = "○"
        else:
            icon = "!"
        
        print(f"  {icon} Chapter {chapter}: {status.upper()}")
        
        if status == "success":
            # Extract key metrics from output if available
            output = result.get("output", "")
            if "elapsed_ms" in output.lower():
                # Try to find timing information
                lines = output.split("\n")
                for line in lines:
                    if "ms" in line and any(c.isdigit() for c in line):
                        print(f"      └─ {line.strip()[:60]}")
                        break
    
    print("\n" + "=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run all chapter benchmarks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Run all benchmarks
  %(prog)s --chapters 05,06,07      # Run specific chapters
  %(prog)s --format json            # Output as JSON
  %(prog)s --quiet                  # Minimal output
        """,
    )
    
    parser.add_argument(
        "--chapters",
        type=str,
        help="Comma-separated list of chapters to run (e.g., 05,06,07)",
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress individual benchmark output",
    )
    
    args = parser.parse_args()
    
    # Determine which chapters to run
    if args.chapters:
        chapters_to_run = args.chapters.split(",")
        # Validate chapter numbers
        for ch in chapters_to_run:
            if ch not in CHAPTER_BENCHMARKS:
                print(f"Warning: Unknown chapter '{ch}', skipping", file=sys.stderr)
    else:
        chapters_to_run = list(CHAPTER_BENCHMARKS.keys())
    
    # Run benchmarks
    results: list[dict[str, Any]] = []
    
    for chapter in chapters_to_run:
        if chapter not in CHAPTER_BENCHMARKS:
            continue
        
        script_path = CHAPTER_BENCHMARKS[chapter]
        
        if not args.quiet:
            print(f"\nRunning Chapter {chapter} benchmark...", file=sys.stderr)
        
        result = run_benchmark(chapter, script_path)
        results.append(result)
        
        if not args.quiet and result["status"] == "success":
            print(result.get("output", ""))
        elif not args.quiet and result.get("stderr"):
            print(result["stderr"], file=sys.stderr)
    
    # Output results
    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print_summary(results)


if __name__ == "__main__":
    main()
