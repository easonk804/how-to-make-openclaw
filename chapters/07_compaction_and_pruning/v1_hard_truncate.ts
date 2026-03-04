// TypeScript mirror for Chapter 07: Compaction and Pruning (v1)
// Run with: npx ts-node v1_hard_truncate.ts

function hardTruncate(messages: string[], keepLast: number = 4): string[] {
  if (keepLast <= 0) {
    return [];
  }
  return messages.slice(-keepLast);
}

function main(): void {
  const data = Array.from({ length: 7 }, (_, i) => `m${i + 1}`);
  console.log(hardTruncate(data, 3));
}

main();
