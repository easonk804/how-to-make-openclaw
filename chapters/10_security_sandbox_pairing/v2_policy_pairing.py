from __future__ import annotations


def enforce_dm_policy(
    is_dm: bool,
    user: str,
    dm_policy: str,
    paired_users: set[str],
) -> tuple[str, str]:
    if not is_dm:
        return "allowed", "non-dm"

    if dm_policy == "allow_all":
        return "allowed", "dm-allow-all"

    if dm_policy == "paired_only" and user in paired_users:
        return "allowed", "dm-paired"

    return "blocked", "dm-policy"


def main() -> None:
    decision, reason = enforce_dm_policy(True, "alice", "paired_only", {"bob"})
    print(decision, reason)


if __name__ == "__main__":
    main()
