// TypeScript mirror for Chapter 04: ReAct and Tool Stream (v2)
// Run with: npx ts-node v2_structured_reasoning.ts

function reasonSteps(problem: string): string[] {
  const steps = ["Inspect error type", "Identify missing package"];
  if (problem.includes("requests")) {
    steps.push("Suggest installation command");
  } else {
    steps.push("Suggest dependency check");
  }
  return steps;
}

function reasonAndAnswer(problem: string): [string[], string] {
  const steps = reasonSteps(problem);
  const final = problem.includes("requests")
    ? "Run: pip install requests"
    : "Verify project dependencies and reinstall.";
  return [steps, final];
}

function main(): void {
  const [steps, final] = reasonAndAnswer("ModuleNotFoundError: No module named 'requests'");
  console.log(steps);
  console.log(final);
}

main();
