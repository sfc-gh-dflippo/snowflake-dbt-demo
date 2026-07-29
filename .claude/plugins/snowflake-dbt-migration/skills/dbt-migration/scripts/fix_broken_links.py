#!/usr/bin/env python3
"""
Fix broken relative links in translation reference markdown files.

Validates all markdown links and converts broken relative links to
external Snowflake documentation URLs.
"""

import re
from pathlib import Path

TARGET_DIR = Path(__file__).parent.parent / "translation-references"

# Base URL for Snowflake documentation
SNOWFLAKE_DOCS_BASE = "https://docs.snowflake.com/en/migrations/snowconvert-docs/"

# Pattern to match markdown links: [text](url)
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def resolve_relative_path(source_file: Path, relative_link: str) -> Path:
    """Resolve a relative link to an absolute path."""
    # Remove any anchor
    path_part = relative_link.split("#")[0]
    if not path_part:
        return source_file  # Same file anchor

    # Resolve relative to source file's directory
    source_dir = source_file.parent
    resolved = (source_dir / path_part).resolve()
    return resolved


def convert_to_snowflake_url(relative_link: str, source_file: Path) -> str:
    """Convert a relative link to a Snowflake documentation URL."""
    # Get the path relative to translation-references
    source_dir = source_file.parent

    # Parse the relative link
    path_part = relative_link.split("#")[0]
    anchor = "#" + relative_link.split("#")[1] if "#" in relative_link else ""

    # Remove .html extension if present (Snowflake docs don't use .html in URLs)
    path_part = path_part.replace(".html", "")

    # Resolve the path
    resolved = (source_dir / path_part).resolve()

    # Try to find the path relative to translation-references
    try:
        rel_to_target = resolved.relative_to(TARGET_DIR.resolve())
        # Build Snowflake URL
        url_path = str(rel_to_target).replace("\\", "/")
        return SNOWFLAKE_DOCS_BASE + "translation-references/" + url_path + anchor
    except ValueError:
        pass

    # Check if it's pointing to general/technical-documentation
    rel_link_str = str(relative_link)
    if "general/technical-documentation" in rel_link_str:
        # Extract the path from general/ onwards
        match = re.search(r"(general/technical-documentation[^#]*)", rel_link_str)
        if match:
            path = match.group(1).replace(".html", "")
            return SNOWFLAKE_DOCS_BASE + path + anchor

    # For other paths, try to construct a reasonable URL
    if "general/" in rel_link_str:
        match = re.search(r"(general/[^#]*)", rel_link_str)
        if match:
            path = match.group(1).replace(".html", "")
            return SNOWFLAKE_DOCS_BASE + path + anchor

    # Fall back to translation-references path construction
    clean_path = re.sub(r"^(\.\./)+", "", rel_link_str)
    clean_path = clean_path.replace(".html", "").split("#")[0]

    return SNOWFLAKE_DOCS_BASE + clean_path + anchor


def is_external_link(url: str) -> bool:
    """Check if a URL is external (http/https)."""
    return url.startswith("http://") or url.startswith("https://")


def is_anchor_only(url: str) -> bool:
    """Check if the link is just an anchor to the same page."""
    return url.startswith("#")


def validate_and_fix_links(file_path: Path) -> tuple[bool, dict]:
    """Validate links in a file and fix broken ones."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, {"error": str(e)}

    original = content
    stats = {"checked": 0, "fixed": 0, "already_valid": 0}

    def fix_link(match):
        text = match.group(1)
        url = match.group(2)
        stats["checked"] += 1

        # Skip external links and anchors
        if is_external_link(url) or is_anchor_only(url):
            stats["already_valid"] += 1
            return match.group(0)

        # Check if the relative link resolves to an existing file
        resolved = resolve_relative_path(file_path, url)

        # Try with .md extension if not found
        if not resolved.exists():
            md_path = resolved.with_suffix(".md")
            if md_path.exists():
                resolved = md_path

        # Try without .html extension
        if not resolved.exists() and ".html" in str(resolved):
            no_html = Path(str(resolved).replace(".html", ""))
            if no_html.exists():
                resolved = no_html
            elif no_html.with_suffix(".md").exists():
                resolved = no_html.with_suffix(".md")

        if resolved.exists():
            stats["already_valid"] += 1
            return match.group(0)

        # Convert to Snowflake URL
        new_url = convert_to_snowflake_url(url, file_path)
        stats["fixed"] += 1
        return f"[{text}]({new_url})"

    content = LINK_PATTERN.sub(fix_link, content)

    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return True, stats

    return False, stats


def main():
    if not TARGET_DIR.exists():
        print(f"Error: {TARGET_DIR} not found")
        return

    md_files = list(TARGET_DIR.rglob("*.md"))
    print(f"Checking {len(md_files)} markdown files for broken links...\n")

    total_stats = {"checked": 0, "fixed": 0, "already_valid": 0}
    modified_files = []

    for file_path in sorted(md_files):
        modified, stats = validate_and_fix_links(file_path)

        for k, v in stats.items():
            if k in total_stats:
                total_stats[k] += v

        if modified and stats.get("fixed", 0) > 0:
            rel_path = file_path.relative_to(TARGET_DIR)
            modified_files.append((rel_path, stats["fixed"]))

    print("Summary:")
    print(f"  Links checked: {total_stats['checked']}")
    print(f"  Already valid: {total_stats['already_valid']}")
    print(f"  Fixed: {total_stats['fixed']}")
    print(f"\nModified {len(modified_files)} files:")

    for rel_path, count in modified_files:
        print(f"  {rel_path}: {count} links fixed")


if __name__ == "__main__":
    main()
