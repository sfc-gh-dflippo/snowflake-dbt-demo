# Skills MCP Server

Manage AI agent skills from GitHub repositories using an MCP server that provides downloadable sync scripts.

## Quick Start

### 1. Configure Repositories

Create or edit `.skills/repos.txt` in your project root with one repository URL per line:

```
https://github.com/anthropics/skills
https://github.com/your-org/custom-skills
```

### 2. Install MCP Server

**Option A: Use from This Repository (Recommended)**

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skills": {
      "command": "node",
      "args": ["skills-mcp-server/dist/index.js"]
    }
  }
}
```

Build the server:

```bash
cd skills-mcp-server
npm install
npm run build
```

**Option B: Use Published Package from GitHub**

Published package: `@sfc-gh-dflippo/skills-mcp-server` on [GitHub Package Registry](https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/pkgs/npm/skills-mcp-server)

**Note:** GitHub Package Registry requires authentication even for public packages.

**Setup authentication:**

1. Create a GitHub Personal Access Token with `read:packages` scope:
   - Go to: https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scope: `read:packages`

2. Configure npm globally:
```bash
cat > ~/.npmrc << 'EOF'
@sfc-gh-dflippo:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=YOUR_GITHUB_TOKEN
EOF
```

3. Use in `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "skills": {
      "command": "npx",
      "args": ["-y", "@sfc-gh-dflippo/skills-mcp-server"]
    }
  }
}
```

**Note:** Path is relative to your workspace root (where `.cursor/` folder is located).

Restart Cursor to load the MCP server.

### 3. Sync Skills

**Option A: Ask your AI agent**
```
Please sync my skill repositories
```

**Option B: Use the Cursor command**
```
/skills/sync-skills
```

The agent will download and execute a sync script that:
- Clones/pulls repositories from `.skills/repos.txt`
- Scans for `SKILL.md` files (local and remote)
- Updates `AGENTS.md` with your skills catalog
- Uses shallow git clones for minimal storage (~3MB per repo)

## What Are Skills?

Skills are structured instruction sets (SKILL.md files) that enhance AI assistant capabilities for specific domains. Each skill provides:
- Domain-specific knowledge and best practices
- Code templates and examples
- Troubleshooting strategies

**Local skills** (in your project) override remote skills with the same name.

## How It Works

The server provides sync scripts as **MCP resources** (not direct tool calls):

1. **Agent requests sync** via command or prompt
2. **Server provides script** (TypeScript or Python)
3. **Agent downloads and executes** script locally
4. **Script syncs repositories** and updates AGENTS.md

**Why this approach?**

This follows the **resource pattern** recommended in [Anthropic's Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) blog post:

> "Agents can load only the definitions they need for the current task... Progressive disclosure."

Benefits:
- **Security**: Server never executes code
- **Remote-ready**: Works with remote MCP servers
- **Agent control**: Code runs in agent's environment
- **Efficiency**: No script bloat in context windows

## Development & Testing

### Running Tests

```bash
# Run all tests (34 total, ~3 seconds)
npm test

# Individual test suites
npm run test:server      # MCP server tests (16 tests)
npm run test:ts-script   # TypeScript script tests (11 tests)
npm run test:py-script   # Python script tests (7 tests)
```

**Test Coverage:**
- ✅ Server resources, prompts, and tools (100%)
- ✅ Script structure and syntax validation (100%)
- ✅ Script compilation (TypeScript → JavaScript, Python bytecode)

### Interactive Development

**FastMCP Dev Mode** - Interactive CLI testing:
```bash
npm run dev
```

**MCP Inspector** - Visual web UI at `http://localhost:6274`:
```bash
npm run inspect
```

### Python Test Setup (First Time)

```bash
python3 -m venv .venv-test
source .venv-test/bin/activate
pip install -r tests/requirements.txt
```

### Troubleshooting

**"Module not found" errors:**
```bash
npm run build  # Rebuild dist/ directory
```

**Python tests fail:**
```bash
rm -rf .venv-test
python3 -m venv .venv-test
source .venv-test/bin/activate
pip install -r tests/requirements.txt
```

## License

Apache-2.0

## Links

- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Cloudflare: Code Mode](https://blog.cloudflare.com/code-mode/)
