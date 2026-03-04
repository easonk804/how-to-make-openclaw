// TypeScript mirror for Chapter 08: Queue and Concurrency Lanes (v2)
// Run with: npx ts-node v2_background_queue.ts

class BackgroundQueue {
  pending: string[] = [];
  done: string[] = [];

  enqueue(taskName: string): void {
    this.pending.push(taskName);
  }

  processNext(): string | null {
    if (this.pending.length === 0) {
      return null;
    }
    const task = this.pending.shift()!;
    this.done.push(task);
    return task;
  }

  progress(): { pending: number; done: number } {
    return {
      pending: this.pending.length,
      done: this.done.length,
    };
  }
}

function main(): void {
  const q = new BackgroundQueue();
  q.enqueue("task-1");
  q.enqueue("task-2");
  q.processNext();
  console.log(q.progress());
}

main();
