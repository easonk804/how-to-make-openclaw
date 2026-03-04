# Chapter 05: Retry and Recovery

## Problem
Provider/tool calls can fail for different reasons. We need retries, but not all errors deserve the same strategy.

## What you will learn
- v1: fail-stop
- v2: fixed retry attempts
- v3: adaptive retry by error category + structured logs

## Progressive Versions

1. `v1_fail_stop.py`
2. `v2_fixed_retry.py`
3. `v3_adaptive_retry.py`

## ASCII Flow

```text
Call -> Error? -> Retry Policy -> Success/Fail
```

## OpenBot Source Anchors

- Generic reconnect/backoff utility: `openbot-main/src/channels/reconnect.ts`
- Browser tool retry/error handling example: `openbot-main/src/tools/browser.ts`
- Gateway-side session run sequencing around retries: `openbot-main/src/gateway/index.ts`

## Run

```bash
python chapters/05_retry_and_recovery/v1_fail_stop.py
python chapters/05_retry_and_recovery/v2_fixed_retry.py
python chapters/05_retry_and_recovery/v3_adaptive_retry.py
```
