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


v1_hard_truncate = _load_local_module("v1_hard_truncate.py", "chapter07_v1_hard_truncate")
v2_summary_compaction = _load_local_module("v2_summary_compaction.py", "chapter07_v2_summary_compaction")
v3_compaction_pruning = _load_local_module("v3_compaction_pruning.py", "chapter07_v3_compaction_pruning")


hard_truncate = v1_hard_truncate.hard_truncate
compact_with_summary = v2_summary_compaction.compact_with_summary
Memory = v3_compaction_pruning.Memory
compact_memory = v3_compaction_pruning.compact_memory
prune_tool_results = v3_compaction_pruning.prune_tool_results
prune_working_messages = v3_compaction_pruning.prune_working_messages


def test_v1_hard_truncate() -> None:
    out = hard_truncate(["a", "b", "c", "d"], keep_last=2)
    assert out == ["c", "d"]


def test_v2_summary_compaction() -> None:
    out = compact_with_summary(["m1", "m2", "m3", "m4"], keep_last=2)
    assert "summary:" in out["summary"]
    assert out["working"] == ["m3", "m4"]


def test_v3_compact_and_prune() -> None:
    mem = Memory(working=["1", "2", "3", "4"], tool_results=["a", "b", "c"])
    compact_memory(mem, working_limit=2)
    prune_tool_results(mem, tool_limit=2)
    assert len(mem.working) == 2
    assert len(mem.tool_results) == 2
    assert len(mem.summary) == 1


def test_v3_prune_by_token_budget() -> None:
    working = ["short", "another short", "x" * 80]
    pruned = prune_working_messages(working, max_messages=3, max_tokens=8)
    assert len(pruned) == 1
    assert pruned[0] == "x" * 80
