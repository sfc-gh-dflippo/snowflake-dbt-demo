#!/usr/bin/env python3
"""
Migration script to move translation reference files from the consolidated
dbt-migration/translation-references folder to database-specific skill folders.

This script:
1. Reads files from dbt-migration/translation-references/{db}/
2. Generates flattened filenames with proper DB prefix
3. Checks for duplicates in target locations
4. Uses git mv for new files, git rm for duplicates
"""

import os
import subprocess
from pathlib import Path

# Base paths
SKILLS_DIR = Path(__file__).parent.parent.parent  # .claude/skills/
SOURCE_DIR = SKILLS_DIR / "dbt-migration" / "translation-references"

# Mapping of source folders to target skills and prefixes
FOLDER_MAPPING = {
    "bigquery": ("dbt-migration-bigquery", "bigquery-"),
    "db2": ("dbt-migration-db2", "db2-"),
    "hive": ("dbt-migration-hive", "hive-"),
    "oracle": ("dbt-migration-oracle", "oracle-"),
    "postgres": ("dbt-migration-postgres", "postgres-"),
    "redshift": ("dbt-migration-redshift", "redshift-"),
    "sybase": ("dbt-migration-sybase", "sybase-"),
    "teradata": ("dbt-migration-teradata", "teradata-"),
    "transact": ("dbt-migration-ms-sql-server", "ms-sql-server-"),
    "ssis": ("dbt-migration-ms-sql-server", "ms-sql-server-ssis-"),
    "vertica": ("dbt-migration-vertica", "vertica-"),
}

# Files/folders to keep in dbt-migration
KEEP_IN_PLACE = {"general", "README.md"}


# Workspace root (where .git folder is)
WORKSPACE_ROOT = SKILLS_DIR.parent.parent  # /Users/.../snowflake-dbt-demo


def run_git_command(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command and return the result."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=WORKSPACE_ROOT,
    )
    if check and result.returncode != 0:
        print(f"Git command failed: git {' '.join(args)}")
        print(f"stderr: {result.stderr}")
    return result


def generate_target_filename(source_path: Path, db_folder: str, prefix: str) -> str:
    """
    Generate the flattened target filename with proper prefix.

    Examples:
    - oracle/pl-sql-to-snowflake-scripting/cursor.md -> oracle-pl-sql-to-snowflake-scripting-cursor.md
    - bigquery/bigquery-create-table.md -> bigquery-create-table.md (already prefixed)
    - hive/ddls/create-view.md -> hive-ddls-create-view.md
    """
    # Get relative path from the db folder
    rel_path = source_path.relative_to(SOURCE_DIR / db_folder)

    # Convert path to flattened filename
    parts = list(rel_path.parts)
    filename = parts[-1]  # The actual filename
    subdirs = parts[:-1]  # Any subdirectories

    # Remove .md extension for processing
    name_without_ext = filename.replace(".md", "")

    # Build the new filename
    if subdirs:
        # Join subdirectories with the filename
        subdir_part = "-".join(subdirs)
        new_name = f"{prefix}{subdir_part}-{name_without_ext}.md"
    else:
        # No subdirectories
        if name_without_ext.lower().startswith(
            db_folder.lower()
        ) or name_without_ext.lower().startswith(prefix.replace("-", "").lower()):
            # Already has prefix (like bigquery-create-table.md)
            new_name = f"{name_without_ext}.md"
        else:
            new_name = f"{prefix}{name_without_ext}.md"

    # Normalize: convert to lowercase and handle special cases
    new_name = new_name.lower()

    return new_name


def find_existing_file(target_dir: Path, target_name: str) -> Path | None:
    """Check if a similar file already exists in the target directory."""
    target_path = target_dir / target_name
    if target_path.exists():
        return target_path

    # Also check for variations (case differences, slight naming differences)
    for existing in target_dir.glob("*.md"):
        if existing.name.lower() == target_name.lower():
            return existing

    return None


def migrate_folder(db_folder: str, dry_run: bool = False) -> tuple[int, int, int]:
    """
    Migrate all files from a source database folder to its target skill folder.

    Returns: (moved_count, deleted_count, skipped_count)
    """
    if db_folder not in FOLDER_MAPPING:
        print(f"Warning: No mapping for folder '{db_folder}'")
        return 0, 0, 0

    target_skill, prefix = FOLDER_MAPPING[db_folder]
    source_folder = SOURCE_DIR / db_folder
    target_dir = SKILLS_DIR / target_skill / "translation-references"

    if not source_folder.exists():
        print(f"Source folder does not exist: {source_folder}")
        return 0, 0, 0

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    moved = 0
    deleted = 0
    skipped = 0

    # Find all .md files in the source folder (recursively)
    for source_file in sorted(source_folder.rglob("*.md")):
        target_name = generate_target_filename(source_file, db_folder, prefix)
        target_path = target_dir / target_name

        # Check if file already exists in target
        existing = find_existing_file(target_dir, target_name)

        if existing:
            # File already exists - delete the source (it's a duplicate)
            print(f"DELETE (duplicate): {source_file.relative_to(SKILLS_DIR)}")
            print(f"  -> Already exists: {existing.relative_to(SKILLS_DIR)}")
            if not dry_run:
                run_git_command(["rm", str(source_file)])
            deleted += 1
        else:
            # Move the file
            print(f"MOVE: {source_file.relative_to(SKILLS_DIR)}")
            print(f"  -> {target_path.relative_to(SKILLS_DIR)}")
            if not dry_run:
                run_git_command(["mv", str(source_file), str(target_path)])
            moved += 1

    return moved, deleted, skipped


def cleanup_empty_dirs(dry_run: bool = False) -> int:
    """Remove empty directories from the source translation-references folder."""
    removed = 0

    # Walk bottom-up to remove empty directories
    for dirpath, _dirnames, _filenames in os.walk(SOURCE_DIR, topdown=False):
        dir_path = Path(dirpath)

        # Skip the root and 'general' folder
        if dir_path == SOURCE_DIR:
            continue
        if dir_path.name == "general" or "general" in dir_path.parts:
            continue

        # Check if directory is empty (no files and no non-empty subdirs)
        try:
            remaining = list(dir_path.iterdir())
            if not remaining:
                print(f"REMOVE DIR: {dir_path.relative_to(SKILLS_DIR)}")
                if not dry_run:
                    dir_path.rmdir()
                removed += 1
        except Exception as e:
            print(f"Error checking {dir_path}: {e}")

    return removed


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Migrate translation reference files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument("--folder", type=str, help="Only migrate a specific folder")
    parser.add_argument(
        "--cleanup", action="store_true", help="Only cleanup empty directories"
    )
    args = parser.parse_args()

    if args.cleanup:
        removed = cleanup_empty_dirs(args.dry_run)
        print(f"\nRemoved {removed} empty directories")
        return

    total_moved = 0
    total_deleted = 0
    total_skipped = 0

    folders_to_process = [args.folder] if args.folder else list(FOLDER_MAPPING.keys())

    for folder in folders_to_process:
        if folder in KEEP_IN_PLACE:
            continue

        print(f"\n{'='*60}")
        print(f"Processing: {folder}")
        print(f"{'='*60}")

        moved, deleted, skipped = migrate_folder(folder, args.dry_run)
        total_moved += moved
        total_deleted += deleted
        total_skipped += skipped

    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Files moved: {total_moved}")
    print(f"  Duplicates deleted: {total_deleted}")
    print(f"  Skipped: {total_skipped}")
    print(f"{'='*60}")

    if args.dry_run:
        print("\n[DRY RUN - no changes made]")


if __name__ == "__main__":
    main()
