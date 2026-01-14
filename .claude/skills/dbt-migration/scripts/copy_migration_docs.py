#!/usr/bin/env python3
"""
Copy migration documentation from snowflake-docs to translation-references.

This script copies translation reference files from the snowflake-docs skill
to the dbt-migration skill's translation-references folder, organizing them
by database platform.

Usage:
    python copy_migration_docs.py

Source: .claude/skills/snowflake-docs/en/migrations/snowconvert-docs/translation-references/
Target: .claude/skills/dbt-migration/translation-references/
"""

import shutil
from pathlib import Path

# Get paths relative to script location
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent.parent

# Source and target directories
SOURCE_DIR = (
    REPO_ROOT
    / ".claude/skills/snowflake-docs/en/migrations/snowconvert-docs/translation-references"
)
TARGET_DIR = SKILL_DIR / "translation-references"

# Database folders to copy
DATABASE_FOLDERS = [
    "bigquery",
    "db2",
    "general",
    "hive",
    "oracle",
    "postgres",
    "redshift",
    "ssis",
    "sybase",
    "teradata",
    "transact",
    "vertica",
]


def copy_database_folder(db_name: str) -> int:
    """Copy a database folder from source to target.

    Args:
        db_name: Name of the database folder to copy

    Returns:
        Number of files copied
    """
    source_path = SOURCE_DIR / db_name
    target_path = TARGET_DIR / db_name

    if not source_path.exists():
        print(f"  Warning: Source folder not found: {source_path}")
        return 0

    # Create target directory
    target_path.mkdir(parents=True, exist_ok=True)

    # Copy all markdown files (excluding .html.md duplicates)
    files_copied = 0
    for source_file in source_path.rglob("*.md"):
        # Skip .html.md files (duplicates)
        if source_file.name.endswith(".html.md"):
            continue

        # Calculate relative path and target location
        rel_path = source_file.relative_to(source_path)
        target_file = target_path / rel_path

        # Create parent directories if needed
        target_file.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file
        shutil.copy2(source_file, target_file)
        files_copied += 1

    return files_copied


def main():
    """Main function to copy all migration documentation."""

    if not SOURCE_DIR.exists():
        print(f"Error: Source directory not found: {SOURCE_DIR}")
        print("Make sure the snowflake-docs skill is present.")
        return

    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print()

    # Create target directory
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    total_files = 0
    for db_name in DATABASE_FOLDERS:
        print(f"Copying {db_name}...")
        count = copy_database_folder(db_name)
        print(f"  Copied {count} files")
        total_files += count

    print()
    print(f"Done! Copied {total_files} total files.")
    print()
    print("Next steps:")
    print("  1. Run clean_migration_docs.py to remove boilerplate")
    print("  2. Run clean_skill_descriptions.py to update SKILL.md")
    print("  3. Run pre-commit to format files")


if __name__ == "__main__":
    main()
