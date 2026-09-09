---
name: teradata-connection
description: Connect to a source Teradata database for full migration to Snowflake using scai CLI (code, scai test, cloud table data migration/validation). Requires a user-provided Teradata driver (NuGet package). Triggers: teradata, source connection, source database, connect to teradata, add teradata connection.
---

# Teradata Connection Skill

## On Entry

Tell the user:
> **Setting up Teradata connection** — I'll configure and test a connection to your source Teradata database. This requires a driver download on first use.

## Prerequisites

- Network access to the Teradata database instance
- Teradata credentials (username/password) — standard or LDAP-backed
- The `scai` CLI installed and available
- The Teradata .NET driver NuGet package (`Teradata.Client.Provider.nupkg`) — see Step 1

## Required Connection Details

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-s, --source-connection` | Yes | Friendly name for this connection |
| `--auth` | Yes | Authentication method (`standard` or `ldap`) |
| `--host` | Yes | Teradata hostname or IP |
| `--database` | Yes | Teradata database name |
| `--port` | No | Port number (default: 1025) |
| `--user` | Yes | Teradata username |
| `--password` | Yes | Teradata password (prompted securely) |
| `--connection-timeout` | No | Connection timeout in seconds (default: 30) |

## Workflow

### Step 1: Provision the Teradata Driver

The required driver is the `Teradata.Client.Provider` NuGet package. Resolve it by following the canonical bootstrap flow:

> **Driver bootstrap:** see [`../references/driver-bootstrap.md`](../references/driver-bootstrap.md) with parameters
> `<dialect>=teradata`, `<package>=Teradata.Client.Provider`, `<driver_file>=Teradata.Client.Provider.nupkg`,
> `<cache_dir>=~/.snowflake/scai/drivers/teradata/`,
> `<nuget_url>=https://www.nuget.org/api/v2/package/Teradata.Client.Provider`.

That doc walks through cache check → ask-on-miss → user-provided path or download → first SCAI invocation with `--driver-path` if needed. Follow it silently — don't narrate "the bootstrap flow" or step labels to the user.

**Naming guard:** the driver is a `.NET` NuGet package, **not** a JDBC driver. Refer to it only as "the Teradata driver" or "the Teradata NuGet package" when talking to the user.

For this skill specifically, the first SCAI invocation called out by the bootstrap is the `configure` tool call in **Step 4 below** — pass `driver_path=<PATH>` there if the driver wasn't already cached. The MCP server invokes `scai connection test --driver-path <PATH>` internally, which seeds the driver cache.

### Step 2: Ask How to Provide Credentials

Ask the user:

> "I need the following to connect to Teradata:
> - **Host** (hostname or IP)
> - **Database** name
> - **Username** and **Password**
> - **Authentication method** — `standard` (username/password) or `ldap` (LDAP-backed credentials)
>
> How would you like to provide these?"

Options:
1. **Enter manually** - Provide values interactively

### Step 3: Add the Connection (Manual Entry)

**Interactive mode (recommended):**
```bash
scai connection add-teradata
```

**Inline mode (standard auth):**
```bash
scai connection add-teradata \
  -s <CONNECTION_NAME> \
  --auth standard \
  --host <HOST> \
  --database <DATABASE> \
  --port 1025 \
  --user <USERNAME>
```

**Inline mode (LDAP auth):**
```bash
scai connection add-teradata \
  -s <CONNECTION_NAME> \
  --auth ldap \
  --host <HOST> \
  --database <DATABASE> \
  --user <USERNAME>
```

Password will be prompted securely.

### Step 4: Save and Test Source Connection

This is the "first SCAI invocation" called out as 1e in the bootstrap reference. Use the path resolved in Step 1.

Call the `configure` tool with `source_connection` set to `<CONNECTION_NAME>`. The MCP server runs `scai connection test` internally and only persists the connection if the test passes.

- **First use (driver not yet cached):** also pass `driver_path=<PATH_TO_NUPKG>`. The first call copies the driver into `~/.snowflake/scai/drivers/teradata/`, so every subsequent `configure` call (in this project or any other) can omit `driver_path`.

  ```
  configure(source_connection=<CONNECTION_NAME>, driver_path=<PATH_TO_NUPKG>)
  ```

