from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]


def read_event() -> dict[str, Any]:
    event = json.load(__import__("sys").stdin)
    if not isinstance(event, dict):
        raise ValueError("hook input must be a JSON object")
    return event


def emit(payload: dict[str, Any] | None) -> None:
    if payload:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))


def load_policy(env_name: str, default_relative_path: str) -> dict[str, Any]:
    configured = os.environ.get(env_name)
    path = Path(configured) if configured else EXPERIMENT_ROOT / default_relative_path
    with path.open(encoding="utf-8") as handle:
        policy = json.load(handle)
    if not isinstance(policy, dict):
        raise ValueError(f"policy must be a JSON object: {path}")
    return policy


def fail_closed(component: str, error: Exception) -> None:
    emit(
        {
            "continue": False,
            "stopReason": f"{component} hook configuration or runtime error: {type(error).__name__}",
        }
    )


def run_argv(
    argv: list[str], cwd: Path, timeout_seconds: int
) -> tuple[str, int | None, str]:
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except FileNotFoundError:
        return "missing", None, f"executable not found: {argv[0]}"
    except subprocess.TimeoutExpired:
        return "timeout", None, f"timed out after {timeout_seconds}s"

    output = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
    return "completed", completed.returncode, output[-4000:]
