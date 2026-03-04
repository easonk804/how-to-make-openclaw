// TypeScript mirror for Chapter 02: Channel Adapter Registry (v3)
// Run with: npx ts-node v3_registry_dispatch.ts

import * as fs from "fs";
import * as path from "path";

class AdapterRegistry {
  private workspace: string;
  private handlers: Map<string, (...args: any[]) => string>;

  constructor(workspace: string) {
    this.workspace = path.resolve(workspace);
    if (!fs.existsSync(this.workspace)) {
      fs.mkdirSync(this.workspace, { recursive: true });
    }
    this.handlers = new Map();
  }

  register(name: string, handler: (...args: any[]) => string): void {
    this.handlers.set(name, handler);
  }

  dispatch(name: string, ...args: any[]): string {
    const handler = this.handlers.get(name);
    if (!handler) return `unknown adapter:${name}`;
    return handler(...args);
  }
}

function safeJoin(base: string, relPath: string): string {
  const baseResolved = path.resolve(base);
  const candidate = path.resolve(baseResolved, relPath);
  if (!candidate.startsWith(baseResolved)) {
    throw new Error("path escape rejected");
  }
  return candidate;
}

function buildRegistry(workspace: string): AdapterRegistry {
  const registry = new AdapterRegistry(workspace);

  registry.register("write_file", (filePath: string, content: string): string => {
    const p = safeJoin(workspace, filePath);
    const dir = path.dirname(p);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(p, content, "utf-8");
    return `wrote:${filePath}`;
  });

  registry.register("read_file", (filePath: string): string => {
    const p = safeJoin(workspace, filePath);
    if (!fs.existsSync(p)) return "not_found";
    return fs.readFileSync(p, "utf-8");
  });

  return registry;
}

function main(): void {
  const workspace = path.join(__dirname, "sandbox");
  const registry = buildRegistry(workspace);
  console.log(registry.dispatch("write_file", "demo.txt", "hello"));
  console.log(registry.dispatch("read_file", "demo.txt"));
}

main();
