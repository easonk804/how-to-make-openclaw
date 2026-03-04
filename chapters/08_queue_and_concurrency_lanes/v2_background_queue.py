from __future__ import annotations


class BackgroundQueue:
    def __init__(self) -> None:
        self.pending: list[str] = []
        self.done: list[str] = []

    def enqueue(self, task_name: str) -> None:
        self.pending.append(task_name)

    def process_next(self) -> str | None:
        if not self.pending:
            return None
        task = self.pending.pop(0)
        self.done.append(task)
        return task

    def progress(self) -> dict[str, int]:
        return {
            "pending": len(self.pending),
            "done": len(self.done),
        }


def main() -> None:
    q = BackgroundQueue()
    q.enqueue("task-1")
    q.enqueue("task-2")
    q.process_next()
    print(q.progress())


if __name__ == "__main__":
    main()
