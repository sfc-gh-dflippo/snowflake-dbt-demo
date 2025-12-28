#!/usr/bin/env python3
"""
Skills Sync Script - Sync AI agent skills from GitHub repositories using Git.

Supports four skill locations with clear precedence:
1. PROJECT_ROOT/.cortex/skills/ (highest)
2. PROJECT_ROOT/.claude/skills/
3. ~/.snowflake/cortex/skills/
4. ~/.claude/skills/ (lowest)

Repository skills are extracted to ~/.claude/skills/ with repo-prefixed names.
Configure repositories in repos.txt in any of the four skill directories.

Generates Cursor rules file with embedded XML from Agent Skills specification.

Requirements: git (uv auto-installed if running as script)
"""

import platform
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing_extensions import Annotated

# Initialize Typer app and Rich console
app = typer.Typer(help="Sync AI agent skills from repositories and local directories")
console = Console()

# Global debug flag
DEBUG = False


# ============================================================================
# LOGGING HELPERS
# ============================================================================


def log(message: str, level: str = "info", **kwargs) -> None:
    """Unified logging function with different levels.

    Args:
        message: Message to log
        level: Log level (debug, info, success, warning, error)
        **kwargs: Additional arguments passed to console.print()
    """
    if level == "debug" and not DEBUG:
        return

    styles = {
        "debug": "[dim]",
        "info": "",
        "success": "[green]",
        "warning": "[yellow]",
        "error": "[red]",
    }

    style = styles.get(level, "")
    console.print(f"{style}{message}", **kwargs)


# ============================================================================
# FILE OPERATION HELPERS
# ============================================================================


def sync_item(
    source: Path, dest: Path, should_move: bool, is_directory: bool = True
) -> None:
    """Sync a file or directory from source to destination.

    Args:
        source: Source path
        dest: Destination path
        should_move: If True, move (delete source). If False, copy (keep source).
        is_directory: If True, treat as directory. If False, treat as file.
    """
    # Remove existing destination
    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()

    # Move or copy
    if should_move:
        shutil.move(str(source), str(dest))
    else:
        if is_directory:
            shutil.copytree(source, dest)
        else:
            shutil.copy2(source, dest)


