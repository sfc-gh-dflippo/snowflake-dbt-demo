# Oracle Connection Reference

Detailed reference for Oracle connection options, authentication methods, driver setup, and troubleshooting.

## Driver Setup

Oracle requires the **`Oracle.ManagedDataAccess.Core` NuGet package** (.NET driver). This is **not** the Oracle JDBC driver (`ojdbc*.jar`) — SCAI uses .NET internally, so the JDBC driver will not work. The NuGet package is **not** bundled with SCAI.

### Download

```bash
# macOS / Linux
curl -L -o Oracle.ManagedDataAccess.Core.nupkg \
  https://www.nuget.org/api/v2/package/Oracle.ManagedDataAccess.Core

# Windows PowerShell
curl.exe -L -o Oracle.ManagedDataAccess.Core.nupkg `
  https://www.nuget.org/api/v2/package/Oracle.ManagedDataAccess.Core
```

### How Driver Caching Works

When `--driver-path` is provided, SCAI copies the file into `~/.snowflake/scai/drivers/oracle/`. On subsequent commands, SCAI checks that cache directory first. If a driver is found there, `--driver-path` is not needed.

- **Cache location:** `~/.snowflake/scai/drivers/oracle/`
- **Accepted formats:** `.nupkg` or `.dll` (must be the .NET Oracle driver, not JDBC)
- **Scope:** Machine-wide — shared across all projects
- **Persistence:** Until the cached file is manually deleted

### Commands That Accept `--driver-path`

| Command | When driver is needed |
|---------|----------------------|
| `scai connection test -l oracle --json` | Testing an Oracle connection |
| `scai code extract -s <conn> --json` | Extracting code from Oracle |
| `scai query -s <conn> --json` | Querying the Oracle source |
| `scai project defaults set -s <conn>` | Setting project defaults with an Oracle source |

### Pre-caching the Driver

To cache the driver without running any other operation, use `project defaults set`:

```bash
scai project defaults set -s <CONNECTION_NAME> --driver-path ./Oracle.ManagedDataAccess.Core.nupkg
```

Note: `--driver-path` alone is not sufficient — it must accompany another flag like `-s`.

## Connection Options

### Required Parameters

| Parameter | Flag | Description |
|-----------|------|-------------|
| Connection name | `-c, --connection` | Unique identifier for this connection |
| Authentication | `--auth` | Authentication method: `standard` |
| Host | `--host` | Oracle hostname or IP address |
| Service name | `--service-name` | Oracle service name |
| Username | `--user` | Oracle database username |
| Password | `--password` | Oracle password (prompted securely if omitted) |

### Optional Parameters

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Port | `--port` | 1521 | Oracle listener port number |
| Connection timeout | `--connection-timeout` | 30 | Timeout in seconds |

## Authentication Methods

### Standard Authentication (Username/Password)

The only supported authentication method for Oracle.

```bash
scai connection add-oracle \
  --connection my-oracle \
  --auth standard \
  --host oracle-server.example.com \
  --service-name ORCL \
  --user myuser
```

Password will be prompted securely.

**When to use:**
- All Oracle connections (only method available)

**Full inline example with all options:**
```bash
scai connection add-oracle \
  --connection my-oracle \
  --auth standard \
  --host oracle-server.example.com \
  --port 1521 \
  --service-name ORCL \
  --user myuser \
  --password mypassword \
  --connection-timeout 60
```

## Connection String Format

For reference, SCAI builds Oracle connection strings in TNS format:

```
Data Source=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=<host>)(PORT=<port>))(CONNECT_DATA=(SERVICE_NAME=<service_name>)));User Id=<user>;Password=***;Connection Timeout=30;
```

The connection string always uses `SERVICE_NAME` in the `CONNECT_DATA` section.

## Port Configuration

### Default Port (1521)

Most Oracle instances use the default listener port:

```bash
scai connection add-oracle \
  --connection my-oracle \
  --auth standard \
  --host oracle-server.example.com \
  --service-name ORCL \
  --user myuser
```

### Non-Default Port

For Oracle instances on custom ports:

```bash
scai connection add-oracle \
  --connection my-oracle \
  --auth standard \
  --host oracle-server.example.com \
  --port 1522 \
  --service-name ORCL \
  --user myuser
