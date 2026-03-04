from pathlib import Path
import importlib.util
import sys


def _load_local_module(module_path: Path, alias: str):
    spec = importlib.util.spec_from_file_location(alias, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


root = Path(__file__).resolve().parents[1]
full_path = root / "final" / "openclaw_full.py"
full_mod = _load_local_module(full_path, "final_openclaw_full")
run_full_demo = full_mod.run_full_demo


def test_run_full_demo_output_shape() -> None:
    out = run_full_demo()

    required = {
        "ch01_action",
        "ch02_write",
        "ch02_read",
        "ch03_session",
        "ch04_final",
        "ch05_status",
        "ch06_answer",
        "ch06_provider",
        "ch06_attempts",
        "ch07_prompt",
        "ch08_results",
        "ch08_trace_steps",
        "ch09_centralized",
        "ch09_decentralized",
        "ch09_matched_by",
        "ch10_decision",
        "ch10_audit_summary",
    }
    assert required.issubset(out.keys())

    assert out["ch01_action"] in {"create_file", "read_file", "reply"}
    assert isinstance(out["ch08_results"], list)
    assert isinstance(out["ch06_attempts"], int)
    assert out["ch09_matched_by"] in {"build ui", "implement api", "write test", "default"}
    assert isinstance(out["ch10_audit_summary"], dict)
    assert out["ch10_decision"] == "blocked"
