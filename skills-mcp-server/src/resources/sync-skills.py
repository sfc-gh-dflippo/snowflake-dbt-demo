#!/usr/bin/env python3
"""
Skills Sync Script - Sync AI agent skills from GitHub repositories using Git.
Uses git clone/pull for efficiency. Local SKILL.md files take precedence.
Configure repositories in .skills/repos.txt (created automatically).
"""

import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

# Auto-install frontmatter if needed
try:
    import frontmatter
except ImportError:
    print("Installing python-frontmatter...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "python-frontmatter"])
    import frontmatter

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILLS_DIR = SCRIPT_DIR / ".skills" / "repositories"
CONFIG_FILE = SCRIPT_DIR / ".skills" / "repos.txt"
AGENTS_MD = SCRIPT_DIR / "AGENTS.md"
MARKERS = ("<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->", 
           "<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->")

def check_git_installed():
    """Check if git CLI is available."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Git is not installed. Please install Git.")
        sys.exit(1)

def read_repo_list():
    """Read repository URLs from config file."""
    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text("https://github.com/anthropics/skills\n")
    
    return [line.strip() for line in CONFIG_FILE.read_text().splitlines() 
            if line.strip() and not line.startswith('#')]

def url_to_repo_name(url):
    """Convert GitHub URL to directory-safe name."""
    parsed = urlparse(url)
    hostname = parsed.hostname.replace('.', '-')
    path_parts = parsed.path.strip('/').replace('.git', '').split('/')
    return f"{hostname}/{'-'.join(path_parts)}"

def get_current_commit(repo_path):
    """Get current commit hash of a Git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def clone_or_pull_repo(url, target_path):
    """Clone repo if new, or pull if exists. Returns (changed, commit_hash)."""
    if target_path.exists() and (target_path / ".git").exists():
        # Repo exists, check for changes
        old_commit = get_current_commit(target_path)
        
        # Pull latest
        subprocess.run(
            ["git", "pull", "--quiet"],
            cwd=target_path,
            check=True,
            capture_output=True
        )
        
        new_commit = get_current_commit(target_path)
        changed = (old_commit != new_commit)
        
        if changed:
            print(f"  Updated: {old_commit[:7]} → {new_commit[:7]}")
        else:
            print(f"  No changes")
        
        return changed, new_commit
    else:
        # Clone new repo
        target_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(target_path)],
            check=True,
            capture_output=True
        )
        commit = get_current_commit(target_path)
        print(f"  Cloned: {commit[:7]}")
        return True, commit

def scan_all_skills(project_root, repo_paths):
    """Scan entire project for SKILL.md files, classifying by location.
    
    Skills found in .skills/repositories/ are classified as repository skills.
    Skills found anywhere else are classified as local skills.
    
    Returns:
        tuple: (local_skills, repo_skills) dictionaries
    """
    local_skills = {}
    repo_skills = {}
    repositories_dir = SKILLS_DIR
    
    for skill_path in project_root.rglob("SKILL.md"):
        # Skip common directories that should never contain skills
        if any(part in ["node_modules", ".git", "venv", "__pycache__"] 
               for part in skill_path.parts):
            continue
        
        try:
            post = frontmatter.load(skill_path)
            name = post.get("name", "")
            description = post.get("description", "")
            if not (name and description):
                continue
            
            rel_path = skill_path.relative_to(project_root)
            
            # Check if this skill is inside .skills/repositories/
            try:
                skill_path.relative_to(repositories_dir)
                # It's inside repositories dir - find which repo
                repo_name = None
                for rname, rpath in repo_paths.items():
                    try:
                        skill_path.relative_to(rpath)
                        repo_name = rname
                        break
                    except ValueError:
                        continue
                
                if repo_name:
                    repo_skills[name] = {
                        "name": name,
                        "path": str(rel_path),
                        "description": description,
                        "source": repo_name
                    }
            except ValueError:
                # Not in repositories dir - it's a local skill
                local_skills[name] = {
                    "name": name,
                    "path": str(rel_path),
                    "description": description,
                    "source": "local"
                }
        except Exception as e:
            print(f"Warning: Failed to parse {skill_path}: {e}")
    
    return local_skills, repo_skills