def run_git_command(
    cmd: list[str], cwd: Path, timeout: int = 120, description: str = ""
) -> tuple[bool, str]:
    """Run a git command with error handling.

    Args:
        cmd: Command to run
        cwd: Working directory
        timeout: Timeout in seconds
        description: Description for error messages

    Returns:
        Tuple of (success, output/error message)
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            timeout=timeout,
            text=True,
        )
        return True, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, f"{description} timed out"
    except subprocess.CalledProcessError as e:
        stderr = e.stderr if e.stderr else str(e)
        return False, f"{description} failed: {stderr}"
    except Exception as e:
        return False, f"{description} error: {e}"


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


# ============================================================================
# CONFIGURATION - All paths and constants
# ============================================================================

# Sync behavior configuration: True = move (delete source), False = copy (keep source)
MOVE_SKILLS = True  # Move skills from cortex to claude
MOVE_COMMANDS = True  # Move commands from cortex to claude
MOVE_AGENTS = False  # Copy agents (keep in cortex, Cortex code needs them there)

PROJECT_ROOT = find_project_root()

# Cortex directory structure - both project and global
CORTEX_ROOT_PROJECT = PROJECT_ROOT / ".cortex"
CORTEX_ROOT_GLOBAL = Path.home() / ".snowflake" / "cortex"

# Project-level cortex locations
PROJECT_CORTEX_SKILLS = CORTEX_ROOT_PROJECT / "skills"
PROJECT_CORTEX_AGENTS = CORTEX_ROOT_PROJECT / "agents"
PROJECT_CORTEX_COMMANDS = CORTEX_ROOT_PROJECT / "commands"

# Global cortex locations
GLOBAL_CORTEX_SKILLS = CORTEX_ROOT_GLOBAL / "skills"
GLOBAL_CORTEX_AGENTS = CORTEX_ROOT_GLOBAL / "agents"
GLOBAL_CORTEX_COMMANDS = CORTEX_ROOT_GLOBAL / "commands"

# Claude directory locations (for compatibility with existing code)
PROJECT_CLAUDE_DIR = PROJECT_ROOT / ".claude" / "skills"
GLOBAL_CLAUDE_DIR = Path.home() / ".claude" / "skills"

# Backward compatibility aliases (deprecated, use specific paths above)
PROJECT_CORTEX_DIR = PROJECT_CORTEX_SKILLS
GLOBAL_CORTEX_DIR = GLOBAL_CORTEX_SKILLS

# Cortex component directories (for marketplace registration)
CORTEX_COMPONENTS = {
    "project": {
        "skills": PROJECT_CORTEX_SKILLS,
        "agents": PROJECT_CORTEX_AGENTS,
        "commands": PROJECT_CORTEX_COMMANDS,
    },
    "global": {
        "skills": GLOBAL_CORTEX_SKILLS,
        "agents": GLOBAL_CORTEX_AGENTS,
        "commands": GLOBAL_CORTEX_COMMANDS,
    },
}

# Four scan locations for skills (in precedence order, highest to lowest)
SKILL_SCAN_LOCATIONS = [
    PROJECT_CORTEX_SKILLS,
    PROJECT_CLAUDE_DIR,
    GLOBAL_CORTEX_SKILLS,
    GLOBAL_CLAUDE_DIR,
]

# Repository extraction target (always to global .claude)
GLOBAL_SKILLS_DIR = GLOBAL_CLAUDE_DIR

# Temp clone location
TEMP_CLONE_DIR = Path.home() / ".claude" / ".cache" / "repos"

# Skill search paths within repositories
REPO_SKILL_PATHS = [".cortex/skills/*/SKILL.md", ".claude/skills/*/SKILL.md"]

AGENTS_MD = PROJECT_ROOT / "AGENTS.md"
CURSOR_RULES_DIR = PROJECT_ROOT / ".cursor" / "rules"
CURSOR_SKILLS_RULE = CURSOR_RULES_DIR / "skills.mdc"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_platform() -> str:
    """Detect current platform."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "linux"


def is_running_as_script() -> bool:
    """Check if running as a direct Python script vs installed uv tool."""
    return sys.argv[0].endswith(".py")


def install_uv() -> bool:
    """Attempt to install uv. Returns True if successful."""
    plat = get_platform()
    print("Installing uv...")

    try:
        if plat == "windows":
            subprocess.run(
                [
                    "powershell",
                    "-ExecutionPolicy",
                    "ByPass",
                    "-c",
                    "irm https://astral.sh/uv/install.ps1 | iex",
                ],
                check=True,
                timeout=120,
            )
        else:  # macOS and Linux
            subprocess.run(
                ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"],
                check=True,
                timeout=120,
            )
        print("  ✓ uv installed successfully")
        return True
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ) as e:
        print(f"  ✗ Failed to install uv: {e}")
        return False


def install_git() -> bool:
    """Attempt to install git. Returns True if successful."""
    plat = get_platform()
    print("Installing Git...")

    try:
        if plat == "macos":
            # Try Homebrew first, fall back to xcode-select
            if shutil.which("brew"):
                subprocess.run(["brew", "install", "git"], check=True, timeout=300)
            else:
                # xcode-select --install triggers GUI on macOS
                subprocess.run(["xcode-select", "--install"], check=True, timeout=30)
                print("  Note: Xcode command line tools installation started.")
                print("  Please complete the installation and run this script again.")
                return False
        elif plat == "windows":
            # Windows: Use winget if available
            if shutil.which("winget"):
                subprocess.run(
                    [
                        "winget",
                        "install",
                        "--id",
                        "Git.Git",
                        "-e",
                        "--source",
                        "winget",
                    ],
                    check=True,
                    timeout=300,
                )
            else:
                print("  ✗ Cannot auto-install Git on Windows without winget.")
                print("  Please download from: https://git-scm.com/download/win")
                return False
        else:  # Linux
            # Try apt-get, yum, or dnf
            if shutil.which("apt-get"):
                subprocess.run(
                    ["sudo", "apt-get", "install", "-y", "git"], check=True, timeout=300
                )
            elif shutil.which("yum"):
                subprocess.run(
                    ["sudo", "yum", "install", "-y", "git"], check=True, timeout=300
                )
            elif shutil.which("dnf"):
                subprocess.run(
                    ["sudo", "dnf", "install", "-y", "git"], check=True, timeout=300
                )
            else:
                print(
                    "  ✗ Cannot auto-install Git. No supported package manager found."
                )
                print("  Please install Git manually.")
                return False

        print("  ✓ Git installed successfully")
        return True
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ) as e:
        print(f"  ✗ Failed to install Git: {e}")
        return False


