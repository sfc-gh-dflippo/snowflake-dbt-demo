# PostgreSQL Connection Reference

Detailed reference for PostgreSQL connection options, authentication methods, SSL configuration, and troubleshooting.

## Connection Options

### Required Parameters

| Parameter | Flag | Description |
|-----------|------|-------------|
| Connection name | `-c, --connection` | Unique identifier for this connection |
| Authentication | `--auth` | Authentication method: `standard` |
| Host | `--host` | PostgreSQL hostname or IP address |
| Database | `--database` | Database name (bound at connection time) |
| Username | `--user` | PostgreSQL username |
| Password | `--password` | PostgreSQL password |

### Optional Parameters

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Port | `--port` | 5432 | TCP port number |
| SSL mode | `--ssl-mode` | `Require` | One of `Disable`, `Allow`, `Prefer`, `Require`, `VerifyCA`, `VerifyFull` |
| Connection timeout | `--connection-timeout` | 30 | Timeout in seconds |

## Authentication Methods

### Standard Authentication (Username/Password)

The only supported authentication method for PostgreSQL.

```bash
scai connection add-postgresql \
  -c my-postgres \
  --auth standard \
  --host pg-server.example.com \
  --port 5432 \
  --database mydb \
  --user myuser \
  --password mypassword \
  --ssl-mode Require
```

**When to use:**
- All PostgreSQL connections (only method available in MVP)

**Full inline example with all options:**

```bash
scai connection add-postgresql \
  -c my-postgres \
  --auth standard \
  --host pg-server.example.com \
  --port 5432 \
  --database mydb \
  --user myuser \
  --password mypassword \
  --ssl-mode VerifyFull \
  --connection-timeout 60
```

## SSL/TLS Configuration

### Managed PostgreSQL (RDS, Cloud SQL, Azure, Supabase, Neon)

Managed services require encrypted connections. Use `Require` (default) or stricter:

```bash
scai connection add-postgresql \
  -c managed-pg \
  --auth standard \
  --host my-instance.us-east-1.rds.amazonaws.com \
  --database mydb \
  --user myuser \
  --password mypassword \
  --ssl-mode Require
```

### Strict Certificate Validation

For environments requiring full certificate chain verification:

```bash
scai connection add-postgresql \
  -c strict-pg \
  --auth standard \
  --host pg-server.example.com \
  --database mydb \
  --user myuser \
  --password mypassword \
  --ssl-mode VerifyFull
```

### Local / Docker Development

For local PostgreSQL instances without TLS configured:

```bash
scai connection add-postgresql \
  -c local-pg \
  --auth standard \
  --host localhost \
  --port 5432 \
  --database mydb \
  --user postgres \
  --password postgres \
  --ssl-mode Disable
```

**Warning:** Only use `--ssl-mode Disable` for trusted local development. Never use in production or with managed services.

### SSL Mode Reference

| Mode | Description | Use case |
|------|-------------|----------|
| `Disable` | No SSL | Local dev / Docker only |
| `Allow` | Try non-SSL first, fall back to SSL | Rare |
| `Prefer` | Try SSL first, fall back to non-SSL | Legacy servers |
| `Require` | Require SSL, skip CA verification | **Default — managed PG** |
| `VerifyCA` | Require SSL, verify CA certificate | Corporate environments |
| `VerifyFull` | Require SSL, verify CA + hostname | Highest security |

## Port Configuration

### Default Port (5432)

Most PostgreSQL instances use the default port:

```bash
scai connection add-postgresql \
  -c my-postgres \
  --auth standard \
  --host pg-server.example.com \
  --database mydb \
  --user myuser \
  --password mypassword
```

### Non-Default Port

For PostgreSQL instances on custom ports:

```bash
scai connection add-postgresql \
  -c my-postgres \
  --auth standard \
  --host pg-server.example.com \
  --port 5433 \
  --database mydb \
  --user myuser \
  --password mypassword
```

### Common Port Scenarios

| Scenario | Typical Port |
|----------|--------------|
| Standard PostgreSQL | 5432 |
| Second instance on same host | 5433 |
| Amazon RDS | 5432 |
| Google Cloud SQL | 5432 |
| Azure Database for PostgreSQL | 5432 |
| Supabase | 5432 (pooler: 6543) |
| Neon | 5432 |

## Data Exchange Worker (cloud migration / validation)

The worker connects via Npgsql using the same credentials as `scai connection add-postgresql`. The generated worker TOML uses the COPY protocol for all data extraction:

```toml
[connections.source.postgresql]
username = "<username>"
password = "<password>"
database = "<database_name>"
host = "<host>"
port = 5432
use_copy = true
```

`use_copy = true` is always enabled — the COPY protocol provides higher throughput than row-by-row reads.

Ensure the PostgreSQL user has:

