// TypeScript mirror for Chapter 04: ReAct and Tool Stream (v1)
// Run with: npx ts-node v1_direct_answer.ts

function directAnswer(problem: string): string {
  if (problem.includes("ModuleNotFoundError") && problem.includes("requests")) {
    return "Install dependency: pip install requests";
  }
  return "Use logs to diagnose the issue.";
}

function main(): void {
  console.log(directAnswer("ModuleNotFoundError: No module named 'requests'"));
}

main();
