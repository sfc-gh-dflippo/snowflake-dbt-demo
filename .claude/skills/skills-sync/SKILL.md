---
name: skills-sync
description: Manage and synchronize AI agent skills from local SKILL.md files and remote Git repositories to AGENTS.md. This skill should be used when users need to sync skills, add/remove skill repositories, update skill catalogs, or set up the skills infrastructure in their projects.
---

# Skills Sync

## Overview

Sync AI agent skills from four locations into a consolidated AGENTS.md catalog. Supports both `.cortex` and `.claude` directories at project and global levels, with clear precedence rules.

## Quick Start

**To sync skills:**

1. Optionally configure repositories in `repos.txt` (see locations below)
2. Run the sync script:

```bash
python3 .claude/skills/skills-sync/scripts/sync-skills.py
```

3. Check AGENTS.md for updated skills catalog

**Note:** The script automatically detects project root by walking up the directory tree, so it works from any location.

## Skill Locations (Precedence Order)

Skills are scanned from four locations. Higher precedence locations override lower ones for skills with the same name:

| Priority | Location | Type |
|----------|----------|------|
| 1 (highest) | `$PROJECT/.cortex/skills/` | Project |
| 2 | `$PROJECT/.claude/skills/` | Project |
| 3 | `~/.snowflake/cortex/skills/` | Global |
| 4 (lowest) | `~/.claude/skills/` | Global |

### Project Skills

Create project-specific skills in your project directory:
- `$PROJECT/.cortex/skills/your-skill/SKILL.md` (highest precedence)
- `$PROJECT/.claude/skills/your-skill/SKILL.md`

### Global Skills

Create personal skills available across all projects:
- `~/.snowflake/cortex/skills/your-skill/SKILL.md`
- `~/.claude/skills/your-skill/SKILL.md`

## Repository Configuration

### repos.txt Locations

The `repos.txt` file can be placed in any of the four skill directories:

1. `$PROJECT/.cortex/skills/repos.txt` (project-specific repos)
2. `$PROJECT/.claude/skills/repos.txt`
3. `~/.snowflake/cortex/skills/repos.txt` (global default repos)
4. `~/.claude/skills/repos.txt`

All locations are checked, and repository URLs are deduplicated.

### repos.txt Format

```text
https://github.com/anthropics/skills
https://github.com/your-org/your-skills-repo
# This is a comment
```

- One URL per line
- Lines starting with `#` are comments
- Private repos require Git credentials configured
- Duplicate URLs (with/without `.git` suffix) are automatically deduplicated

### Repository Skill Extraction

Skills are extracted ONLY from these paths within repositories:
- `.cortex/skills/*/SKILL.md`
- `.claude/skills/*/SKILL.md`

Extracted skills are placed in `~/.snowflake/cortex/skills/` with a repo prefix:
- Example: `skills` repo → `~/.snowflake/cortex/skills/skills-dbt-core/`
- Example: `my-repo` repo → `~/.snowflake/cortex/skills/my-repo-custom-skill/`

**Note:** Skills in other locations within repositories (like `skills/` at root) are NOT extracted. This ensures only properly structured skills are synced.

## Sync Process

The script:

1. **Migration**: Detects and migrates old `.claude/skills/repositories/` structure
2. **Read repos.txt**: Reads from all four locations, deduplicates URLs
3. **Clone repositories**: Clones to temp location (`~/.snowflake/.cache/repos/`)
4. **Extract skills**: Copies skill directories to `~/.snowflake/cortex/skills/` with repo prefix
5. **Scan skills**: Scans all four locations with precedence rules
6. **Update AGENTS.md**: Writes organized catalog with Project/Global sections
7. **Cleanup**: Removes old `repositories/` directories if present

## Managing Repositories

**Add Repository:**

1. Add URL to any `repos.txt` file
2. Run sync script

**Remove Repository:**

1. Delete or comment out URL from `repos.txt`
2. Run sync script
3. Optionally delete extracted skills from `~/.snowflake/cortex/skills/<repo>-<skill>/`

## AGENTS.md Format

The script generates two sections in AGENTS.md:

```markdown
### Project Skills

- [x] **[skill-name](.cortex/skills/skill-name/SKILL.md)** - description

### Global Skills

- [x] **[repo-skill-name](~/.snowflake/cortex/skills/repo-skill-name/SKILL.md)** - description
```

## Script Requirements

- Python 3.8+
- Git installed
- Auto-installs `python-frontmatter` if needed

## Troubleshooting

### Git not installed

Install: `brew install git` (macOS), `apt-get install git` (Linux), or download from git-scm.com

### Private repository access

Configure Git credentials (HTTPS tokens or SSH keys)

### Python frontmatter missing

Script auto-installs, or run: `pip install python-frontmatter`

### SKILL.md parse errors

Verify valid YAML frontmatter with `name` and `description` fields:

```yaml
---
name: my-skill
description: Brief description of what this skill does
---
```

### AGENTS.md merge conflicts

- Never edit between markers manually
- Keep markers intact and re-run sync script

### Skills not appearing

- Check that SKILL.md is in the immediate child directory (flat structure required)
- Verify the skill has valid `name` and `description` in frontmatter
- Ensure the directory is not named `.cache`, `repositories`, or `.git`

### Repository skills not extracted

- Ensure skills are in `.cortex/skills/*/SKILL.md` or `.claude/skills/*/SKILL.md` within the repo
- Skills in other locations (like root `skills/` folder) are intentionally ignored

## Migration from Old Structure

If you have an old `.claude/skills/repositories/` structure, the script automatically:

1. Detects the old structure
2. Migrates skills to `~/.snowflake/cortex/skills/` with repo prefixes
3. Cleans up the old `repositories/` directory

No manual intervention required.

## Resources

**scripts/sync-skills.py** - Python sync script (standalone, auto-installs dependencies)
