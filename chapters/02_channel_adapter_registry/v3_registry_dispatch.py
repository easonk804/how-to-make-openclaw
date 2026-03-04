from __future__ import annotations

from pathlib import Path


class AdapterRegistry:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self._handlers: dict[str, callable] = {}

    def register(self, name: str, handler) -> None:
        self._handlers[name] = handler

    def dispatch(self, name: str, **kwargs) -> str:
        handler = self._handlers.get(name)
        if handler is None:
            return f"unknown adapter:{name}"
        return str(handler(**kwargs))


def _safe_join(base: Path, rel_path: str) -> Path:
    base_resolved = base.resolve()
    candidate = (base_resolved / rel_path).resolve()
    if not str(candidate).startswith(str(base_resolved)):
        raise ValueError("path escape rejected")
    return candidate


def build_registry(workspace: Path) -> AdapterRegistry:
    registry = AdapterRegistry(workspace)

    def write_message(path: str, content: str) -> str:
        p = _safe_join(workspace, path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"wrote:{path}"

    def read_message(path: str) -> str:
        p = _safe_join(workspace, path)
        if not p.exists():
            return "not_found"
        return p.read_text(encoding="utf-8")

    registry.register("write_file", write_message)
    registry.register("read_file", read_message)
    return registry


def main() -> None:
    workspace = Path(__file__).resolve().parent / "sandbox"
    registry = build_registry(workspace)
    print(registry.dispatch("write_file", path="demo.txt", content="hello"))
    print(registry.dispatch("read_file", path="demo.txt"))


if __name__ == "__main__":
    main()
