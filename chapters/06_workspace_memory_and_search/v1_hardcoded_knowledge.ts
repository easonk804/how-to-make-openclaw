// TypeScript mirror for Chapter 06: Workspace Memory and Search (v1)
// Run with: npx ts-node v1_hardcoded_knowledge.ts

const KNOWLEDGE: Record<string, string> = {
  session: "OpenClaw supports configurable session scoping.",
  queue: "OpenClaw uses queue lanes for controlled concurrency.",
  sandbox: "OpenClaw enforces sandbox boundaries for safe tool execution.",
};

function answerHardcoded(query: string): string {
  const lowered = query.toLowerCase();
  for (const [key, value] of Object.entries(KNOWLEDGE)) {
    if (lowered.includes(key)) {
      return value;
    }
  }
  return "No hardcoded memory hit.";
}

function main(): void {
  console.log(answerHardcoded("How does session work?"));
}

main();
