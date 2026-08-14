#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml>=6.0",
#     "typer>=0.9.0",
#     "rich>=13.0.0",
#     "GitPython>=3.1",
# ]
# ///
"""
Zero-install entry point.

``uv run scripts/audit.py audit <path>`` resolves the dependencies above into a
throwaway environment, so the audit runs against an unfamiliar repo without
installing anything into the user's project or their global Python.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from dbt_quality.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
