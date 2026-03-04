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


v1_no_session = _load_local_module("v1_no_session.py", "chapter03_v1_no_session")
v2_main_session = _load_local_module("v2_main_session.py", "chapter03_v2_main_session")
v3_scope_policy = _load_local_module("v3_scope_policy.py", "chapter03_v3_scope_policy")


handle_without_session = v1_no_session.handle_without_session
SessionStore = v2_main_session.SessionStore
handle_with_main_session = v2_main_session.handle_with_main_session
build_session_key = v3_scope_policy.build_session_key


def test_v1_ephemeral_session() -> None:
    out = handle_without_session("hello")
    assert out["session_key"] == "ephemeral"


def test_v2_main_session_history_growth() -> None:
    store = SessionStore()
    out = handle_with_main_session(store, "hello")
    assert out["session_key"].endswith(":main")
    assert out["history_size"] == 2


def test_v3_policy_switching() -> None:
    assert build_session_key("tg", "alice", True, "main") == "main"
    assert build_session_key("tg", "alice", True, "per-peer") == "peer:alice"
    assert build_session_key("tg", "alice", True, "per-channel-peer") == "tg:alice"
