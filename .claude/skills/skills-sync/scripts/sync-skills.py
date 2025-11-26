#!/usr/bin/env python3
"""
Skills Sync Script - Sync AI agent skills from GitHub repositories using Git.
Uses git clone/pull for efficiency. Local SKILL.md files take precedence.
Configure repositories in .claude/skills/repos.txt (created automatically).
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
    """Find project root by walking up from script location."""
    current = Path(__file__).parent.resolve()

    # Walk up directory tree
    for _ in range(10):  # Limit depth to prevent infinite loop
        # Check for project root indicators
        if (current / ".claude" / "skills" / "repos.txt").exists():
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
SKILLS_DIR = PROJECT_ROOT / ".claude" / "skills" / "repositories"
CONFIG_FILE = PROJECT_ROOT / ".claude" / "skills" / "repos.txt"
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
    """Read repository URLs from config file."""
    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        _ = CONFIG_FILE.write_text("https://github.com/anthropics/skills\n")

    return [
        line.strip()
        for line in CONFIG_FILE.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]


def url_to_repo_name(url: str) -> str:
    """Convert GitHub URL to directory-safe name."""
    parsed = urlparse(url)
    hostname = (parsed.hostname or "unknown").replace(".", "-")
    path_parts = parsed.path.strip("/").replace(".git", "").split("/")
    return f"{hostname}/{'-'.join(path_parts)}"


def get_current_commit(repo_path: Path) -> str | None:
    """Get current commit hash of a Git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def clone_or_pull_repo(url: str, target_path: Path) -> tuple[bool, str | None]:
    """Clone repo if new, or pull if exists. Returns (changed, commit_hash)."""
    if target_path.exists() and (target_path / ".git").exists():
        # Repo exists, check for changes
        old_commit = get_current_commit(target_path)

        # Pull latest
        _ = subprocess.run(
            ["git", "pull", "--quiet"], cwd=target_path, check=True, capture_output=True
        )

        new_commit = get_current_commit(target_path)
        changed = old_commit != new_commit

        if changed and old_commit and new_commit:
            print(f"  Updated: {old_commit[:7]} → {new_commit[:7]}")
        else:
            print("  No changes")

        return changed, new_commit
    else:
        # Clone new repo
        target_path.parent.mkdir(parents=True, exist_ok=True)
        _ = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(target_path)],
            check=True,
            capture_output=True,
        )
        commit = get_current_commit(target_path)
        if commit:
            print(f"  Cloned: {commit[:7]}")
        return True, commit


