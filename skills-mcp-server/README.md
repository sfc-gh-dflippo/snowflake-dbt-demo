# Skills MCP Server (TypeScript)

Dynamic skill delivery for AI agents via Model Context Protocol (MCP).

## Overview

The Skills MCP Server manages AI agent skills from Git repositories with zero manual synchronization overhead. Skills are automatically synced on a 5-minute interval, with a local cache for instant startup.

## Features

- ✅ **Multi-Repository Support** - Aggregate skills from multiple Git repositories
- ✅ **Local Skills Support** - Scan project root for local SKILL.md files (with precedence over remote)
- ✅ **AGENTS.md Integration** - Skills list embedded directly in AGENTS.md
- ✅ **Automatic Background Sync** - 5-minute interval with change detection
- ✅ **Fast Startup** - Starts in <2 seconds using cached database
- ✅ **Simple Configuration** - YAML-based repository management
- ✅ **Git CLI Integration** - Uses simple-git wrapper (no native bindings)
- ✅ **MCP Tools** - 4 focused tools for repository management
- ✅ **Change Detection** - Only regenerates catalog when skills actually change
- ✅ **Native Node.js Libraries** - Uses built-in `node:sqlite` module (no native bindings)

## Installation

### Prerequisites

- Node.js 22.5.0+ (for native SQLite support)
- npm or yarn
- git CLI (required)

### Install Dependencies

```bash
cd skills-mcp-server
npm install
```

### Build TypeScript

```bash
npm run build
```

## Configuration

### MCP Server Configuration

Add to your `.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "skills": {
      "command": "node",
      "args": ["dist/index.js"],
      "cwd": "/absolute/path/to/your-project/skills-mcp-server",
      "env": {
        "SKILLS_SYNC_INTERVAL_MS": "300000"
      }
    }
  }
}
```

Or use `tsx` for development:

```json
{
  "mcpServers": {
    "skills": {
      "command": "npx",
      "args": ["tsx", "src/index.ts"],
      "cwd": "/absolute/path/to/your-project/skills-mcp-server",
      "env": {
        "SKILLS_SYNC_INTERVAL_MS": "300000"
      }
    }
  }
}
```

**Note:** The server automatically detects your project root by looking for the parent directory of `skills-mcp-server` or a `.git` directory.

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SKILLS_SYNC_INTERVAL_MS` | No | `300000` | Background sync interval in milliseconds (5 minutes) |
| `SKILLS_WORKSPACE_DIR` | No | Auto-detected | Override project root detection (mainly for tests) |

**Auto-Detection:** The server automatically finds your project root by:
1. Looking for the parent directory of `skills-mcp-server` directory
2. Walking up to find a `.git` directory
3. Falling back to `process.cwd()`

This means you typically don't need to set `SKILLS_WORKSPACE_DIR` - just set the `cwd` in your mcp.json configuration.

## How It Works

### Directory Structure

When the MCP server starts, it creates a `.skills/` folder in your **project root**:

```
your-project/
├── .skills/                     # Created by MCP server
│   ├── .gitignore              # Excludes from your repo
│   ├── skills.yaml             # Your repository configuration
│   ├── skills.db               # SQLite cache (change detection)
│   └── repositories/           # Cloned repos (main/master only)
│       ├── github-com/
│       │   └── anthropics-skills/
│       └── github-com/
│           └── other-user-repo/
├── AGENTS.md                    # Skills catalog embedded here
└── ... (your project files)
```

### Skills Discovery

1. Server reads `.skills/skills.yaml` for repository list
2. Clones/pulls repositories (shallow, main/master only)
3. Recursively scans for `SKILL.md` files in repositories
4. **Scans project root for local SKILL.md files** (new!)
5. Parses frontmatter (name, description)
6. Calculates file hashes for change detection
7. Updates SQLite database with git commit hashes
8. Merges local and remote skills (local takes precedence)
9. Updates `AGENTS.md` when changes detected

### Local Skills Support

The server now scans your project root for local `SKILL.md` files, excluding:
- `.skills/` directory (managed repositories)
- `node_modules/`, `venv/`, `__pycache__/`
- `.git/`, `.github/`
- `skills-mcp-server/` directory

**Precedence:** If a local skill has the same name as a remote skill, the **local skill takes precedence** and will be shown instead of the remote version.

### Skills Catalog Format

The skills list is **embedded directly in AGENTS.md** between special markers:
```markdown
<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->
...skills list here...
<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->
```

The generated section includes:
- Local skills first (if any)
- Remote skills from repositories
- Skills grouped by source
- Checkboxes for enabled/disabled state
- Links to actual SKILL.md files

## MCP Tools

### 1. list_skill_repositories

List all configured repositories with sync status.

**Returns:**
```json
{
  "repositories": [
    {
      "url": "https://github.com/anthropics/skills",
      "branch": "main",
      "name": "github-com/anthropics-skills",
      "syncStatus": "synced",
      "lastSynced": "2025-01-01T10:30:00.000Z",
      "skillCount": 15
    }
  ],
  "totalRepositories": 1,
  "totalSkills": 15
}
```

### 2. add_skill_repository

Add a new skill repository.

**Arguments:**
- `url` (required): Git repository URL
- `branch` (optional): Branch name (defaults to "main")

**Example:**
```json
{
  "url": "https://github.com/user/my-skills",
  "branch": "main"
}
```

The repository will be cloned in the background. Check `AGENTS.md` after a few moments.

### 3. remove_skill_repository

Remove a skill repository.

**Arguments:**
- `url` (required): Git repository URL to remove

Removes the repository from configuration, deletes local files, and updates AGENTS.md.

### 4. refresh_skill_repositories

Force immediate sync of all repositories (outside of the 5-minute interval).

Useful when you know a repository has been updated and want immediate access.

## Configuration File

Edit `.skills/skills.yaml` manually or use the MCP tools:

```yaml
repositories:
  - url: https://github.com/anthropics/skills
    branch: main
  - url: https://github.com/your-org/custom-skills
    branch: main
  - url: https://github.com/another-user/dbt-skills
    branch: master
