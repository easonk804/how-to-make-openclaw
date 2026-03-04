// TypeScript mirror for Chapter 01: Gateway Event Loop (v3)
// Run with: npx ts-node v3_event_lifecycle.ts

interface LifecycleEvent {
  type: string;
  [key: string]: string | undefined;
}

interface MessageResult {
  message: string;
  events: LifecycleEvent[];
  final: string;
}

function intentFromText(text: string): string {
  const lowered = text.toLowerCase();
  if (lowered.includes("create") || text.includes("创建")) {
    return "create_file";
  }
  if (lowered.includes("read") || text.includes("读取")) {
    return "read_file";
  }
  return "reply";
}

function lifecycleForMessage(
  text: string,
  channel: string = "cli",
  user: string = "u1"
): LifecycleEvent[] {
  const intent = intentFromText(text);
  return [
    { type: "lifecycle_start", channel, user },
    { type: "ingress", text },
    { type: "act", intent },
    { type: "egress", message: `done:${intent}` },
    { type: "lifecycle_end", status: "ok" },
  ];
}

function runGatewayLoop(
  inputs: string[],
  channel: string = "cli",
  user: string = "u1"
): MessageResult[] {
  return inputs.map((text) => {
    const events = lifecycleForMessage(text, channel, user);
    return {
      message: text,
      events,
      final: events[events.length - 2].message ?? "",
    };
  });
}

function main(): void {
  const out = runGatewayLoop(["create a file", "read file"]);
  console.log(out);
}

main();
