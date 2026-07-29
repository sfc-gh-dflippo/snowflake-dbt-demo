#!/usr/bin/env python3
"""
Clean up migration documentation files by removing boilerplate.

This script processes markdown files in the translation-references folder,
removing navigation elements, footers, and other boilerplate content from
the original Snowflake documentation while preserving the technical content.

Usage:
    python clean_migration_docs.py

The script will:
1. Remove navigation sidebar content
2. Remove footer links and metadata
3. Clean up YAML frontmatter (remove unnecessary fields)
4. Remove "Copy" button placeholders
5. Preserve technical content and code examples
"""

import re
from pathlib import Path

# Get paths relative to script location
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
TARGET_DIR = SKILL_DIR / "translation-references"

# YAML fields to remove from frontmatter
YAML_FIELDS_TO_REMOVE = [
    "keywords",
    "seo",
    "categories",
    "resourceType",
    "source_url",  # Keep this actually, it's useful
]

# Patterns to remove from content
PATTERNS_TO_REMOVE = [
    # Navigation and sidebar
    r"## On this page\n[\s\S]*?(?=\n## [A-Z]|\n# [A-Z]|\Z)",
    r"### In this section\n[\s\S]*?(?=\n## [A-Z]|\n# [A-Z]|\Z)",
    # Footer content
    r"\n---\n\n\*\*Related topics\*\*[\s\S]*$",
    r"\n---\n\nWas this page helpful\?[\s\S]*$",
    r"\nVisit Snowflake[\s\S]*$",
    # Copy button placeholders (after code blocks)
    r"\n\nCopy\n",
    # Link anchor title text that is just noise
    r'\s*"Link to this heading"',
    # Empty sections
    r"\n## \n",
    r"\n### \n",
]

# Patterns to replace (not remove)
PATTERNS_TO_REPLACE = [
    # Standalone "Note" should be formatted as "**Note:**"
    (r"\n\nNote\n\n", r"\n\n**Note:**\n\n"),
]


def clean_yaml_frontmatter(content: str) -> str:
    """Clean up YAML frontmatter by removing unnecessary fields."""

    # Check if file has frontmatter
    if not content.startswith("---"):
        return content

    # Find the end of frontmatter
    end_match = re.search(r"\n---\n", content[3:])
    if not end_match:
        return content

    frontmatter_end = end_match.end() + 3
    frontmatter = content[:frontmatter_end]
    rest = content[frontmatter_end:]

    # Remove specified fields from frontmatter
    for field in YAML_FIELDS_TO_REMOVE:
        # Remove single-line fields
        frontmatter = re.sub(rf"^{field}:.*\n", "", frontmatter, flags=re.MULTILINE)
        # Remove multi-line fields (indented content)
        frontmatter = re.sub(
            rf"^{field}:\n(?:  .*\n)*", "", frontmatter, flags=re.MULTILINE
        )

    return frontmatter + rest


def minimize_table_row(line: str) -> str:
    """Minimize a table row by stripping whitespace from cells."""
    if not line.startswith("|"):
        return line

    # Check if this is a separator row (only |, -, :, and whitespace)
    if re.match(r"^[\|\-\:\s]+$", line):
        parts = [p for p in line.split("|") if p.strip() or p == ""]
        num_cols = len([p for p in parts if p.strip()])
        if num_cols > 0:
            return "|" + "|".join(["---"] * num_cols) + "|"
        return line

    # Regular row - strip whitespace from each cell
    parts = line.split("|")
    minimized_parts = [p.strip() for p in parts]
    return "|".join(minimized_parts)


def clean_content(content: str) -> str:
    """Remove boilerplate patterns from content."""

    for pattern in PATTERNS_TO_REMOVE:
        content = re.sub(pattern, "", content)

    # Apply replacements
    for pattern, replacement in PATTERNS_TO_REPLACE:
        content = re.sub(pattern, replacement, content)

    # Clean up multiple consecutive blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    # Remove trailing whitespace from lines
    content = "\n".join(line.rstrip() for line in content.split("\n"))

    # Minimize tables and add prettier-ignore
    lines = content.split("\n")
    new_lines = []
    in_table = False

    for line in lines:
        if line.startswith("|"):
            if not in_table:
                in_table = True
                # Add prettier-ignore before table if not present
                if new_lines and "<!-- prettier-ignore -->" not in new_lines[-1]:
                    new_lines.append("<!-- prettier-ignore -->")
            new_lines.append(minimize_table_row(line))
        else:
            in_table = False
            new_lines.append(line)

    content = "\n".join(new_lines)

    # Ensure file ends with single newline
    content = content.rstrip() + "\n"

    return content


def process_file(file_path: Path) -> bool:
    """Process a single markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        True if file was modified, False otherwise
    """
    try:
        original_content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  Error reading {file_path}: {e}")
        return False

    # Apply cleaning
    content = clean_yaml_frontmatter(original_content)
    content = clean_content(content)

    # Only write if content changed
    if content != original_content:
        try:
            file_path.write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"  Error writing {file_path}: {e}")
            return False

    return False


def main():
    """Main function to clean all migration documentation."""

    if not TARGET_DIR.exists():
        print(f"Error: Target directory not found: {TARGET_DIR}")
        print("Run copy_migration_docs.py first.")
        return

    print(f"Cleaning files in: {TARGET_DIR}")
    print()

    # Find all markdown files
    md_files = list(TARGET_DIR.rglob("*.md"))

    if not md_files:
        print("No markdown files found.")
        return

    print(f"Found {len(md_files)} markdown files")
    print()

    # Process each file
    modified_count = 0
    for file_path in md_files:
        rel_path = file_path.relative_to(TARGET_DIR)
        if process_file(file_path):
            print(f"  Modified: {rel_path}")
            modified_count += 1

    print()
    print(f"Done! Modified {modified_count} of {len(md_files)} files.")
    print()
    print("Next steps:")
    print("  1. Run clean_skill_descriptions.py to update SKILL.md")
    print("  2. Run pre-commit to format files")


if __name__ == "__main__":
    main()
