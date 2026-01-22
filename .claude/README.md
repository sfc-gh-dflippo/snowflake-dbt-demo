# Claude Skills Management

This directory contains Claude AI skills for the snowflake-dbt-demo project.

## Directory Structure

- `skills/` - Contains all skill definitions
  - `anthropic-skills/` - Official Anthropic skills (auto-synced)
  - Custom project-specific skills (dbt-, snowflake-, etc.)

## Syncing Skills

The project includes a Python script (`sync-agent-skills.py`) at the project root that automatically syncs Anthropic skills and updates the `AGENTS.md` file.

### Running the Sync

Execute the sync script from the project root:

```bash
python3 sync-agent-skills.py
```

**Note:** The script automatically installs the `python-frontmatter` dependency if it's not already installed.

### What the Script Does

1. **Cleans up** old skill directories (if present)
2. **Downloads** the latest Anthropic skills from GitHub
3. **Extracts** them to `.claude/skills/anthropic-skills/`
4. **Discovers** all `SKILL.md` files (both project-specific and Anthropic)
5. **Parses** frontmatter metadata (`name` and `description`) from each skill
6. **Updates** the Skills section at the end of `AGENTS.md`

### How It Updates AGENTS.md

The script appends or updates the "Skills" section at the end of `AGENTS.md` between these markers:

```html
<!-- BEGIN SKILLS - DO NOT EDIT MANUALLY -->
... auto-generated content here ...
<!-- END SKILLS - DO NOT EDIT MANUALLY -->
```

**Important:**

- Do not manually edit content between these markers - it will be overwritten on the next sync
- The Skills section is always placed at the end of AGENTS.md
- If the markers don't exist, they are automatically appended to the file

### Generated Content Format

The script automatically creates a unified skill list with:

- **Header section** explaining what skills are and how they work
- **Sync command** showing how to update skills
- **Alphabetically sorted** list of all skills (both project and Anthropic)
- **Checkboxes** `- [x]` for each skill entry
- **Skill names** linked to their respective `SKILL.md` files
- **Descriptions** extracted from frontmatter with use case guidance
- **Automatic updates** whenever new skills are added

## Skills Overview

The sync script discovers all skills automatically, including:

### Official Anthropic Skills

- Creative & Design (algorithmic art, visual design, GIF creation)
- Development & Technical (artifacts, MCP servers, webapp testing)
- Enterprise & Communication (brand guidelines, internal comms, themes)
- Document Skills (docx, pdf, pptx, xlsx)
- Meta Skills (skill creation templates)

### Project-Specific Skills

- dbt development (architecture, modeling, testing, performance)
- Snowflake operations (CLI, connections, schemachange)
- Streamlit development and testing (with Playwright)
- Task management (task-master workflow)
- dbt Projects on Snowflake (deployment and monitoring)

All skills are automatically discovered and listed in [AGENTS.md](../AGENTS.md) at the end of the file.

```sql

```
