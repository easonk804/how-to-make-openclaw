from __future__ import annotations


def hard_truncate(messages: list[str], keep_last: int = 4) -> list[str]:
    if keep_last <= 0:
        return []
    return messages[-keep_last:]


def main() -> None:
    data = [f"m{i}" for i in range(1, 8)]
    print(hard_truncate(data, keep_last=3))


if __name__ == "__main__":
    main()
