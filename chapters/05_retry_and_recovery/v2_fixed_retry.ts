// TypeScript mirror for Chapter 05: Retry and Recovery (v2)
// Run with: npx ts-node v2_fixed_retry.ts

function runWithFixedRetry(
  simulatedErrors: string[],
  maxRetries: number = 3
): [string, string[]] {
  const logs: string[] = [];

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    logs.push(`attempt:${attempt}`);
    if (attempt < simulatedErrors.length) {
      logs.push(`error:${simulatedErrors[attempt]}`);
      continue;
    }
    logs.push("success");
    return ["success", logs];
  }

  logs.push("exhausted");
  return ["failed", logs];
}

function main(): void {
  console.log(runWithFixedRetry(["timeout", "timeout"], 2));
}

main();
