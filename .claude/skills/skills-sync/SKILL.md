---
name: skills-sync
description: Manage and synchronize AI agent skills from local SKILL.md files and remote Git repositories to AGENTS.md. This skill should be used when users need to sync skills, add/remove skill repositories, update skill catalogs, or set up the skills infrastructure in their projects.
---

# Skills Sync

## Overview

Sync AI agent skills from local SKILL.md files and remote Git repositories into a consolidated AGENTS.md catalog. Local skills take precedence over repository skills with the same name.

## Quick Start

**To sync skills:**

1. Ensure `.claude/skills/repos.txt` exists with repository URLs (auto-created if missing)
2. Run the sync script (automatically finds project root):

```bash
python3 .claude/skills/skills-sync/scripts/sync-skills.py
```

3. Check AGENTS.md for updated skills catalog

**Note:** The script automatically detects project root by walking up the directory tree, so it works from any location without copying.

## How It Works

### Configuration

Edit `.claude/skills/repos.txt` in project root to specify repositories to sync:

```text
https://github.com/anthropics/skills
https://github.com/sfc-gh-dflippo/snowflake-dbt-demo
```

- One URL per line
- Lines starting with `#` are comments
- Private repos require Git credentials configured

### Sync Process

The script:

1. Clones/pulls repositories to `.claude/skills/repositories/` (shallow clones for efficiency)
2. Scans entire project for SKILL.md files (excluding node_modules, .git, venv, __pycache__)
3. Parses YAML frontmatter (`name` and `description` fields)
4. Applies precedence: local skills override repository skills
5. Updates AGENTS.md between markers with organized catalog

### Skill Precedence

**Local Skills** (anywhere except `.claude/skills/repositories/`):

- Listed first in AGENTS.md
- Override repository skills with same name
- Enable project-specific customizations

**Repository Skills** (inside `.claude/skills/repositories/`):

- Grouped by source repository
- Skipped if local skill has same name

## Managing Repositories

**Add Repository:**

1. Add URL to `.claude/skills/repos.txt`
2. Run sync script

**Remove Repository:**

1. Delete or comment out URL in `.claude/skills/repos.txt`
2. Run sync script
3. Optionally delete `.claude/skills/repositories/<repo-name>/`

## Script Requirements

- Python 3.8+
- Auto-installs `python-frontmatter` if needed

## Troubleshooting

**Git not installed:**

- Install: `brew install git` (macOS), `apt-get install git` (Linux), or download from git-scm.com

**Private repository access:**

- Configure Git credentials (HTTPS tokens or SSH keys)

**Python frontmatter missing:**

- Script auto-installs, or run: `pip install python-frontmatter`

**SKILL.md parse errors:**

- Verify valid YAML frontmatter with `name` and `description` fields

**AGENTS.md merge conflicts:**

- Never edit between markers manually
- Keep markers intact and re-run sync script

## Resources

**scripts/sync-skills.py** - Python sync script (standalone, auto-installs dependencies)
