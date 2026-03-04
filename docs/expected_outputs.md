# Expected Outputs

This document gives representative output shapes for each chapter's runnable versions.

## Chapter 01 Gateway Event Loop
- v1 returns keys: `ingress`, `action`, `target`, `egress`
- v2 returns keys: `id`, `intent`, `result`
- v3 returns list of messages with lifecycle events including `lifecycle_start` and `lifecycle_end`

## Chapter 02 Channel Adapter Registry
- v1 output example: `telegram_adapter:handled:hello`
- v2 output example: `discord_adapter:handled:ping`
- v3 output examples:
  - `wrote:demo.txt`
  - file content string from `read_file`

## Chapter 03 Session and DM Scope
- v1 output example: `{"session_key": "ephemeral", "reply": "stateless:..."}`
- v2 output keys: `session_key`, `history_size`
- v3 output keys: `policy`, `session_key`

## Chapter 04 ReAct and Tool Stream
- v1 output: direct advice string
- v2 output: tuple `(steps, final_answer)`
- v3 output: tuple `(trace, final)` where `trace` includes `thought/action/observation/final`

## Chapter 05 Retry and Recovery
- v1 output: tuple `(status, logs)`
- v2 output: tuple `(status, logs)` with attempt sequence
- v3 output: tuple `(status, structured_logs)` with `event/value` entries
  - includes `category`, `retry_delay_ms`, and `decision` (`retry|stop|success|exhausted`)

## Chapter 06 Workspace Memory and Search
- v1 output: matched hardcoded memory string
- v2 output: `Top memory: ...` or `No memory result found.`
- v3 output: `Retrieved: ...`
  - `search_with_fallback(...)` returns `{ok, provider_used, attempts, hits}`
  - provider health counters are tracked in `provider_health`

## Chapter 07 Compaction and Pruning
- v1 output: truncated list
- v2 output keys: `summary`, `working`
- v3 prompt sections: `[summary]`, `[working]`, `[tools]`
  - working-memory prune order: `max_messages` first, then `max_tokens`

## Chapter 08 Queue and Concurrency Lanes
- v1 output: serial run list (`run:A:...`)
- v2 progress output keys: `pending`, `done`
- v3 output: async results list, each starts with `done:`
  - `run_with_lanes_trace(...)` returns `(results, trace)` for lane/global scheduling inspection

## Chapter 09 Multi-Agent Routing
- v1 output keys: `agent`, `task`, `result`
- v2 output: route log list (`routed:task->agent`)
- v2 helper `route_task_with_match(...)` returns `{agent, matched_by}`
- v3 output: isolation route result and handoff logs

## Chapter 10 Security Sandbox Pairing
- v1 output decision: `allowed` (anti-pattern demo)
- v2 output tuple: `(decision, reason)`
- v3 output tuple: `(decision, AuditRecord)` where dangerous command returns `blocked`
  - audit helpers: `list_audit(limit)` and `clear_audit()`
  - whitelist block reason shape: `whitelist_block:<base_command>`

## Final Integration
`final/openclaw_full.py` returns a dict with keys:
- `ch01_action`
- `ch02_write`
- `ch02_read`
- `ch03_session`
- `ch04_final`
- `ch05_status`
- `ch06_answer`
- `ch06_provider`
- `ch06_attempts`
- `ch07_prompt`
- `ch08_results`
- `ch08_trace_steps`
- `ch09_centralized`
- `ch09_decentralized`
- `ch09_matched_by`
- `ch10_decision`
- `ch10_audit_summary`
