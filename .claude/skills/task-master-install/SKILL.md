---
name: task-master-install
description: Install and initialize task-master for AI-powered task management and specification-driven development. Use this skill when users ask you to parse a new PRD, when starting a new project that needs structured task management, when users mention wanting task breakdown or project planning, or when implementing specification-driven development workflows.
---

# Task Master Install

## Overview

Task-master is an AI-powered task management system for breaking down complex projects into manageable tasks and subtasks. It supports PRD parsing, complexity analysis, and specification-driven development workflows.

## Installation

### Step 1: Check if already installed:

```bash
task-master --version
```

If task-master is already installed and the project has a `.taskmaster/` folder, you are finished.

### Step 2: If you need to install Task-Master:

**Global installation (recommended):**
```bash
npm install -g task-master-ai
```

**Local/npx alternative:**
```bash
npx task-master-ai init
```

### Step 3: If you don't have a `.taskmaster/` folder in your project

```bash
task-master init
```

**Common flags:**
- `--name <name>` - Set project name
- `--description <text>` - Set project description
- `--version <version>` - Set initial version (e.g., '0.1.0')
- `--rules <profiles>` - Specify rule profiles (e.g., `cursor,windsurf`)
- `-y, --yes` - Skip prompts, use defaults

**Example:**
```bash
task-master init --name "My Project" --description "AI-powered web app" --version "0.1.0" --rules cursor,windsurf --yes
```

## What Happens During Init

Task-master init automatically creates:
- `.taskmaster/` directory structure (config, tasks, docs, reports, templates)
- Rule files for AI coding assistants (`.cursor/rules/`, etc.)
- Configures AI provider and models to use: Cortex-Code, Claude-Code, Gemini-CLI, Codex-CLI, API, etc.

**The bootstrapped rules guide all future task-master workflows** - no additional setup needed.

## Troubleshooting

**Node.js not found** - Install Node.js v16+ using:
- Windows (with admin): `winget install OpenJS.NodeJS`
- macOS: `brew install node`
- Linux: `sudo apt install nodejs npm` (Debian/Ubuntu) or `sudo yum install nodejs` (RHEL/CentOS)
- Download installer: [nodejs.org](https://nodejs.org/)

**Installation issues** - Uninstall and reinstall globally:
```bash
npm uninstall -g task-master-ai
npm install -g task-master-ai
```
Then restart terminal and verify with `task-master --version`

**Permission errors:**
- Unix/macOS: Install via nvm using `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash`, restart terminal, and run `nvm install 24`
- Windows without admin: Use Node.js installer's "Install for me only" option
