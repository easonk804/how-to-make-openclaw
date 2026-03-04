# Chapter-by-Chapter Event Diagrams

This document provides detailed ASCII diagrams showing event flows for each chapter's v3 implementation.

## Chapter 01: Gateway Event Loop

```
Inbound Message
       |
       v
[lifecycle_start] -----> [ingress] -----> [act/decide] -----> [egress] -----> [lifecycle_end]
    channel                    |              |                  |
    user                       text         intent            result
                               |              |                  |
                               v              v                  v
                         Parse command   Route action     Send response
```

## Chapter 02: Channel Adapter Registry

```
Inbound Envelope
       |
       v
[route_adapter] --> Adapter Name
       |
       v
[dispatch] --> Handler Selection
       |
       +---> write_file --> Sandbox Check --> Write
       |
       +---> read_file  --> Sandbox Check --> Read
       |
       +---> unknown    --> Error
```

## Chapter 03: Session and DM Scope

```
Message Context
       |
       +-- is_dm? --+--> per-peer routing --> peer:{user}
       |             |
       +-- channel? -+--> per-channel-peer --> {channel}:{user}
       |
       +-- default --+--> main session --> main
```

## Chapter 04: ReAct and Tool Stream

```
Problem Input
       |
       v
[thought] -----> [action] -----> [observation] -----> [final]
   |                 |                |                  |
   |            tool selection    execute result      synthesize
   |                 |                |
   +-----------------+                |
         ^                            |
         +----------------------------+
              (loop until resolved)
```

## Chapter 05: Retry and Recovery

```
Attempt Call
       |
       v
[execute] -----> Error?
       |           |
       |           +-- transient? ----> [retry] ----> exponential backoff
       |           |                                      |
       |           |                                      v
       |           +-- fatal? --------> [stop immediately]
       |           |
       |           +-- unknown? ------> [retry with limit]
       |
       v
  [success]
```

## Chapter 06: Workspace Memory and Search

```
Query Input
       |
       v
[embed query] -----> [search index] -----> [rank results]
                          |                     |
                    tf-idf/cosine           top-k select
                          |                     |
                          v                     v
                    candidate docs      [retrieve best]
                                              |
                                              v
                                        [compose answer]
```

## Chapter 07: Compaction and Pruning

```
Memory Buffer (working + tools)
       |
       v
[compact_memory] -----> working > limit?
       |                      |
       |                      +-- overflow --> [summarize] --> archive
       |                                          |
       v                                          v
[prune_tools] -----> tool count > limit? ----> [keep recent]
       |
       v
[build_prompt] = [summary] + [working] + [tools]
```

## Chapter 08: Queue and Concurrency Lanes

```
Task Arrival
       |
       v
[enqueue] -----> Queue State (pending: N, done: M)
       |
       v
[lane_scheduler] -----> Lane Limit Check?
       |                      |
       |                      +-- lane full? ----> [wait]
       |                      |
       |                      +-- global full? --> [wait]
       |                      |
       |                      +-- available? ----> [execute]
       |                                              |
       v                                              v
[progress tracker] <---------------------------- [result]
```

## Chapter 09: Multi-Agent Routing

```
Intent Detection
       |
       +-- frontend? ---> [frontend_agent]
       |
       +-- backend? ----> [backend_agent]
       |
       +-- default? ----> [generalist_agent]
                              |
                              v
                       [isolation check]
                       workspace/session/auth
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
         [allow]         [block]       [handoff]
              |               |               |
              v               v               v
         execute          reject      forward to peer
```

## Chapter 10: Security Sandbox Pairing

```
Command Input
       |
       v
[dm_policy_check] -----> DM channel?
       |                      |
       |                      +-- allow_all? ----> [pass]
       |                      |
       |                      +-- paired_only? --> [check pairing]
       |                                              |
       |                                              +-- paired? --> [pass]
       |                                              |
       |                                              +-- not? -----> [block]
       v
[sandbox_check] -----> dangerous pattern?
       |                      |
       |                      +-- pattern match? --> [block + audit]
       |                      |
       |                      +-- safe? ----------> [allow + audit]
       v
[audit_record] = {command, decision, reason, timestamp}
```

## Full Pipeline Integration

```
Chapter Flow in final/openclaw_full.py

01 Gateway Loop      --> 02 Adapter Dispatch
       |                        |
       v                        v
03 Session Scope     --> 04 ReAct Reasoning
       |                        |
       v                        v
05 Retry Policy      --> 06 Memory Retrieval
       |                        |
       v                        v
07 Compaction        --> 08 Concurrent Execution
       |                        |
       v                        v
09 Multi-Agent Route --> 10 Security Enforcement
                              |
                              v
                    [aggregated result dict]
```
