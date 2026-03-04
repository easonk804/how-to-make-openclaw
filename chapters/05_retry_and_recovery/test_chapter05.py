from pathlib import Path
import importlib.util


def _load_local_module(module_filename: str, alias: str):
    path = Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {module_filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v1_fail_stop = _load_local_module("v1_fail_stop.py", "chapter05_v1_fail_stop")
v2_fixed_retry = _load_local_module("v2_fixed_retry.py", "chapter05_v2_fixed_retry")
v3_adaptive_retry = _load_local_module("v3_adaptive_retry.py", "chapter05_v3_adaptive_retry")


run_once = v1_fail_stop.run_once
run_with_fixed_retry = v2_fixed_retry.run_with_fixed_retry
run_with_adaptive_retry = v3_adaptive_retry.run_with_adaptive_retry


def test_v1_fail_stop() -> None:
    status, logs = run_once("timeout")
    assert status == "failed"
    assert logs[-1] == "stop"


def test_v2_fixed_retry_success_after_errors() -> None:
    status, logs = run_with_fixed_retry(["timeout", "timeout"], max_retries=3)
    assert status == "success"
    assert "success" in logs


def test_v3_fatal_error_stops_early() -> None:
    status, logs = run_with_adaptive_retry(["permission denied", "timeout"], max_retries=4)
    assert status == "failed"
    decisions = [entry for entry in logs if entry["event"] == "decision"]
    assert decisions[-1]["value"] == "stop"


def test_v3_transient_error_records_retry_backoff() -> None:
    status, logs = run_with_adaptive_retry(["network timeout"], max_retries=2)
    assert status == "success"
    delays = [entry for entry in logs if entry["event"] == "retry_delay_ms"]
    assert len(delays) == 1
    assert delays[0]["value"] == "1000"
