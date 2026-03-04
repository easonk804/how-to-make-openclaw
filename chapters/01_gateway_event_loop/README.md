# Chapter 01: Gateway Event Loop

## Problem
How does an inbound message move through a gateway from receive to reply?

## What you will learn
- v1: single-message synchronous handling
- v2: message envelope for structured transport
- v3: lifecycle events (`start -> ingress -> act -> egress -> end`)

## Progressive Versions

1. `v1_sync_flow.py`  
   Minimal flow for one message.
2. `v2_envelope.py`  
   Introduces envelope metadata (`channel/user/id/payload`).
3. `v3_event_lifecycle.py`  
   Adds full lifecycle events and looped processing.

## ASCII Flow

```text
Inbound Message
   |
   v
[Ingress] -> [Action Decision] -> [Egress Reply]
   |
   v
Lifecycle Start/End Events
```

## OpenBot Source Anchors

- Gateway startup + run orchestration: `openbot-main/src/gateway/index.ts`
- Webhook ingress normalization and dispatch: `openbot-main/src/gateway/webhooks.ts`
- Webhook token policy regression tests: `openbot-main/src/gateway/webhooks-agent.test.ts`

## Run

```bash
python chapters/01_gateway_event_loop/v1_sync_flow.py
python chapters/01_gateway_event_loop/v2_envelope.py
python chapters/01_gateway_event_loop/v3_event_lifecycle.py
```
