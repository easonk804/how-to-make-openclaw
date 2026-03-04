from pathlib import Path


CHAPTERS = [
    "01_gateway_event_loop",
    "02_channel_adapter_registry",
    "03_session_and_dm_scope",
    "04_react_and_tool_stream",
    "05_retry_and_recovery",
    "06_workspace_memory_and_search",
    "07_compaction_and_pruning",
    "08_queue_and_concurrency_lanes",
    "09_multi_agent_routing",
    "10_security_sandbox_pairing",
]


def test_chapter_directories_exist() -> None:
    root = Path(__file__).resolve().parents[1] / "chapters"
    for name in CHAPTERS:
        assert (root / name).exists(), f"missing chapter dir: {name}"
