from pathlib import Path
import asyncio
import importlib.util


def _load_local_module(module_filename: str, alias: str):
    path = Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {module_filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v1_blocking_serial = _load_local_module("v1_blocking_serial.py", "chapter08_v1_blocking_serial")
v2_background_queue = _load_local_module("v2_background_queue.py", "chapter08_v2_background_queue")
v3_lane_concurrency = _load_local_module("v3_lane_concurrency.py", "chapter08_v3_lane_concurrency")


run_blocking = v1_blocking_serial.run_blocking
BackgroundQueue = v2_background_queue.BackgroundQueue
run_with_lanes = v3_lane_concurrency.run_with_lanes
run_with_lanes_trace = v3_lane_concurrency.run_with_lanes_trace


def test_v1_blocking_serial() -> None:
    out = run_blocking([("A", 1), ("B", 2)])
    assert out == ["run:A:1ms", "run:B:2ms"]


def test_v2_background_queue_progress() -> None:
    q = BackgroundQueue()
    q.enqueue("t1")
    q.enqueue("t2")
    assert q.process_next() == "t1"
    progress = q.progress()
    assert progress["pending"] == 1
    assert progress["done"] == 1


def test_v3_lane_concurrency_shape() -> None:
    tasks = [("A", "lane1"), ("B", "lane1"), ("C", "lane2")]
    out = asyncio.run(run_with_lanes(tasks, lane_limit=1, global_limit=2))
    assert len(out) == 3
    assert all(item.startswith("done:") for item in out)


def test_v3_same_lane_is_serialized() -> None:
    _, trace = asyncio.run(
        run_with_lanes_trace(
            [("A", "lane1", 0.03), ("B", "lane1", 0.0), ("C", "lane2", 0.01)],
            lane_limit=1,
            global_limit=2,
        )
    )
    idx_exit_a = trace.index("exit-lane:A:lane1")
    idx_enter_b = trace.index("enter-lane:B:lane1")
    assert idx_exit_a < idx_enter_b


def test_v3_different_lanes_can_overlap() -> None:
    _, trace = asyncio.run(
        run_with_lanes_trace(
            [("A", "lane1", 0.03), ("C", "lane2", 0.03)],
            lane_limit=1,
            global_limit=2,
        )
    )
    idx_enter_a = trace.index("enter-lane:A:lane1")
    idx_enter_c = trace.index("enter-lane:C:lane2")
    idx_first_exit = min(trace.index("exit-lane:A:lane1"), trace.index("exit-lane:C:lane2"))
    assert idx_enter_a < idx_first_exit
    assert idx_enter_c < idx_first_exit
