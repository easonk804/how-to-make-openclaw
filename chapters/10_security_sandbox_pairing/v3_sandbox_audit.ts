// TypeScript mirror for Chapter 10: Security Sandbox Pairing (v3)
// Run with: npx ts-node v3_sandbox_audit.ts

interface AuditRecord {
  timestamp: number;
  command: string;
  decision: string;
  reason: string;
}

const DEFAULT_WHITELIST = ["echo", "pwd", "ls", "dir", "whoami", "python", "node", "npm", "npx"];
const AUDIT_LOG: AuditRecord[] = [];
const MAX_AUDIT_LOG_SIZE = 1000;

function isDangerous(command: string): boolean {
  const lowered = command.toLowerCase();
  const blockedPatterns = ["rm -rf", "del /f", "format c:"];
  return blockedPatterns.some((pattern) => lowered.includes(pattern));
}

function baseCommand(command: string): string {
  const parts = command.trim().split(/\s+/);
  return parts[0]?.toLowerCase() ?? "";
}

function appendAudit(record: AuditRecord): void {
  AUDIT_LOG.push(record);
  if (AUDIT_LOG.length > MAX_AUDIT_LOG_SIZE) {
    AUDIT_LOG.splice(0, AUDIT_LOG.length - MAX_AUDIT_LOG_SIZE);
  }
}

function listAudit(limit: number = 100): AuditRecord[] {
  const keep = Math.max(1, limit);
  return AUDIT_LOG.slice(-keep).reverse();
}

function clearAudit(): void {
  AUDIT_LOG.length = 0;
}

function enforce(command: string, whitelist?: string[]): [string, AuditRecord] {
  const allow = new Set((whitelist || DEFAULT_WHITELIST).map((item) => item.toLowerCase()));

  if (isDangerous(command)) {
    const record: AuditRecord = {
      timestamp: Date.now(),
      command,
      decision: "blocked",
      reason: "sandbox_dangerous_pattern",
    };
    appendAudit(record);
    return ["blocked", record];
  }

  const base = baseCommand(command);
  if (!base) {
    const record: AuditRecord = {
      timestamp: Date.now(),
      command,
      decision: "blocked",
      reason: "command_required",
    };
    appendAudit(record);
    return ["blocked", record];
  }

  if (!allow.has(base)) {
    const record: AuditRecord = {
      timestamp: Date.now(),
      command,
      decision: "blocked",
      reason: `whitelist_block:${base}`,
    };
    appendAudit(record);
    return ["blocked", record];
  }

  const record: AuditRecord = {
    timestamp: Date.now(),
    command,
    decision: "allowed",
    reason: "sandbox_ok",
  };
  appendAudit(record);
  return ["allowed", record];
}

function main(): void {
  console.log(enforce("rm -rf /tmp/demo"));
}

main();
