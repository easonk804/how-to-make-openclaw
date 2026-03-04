// TypeScript mirror for Chapter 04: ReAct and Tool Stream (v3)
// Run with: npx ts-node v3_react_tool_stream.ts

interface TraceEvent {
  type: string;
  content?: string;
  tool?: string;
  command?: string;
}

function simulateTool(action: string): string {
  if (action === "pip_install_requests") return "ok:installed requests";
  return "failed:unknown action";
}

function reactSolve(problem: string): [TraceEvent[], string] {
  const trace: TraceEvent[] = [];

  trace.push({ type: "thought", content: `Analyze problem: ${problem}` });

  if (problem.includes("requests")) {
    trace.push({
      type: "action",
      tool: "shell",
      command: "pip install requests",
    });
    const observation = simulateTool("pip_install_requests");
    trace.push({ type: "observation", content: observation });
    const final = "Dependency fixed: requests installed.";
    trace.push({ type: "final", content: final });
    return [trace, final];
  }

  trace.push({
    type: "action",
    tool: "log_inspector",
    command: "inspect logs",
  });
  const observation = simulateTool("unknown");
  trace.push({ type: "observation", content: observation });
  const final = "Need deeper diagnostics from logs.";
  trace.push({ type: "final", content: final });
  return [trace, final];
}

function main(): void {
  const [trace, final] = reactSolve("ModuleNotFoundError: No module named 'requests'");
  console.log(trace);
  console.log(final);
}

main();
