from __future__ import annotations

import asyncio


async def _run_one(task_id: str, delay: float = 0.01) -> str:
    await asyncio.sleep(delay)
    return f"done:{task_id}"


def _parse_task(task: tuple[str, str] | tuple[str, str, float]) -> tuple[str, str, float]:
    if len(task) == 2:
        task_id, lane = task
        return task_id, lane, 0.01
    task_id, lane, delay = task
    return task_id, lane, delay


async def run_with_lanes(
    tasks: list[tuple[str, str] | tuple[str, str, float]],
    lane_limit: int = 1,
    global_limit: int = 2,
) -> list[str]:
    results, _ = await run_with_lanes_trace(tasks, lane_limit=lane_limit, global_limit=global_limit)
    return results


async def run_with_lanes_trace(
    tasks: list[tuple[str, str] | tuple[str, str, float]],
    lane_limit: int = 1,
    global_limit: int = 2,
) -> tuple[list[str], list[str]]:
    lane_locks: dict[str, asyncio.Semaphore] = {}
    global_lock = asyncio.Semaphore(global_limit)
    trace: list[str] = []

    async def run_task(task_id: str, lane: str, delay: float) -> str:
        trace.append(f"queued:{task_id}:{lane}")
        lane_lock = lane_locks.setdefault(lane, asyncio.Semaphore(lane_limit))
        async with global_lock:
            trace.append(f"enter-global:{task_id}:{lane}")
            async with lane_lock:
                trace.append(f"enter-lane:{task_id}:{lane}")
                out = await _run_one(task_id, delay=delay)
                trace.append(f"exit-lane:{task_id}:{lane}")
                return out

    coros = []
    for item in tasks:
        task_id, lane, delay = _parse_task(item)
        coros.append(run_task(task_id, lane, delay))
    return list(await asyncio.gather(*coros)), trace


def main() -> None:
    tasks = [("A", "s1"), ("B", "s1"), ("C", "s2")]
    print(asyncio.run(run_with_lanes(tasks, lane_limit=1, global_limit=2)))


if __name__ == "__main__":
    main()
