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
Single-file validation entry point.

Zero-install: `uv run` reads the PEP 723 block above and resolves dependencies
into a throwaway environment, so the editor hook needs nothing installed.

Usage:
    uv run scripts/validate.py path/to/models/gold/dim_customers.sql
    uv run scripts/validate.py --simple "$FILE_PATH"

Exits 0 for anything that is not a dbt model, including a nonexistent path, so it
is safe on a hook that fires for every write.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from dbt_quality.cli import validate_main  # noqa: E402

if __name__ == "__main__":
    validate_main()
