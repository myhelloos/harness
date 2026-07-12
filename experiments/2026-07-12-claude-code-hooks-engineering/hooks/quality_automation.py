from __future__ import annotations

from pathlib import Path
from typing import Any

from hooklib import emit, fail_closed, load_policy, read_event, run_argv


def expand_argv(argv: list[str], file_path: str | None, cwd: Path) -> list[str]:
    replacements = {"{cwd}": str(cwd), "{file}": file_path or ""}
    return [replacements.get(item, item) for item in argv]


def formatter_for(file_path: str, policy: dict[str, Any]) -> dict[str, Any] | None:
    suffix = Path(file_path).suffix.lower()
    for formatter in policy.get("formatters", []):
        if suffix in {item.lower() for item in formatter.get("suffixes", [])}:
            return formatter
    return None


def post_tool_use(event: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any] | None:
    tool_input = event.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not isinstance(file_path, str) or not file_path:
        return None

    formatter = formatter_for(file_path, policy)
    if not formatter:
        return None

    cwd = Path(str(event.get("cwd") or ".")).resolve(strict=False)
    argv = expand_argv(formatter["argv"], file_path, cwd)
    status, returncode, output = run_argv(argv, cwd, int(formatter.get("timeout_seconds", 30)))
    name = formatter["name"]

    if status == "missing" and not formatter.get("required", False):
        return None
    if status == "completed" and returncode == 0:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"Formatter {name} completed for {file_path}.",
            }
        }

    details = output or f"status={status}, returncode={returncode}"
    return {
        "decision": "block",
        "reason": f"Formatter {name} failed for {file_path}: {details}",
    }


def run_checks(event: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any] | None:
    cwd = Path(str(event.get("cwd") or ".")).resolve(strict=False)
    failures: list[str] = []
    for check in policy.get("checks", []):
        argv = expand_argv(check["argv"], None, cwd)
        status, returncode, output = run_argv(argv, cwd, int(check.get("timeout_seconds", 120)))
        if status != "completed" or returncode != 0:
            details = output or f"status={status}, returncode={returncode}"
            failures.append(f"{check['name']}: {details}")

    if not failures:
        return None

    reason = "Quality gate failed:\n- " + "\n- ".join(failures)
    if event.get("stop_hook_active"):
        return {
            "continue": False,
            "stopReason": "Quality checks still fail after one Stop-hook continuation; stopping the run to avoid an infinite loop.",
        }
    return {"decision": "block", "reason": reason}


def evaluate(event: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any] | None:
    event_name = event.get("hook_event_name")
    if event_name == "PostToolUse":
        return post_tool_use(event, policy)
    if event_name == "Stop":
        return run_checks(event, policy)
    return None


def main() -> None:
    try:
        event = read_event()
        policy = load_policy("CLAUDE_HOOK_QUALITY_POLICY", "policies/quality-policy.example.json")
        emit(evaluate(event, policy))
    except Exception as error:
        fail_closed("quality", error)


if __name__ == "__main__":
    main()
