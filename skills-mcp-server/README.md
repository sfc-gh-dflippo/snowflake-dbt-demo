# Skills MCP Server

Dynamic skill delivery for AI agents via Model Context Protocol (MCP).

## Overview

The Skills MCP Server discovers and serves AI agent skills from multiple Git repositories with zero content processing overhead. Skills are delivered on-demand via MCP Resources, with a catalog automatically injected into agent context.

## Features

- ✅ **Multi-Repository Support** - Aggregate skills from multiple Git repositories
- ✅ **Dynamic Loading** - Skills loaded on-demand, not statically embedded
- ✅ **Zero Processing** - Raw file serving for maximum performance
- ✅ **Simple Configuration** - Environment variables via mcp.json
- ✅ **MCP Resources** - Skills exposed as MCP resources with proper URIs
- ✅ **Discovery Tools** - List, search, and refresh skills via MCP tools

## Installation

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### Install Dependencies

```bash
cd skills-mcp-server
pip install -r requirements.txt
```

### Install as Package (Optional)

```bash
cd skills-mcp-server
pip install -e .
```

## Configuration

Configure the server via environment variables in your `.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "skills": {
      "command": "python",
      "args": ["-m", "skills_mcp_server.src.server"],
      "cwd": "/path/to/skills-mcp-server",
      "env": {
        "SKILLS_REPOS": "https://github.com/sfc-gh-dflippo/snowflake-dbt-demo,https://github.com/anthropics/skills",
        "SKILLS_BRANCHES": "main,main",
        "SKILLS_PATHS": ".claude/skills,.",
        "CACHE_DIR": "./.mcp_cache/skills",
        "REFRESH_ON_STARTUP": "true"
      }
    }
  }
}
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SKILLS_REPOS` | Yes | - | Comma-separated list of Git repository URLs |
| `SKILLS_BRANCHES` | No | `main` | Comma-separated list of branches (one per repo) |
| `SKILLS_PATHS` | No | `.` | Comma-separated list of paths to skills within repos |
| `CACHE_DIR` | No | `./cache` | Directory for local repository cache |
| `REFRESH_ON_STARTUP` | No | `true` | Whether to refresh repositories on server startup |

## Usage

### Running the Server

The server is designed to run as an MCP server via Cursor or other MCP-compatible tools.

#### Via MCP (Recommended)

Configure in `.cursor/mcp.json` as shown above, then restart Cursor.

#### Direct Testing

```bash
cd skills-mcp-server
export SKILLS_REPOS="https://github.com/anthropics/skills"
python -m skills_mcp_server.src.server
```

### Skills Catalog

When agents connect, they automatically receive a skills catalog listing all available skills:

```markdown
# Available Skills

## Skills from anthropic-skills

### mcp-builder
**URI:** `skill://anthropic-skills/mcp-builder`
**Description:** Guide for creating high-quality MCP servers...
**Resources:** 5 files available
```

### Loading Skills

Agents can load specific skills by requesting their URI:

```
skill://anthropic-skills/mcp-builder
```

### Accessing Resources

Agents can access skill resources (scripts, references, configs):

```
skill://anthropic-skills/mcp-builder/resource/scripts/evaluation.py
```

## MCP Interface

### Prompts

- **`skills_catalog`** - Complete catalog of all available skills (always in context)

### Resources

- `skill://{repo}/{skill}` - Raw SKILL.md content
- `skill://{repo}/{skill}/resource/{path}` - Raw resource file content

### Tools

#### `list_skills`

List all available skills with metadata.

**Arguments:**
- `filter_repo` (optional) - Repository name to filter results

**Returns:**
```json
[
  {
    "name": "mcp-builder",
    "full_name": "anthropic-skills/mcp-builder",
    "description": "Guide for creating high-quality MCP servers...",
    "repo": "anthropic-skills",
    "uri": "skill://anthropic-skills/mcp-builder",
    "resource_count": 5
  }
]
```

#### `get_skill_resources`

List available resources for a specific skill.

**Arguments:**
- `skill_name` (required) - Name of skill (format: "repo/skill" or just "skill")

**Returns:**
```json
[
  {
    "name": "evaluation.py",
    "path": "scripts/evaluation.py",
    "type": "script",
    "uri": "skill://anthropic-skills/mcp-builder/resource/scripts/evaluation.py",
    "mime_type": "text/x-python",
    "size": 1234
  }
]
```

#### `refresh_repositories`

Re-download and sync repositories.

**Arguments:**
- `repo_name` (optional) - Specific repository to refresh (default: all)

**Returns:**
```json
{
  "refreshed": ["anthropic-skills"],
  "skills_discovered": 13,
  "timestamp": "2025-11-08T10:30:00"
}
```

## Architecture

```
┌─────────────────────────────┐
│     MCP Client (Cursor)     │
└──────────────┬──────────────┘
               │ MCP Protocol
┌──────────────▼──────────────┐
│    FastMCP Server (server)  │
│  - Prompts (catalog)        │
│  - Resources (skills)       │
│  - Tools (list, refresh)    │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Skill Manager              │
│  - Discover skills          │
│  - Serve files raw          │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Git Sync                   │
│  - Download repo ZIPs       │
│  - Extract to cache         │
└─────────────────────────────┘
```

## Development

### Project Structure

```
skills-mcp-server/
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py           # FastMCP server implementation
│   ├── skill_manager.py    # Skill discovery and serving
│   └── git_sync.py         # Repository synchronization
├── tests/
│   ├── test_skill_manager.py
│   ├── test_git_sync.py
│   └── test_server.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Running Tests

```bash
cd skills-mcp-server
pytest tests/
```

### Logging

Set log level via environment variable:

```bash
export LOG_LEVEL=DEBUG
python -m skills_mcp_server.src.server
```

## Troubleshooting

### Server Won't Start

**Issue:** `SKILLS_REPOS environment variable is required`

**Solution:** Ensure `SKILLS_REPOS` is set in mcp.json configuration.

### No Skills Discovered

**Issue:** Server starts but discovers 0 skills

**Solutions:**
1. Check `SKILLS_PATHS` points to correct directory
2. Verify SKILL.md files have valid frontmatter (name, description)
3. Check server logs for parsing errors

### Download Failures

**Issue:** Failed to download repository

**Solutions:**
1. Check internet connection
2. Verify repository URL is correct and accessible
3. For private repos, authentication is not yet supported (coming soon)

### Resource Not Found

**Issue:** Agent can't access skill resource

**Solutions:**
1. Verify resource path is relative to skill directory
2. Check resource exists in repository
3. Ensure no directory traversal attempts (security check)

## Performance

- **Startup Time:** < 30 seconds for initial repository sync
- **Catalog Generation:** < 500ms for 100+ skills
- **Resource Retrieval:** < 50ms for cached content
- **Memory Footprint:** < 100MB typical usage

## Limitations

### Current Version (v1.0.0)

- Public repositories only (no authentication)
- GitHub only (no GitLab, Bitbucket support)
- No markdown processing (raw files only)
- No skill validation beyond frontmatter
- Manual refresh only (no automatic polling)

### Future Enhancements

- Private repository support with authentication
- Multiple Git providers (GitLab, Bitbucket)
- Automatic refresh on schedule
- Skill validation and linting
- Usage analytics and metrics

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/your-org/skills-mcp-server/issues)
- Documentation: See PRD in `.taskmaster/docs/skills-mcp-server-prd.md`

## Related Projects

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)


