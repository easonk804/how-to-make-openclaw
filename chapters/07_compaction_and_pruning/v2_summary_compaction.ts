// TypeScript mirror for Chapter 07: Compaction and Pruning (v2)
// Run with: npx ts-node v2_summary_compaction.ts

interface Compacted {
  summary: string;
  working: string[];
}

function compactWithSummary(messages: string[], keepLast: number = 3): Compacted {
  if (messages.length <= keepLast) {
    return { summary: "", working: [...messages] };
  }

  const old = messages.slice(0, -keepLast);
  const summary = `summary:${old.slice(0, 3).join("; ")}`;
  return {
    summary,
    working: messages.slice(-keepLast),
  };
}

function buildPrompt(compacted: Compacted): string {
  const summary = compacted.summary;
  const working = compacted.working;
  return `${summary}\nworking:${working.join(" | ")}`;
}

function main(): void {
  const msgs = Array.from({ length: 6 }, (_, i) => `turn${i + 1}`);
  const compacted = compactWithSummary(msgs, 2);
  console.log(buildPrompt(compacted));
}

main();