- **Driver already cached:** omit `driver_path`.

  ```
  configure(source_connection=<CONNECTION_NAME>)
  ```

- **On success:** the response includes `connection_test: ok`.
- **On failure:** the tool returns an error containing the scai message. Surface it to the user, help them fix the issue, then re-run `configure(...)`. See `./references/REFERENCE.md` for detailed troubleshooting.

**Common errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Socket closed` | Invalid host or port | Verify host and port (default 1025) |
| `Logon failed` | Wrong credentials | Check username and password |
| `Database does not exist` | Invalid database name | Verify the database name |
| `Connection timed out` | Network/firewall issue | Check VPN, firewall rules, security groups |
| `Driver not found` | Missing or invalid `driver_path` | Re-download the NuGet package and verify the file path |
| `LDAP authentication failed` | Invalid LDAP credentials | Verify LDAP username and password with your admin |

## CHECKPOINT

Confirm with user:
- [ ] Teradata driver resolved via one of:
  - [ ] Already cached in `~/.snowflake/scai/drivers/teradata/` (Step 1a)
  - [ ] User-provided local path supplied via `driver_path` (Step 1c)
  - [ ] Downloaded by the agent and supplied via `driver_path` (Step 1d)
- [ ] `configure` returned `connection_test: ok`
- [ ] Connection appears in `scai connection list -l teradata --json`
- [ ] Source connection saved to session config

## Supported Operations

Teradata is a **full-migration** source (`project_type: full_migration`). After connection setup:

- **Code pipeline:** `scai code extract`, `scai code convert`, `scai code deploy`
- **2-sided testing:** `scai test capture`, `scai test validate` (baseline capture and Snowflake result comparison)
- **Cloud table data:** `scai data migrate` and cloud data validation via the Data Exchange Worker

For cloud data paths, align worker TOML `[connections.source.teradata].database` with workflow YAML `source.databaseName` (the `--database` value from this connection). LDAP connections map to worker TOML `authentication = "LDAP"`. See [`./references/REFERENCE.md`](./references/REFERENCE.md) for worker setup and troubleshooting.

> **Legacy projects:** If an older project has `project_type: code_conversion_only` in `project.yml`, the CLI honors that setting and routes through the code-conversion-only flow. New Teradata projects default to `full_migration`.

## On Completion

After the CHECKPOINT passes, tell the user:
> **Connection configured** — Successfully connected to Teradata using connection `<connection_name>`.

Then return to the calling skill.

## Security Rules

- **NEVER** log or display passwords in plain text
- **NEVER** include passwords in command-line arguments that might be logged
- Use interactive mode to avoid password exposure

## Quick Reference

| Action | Command |
|--------|---------|
| Check driver cache | List `.nupkg`/`.dll` files in `~/.snowflake/scai/drivers/teradata/` (POSIX) or `%USERPROFILE%\.snowflake\scai\drivers\teradata\` (Windows) |
| Use existing local driver | `scai project defaults set -s <CONNECTION_NAME> --driver-path <PATH_TO_NUPKG>` |
| Download driver (macOS/Linux) | `curl -L -o Teradata.Client.Provider.nupkg https://www.nuget.org/api/v2/package/Teradata.Client.Provider` |
| Download driver (Windows PowerShell) | `curl.exe -L -o Teradata.Client.Provider.nupkg https://www.nuget.org/api/v2/package/Teradata.Client.Provider` |
| Add connection (interactive) | `scai connection add-teradata` |
| Add connection (standard) | `scai connection add-teradata -s NAME --auth standard --host HOST --database DB --user USER` |
| Add connection (LDAP) | `scai connection add-teradata -s NAME --auth ldap --host HOST --database DB --user USER` |
| Test connection (first time) | `configure(source_connection=NAME, driver_path=<PATH_TO_NUPKG>)` |
| Test connection (driver cached) | `configure(source_connection=NAME)` |
| List connections | `scai connection list -l teradata --json` |
| Set default | `scai connection set-default -l teradata -s NAME` |
| Extract code | `scai code extract -s NAME --json` |
