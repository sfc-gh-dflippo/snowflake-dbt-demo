---
name: db2-connection
description: Connect to a source IBM DB2 (LUW) database for migration to Snowflake using scai CLI. Triggers: db2, ibm db2, source connection, source database, connect to db2, add db2 connection.
license: Proprietary. See License-Skills for complete terms
---

# DB2 Connection Skill

## On Entry

Tell the user:
> **Setting up DB2 connection** — I'll configure and test a connection to your source IBM DB2 (LUW) database. I'll need a few connection details.

## Prerequisites

- Network access to the DB2 host (self-hosted LUW or cloud-hosted)
- DB2 username and password with read access to the system catalog (`SYSCAT`)
- The `scai` CLI installed and available

## Required Connection Details

### Standard Auth (only auth method supported in MVP)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-s, --source-connection` | Yes | Friendly name for this source connection |
| `--auth` | Yes | `standard` |
| `--host` | Yes | DB2 host |
| `--port` | No | TCP port (default: `50000`) |
| `--database` | Yes | Database name |
| `--user` | Yes | DB2 username |
| `--password` | Yes | DB2 password |
| `--connection-timeout` | No | Connection timeout in seconds |

> DB2 is read through the `ibm_db` DB-API driver, which stages Parquet — there is no ODBC install required on the worker host.

## Workflow

### Step 1: Ask How to Provide Credentials

Ask the user:
> "I need the following to connect to DB2:
> - **Host**
> - **Port** (default `50000`)
> - **Database name**
> - **Username** and **password**
>
> How would you like to provide these?"

Options:
1. **1Password** — Credentials stored in 1Password vault
2. **Enter manually** — Provide values directly

### Step 2: Route Based on Answer

| User says | Action |
|-----------|--------|
| "1Password" | Follow `../1PASSWORD.md` (DB2 section) |
| "Enter manually" | Proceed to Step 3 |
| Other credential manager | Check if `../references/<NAME>.md` exists; if not, ask user to explain their setup |

### Step 3: Add the Connection

```bash
scai connection add-db2 \
  -s <CONNECTION_NAME> \
  --auth standard \
  --host <HOST> \
  --port <PORT> \
  --database <DATABASE> \
  --user <USERNAME> \
  --password <PASSWORD>
```

- Omit `--port` if the server uses the default (`50000`).

### Step 4: Save and Test Source Connection

Call the `configure` tool with `source_connection` set to `<CONNECTION_NAME>`. The MCP server runs `scai connection test` internally and only persists the connection if the test passes.

- **On success:** the response includes `connection_test: ok`.
- **On failure:** the tool returns an error containing the scai message. Surface it to the user, help them fix the issue, then re-run `configure(source_connection=<CONNECTION_NAME>)`.

**Common errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Operation timed out` | Network / firewall | Check VPN, security groups, firewall rules |
| `SQL30081N` (communication error) | Wrong host/port or server down | Verify host, port (default `50000`), and that DB2 is listening |
| `SQL1013N` (database not found) | Wrong database name | Verify the database alias / name on the server |
| `SQL30082N` (auth failed) | Bad credentials | Re-check username and password |

## CHECKPOINT

Confirm with user:
- [ ] `configure` returned `connection_test: ok`
- [ ] Connection appears in `scai connection list -l db2 --json`
- [ ] Source connection saved to session config

## On Completion

After the CHECKPOINT passes, tell the user:
> **Connection configured** — Successfully connected to DB2 using connection `<connection_name>`.

Then return to the calling skill.

## Security Rules

- **NEVER** log or display secrets (passwords) in plain text.
- **NEVER** include secrets in command-line arguments that might be logged. Prefer a credential manager (e.g. 1Password `op run`, or use /secrets capability from Cortex Code to store them).

## Quick Reference

| Action | Command |
|--------|---------|
| Add connection | `scai connection add-db2 -s NAME --auth standard --host HOST --port 50000 --database DB --user USER --password PASS` |
| Test connection | `configure(source_connection=NAME)` (runs the test internally) |
| List connections | `scai connection list -l db2 --json` |
| Set default | `scai connection set-default -l db2 -c NAME` |
| Extract code | `scai code extract -s NAME --json` |
