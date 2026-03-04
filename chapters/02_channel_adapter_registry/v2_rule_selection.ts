// TypeScript mirror for Chapter 02: Channel Adapter Registry (v2)
// Run with: npx ts-node v2_rule_selection.ts

interface Rule {
  when: Record<string, string>;
  adapter: string;
}

const DEFAULT_RULES: Rule[] = [
  { when: { channel: "telegram" }, adapter: "telegram_adapter" },
  { when: { channel: "discord" }, adapter: "discord_adapter" },
  { when: { channel: "webchat" }, adapter: "webchat_adapter" },
];

function chooseAdapter(
  envelope: Record<string, string>,
  rules?: Rule[]
): string {
  const useRules = rules ?? DEFAULT_RULES;

  for (const rule of useRules) {
    const when = rule.when;
    const matches = Object.entries(when).every(
      ([k, v]) => envelope[k] === v
    );
    if (matches) return rule.adapter;
  }
  return "default_adapter";
}

function dispatchWithRules(envelope: Record<string, string>): string {
  const adapter = chooseAdapter(envelope);
  return `${adapter}:handled:${envelope.text ?? ""}`;
}

function main(): void {
  const env = { channel: "discord", text: "ping" };
  console.log(dispatchWithRules(env));
}

main();
