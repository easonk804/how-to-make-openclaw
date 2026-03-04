# Practical Deployment Guide

This guide provides a reproducible path to run and validate the teaching project in real environments, with **offline-first mode as the default** and optional OpenBot alignment steps.

## 1. Deployment Modes

| Mode | Target User | Network Needed | API Key Needed | Recommended |
|---|---|---|---|---|
| A. Offline Teaching | Learners and instructors | No | No | Yes (default) |
| B. Teaching + OpenBot Source Alignment | Learners comparing architecture | No (for this repo) | No | Yes |
| C. Optional Real Gateway Integration (Appendix) | Advanced users | Yes | Possibly | Optional |

---

## 2. Environment Preparation (Windows-first)

## 2.1 Prerequisites
- Python 3.10+
- pip
- Git

Check versions:

```powershell
python --version
pip --version
git --version
```

## 2.2 Clone and enter project

```powershell
git clone <your-repo-url>
cd how-to-make-openclaw-main
```

## 2.3 Create virtual environment and install dependencies

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3. Minimal Deploy-and-Run Flow (Mode A)

Execute in this order.

## 3.1 Structural smoke check

```powershell
python -m pytest tests/test_chapter_scaffolds.py -q
```

Expected: pass, confirming all chapters include README/exercises/v1/v2/v3/test.

## 3.2 Full test validation

```powershell
python -m pytest -q
```

Expected: all tests pass.

## 3.3 Run final integrated demo

```powershell
python final/openclaw_full.py
```

Expected output should include (at minimum):
- `ch06_provider`
- `ch06_attempts`
- `ch08_trace_steps`
- `ch09_matched_by`
- `ch10_audit_summary`

## 3.4 Optional: run every chapter script

```powershell
python -c "import glob,runpy; [runpy.run_path(f, run_name='__main__') for f in sorted(glob.glob('chapters/*/v*.py'))]"
```

---

## 4. Teaching + OpenBot Alignment Flow (Mode B)

This mode keeps execution offline but helps learners map concepts to `openbot-main`.

1. Read chapter guide in `chapters/*/README.md`
2. Check diagram flow in `docs/chapter_diagrams.md`
3. Compare contracts in `docs/expected_outputs.md`
4. Inspect architecture mapping in `docs/final_architecture.md`
5. Run chapter test and identify matching behavior

Suggested loop per chapter:

```text
README -> v1/v2/v3 code -> chapter test -> chapter_diagrams -> openbot anchor files
```

---

## 5. Validation Checklist (Release-Ready Teaching Build)

Before sharing this project with students or publishing updates, verify:

- [ ] `python -m pytest -q` passes
- [ ] `python final/openclaw_full.py` runs and prints all chapter outputs
- [ ] `docs/expected_outputs.md` matches actual output keys/shapes
- [ ] `docs/chapter_diagrams.md` matches current v3 behavior
- [ ] `README.md` doc links are valid
- [ ] No secrets in tracked files (`.env`, API keys, tokens)

---

## 6. Troubleshooting

## 6.1 `ModuleNotFoundError`
- Ensure virtual env is activated:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

## 6.2 `python` points to wrong interpreter
Use explicit executable:

```powershell
.venv\Scripts\python -m pytest -q
```

## 6.3 Test path errors on Windows
- Run commands from project root (where `README.md` exists).
- Avoid running tests from subdirectories.

## 6.4 Encoding/display issues in terminal
Use UTF-8 code page:

```powershell
chcp 65001
```

---

## 7. Security and GitHub Push Checklist

Before pushing publicly:

- [ ] `.env` is not committed
- [ ] sample values only in `.env.example`
- [ ] no personal tokens in commit history
- [ ] generated runtime folders are ignored (`__pycache__`, `.pytest_cache`, `.venv`)

If `.gitignore` is missing, add at least:

```gitignore
__pycache__/
*.pyc
.pytest_cache/
.venv/
.env
```

---

## 8. Appendix: Optional Real Gateway Integration (Mode C)

This project is intentionally offline by default. If you need a real gateway demonstration:

1. Keep this repo as the teaching baseline.
2. Use `openbot-main` as the runtime integration target.
3. Compare specific chapter anchors (listed in each chapter README).
4. If external search/providers are enabled in `openbot-main`, configure API keys via env vars only.

Security note:
- Never hardcode API keys in source files.
- Prefer environment-variable loading and local secret files excluded by git.
