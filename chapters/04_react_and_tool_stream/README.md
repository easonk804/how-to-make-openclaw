# Chapter 04: ReAct and Tool Stream

## Problem
Direct answers are brittle for complex tasks. We need a visible reasoning loop and tool interaction trace.

## What you will learn
- v1: direct answer mode
- v2: structured step reasoning
- v3: ReAct trace (`Thought -> Action -> Observation -> Final`) with tool stream events

## Progressive Versions

1. `v1_direct_answer.py`
2. `v2_structured_reasoning.py`
3. `v3_react_tool_stream.py`

## ASCII Flow

```text
Question
  |
  v
Thought -> Action(tool) -> Observation -> Final Answer
```

## OpenBot Source Anchors

- Agent stream + tool-call loop: `openbot-main/src/agent/client.ts`
- Tool policy/shape contract: `openbot-main/src/tools/index.ts`
- Search tool as concrete tool-loop target: `openbot-main/src/tools/search.ts`

## Run

```bash
python chapters/04_react_and_tool_stream/v1_direct_answer.py
python chapters/04_react_and_tool_stream/v2_structured_reasoning.py
python chapters/04_react_and_tool_stream/v3_react_tool_stream.py
```
