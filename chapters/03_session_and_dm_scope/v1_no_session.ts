// TypeScript mirror for Chapter 03: Session and DM Scope (v1)
// Run with: npx ts-node v1_no_session.ts

function handleWithoutSession(text: string): { session_key: string; reply: string } {
  return {
    session_key: "ephemeral",
    reply: `stateless:${text}`,
  };
}

function main(): void {
  console.log(handleWithoutSession("hello"));
}

main();
