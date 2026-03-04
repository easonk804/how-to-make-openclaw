// TypeScript mirror for Chapter 03: Session and DM Scope (v3)
// Run with: npx ts-node v3_scope_policy.ts

type Policy = "main" | "per-peer" | "per-channel-peer";

interface Envelope {
  channel?: string;
  user?: string;
  is_dm?: boolean;
  [key: string]: unknown;
}

function buildSessionKey(
  channel: string,
  user: string,
  isDm: boolean,
  policy: Policy
): string {
  if (policy === "main") {
    return "main";
  }

  if (policy === "per-peer") {
    if (isDm) {
      return `peer:${user}`;
    }
    return "main";
  }

  if (policy === "per-channel-peer") {
    return `${channel}:${user}`;
  }

  throw new Error(`unknown policy: ${policy}`);
}

function routeSession(
  envelope: Envelope,
  policy: Policy
): { policy: Policy; session_key: string } {
  const channel = envelope.channel ?? "unknown";
  const user = envelope.user ?? "unknown";
  const isDm = envelope.is_dm ?? false;

  const key = buildSessionKey(channel, user, isDm, policy);
  return {
    policy,
    session_key: key,
  };
}

function main(): void {
  const env: Envelope = { channel: "telegram", user: "alice", is_dm: true };
  console.log(routeSession(env, "per-peer"));
  console.log(routeSession(env, "per-channel-peer"));
}

main();
