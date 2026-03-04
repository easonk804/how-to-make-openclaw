# Chapter 03: Session and DM Scope

## Problem
A bot must remember context, but session boundaries should change by scenario (shared main session vs per-user DM session).

## What you will learn
- v1: no session memory
- v2: shared main session
- v3: policy-driven session key strategy (`main`, `per-peer`, `per-channel-peer`)

## Progressive Versions

1. `v1_no_session.py`
2. `v2_main_session.py`
3. `v3_scope_policy.py`

## ASCII Flow

```text
Message -> Session Key Strategy -> Session Store -> Prompt Context
```

## OpenBot Source Anchors

- Session key routing + agent binding priority: `openbot-main/src/session/router.ts`
- Router behavior tests (`teamId`/`guildId`/default): `openbot-main/src/session/router.test.ts`
- DM/group policy enforcement and route application: `openbot-main/src/channels/manager.ts`

## Run

```bash
python chapters/03_session_and_dm_scope/v1_no_session.py
python chapters/03_session_and_dm_scope/v2_main_session.py
python chapters/03_session_and_dm_scope/v3_scope_policy.py
```
