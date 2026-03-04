// TypeScript mirror for Chapter 07: Compaction and Pruning (v3)
// Run with: npx ts-node v3_compaction_pruning.ts

interface Memory {
  summary: string;
  working: string[];
  tool_results: string[];
}

function createMemory(working: string[], toolResults: string[]): Memory {
  return {
    summary: "",
    working: [...working],
    tool_results: [...toolResults],
  };
}

function compactMemory(memory: Memory, workingLimit: number, maxTokens?: number): void {
  if (memory.working.length > workingLimit) {
    const overflow = memory.working.slice(0, -workingLimit);
    memory.summary = `compact:${overflow.join(" ; ")}`;
    memory.working = memory.working.slice(-workingLimit);
  }
  if (maxTokens !== undefined) {
    const tokenBudget = maxTokens;
    let used = memory.working.join(" ").length;
    while (used > tokenBudget && memory.working.length > 0) {
      const removed = memory.working.shift();
      if (removed) {
        memory.summary += ` ; ${removed}`;
        used = memory.working.join(" ").length;
      }
    }
  }
}

function pruneToolResults(memory: Memory, toolLimit: number): void {
  if (memory.tool_results.length > toolLimit) {
    memory.tool_results = memory.tool_results.slice(-toolLimit);
  }
}

function memoryPrompt(memory: Memory): string {
  const parts: string[] = [];
  if (memory.summary) {
    parts.push(`[summary]\n${memory.summary}`);
  }
  parts.push(`[working]\n${memory.working.join("\n")}`);
  if (memory.tool_results.length > 0) {
    parts.push(`[tools]\n${memory.tool_results.join("\n")}`);
  }
  return parts.join("\n");
}

function main(): void {
  const mem = createMemory(
    ["topic=final integration", "chapter=07", "need short prompt", "todo=add tests", "style=beginner"],
    ["tool:step1", "tool:step2", "tool:step3"]
  );
  compactMemory(mem, 2, 12);
  pruneToolResults(mem, 2);
  console.log(memoryPrompt(mem));
}

main();
