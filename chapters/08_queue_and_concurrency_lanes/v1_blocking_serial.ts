// TypeScript mirror for Chapter 08: Queue and Concurrency Lanes (v1)
// Run with: npx ts-node v1_blocking_serial.ts

function runBlocking(tasks: [string, number][]): string[] {
  const results: string[] = [];
  for (const [name, durationMs] of tasks) {
    results.push(`run:${name}:${durationMs}ms`);
  }
  return results;
}

function main(): void {
  console.log(runBlocking([["A", 10], ["B", 20]]));
}

main();
