// TypeScript mirror for Chapter 06: Workspace Memory and Search (v2)
// Run with: npx ts-node v2_keyword_memory.ts

import * as fs from "fs";
import * as path from "path";

function loadMemoryLines(): string[] {
  const memoryFile = path.join(__dirname, "MEMORY.md");
  if (!fs.existsSync(memoryFile)) {
    return [];
  }
  return fs
    .readFileSync(memoryFile, "utf-8")
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0);
}

function keywordSearch(query: string, memoryLines: string[], topK: number = 2): string[] {
  const tokens = query.toLowerCase().split(/\s+/).filter((t) => t);
  const scored: [number, string][] = [];

  for (const line of memoryLines) {
    const lowered = line.toLowerCase();
    const score = tokens.reduce((sum, token) => sum + (lowered.includes(token) ? 1 : 0), 0);
    if (score > 0) {
      scored.push([score, line]);
    }
  }

  scored.sort((a, b) => b[0] - a[0]);
  return scored.slice(0, topK).map(([, line]) => line);
}

function answerWithKeywordMemory(query: string): string {
  const lines = loadMemoryLines();
  const hits = keywordSearch(query, lines);
  if (hits.length === 0) {
    return "No memory result found.";
  }
  return `Top memory: ${hits[0]}`;
}

function main(): void {
  console.log(answerWithKeywordMemory("session key policy"));
}

main();
