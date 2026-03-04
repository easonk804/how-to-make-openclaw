// TypeScript mirror for Chapter 06: Workspace Memory and Search (v3)
// Run with: npx ts-node v3_vector_retrieval.ts

interface Doc {
  id: string;
  text: string;
}

type Vector = Record<string, number>;
type Index = [Doc, Vector][];

function tokenize(text: string): string[] {
  return text
    .split(/\s+/)
    .map((t) => t.trim().toLowerCase().replace(/[.,:;!?()\[\]{}"']/g, ""))
    .filter((t) => t.length > 0);
}

function embed(text: string): Vector {
  const tokens = tokenize(text);
  const counts: Record<string, number> = {};
  for (const t of tokens) {
    counts[t] = (counts[t] || 0) + 1;
  }
  return counts;
}

function cosine(a: Vector, b: Vector): number {
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  let dot = 0;
  let normA = 0;
  let normB = 0;
  for (const k of keys) {
    const av = a[k] || 0;
    const bv = b[k] || 0;
    dot += av * bv;
    normA += av * av;
    normB += bv * bv;
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

function loadSampleDocs(): Doc[] {
  return [
    { id: "d1", text: "Session policy controls whether context is shared or isolated." },
    { id: "d2", text: "Queue lanes limit concurrency and protect provider stability." },
    { id: "d3", text: "Sandbox and pairing improve security in DM workflows." },
  ];
}

function buildIndex(docs: Doc[]): Index {
  return docs.map((d) => [d, embed(d.text)]);
}

function retrieveTopK(query: string, index: Index, topK: number = 2): Doc[] {
  const q = embed(query);
  const scored: [number, Doc][] = [];
  for (const [doc, vec] of index) {
    scored.push([cosine(q, vec), doc]);
  }
  scored.sort((a, b) => b[0] - a[0]);
  return scored.slice(0, topK).map(([, d]) => d);
}

function answerWithRetrieval(query: string, index: Index): string {
  const hits = retrieveTopK(query, index, 1);
  if (hits.length === 0) return "No retrieval hit.";
  return `Retrieved: ${hits[0].text}`;
}

function main(): void {
  const docs = loadSampleDocs();
  const index = buildIndex(docs);
  console.log(answerWithRetrieval("How does session isolation work?", index));
}

main();
