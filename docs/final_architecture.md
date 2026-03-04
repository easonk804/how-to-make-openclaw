# Final Architecture (OpenBot Alignment)

## Goal
Use `final/openclaw_full.py` as a deterministic integration harness that demonstrates how each teaching chapter maps to concrete `openbot-main` architecture.

## Module Loading Pattern
The final demo dynamically loads chapter modules via `importlib`:

1. Resolve project root
2. Load chapter module by relative path
3. Execute chapter function(s)
4. Aggregate outputs into one structured result dict

## Chapter -> OpenBot Mapping

```text
Ch01 Gateway Event Loop        -> openbot gateway ingress/webhooks
Ch02 Adapter Registry          -> channel adapter loader registry
Ch03 Session Scope             -> session key routing + dm/group policy gate
Ch04 ReAct Tool Stream         -> agent stream + tool-call loop
Ch05 Retry Recovery            -> reconnect backoff + retry classification
Ch06 Workspace Memory Search   -> provider fallback + attempts + health
Ch07 Compaction Pruning        -> maxMessages/maxTokens pruning order
Ch08 Queue Concurrency Lanes   -> same-session serialize / cross-session parallel
Ch09 Multi-Agent Routing       -> binding match + selected agent trace
Ch10 Security Sandbox Pairing  -> pairing gate + whitelist + audit trail
```

## Integration Contracts
Each chapter keeps a small deterministic API while exposing one openbot-aligned signal:

- Ch06: provider attempts and selected provider
- Ch08: scheduler trace length
- Ch09: matched binding key
- Ch10: audit summary with latest reason

## Determinism Strategy
- No external network calls
- No required API key
- Simulated provider/tool behavior only
- Fixed sample data for retrieval/routing/security demos

## Testing Contract
`tests/test_final_integration.py` validates:

1. required chapter outputs + alignment telemetry keys exist
2. type shape is stable for list/int/dict telemetry fields
3. security enforcement still blocks dangerous command
