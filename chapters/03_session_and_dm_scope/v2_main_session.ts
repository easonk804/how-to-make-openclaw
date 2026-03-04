// TypeScript mirror for Chapter 03: Session and DM Scope (v2)
// Run with: npx ts-node v2_main_session.ts

class SessionStore {
  private _messages: Map<string, string[]> = new Map();

  append(key: string, message: string): void {
    if (!this._messages.has(key)) {
      this._messages.set(key, []);
    }
    this._messages.get(key)!.push(message);
  }

  history(key: string): string[] {
    return [...(this._messages.get(key) || [])];
  }
}

function mainSessionKey(workspace: string, agent: string): string {
  return `${workspace}:${agent}:main`;
}

function handleWithMainSession(
  store: SessionStore,
  text: string,
  workspace: string = "demo",
  agent: string = "openclaw"
): { session_key: string; history_size: number } {
  const key = mainSessionKey(workspace, agent);
  store.append(key, `user:${text}`);
  store.append(key, `assistant:ack:${text}`);
  return {
    session_key: key,
    history_size: store.history(key).length,
  };
}

function main(): void {
  const store = new SessionStore();
  console.log(handleWithMainSession(store, "hello"));
}

main();
