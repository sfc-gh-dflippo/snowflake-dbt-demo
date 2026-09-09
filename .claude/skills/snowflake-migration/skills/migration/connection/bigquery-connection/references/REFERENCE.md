# BigQuery Connection Reference

Detailed reference for Google BigQuery connection options, authentication, extraction, and troubleshooting.

## Connection Options

### Required Parameters

| Parameter | Flag | Description |
|-----------|------|-------------|
| Connection name | `-s, --source-connection` | Unique identifier for this connection |
| Authentication | `--auth` | Authentication method: `service-account` |
| Project ID | `--project-id` | GCP project ID that owns the datasets and runs the queries |
| Credentials file | `--credentials-file` | Path to the service account JSON key file |

### Optional Parameters

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Default dataset | `--dataset` | (none) | Dataset to scope discovery to; whole project if omitted |
| Location | `--location` | auto | Dataset location / region (e.g. `US`, `EU`, `us-central1`) |
| Connection timeout | `--connection-timeout` | 30 | Timeout in seconds |

> BigQuery is serverless — there is no host or port to configure. The worker reaches
> the BigQuery API over HTTPS on port `443` and TLS is always enforced by the endpoint.

## Authentication Methods

### Service Account (JSON key)

The only supported authentication method for BigQuery in MVP.

```bash
scai connection add-bigquery \
  -s my-bigquery \
  --auth service-account \
  --project-id my-gcp-project \
  --dataset analytics \
  --credentials-file /secure/path/sa-key.json \
  --location US
```

**When to use:**
- All BigQuery connections (only method available in MVP)

> Application Default Credentials (ADC) via `GOOGLE_APPLICATION_CREDENTIALS` or the GCE
> metadata server are a possible future option, but MVP requires an explicit service
> account key file so the worker config is self-contained.

## Data Exchange Worker (cloud migration / validation)

The worker connects via the `google-cloud-bigquery` client using the same service
account as `scai connection add-bigquery`. BigQuery is read off the BigQuery Storage
Read API and staged as **Parquet** (not CSV) — Parquet preserves NULL-vs-empty-string
and nested/repeated data that a CSV extract would corrupt. The generated worker TOML:

```toml
[connections.source.bigquery]
project_id = "<gcp_project_id>"
dataset = "<default_dataset>"
credentials_file = "<path_to_service_account_json>"
location = "<location>"
```

Ensure the service account has:

- `roles/bigquery.dataViewer` — read table data
- `roles/bigquery.jobUser` — run query / extract jobs
- `roles/bigquery.readSessionUser` — open Storage Read API sessions
- Read access to `INFORMATION_SCHEMA` for schema discovery (implied by dataViewer)

Network: the worker host must reach `bigquery.googleapis.com` and
`bigquerystorage.googleapis.com` over HTTPS (443). For SPCS workers, ensure
`EXTERNAL_ACCESS_INTEGRATIONS` covers those hosts. No separate ODBC install is required.

Worker TOML `[connections.source.bigquery].project_id` (and `dataset`, when set) must
match `source.databaseName` / dataset scoping in the migration/validation workflow YAML.

## scai TOML Fields (`~/.snowflake/snowct/bigquery.toml`)

Populated by `scai connection add-bigquery`. The MCP server reads this file when
generating the DEW worker config.

| Field | Required | Description |
|---|---|---|
| `auth_method` | Yes | Always `service-account` |
| `project_id` | Yes | GCP project ID |
| `credentials_file` | Yes | Path to the service account JSON key file |
| `dataset` | No | Default dataset scope |
| `location` | No | Dataset location / region |
| `connection_timeout` | No | Timeout in seconds (if set) |

## Workflow YAML

`sourcePlatform` for BigQuery validation workflows:

```yaml
sourcePlatform: bigquery
```

## `whereClauseCriteria`

BigQuery uses standard SQL and backticks for identifiers; column names are
case-insensitive on resolution but preserved:

```yaml
tables:
  - source:
      schemaName: analytics
      name: events
    whereClauseCriteria: '`id` > 1000'
```

## Partition Column Guidance

BigQuery has no portable system row identifier suitable for partitioning. Use:

- The table's DATE/TIMESTAMP partitioning column — most reliable for partitioned tables
- A monotonic integer key (e.g. `id INT64`) — for unpartitioned tables
- No partition column — omit `columnNamesToPartitionBy` for a single-partition full extract

## Troubleshooting

### Credentials Not Found

**Symptoms:**
- `Could not automatically determine credentials`
- `File ... was not found`

**Solutions:**
1. Verify `--credentials-file` points to a readable service account JSON key
2. Confirm the key belongs to the same project as `--project-id`

### Access Denied (403)

**Symptoms:**
- `403 Access Denied`
- `User does not have permission to query / read`

**Solutions:**
1. Grant `roles/bigquery.dataViewer` and `roles/bigquery.jobUser` on the project
2. Grant `roles/bigquery.readSessionUser` for Storage Read API extraction
3. Confirm the service account is bound at the project (not only dataset) level

### Dataset / Table Not Found (404)

**Solutions:**
1. Verify the project ID, dataset name, and `--location`
2. Confirm the dataset exists and the location matches (`US` vs `EU` mismatches read as 404)

### Expired or Revoked Key (invalid_grant)

**Solutions:**
1. Re-issue the service account key in the GCP console
2. Re-run `scai connection add-bigquery` with the new key file

## Verifying Connectivity

```bash
scai connection test -l bigquery -c <CONNECTION_NAME> --json
```

Manual network test:

```bash
nc -zv bigquery.googleapis.com 443
```

## Stored Connection Format

SCAI stores BigQuery connections in TOML format with these fields:

| TOML key | Description |
|----------|-------------|
| `auth_method` | Always `service-account` |
| `project_id` | GCP project ID |
| `credentials_file` | Path to the service account JSON key file |
| `dataset` | Default dataset scope (if set) |
| `location` | Dataset location / region (if set) |
| `connection_timeout` | Timeout in seconds (if set) |