def check_and_install_uv() -> None:
    """Check if uv is installed, attempt to install if not."""
    if shutil.which("uv"):
        return

    if not install_uv():
        plat = get_platform()
        print("\nManual installation required. Run:")
        if plat == "windows":
            print(
                '  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
            )
        else:
            print("  curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("\nThen restart your terminal and run this script again.")
        sys.exit(1)

    # Refresh PATH to find newly installed uv
    if not shutil.which("uv"):
        print("\nuv was installed but not found in PATH.")
        print("Please restart your terminal and run this script again.")
        sys.exit(1)


def check_and_install_git() -> None:
    """Check if git is installed, attempt to install if not."""
    if shutil.which("git"):
        return

    if not install_git():
        plat = get_platform()
        print("\nManual installation required:")
        if plat == "macos":
            print("  brew install git")
        elif plat == "windows":
            print("  Download from: https://git-scm.com/download/win")
        else:
            print("  sudo apt-get install git  # or: sudo yum install git")
        print("\nThen restart your terminal and run this script again.")
        sys.exit(1)

    # Refresh PATH to find newly installed git
    if not shutil.which("git"):
        print("\nGit was installed but not found in PATH.")
        print("Please restart your terminal and run this script again.")
        sys.exit(1)


def install_self_as_uv_tool() -> None:
    """Install this package as a uv tool and exit."""
    # Find the package directory (parent of scripts/)
    script_path = Path(__file__).resolve()
    package_dir = script_path.parent.parent  # scripts/ -> skills-sync/

    print(f"Installing skills-sync as uv tool from {package_dir}...")
    try:
        subprocess.run(
            ["uv", "tool", "install", "--force", str(package_dir)],
            check=True,
            timeout=300,
        )
        print("\n✓ skills-sync installed successfully!")
        print("\nRun 'skills-sync' to sync your skills.")
        sys.exit(0)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"\n✗ Failed to install skills-sync: {e}")
        print("\nTry installing manually:")
        print(f"  uv tool install {package_dir}")
        sys.exit(1)


# Bootstrap: if running as script, install uv and self as tool
if is_running_as_script():
    check_and_install_uv()
    install_self_as_uv_tool()

# Always check for git (required in both modes)
check_and_install_git()

# Auto-install skills-ref using uv (only reached when running as installed tool)
try:
    from skills_ref import to_prompt, validate
