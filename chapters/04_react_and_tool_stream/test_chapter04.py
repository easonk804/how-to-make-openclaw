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


v1_direct_answer = _load_local_module("v1_direct_answer.py", "chapter04_v1_direct_answer")
v2_structured_reasoning = _load_local_module("v2_structured_reasoning.py", "chapter04_v2_structured_reasoning")
v3_react_tool_stream = _load_local_module("v3_react_tool_stream.py", "chapter04_v3_react_tool_stream")


direct_answer = v1_direct_answer.direct_answer
reason_and_answer = v2_structured_reasoning.reason_and_answer
react_solve = v3_react_tool_stream.react_solve


def test_v1_direct_answer_requests() -> None:
    assert "pip install requests" in direct_answer("ModuleNotFoundError: requests")


def test_v2_structured_reasoning_steps() -> None:
    steps, final = reason_and_answer("ModuleNotFoundError: requests")
    assert len(steps) >= 3
    assert "Run:" in final


def test_v3_react_trace_shape() -> None:
    trace, final = react_solve("ModuleNotFoundError: requests")
    kinds = [item["type"] for item in trace]
    assert "thought" in kinds and "action" in kinds and "observation" in kinds
    assert final.startswith("Dependency fixed")
