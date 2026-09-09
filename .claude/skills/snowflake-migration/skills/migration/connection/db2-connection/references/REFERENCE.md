# DB2 Connection Reference

Detailed reference for IBM DB2 (LUW) connection options, authentication, extraction, and troubleshooting.

## Connection Options

### Required Parameters

| Parameter | Flag | Description |
|-----------|------|-------------|
| Connection name | `-s, --source-connection` | Unique identifier for this connection |
| Authentication | `--auth` | Authentication method: `standard` |
| Host | `--host` | DB2 hostname or IP address |
| Database | `--database` | Database name (bound at connection time) |
| Username | `--user` | DB2 username |
| Password | `--password` | DB2 password |

### Optional Parameters

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Port | `--port` | 50000 | TCP port number |
| Connection timeout | `--connection-timeout` | 30 | Timeout in seconds |

## Authentication Methods

### Standard Authentication (Username/Password)

The only supported authentication method for DB2.

```bash
scai connection add-db2 \
  -s my-db2 \
  --auth standard \
  --host db2-server.example.com \
  --port 50000 \
  --database SAMPLE \
  --user myuser \
  --password mypassword
```

**When to use:**
- All DB2 connections (only method available in MVP)

## Data Exchange Worker (cloud migration / validation)

The worker connects via the `ibm_db` DB-API driver using the same credentials as
`scai connection add-db2`. DB2 is read off a DB-API cursor and staged as **Parquet**
(not CSV) — Parquet preserves NULL-vs-empty-string and multi-byte data that a CSV
extract would corrupt. The generated worker TOML:

```toml
[connections.source.db2]
user = "<username>"
password = "<password>"
database = "<database_name>"
host = "<host>"
port = 50000
```

Ensure the DB2 user has:

- `SELECT` on all tables being migrated or validated
- Read access to `SYSCAT.COLUMNS` / `SYSCAT.TABLES` for schema discovery

Network: the worker host must reach the DB2 server on the configured port. For SPCS
workers, ensure `EXTERNAL_ACCESS_INTEGRATIONS` covers the database host. DB2 requires
the `ibm_db` driver, which is bundled with the worker — no separate ODBC install.

Worker TOML `[connections.source.db2].database` must match `source.databaseName` in the
migration/validation workflow YAML.

## scai TOML Fields (`~/.snowflake/snowct/db2.toml`)

Populated by `scai connection add-db2`. The MCP server reads this file when generating
the DEW worker config.

| Field | Required | Description |
|---|---|---|
| `auth_method` | Yes | Always `standard` |
| `user` | Yes | DB2 username |
| `password` | Yes | DB2 password |
| `host` | Yes | DB2 host |
| `port` | No | TCP port (default: `50000`) |
| `database` | Yes | Database name (bound at connection time) |
| `connection_timeout` | No | Timeout in seconds (if set) |

## Workflow YAML

`sourcePlatform` for DB2 validation workflows:

```yaml
sourcePlatform: db2
```

## `whereClauseCriteria`

DB2 folds unquoted identifiers to uppercase and uses double quotes for case-sensitive names:

```yaml
tables:
  - source:
      schemaName: MYSCHEMA
      name: MYTABLE
    whereClauseCriteria: '"ID" > 1000'
```

## Partition Column Guidance

DB2 has no portable system row identifier suitable for partitioning. Use:

- A monotonic integer primary key (e.g. `ID BIGINT`) — most common and reliable
- A timestamp column with a narrow range — for time-partitioned loads
- No partition column — omit `columnNamesToPartitionBy` for a single-partition full extract

## Troubleshooting

### Communication Error (SQL30081N)

**Symptoms:**
- `SQL30081N ... communication error`
- Connection hangs then times out

**Solutions:**
1. Verify host and port (default `50000`)
2. Check VPN / firewall / security-group rules allow the port
3. Confirm the DB2 instance is listening: `db2 get dbm cfg | grep SVCENAME`
4. Test network path: `nc -zv <host> 50000`

### Authentication Failed (SQL30082N)

**Solutions:**
1. Verify username and password are correct
2. DB2 usernames map to OS/LDAP accounts — verify the account is valid on the server

### Database Not Found (SQL1013N)

**Solutions:**
1. Verify the database name / alias (`db2 list database directory`)
2. Confirm the database is cataloged on the target instance

### Insufficient Privileges

**Solutions:**
1. Grant read access: `GRANT SELECT ON <schema>.<table> TO <user>;`
2. Ensure the user can read `SYSCAT` catalog views (granted to `PUBLIC` by default)

## Verifying Connectivity

```bash
scai connection test -l db2 -c <CONNECTION_NAME> --json
```

Manual network test:

```bash
nc -zv <host> 50000
```

## Stored Connection Format

SCAI stores DB2 connections in TOML format with these fields:

| TOML key | Description |
|----------|-------------|
| `auth_method` | Always `standard` |
| `user` | DB2 username |
| `host` | DB2 hostname or IP |
| `database` | Database name |
| `port` | Port number (default `50000`) |
| `password` | Encrypted password |
| `connection_timeout` | Timeout in seconds (if set) |