def scan_all_skills(
    project_root: Path, repo_paths: dict[str, Path]
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    """Scan entire project for SKILL.md files, classifying by location.

    Skills found in .claude/skills/repositories/ are classified as repository skills.
    Skills found anywhere else are classified as local skills.

    Returns:
        tuple: (local_skills, repo_skills) dictionaries
    """
    local_skills: dict[str, dict[str, str]] = {}
    repo_skills: dict[str, dict[str, str]] = {}
    repositories_dir = SKILLS_DIR

    for skill_path in project_root.rglob("SKILL.md"):
        # Skip common directories that should never contain skills
        if any(
            part in ["node_modules", ".git", "venv", "__pycache__"] for part in skill_path.parts
        ):
            continue

        try:
            post = frontmatter.load(str(skill_path))
            name_val = post.get("name", "")
            description_val = post.get("description", "")

            # Ensure we have strings
            if not isinstance(name_val, str) or not isinstance(description_val, str):
                continue
            if not (name_val and description_val):
                continue

            rel_path = skill_path.relative_to(project_root)

            # Check if this skill is inside .claude/skills/repositories/
            try:
                _ = skill_path.relative_to(repositories_dir)
                # It's inside repositories dir - find which repo
                repo_name = None
                for rname, rpath in repo_paths.items():
                    try:
                        _ = skill_path.relative_to(rpath)
                        repo_name = rname
                        break
                    except ValueError:
                        continue

                if repo_name:
                    repo_skills[name_val] = {
                        "name": name_val,
                        "path": str(rel_path),
                        "description": description_val,
                        "source": repo_name,
                    }
            except ValueError:
                # Not in repositories dir - it's a local skill
                local_skills[name_val] = {
                    "name": name_val,
                    "path": str(rel_path),
                    "description": description_val,
                    "source": "local",
                }
        except Exception as e:
            print(f"Warning: Failed to parse {skill_path}: {e}")

    return local_skills, repo_skills


def format_skills_section(
    local_skills: dict[str, dict[str, str]],
    repo_skills_by_name: dict[str, dict[str, str]],
) -> str:
    """Format skills for AGENTS.md with local priority and grouping."""
    output: list[str] = []
    output.append("## Skills\n\n")
    output.append(
        "This project uses the **sync-skills.py** script to automatically sync both local SKILL.md files and skills from remote Git repositories.\n\n"
    )
    output.append("**What are Skills?**\n\n")
    output.append(
        "Skills are structured instruction sets that enhance AI assistant "
        + "capabilities for specific domains or tasks. "
        + "Each skill is a folder containing:\n\n"
    )
    output.append("- **SKILL.md** - Core instructions and guidelines\n")
    output.append("- **references/** - Detailed documentation and examples\n")
    output.append("- **scripts/** - Helper scripts and templates\n")
    output.append("- **config/** - Configuration files\n\n")
    output.append(
        "Skills provide domain-specific knowledge, best practices, "
        + "code templates, and troubleshooting strategies. "
        + 'Think of them as specialized "expert personas" for areas like '
        + "dbt development, Snowflake operations, or testing frameworks.\n\n"
    )
    output.append("**Key Features:**\n\n")
    output.append("- Skills can be enabled `[x]` or disabled `[ ]` individually\n\n")
    output.append("**Available Skills:**\n\n")

    # Local skills first
    if local_skills:
        output.append("### Local Skills\n\n")
        for name in sorted(local_skills.keys()):
            skill = local_skills[name]
            output.append(f"- [x] **[{name}]({skill['path']})** - {skill['description']}\n")
        output.append("\n")

    # Group repo skills by source
    repo_groups: dict[str, dict[str, dict[str, str]]] = {}
    for name, skill in repo_skills_by_name.items():
        if name not in local_skills:  # Skip if overridden by local
            source = skill["source"]
            if source not in repo_groups:
                repo_groups[source] = {}
            repo_groups[source][name] = skill

    for repo_name in sorted(repo_groups.keys()):
        output.append(f"### {repo_name}\n\n")
        for name in sorted(repo_groups[repo_name].keys()):
            skill = repo_groups[repo_name][name]
            output.append(f"- [x] **[{name}]({skill['path']})** - {skill['description']}\n")
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

    # Check for old MCP markers and replace them with new markers
    old_markers = (
        "<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->",
        "<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->",
    )
    old_start_marker, old_end_marker = old_markers

    # Replace old markers with new ones if found
    if old_start_marker in agents_content:
        agents_content = agents_content.replace(old_start_marker, start_marker)
    if old_end_marker in agents_content:
        agents_content = agents_content.replace(old_end_marker, end_marker)

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


def cleanup_non_skill_folders(repo_paths: dict[str, Path]) -> None:
    """Remove all files and folders from cloned repositories except .git and skill directory trees."""
    for repo_name, repo_path in repo_paths.items():
        if not repo_path.exists():
            continue

        # Collect all directories that directly contain SKILL.md
        skill_containing_dirs = set()
        try:
            for skill_file in repo_path.rglob("SKILL.md"):
                skill_containing_dirs.add(skill_file.parent)
        except (PermissionError, OSError):
            continue

        removed_count = 0

        def contains_skill(dir_path: Path) -> bool:
            """Check if directory or any subdirectory contains SKILL.md."""
            return any(skill_dir.is_relative_to(dir_path) for skill_dir in skill_containing_dirs)

        def is_within_skill_dir(item_path: Path) -> bool:
            """Check if path is within a skill directory (at or below SKILL.md level)."""
            try:
                for skill_dir in skill_containing_dirs:
                    if item_path.is_relative_to(skill_dir):
                        return True
            except ValueError:
                pass
            return False

        def cleanup_directory(dir_path: Path) -> None:
            """Recursively clean up a directory."""
            nonlocal removed_count

            try:
                for item in dir_path.iterdir():
                    # Always skip .git folder
                    if item.name == ".git":
                        continue

                    # If item is within a skill directory, keep it entirely
                    if is_within_skill_dir(item):
                        continue

                    if item.is_file():
                        # File is not in a skill directory, remove it
                        try:
                            item.unlink()
                            removed_count += 1
                        except (PermissionError, OSError) as e:
                            print(f"    Warning: Could not remove {item.relative_to(repo_path)}: {e}")
                    elif item.is_dir():
                        # Check if this subdirectory contains any SKILL.md files
                        if contains_skill(item):
                            # This directory has skills below it, recurse to clean intermediate files
                            cleanup_directory(item)
                        else:
                            # No skills in this subtree, remove it entirely
                            try:
                                shutil.rmtree(item)
                                removed_count += 1
                            except (PermissionError, OSError) as e:
                                print(f"    Warning: Could not remove {item.relative_to(repo_path)}: {e}")
            except (PermissionError, OSError):
                pass

        cleanup_directory(repo_path)

        if removed_count > 0:
            print(f"    Cleaned up {removed_count} item(s)")


def main() -> None:
    """Main execution."""
    _ = check_git_installed()

    print("Reading repository configuration...")
    repos = read_repo_list()
    print(f"Configured repositories: {len(repos)}")

    # Sync repositories
    print("\nSyncing repositories...")
    repo_paths: dict[str, Path] = {}
    for url in repos:
        repo_name = url_to_repo_name(url)
        print(f"  {repo_name}:")
        target_path = SKILLS_DIR / repo_name
        _ = clone_or_pull_repo(url, target_path)
        repo_paths[repo_name] = target_path

    # Clean up folders without SKILL.md files
    print("\nCleaning up non-skill folders...")
    cleanup_non_skill_folders(repo_paths)

    # Scan all skills and classify by location
    print("\nScanning all SKILL.md files...")
    local_skills, all_repo_skills = scan_all_skills(PROJECT_ROOT, repo_paths)
    print(f"  Found {len(local_skills)} local skills")
    print(f"  Found {len(all_repo_skills)} repository skills")

    # Report overrides
    overridden = set(local_skills.keys()) & set(all_repo_skills.keys())
    if overridden:
        print(
            f"\n  Local skills override {len(overridden)} repo skills: {', '.join(sorted(overridden))}"
        )

    # Update AGENTS.md
    print("\nUpdating AGENTS.md...")
    content = format_skills_section(local_skills, all_repo_skills)
    update_agents_md(content)

    total = len(local_skills) + len(set(all_repo_skills.keys()) - set(local_skills.keys()))
    print(f"\n✓ Synced {total} total skills to AGENTS.md")
    print(f"  ({len(local_skills)} local, {len(all_repo_skills) - len(overridden)} from repos)")


if __name__ == "__main__":
    main()