except ImportError:
    if DEBUG:
        log("Installing skills-ref dependency...", "debug")
    try:
        subprocess.check_call(
            [
                "uv",
                "pip",
                "install",
                "--python",
                sys.executable,
                "skills-ref@git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref",
            ],
            timeout=300,
            capture_output=not DEBUG,  # Show output only in debug mode
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        console.print(f"[red]Error: Failed to install skills-ref: {e}[/red]")
        console.print("Try running manually:")
        console.print(
            "  uv pip install git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
        )
        sys.exit(1)

    # Refresh import paths and try again
    import importlib
    import site

    importlib.invalidate_caches()
    site.main()

    try:
        from skills_ref import validate  # noqa: F401 - verify import works
    except ImportError:
        console.print(
            "[red]Error: skills-ref was installed but cannot be imported.[/red]"
        )
        console.print(
            "Please run the script again or manually verify the installation:"
        )
        console.print(
            f"  {sys.executable} -c 'import skills_ref; print(skills_ref.__file__)'"
        )
        sys.exit(1)


def read_repo_list() -> list[str]:
    """Read repository URLs from repos.txt files in all four locations.

    Checks in precedence order, deduplicates URLs, maintains order.

    Locations checked:
    1. PROJECT_ROOT/.cortex/skills/repos.txt
    2. PROJECT_ROOT/.claude/skills/repos.txt
    3. ~/.snowflake/cortex/skills/repos.txt
    4. ~/.claude/skills/repos.txt

    Returns:
        Deduplicated list of repository URLs
    """
    all_repos: list[str] = []
    seen_urls: set[str] = set()

    # Check all four locations in precedence order
    repos_files = [location / "repos.txt" for location in SKILL_SCAN_LOCATIONS]

    found_any = False
    for repos_file in repos_files:
        if repos_file.exists():
            found_any = True
            log(f"  Reading {repos_file}", "debug")
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
        log("  No repos.txt found, creating default...", "debug")
        default_file = PROJECT_CORTEX_SKILLS / "repos.txt"
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
        target_dir: Destination directory (~/.claude/skills/)

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

            # Target: ~/.claude/skills/anthropics-skills-my-skill/
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
        global_dir: Target directory for extracted skills (~/.claude/skills/)
        temp_dir: Directory for temporary clones (~/.claude/.cache/repos/)

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
        success, message = run_git_command(
            ["git", "pull", "--quiet"], temp_repo_path, description="Git pull"
        )

        if not success:
            # Pull failed, try fresh clone
            shutil.rmtree(temp_repo_path, ignore_errors=True)
            success, message = run_git_command(
                ["git", "clone", "--depth", "1", url, str(temp_repo_path)],
                temp_dir,
                description="Git clone",
            )

        new_commit = get_current_commit(temp_repo_path)
        changed = old_commit != new_commit

        if changed and old_commit and new_commit:
            log(f"    Updated: {old_commit[:7]} → {new_commit[:7]}", "debug")
        else:
            log(
                f"    No changes (commit: {new_commit[:7] if new_commit else 'unknown'})",
                "debug",
            )
    else:
        # Clone new repo
        if temp_repo_path.exists():
            shutil.rmtree(temp_repo_path, ignore_errors=True)

        success, message = run_git_command(
            ["git", "clone", "--depth", "1", url, str(temp_repo_path)],
            temp_dir,
            description="Git clone",
        )

        if not success:
            log(f"    Warning: {message}", "warning")
            return False, []

        commit = get_current_commit(temp_repo_path)
        if commit:
            log(f"    Cloned: {commit[:7]}", "debug")
        changed = True

    # Extract skills from repo (always overwrite)
    extracted_skills = extract_skills_from_repo(
        temp_repo_path, repo_short_name, global_dir
    )

    return changed, extracted_skills


def scan_skills() -> list[Path]:
    """Scan for skills in four locations with precedence order.

    Locations (highest to lowest precedence):
    1. PROJECT_ROOT/.cortex/skills/
    2. PROJECT_ROOT/.claude/skills/
    3. ~/.snowflake/cortex/skills/
    4. ~/.claude/skills/

    Skills in higher precedence locations override those with same name in lower.

    Returns:
        List of Path objects to skill directories (deduplicated by name)
    """
    skill_paths: list[Path] = []
    seen_names: set[str] = set()

    # Scan in reverse precedence order, so higher precedence overwrites
    scan_locations = list(reversed(SKILL_SCAN_LOCATIONS))

    for location in scan_locations:
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

                # Get skill name from directory name (should match SKILL.md frontmatter)
                skill_name = skill_dir.name

                # If we haven't seen this skill name yet, add it
                # (higher precedence locations are scanned last, so they overwrite)
                if skill_name not in seen_names:
                    skill_paths.insert(0, skill_dir)  # Insert at beginning
                    seen_names.add(skill_name)
                else:
                    # Replace with higher precedence version
                    # Find and remove the lower precedence one
                    for i, existing_path in enumerate(skill_paths):
                        if existing_path.name == skill_name:
                            skill_paths[i] = skill_dir
                            break

        except (PermissionError, OSError) as e:
            log(f"  Warning: Could not scan {location}: {e}", "debug")

    return skill_paths


def generate_cursor_rule(xml_content: str) -> None:
    """Generate .cursor/rules/skills.mdc with embedded XML.

    Args:
        xml_content: XML string from skills-ref to_prompt()
    """
    # Ensure .cursor/rules directory exists
    CURSOR_RULES_DIR.mkdir(parents=True, exist_ok=True)

    # MDC frontmatter and content
    mdc_content = f"""---
description: Available AI agent skills with instructions and capabilities from Agent Skills specification
globs: **/*
alwaysApply: true
---

{xml_content}
"""

    CURSOR_SKILLS_RULE.write_text(mdc_content)
    log(f"  ✓ Created {CURSOR_SKILLS_RULE.relative_to(PROJECT_ROOT)}", "debug")


def cleanup_agents_md() -> None:
    """Remove all marker-delimited sections from AGENTS.md.

    Removes both current and legacy marker pairs:
    - <!-- BEGIN AUTO-GENERATED SKILLS ... --> / <!-- END AUTO-GENERATED SKILLS ... -->
    - <!-- BEGIN MCP SKILLS ... --> / <!-- END MCP SKILLS ... -->
    """
    if not AGENTS_MD.exists():
        return

    agents_content = AGENTS_MD.read_text()

    # Marker pairs to remove (partial match on BEGIN marker)
    marker_pairs = [
        ("<!-- BEGIN AUTO-GENERATED SKILLS", "<!-- END AUTO-GENERATED SKILLS"),
        ("<!-- BEGIN MCP SKILLS", "<!-- END MCP SKILLS"),
    ]

    modified = False
    for start_marker_prefix, end_marker_prefix in marker_pairs:
        # Find start marker (may have additional text after the prefix)
        start_idx = agents_content.find(start_marker_prefix)
        if start_idx == -1:
            continue

        # Find the end of the start marker line
        start_line_end = agents_content.find("-->", start_idx)
        if start_line_end == -1:
            continue
        start_line_end += 3  # Include the -->

        # Find end marker
        end_idx = agents_content.find(end_marker_prefix, start_line_end)
        if end_idx == -1:
            continue

        # Find the end of the end marker line
        end_line_end = agents_content.find("-->", end_idx)
        if end_line_end == -1:
            continue
        end_line_end += 3  # Include the -->

        # Remove entire section including both markers
        before = agents_content[:start_idx].rstrip()
        after = agents_content[end_line_end:].lstrip()

        # Rejoin with proper spacing
        if after:
            agents_content = before + "\n\n" + after
        else:
            agents_content = before + "\n"

        modified = True
        log(f"  Removed marker section: {start_marker_prefix}", "debug")

    if modified:
        AGENTS_MD.write_text(agents_content)
        log(f"  ✓ Cleaned up {AGENTS_MD.relative_to(PROJECT_ROOT)}", "debug")


def sync_cortex_to_claude() -> None:
    """Sync skills, agents, and commands from cortex directories to claude directories.

    This allows Claude Code to discover them natively without marketplace registration.
    Behavior controlled by MOVE_SKILLS, MOVE_AGENTS, MOVE_COMMANDS flags:
    - True = move (delete source after copying)
    - False = copy (keep source intact)

    Syncs from:
    - .cortex/skills/ → .claude/skills/
    - .cortex/agents/ → .claude/agents/
    - .cortex/commands/ → .claude/commands/

    For both project and global locations.
    """
    log("\n[bold]Syncing cortex content to claude...[/bold]")

    sync_operations = []

    # Define source → destination mappings with their sync behavior
    mappings = [
        # Project-level: (source, dest, description, should_move, file_filter)
        (
            PROJECT_CORTEX_SKILLS,
            PROJECT_CLAUDE_DIR,
            "project skills",
            MOVE_SKILLS,
            lambda p: p.is_dir() and (p / "SKILL.md").exists(),
        ),
        (
            PROJECT_CORTEX_AGENTS,
            PROJECT_ROOT / ".claude" / "agents",
            "project agents",
            MOVE_AGENTS,
            lambda p: p.is_file() and p.suffix == ".md",
        ),
        (
            PROJECT_CORTEX_COMMANDS,
            PROJECT_ROOT / ".claude" / "commands",
            "project commands",
            MOVE_COMMANDS,
            lambda p: True,
        ),  # All files/dirs
        # Global-level
        (
            GLOBAL_CORTEX_SKILLS,
            GLOBAL_CLAUDE_DIR,
            "global skills",
            MOVE_SKILLS,
            lambda p: p.is_dir() and (p / "SKILL.md").exists(),
        ),
        (
            GLOBAL_CORTEX_AGENTS,
            Path.home() / ".claude" / "agents",
            "global agents",
            MOVE_AGENTS,
            lambda p: p.is_file() and p.suffix == ".md",
        ),
        (
            GLOBAL_CORTEX_COMMANDS,
            Path.home() / ".claude" / "commands",
            "global commands",
            MOVE_COMMANDS,
            lambda p: True,
        ),
    ]

    skip_dirs = {".cache", "repositories", ".git", ".claude-plugin"}

    for source_dir, dest_dir, description, should_move, file_filter in mappings:
        if not source_dir.exists():
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)
        items_synced = 0
        operation = "moved" if should_move else "copied"

        for item in source_dir.iterdir():
            # Skip special directories
            if item.name in skip_dirs:
                continue

            # Apply filter
            if not file_filter(item):
                continue

            dest_item = dest_dir / item.name
            sync_item(item, dest_item, should_move, is_directory=item.is_dir())
            items_synced += 1

        if items_synced > 0:
            sync_operations.append(f"{description}: {items_synced} items")
            log(
                f"  ✓ {operation.capitalize()} {description} ({items_synced} items)",
                "debug",
            )

    if not sync_operations:
        log("  No cortex content found to sync", "debug")
    else:
        log(f"  ✓ Synced {len(sync_operations)} cortex directories")


