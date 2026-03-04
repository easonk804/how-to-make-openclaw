# Chapter 09: Multi-Agent Routing

## Problem
One agent cannot do everything efficiently. We need routing across specialized agents while preserving isolation boundaries.

## What you will learn
- v1: single-agent handling
- v2: centralized coordinator with bindings
- v3: isolated multi-agent routing (`workspace/session/auth`) + agent-to-agent handoff

## Progressive Versions

1. `v1_single_agent.py`
2. `v2_central_router.py`
3. `v3_isolated_routing.py`

## ASCII Flow

```text
Message -> Router -> Target Agent -> Result
                 \-> Handoff -> Peer Agent -> Result
```

## OpenBot Source Anchors

- Agent routing + session key output: `openbot-main/src/session/router.ts`
- Routing test coverage across binding dimensions: `openbot-main/src/session/router.test.ts`
- Gateway/channel manager apply resolved route before agent run: `openbot-main/src/channels/manager.ts`

## Run

```bash
python chapters/09_multi_agent_routing/v1_single_agent.py
python chapters/09_multi_agent_routing/v2_central_router.py
python chapters/09_multi_agent_routing/v3_isolated_routing.py
```
