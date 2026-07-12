from __future__ import annotations

import re
from typing import Any

from hooklib import emit, fail_closed, load_policy, read_event


def agent_policy(agent_type: str, policy: dict[str, Any]) -> dict[str, Any]:
    agents = policy.get("agents", {})
    return agents.get(agent_type) or agents.get("default") or {}


def start_context(agent_type: str, spec: dict[str, Any]) -> dict[str, Any] | None:
    context = spec.get("context", [])
    required = spec.get("required_sections", [])
    if not context and not required:
        return None

    lines = [f"Scoped contract for subagent type {agent_type}:"]
    lines.extend(f"- {item}" for item in context)
    if required:
        lines.append("- Final response must contain these Markdown sections: " + ", ".join(required))
    return {
        "hookSpecificOutput": {
            "hookEventName": "SubagentStart",
            "additionalContext": "\n".join(lines),
        }
    }


def has_section(message: str, section: str) -> bool:
    pattern = rf"^\s*(?:#{{1,6}}\s*)?{re.escape(section)}\s*:?\s*$"
    return re.search(pattern, message, re.IGNORECASE | re.MULTILINE) is not None


def stop_decision(event: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any] | None:
    required = spec.get("required_sections", [])
    message = str(event.get("last_assistant_message") or "")
    missing = [section for section in required if not has_section(message, section)]
    if not missing:
        return None

    if event.get("stop_hook_active"):
        return {
            "continue": False,
            "stopReason": "Subagent output contract is still incomplete after one continuation; stopping it to avoid an infinite loop.",
        }
    return {
        "decision": "block",
        "reason": "Complete the output contract before stopping. Missing sections: " + ", ".join(missing),
    }


def evaluate(event: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any] | None:
    agent_type = str(event.get("agent_type") or "default")
    spec = agent_policy(agent_type, policy)
    if event.get("hook_event_name") == "SubagentStart":
        return start_context(agent_type, spec)
    if event.get("hook_event_name") == "SubagentStop":
        return stop_decision(event, spec)
    return None


def main() -> None:
    try:
        event = read_event()
        policy = load_policy("CLAUDE_HOOK_SUBAGENT_POLICY", "policies/subagent-context.json")
        emit(evaluate(event, policy))
    except Exception as error:
        fail_closed("subagent-context", error)


if __name__ == "__main__":
    main()
