#!/usr/bin/env python3
"""
Generate the translation reference index tables for SKILL.md.

This script reads all markdown files in translation-references/ and generates
index tables that can be added to SKILL.md. It extracts descriptions from
YAML frontmatter and creates properly formatted markdown tables.

Usage:
    python generate_reference_index.py

Output:
    Prints markdown tables to stdout that can be copied into SKILL.md
"""

import re
from pathlib import Path
from typing import Optional

# Get paths relative to script location
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
TARGET_DIR = SKILL_DIR / "translation-references"


def extract_description(file_path: Path) -> Optional[str]:
    """Extract description from YAML frontmatter.

    Args:
        file_path: Path to markdown file

    Returns:
        Description string or None if not found
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return None

    # Check for frontmatter
    if not content.startswith("---"):
        return None

    # Find frontmatter end
    end_match = re.search(r"\n---\n", content[3:])
    if not end_match:
        return None

    frontmatter = content[3 : end_match.start() + 3]

    # Extract description field
    # Handle multi-line descriptions
    desc_match = re.search(
        r"^description:\s*['\"]?(.*?)['\"]?\s*$|^description:\s*\n((?:  .*\n)*)",
        frontmatter,
        re.MULTILINE,
    )

    if desc_match:
        if desc_match.group(1):
            return desc_match.group(1).strip()
        elif desc_match.group(2):
            # Multi-line description - join lines
            lines = desc_match.group(2).strip().split("\n")
            return " ".join(line.strip().strip("\"'") for line in lines)

    return None


def get_top_level_folders() -> list[str]:
    """Get sorted list of top-level folders in translation-references."""
    if not TARGET_DIR.exists():
        return []

    folders = []
    for item in TARGET_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            folders.append(item.name)

    return sorted(folders)


def generate_compact_index() -> str:
    """Generate compact index with one row per folder (README only)."""

    lines = [
        "### Full Translation Reference Index",
        "",
        "<!-- prettier-ignore -->",
        "|Folder|Description|",
        "|---|---|",
    ]

    for folder in get_top_level_folders():
        readme_path = TARGET_DIR / folder / "README.md"
        if readme_path.exists():
            desc = extract_description(readme_path)
            if desc:
                # Truncate long descriptions
                if len(desc) > 60:
                    desc = desc[:57] + "..."
                link = f"[{desc}](translation-references/{folder}/README.md)"
            else:
                link = f"[{folder.title()}](translation-references/{folder}/README.md)"
        else:
            link = f"{folder.title()}"

        lines.append(f"|{folder}|{link}|")

    return "\n".join(lines)


def generate_expanded_index() -> str:
    """Generate expanded index with one row per file."""

    lines = [
        "### Full Translation Reference Index (Expanded)",
        "",
        "<!-- prettier-ignore -->",
        "|Folder|Description|",
        "|---|---|",
    ]

    for folder in get_top_level_folders():
        folder_path = TARGET_DIR / folder

        # Get all markdown files in this folder and subfolders
        md_files = sorted(folder_path.rglob("*.md"))

        for md_file in md_files:
            rel_path = md_file.relative_to(TARGET_DIR)
            desc = extract_description(md_file)

            if desc:
                # Truncate long descriptions
                if len(desc) > 80:
                    desc = desc[:77] + "..."
                link = f"[{desc}](translation-references/{rel_path})"
            else:
                # Use filename as description
                name = md_file.stem.replace("-", " ").replace("_", " ").title()
                link = f"[{name}](translation-references/{rel_path})"

            lines.append(f"|{folder}|{link}|")

    return "\n".join(lines)


def main():
    """Main function to generate index tables."""

    if not TARGET_DIR.exists():
        print(f"Error: Target directory not found: {TARGET_DIR}")
        print("Run copy_migration_docs.py first.")
        return

    print("=" * 80)
    print("COMPACT INDEX (one row per folder)")
    print("=" * 80)
    print()
    print(generate_compact_index())
    print()
    print()
    print("=" * 80)
    print("EXPANDED INDEX (one row per file)")
    print("=" * 80)
    print()
    print(generate_expanded_index())
    print()
    print()
    print("Copy the desired index format into SKILL.md")


if __name__ == "__main__":
    main()
