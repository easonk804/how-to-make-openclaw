# Chapter 10: Security Sandbox Pairing

## Problem
Agent power without boundaries is dangerous. We need DM policy checks, pairing rules, sandbox restrictions, and audit logs.

## What you will learn
- v1: no protection (anti-pattern)
- v2: dmPolicy + allowlist/pairing gate
- v3: sandbox allow/deny + audit record

## Progressive Versions

1. `v1_no_protection.py`
2. `v2_policy_pairing.py`
3. `v3_sandbox_audit.py`

## ASCII Flow

```text
Command -> Policy Check -> Sandbox Check -> Allow/Block + Audit
```

## OpenBot Source Anchors

- Pairing store + approve/check flow: `openbot-main/src/security/pairing.ts`
- DM/group policy gate wiring in channel manager: `openbot-main/src/channels/manager.ts`
- Run tool whitelist + audit model: `openbot-main/src/tools/run.ts`
- Run tool audit tests: `openbot-main/src/tools/run.test.ts`

## Run

```bash
python chapters/10_security_sandbox_pairing/v1_no_protection.py
python chapters/10_security_sandbox_pairing/v2_policy_pairing.py
python chapters/10_security_sandbox_pairing/v3_sandbox_audit.py
```
