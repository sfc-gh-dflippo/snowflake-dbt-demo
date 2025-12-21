---
name: dbt-core
description:
  Managing dbt-core locally - installation, configuration, project setup, package management,
  troubleshooting, and development workflow. Use this skill for all aspects of local dbt-core
  development including non-interactive scripts for environment setup with conda or venv, and
  comprehensive configuration templates for profiles.yml and dbt_project.yml.
---

# dbt-core Local Development Guide

## Purpose

Guide AI agents through a systematic, user-choice-driven installation process for dbt-core on local
machines. The agent runs diagnostic scripts, presents options to users, and executes non-interactive
installation scripts based on user preferences.

## When to Use This Skill

Activate this skill when users ask about:

- Installing dbt-core and dbt-snowflake
- Configuring profiles.yml for Snowflake
- Setting up authentication (PAT, SSO, key pair, OAuth)
- Installing and managing dbt packages
- Troubleshooting connection issues
- Initializing new dbt projects
- Verifying installation and configuration
- Upgrading dbt versions

**Official dbt Documentation**:
[Install dbt](https://docs.getdbt.com/docs/core/installation-overview)

---

## AI Agent Workflow

**IMPORTANT**: This skill uses non-interactive scripts. The AI agent must:

1. Run diagnostic scripts to check the environment
2. Present options to the user based on findings
3. Execute the script chosen by the user
4. Guide the user through next steps

### Step 1: Check Environment

**AI Agent Action**: Run the check script to assess what's already installed:

**macOS/Linux:**

```bash
cd .claude/skills/dbt-core/scripts/
./check-environment.sh
```

**Windows:**

```cmd
cd .claude\skills\dbt-core\scripts\
check-environment.bat
```

**What It Checks:**

- conda installation status
- Python installation and version compatibility (3.9-3.12)
- dbt installation status
- curl availability (for downloads)

**Output**: Structured summary with recommendations for next steps.

### Step 2: Present Options to User

Based on the check results, the AI agent should **ask the user** which installation path they
prefer:

**If conda is NOT installed:**

- Option A: Install Miniforge (recommended, free, conda-forge channel)
- Option B: Install Miniconda (minimal, defaults channel)
- Option C: Skip conda and use Python venv (if Python 3.9-3.12 is installed)

**If conda IS installed:**

- Option A: Create conda environment for dbt
- Option B: Create venv environment for dbt (if Python is also available)

**If dbt is already installed:**

- Show version information
- Offer to update or reconfigure

### Step 3: Execute User's Choice

**AI Agent Action**: Run the appropriate script from `scripts/` folder (use `.sh` for macOS/Linux,
`.bat` for Windows):

| Option                   | Script              | Action After                                | User Action                                                                     |
| ------------------------ | ------------------- | ------------------------------------------- | ------------------------------------------------------------------------------- |
| **A: Install Miniforge** | `install-miniforge` | Restart terminal, rerun `check-environment` | None                                                                            |
| **B: Install Miniconda** | `install-miniconda` | Restart terminal, rerun `check-environment` | None                                                                            |
| **C: Setup Conda Env**   | `setup-conda-env`   | Instruct user to activate                   | `conda activate dbt`                                                            |
| **D: Setup Venv Env**    | `setup-venv-env`    | Instruct user to activate                   | `source .venv/bin/activate` (macOS/Linux)<br>`.venv\Scripts\activate` (Windows) |

**Example execution**:

```bash
cd .claude/skills/dbt-core/scripts/
./install-miniforge.sh  # or install-miniforge.bat on Windows
```

### Step 4: Next Steps

**AI Agent Action**: Once dbt is installed and verified, guide user to configure Snowflake
connection (see profiles.yml configuration section below).

---

## Available Scripts

All scripts are in the `scripts/` folder and are non-interactive for AI agent execution:

### Diagnostic Script

- **`check-environment.sh/.bat`** - Comprehensive environment check that:
  - Scans all conda environments for dbt installations
  - Shows dbt-core and dbt-snowflake versions
  - Activates appropriate environment (prefers those with dbt-snowflake)
  - Verifies dbt installation and functionality
  - Tests dbt commands
  - Provides recommendations for next steps

### Installation Scripts

- `install-miniforge.sh/.bat` - Install Miniforge (conda-forge)
- `install-miniconda.sh/.bat` - Install Miniconda
- `setup-conda-env.sh/.bat` - Create conda environment from `dbt-conda-env.yml`
- `setup-venv-env.sh/.bat` - Create venv environment from `requirements.txt`

### Environment Files (also in `scripts/` folder)

- `dbt-conda-env.yml` - Conda environment specification
- `requirements.txt` - pip requirements for venv

### Sample Configuration Files (in `samples/` folder)

- `profiles.yml.sample` - Snowflake connection configuration examples
- `dbt_project.yml.sample` - dbt project configuration patterns
- `packages.yml.sample` - Package dependencies
- `gitignore.sample` - Version control setup

---

## Manual Installation

For manual installation instructions, review the automated scripts (see AI Agent Workflow above) or
refer to:

- **Official dbt Docs**:
  [Core Installation](https://docs.getdbt.com/docs/core/installation-overview)
- **Environment files in `scripts/` folder**: `dbt-conda-env.yml` (conda) or `requirements.txt`
  (pip/venv)

---

## Snowflake Configuration & Authentication

**All profiles.yml configuration and authentication methods are documented in**:
`samples/profiles.yml.sample`

The sample file includes:

- **Complete profiles.yml examples** for all authentication methods
- **PAT (Programmatic Access Token)** generation using Snowflake CLI (recommended)
- **SSO authentication** with externalbrowser
- **Key pair authentication** with setup instructions
- **OAuth authentication**
- **Multi-environment configurations** (dev, prod)
- **Account identifier formats** (preferred account name and legacy locator formats)
- **Configuration tips** for warehouses, threads, and schemas

**To configure**:

1. Copy `samples/profiles.yml.sample` to `~/.dbt/profiles.yml`
2. Update with your Snowflake account details
3. Choose and configure your authentication method
4. Test with `dbt debug`

**Official dbt Docs**:
[profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml)

---

## Package Installation

Copy `samples/packages.yml.sample` to your project root as `packages.yml`, then run `dbt deps`.

**Official dbt Docs**: [Package Management](https://docs.getdbt.com/docs/build/packages)

---

## Verify Installation

Run the diagnostic script to verify installation and test connection:

```bash
# macOS/Linux
cd scripts/
./check-environment.sh

# Windows
cd scripts\
check-environment.bat
```

This script checks dbt installation, tests commands, and validates the dbt-snowflake adapter. For
manual verification, use `dbt debug`.

---

## Troubleshooting

**Connection issues**: Run `dbt debug` and check:

- Environment variables set (`DBT_ENV_SECRET_SNOWFLAKE_PAT`)
- `~/.dbt/profiles.yml` exists and configured correctly
- Snowflake connectivity: `snow sql -q "SELECT CURRENT_USER()"`

**Package issues**: `rm -rf dbt_packages/ && dbt deps --upgrade`

**Python compatibility**: dbt requires Python 3.9-3.12

**For detailed troubleshooting**: See `samples/profiles.yml.sample`

**Official Docs**:
[Network Issues](https://docs.snowflake.com/en/user-guide/troubleshooting-network)

---

## Project Initialization

```bash
# Non-interactive (recommended for AI agents)
dbt init my_project_name --skip-profile-setup

# Configure ~/.dbt/profiles.yml separately (see samples/profiles.yml.sample)
# Configure project with dbt_project.yml (see samples/dbt_project.yml.sample)
```

**Project structure**: models/, tests/, macros/, seeds/, snapshots/

---

## dbt_project.yml Configuration

**All project configuration patterns are documented in**: `samples/dbt_project.yml.sample`

The sample file includes:

- **Basic project setup** (name, version, profile connection)
- **Project paths** (models, tests, macros, seeds, snapshots)
- **Global hooks** (on-run-start, on-run-end)
- **Global variables** for project-wide settings
- **Model configurations** with materialization defaults
- **Medallion architecture pattern** (bronze/silver/gold layers)
- **Basic structure pattern** (staging/marts)
- **Snapshot configurations** for SCD Type 2
- **Test configurations** with failure storage
- **Common patterns** (incremental facts, Python models, dynamic tables)

**To configure**:

1. Copy `samples/dbt_project.yml.sample` to your project root as `dbt_project.yml`
2. Update `name` to match your project name
3. Update `profile` to match your profiles.yml profile name
4. Choose your architecture pattern (basic or medallion)
5. Customize materializations and schemas
6. Run `dbt debug` to verify configuration

**Official dbt Docs**: [dbt_project.yml](https://docs.getdbt.com/reference/dbt_project.yml)

---

## Development Workflow

### 1. Initial Setup

```bash
# Install packages
dbt deps

# Verify connection
dbt debug

# Load seed data (if any)
dbt seed
```

---

### 2. Development Cycle

```bash
# Build specific model
dbt build --select model_name

# Build with dependencies
dbt build --select +model_name+

# Build entire project
dbt build
```

---

### 3. Deploy to Production

```bash
# Build against production target
dbt build --target prod

# Test production
dbt test --target prod

# Generate documentation
dbt docs generate --target prod
```

---

## Best Practices

- **Use virtual environments** (conda or venv) for isolation
- **Separate dev/prod configs** - Use `{{ env_var('SCHEMA_NAME', 'DEFAULT_NAME') }}` to allow
  overriding of schema names
- **Version control** - See `samples/gitignore.sample` for what to commit/ignore
- **Never commit** `profiles.yml` or `.env` files (contain credentials)

---

## Upgrade dbt Version

```bash
# Upgrade to latest
pip install --upgrade dbt-core dbt-snowflake

# Or specific version (for dbt Projects on Snowflake: 1.9.4 / 1.9.2)
pip install dbt-core==1.9.4 dbt-snowflake==1.9.2
```

Check [Migration Guides](https://docs.getdbt.com/docs/dbt-versions/core-upgrade) for breaking
changes and test in dev first.

---

## Related Official Documentation

- [dbt Docs: Installation](https://docs.getdbt.com/docs/core/installation-overview)
- [dbt Docs: profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml)
- [dbt Docs: Environment Variables](https://docs.getdbt.com/docs/build/environment-variables)
- [Snowflake Docs: dbt](https://docs.snowflake.com/en/user-guide/data-engineering/dbt)
- [Snowflake Docs: PAT](https://docs.snowflake.com/en/user-guide/programmatic-access-tokens)

---

**Goal**: Transform AI agents into expert dbt setup specialists who guide users through
installation, configuration, authentication, and troubleshooting with clear, actionable instructions
and best practices.
