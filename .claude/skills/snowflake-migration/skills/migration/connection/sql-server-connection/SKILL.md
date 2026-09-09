---
name: sql-server-connection
description: Connect to a source SQL Server database for migration to Snowflake using scai CLI. Triggers: sql server, sqlserver, source connection, source database, connect to sql server, add sql server connection.
license: Proprietary. See License-Skills for complete terms
---

# SQL Server Connection Skill

## On Entry

Tell the user:
> **Setting up SQL Server connection** — I'll configure and test a connection to your source SQL Server database. I'll need some connection details from you shortly.

## Prerequisites

- Network access to the SQL Server instance
- SQL Server credentials (username/password for Standard auth, or domain credentials for Windows auth)
- The `scai` CLI installed and available

## Required Connection Details

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-s, --source-connection` | Yes | Friendly name for this connection |
| `--auth` | Yes | Authentication method: `standard` or `windows` |
| `--server-url` | Yes | SQL Server hostname or IP |
| `--database` | Yes | Database name to connect to |
| `--user` | For standard auth | SQL Server username |
| `--password` | For standard auth | SQL Server password (prompted securely) |
| `--port` | No | Port number (default: 1433) |
| `--trust-server-certificate` | No | Trust server certificate |
| `--encrypt` | No | Encrypt connection |

## Workflow

### Step 1: Ask How to Provide Credentials

Ask the user:

> "I need the following to connect to SQL Server:
> - **Server URL** (hostname or IP)
> - **Database name**
> - **Username** and **Password** (for standard auth)
>
> How would you like to provide these?"

Options:
1. **1Password** - Credentials stored in 1Password vault
2. **Enter manually** - Provide values interactively

### Step 2: Route Based on Answer

| User says | Action |
|-----------|--------|
| "1Password" | Follow `../1PASSWORD.md` |
| "Enter manually" | Proceed to Step 3 (manual entry) |
| Other credential manager | Check if `../references/<NAME>.md` exists; if not, ask user to explain their setup |

### Step 3: Add the Connection (Manual Entry)

**Interactive mode (recommended):**
```bash
scai connection add-sql-server
```

**Inline mode:**
```bash
scai connection add-sql-server \
  -s <SOURCE_CONNECTION_NAME> \
  --auth standard \
  --server-url <SERVER_URL> \
  --port 1433 \
  --database <DATABASE> \
  --user <USERNAME>
```
Password will be prompted securely.

### Step 4: Save and Test Source Connection

Call the `configure` tool with `source_connection` set to `<SOURCE_CONNECTION_NAME>`. The MCP server runs `scai connection test` internally and only persists the connection if the test passes.

- **On success:** the response includes `connection_test: ok`.
- **On failure:** the tool returns an error containing the scai message. Surface it to the user, help them fix the issue, then re-run `configure(source_connection=<SOURCE_CONNECTION_NAME>)`. See `./references/REFERENCE.md` for troubleshooting.

## CHECKPOINT

Confirm with user:
- [ ] `configure` returned `connection_test: ok`
- [ ] Connection appears in `scai connection list -l sqlserver --json`
- [ ] Source connection saved to session config

## On Completion

After the CHECKPOINT passes, tell the user:
> **Connection configured** — Successfully connected to SQL Server using connection `<connection_name>`.

Then return to the calling skill.

## Security Rules

- **NEVER** log or display passwords in plain text
- **NEVER** include passwords in command-line arguments that might be logged
- Use interactive mode or credential managers to avoid password exposure

## Quick Reference

| Action | Command |
|--------|---------|
| Add connection (interactive) | `scai connection add-sql-server` |
| Add connection (inline) | `scai connection add-sql-server -s NAME --auth standard --server-url HOST --database DB --user USER` |
| Test connection | `configure(source_connection=NAME)` (runs the test internally) |
| Set default | `scai connection set-default -l sqlserver -s NAME` |
