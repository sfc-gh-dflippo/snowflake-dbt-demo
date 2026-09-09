---
name: bigquery-connection
description: Connect to a source Google BigQuery project for migration to Snowflake using scai CLI. Triggers: bigquery, google bigquery, gbq, source connection, source database, connect to bigquery, add bigquery connection.
license: Proprietary. See License-Skills for complete terms
---

# BigQuery Connection Skill

## On Entry

Tell the user:
> **Setting up BigQuery connection** — I'll configure and test a connection to your source Google BigQuery project. I'll need a few connection details.

## Prerequisites

- A Google Cloud project with BigQuery enabled and the datasets you want to migrate
- A service account JSON key with read access to the source data and catalog (`INFORMATION_SCHEMA`)
- The service account granted `roles/bigquery.dataViewer`, `roles/bigquery.jobUser`, and `roles/bigquery.readSessionUser` on the project
- The `scai` CLI installed and available

## Required Connection Details

### Service Account Auth (only auth method supported in MVP)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-s, --source-connection` | Yes | Friendly name for this source connection |
| `--auth` | Yes | `service-account` |
| `--project-id` | Yes | GCP project ID that owns the datasets and runs the queries |
| `--dataset` | No | Default dataset to scope discovery to (all datasets in the project if omitted) |
| `--credentials-file` | Yes | Path to the service account JSON key file |
| `--location` | No | Dataset location / region (e.g. `US`, `EU`, `us-central1`) |
| `--connection-timeout` | No | Connection timeout in seconds |

> BigQuery has no host or port to configure — the worker reaches the BigQuery API over HTTPS on port `443`, and TLS is always enforced by the endpoint. BigQuery is read through the `google-cloud-bigquery` client (BigQuery Storage Read API), which stages Parquet — there is no ODBC install required on the worker host.

## Workflow

### Step 1: Ask How to Provide Credentials

Ask the user:
> "I need the following to connect to BigQuery:
> - **GCP project ID**
> - **Service account JSON key file** (path)
> - **Default dataset** (optional)
> - **Location** (optional, e.g. `US`)
>
> How would you like to provide these?"

Options:
1. **1Password** — Credentials stored in 1Password vault
2. **Enter manually** — Provide values directly

### Step 2: Route Based on Answer

| User says | Action |
|-----------|--------|
| "1Password" | Follow `../1PASSWORD.md` (BigQuery section) |
| "Enter manually" | Proceed to Step 3 |
| Other credential manager | Check if `../references/<NAME>.md` exists; if not, ask user to explain their setup |

### Step 3: Add the Connection

```bash
scai connection add-bigquery \
  -s <CONNECTION_NAME> \
  --auth service-account \
  --project-id <GCP_PROJECT_ID> \
  --dataset <DATASET> \
  --credentials-file <PATH_TO_SERVICE_ACCOUNT_JSON> \
  --location <LOCATION>
```

- Omit `--dataset` to scope discovery to the whole project.
- Omit `--location` unless your datasets live in a specific region and auto-detection fails.

### Step 4: Save and Test Source Connection

Call the `configure` tool with `source_connection` set to `<CONNECTION_NAME>`. The MCP server runs `scai connection test` internally and only persists the connection if the test passes.

- **On success:** the response includes `connection_test: ok`.
- **On failure:** the tool returns an error containing the scai message. Surface it to the user, help them fix the issue, then re-run `configure(source_connection=<CONNECTION_NAME>)`.

**Common errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Could not automatically determine credentials` | Missing / wrong key file | Verify the `--credentials-file` path points to a valid service account JSON key |
| `403 Access Denied` / `does not have permission` | Missing IAM role | Grant `roles/bigquery.dataViewer` + `roles/bigquery.jobUser` (+ `readSessionUser`) on the project |
| `404 Not found: Dataset ...` | Wrong project or dataset | Verify the project ID and dataset name (and location) |
| `invalid_grant` / `Reauthentication is needed` | Expired / revoked key | Re-issue the service account key and re-add the connection |

## CHECKPOINT

Confirm with user:
- [ ] `configure` returned `connection_test: ok`
- [ ] Connection appears in `scai connection list -l bigquery --json`
- [ ] Source connection saved to session config

## On Completion

After the CHECKPOINT passes, tell the user:
> **Connection configured** — Successfully connected to BigQuery using connection `<connection_name>`.

Then return to the calling skill.

## Security Rules

- **NEVER** log or display secrets (service account keys) in plain text.
- **NEVER** include secrets in command-line arguments that might be logged. Prefer a credential manager (e.g. 1Password `op run`, or use /secrets capability from Cortex Code to store them). Pass the key as a file path, not inline JSON.

## Quick Reference

| Action | Command |
|--------|---------|
| Add connection | `scai connection add-bigquery -s NAME --auth service-account --project-id PROJECT --credentials-file KEY.json` |
| Test connection | `configure(source_connection=NAME)` (runs the test internally) |
| List connections | `scai connection list -l bigquery --json` |
| Set default | `scai connection set-default -l bigquery -c NAME` |
| Extract code | `scai code extract -s NAME --json` |
