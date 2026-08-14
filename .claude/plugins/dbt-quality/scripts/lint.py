#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml>=6.0",
#     "typer>=0.9.0",
#     "rich>=13.0.0",
# ]
# ///
"""
Linter entry point, for wiring into an editor.

Emits one line per suggestion in the classic linter shape:

    path:line:col:endLine:endCol: level: [RULE] message -> fix

which a VS Code ``problemMatcher`` can parse into the Problems panel. See
``.vscode/tasks.json`` for the matcher, and the ``dbt-validate`` skill for how the
two editor integrations differ.

Usage:
    uv run scripts/lint.py .
    uv run scripts/lint.py . --min-level error
    uv run scripts/lint.py . --format json

Always exits 0 unless ``--strict`` is passed. A suggestion is not a failure.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from dbt_quality.cli import lint_main  # noqa: E402

if __name__ == "__main__":
    lint_main()
