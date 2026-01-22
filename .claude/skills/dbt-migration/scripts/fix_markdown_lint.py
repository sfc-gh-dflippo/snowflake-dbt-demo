#!/usr/bin/env python3
"""
Fix markdown lint issues in translation reference files.

Fixes:
- MD040: Add 'sql' language to fenced code blocks
- MD051: Remove invalid anchor links [¶](#...)
- MD024: Make duplicate headings unique
- MD036: Convert emphasis-as-heading to proper headings
- Uses Prettier for line wrapping and general formatting
"""

import re
import subprocess
import sys
from pathlib import Path


def fix_fenced_code_blocks(content: str) -> str:
    """Add 'sql' language specifier to plain fenced code blocks."""
    lines = content.split("\n")
    result = []
    in_code_block = False

    for line in lines:
        if line.strip() == "```":
            if not in_code_block:
                # Opening code block - add sql
                result.append("```sql")
                in_code_block = True
            else:
                # Closing code block - keep as is
                result.append("```")
                in_code_block = False
        elif line.startswith("```") and not in_code_block:
            # Already has a language specifier
            result.append(line)
            in_code_block = True
        else:
            result.append(line)

    return "\n".join(result)


def fix_anchor_links(content: str) -> str:
    """Remove invalid anchor links like [¶](#id1) or [¶](#section-name)."""
    content = re.sub(r"\[¶\]\(#[^)]*\)", "", content)
    return content


def fix_trailing_punctuation(content: str) -> str:
    """Remove trailing punctuation from headings (MD026)."""
    lines = content.split("\n")
    result = []

    for line in lines:
        heading_match = re.match(r"^(#{1,6}\s+.+?)([.:;,!?])$", line)
        if heading_match:
            result.append(heading_match.group(1))
        else:
            result.append(line)

    return "\n".join(result)


def fix_inline_html(content: str) -> str:
    """Escape inline HTML that looks like generic types (MD033)."""
    # Replace <T>, <number>, <expr>, <type> etc. with escaped versions
    # But not inside code blocks
    lines = content.split("\n")
    result = []
    in_code_block = False

    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if not in_code_block:
            # Replace <word> patterns that look like HTML tags
            line = re.sub(r"<(\w+)>", r"`<\1>`", line)

        result.append(line)

    return "\n".join(result)


def fix_hard_tabs(content: str) -> str:
    """Convert hard tabs to spaces (MD010)."""
    return content.replace("\t", "    ")


def fix_no_space_after_hash(content: str) -> str:
    """Add space after hash in headings (MD018)."""
    lines = content.split("\n")
    result = []

    for line in lines:
        # Match heading without space after hash
        match = re.match(r"^(#{1,6})([^#\s])", line)
        if match:
            result.append(
                f"{match.group(1)} {match.group(2)}{line[len(match.group(0)):]}"
            )
        else:
            result.append(line)

    return "\n".join(result)


def fix_blanks_around_headings(content: str) -> str:
    """Ensure blank lines around headings (MD022)."""
    lines = content.split("\n")
    result = []
    prev_was_blank = True
    prev_was_heading = False
    in_code_block = False
    in_frontmatter = False

    for i, line in enumerate(lines):
        # Track frontmatter
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            result.append(line)
            prev_was_blank = False
            prev_was_heading = False
            continue
        if in_frontmatter:
            if line.strip() == "---":
                in_frontmatter = False
            result.append(line)
            prev_was_blank = False
            prev_was_heading = False
            continue

        # Track code blocks
        if line.startswith("```"):
            in_code_block = not in_code_block

        is_heading = not in_code_block and re.match(r"^#{1,6}\s", line)
        is_blank = line.strip() == ""

        if is_heading and not prev_was_blank:
            # Add blank line before heading
            result.append("")

        result.append(line)

        if prev_was_heading and not is_blank and not is_heading:
            # Previous was heading and this is content, check if we need blank after heading
            # Actually, we need to insert blank between heading and this line
            # Revisit: insert blank after heading in previous iteration logic
            pass

        prev_was_blank = is_blank
        prev_was_heading = is_heading

    return "\n".join(result)


def fix_multiple_h1(content: str) -> str:
    """Convert H1 to H2 if frontmatter has a title (MD025)."""
    lines = content.split("\n")
    result = []
    has_frontmatter_title = False
    in_frontmatter = False

    # First pass: check if frontmatter has a title
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line.strip() == "---":
                break
            if line.startswith("title:"):
                has_frontmatter_title = True
                break

    # Second pass: convert H1 to H2 if frontmatter has title
    in_frontmatter = False
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            result.append(line)
            continue
        if in_frontmatter and line.strip() == "---":
            in_frontmatter = False
            result.append(line)
            continue
        if in_frontmatter:
            result.append(line)
            continue

        # Convert H1 to H2 if frontmatter has title
        if (
            has_frontmatter_title
            and line.startswith("# ")
            and not line.startswith("## ")
        ):
            result.append("#" + line)
        else:
            result.append(line)

    return "\n".join(result)