def cleanup_old_repositories() -> None:
    """Remove old nested repository structures and cache after successful sync.

    Checks both project and global .cortex/skills/repositories and .claude/skills/repositories.
    Also removes old ~/.snowflake/.cache/ directory since we now use ~/.claude/.cache/
    """
    # Build list of old directories to clean up
    old_dirs = [location / "repositories" for location in SKILL_SCAN_LOCATIONS]
    # Add old cache directory
    old_dirs.append(Path.home() / ".snowflake" / ".cache")

    for old_dir in old_dirs:
        if old_dir.exists() and old_dir.is_dir():
            try:
                # Try to get relative path, fall back to absolute for global dirs
                try:
                    rel_path = old_dir.relative_to(PROJECT_ROOT)
                    display_path = str(rel_path)
                except ValueError:
                    display_path = str(old_dir)

                log(f"  Cleaning up old structure: {display_path}", "debug")
                shutil.rmtree(old_dir)
                log("  ✓ Removed old repository structure", "debug")
            except Exception as e:
                log(f"  Warning: Could not remove {old_dir}: {e}", "debug")


@app.command()
def sync_skills(
    debug: Annotated[
        bool, typer.Option("--debug", help="Enable verbose debug logging")
    ] = False
) -> None:
    """Main execution with four-location scanning and Agent Skills CLI integration."""
    # Set global DEBUG flag
    global DEBUG
    DEBUG = debug

    # Recalculate PROJECT_ROOT for current working directory
    # This is important when script is run as installed tool from different directories
    global PROJECT_ROOT, CORTEX_ROOT_PROJECT
    global PROJECT_CORTEX_SKILLS, PROJECT_CORTEX_AGENTS, PROJECT_CORTEX_COMMANDS
    global PROJECT_CLAUDE_DIR, PROJECT_CORTEX_DIR
    global CORTEX_COMPONENTS, SKILL_SCAN_LOCATIONS
    global AGENTS_MD, CURSOR_RULES_DIR, CURSOR_SKILLS_RULE

    PROJECT_ROOT = find_project_root()

    # Debug: Show what project root was found
    log(f"\nProject root: {PROJECT_ROOT}", "debug")
    log(f"Current working directory: {Path.cwd()}", "debug")

    # Recalculate all project-specific paths
    CORTEX_ROOT_PROJECT = PROJECT_ROOT / ".cortex"
    PROJECT_CORTEX_SKILLS = CORTEX_ROOT_PROJECT / "skills"
    PROJECT_CORTEX_AGENTS = CORTEX_ROOT_PROJECT / "agents"
    PROJECT_CORTEX_COMMANDS = CORTEX_ROOT_PROJECT / "commands"
    PROJECT_CLAUDE_DIR = PROJECT_ROOT / ".claude" / "skills"
    PROJECT_CORTEX_DIR = PROJECT_CORTEX_SKILLS

    # Debug: Show if cortex directories exist
    log("Checking cortex directories:", "debug")
    log(f"  {PROJECT_CORTEX_SKILLS} exists: {PROJECT_CORTEX_SKILLS.exists()}", "debug")
    log(f"  {PROJECT_CORTEX_AGENTS} exists: {PROJECT_CORTEX_AGENTS.exists()}", "debug")
    log(
        f"  {PROJECT_CORTEX_COMMANDS} exists: {PROJECT_CORTEX_COMMANDS.exists()}",
        "debug",
    )

    # Update CORTEX_COMPONENTS with new project paths
    CORTEX_COMPONENTS["project"] = {
        "skills": PROJECT_CORTEX_SKILLS,
        "agents": PROJECT_CORTEX_AGENTS,
        "commands": PROJECT_CORTEX_COMMANDS,
    }

    # Update SKILL_SCAN_LOCATIONS with new project paths
    SKILL_SCAN_LOCATIONS = [
        PROJECT_CORTEX_SKILLS,
        PROJECT_CLAUDE_DIR,
        GLOBAL_CORTEX_SKILLS,
        GLOBAL_CLAUDE_DIR,
    ]

    # Update output paths
    AGENTS_MD = PROJECT_ROOT / "AGENTS.md"
    CURSOR_RULES_DIR = PROJECT_ROOT / ".cursor" / "rules"
    CURSOR_SKILLS_RULE = CURSOR_RULES_DIR / "skills.mdc"

    # 1. Read repos.txt from all four locations (deduplicated)
    log("\n[bold]Syncing repository skills...[/bold]")
    repos = read_repo_list()
    log(f"Configured repositories: {len(repos)} (deduplicated)", "debug")

    # 2. Sync each repo to temp, extract to ~/.claude/skills/
    if repos:
        for url in repos:
            repo_short_name = get_repo_short_name(url)
            log(f"  • {repo_short_name}")

            try:
                _changed, extracted_skills = sync_repo_to_global(
                    url, GLOBAL_SKILLS_DIR, TEMP_CLONE_DIR
                )

                log(f"    Extracted {len(extracted_skills)} skill(s)", "debug")
            except subprocess.TimeoutExpired:
                console.print("    [yellow]⚠ Warning: Git operation timed out[/yellow]")
            except subprocess.CalledProcessError as e:
                console.print(
                    f"    [yellow]⚠ Warning: Failed to sync repository: {e}[/yellow]"
                )
            except Exception as e:
                console.print(f"    [yellow]⚠ Warning: {e}[/yellow]")

    # 3. Move cortex directories to claude directories FIRST
    # This must happen before scanning so the Cursor rules reflect the final locations
    sync_cortex_to_claude()

    # 4. Scan four locations with precedence (after move)
    log("\n[bold]Scanning local skills...[/bold]")
    for i, location in enumerate(SKILL_SCAN_LOCATIONS, 1):
        try:
            rel_path = location.relative_to(PROJECT_ROOT)
            display = f"{rel_path} (project)"
        except ValueError:
            if location == GLOBAL_CORTEX_SKILLS:
                display = f"{location} (global .cortex)"
            else:
                display = f"{location} (global .claude)"
        log(f"  {i}. {display}", "debug")

    skill_paths = scan_skills()

    log(f"  Found {len(skill_paths)} total skill(s)", "debug")

    # 5. Validate skills and generate XML using skills-ref
    log("\n[bold]Generating Cursor rules...[/bold]")

    # Validate and filter out skills with fatal errors
    # Non-fatal errors (like directory name mismatch) are OK
    usable_skill_paths = []
    fatal_error_count = 0

    for skill_path in skill_paths:
        errors = validate(skill_path)
        if errors:
            # Fatal errors: missing frontmatter, unparseable YAML, missing name/description
            fatal_error_keywords = [
                "must start with YAML frontmatter",
                "must contain 'name' field",
                "must contain 'description' field",
                "Invalid YAML",
            ]
            fatal_errors = [
                e
                for e in errors
                if any(keyword in e for keyword in fatal_error_keywords)
            ]

            if fatal_errors:
                log(f"  Skipping {skill_path.name} (fatal errors):", "debug")
                for error in fatal_errors:
                    log(f"    - {error}", "debug")
                fatal_error_count += 1
            else:
                # Only non-fatal errors (e.g., directory name mismatch) - include it
                usable_skill_paths.append(skill_path)
        else:
            # No errors at all
            usable_skill_paths.append(skill_path)

    # Generate XML for all usable skills
    if usable_skill_paths:
        try:
            xml_output = to_prompt(usable_skill_paths)

            # 6. Generate Cursor rules file (after move, with correct paths)
            generate_cursor_rule(xml_output)
            log(f"  ✓ Created Cursor rules with {len(usable_skill_paths)} skills")
        except Exception as e:
            console.print(
                f"  [yellow]⚠ Warning: Could not generate Cursor rules: {e}[/yellow]"
            )
    else:
        console.print(
            "  [yellow]⚠ Warning: No usable skills found, skipping Cursor rules generation[/yellow]"
        )

    # 7. Clean up AGENTS.md
    log("\nCleaning up AGENTS.md...", "debug")
    cleanup_agents_md()

    # 8. Cleanup old repository structures
    cleanup_old_repositories()

    # 9. Report summary
    console.print()
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="green bold")
    table.add_column()

    table.add_row("✓", f"Synced [bold]{len(usable_skill_paths)}[/bold] usable skills")
    if fatal_error_count > 0:
        table.add_row(
            "⚠",
            f"[yellow]{fatal_error_count} skills skipped (validation errors)[/yellow]",
        )
    table.add_row(
        "✓", "Skills available in Cursor via [cyan].cursor/rules/skills.mdc[/cyan]"
    )
    table.add_row("✓", "Cortex content synced to claude directories")
    table.add_row("", f"[dim]  • Skills: {'moved' if MOVE_SKILLS else 'copied'}[/dim]")
    table.add_row("", f"[dim]  • Agents: {'moved' if MOVE_AGENTS else 'copied'}[/dim]")
    table.add_row(
        "", f"[dim]  • Commands: {'moved' if MOVE_COMMANDS else 'copied'}[/dim]"
    )

    console.print(
        Panel(
            table,
            title="[bold green]Skills Sync Complete[/bold green]",
            border_style="green",
        )
    )


def main() -> None:
    """Entry point for the CLI tool."""
    app()


if __name__ == "__main__":
    main()
