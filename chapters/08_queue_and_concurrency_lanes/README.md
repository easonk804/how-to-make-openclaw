# Chapter 08: Queue and Concurrency Lanes

## Problem
If all requests run in one blocking flow, one slow task can delay every user.

## What you will learn
- v1: blocking serial execution
- v2: background queue with progress
- v3: lane-based concurrency limits (session lane + global lane)

## Progressive Versions

1. `v1_blocking_serial.py`
2. `v2_background_queue.py`
3. `v3_lane_concurrency.py`

## ASCII Flow

```text
Inbound Tasks
   |
   v
[Queue] -> [Lane Scheduler] -> [Runner] -> [Results]
```

## OpenBot Source Anchors

- Per-session serialization primitive: `openbot-main/src/session/run-queue.ts`
- Queue concurrency regression tests: `openbot-main/src/session/run-queue.test.ts`
- Gateway scheduling usage for same/different session keys: `openbot-main/src/gateway/index.ts`

## Run

```bash
python chapters/08_queue_and_concurrency_lanes/v1_blocking_serial.py
python chapters/08_queue_and_concurrency_lanes/v2_background_queue.py
python chapters/08_queue_and_concurrency_lanes/v3_lane_concurrency.py
```
