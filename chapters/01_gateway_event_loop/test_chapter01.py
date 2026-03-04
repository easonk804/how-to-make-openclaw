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


v1_sync_flow = _load_local_module("v1_sync_flow.py", "chapter01_v1_sync_flow")
v2_envelope = _load_local_module("v2_envelope.py", "chapter01_v2_envelope")
v3_event_lifecycle = _load_local_module("v3_event_lifecycle.py", "chapter01_v3_event_lifecycle")


handle_sync = v1_sync_flow.handle_sync
build_envelope = v2_envelope.build_envelope
handle_envelope = v2_envelope.handle_envelope
run_gateway_loop = v3_event_lifecycle.run_gateway_loop


def test_v1_create_action() -> None:
    out = handle_sync("please create file")
    assert out["action"] == "create_file"
    assert out["egress"].startswith("created:")


def test_v2_envelope_shape() -> None:
    env = build_envelope("discord", "u2", "hello")
    out = handle_envelope(env)
    assert env["channel"] == "discord"
    assert out["id"] == env["id"]


def test_v3_lifecycle_start_end() -> None:
    out = run_gateway_loop(["read file"])
    events = out[0]["events"]
    assert events[0]["type"] == "lifecycle_start"
    assert events[-1]["type"] == "lifecycle_end"
