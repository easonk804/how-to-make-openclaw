// TypeScript mirror for Chapter 09: Multi-Agent Routing (v3)
// Run with: npx ts-node v3_isolated_routing.ts

interface RouteResult {
  workspace: string;
  session: string;
  agent: string;
  status: string;
}

function routeWithIsolation(
  workspace: string,
  user: string,
  auth: string,
  intent: string
): RouteResult {
  if (auth !== "allowed") {
    return {
      workspace,
      session: `${workspace}:denied:${user}`,
      agent: "none",
      status: "blocked",
    };
  }

  let agent: string;
  if (intent === "frontend") {
    agent = "frontend_agent";
  } else if (intent === "backend") {
    agent = "backend_agent";
  } else {
    agent = "generalist_agent";
  }

  return {
    workspace,
    session: `${workspace}:${user}:${intent}`,
    agent,
    status: "ok",
  };
}

function agentHandoff(sender: string, receiver: string, payload: string): string {
  return `handoff:${sender}->${receiver}:${payload}`;
}

function decentralizedRun(): string[] {
  const logs: string[] = [];
  const route = routeWithIsolation("ws1", "alice", "allowed", "frontend");
  logs.push(`route:${route.agent}:${route.status}`);
  logs.push(agentHandoff("frontend_agent", "backend_agent", "need API contract"));
  return logs;
}

function main(): void {
  console.log(decentralizedRun());
}

main();
