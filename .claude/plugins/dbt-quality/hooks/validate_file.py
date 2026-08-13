#!/usr/bin/env python3
"""
PostToolUse hook: validate a dbt model immediately after it is written.

Reads the hook payload on stdin, extracts the written path, and delegates to
``scripts/validate.py`` through ``uv run --script``. The PEP 723 header on that
script declares its own dependencies, so nothing needs installing and the hook
never depends on what happens to be importable by the system Python.

This wrapper itself uses only the standard library, so it runs under the bare
``python3`` that ``hooks.json`` invokes.

Contract with the hook runner:

- writes plain (non-JSON) text to stdout when there is something to report.
  The hook runner maps non-JSON stdout to ``additionalContext`` automatically;
  the JSON ``hookSpecificOutput.additionalContext`` form does not reach the
  agent for ``PostToolUse``, only the Desktop UI's transcript row.
- writes ``{"continue": true}`` when there is nothing to report.
- always exits 0. Nothing here blocks a save: an Error prints loudly, but a hook that
  fails mid-refactor gets switched off, after which it protects nothing. Gate on
  errors in CI with ``dbt-lint --strict`` instead.

Silent for anything that is not a dbt model, so it can fire on every write.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
VALIDATE = PLUGIN_ROOT / "scripts" / "validate.py"

#: Only these extensions can be dbt models. Checked before anything expensive.
MODEL_SUFFIXES = {".sql", ".py"}

#: Bound on the whole validation, including uv's dependency resolution. The first
#: run on a machine pays for a download; later runs come from uv's cache.
TIMEOUT_SECONDS = 60


def _continue(context: str = "") -> None:
    sys.stdout.write(context if context else '{"continue": true}')


def _target_from_payload(payload: dict) -> str | None:
    """Extract the written path, tolerating differences in payload shape."""
    tool_input = payload.get("tool_input") or {}
    for key in ("file_path", "path", "filePath", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            return value
    return os.environ.get("FILE_PATH") or None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # A malformed payload is the runner's problem. Never surface it as a
        # validation failure.
        _continue()
        return 0

    raw_target = _target_from_payload(payload)
    if not raw_target:
        _continue()
        return 0

    target = Path(raw_target)
    if target.suffix.lower() not in MODEL_SUFFIXES or "models" not in target.parts:
        _continue()
        return 0
    if not target.is_file() or not VALIDATE.is_file():
        _continue()
        return 0

    uv = shutil.which("uv")
    if uv is None:
        # No uv, so nothing can run. Stay quiet rather than blocking a save on a
        # tooling gap, but do not pretend the file was checked.
        _continue()
        return 0

    try:
        completed = subprocess.run(  # noqa: S603 -- fixed argv, no shell
            [uv, "run", "--script", str(VALIDATE), "--simple", str(target)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        _continue()
        return 0

    output = (completed.stdout or "") + (completed.stderr or "")
    _continue(output.strip())
    # Always 0. The validator's own exit code is deliberately ignored here -- see the
    # module docstring on why a save-time hook must not fail.
    return 0


if __name__ == "__main__":
    sys.exit(main())
