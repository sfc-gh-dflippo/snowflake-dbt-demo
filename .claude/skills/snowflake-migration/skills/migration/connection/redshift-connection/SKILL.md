---
name: redshift-connection
description: Connect to a source Redshift database for migration to Snowflake using scai CLI. Triggers: redshift, source connection, source database, connect to redshift, add redshift connection.
license: Proprietary. See License-Skills for complete terms
---

# Redshift Connection Skill

## On Entry

Tell the user:
> **Setting up Redshift connection** — I'll configure and test a connection to your source Redshift cluster. I'll need some connection details from you shortly.

## Prerequisites

- Network access to the Redshift cluster or serverless endpoint
- For IAM auth: AWS credentials (access key ID + secret access key)
- For standard auth: Redshift username and password
- The `scai` CLI installed and available

## Required Connection Details

### IAM Provisioned Cluster (Recommended)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c, --connection` | Yes | Friendly name for this connection |
| `--auth` | Yes | `iam-provisioned-cluster` |
| `--cluster-id` | Yes | Redshift cluster identifier |
| `--database` | Yes | Database name to connect to |
| `--region` | Yes | AWS region (e.g., `us-west-2`) |
| `--user` | Yes | Redshift database user |
| `--access-key-id` | Yes | AWS Access Key ID |
| `--secret-access-key` | Yes | AWS Secret Access Key |

### IAM Serverless

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c, --connection` | Yes | Friendly name for this connection |
| `--auth` | Yes | `iam-serverless` |
| `--workgroup` | Yes | Redshift Serverless workgroup name |
| `--database` | Yes | Database name to connect to |
| `--region` | Yes | AWS region (e.g., `us-west-2`) |
| `--access-key-id` | Yes | AWS Access Key ID |
| `--secret-access-key` | Yes | AWS Secret Access Key |

### Standard Auth

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c, --connection` | Yes | Friendly name for this connection |
| `--auth` | Yes | `standard` |
| `--host` | Yes | Redshift endpoint hostname |
| `--port` | No | Port number (default: 5439) |
| `--database` | Yes | Database name to connect to |
| `--user` | Yes | Redshift username |
| `--password` | Yes | Redshift password |

## Workflow

### Step 1: Ask How to Provide Credentials

Ask the user:

> "I need the following to connect to Redshift:
> - **Cluster ID** or **Workgroup** (depending on auth method)
> - **Database name**
> - **AWS credentials** (for IAM auth) or **username/password** (for standard auth)
>
> How would you like to provide these?"

Options:
1. **1Password** - Credentials stored in 1Password vault
2. **Enter manually** - Provide values interactively

### Step 2: Route Based on Answer

| User says | Action |
|-----------|--------|
| "1Password" | Follow `../1PASSWORD.md` (Redshift section) |
| "Enter manually" | Proceed to Step 3 (manual entry) |
| Other credential manager | Check if `../references/<NAME>.md` exists; if not, ask user to explain their setup |

### Step 3: Add the Connection (Manual Entry)

**Interactive mode (recommended):**
```bash
scai connection add-redshift
```

**IAM Provisioned Cluster (inline):**
```bash
scai connection add-redshift \
  -c <CONNECTION_NAME> \
  --auth iam-provisioned-cluster \
  --user <USER> \
  --cluster-id <CLUSTER_ID> \
  --database <DATABASE> \
  --region <REGION> \
  --access-key-id <ACCESS_KEY_ID> \
  --secret-access-key <SECRET_ACCESS_KEY>
```

**IAM Serverless (inline):**
```bash
scai connection add-redshift \
  -c <CONNECTION_NAME> \
  --auth iam-serverless \
  --workgroup <WORKGROUP> \
  --database <DATABASE> \
  --region <REGION> \
  --access-key-id <ACCESS_KEY_ID> \
  --secret-access-key <SECRET_ACCESS_KEY>
```

**Standard auth (inline):**
```bash
scai connection add-redshift \
  -c <CONNECTION_NAME> \
  --auth standard \
  --host <HOST> \
  --port 5439 \
  --database <DATABASE> \
  --user <USERNAME> \
  --password <PASSWORD>
```

### Step 4: Save and Test Source Connection

Call the `configure` tool with `source_connection` set to `<CONNECTION_NAME>`. The MCP server runs `scai connection test` internally and only persists the connection if the test passes.

- **On success:** the response includes `connection_test: ok`.
- **On failure:** the tool returns an error containing the scai message. Surface it to the user, help them fix the issue, then re-run `configure(source_connection=<CONNECTION_NAME>)`. See `./references/REFERENCE.md` for detailed troubleshooting.

**Common errors:**
| Error | Cause | Solution |
|-------|-------|----------|
| `Operation timed out` | Network/firewall issue | Check VPN, security groups, firewall rules |
| `database "X" does not exist` | Wrong database name | Verify database name on cluster |
| `IAM authentication failed` | Invalid AWS credentials | Check access key ID and secret |

## CHECKPOINT

Confirm with user:
- [ ] `configure` returned `connection_test: ok`
- [ ] Connection appears in `scai connection list -l redshift --json`
- [ ] Source connection saved to session config

## On Completion

After the CHECKPOINT passes, tell the user:
> **Connection configured** — Successfully connected to Redshift using connection `<connection_name>`.

Then return to the calling skill.

## Security Rules

- **NEVER** log or display secrets (passwords, secret access keys) in plain text
- **NEVER** include secrets in command-line arguments that might be logged
- Use interactive mode or credential managers (1Password) to avoid secret exposure

## Quick Reference

| Action | Command |
|--------|---------|
| Add connection (interactive) | `scai connection add-redshift` |
| Add IAM provisioned | `scai connection add-redshift -c NAME --auth iam-provisioned-cluster --cluster-id CLUSTER --database DB --region REGION --user USER --access-key-id KEY --secret-access-key SECRET` |
| Add IAM serverless | `scai connection add-redshift -c NAME --auth iam-serverless --workgroup WG --database DB --region REGION --access-key-id KEY --secret-access-key SECRET` |
| Add standard auth | `scai connection add-redshift -c NAME --auth standard --host HOST --database DB --user USER --password PASS` |
| Test connection | `configure(source_connection=NAME)` (runs the test internally) |
| List connections | `scai connection list -l redshift --json` |
| Set default | `scai connection set-default -l redshift -c NAME` |
| Extract code | `scai code extract -s NAME --json` |
