// TypeScript mirror for Chapter 01: Gateway Event Loop (v2)
// Run with: npx ts-node v2_envelope.ts

interface Envelope {
  id: string;
  channel: string;
  user: string;
  payload: { text: string };
  meta: { version: number };
}

function buildEnvelope(channel: string, user: string, text: string): Envelope {
  return {
    id: `${channel}:${user}:001`,
    channel,
    user,
    payload: { text },
    meta: { version: 2 },
  };
}

function classifyIntent(text: string): string {
  const lowered = text.toLowerCase();
  if (lowered.includes("create") || text.includes("创建")) {
    return "create_file";
  }
  if (lowered.includes("read") || text.includes("读取")) {
    return "read_file";
  }
  return "reply";
}

function handleEnvelope(envelope: Envelope): Record<string, string> {
  const text = envelope.payload?.text ?? "";
  const intent = classifyIntent(text);
  return {
    id: envelope.id,
    intent,
    result: `handled:${intent}`,
  };
}

function main(): void {
  const env = buildEnvelope("telegram", "u1", "please create file");
  console.log(handleEnvelope(env));
}

main();
