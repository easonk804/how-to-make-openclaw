// TypeScript mirror for Chapter 01: Gateway Event Loop
// Run with: npx ts-node v1_sync_flow.ts

function decideAction(text: string): [string, string] {
  const lowered = text.toLowerCase();
  if (lowered.includes("create") || text.includes("创建")) {
    return ["create_file", "demo.txt"];
  }
  if (lowered.includes("read") || text.includes("读取")) {
    return ["read_file", "demo.txt"];
  }
  return ["reply", "-"];
}

function handleSync(text: string): Record<string, string> {
  const [action, target] = decideAction(text);
  let egress: string;

  if (action === "create_file") {
    egress = `created:${target}`;
  } else if (action === "read_file") {
    egress = `content:${target}=<mock>`;
  } else {
    egress = `reply:${text}`;
  }

  return {
    ingress: text,
    action,
    target,
    egress,
  };
}

function main(): void {
  const out = handleSync("请创建一个演示文件");
  console.log(out);
}

main();
