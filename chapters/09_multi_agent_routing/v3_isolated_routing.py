from __future__ import annotations


def route_with_isolation(
    workspace: str,
    user: str,
    auth: str,
    intent: str,
) -> dict[str, str]:
    if auth != "allowed":
        return {
            "workspace": workspace,
            "session": f"{workspace}:denied:{user}",
            "agent": "none",
            "status": "blocked",
        }

    if intent == "frontend":
        agent = "frontend_agent"
    elif intent == "backend":
        agent = "backend_agent"
    else:
        agent = "generalist_agent"

    return {
        "workspace": workspace,
        "session": f"{workspace}:{user}:{intent}",
        "agent": agent,
        "status": "ok",
    }


def agent_handoff(sender: str, receiver: str, payload: str) -> str:
    return f"handoff:{sender}->{receiver}:{payload}"


def decentralized_run() -> list[str]:
    logs: list[str] = []
    route = route_with_isolation("ws1", "alice", "allowed", "frontend")
    logs.append(f"route:{route['agent']}:{route['status']}")
    logs.append(agent_handoff("frontend_agent", "backend_agent", "need API contract"))
    return logs


def main() -> None:
    print(decentralized_run())


if __name__ == "__main__":
    main()
