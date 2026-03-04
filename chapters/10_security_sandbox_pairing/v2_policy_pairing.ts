// TypeScript mirror for Chapter 10: Security Sandbox Pairing (v2)
// Run with: npx ts-node v2_policy_pairing.ts

function enforceDmPolicy(
  isDm: boolean,
  user: string,
  dmPolicy: string,
  pairedUsers: Set<string>
): [string, string] {
  if (!isDm) {
    return ["allowed", "non-dm"];
  }

  if (dmPolicy === "allow_all") {
    return ["allowed", "dm-allow-all"];
  }

  if (dmPolicy === "paired_only" && pairedUsers.has(user)) {
    return ["allowed", "dm-paired"];
  }

  return ["blocked", "dm-policy"];
}

function main(): void {
  const [decision, reason] = enforceDmPolicy(true, "alice", "paired_only", new Set(["bob"]));
  console.log(decision, reason);
}

main();