```

Changes are automatically detected on the next sync interval.

## AGENTS.md Integration

The MCP server now **automatically updates your AGENTS.md file** with the complete skills list.

### Automatic Setup

If `AGENTS.md` doesn't exist, the server creates one with default content. If it exists, the server adds a skills section with special markers:

```markdown
<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->

## MCP-Managed Skills

This project uses the **Skills MCP Server** to dynamically manage both local SKILL.md files and skills from remote Git repositories.

# Skills

**What are Skills?**

Skills are structured instruction sets that enhance AI assistant capabilities for specific domains or tasks. Each skill is a folder containing:
- **SKILL.md** - Core instructions and guidelines
- **references/** - Detailed documentation and examples
- **scripts/** - Helper scripts and templates
- **config/** - Configuration files

Skills provide domain-specific knowledge, best practices, code templates, and troubleshooting strategies. Think of them as specialized "expert personas" for areas like dbt development, Snowflake operations, or testing frameworks.

**Key Features:**
- Skills can be enabled `[x]` or disabled `[ ]` individually

**Available Skills:**

### Local Skills

- [x] **[my-custom-skill](path/to/SKILL.md)** - Description of my local skill

### github-com/anthropics-skills

- [x] **[skill-name](.skills/repositories/.../SKILL.md)** - Skill description

<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->
```

### How It Works

1. Server checks for `AGENTS.md` in project root
2. If missing, creates a default template with the skills section
3. If exists, adds the skills section at the end (if not present)
4. During sync, **updates the section content** with current skills
5. Preserves all content outside the markers
6. **Never edit content between the markers** - it's auto-generated

### Local Skills Precedence

When you create a local `SKILL.md` file in your project with the same name as a remote skill:
- The local version appears in the catalog
- The remote version is **excluded** from the list
- This allows you to override/customize remote skills locally

## Development

### Run in Development Mode

```bash
npm run dev
```

### Build for Production

```bash
npm run build
npm start
```

### Watch Mode

```bash
npm run watch
```

## Architecture

### Components

- **index.ts** - MCP server entry point, tool handlers
- **repository-manager.ts** - Git operations with fallback
- **skill-scanner.ts** - SKILL.md discovery and parsing (repositories + local project)
- **database.ts** - SQLite change tracking
- **agents-md-generator.ts** - AGENTS.md skills section management
- **background-sync.ts** - Interval-based synchronization + local skill scanning
- **types.ts** - TypeScript type definitions

### Change Detection

The server uses git commit hashes and file hashes to detect changes:
1. After pulling a repo, compare git commit hash with database
2. After scanning skills, compare file hashes with database
3. Only update `AGENTS.md` if hashes differ

This prevents unnecessary AGENTS.md updates and improves performance.

### Git Requirements

The server **requires Git CLI to be installed** on the system. On startup:
1. Verifies git CLI is available (`git --version`)
2. Uses `simple-git` library for all git operations
3. Performs shallow clones (`--depth 1`) for efficiency
4. Exits with error if git is not found

## Testing

Test repositories used in development:
- `https://github.com/anthropics/skills` (root level skills)
- `https://github.com/sfc-gh-dflippo/snowflake-dbt-demo` (`.claude/skills` subdirectory)

### Manual Testing

1. Start server and verify `.skills/` folder created
2. Check `AGENTS.md` is updated with skills section
3. Use `add_skill_repository` with test repos
4. Wait for background sync or use `refresh_skill_repositories`
5. Verify skills appear in `AGENTS.md`
6. Test `list_skill_repositories` shows correct status
7. Test `remove_skill_repository` cleans up properly

## Performance

- **Startup Time:** < 2 seconds (cached database)
- **Background Sync:** 5 minutes (configurable)
- **AGENTS.md Update:** < 500ms for 100+ skills
- **Memory Footprint:** < 50MB typical usage
- **Disk Usage:** Minimal (shallow clones only)

## Troubleshooting

### Server Won't Start

**Issue:** Module not found errors

**Solution:** Run `npm install` and `npm run build`

### No Skills Discovered

**Issue:** Server starts but `AGENTS.md` has no skills

**Solutions:**
1. Check `.skills/skills.yaml` has valid repository URLs
2. Verify repositories contain `SKILL.md` files
3. Check SKILL.md files have valid frontmatter (name, description)
4. Check server logs for errors

### Git Clone Failures

**Issue:** Repositories fail to clone

**Solutions:**
1. Check internet connection
2. Verify repository URLs are correct and public
3. Check if native git is available: `git --version`
4. Server will automatically fall back to isomorphic-git

### Sync Not Working

**Issue:** Changes in remote repos not appearing

**Solutions:**
1. Use `refresh_skill_repositories` tool to force sync
2. Check background sync interval setting
3. Review server logs for errors
4. Verify `.skills/skills.yaml` configuration

## Migration from Python Version

The TypeScript version provides:
- ✅ Faster startup (< 2 seconds vs 30+ seconds)
- ✅ Better change detection (no unnecessary regeneration)
- ✅ Simplified architecture (no prompts/resources, just tools)
- ✅ Improved error handling
- ✅ More efficient git operations

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## Related Projects

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP SDK](https://github.com/modelcontextprotocol/sdk)
