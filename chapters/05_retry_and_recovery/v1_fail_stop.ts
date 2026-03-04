// TypeScript mirror for Chapter 05: Retry and Recovery (v1)
// Run with: npx ts-node v1_fail_stop.ts

function runOnce(simulatedError?: string): [string, string[]] {
  const logs: string[] = ["start"];
  if (simulatedError) {
    logs.push(`error:${simulatedError}`);
    logs.push("stop");
    return ["failed", logs];
  }

  logs.push("success");
  return ["success", logs];
}

function main(): void {
  console.log(runOnce("timeout"));
}

main();
