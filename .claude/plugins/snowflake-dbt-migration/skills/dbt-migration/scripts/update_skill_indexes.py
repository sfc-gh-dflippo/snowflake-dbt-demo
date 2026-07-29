#!/usr/bin/env python3
"""
Update the Reference Index section in each SKILL.md file with all translation reference files.
"""

import re
from pathlib import Path

# Base paths
SKILLS_DIR = Path(__file__).parent.parent.parent  # .claude/skills/

# Database-specific skills
DB_SKILLS = [
    "dbt-migration-bigquery",
    "dbt-migration-db2",
    "dbt-migration-hive",
    "dbt-migration-ms-sql-server",
    "dbt-migration-oracle",
    "dbt-migration-postgres",
    "dbt-migration-redshift",
    "dbt-migration-sybase",
    "dbt-migration-teradata",
    "dbt-migration-vertica",
]


def format_title(filename: str) -> str:
    """
    Convert filename to a human-readable title.

    Examples:
    - bigquery-create-table.md -> Create Table
    - oracle-pl-sql-to-snowflake-scripting-cursor.md -> PL SQL to Snowflake Scripting - Cursor
    - db2-readme.md -> README
    """
    # Remove .md extension
    name = filename.replace(".md", "")

    # Remove common prefixes (db name)
    for prefix in [
        "bigquery-",
        "db2-",
        "hive-",
        "ms-sql-server-",
        "oracle-",
        "postgres-",
        "postgresql-",
        "redshift-",
        "sybase-",
        "teradata-",
        "vertica-",
        "transact-",
        "ssis-",
    ]:
        if name.lower().startswith(prefix):
            name = name[len(prefix) :]
            break

    # Handle README
    if name.lower() == "readme":
        return "Overview (README)"

    # Handle special patterns
    name = name.replace("-", " ")
    name = name.replace("_", " ")

    # Capitalize words
    words = name.split()
    formatted_words = []
    for word in words:
        # Keep acronyms uppercase
        if word.upper() in [
            "SQL",
            "DDL",
            "DML",
            "BI",
            "ETL",
            "UDF",
            "UDFS",
            "TPT",
            "BTEQ",
            "SSIS",
        ]:
            formatted_words.append(word.upper())
        elif word.upper() in ["PL", "DBC"]:
            formatted_words.append(word.upper())
        else:
            formatted_words.append(word.capitalize())

    return " ".join(formatted_words)


def generate_reference_index(skill_dir: Path) -> str:
    """Generate the reference index markdown for a skill."""
    refs_dir = skill_dir / "translation-references"

    if not refs_dir.exists():
        return "No translation references available."

    files = sorted(refs_dir.glob("*.md"))
    if not files:
        return "No translation references available."

    lines = []
    for f in files:
        title = format_title(f.name)
        rel_path = f"translation-references/{f.name}"
        lines.append(f"- [{title}]({rel_path})")

    return "\n".join(lines)


def update_skill_md(skill_name: str, dry_run: bool = False) -> bool:
    """Update the Reference Index section in a SKILL.md file."""
    skill_dir = SKILLS_DIR / skill_name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        print(f"SKILL.md not found for {skill_name}")
        return False

    content = skill_md.read_text()

    # Generate new reference index
    new_index = generate_reference_index(skill_dir)

    # Pattern to match the Reference Index section
    # Matches from "### Reference Index" to end of file or next ## section
    pattern = r"(### Reference Index\s*\n)(.*?)(\n## |\Z)"

    def replacement(match):
        header = (
            match.group(1).rstrip("\n") + "\n"
        )  # Ensure single newline after header
        next_section = match.group(3)
        return f"{header}\n{new_index}\n{next_section}"

    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count == 0:
        # No Reference Index section found - append it
        print(f"  Warning: No Reference Index section found in {skill_name}")
        # Find the end of the file and append
        if "## Translation References" in content:
            # Add after Translation References section
            pattern = r"(## Translation References.*?)((?:\n## |\Z))"

            def append_replacement(match):
                section = match.group(1)
                next_part = match.group(2)
                return f"{section}\n\n### Reference Index\n\n{new_index}\n{next_part}"

            new_content, count = re.subn(
                pattern, append_replacement, content, flags=re.DOTALL
            )

    if new_content != content:
        print(f"UPDATING: {skill_name}")
        if not dry_run:
            skill_md.write_text(new_content)
        return True
    else:
        print(f"NO CHANGE: {skill_name}")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Update Reference Index in SKILL.md files"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done"
    )
    parser.add_argument("--skill", type=str, help="Update only a specific skill")
    args = parser.parse_args()

    skills = [args.skill] if args.skill else DB_SKILLS

    updated = 0
    for skill in skills:
        if update_skill_md(skill, args.dry_run):
            updated += 1

    print(f"\nUpdated {updated} SKILL.md files")
    if args.dry_run:
        print("[DRY RUN - no changes made]")


if __name__ == "__main__":
    main()
