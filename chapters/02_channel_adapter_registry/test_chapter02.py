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


v1_if_routing = _load_local_module("v1_if_routing.py", "chapter02_v1_if_routing")
v2_rule_selection = _load_local_module("v2_rule_selection.py", "chapter02_v2_rule_selection")
v3_registry_dispatch = _load_local_module("v3_registry_dispatch.py", "chapter02_v3_registry_dispatch")


route_adapter = v1_if_routing.route_adapter
choose_adapter = v2_rule_selection.choose_adapter
build_registry = v3_registry_dispatch.build_registry
_safe_join = v3_registry_dispatch._safe_join


def test_v1_routing() -> None:
    assert route_adapter("telegram") == "telegram_adapter"
    assert route_adapter("unknown") == "default_adapter"


def test_v2_rule_selection() -> None:
    env = {"channel": "discord", "text": "hi"}
    assert choose_adapter(env) == "discord_adapter"


def test_v3_registry_dispatch(tmp_path: Path) -> None:
    reg = build_registry(tmp_path)
    assert reg.dispatch("write_file", path="a.txt", content="x").startswith("wrote:")
    assert reg.dispatch("read_file", path="a.txt") == "x"


def test_v3_safe_join_blocks_escape(tmp_path: Path) -> None:
    try:
        _safe_join(tmp_path, "../evil.txt")
        assert False, "should reject path escape"
    except ValueError:
        assert True
