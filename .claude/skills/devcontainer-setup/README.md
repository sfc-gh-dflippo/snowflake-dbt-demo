# Universal DevContainer Setup

Create "kitchen sink" development containers for AI agentic workflows with comprehensive tooling.

**Supports both ARM64 (Apple Silicon) and x86_64 (Intel/AMD) architectures.**

## What's Included

### Base Configuration

- **Base image** - `mcr.microsoft.com/devcontainers/python:3.13-bookworm` (includes Python 3.13, zsh, oh-my-zsh, vscode user)
- **Node.js 25** - via devcontainers/features/node
- **Java 25 + Maven & Gradle** - via devcontainers/features/java
- **Java 25.0.1 (Temurin)** - via devcontainers/features/java
- **Rust** - via devcontainers/features/rust
- **Docker-in-Docker** - for container operations
- **GitHub CLI** - for repo operations
- **Git, Git LFS** - for version control

### Custom Feature: snowflake-ai-tools

The `./snowflake-ai-tools` feature installs AI and data tools. It requires Node.js feature to be installed first (declared via `installsAfter`). Python is managed via uv.

**Feature Options:**

```json
"./snowflake-ai-tools": {
  "installSnowflakeCli": true,
  "installSchemachange": true,
  "installClaudeCode": true,
  "installCortexCode": true,
  "installRipgrep": true,
  "remoteUser": "vscode"
}
```

**Build Phase (install.sh as root):**

- **Package manager detection** - Works with apt-get, apk, dnf, yum
- **User detection** - Uses `$_REMOTE_USER` or detects dynamically
- **uv** - Fast Python package manager
- **Snowflake CLI** - via `uv tool install`
- **schemachange** - via `uv tool install`
- **Claude Code CLI** - AI coding assistant
- **Cortex Code CLI** - Snowflake AI agent (Private Preview, requires Node.js)
- **ripgrep** - Fast recursive text search (rg)
- **Build tools** - fzf, jq

**Post-Create Phase (snowflake-ai-tools-setup as user):**

- Creates Python venv at `~/.venv/dbt` using uv
- Installs project dependencies from `requirements.txt` or defaults
- Configures shell auto-activation
- Updates AI tools
- Fixes permissions

**Feature Installation Order:**

The devcontainer installs features in dependency order: Node.js → snowflake-ai-tools (others in parallel). Python 3.13 is installed via `uv python install` in the onCreateCommand.

### Cache Mounts

| Mount         | Provided By                |
| ------------- | -------------------------- |
| ~/.m2 (Maven) | devcontainer.json          |
| ~/.npm        | devcontainer.json          |
| ~/.cargo      | devcontainer.json          |
| ~/.cache/uv   | snowflake-ai-tools feature |
| ~/.snowflake  | snowflake-ai-tools feature |
| ~/.claude     | snowflake-ai-tools feature |
| ~/.cursor     | snowflake-ai-tools feature |

## File Structure

```text
.devcontainer/
├── devcontainer.json       # Base config, mounts, env vars, extensions
└── snowflake-ai-tools/
    ├── devcontainer-feature.json  # Feature metadata and options
    └── install.sh                  # Multi-distro installer + post-create script
```

## Compatibility

### Supported Base Images

| Base Image                                           | Package Manager | Status    |
| ---------------------------------------------------- | --------------- | --------- |
| mcr.microsoft.com/devcontainers/python:3.13-bookworm | apt-get         | Tested    |
| mcr.microsoft.com/devcontainers/base:debian          | apt-get         | Supported |
| mcr.microsoft.com/devcontainers/base:alpine          | apk             | Supported |
| fedora                                               | dnf             | Supported |
| centos/rhel                                          | yum             | Supported |

### Architecture Support

| Architecture                        | Status |
| ----------------------------------- | ------ |
| ARM64 (Apple Silicon, AWS Graviton) | Native |
| x86_64 (Intel/AMD)                  | Native |

### Limitations

1. **Mount paths** - Mounts in devcontainer.json require hardcoded container paths (e.g., `/home/vscode`). If using a different user, update the paths.

2. **containerEnv paths** - Same limitation as mounts.

3. **python.defaultInterpreterPath** - Points to `/home/vscode/.venv/dbt/bin/python`. Update if using different user.

## Python Environment

The setup uses `uv` for fast Python package management:

- Virtual environment created at `~/.venv/dbt`
- Auto-activated on container start and new terminal sessions
- Uses `requirements.txt` from project root (or creates default packages)

To add packages:

```bash
uv pip install package-name
```