```

## Data Exchange Worker (cloud migration / validation)

The worker connects with ODP.NET using the same credentials as `scai connection add-oracle`. Ensure the Oracle user can:

- `SELECT` on tables (and views) being migrated or validated
- Read data dictionary views needed for schema/metadata extraction (typical: `SELECT_CATALOG_ROLE` or explicit grants on `ALL_*` / `DBA_*` views as required by your security model)

Network: the worker host must reach the Oracle listener (`host`:`port`). For SPCS workers, configure `EXTERNAL_ACCESS_INTEGRATIONS` for the database host and the NuGet driver download endpoint (see [`../../data-infrastructure/worker-spcs/SKILL.md`](../../data-infrastructure/worker-spcs/SKILL.md)).

Worker TOML `[connections.source.oracle].database` must be the **service name**, matching `source.databaseName` in migration/validation workflow YAML.

## Troubleshooting

### Driver Not Found

**Symptoms:**
- "Driver resolution failed"
- "No driver found for Oracle"

**Solutions:**
1. Download the NuGet package (see Driver Setup above)
2. Provide the path: `--driver-path ./Oracle.ManagedDataAccess.Core.nupkg`
3. Verify the file exists and has a `.nupkg` or `.dll` extension
4. Check if a cached driver exists: `ls ~/.snowflake/scai/drivers/oracle/`

### TNS Resolution Failure (ORA-12154)

**Symptoms:**
- `ORA-12154: TNS:could not resolve the connect identifier specified`

**Solutions:**
1. Verify the host is correct and reachable: `ping <host>`
2. Verify the service name matches the Oracle instance
3. Check the port number (default 1521)
4. Test network connectivity: `nc -zv <host> 1521`

### Invalid Credentials (ORA-01017)

**Symptoms:**
- `ORA-01017: invalid username/password; logon denied`

**Solutions:**
1. Verify username and password are correct
2. Check if the account is locked: `SELECT account_status FROM dba_users WHERE username = '<USER>'`
3. Oracle usernames are case-sensitive when quoted — try uppercase
4. Verify the user has CONNECT privilege

### No Listener (ORA-12541)

**Symptoms:**
- `ORA-12541: TNS:no listener`

**Solutions:**
1. Verify the Oracle listener is running on the target host
2. Check the port number matches the listener configuration
3. Test the port directly: `nc -zv <host> 1521`
4. Ask the DBA to check: `lsnrctl status`

### Connection Timeout

**Symptoms:**
- Connection hangs then times out
- "Connection timeout expired"

**Solutions:**
1. **Check VPN** — Oracle databases are often in private networks
2. Verify firewall rules allow port 1521 (or custom port)
3. Increase timeout: `--connection-timeout 60`
4. Test network path: `traceroute <host>`

### VPN Connection Required

**Symptoms:**
- Timeout when host is correct
- Works from office but not remotely

**Solutions:**

1. **Verify VPN is connected:**
   ```bash
   ifconfig | grep -E "utun|tun|ppp"
   traceroute <oracle-host>
   ```

2. **If VPN is connected but still failing:**
   - Check if split tunneling excludes the Oracle subnet
   - Ask IT/network team to verify VPN routes
   - Try connecting from the office network to confirm it's a VPN issue

### Account Locked (ORA-28000)

**Symptoms:**
- `ORA-28000: the account is locked`

**Solutions:**
1. Ask the DBA to unlock: `ALTER USER <username> ACCOUNT UNLOCK`
2. Check if the account was locked due to failed login attempts
3. Verify the password profile's `FAILED_LOGIN_ATTEMPTS` setting

### Insufficient Privileges (ORA-01031)

**Symptoms:**
- `ORA-01031: insufficient privileges`
- Extraction returns no objects

**Solutions:**
1. The user needs SELECT access to `DBA_*` or `ALL_*` dictionary views
2. Minimum grants for extraction:
   ```sql
   GRANT SELECT ANY DICTIONARY TO <username>;
   -- or more restrictive:
   GRANT SELECT ON DBA_OBJECTS TO <username>;
   GRANT SELECT ON DBA_SOURCE TO <username>;
   GRANT SELECT ON DBA_TABLES TO <username>;
   GRANT SELECT ON DBA_VIEWS TO <username>;
   GRANT SELECT ON DBA_PROCEDURES TO <username>;
   GRANT SELECT ON DBA_TRIGGERS TO <username>;
   GRANT SELECT ON DBA_SEQUENCES TO <username>;
   GRANT SELECT ON DBA_SYNONYMS TO <username>;
   GRANT SELECT ON DBA_TYPES TO <username>;
   ```

## Verifying Connectivity

### Test with scai

```bash
scai connection test -l oracle -s <CONNECTION_NAME> --json
```

### Manual Network Test

```bash
# Test TCP connectivity to Oracle listener
nc -zv <host> 1521

# Or with telnet
telnet <host> 1521
```

### Check Oracle Status (if you have access)

```sql
-- Verify connection
SELECT * FROM V$VERSION;
SELECT SYS_CONTEXT('USERENV', 'SERVICE_NAME') FROM DUAL;
SELECT SYS_CONTEXT('USERENV', 'DB_NAME') FROM DUAL;
```

## Finding Oracle Connection Details

### From tnsnames.ora

If the Oracle instance is configured in `tnsnames.ora`:

```bash
# Common locations
cat $ORACLE_HOME/network/admin/tnsnames.ora
cat /etc/tnsnames.ora
```

Look for entries like:
```
ORCL =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = oracle-server.example.com)(PORT = 1521))
    (CONNECT_DATA =
      (SERVICE_NAME = ORCL)
    )
  )
```

Extract `HOST`, `PORT`, and `SERVICE_NAME` from the entry.

### From the DBA

Ask the Oracle DBA for:
- **Host** — server hostname or IP
- **Port** — listener port (usually 1521)
- **Service name** — the Oracle service name (not the SID)
- **User credentials** — username with appropriate read access

## Stored Connection Format

SCAI stores Oracle connections in TOML format with these fields:

| TOML key | Description |
|----------|-------------|
| `auth_method` | Always `standard` |
| `user` | Oracle username |
| `host` | Oracle hostname or IP |
| `service_name` | Oracle service name |
| `port` | Port number (if non-default) |
| `password` | Encrypted password |
| `connection_timeout` | Timeout in seconds (if set) |