def format_skills_section(local_skills, repo_skills_by_name):
    """Format skills for AGENTS.md with local priority and grouping."""
    output = []
    output.append("## MCP-Managed Skills\n\n")
    output.append("This project uses the **Skills MCP Server** to dynamically manage both local SKILL.md files and skills from remote Git repositories.\n\n")
    output.append("# Skills\n\n")
    output.append("**What are Skills?**\n\n")
    output.append("Skills are structured instruction sets that enhance AI assistant capabilities for specific domains or tasks. Each skill is a folder containing:\n")
    output.append("- **SKILL.md** - Core instructions and guidelines\n")
    output.append("- **references/** - Detailed documentation and examples\n")
    output.append("- **scripts/** - Helper scripts and templates\n")
    output.append("- **config/** - Configuration files\n\n")
    output.append("Skills provide domain-specific knowledge, best practices, code templates, and troubleshooting strategies. Think of them as specialized \"expert personas\" for areas like dbt development, Snowflake operations, or testing frameworks.\n\n")
    output.append("**Key Features:**\n")
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
    repo_groups = {}
    for name, skill in repo_skills_by_name.items():
        if name not in local_skills:  # Skip if overridden by local
            source = skill['source']
            if source not in repo_groups:
                repo_groups[source] = {}
            repo_groups[source][name] = skill
    
    for repo_name in sorted(repo_groups.keys()):
        output.append(f"### {repo_name}\n\n")
        for name in sorted(repo_groups[repo_name].keys()):
            skill = repo_groups[repo_name][name]
            output.append(f"- [x] **[{name}]({skill['path']})** - {skill['description']}\n")
        output.append("\n")
    
    return "".join(output)

def update_agents_md(content):
    """Update AGENTS.md between markers."""
    if not AGENTS_MD.exists():
        # Create basic AGENTS.md
        template = "# AI Agent Configuration\n\nContext and guidelines for AI coding agents.\n\n"
        AGENTS_MD.write_text(template)
    
    agents_content = AGENTS_MD.read_text()
    start_marker, end_marker = MARKERS
    start_idx = agents_content.find(start_marker)
    end_idx = agents_content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        # Append at end
        if not agents_content.endswith('\n'):
            agents_content += '\n'
        new_content = f"\n{start_marker}\n{content}\n{end_marker}\n"
        AGENTS_MD.write_text(agents_content + new_content)
    else:
        # Replace between markers
        before = agents_content[:start_idx + len(start_marker)]
        after = agents_content[end_idx:]
        new_content = f"{before}\n{content}\n{after}"
        AGENTS_MD.write_text(new_content)

def main():
    """Main execution."""
    check_git_installed()
    
    print("Reading repository configuration...")
    repos = read_repo_list()
    print(f"Configured repositories: {len(repos)}")
    
    # Sync repositories
    print("\nSyncing repositories...")
    repo_paths = {}
    for url in repos:
        repo_name = url_to_repo_name(url)
        print(f"  {repo_name}:")
        target_path = SKILLS_DIR / repo_name
        changed, commit = clone_or_pull_repo(url, target_path)
        repo_paths[repo_name] = target_path
    
    # Scan all skills and classify by location
    print("\nScanning all SKILL.md files...")
    local_skills, all_repo_skills = scan_all_skills(SCRIPT_DIR, repo_paths)
    print(f"  Found {len(local_skills)} local skills")
    print(f"  Found {len(all_repo_skills)} repository skills")
    
    # Report overrides
    overridden = set(local_skills.keys()) & set(all_repo_skills.keys())
    if overridden:
        print(f"\n  Local skills override {len(overridden)} repo skills: {', '.join(sorted(overridden))}")
    
    # Update AGENTS.md
    print("\nUpdating AGENTS.md...")
    content = format_skills_section(local_skills, all_repo_skills)
    update_agents_md(content)
    
    total = len(local_skills) + len(set(all_repo_skills.keys()) - set(local_skills.keys()))
    print(f"\n✓ Synced {total} total skills to AGENTS.md")
    print(f"  ({len(local_skills)} local, {len(all_repo_skills) - len(overridden)} from repos)")

if __name__ == "__main__":
    main()