- `SELECT` on all tables being migrated or validated
- `USAGE` on schemas containing those tables
- For `COPY` protocol: no additional grants beyond `SELECT` are required

Network: the worker host must reach the PostgreSQL server on the configured port. For SPCS workers, ensure `EXTERNAL_ACCESS_INTEGRATIONS` covers the database host. PostgreSQL does **not** require a separate driver download (unlike Oracle/Teradata) — Npgsql is bundled with the worker.

Worker TOML `[connections.source.postgresql].database` must match `source.databaseName` in migration/validation workflow YAML.

## scai TOML Fields (`~/.snowflake/snowct/postgresql.toml`)

Populated by `scai connection add-postgresql`. The MCP server reads this file when generating the DEW worker config.

| Field | Required | Description |
|---|---|---|
| `user` | Yes | PostgreSQL username |
| `password` | Yes | PostgreSQL password |
| `host` | Yes | PostgreSQL host |
| `port` | No | TCP port (default: `5432`) |
| `database` | Yes | Database name (bound at connection time) |
| `ssl_mode` | No | `Disable`, `Allow`, `Prefer`, `Require` (default), `VerifyCA`, `VerifyFull` |

## Workflow YAML

`sourcePlatform` for PostgreSQL validation workflows:

```yaml
sourcePlatform: postgresql
```

## `whereClauseCriteria`

PostgreSQL uses double-quoted identifiers for case-sensitive names:

```yaml
tables:
  - source:
      schemaName: public
      name: MyTable
    whereClauseCriteria: '"id" > 1000'
```

Unquoted identifiers are folded to lowercase by PostgreSQL. Quote identifiers that were created with mixed case.

## Partition Column Guidance

PostgreSQL has no system-managed row identifier equivalent to Oracle's `ROWID`. Use:

- A monotonic integer primary key (e.g. `id BIGINT`) — most common and reliable
- A timestamp column with a narrow range (e.g. `created_at`) — for time-partitioned loads
- No partition column — if the table has no suitable column, omit `columnNamesToPartitionBy` and the orchestrator performs a single-partition full extract

**Avoid `ctid`** — it is not stable across vacuum and may produce duplicates.

### Finding a Suitable Partition Column

```sql
-- List primary key columns for a table
SELECT a.attname
FROM pg_index i
JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
WHERE i.indrelid = '"public"."my_table"'::regclass
  AND i.indisprimary;

-- List integer/bigint columns (good partition candidates)
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'my_table'
  AND data_type IN ('integer', 'bigint', 'serial', 'bigserial');
```

## Troubleshooting

### Connection Timeout

**Symptoms:**
- Connection hangs then times out
- "Connection timeout expired"
- `Operation timed out`

**Solutions:**
1. **Check VPN** — PostgreSQL databases in private subnets require VPN access
2. Verify firewall rules allow the configured port (default 5432)
3. Increase timeout: `--connection-timeout 60`
4. Test network path: `nc -zv <host> 5432`
5. For RDS: check security group inbound rules

### Password Authentication Failed

**Symptoms:**
- `password authentication failed for user "<username>"`
- `FATAL: password authentication failed`

**Solutions:**
1. Verify username and password are correct
2. Check `pg_hba.conf` allows the connection method from your IP
3. PostgreSQL usernames are case-sensitive — verify exact case
4. Check if the user exists: `SELECT usename FROM pg_user;`
5. Verify the user has `LOGIN` privilege: `ALTER ROLE <user> LOGIN;`

### Database Does Not Exist

**Symptoms:**
- `FATAL: database "<name>" does not exist`
- `3D000: database "X" does not exist`

**Solutions:**
1. Verify the database name (case-sensitive if quoted at creation)
2. List databases: `SELECT datname FROM pg_database WHERE datistemplate = false;`
3. In `psql`: `\l` to list all databases
4. Common defaults: `postgres`, `defaultdb` (managed services)

### SSL Connection Required

**Symptoms:**
- `SSL connection is required. Specify SSL options and retry.`
- `FATAL: no pg_hba.conf entry for host ... SSL off`

**Solutions:**
1. Use `--ssl-mode Require` (the default) for managed PostgreSQL
2. Verify the server has SSL enabled in `postgresql.conf` (`ssl = on`)
3. For managed services (RDS, Cloud SQL, Azure), SSL is always required

### SSL Not Available on Server

**Symptoms:**
- `server does not support SSL, but SSL was required`
- `SSL error: SSL is not enabled on the server`

**Solutions:**
1. Use `--ssl-mode Disable` for local dev servers without TLS
2. If the server should have SSL, verify `ssl = on` in `postgresql.conf` and that certificate files exist
3. Restart PostgreSQL after enabling SSL

### Connection Refused

**Symptoms:**
- `Connection refused`
- `could not connect to server: Connection refused`

