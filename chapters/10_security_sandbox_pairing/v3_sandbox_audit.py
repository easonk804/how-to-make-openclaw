from __future__ import annotations

from dataclasses import dataclass
import time


@dataclass
class AuditRecord:
    timestamp: int
    command: str
    decision: str
    reason: str


_DEFAULT_WHITELIST = ["echo", "pwd", "ls", "dir", "whoami", "python", "node", "npm", "npx"]
_AUDIT_LOG: list[AuditRecord] = []
_MAX_AUDIT_LOG_SIZE = 1000


def _is_dangerous(command: str) -> bool:
    lowered = command.lower()
    blocked_patterns = ["rm -rf", "del /f", "format c:"]
    return any(pattern in lowered for pattern in blocked_patterns)


def _base_command(command: str) -> str:
    parts = command.strip().split()
    return (parts[0] if parts else "").lower()


def _append_audit(record: AuditRecord) -> None:
    _AUDIT_LOG.append(record)
    if len(_AUDIT_LOG) > _MAX_AUDIT_LOG_SIZE:
        del _AUDIT_LOG[: len(_AUDIT_LOG) - _MAX_AUDIT_LOG_SIZE]


def list_audit(limit: int = 100) -> list[AuditRecord]:
    keep = max(1, limit)
    return list(reversed(_AUDIT_LOG[-keep:]))


def clear_audit() -> None:
    _AUDIT_LOG.clear()


def enforce(command: str, whitelist: list[str] | None = None) -> tuple[str, AuditRecord]:
    allow = {item.lower() for item in (whitelist or _DEFAULT_WHITELIST)}
    if _is_dangerous(command):
        record = AuditRecord(
            timestamp=int(time.time() * 1000),
            command=command,
            decision="blocked",
            reason="sandbox_dangerous_pattern",
        )
        _append_audit(record)
        return "blocked", record

    base = _base_command(command)
    if not base:
        record = AuditRecord(
            timestamp=int(time.time() * 1000),
            command=command,
            decision="blocked",
            reason="command_required",
        )
        _append_audit(record)
        return "blocked", record

    if base not in allow:
        record = AuditRecord(
            timestamp=int(time.time() * 1000),
            command=command,
            decision="blocked",
            reason=f"whitelist_block:{base}",
        )
        _append_audit(record)
        return "blocked", record

    record = AuditRecord(
        timestamp=int(time.time() * 1000),
        command=command,
        decision="allowed",
        reason="sandbox_ok",
    )
    _append_audit(record)
    return "allowed", record


def main() -> None:
    print(enforce("rm -rf /tmp/demo"))


if __name__ == "__main__":
    main()
