// TypeScript mirror for Chapter 09: Multi-Agent Routing (v1)
// Run with: npx ts-node v1_single_agent.ts

function runSingleAgent(task: string): { agent: string; task: string; result: string } {
  return {
    agent: "generalist",
    task,
    result: `generalist handled: ${task}`,
  };
}

function main(): void {
  console.log(runSingleAgent("build ui"));
}

main();