def fix_duplicate_headings(content: str) -> str:
    """Make duplicate headings unique by adding sequential numbers."""
    lines = content.split("\n")
    result = []
    heading_counts = {}

    for line in lines:
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            key = heading_text.lower()

            if key in heading_counts:
                heading_counts[key] += 1
                count = heading_counts[key]
                new_heading = f"{heading_text} {count}"
                result.append(f"{'#' * level} {new_heading}")
            else:
                heading_counts[key] = 1
                result.append(line)
        else:
            result.append(line)

    return "\n".join(result)


def fix_emphasis_as_heading(content: str) -> str:
    """Convert emphasis-as-heading patterns to proper headings."""
    lines = content.split("\n")
    result = []
    current_level = 2

    for line in lines:
        heading_match = re.match(r"^(#{1,6})\s+", line)
        if heading_match:
            current_level = len(heading_match.group(1))
            result.append(line)
            continue

        # Pattern: **1. Some text** (numbered)
        match = re.match(r"^\*\*(\d+\.\s*.+)\*\*$", line.strip())
        if match:
            new_level = min(current_level + 1, 6)
            result.append(f"{'#' * new_level} {match.group(1)}")
            continue

        # Pattern: **Some text** (standalone bold as heading)
        match = re.match(r"^\*\*([^*]+)\*\*$", line.strip())
        if match:
            # Only convert if it looks like a heading (short, no punctuation at end except colon)
            text = match.group(1).strip()
            if len(text) < 50 and not text.endswith((".", ",", ";", "!")):
                new_level = min(current_level + 1, 6)
                # Remove trailing colon if present
                if text.endswith(":"):
                    text = text[:-1]
                result.append(f"{'#' * new_level} {text}")
                continue

        result.append(line)

    return "\n".join(result)


def run_prettier(filepath: Path) -> bool:
    """Run Prettier to format the markdown file."""
    try:
        result = subprocess.run(
            [
                "npx",
                "prettier",
                "--write",
                "--prose-wrap",
                "always",
                "--print-width",
                "80",
                str(filepath),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Prettier error on {filepath}: {e}")
        return False


def fix_file(filepath: Path, dry_run: bool = False) -> tuple[bool, list]:
    """Fix all markdown lint issues in a file."""
    content = filepath.read_text()
    original = content

    # Apply manual fixes
    content = fix_fenced_code_blocks(content)
    content = fix_anchor_links(content)
    content = fix_trailing_punctuation(content)
    content = fix_hard_tabs(content)
    content = fix_no_space_after_hash(content)
    content = fix_blanks_around_headings(content)
    content = fix_inline_html(content)
    content = fix_multiple_h1(content)
    content = fix_emphasis_as_heading(content)
    content = fix_duplicate_headings(content)

    # Clean up double blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    changed = content != original

    if not dry_run:
        filepath.write_text(content)

    return changed, []


def run_prettier_batch(files: list[Path]) -> bool:
    """Run Prettier on multiple files at once."""
    if not files:
        return True
    try:
        result = subprocess.run(
            [
                "npx",
                "prettier",
                "--write",
                "--prose-wrap",
                "always",
                "--print-width",
                "80",
            ]
            + [str(f) for f in files],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Prettier error: {e}")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fix markdown lint issues")
    parser.add_argument("files", nargs="*", help="Files to fix")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done"
    )
    parser.add_argument(
        "--all", action="store_true", help="Fix all translation reference files"
    )
    parser.add_argument(
        "--no-prettier", action="store_true", help="Skip Prettier formatting"
    )
    args = parser.parse_args()

    if args.all:
        skills_dir = Path(__file__).parent.parent.parent
        files = list(skills_dir.glob("dbt-migration-*/translation-references/*.md"))
    elif args.files:
        files = [Path(f) for f in args.files]
    else:
        print("Specify files or use --all")
        sys.exit(1)

    fixed = 0
    for filepath in sorted(files):
        changed, _ = fix_file(filepath, args.dry_run)
        if changed:
            print(f"{'WOULD FIX' if args.dry_run else 'FIXED'}: {filepath.name}")
            fixed += 1
        else:
            print(f"NO CHANGE: {filepath.name}")

    # Run Prettier on all files at once
    if not args.dry_run and not args.no_prettier:
        print(f"\nRunning Prettier on {len(files)} files...")
        run_prettier_batch(files)

    print(f"\n{'Would fix' if args.dry_run else 'Processed'} {len(files)} files")


if __name__ == "__main__":
    main()
