# Skills MCP Server

An MCP (Model Context Protocol) server built with [FastMCP](https://github.com/punkpeye/fastmcp) that provides AI agent skills management through downloadable sync scripts.

## Architecture

This server follows the **resource pattern** recommended by Anthropic and Cloudflare:

- **Exposes scripts as MCP resources** (not direct tool calls)
- **Agents download scripts** and execute them locally
- **Server never executes code** - just serves script content
- **Works even if server is remote** - no local file dependencies

## How It Works

```
┌─────────┐                  ┌──────────────┐
│  Agent  │                  │  MCP Server  │
└────┬────┘                  └──────┬───────┘
     │                              │
     │  1. List resources           │
     ├─────────────────────────────>│
     │                              │
     │  2. Returns: script://sync-  │
     │     skills.py, etc.          │
     │<─────────────────────────────┤
     │                              │
     │  3. Read resource:           │
     │     script://sync-skills.py  │
     ├─────────────────────────────>│
     │                              │
     │  4. Returns: full Python     │
     │     script content (10KB)    │
     │<─────────────────────────────┤
     │                              │
     │  5. Write to local file      │
     │     sync-skills.py           │
     │                              │
     │  6. Execute: python3         │
     │     sync-skills.py           │
     │                              │
```

The agent is responsible for:
1. Fetching the script
2. Writing it to a local file
3. Executing it in the local environment

The server is responsible for:
1. Listing available scripts
2. Serving script content on demand
3. **NOT executing anything**

## Available Resources

### Scripts

- `script://sync-skills.py` - Python sync script (10KB)
  - Clones/pulls GitHub repos
  - Scans for SKILL.md files
  - Updates AGENTS.md
  - Usage: `python3 sync-skills.py`

- `script://sync-skills.ts` - TypeScript sync script (11KB)
  - Same functionality as Python version
  - Zero external dependencies (Node.js built-ins only)
  - Usage: `tsx sync-skills.ts`

### Documentation

- `doc://manage-repositories` - How to add and remove GitHub repositories

## Configuration

Scripts read configuration from `.skills/repos.txt`:

```
# One repository URL per line
https://github.com/anthropics/skills
https://github.com/your-org/custom-skills
```

## Installation

### For MCP Clients

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "skills": {
      "command": "node",
      "args": ["/path/to/skills-mcp-server/dist/index.js"]
    }
  }
}
```

### For Cursor

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

**Note:** Cursor currently doesn't expose MCP resources to agents. See [Known Limitations](#known-limitations) below.

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Develop with FastMCP CLI (interactive testing)
npm run dev

# Test (verifies resources work correctly)
npm run test
```

## Testing

Three test suites validate the complete server:

```bash
npm test  # Runs all tests (34 total)
```

**Test Breakdown:**
- **TypeScript Server Tests** (16 tests) - Tests MCP server resources, prompts, and tools
- **TypeScript Script Tests** (11 tests) - Tests TypeScript sync script structure and compilation
- **Python Script Tests** (7 tests) - Tests Python sync script structure and syntax

**Individual test suites:**
```bash
npm run test:server      # TypeScript MCP server tests
npm run test:ts-script   # TypeScript sync script tests
npm run test:py-script   # Python sync script tests
```

**Interactive Testing:**
```bash
npm run dev     # FastMCP dev mode (interactive CLI)
npm run inspect # MCP Inspector (web UI at http://localhost:6274)
```

See [TESTING.md](./TESTING.md) for detailed testing guide.

## Why This Approach?

From [Anthropic's blog](https://www.anthropic.com/engineering/code-execution-with-mcp):

> "agents can load only the definitions they need for the current task... Progressive disclosure."

From [Cloudflare's blog](https://blog.cloudflare.com/code-mode/):

> "LLMs are better at writing code to call MCP, than at calling MCP directly."

### Benefits

1. **Progressive Disclosure**: Agents load only what they need
2. **Context Efficiency**: No script bloat in context windows
3. **Remote-Ready**: Works with remote servers
4. **Execution Isolation**: Code runs in agent's environment, not server's
5. **Security**: Server can't execute arbitrary code

## What the Scripts Do

Both Python and TypeScript scripts:

1. **Read Configuration** - Load repository URLs from `.skills/repos.txt`
2. **Sync Repositories** - Clone new repos or `git pull` existing ones (efficient!)
3. **Scan for Skills** - Find `SKILL.md` files in:
   - Project root (local skills)
   - `.skills/repositories/` (remote skills)
4. **Apply Precedence** - Local skills override remote skills with same name
5. **Update AGENTS.md** - Generate skills catalog between markers

## License

Apache-2.0

## Links

- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Cloudflare: Code Mode](https://blog.cloudflare.com/code-mode/)
