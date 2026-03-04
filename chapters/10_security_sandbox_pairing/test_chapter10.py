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


v1_no_protection = _load_local_module("v1_no_protection.py", "chapter10_v1_no_protection")
v2_policy_pairing = _load_local_module("v2_policy_pairing.py", "chapter10_v2_policy_pairing")
v3_sandbox_audit = _load_local_module("v3_sandbox_audit.py", "chapter10_v3_sandbox_audit")


execute_without_guard = v1_no_protection.execute_without_guard
enforce_dm_policy = v2_policy_pairing.enforce_dm_policy
enforce = v3_sandbox_audit.enforce
list_audit = v3_sandbox_audit.list_audit
clear_audit = v3_sandbox_audit.clear_audit


def test_v1_no_protection_allows() -> None:
    out = execute_without_guard("rm -rf /tmp/demo")
    assert out["decision"] == "allowed"


def test_v2_dm_policy_blocks_unpaired() -> None:
    decision, reason = enforce_dm_policy(True, "alice", "paired_only", {"bob"})
    assert decision == "blocked"
    assert reason == "dm-policy"


def test_v3_enforce_blocks_dangerous_command() -> None:
    clear_audit()
    decision, record = enforce("rm -rf /tmp/demo")
    assert decision == "blocked"
    assert record.reason == "sandbox_dangerous_pattern"


def test_v3_enforce_blocks_non_whitelisted_command() -> None:
    clear_audit()
    decision, record = enforce("curl http://example.com")
    assert decision == "blocked"
    assert record.reason.startswith("whitelist_block:")


def test_v3_audit_list_contains_latest_record() -> None:
    clear_audit()
    _ = enforce("echo hello")
    rows = list_audit(limit=1)
    assert len(rows) == 1
    assert rows[0].command == "echo hello"
