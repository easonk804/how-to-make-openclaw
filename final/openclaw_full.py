#!/usr/bin/env python3
"""
OpenClaw Full (integrated demo)

This script stitches together simplified pieces from chapter 01-10
to show a compact end-to-end OpenClaw teaching pipeline.
"""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(relative_path: str, alias: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


def run_full_demo() -> dict[str, object]:
    # chapter 01: gateway event loop
    ch01 = _load_module("chapters/01_gateway_event_loop/v1_sync_flow.py", "final_ch01_v1")
    ch01_out = ch01.handle_sync("please create file")

    # chapter 02: adapter registry
    ch02 = _load_module(
        "chapters/02_channel_adapter_registry/v3_registry_dispatch.py",
        "final_ch02_v3",
    )
    workspace = Path(__file__).resolve().parent / "sandbox"
    workspace.mkdir(parents=True, exist_ok=True)
    registry = ch02.build_registry(workspace)
    write_out = registry.dispatch("write_file", path="demo.txt", content="hello from final demo\n")
    read_out = registry.dispatch("read_file", path="demo.txt")

    # chapter 03: session routing policy
    ch03 = _load_module("chapters/03_session_and_dm_scope/v3_scope_policy.py", "final_ch03_v3")
    session_out = ch03.route_session(
        {"channel": "telegram", "user": "alice", "is_dm": True},
        policy="per-peer",
    )

    # chapter 04: react + tool stream
    ch04 = _load_module("chapters/04_react_and_tool_stream/v3_react_tool_stream.py", "final_ch04_v3")
    react_trace, react_final = ch04.react_solve("ModuleNotFoundError: No module named 'requests'")

    # chapter 05: retry + recovery
    ch05 = _load_module("chapters/05_retry_and_recovery/v3_adaptive_retry.py", "final_ch05_v3")
    retry_status, retry_logs = ch05.run_with_adaptive_retry(
        simulated_errors=["network timeout", "network timeout"],
        max_retries=4,
    )

    # chapter 06: workspace memory retrieval
    ch06 = _load_module(
        "chapters/06_workspace_memory_and_search/v3_vector_retrieval.py",
        "final_ch06_v3",
    )
    docs = ch06.load_sample_docs()
    index = ch06.build_index(docs)
    rag_answer = ch06.answer_with_retrieval("How does session isolation work?", index)
    search_trace = ch06.search_with_fallback(
        "How does session isolation work?",
        index,
        provider_order=["local-index", "memory-lines"],
        top_k=1,
    )

    # chapter 07: compaction + pruning
    ch07 = _load_module(
        "chapters/07_compaction_and_pruning/v3_compaction_pruning.py",
        "final_ch07_v3",
    )
    mem = ch07.Memory(
        working=[
            "topic=final integration",
            "chapter=07",
            "need short prompt",
            "todo=add tests",
            "style=beginner",
        ],
        tool_results=["tool:step1", "tool:step2", "tool:step3"],
    )
    ch07.compact_memory(mem, working_limit=2, max_tokens=12)
    ch07.prune_tool_results(mem, tool_limit=2)
    compacted_prompt = ch07.memory_prompt(mem)

    # chapter 08: queue lanes + concurrency
    ch08 = _load_module(
        "chapters/08_queue_and_concurrency_lanes/v3_lane_concurrency.py",
        "final_ch08_v3",
    )
    async_results, lane_trace = asyncio.run(
        ch08.run_with_lanes_trace(
            [("A", "s1", 0.02), ("B", "s1", 0.0), ("C", "s2", 0.01)],
            lane_limit=1,
            global_limit=2,
        )
    )

    # chapter 09: multi-agent routing
    ch09_v2 = _load_module("chapters/09_multi_agent_routing/v2_central_router.py", "final_ch09_v2")
    ch09_v3 = _load_module("chapters/09_multi_agent_routing/v3_isolated_routing.py", "final_ch09_v3")
    centralized_logs = ch09_v2.run_centralized(["build ui", "implement api"])
    matched = ch09_v2.route_task_with_match("build ui")
    decentralized_logs = ch09_v3.decentralized_run()

    # chapter 10: security + sandbox + audit
    ch10 = _load_module(
        "chapters/10_security_sandbox_pairing/v3_sandbox_audit.py",
        "final_ch10_v3",
    )
    ch10.clear_audit()
    decision, audit = ch10.enforce("rm -rf /tmp/demo")
    audit_rows = ch10.list_audit(limit=1)

    return {
        "ch01_action": ch01_out["action"],
        "ch02_write": write_out,
        "ch02_read": read_out,
        "ch03_session": session_out["session_key"],
        "ch04_final": react_final,
        "ch04_steps": len(react_trace),
        "ch05_status": retry_status,
        "ch05_logs": retry_logs,
        "ch06_answer": rag_answer,
        "ch06_provider": search_trace.get("provider_used"),
        "ch06_attempts": len(search_trace.get("attempts", [])),
        "ch07_prompt": compacted_prompt,
        "ch08_results": async_results,
        "ch08_trace_steps": len(lane_trace),
        "ch09_centralized": centralized_logs,
        "ch09_decentralized": decentralized_logs,
        "ch09_matched_by": matched["matched_by"],
        "ch10_decision": decision,
        "ch10_audit": str(audit),
        "ch10_audit_summary": {
            "count": len(audit_rows),
            "last_reason": audit_rows[0].reason if audit_rows else "",
        },
    }


def main() -> None:
    result = run_full_demo()
    print("=== OpenClaw Full Demo ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
