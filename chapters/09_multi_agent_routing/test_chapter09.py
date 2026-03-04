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


v1_single_agent = _load_local_module("v1_single_agent.py", "chapter09_v1_single_agent")
v2_central_router = _load_local_module("v2_central_router.py", "chapter09_v2_central_router")
v3_isolated_routing = _load_local_module("v3_isolated_routing.py", "chapter09_v3_isolated_routing")


run_single_agent = v1_single_agent.run_single_agent
run_centralized = v2_central_router.run_centralized
route_task_with_match = v2_central_router.route_task_with_match
route_with_isolation = v3_isolated_routing.route_with_isolation
decentralized_run = v3_isolated_routing.decentralized_run


def test_v1_single_agent() -> None:
    out = run_single_agent("build ui")
    assert out["agent"] == "generalist"


def test_v2_central_router() -> None:
    logs = run_centralized(["build ui", "implement api"])
    assert any("frontend_agent" in item for item in logs)
    assert any("backend_agent" in item for item in logs)


def test_v2_route_task_with_match() -> None:
    out = route_task_with_match("build ui")
    assert out["agent"] == "frontend_agent"
    assert out["matched_by"] == "build ui"


def test_v3_isolation_blocks_unauthorized() -> None:
    out = route_with_isolation("ws1", "alice", "denied", "frontend")
    assert out["status"] == "blocked"


def test_v3_decentralized_run_shape() -> None:
    logs = decentralized_run()
    assert any(item.startswith("handoff:") for item in logs)
