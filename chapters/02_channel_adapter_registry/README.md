# Chapter 02: Channel Adapter Registry

## Problem
Different channels (Telegram, Discord, WebChat, CLI) have different message shapes. How do we route cleanly without hardcoding everything in one giant `if` block?

## What you will learn
- v1: direct `if/elif` routing
- v2: rule-based adapter selection
- v3: registry dispatch with sandbox path validation

## Progressive Versions

1. `v1_if_routing.py`
2. `v2_rule_selection.py`
3. `v3_registry_dispatch.py`

## ASCII Flow

```text
Inbound Envelope
   |
   v
[Selector] --> adapter_name
   |
   v
[Registry Dispatch] --> Adapter Handler --> Output
```

## OpenBot Source Anchors

- Adapter loader registry and built-ins: `openbot-main/src/channels/registry.ts`
- Registry behavior tests (built-in + custom): `openbot-main/src/channels/registry.test.ts`
- Channel manager startup uses loader output: `openbot-main/src/channels/manager.ts`

## Run

```bash
python chapters/02_channel_adapter_registry/v1_if_routing.py
python chapters/02_channel_adapter_registry/v2_rule_selection.py
python chapters/02_channel_adapter_registry/v3_registry_dispatch.py
```
