from __future__ import annotations

import fnmatch
import re
from pathlib import Path
from typing import Any

from hooklib import emit, fail_closed, load_policy, read_event


def matches_named_pattern(value: str, patterns: list[dict[str, str]]) -> str | None:
    for item in patterns:
        if re.search(item["pattern"], value, re.IGNORECASE | re.MULTILINE):
            return item["name"]
    return None


def path_candidates(raw_path: str, cwd: str) -> tuple[list[str], bool]:
    target = Path(raw_path).expanduser()
    if not target.is_absolute():
        target = Path(cwd) / target
    target = target.resolve(strict=False)
    workspace = Path(cwd).resolve(strict=False)
    try:
        relative = target.relative_to(workspace).as_posix()
        outside = False
    except ValueError:
        relative = target.as_posix()
        outside = True
    return [relative, target.name, target.as_posix()], outside


def protected_path_reason(event: dict[str, Any], policy: dict[str, Any]) -> str | None:
    tool_input = event.get("tool_input") or {}
    raw_path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not isinstance(raw_path, str) or not raw_path:
        return None

    candidates, outside = path_candidates(raw_path, str(event.get("cwd") or "."))
    if outside and policy.get("deny_writes_outside_workspace", True):
        return "writes outside the workspace are blocked"

    for pattern in policy.get("protected_paths", []):
        if any(fnmatch.fnmatch(candidate, pattern) for candidate in candidates):
            return f"path matches protected pattern {pattern}"
    return None


def pre_tool_decision(event: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any] | None:
    tool_name = str(event.get("tool_name") or "")
    tool_input = event.get("tool_input") or {}

    if tool_name in {"Edit", "Write", "NotebookEdit"}:
        reason = protected_path_reason(event, policy)
        if reason:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }

    if tool_name in {"Bash", "PowerShell"}:
        command = str(tool_input.get("command") or "")
        name = matches_named_pattern(command, policy.get("deny_commands", []))
        if name:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"blocked by security policy: {name}",
                }
            }
        name = matches_named_pattern(command, policy.get("ask_commands", []))
        if name:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": f"human confirmation required: {name}",
                }
            }

    name = matches_named_pattern(tool_name, policy.get("ask_tools", []))
    if name:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": f"human confirmation required: {name}",
            }
        }
    return None


def evaluate(event: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any] | None:
    event_name = event.get("hook_event_name")
    if event_name == "UserPromptSubmit":
        prompt = str(event.get("prompt") or "")
        name = matches_named_pattern(prompt, policy.get("secret_patterns", []))
        if name:
            return {
                "decision": "block",
                "reason": f"Prompt rejected: detected material matching the {name} secret pattern.",
            }
        return None
    if event_name == "PreToolUse":
        return pre_tool_decision(event, policy)
    return None


def main() -> None:
    try:
        event = read_event()
        policy = load_policy("CLAUDE_HOOK_SECURITY_POLICY", "policies/security-policy.json")
        emit(evaluate(event, policy))
    except Exception as error:
        fail_closed("security", error)


if __name__ == "__main__":
    main()
