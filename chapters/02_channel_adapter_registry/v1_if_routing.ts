// TypeScript mirror for Chapter 02: Channel Adapter Registry (v1)
// Run with: npx ts-node v1_if_routing.ts

function routeAdapter(channel: string): string {
  const name = channel.toLowerCase();
  if (name === "telegram") return "telegram_adapter";
  if (name === "discord") return "discord_adapter";
  if (name === "webchat") return "webchat_adapter";
  return "default_adapter";
}

function dispatchMessage(channel: string, text: string): string {
  const adapter = routeAdapter(channel);
  return `${adapter}:handled:${text}`;
}

function main(): void {
  console.log(dispatchMessage("telegram", "hello"));
}

main();