**Solutions:**
1. Verify PostgreSQL is running: `pg_isready -h <host> -p <port>`
2. Check `listen_addresses` in `postgresql.conf` (should be `'*'` or include your subnet)
3. Verify the port is correct
4. Check if `pg_hba.conf` allows connections from your IP/subnet
5. For Docker: ensure port is published (`-p 5432:5432`)

### VPN Connection Required

**Symptoms:**
- Timeout when host is correct
- Works from office but not remotely
- RDS/Cloud SQL endpoint unreachable

**Solutions:**

1. **Verify VPN is connected:**
   ```bash
   ifconfig | grep -E "utun|tun|ppp"
   traceroute <pg-host>
   ```

2. **If VPN is connected but still failing:**
   - Check if split tunneling excludes the database subnet
   - Ask IT/network team to verify VPN routes
   - For RDS: verify security group allows VPN subnet CIDR

### Insufficient Privileges

**Symptoms:**
- `permission denied for table <table>`
- `permission denied for schema <schema>`
- Extraction returns no objects

**Solutions:**
1. Grant schema access:
   ```sql
   GRANT USAGE ON SCHEMA <schema> TO <username>;
   ```
2. Grant table read access:
   ```sql
   GRANT SELECT ON ALL TABLES IN SCHEMA <schema> TO <username>;
   ```
3. For future tables:
   ```sql
   ALTER DEFAULT PRIVILEGES IN SCHEMA <schema>
     GRANT SELECT ON TABLES TO <username>;
   ```
4. Verify the user can see the schema:
   ```sql
   SELECT schema_name FROM information_schema.schemata;
   ```

### Too Many Connections

**Symptoms:**
- `FATAL: too many connections for role "<user>"`
- `FATAL: remaining connection slots are reserved for non-replication superuser connections`

**Solutions:**
1. Check current connection count: `SELECT count(*) FROM pg_stat_activity;`
2. Increase `max_connections` in `postgresql.conf` (requires restart)
3. For managed services: upgrade instance size or use connection pooling
4. Close idle connections from the worker before retrying

### Network / SPCS Notes

- The DEW worker must have outbound network access to the PostgreSQL host on the configured port.
- For managed PostgreSQL (Amazon RDS, Google Cloud SQL, Azure Database for PostgreSQL, Supabase, Neon):
  - Verify security group / firewall rules allow outbound from the worker host
  - Keep `ssl_mode = Require` or stricter (default)
- For local / Docker PostgreSQL during development:
  - `--ssl-mode Disable` may be required if the server has no TLS configured
- PostgreSQL does **not** require an external driver download — no `EXTERNAL_ACCESS_INTEGRATION` for a driver endpoint is needed (unlike Oracle/Teradata)

## Verifying Connectivity

### Test with scai

```bash
scai connection test -l postgresql -c <CONNECTION_NAME> --json
```

### Manual Network Test

```bash
# Test TCP connectivity to PostgreSQL
nc -zv <host> 5432

# Or with telnet
telnet <host> 5432

# Check if PostgreSQL is accepting connections
pg_isready -h <host> -p 5432
```

### Using psql (if installed)

```bash
psql -h <host> -p 5432 -d <database> -U <user>
```

### Check PostgreSQL Status (if you have access)

```sql
-- Verify connection
SELECT version();
SELECT current_database();
SELECT current_user;
SELECT inet_server_addr(), inet_server_port();
```

## Finding PostgreSQL Connection Details

### From Environment Variables

PostgreSQL clients commonly use standard environment variables:

```bash
echo $PGHOST $PGPORT $PGDATABASE $PGUSER
```

### From Connection Service File

If configured in `~/.pg_service.conf`:

```ini
[myservice]
host=pg-server.example.com
port=5432
dbname=mydb
user=myuser
```

### From Managed Service Console

**Amazon RDS:**
- Endpoint: RDS Console → Databases → select instance → Connectivity & security → Endpoint
- Port: usually 5432
- Database: Configuration → DB name

**Google Cloud SQL:**
- IP: Cloud SQL Console → select instance → Connect to this instance → Public/Private IP
- Port: 5432
- Database: Databases tab

**Azure Database for PostgreSQL:**
- Server name: Overview → Server name (ends in `.postgres.database.azure.com`)
- Port: 5432
- Database: Connect → select database

**Supabase:**
- Host: Project Settings → Database → Connection info → Host
- Port: 5432 (direct) or 6543 (connection pooler)
- Database: `postgres` (default)

## Stored Connection Format

SCAI stores PostgreSQL connections in TOML format with these fields:

| TOML key | Description |
|----------|-------------|
| `auth_method` | Always `standard` |
| `user` | PostgreSQL username |
| `host` | PostgreSQL hostname or IP |
| `database` | Database name |
| `port` | Port number (if non-default) |
| `password` | Encrypted password |
| `ssl_mode` | SSL mode setting |
| `connection_timeout` | Timeout in seconds (if set) |
