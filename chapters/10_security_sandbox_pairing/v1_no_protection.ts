// TypeScript mirror for Chapter 10: Security Sandbox Pairing (v1)
// Run with: npx ts-node v1_no_protection.ts

function executeWithoutGuard(command: string): { decision: string; command: string; note: string } {
  return {
    decision: "allowed",
    command,
    note: "no protection enabled",
  };
}

function main(): void {
  console.log(executeWithoutGuard("rm -rf /tmp/demo"));
}

main();
