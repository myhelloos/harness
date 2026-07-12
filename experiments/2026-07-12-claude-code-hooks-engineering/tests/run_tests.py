from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
HOOKS = ROOT / "hooks"


def fixture(name: str) -> dict[str, Any]:
    with (FIXTURES / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def run_hook(script: str, event: dict[str, Any], env: dict[str, str] | None = None) -> tuple[int, str, str]:
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
    completed = subprocess.run(
        [sys.executable, str(HOOKS / script)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env=process_env,
        check=False,
    )
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def parsed(stdout: str) -> dict[str, Any]:
    return json.loads(stdout) if stdout else {}


class SecurityGuardTests(unittest.TestCase):
    def test_safe_command_has_no_decision(self) -> None:
        code, stdout, stderr = run_hook("security_guard.py", fixture("security-safe-bash.json"))
        self.assertEqual((code, stdout, stderr), (0, "", ""))

    def test_secret_prompt_is_blocked_without_echoing_secret(self) -> None:
        event = fixture("security-secret-prompt.json")
        code, stdout, stderr = run_hook("security_guard.py", event)
        output = parsed(stdout)
        self.assertEqual((code, stderr, output["decision"]), (0, "", "block"))
        self.assertNotIn("ghp_", stdout)

    def test_dangerous_command_is_denied(self) -> None:
        _, stdout, _ = run_hook("security_guard.py", fixture("security-dangerous-bash.json"))
        specific = parsed(stdout)["hookSpecificOutput"]
        self.assertEqual(specific["permissionDecision"], "deny")

    def test_protected_write_is_denied(self) -> None:
        _, stdout, _ = run_hook("security_guard.py", fixture("security-protected-write.json"))
        specific = parsed(stdout)["hookSpecificOutput"]
        self.assertEqual(specific["permissionDecision"], "deny")

    def test_force_push_requires_confirmation(self) -> None:
        _, stdout, _ = run_hook("security_guard.py", fixture("security-force-push.json"))
        specific = parsed(stdout)["hookSpecificOutput"]
        self.assertEqual(specific["permissionDecision"], "ask")


class QualityAutomationTests(unittest.TestCase):
    def policy_env(self, name: str) -> dict[str, str]:
        return {"CLAUDE_HOOK_QUALITY_POLICY": str(FIXTURES / name)}

    def test_formatter_success_adds_context(self) -> None:
        _, stdout, _ = run_hook(
            "quality_automation.py",
            fixture("quality-post-write.json"),
            self.policy_env("quality-policy-pass.json"),
        )
        specific = parsed(stdout)["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "PostToolUse")
        self.assertIn("completed", specific["additionalContext"])

    def test_stop_failure_requests_continuation(self) -> None:
        _, stdout, _ = run_hook(
            "quality_automation.py",
            fixture("quality-stop.json"),
            self.policy_env("quality-policy-fail.json"),
        )
        output = parsed(stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("failing check", output["reason"])

    def test_repeated_stop_failure_does_not_loop(self) -> None:
        event = fixture("quality-stop.json")
        event["stop_hook_active"] = True
        _, stdout, _ = run_hook(
            "quality_automation.py", event, self.policy_env("quality-policy-fail.json")
        )
        output = parsed(stdout)
        self.assertNotIn("decision", output)
        self.assertFalse(output["continue"])
        self.assertIn("infinite loop", output["stopReason"])

    def test_stop_success_has_no_decision(self) -> None:
        code, stdout, stderr = run_hook(
            "quality_automation.py",
            fixture("quality-stop.json"),
            self.policy_env("quality-policy-pass.json"),
        )
        self.assertEqual((code, stdout, stderr), (0, "", ""))


class SubagentContextTests(unittest.TestCase):
    def test_start_injects_agent_specific_context(self) -> None:
        _, stdout, _ = run_hook("subagent_context.py", fixture("subagent-start-explore.json"))
        context = parsed(stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("read-only discovery task", context)
        self.assertIn("Summary, Evidence, Unknowns", context)

    def test_incomplete_output_keeps_subagent_running(self) -> None:
        _, stdout, _ = run_hook("subagent_context.py", fixture("subagent-stop-incomplete.json"))
        output = parsed(stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("Evidence", output["reason"])
        self.assertIn("Unknowns", output["reason"])

    def test_complete_output_can_stop(self) -> None:
        code, stdout, stderr = run_hook(
            "subagent_context.py", fixture("subagent-stop-complete.json")
        )
        self.assertEqual((code, stdout, stderr), (0, "", ""))

    def test_repeated_incomplete_output_does_not_loop(self) -> None:
        event = fixture("subagent-stop-incomplete.json")
        event["stop_hook_active"] = True
        _, stdout, _ = run_hook("subagent_context.py", event)
        output = parsed(stdout)
        self.assertNotIn("decision", output)
        self.assertFalse(output["continue"])
        self.assertIn("infinite loop", output["stopReason"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
