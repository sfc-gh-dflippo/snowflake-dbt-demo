#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml>=6.0",
#     "typer>=0.9.0",
#     "rich>=13.0.0",
# ]
# ///
"""
dbt File Validator

Validates dbt SQL models and schema YAML files for best practices.

Usage:
    # With uv (auto-installs dependencies)
    uv run validate_dbt_file.py <file_path>

    # With Python (requires: pip install pyyaml typer rich)
    python validate_dbt_file.py <file_path>

    # Or make executable
    chmod +x validate_dbt_file.py
    ./validate_dbt_file.py <file_path>
"""

import sys
from pathlib import Path

# Check for required dependencies
MISSING_DEPS = []

try:
    import yaml  # noqa: F401
except ImportError:
    MISSING_DEPS.append("pyyaml")

try:
    import typer  # noqa: F401
except ImportError:
    MISSING_DEPS.append("typer")

try:
    import rich  # noqa: F401
except ImportError:
    MISSING_DEPS.append("rich")

if MISSING_DEPS:
    print(
        f"Error: Missing required dependencies: {', '.join(MISSING_DEPS)}",
        file=sys.stderr,
    )
    print("\nInstall with one of:", file=sys.stderr)
    print(f"  pip install {' '.join(MISSING_DEPS)}", file=sys.stderr)
    print("  uv run validate_dbt_file.py <file>  # auto-installs deps", file=sys.stderr)
    sys.exit(1)

# Add src directory to path for package imports
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from dbt_validation.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
