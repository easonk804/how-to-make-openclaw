# Chapter 07: Compaction and Pruning

## Problem
Context grows quickly. We must keep useful information while staying within context budget.

## What you will learn
- v1: hard truncation
- v2: naive summary compaction
- v3: dual mechanism (working memory compaction + tool result pruning)

## Progressive Versions

1. `v1_hard_truncate.py`
2. `v2_summary_compaction.py`
3. `v3_compaction_pruning.py`

## ASCII Flow

```text
Long History -> Compact Old Context -> Prune Low-value Tool Results -> Short Prompt
```

## OpenBot Source Anchors

- Session message pruning (maxMessages + maxTokens): `openbot-main/src/session/store.ts`
- Session store pruning regression tests: `openbot-main/src/session/store.test.ts`
- Gateway applies pruning limits when appending/retrieving messages: `openbot-main/src/gateway/index.ts`

## Run

```bash
python chapters/07_compaction_and_pruning/v1_hard_truncate.py
python chapters/07_compaction_and_pruning/v2_summary_compaction.py
python chapters/07_compaction_and_pruning/v3_compaction_pruning.py
```
