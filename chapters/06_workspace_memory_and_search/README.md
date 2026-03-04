# Chapter 06: Workspace Memory and Search

## Problem
An agent should answer using project memory, not only built-in prompts.

## What you will learn
- v1: hardcoded knowledge
- v2: keyword retrieval over memory text
- v3: vector retrieval + provider fallback attempts + provider health

## Progressive Versions

1. `v1_hardcoded_knowledge.py`
2. `v2_keyword_memory.py`
3. `v3_vector_retrieval.py`

## ASCII Flow

```text
Query -> Retrieve Memory -> Compose Answer
```

## OpenBot Source Anchors

- Search provider fallback + attempts + health: `openbot-main/src/tools/search.ts`
- Search fallback/normalization tests: `openbot-main/src/tools/search.test.ts`
- Search tool config model: `openbot-main/src/config/types.ts`

## Run

```bash
python chapters/06_workspace_memory_and_search/v1_hardcoded_knowledge.py
python chapters/06_workspace_memory_and_search/v2_keyword_memory.py
python chapters/06_workspace_memory_and_search/v3_vector_retrieval.py
```
