// TypeScript mirror for Chapter 08: Queue and Concurrency Lanes (v3)
// Run with: npx ts-node v3_lane_concurrency.ts

// Note: This uses async/await patterns compatible with Node.js

type Task2 = [string, string];
type Task3 = [string, string, number];
type Task = Task2 | Task3;

interface Semaphore {
  permits: number;
  queue: (() => void)[];
}

function createSemaphore(permits: number): Semaphore {
  return { permits, queue: [] };
}

async function acquire(sem: Semaphore): Promise<void> {
  if (sem.permits > 0) {
    sem.permits--;
    return;
  }
  return new Promise((resolve) => {
    sem.queue.push(resolve);
  });
}

function release(sem: Semaphore): void {
  if (sem.queue.length > 0) {
    const next = sem.queue.shift()!;
    next();
  } else {
    sem.permits++;
  }
}

async function runOne(taskId: string, delay: number): Promise<string> {
  await new Promise((r) => setTimeout(r, delay * 1000));
  return `done:${taskId}`;
}

function parseTask(task: Task): [string, string, number] {
  if (task.length === 2) {
    const [taskId, lane] = task;
    return [taskId, lane, 0.01];
  }
  return task;
}

async function runWithLanesTrace(
  tasks: Task[],
  laneLimit: number = 1,
  globalLimit: number = 2
): Promise<[string[], string[]]> {
  const laneLocks: Map<string, Semaphore> = new Map();
  const globalLock = createSemaphore(globalLimit);
  const trace: string[] = [];

  async function runTask(taskId: string, lane: string, delay: number): Promise<string> {
    trace.push(`queued:${taskId}:${lane}`);
    if (!laneLocks.has(lane)) {
      laneLocks.set(lane, createSemaphore(laneLimit));
    }
    const laneLock = laneLocks.get(lane)!;

    await acquire(globalLock);
    trace.push(`enter-global:${taskId}:${lane}`);

    await acquire(laneLock);
    trace.push(`enter-lane:${taskId}:${lane}`);

    const out = await runOne(taskId, delay);

    trace.push(`exit-lane:${taskId}:${lane}`);
    release(laneLock);
    release(globalLock);

    return out;
  }

  const coros = tasks.map((t) => {
    const [taskId, lane, delay] = parseTask(t);
    return runTask(taskId, lane, delay);
  });

  const results = await Promise.all(coros);
  return [results, trace];
}

async function main(): Promise<void> {
  const tasks: Task[] = [["A", "s1"], ["B", "s1"], ["C", "s2"]];
  const [results, trace] = await runWithLanesTrace(tasks, 1, 2);
  console.log(results);
  console.log(trace);
}

main();
