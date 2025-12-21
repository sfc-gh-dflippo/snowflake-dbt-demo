# name: Task Master AI - Setup & Configuration

# description: Complete installation and configuration guide for Task Master AI covering npm installation, MCP setup for Cursor/VS Code/Windsurf, API key configuration, model selection, and project initialization.

# Task Master AI - Setup & Configuration

Complete guide for installing and configuring Task Master AI for AI agents integration.

## Installation Methods

### Method 1: Global Installation (Recommended)

```bash
npm install -g task-master-ai
```

**Benefits:**

- Available in any project
- Single installation
- Easy updates

### Method 2: Project-Local Installation

```bash
npm install task-master-ai
```

**Benefits:**

- Project-specific version
- Included in package.json
- Version control

### Method 3: Direct Usage (No Installation)

```bash
npx task-master-ai init
```

**Benefits:**

- No installation required
- Always latest version
- Quick testing

## MCP Configuration

### Cursor IDE

**Location:** `~/.cursor/mcp.json` (global) or `<project>/.cursor/mcp.json` (project)

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "PERPLEXITY_API_KEY": "pplx-...",
        "OPENAI_API_KEY": "sk-...",
        "GOOGLE_API_KEY": "AI...",
        "MISTRAL_API_KEY": "...",
        "OPENROUTER_API_KEY": "sk-or-..."
      }
    }
  }
}
```

**Enable in Cursor:**

1. Open Cursor Settings (Ctrl+Shift+J)
2. Click MCP tab
3. Enable task-master-ai toggle

### VS Code

**Location:** `<project>/.vscode/mcp.json`

```json
{
  "servers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "PERPLEXITY_API_KEY": "pplx-..."
      },
      "type": "stdio"
    }
  }
}
```

### Windsurf

**Location:** `~/.codeium/windsurf/mcp_config.json`

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "PERPLEXITY_API_KEY": "pplx-..."
      }
    }
  }
}
```

## API Keys

### Required Keys

**Anthropic (Required for main operations):**

```bash
ANTHROPIC_API_KEY=sk-ant-...
```

Get from: https://console.anthropic.com/

**Perplexity (Required for research):**

```bash
PERPLEXITY_API_KEY=pplx-...
```

Get from: https://www.perplexity.ai/settings/api

### Optional Keys

**OpenAI:**

```bash
OPENAI_API_KEY=sk-...
```

**Google (Gemini):**

```bash
GOOGLE_API_KEY=AI...
```

**Mistral:**

```bash
MISTRAL_API_KEY=...
```

**OpenRouter:**

```bash
OPENROUTER_API_KEY=sk-or-...
```

**Groq:**

```bash
GROQ_API_KEY=gsk_...
```

**xAI:**

```bash
XAI_API_KEY=xai-...
```

**Azure OpenAI:**

```bash
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://...
```

**Ollama (Local):**

```bash
OLLAMA_API_KEY=...
OLLAMA_BASE_URL=http://localhost:11434/api
```

## Project Initialization

### Interactive Setup

```bash
task-master init
```

Prompts for:

- Project name
- Description
- Version
- Author
- Rule profiles (cursor, windsurf, vscode, etc.)

### Quick Setup (Non-Interactive)

```bash
task-master init --yes
```

Uses defaults for all settings.

### With Rule Profiles

```bash
task-master init --rules cursor,windsurf
```

Available profiles:

- `cursor` - Cursor IDE rules
- `windsurf` - Windsurf IDE rules
- `vscode` - VS Code rules
- `claude` - Claude Code rules
- `cline` - Cline rules
- `roo` - Roo Code rules
- `trae` - Trae rules

### Project Structure Created

```
.taskmaster/
├── config.json          # Configuration
├── state.json           # Current state
├── tasks/
│   └── tasks.json       # Task definitions
├── docs/
│   ├── prd.txt          # Your PRD (create this)
│   └── research/        # Research outputs
├── reports/
│   └── task-complexity-report.json
└── templates/
    └── example_prd.txt  # Example PRD
```

## Model Configuration

### View Current Configuration

```bash
task-master models
```

### Interactive Setup

```bash
task-master models --setup
```

### Set Specific Models

```bash
# Set main model
task-master models --set-main claude-3-5-sonnet-20241022

# Set research model
task-master models --set-research perplexity/sonar-pro

# Set fallback model
task-master models --set-fallback gpt-4o
```

