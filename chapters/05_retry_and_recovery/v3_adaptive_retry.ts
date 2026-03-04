// TypeScript mirror for Chapter 05: Retry and Recovery (v3)
// Run with: npx ts-node v3_adaptive_retry.ts

type ErrorCategory = "transient" | "fatal" | "unknown";

interface LogEntry {
  event: string;
  value: string;
}

function classifyError(error: string): ErrorCategory {
  const lowered = error.toLowerCase();
  if (lowered.includes("timeout") || lowered.includes("network") || lowered.includes("429")) {
    return "transient";
  }
  if (lowered.includes("permission") || lowered.includes("auth") || lowered.includes("401") || lowered.includes("403")) {
    return "fatal";
  }
  if (lowered.includes("5xx") || lowered.includes("500") || lowered.includes("502") || lowered.includes("503") || lowered.includes("504")) {
    return "transient";
  }
  if (lowered.includes("4xx") || lowered.includes("400") || lowered.includes("404")) {
    return "fatal";
  }
  return "unknown";
}

function runWithAdaptiveRetry(
  simulatedErrors: string[],
  maxRetries: number = 4
): [string, LogEntry[]] {
  const logs: LogEntry[] = [];

  let attempt = 0;
  while (attempt <= maxRetries) {
    logs.push({ event: "attempt", value: String(attempt) });

    if (attempt < simulatedErrors.length) {
      const error = simulatedErrors[attempt];
      const category = classifyError(error);
      logs.push({ event: "error", value: error });
      logs.push({ event: "category", value: category });

      if (category === "fatal") {
        logs.push({ event: "decision", value: "stop" });
        return ["failed", logs];
      }

      if (attempt >= maxRetries) {
        logs.push({ event: "decision", value: "exhausted" });
        return ["failed", logs];
      }

      const backoffMs = Math.min(1000 * Math.pow(2, attempt), 8000);
      logs.push({ event: "retry_delay_ms", value: String(backoffMs) });
      logs.push({ event: "decision", value: "retry" });

      attempt++;
      continue;
    }

    logs.push({ event: "decision", value: "success" });
    return ["success", logs];
  }

  logs.push({ event: "decision", value: "exhausted" });
  return ["failed", logs];
}

function main(): void {
  const [status, logs] = runWithAdaptiveRetry(["network timeout", "network timeout"], 3);
  console.log(status);
  console.log(logs);
}

main();
