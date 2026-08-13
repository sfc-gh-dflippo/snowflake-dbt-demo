#!/usr/bin/env python3
"""
SessionStart hook: bootstrap the dbt-quality VS Code tasks into the project.

Cortex Code Desktop is a VS Code fork; ``.vscode/tasks.json`` + a
``problemMatcher`` is the only supported way to populate the Problems panel --
a hook process cannot drive editor UI directly. So instead of touching the
Problems panel itself, this hook makes sure the *task definitions* that do are
present in whichever dbt project the session opened. The editor owns task
execution and Problems-panel diagnostics, so a newly added watcher starts only
after a window reload or when the user starts the task manually.

Idempotent and additive:

- Skipped entirely if the session's cwd is not inside a dbt project (no
  ``dbt_project.yml`` found walking up from cwd).
- Adds only missing dbt-quality tasks. Existing tasks (even hand-edited, even
  pointing at a different script path) are left untouched.
- Skipped, rather than overwritten, if ``.vscode/tasks.json`` exists but is
  not valid JSON (e.g. hand-written JSONC with comments) -- never clobber a
  file this hook cannot safely round-trip.

Uses only the standard library, since it runs under the bare ``python3`` that
``hooks.json`` invokes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
LINT_SCRIPT = PLUGIN_ROOT / "scripts" / "lint.py"

TASK_LABELS = {
    "dbt: quality suggestions",
    "dbt: quality suggestions (watch, every 5 min)",
}

_PATTERN = {
    "regexp": r"^(.+?):(\d+):(\d+):(\d+):(\d+):\s+(error|warning|info):\s+\[(SSC-(?:EWI|FDM|PRF)-DBT[A-Z]{3}\d{4})\]\s+(.*)$",
    "file": 1,
    "line": 2,
    "column": 3,
    "endLine": 4,
    "endColumn": 5,
    "severity": 6,
    "code": 7,
    "message": 8,
}


def _continue(context: str = "") -> None:
    sys.stdout.write(context if context else '{"continue": true}')


def _find_project_root(cwd: Path) -> Path | None:
    """Walk up from cwd looking for dbt_project.yml, stopping at the filesystem root."""
    current = cwd.resolve()
    for _ in range(8):
        if (current / "dbt_project.yml").is_file():
            return current
        if current.parent == current:
            return None
        current = current.parent
    return None


def _new_tasks(lint_script: Path) -> list[dict]:
    lint_cmd = f'uv run --script "{lint_script}" .'
    return [
        {
            "label": "dbt: quality suggestions",
            "detail": "All dbt quality suggestions for the workspace, into the Problems panel.",
            "type": "shell",
            "command": lint_cmd,
            "options": {"cwd": "${workspaceFolder}"},
            "presentation": {"reveal": "silent", "panel": "dedicated", "clear": True},
            "problemMatcher": {
                "owner": "dbt-quality",
                "source": "dbt-quality",
                "fileLocation": ["relative", "${workspaceFolder}"],
                "pattern": _PATTERN,
            },
            "group": "test",
        },
        {
            "label": "dbt: quality suggestions (watch, every 5 min)",
            "detail": "Auto-starts on folder open; re-runs the lint every 5 minutes for as long as this task keeps running, refreshing the Problems panel.",
            "type": "shell",
            "command": (
                f"while true; do echo '>>> dbt-quality lint start'; {lint_cmd}; "
                "echo '>>> dbt-quality lint done'; sleep 300; done"
            ),
            "options": {"cwd": "${workspaceFolder}"},
            "isBackground": True,
            "presentation": {"reveal": "silent", "panel": "dedicated", "clear": False},
            "problemMatcher": {
                "owner": "dbt-quality",
                "source": "dbt-quality",
                "fileLocation": ["relative", "${workspaceFolder}"],
                "pattern": _PATTERN,
                "background": {
                    "activeOnStart": True,
                    "beginsPattern": "^>>> dbt-quality lint start$",
                    "endsPattern": "^>>> dbt-quality lint done$",
                },
            },
            "runOptions": {"runOn": "folderOpen"},
        },
    ]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        _continue()
        return 0

    if not LINT_SCRIPT.is_file():
        _continue()
        return 0

    cwd = Path(payload.get("cwd") or Path.cwd())
    project_root = _find_project_root(cwd)
    if project_root is None:
        _continue()
        return 0

    tasks_path = project_root / ".vscode" / "tasks.json"
    if tasks_path.is_file():
        try:
            config = json.loads(tasks_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            # Cannot safely round-trip hand-edited JSONC; leave it alone.
            _continue()
            return 0
        existing_labels = {t.get("label") for t in config.get("tasks", [])}
        missing_labels = TASK_LABELS - existing_labels
        if not missing_labels:
            _continue(
                "dbt-quality: the five-minute watcher is already configured. "
                'Reload the window or run "dbt: quality suggestions (watch, every 5 min)" '
                "to start it in this session."
            )
            return 0
        config.setdefault("tasks", []).extend(
            task for task in _new_tasks(LINT_SCRIPT) if task["label"] in missing_labels
        )
    else:
        config = {"version": "2.0.0", "tasks": _new_tasks(LINT_SCRIPT)}

    try:
        tasks_path.parent.mkdir(parents=True, exist_ok=True)
        tasks_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    except OSError:
        _continue()
        return 0

    _continue(
        f"dbt-quality: added the lint task(s) to {tasks_path} "
        '(reload the window, or run "dbt: quality suggestions (watch, every 5 min)", '
        "to start the five-minute watcher)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
