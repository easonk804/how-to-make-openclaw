// TypeScript mirror for Chapter 09: Multi-Agent Routing (v2)
// Run with: npx ts-node v2_central_router.ts

const BINDINGS: Record<string, string> = {
  "build ui": "frontend_agent",
  "implement api": "backend_agent",
  "write test": "qa_agent",
};

function routeTask(task: string, bindings?: Record<string, string>): string {
  return routeTaskWithMatch(task, bindings).agent;
}

function routeTaskWithMatch(
  task: string,
  bindings?: Record<string, string>
): { agent: string; matched_by: string } {
  const useBindings = bindings || BINDINGS;
  for (const [keyword, agent] of Object.entries(useBindings)) {
    if (task.includes(keyword)) {
      return { agent, matched_by: keyword };
    }
  }
  return { agent: "generalist_agent", matched_by: "default" };
}

function runCentralized(tasks: string[]): string[] {
  const logs: string[] = [];
  for (const task of tasks) {
    const agent = routeTask(task);
    logs.push(`routed:${task}->${agent}`);
  }
  return logs;
}

function main(): void {
  console.log(runCentralized(["build ui", "implement api", "unknown"]));
}

main();
