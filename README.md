# How to Make OpenClaw (Teaching Edition)

A beginner-friendly, chapter-based project to learn core OpenClaw ideas by building them step by step.

Core method:
- One mechanism per chapter.
- Three progressive versions per chapter: **v1 -> v2 -> v3**.
- Fixed deliverables: README + code + exercises + tests.
- All chapters run offline by default.

## Learning Path (10 Chapters)

1. `01_gateway_event_loop` - Gateway ingress/act/egress lifecycle
2. `02_channel_adapter_registry` - Channel adapter routing and registry dispatch
3. `03_session_and_dm_scope` - Session key strategy and DM scope
4. `04_react_and_tool_stream` - ReAct loop and tool event stream
5. `05_retry_and_recovery` - Retry policy and adaptive recovery
6. `06_workspace_memory_and_search` - Workspace memory and retrieval
7. `07_compaction_and_pruning` - Context compaction and pruning
8. `08_queue_and_concurrency_lanes` - Queue lanes and concurrency control
9. `09_multi_agent_routing` - Multi-agent routing and isolation
10. `10_security_sandbox_pairing` - Security boundary, pairing, and audit

## Quick Start

### Requirements
- Python 3.10+
- pip

### Install

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

### Run tests

```bash
pytest -q
```

### Run one chapter

```bash
python chapters/01_gateway_event_loop/v1_sync_flow.py
python chapters/01_gateway_event_loop/v2_envelope.py
python chapters/01_gateway_event_loop/v3_event_lifecycle.py
```

### Run final integrated demo

```bash
python final/openclaw_full.py
```

## Suggested Study Order

1. Complete chapter README and run v1.
2. Compare v1 vs v2 changes.
3. Run v3 and inspect architecture-style design.
4. Finish exercises.
5. Run corresponding tests.

## FAQ

### Why no API key by default?
This project is designed for deterministic, offline learning. Optional real gateway integrations can be added later.

### Why three versions per chapter?
To make architecture trade-offs visible in small, controlled steps.

## Project Structure

```text
how-to-make-openclaw-main/
├── chapters/
├── final/
├── docs/
├── tests/
├── README.md
├── 开发文档.md
├── requirements.txt
├── pyproject.toml
└── .env.example
```

## License

MIT