### Custom Models

**Ollama:**

```bash
task-master models --set-main llama3.1 --ollama
```

**OpenRouter:**

```bash
task-master models --set-main anthropic/claude-3.5-sonnet --openrouter
```

### Claude Code (No API Key Required)

```bash
task-master models --set-main claude-code/sonnet
```

Requires Claude Code CLI installed.

## Configuration Files

### .taskmaster/config.json

Primary configuration file (auto-generated):

```json
{
  "project": {
    "name": "my-project",
    "description": "Project description",
    "version": "1.0.0"
  },
  "ai": {
    "models": {
      "main": "claude-3-5-sonnet-20241022",
      "research": "perplexity/sonar-pro",
      "fallback": "gpt-4o"
    },
    "parameters": {
      "maxTokens": 8000,
      "temperature": 0.7
    }
  },
  "global": {
    "defaultTag": "master",
    "defaultSubtasks": 5,
    "defaultPriority": "medium"
  },
  "logging": {
    "level": "info"
  }
}
```

**⚠️ Warning:** Do not edit manually. Use `task-master models` commands.

### .taskmaster/state.json

Tracks current state (auto-managed):

```json
{
  "currentTag": "master",
  "lastSwitched": "2025-01-18T10:30:00Z",
  "migrationNoticeShown": true
}
```

### Environment Variables (.env)

For CLI usage, create `.env` in project root:

```bash
# AI Provider Keys
ANTHROPIC_API_KEY=sk-ant-...
PERPLEXITY_API_KEY=pplx-...
OPENAI_API_KEY=sk-...

# Optional
GOOGLE_API_KEY=AI...
MISTRAL_API_KEY=...
OPENROUTER_API_KEY=sk-or-...
```

## Rules Management

### Add Rules After Init

```bash
task-master rules add windsurf,roo
```

### Remove Rules

```bash
task-master rules remove vscode
```

### Interactive Setup

```bash
task-master rules setup
```

### Rule Structure

Each profile creates its directory:

- `.cursor/rules/` - Cursor IDE
- `.windsurf/rules/` - Windsurf IDE
- `.vscode/rules/` - VS Code
- `.roo/rules/` - Roo Code
- etc.

## Verification

### Test MCP Connection

In your IDE's AI chat:

```
Initialize taskmaster-ai in my project
```

Should respond with setup confirmation.

### Test CLI

```bash
task-master list
```

Should show empty task list or existing tasks.

### Check Configuration

```bash
task-master models
```

Should display current model configuration.

## Troubleshooting

### MCP Server Not Responding

1. Check API keys in MCP config
2. Restart your IDE
3. Verify `npx task-master-ai` works in terminal
4. Check MCP settings shows tools enabled

### CLI Commands Fail

```bash
# Try with Node directly
node node_modules/task-master-ai/scripts/init.js

# Or clone and run
git clone https://github.com/eyaltoledano/claude-task-master.git
cd claude-task-master
node scripts/init.js
```

### API Key Issues

**MCP:** Keys must be in `env` section of MCP config **CLI:** Keys must be in `.env` file in project
root

### Model Configuration Issues

```bash
# Reset to defaults
task-master models --setup

# Verify keys are set
task-master models
```

### Permission Errors

```bash
# Global install with sudo (macOS/Linux)
sudo npm install -g task-master-ai

# Or use npx without install
npx task-master-ai init
```

## Best Practices

1. **API Keys**

   - Use environment-specific keys
   - Never commit keys to git
   - Add `.env` to `.gitignore`

2. **Model Selection**

   - Use Claude for main operations
   - Use Perplexity for research
   - Set appropriate fallback

3. **Project Setup**

   - Initialize at project root
   - Create comprehensive PRD first
   - Configure rules for your IDE

4. **MCP Configuration**
   - Use project-level config for team projects
   - Use global config for personal projects
   - Restart IDE after config changes

## Updates

### Update Global Installation

```bash
npm update -g task-master-ai
```

### Update Project Installation

```bash
npm update task-master-ai
```

### Check Version

```bash
task-master --version
```

## References

- [Task Master GitHub](https://github.com/eyaltoledano/claude-task-master)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Anthropic API](https://docs.anthropic.com)
- [Perplexity API](https://docs.perplexity.ai)
