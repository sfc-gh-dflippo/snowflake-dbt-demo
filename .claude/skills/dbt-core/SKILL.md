---
name: dbt-core
description:
  Managing dbt locally - installing dbt 2.0 (Fusion) via the official installer, configuration,
  project setup, package management, troubleshooting, and development workflow, with configuration
  templates for profiles.yml and dbt_project.yml.
---

# dbt Local Development Guide (Fusion / dbt 2.0)

## Purpose

Guide AI agents through installing and configuring dbt on local machines using the **dbt Fusion
engine (dbt 2.0)**. Fusion is a single standalone Rust binary — there is no Python requirement, no
conda, and no separate `dbt-snowflake` adapter package to install. The agent runs a diagnostic
script, installs Fusion via the official installer, and guides the user through Snowflake
configuration.

## When to Use This Skill

Activate this skill when users ask about:

- Installing the dbt Fusion engine (dbt 2.0)
- Configuring profiles.yml for Snowflake
- Setting up authentication (PAT, SSO, key pair, OAuth)
- Installing and managing dbt packages
- Troubleshooting connection issues
- Initializing new dbt projects
- Verifying installation and configuration
- Upgrading dbt versions

**Official dbt Documentation**:
[Install dbt](https://docs.getdbt.com/docs/core/installation-overview) ·
[dbt Projects on Snowflake](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake)

---

## AI Agent Workflow

**IMPORTANT**: This skill uses non-interactive scripts. The AI agent must:

1. Run the diagnostic script to check the environment
2. Install the Fusion engine if dbt is missing or not on version 2.0.x
3. Verify the installation
4. Guide the user through next steps

### Step 1: Check Environment

**AI Agent Action**: Run the check script to see whether dbt Fusion is already installed:

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

- Whether `dbt` is on PATH
- Whether `dbt --version` reports the Fusion engine (2.0.x)
- snowflake-cli availability (optional, separate tool)
- curl availability (required by the installer)

**Output**: Structured summary with a recommendation for next steps.

### Step 2: Install the dbt Fusion Engine

If dbt is not installed (or is not the Fusion 2.0.x engine), run the installer. Fusion installs to a
per-user location and does **not** require sudo/admin.

**macOS/Linux** — installs to `$HOME/.local/bin`, updates PATH, and sets a `dbtf` alias:

```bash
cd .claude/skills/dbt-core/scripts/
./install-dbt.sh
```

Equivalent one-liner:

```bash
curl -fsSL https://public.cdn.getdbt.com/fs/install/install.sh | sh -s -- --update
```

**Windows PowerShell** — installs to `%USERPROFILE%\.local\bin` and updates the user PATH (no admin
required):

```powershell
cd .claude\skills\dbt-core\scripts\
.\install-dbt.ps1
```

Equivalent one-liner:

```powershell
irm https://public.cdn.getdbt.com/fs/install/install.ps1 | iex
```

### Step 3: Verify

Open a new terminal (so PATH changes take effect) and confirm the Fusion engine is active:

```bash
dbt --version
# Expect: dbt-fusion 2.0.0-preview.x
```

### Step 4: Next Steps

**AI Agent Action**: Once dbt is installed and verified, guide the user to configure their Snowflake
connection (see the profiles.yml configuration section below).

---

## Available Scripts

All scripts are in the `scripts/` folder and are non-interactive for AI agent execution:

### Diagnostic Script

- **`check-environment.sh/.bat`** - Environment check that:
  - Confirms `dbt` is on PATH
  - Reports the dbt version and verifies it is the Fusion engine (2.0.x)
  - Checks for the optional snowflake-cli tool and curl
  - Provides a recommendation for next steps

### Installation Scripts

- `install-dbt.sh` - Install the dbt Fusion engine on macOS/Linux, then print `dbt --version`
- `install-dbt.ps1` - Install the dbt Fusion engine on Windows (no admin), then print
  `dbt --version`

### Supporting Files (also in `scripts/` folder)

- `requirements.txt` - Optional supporting Python tools (snowflake-cli, Snowpark, Streamlit, etc.).
  dbt itself is **not** installed here — it comes from the Fusion installer.

---

## Manual Installation

Fusion is a standalone binary installed by the official installer (see Step 2 above). Fusion does
**not** require Python. If you specifically want the Python distribution of dbt 2.0 instead of the
standalone binary, `pip install --pre dbt` is an optional alternative.

- **Official dbt Docs**:
  [Core Installation](https://docs.getdbt.com/docs/core/installation-overview)

---

## Snowflake Configuration & Authentication

Configure your Snowflake connection in `~/.dbt/profiles.yml`. The
[profiles.yml documentation](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml)
covers all authentication methods:

- **PAT (Programmatic Access Token)** — generate with the Snowflake CLI (recommended)
- **SSO authentication** with `authenticator: externalbrowser`
- **Key pair authentication**
- **OAuth authentication**
- **Multi-environment configurations** (dev, prod) via targets
- **Account identifier formats** (preferred account name and legacy locator formats)

**To configure**:

1. Create `~/.dbt/profiles.yml` with your Snowflake account details
2. Choose and configure your authentication method
3. Test with `dbt debug`

**Official dbt Docs**:
[Snowflake setup](https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup) ·
[profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml)

---

## Package Installation

Add a `packages.yml` to your project root, then run `dbt deps`.

**Official dbt Docs**: [Package Management](https://docs.getdbt.com/docs/build/packages)

---

## Verify Installation

Run the diagnostic script to verify the Fusion engine is installed:

```bash
# macOS/Linux
cd scripts/
./check-environment.sh

# Windows
cd scripts\
check-environment.bat
```

The script confirms dbt is on PATH and reports the Fusion (2.0.x) version. To verify the Snowflake
connection, use `dbt debug`.

---

## Troubleshooting

**Connection issues**: Run `dbt debug` and check:

- Environment variables set (`DBT_ENV_SECRET_SNOWFLAKE_PAT`)
- `~/.dbt/profiles.yml` exists and is configured correctly
- Snowflake connectivity: `snow sql -q "SELECT CURRENT_USER()"`

**Package issues**: `rm -rf dbt_packages/ && dbt deps --upgrade`

**`dbt` not found after install**: open a new terminal so the updated PATH takes effect, or ensure
`$HOME/.local/bin` (macOS/Linux) / `%USERPROFILE%\.local\bin` (Windows) is on PATH.

**Python compatibility**: Not applicable — Fusion is a standalone binary and does not require
Python.

**Official Docs**:
[Network Issues](https://docs.snowflake.com/en/user-guide/troubleshooting-network)

---

## Project Initialization

```bash
# Non-interactive (recommended for AI agents)
dbt init my_project_name --skip-profile-setup

# Configure ~/.dbt/profiles.yml separately (see Snowflake Configuration above)
# Configure your project with dbt_project.yml (see below)
```

**Project structure**: models/, tests/, macros/, seeds/, snapshots/

---

## dbt_project.yml Configuration

Configure your project in `dbt_project.yml`. Common patterns include:

- **Basic project setup** (name, version, profile connection)
- **Project paths** (models, tests, macros, seeds, snapshots)
- **Global hooks** (on-run-start, on-run-end)
- **Global variables** for project-wide settings
- **Model configurations** with materialization defaults
- **Medallion architecture pattern** (bronze/silver/gold layers)
- **Snapshot configurations** for SCD Type 2
- **Test configurations** with failure storage

**To configure**:

1. Set `name` to match your project name
2. Set `profile` to match your profiles.yml profile name
3. Choose your architecture pattern (basic or medallion)
4. Customize materializations and schemas
5. Run `dbt debug` to verify configuration

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

- **Separate dev/prod configs** - Use `{{ env_var('SCHEMA_NAME', 'DEFAULT_NAME') }}` to allow
  overriding of schema names
- **Version control** - Do not commit `profiles.yml` or `.env` files (they contain credentials)

---

## Upgrade dbt Version

```bash
# Update the Fusion engine in place
dbt system update
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
