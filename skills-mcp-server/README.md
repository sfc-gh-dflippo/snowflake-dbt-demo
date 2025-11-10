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

**Published package:** `@sfc-gh-dflippo/skills-mcp-server` on [GitHub Package Registry](https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/pkgs/npm/skills-mcp-server)

**Setup authentication:**

GitHub Package Registry requires authentication to download packages.

1. **Create a GitHub Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scope: `read:packages`
   - Copy the token

2. **Configure npm:**
   
   **Option A: If you already have a `GITHUB_API_KEY` environment variable:**
   ```bash
   cat > ~/.npmrc << EOF
   @sfc-gh-dflippo:registry=https://npm.pkg.github.com
   //npm.pkg.github.com/:_authToken=${GITHUB_API_KEY}
   EOF
   ```
   
   **Option B: Replace token manually:**
   ```bash
   cat > ~/.npmrc << 'EOF'
   @sfc-gh-dflippo:registry=https://npm.pkg.github.com
   //npm.pkg.github.com/:_authToken=YOUR_GITHUB_TOKEN
   EOF
   ```
   Replace `YOUR_GITHUB_TOKEN` with your token.

3. **Add to `.cursor/mcp.json`:**
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

4. **Restart Cursor** to load the MCP server.

### Troubleshooting Installation

**Error: `404 Not Found - GET https://registry.npmjs.org/@sfc-gh-dflippo%2fskills-mcp-server`**

This error means npm is looking for the package on the public npm registry instead of GitHub Package Registry.

**Solution:** Configure npm to use GitHub Package Registry for the `@sfc-gh-dflippo` scope:

1. Check if you have `~/.npmrc` configured:
   ```bash
   cat ~/.npmrc
   ```

2. If the file doesn't exist or is missing the configuration, create it:
   
   **Option A: If you have `GITHUB_API_KEY` environment variable:**
   ```bash
   cat > ~/.npmrc << EOF
   @sfc-gh-dflippo:registry=https://npm.pkg.github.com
   //npm.pkg.github.com/:_authToken=${GITHUB_API_KEY}
   EOF
   ```
   
   **Option B: Manual token:**
   ```bash
   cat > ~/.npmrc << 'EOF'
   @sfc-gh-dflippo:registry=https://npm.pkg.github.com
   //npm.pkg.github.com/:_authToken=YOUR_GITHUB_TOKEN
   EOF
   ```
   Replace `YOUR_GITHUB_TOKEN` with your token.

3. Verify the file was created correctly:
   ```bash
   cat ~/.npmrc
   ```
   You should see your registry and token configuration.

4. Restart Cursor and try again

**Still not working?**

Verify your token has the `read:packages` permission:
- Go to: https://github.com/settings/tokens
- Click on your token
- Ensure `read:packages` is checked

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

### Local Development Setup

If you're contributing to the server or need to test changes:

1. **Clone and build:**
   ```bash
   cd skills-mcp-server
   npm install
   npm run build
   ```

2. **Use local build in `.cursor/mcp.json`:**
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
   **Note:** Path is relative to workspace root (where `.cursor/` folder is).

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
