#!/usr/bin/env python3
"""
Skills Sync Script - Sync AI agent skills from GitHub repositories using Git.

Supports four skill locations with clear precedence:
1. PROJECT_ROOT/.cortex/skills/ (highest)
2. PROJECT_ROOT/.claude/skills/
3. ~/.cortex/skills/
4. ~/.claude/skills/ (lowest)

Repository skills are extracted to ~/.cortex/skills/ with repo-prefixed names.
Configure repositories in repos.txt in any of the four skill directories.
"""

import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

# Auto-install frontmatter if needed
try:
    import frontmatter
except ImportError:
    print("Installing python-frontmatter...")
    _ = subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--user", "python-frontmatter"]
    )
    import frontmatter


def find_project_root() -> Path:
    """Find project root by walking up from current working directory."""
    current = Path.cwd().resolve()

    # Walk up directory tree
    for _ in range(10):  # Limit depth to prevent infinite loop
        # Check for project root indicators - look for any skills directory or .git
        if (current / ".cortex" / "skills").exists():
            return current
        if (current / ".claude" / "skills").exists():
            return current
        if (current / ".git").exists():
            return current
        if current.parent == current:  # Reached filesystem root
            break
        current = current.parent

    # Fallback to current working directory
    return Path.cwd()


# Configuration
PROJECT_ROOT = find_project_root()

# Four scan locations (in precedence order, highest to lowest)
PROJECT_CORTEX_DIR = PROJECT_ROOT / ".cortex" / "skills"
PROJECT_CLAUDE_DIR = PROJECT_ROOT / ".claude" / "skills"
GLOBAL_CORTEX_DIR = Path.home() / ".snowflake" / "cortex" / "skills"
GLOBAL_CLAUDE_DIR = Path.home() / ".claude" / "skills"

# Repository extraction target (always to global .cortex)
GLOBAL_SKILLS_DIR = GLOBAL_CORTEX_DIR

# Temp clone location
TEMP_CLONE_DIR = Path.home() / ".snowflake" / ".cache" / "repos"

# Skill search paths within repositories
REPO_SKILL_PATHS = [".cortex/skills/*/SKILL.md", ".claude/skills/*/SKILL.md"]

AGENTS_MD = PROJECT_ROOT / "AGENTS.md"
MARKERS = (
    "<!-- BEGIN AUTO-GENERATED SKILLS - DO NOT EDIT MANUALLY -->",
    "<!-- END AUTO-GENERATED SKILLS - DO NOT EDIT MANUALLY -->",
)


def check_git_installed() -> bool:
    """Check if git CLI is available."""
    try:
        _ = subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Git is not installed. Please install Git.")
        sys.exit(1)


def read_repo_list() -> list[str]:
    """Read repository URLs from repos.txt files in all four locations.

    Checks in precedence order, deduplicates URLs, maintains order.

    Locations checked:
    1. PROJECT_ROOT/.cortex/skills/repos.txt
    2. PROJECT_ROOT/.claude/skills/repos.txt
    3. ~/.cortex/skills/repos.txt
    4. ~/.claude/skills/repos.txt

    Returns:
        Deduplicated list of repository URLs
    """
    all_repos: list[str] = []
    seen_urls: set[str] = set()

    # Check all four locations in precedence order
    repos_files = [
        PROJECT_CORTEX_DIR / "repos.txt",
        PROJECT_CLAUDE_DIR / "repos.txt",
        GLOBAL_CORTEX_DIR / "repos.txt",
        GLOBAL_CLAUDE_DIR / "repos.txt",
    ]

    found_any = False
    for repos_file in repos_files:
        if repos_file.exists():
            found_any = True
            print(f"  Reading {repos_file}")
            for line in repos_file.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    # Normalize URL for comparison (remove trailing .git, slashes)
                    normalized = line.rstrip("/").removesuffix(".git")
                    if normalized not in seen_urls:
                        seen_urls.add(normalized)
                        all_repos.append(line)  # Keep original format

    # If no repos.txt found anywhere, create default in project .cortex
    if not found_any:
        print("  No repos.txt found, creating default...")
        default_file = PROJECT_CORTEX_DIR / "repos.txt"
        default_file.parent.mkdir(parents=True, exist_ok=True)
        default_file.write_text("https://github.com/anthropics/skills\n")
        all_repos.append("https://github.com/anthropics/skills")

    return all_repos


def get_repo_short_name(url: str) -> str:
    """Extract just the repo name from URL (e.g., 'snowflake-dbt-demo').

    Args:
        url: Git repository URL (e.g., 'https://github.com/user/repo.git')

    Returns:
        Short repo name (e.g., 'repo')
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").replace(".git", "").split("/")
    return path_parts[-1]  # Just last part: 'snowflake-dbt-demo'


def extract_skills_from_repo(
    repo_path: Path, repo_short_name: str, target_dir: Path
) -> list[str]:
    """Extract skills ONLY from .cortex/skills/* and .claude/skills/* in cloned repo.

    Copy each skill directory to target_dir with prefix: {repo_short_name}-{skill_name}/

    Args:
        repo_path: Path to cloned repository
        repo_short_name: Short repo name (e.g., 'anthropics-skills')
        target_dir: Destination directory (~/.cortex/skills/)

    Returns:
        List of extracted skill names (without prefix)
    """
    extracted: list[str] = []

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Search only in .cortex/skills/*/SKILL.md and .claude/skills/*/SKILL.md
    for search_pattern in REPO_SKILL_PATHS:
        for skill_md in repo_path.glob(search_pattern):
            # skill_md is like: repo/.cortex/skills/my-skill/SKILL.md
            skill_dir = skill_md.parent  # my-skill/
            skill_name = skill_dir.name

            # Target: ~/.cortex/skills/anthropics-skills-my-skill/
            target_skill_dir = target_dir / f"{repo_short_name}-{skill_name}"

            # Copy entire skill directory, overwrite if exists
            if target_skill_dir.exists():
                shutil.rmtree(target_skill_dir)
            shutil.copytree(skill_dir, target_skill_dir)

            extracted.append(skill_name)

    return extracted


def get_current_commit(repo_path: Path) -> str | None:
    """Get current commit hash of a Git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None


def sync_repo_to_global(
    url: str, global_dir: Path, temp_dir: Path
) -> tuple[bool, list[str]]:
    """Clone repo to temp location, extract skills to global dir with prefix.

    Always overwrites existing global skills.

    Args:
        url: Git repository URL
        global_dir: Target directory for extracted skills (~/.cortex/skills/)
        temp_dir: Directory for temporary clones (~/.cortex/.cache/repos/)

    Returns:
        tuple: (changed, list of skill names extracted)
    """
    repo_short_name = get_repo_short_name(url)
    temp_repo_path = temp_dir / repo_short_name

    # Ensure temp directory exists
    temp_dir.mkdir(parents=True, exist_ok=True)

    if temp_repo_path.exists() and (temp_repo_path / ".git").exists():
        # Repo exists in temp, check for changes
        old_commit = get_current_commit(temp_repo_path)

        # Pull latest
        try:
            _ = subprocess.run(
                ["git", "pull", "--quiet"],
                cwd=temp_repo_path,
                check=True,
                capture_output=True,
                timeout=120,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            # Pull failed, try fresh clone
            shutil.rmtree(temp_repo_path, ignore_errors=True)
            _ = subprocess.run(
                ["git", "clone", "--depth", "1", url, str(temp_repo_path)],
                check=True,
                capture_output=True,
                timeout=120,
            )

        new_commit = get_current_commit(temp_repo_path)
        changed = old_commit != new_commit

        if changed and old_commit and new_commit:
            print(f"    Updated: {old_commit[:7]} → {new_commit[:7]}")
        else:
            print(
                f"    No changes (commit: {new_commit[:7] if new_commit else 'unknown'})"
            )
    else:
        # Clone new repo
        if temp_repo_path.exists():
            shutil.rmtree(temp_repo_path, ignore_errors=True)
        _ = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(temp_repo_path)],
            check=True,
            capture_output=True,
            timeout=120,
        )
        commit = get_current_commit(temp_repo_path)
        if commit:
            print(f"    Cloned: {commit[:7]}")
        changed = True

    # Extract skills from repo (always overwrite)
    extracted_skills = extract_skills_from_repo(
        temp_repo_path, repo_short_name, global_dir
    )

    return changed, extracted_skills


def scan_skills() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    """Scan for skills in four locations with precedence order.

    Locations (highest to lowest precedence):
    1. PROJECT_ROOT/.cortex/skills/
    2. PROJECT_ROOT/.claude/skills/
    3. ~/.cortex/skills/
    4. ~/.claude/skills/

    Skills in higher precedence locations override those with same name in lower.

    Returns:
        tuple: (project_skills, global_skills) where duplicates are already resolved
    """
    project_skills: dict[str, dict[str, str]] = {}
    global_skills: dict[str, dict[str, str]] = {}

    # Track all seen skill names for precedence handling
    all_seen_names: set[str] = set()

    # Scan in reverse precedence order, so higher precedence overwrites
    scan_locations = [
        (GLOBAL_CLAUDE_DIR, "global", "~/.claude/skills"),
        (GLOBAL_CORTEX_DIR, "global", "~/.cortex/skills"),
        (PROJECT_CLAUDE_DIR, "project", ".claude/skills"),
        (PROJECT_CORTEX_DIR, "project", ".cortex/skills"),
    ]

    for location, location_type, location_display in scan_locations:
        if not location.exists():
            continue

        try:
            # Only scan immediate children (flat structure)
            for skill_dir in location.iterdir():
                if not skill_dir.is_dir():
                    continue

                # Skip special directories
                if skill_dir.name in [".cache", "repositories", ".git"]:
                    continue

                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    continue

                try:
                    # Parse frontmatter
                    post = frontmatter.load(str(skill_md))
                    name = post.get("name", "")
                    description = post.get("description", "")

                    # Ensure we have strings
                    if not isinstance(name, str) or not isinstance(description, str):
                        continue
                    if not (name and description):
                        continue

                    # Compute path for display
                    if location_type == "project":
                        # Project paths are relative to PROJECT_ROOT
                        rel_path = skill_md.relative_to(PROJECT_ROOT)
                        display_path = str(rel_path)
                    else:
                        # Global paths use file:// URI
                        display_path = skill_md.as_uri()

                    skill_info = {
                        "name": name,
                        "path": display_path,
                        "description": description,
                        "source": location_display,
                    }

                    # Add to appropriate dict, overwriting lower precedence
                    if location_type == "project":
                        project_skills[name] = skill_info
                        all_seen_names.add(name)
                    else:
                        # Only add to global if not already in project
                        if name not in all_seen_names:
                            global_skills[name] = skill_info
                            all_seen_names.add(name)

                except Exception as e:
                    print(f"  Warning: Failed to parse {skill_md}: {e}")
        except (PermissionError, OSError) as e:
            print(f"  Warning: Could not scan {location}: {e}")

    return project_skills, global_skills


def format_skills_section(
    project_skills: dict[str, dict[str, str]],
    global_skills: dict[str, dict[str, str]],
) -> str:
    """Format skills for AGENTS.md with Project/Global grouping.

    Args:
        project_skills: Skills from PROJECT_ROOT/.cortex/skills and .claude/skills
        global_skills: Skills from ~/.cortex/skills and ~/.claude/skills

    Returns:
        Formatted markdown string for AGENTS.md
    """
    output: list[str] = []
    output.append("## Skills\n\n")
    output.append(
        "This project uses the **sync-skills.py** script to automatically sync "
        "skills from local directories and remote Git repositories.\n\n"
    )
    output.append("**What are Skills?**\n\n")
    output.append(
        "Skills are structured instruction sets that enhance AI assistant "
        "capabilities for specific domains or tasks. "
        "Each skill is a folder containing:\n\n"
    )
    output.append("- **SKILL.md** - Core instructions and guidelines\n")
    output.append("- **references/** - Detailed documentation and examples\n")
    output.append("- **scripts/** - Helper scripts and templates\n")
    output.append("- **config/** - Configuration files\n\n")
    output.append(
        "Skills provide domain-specific knowledge, best practices, "
        "code templates, and troubleshooting strategies. "
        'Think of them as specialized "expert personas" for areas like '
        "dbt development, Snowflake operations, or testing frameworks.\n\n"
    )
    output.append("**Key Features:**\n\n")
    output.append("- Skills can be enabled `[x]` or disabled `[ ]` individually\n")
    output.append(
        "- Repository skills are prefixed with repo name (e.g., `skills-dbt-core`)\n\n"
    )
    output.append("**Available Skills:**\n\n")

    # Project skills first (from .cortex/skills and .claude/skills in project)
    if project_skills:
        output.append("### Project Skills\n\n")
        for name in sorted(project_skills.keys()):
            skill = project_skills[name]
            output.append(
                f"- [x] **[{name}]({skill['path']})** - {skill['description']}\n"
            )
        output.append("\n")

    # Global skills (from ~/.cortex/skills and ~/.claude/skills)
    if global_skills:
        output.append("### Global Skills\n\n")
        for name in sorted(global_skills.keys()):
            skill = global_skills[name]
            output.append(
                f"- [x] **[{name}]({skill['path']})** - {skill['description']}\n"
            )
        output.append("\n")

    # Remove trailing newline to avoid double blank line before closing marker
    result = "".join(output)
    if result.endswith("\n\n"):
        result = result[:-1]
    return result


def update_agents_md(content: str) -> None:
    """Update AGENTS.md between markers."""
    if not AGENTS_MD.exists():
        # Create basic AGENTS.md
        template = "# AI Agent Configuration\n\nContext and guidelines for AI coding agents.\n\n"
        _ = AGENTS_MD.write_text(template)

    agents_content = AGENTS_MD.read_text()
    start_marker, end_marker = MARKERS

    # Remove old MCP SKILLS section entirely if it exists
    old_mcp_start = "<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->"
    old_mcp_end = "<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->"

    old_start_idx = agents_content.find(old_mcp_start)
    old_end_idx = agents_content.find(old_mcp_end)

    if old_start_idx != -1 and old_end_idx != -1:
        # Remove the entire old MCP section including markers
        before_old = agents_content[:old_start_idx].rstrip()
        after_old = agents_content[old_end_idx + len(old_mcp_end) :].lstrip()
        agents_content = (
            before_old + "\n\n" + after_old if after_old else before_old + "\n"
        )
        print("  Removed old MCP SKILLS section")

    start_idx = agents_content.find(start_marker)
    end_idx = agents_content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        # Append at end
        if not agents_content.endswith("\n"):
            agents_content += "\n"
        new_content = f"\n{start_marker}\n{content}\n{end_marker}\n"
        _ = AGENTS_MD.write_text(agents_content + new_content)
    else:
        # Replace between markers
        before = agents_content[: start_idx + len(start_marker)]
        after = agents_content[end_idx:]
        new_content = f"{before}\n{content}\n{after}"
        _ = AGENTS_MD.write_text(new_content)


def migrate_existing_skills() -> None:
    """One-time migration: extract skills from existing nested .claude/skills/repositories/ structure.

    Migrates to new flat structure in ~/.cortex/skills/ with repo prefixes.
    Run only if old structure exists.
    """
    old_dir = PROJECT_CLAUDE_DIR / "repositories"
    if not old_dir.exists():
        return

    print("\nDetected old skills structure, migrating...")
    migrated = 0

    # Find all SKILL.md files in old structure
    for skill_md in old_dir.rglob("SKILL.md"):
        # Parse to get skill name
        try:
            post = frontmatter.load(str(skill_md))
            skill_name = post.get("name", "")
            if not skill_name:
                continue

            # Derive repo name from path structure
            # Path like: .claude/skills/repositories/github-com/anthropics-skills/skills/dbt-core/SKILL.md
            rel_parts = skill_md.relative_to(old_dir).parts
            if len(rel_parts) >= 2:
                repo_name = rel_parts[1]  # e.g., 'anthropics-skills'
                skill_dir = skill_md.parent

                # Target: ~/.cortex/skills/anthropics-skills-dbt-core/
                target_dir = GLOBAL_CORTEX_DIR / f"{repo_name}-{skill_name}"
                target_dir.parent.mkdir(parents=True, exist_ok=True)

                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.copytree(skill_dir, target_dir)
                migrated += 1
                print(f"  Migrated: {repo_name}-{skill_name}")

        except Exception as e:
            print(f"  Warning: Failed to migrate {skill_md}: {e}")

    if migrated > 0:
        print(f"  Migrated {migrated} skills to ~/.cortex/skills/")
        print("  Old structure will be cleaned up at the end of sync")


def cleanup_old_repositories() -> None:
    """Remove old nested repository structures after successful sync.

    Checks both .cortex/skills/repositories and .claude/skills/repositories.
    """
    old_dirs = [
        PROJECT_CORTEX_DIR / "repositories",
        PROJECT_CLAUDE_DIR / "repositories",
    ]

    cleaned = False
    for old_dir in old_dirs:
        if old_dir.exists() and old_dir.is_dir():
            try:
                rel_path = old_dir.relative_to(PROJECT_ROOT)
                print(f"\nCleaning up old structure: {rel_path}")
                shutil.rmtree(old_dir)
                cleaned = True
                print("  ✓ Removed old repository structure")
            except Exception as e:
                print(f"  Warning: Could not remove {old_dir}: {e}")

    if not cleaned:
        # No old structures found, which is fine
        pass


def main() -> None:
    """Main execution with four-location scanning and multi-location repos.txt support."""
    _ = check_git_installed()

    # 1. Check for migration needed
    migrate_existing_skills()

    # 2. Read repos.txt from all four locations (deduplicated)
    print("Reading repository configuration from all locations...")
    repos = read_repo_list()
    print(f"Configured repositories: {len(repos)} (deduplicated)")

    # 3. Sync each repo to temp, extract to ~/.cortex/skills/
    if repos:
        print(f"\nSyncing repositories to {GLOBAL_SKILLS_DIR}...")
        for url in repos:
            repo_short_name = get_repo_short_name(url)
            print(f"  {repo_short_name}:")

            try:
                changed, extracted_skills = sync_repo_to_global(
                    url, GLOBAL_SKILLS_DIR, TEMP_CLONE_DIR
                )

                print(f"    Extracted {len(extracted_skills)} skill(s)")
            except subprocess.TimeoutExpired:
                print("    Error: Git operation timed out (network issue?)")
            except subprocess.CalledProcessError as e:
                print(f"    Error: Failed to sync repository: {e}")
            except Exception as e:
                print(f"    Error: {e}")

    # 4. Scan four locations with precedence
    print("\nScanning skills from four locations...")
    print(f"  1. {PROJECT_CORTEX_DIR} (project .cortex)")
    print(f"  2. {PROJECT_CLAUDE_DIR} (project .claude)")
    print(f"  3. {GLOBAL_CORTEX_DIR} (global .cortex)")
    print(f"  4. {GLOBAL_CLAUDE_DIR} (global .claude)")

    project_skills, global_skills = scan_skills()

    print(f"\n  Found {len(project_skills)} project skill(s)")
    print(f"  Found {len(global_skills)} global skill(s)")

    # 5. Update AGENTS.md
    print("\nUpdating AGENTS.md...")
    content = format_skills_section(project_skills, global_skills)
    update_agents_md(content)

    # 6. Cleanup old repository structures
    cleanup_old_repositories()

    # 7. Report summary
    total = len(project_skills) + len(global_skills)
    print(f"\n✓ Synced {total} total skills to AGENTS.md")
    print(f"  ({len(project_skills)} project, {len(global_skills)} global)")


if __name__ == "__main__":
    main()
