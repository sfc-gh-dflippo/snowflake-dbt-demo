# Teradata Connection Reference

Detailed reference for Teradata connection options, authentication methods, driver setup, and troubleshooting.

## Supported SCAI Operations

Teradata is a **full-migration** source. After `scai connection add-teradata` and a successful connection test:

| Area | Commands / flows |
|------|------------------|
| Connection | `scai connection test`, `scai query` |
| Code | `scai code extract`, `scai code convert`, `scai code deploy` |
| 2-sided testing | `scai test seed`, `scai test capture`, `scai test validate` |
| Cloud table data | `scai data migrate`, cloud data validation (Data Exchange Worker) |

New Teradata projects default to `project_type: full_migration`. Legacy projects with `project_type: code_conversion_only` in `project.yml` stay on the code-conversion-only path until upgraded.

## Driver Setup

Teradata requires the **`Teradata.Client.Provider` NuGet package** (.NET driver). This is **not** the Teradata JDBC driver (`terajdbc*.jar`) — SCAI uses .NET internally, so the JDBC driver will not work. The NuGet package is **not** bundled with SCAI.

### Download

```bash
# macOS / Linux
curl -L -o Teradata.Client.Provider.nupkg \
  https://www.nuget.org/api/v2/package/Teradata.Client.Provider

# Windows PowerShell
curl.exe -L -o Teradata.Client.Provider.nupkg `
  https://www.nuget.org/api/v2/package/Teradata.Client.Provider
```

### How Driver Caching Works

When `--driver-path` is provided, SCAI copies the file into `~/.snowflake/scai/drivers/teradata/`. On subsequent commands, SCAI checks that cache directory first. If a driver is found there, `--driver-path` is not needed.

- **Cache location:** `~/.snowflake/scai/drivers/teradata/`
- **Accepted formats:** `.nupkg` or `.dll` (must be the .NET Teradata driver, not JDBC)
- **Scope:** Machine-wide — shared across all projects
- **Persistence:** Until the cached file is manually deleted

### Commands That Accept `--driver-path`

| Command | When driver is needed |
|---------|----------------------|
| `scai connection test -l teradata --json` | Testing a Teradata connection |
| `scai code extract -s <conn> --json` | Extracting code from Teradata |
| `scai query -s <conn> --json` | Querying the Teradata source |
| `scai project defaults set -s <conn>` | Setting project defaults with a Teradata source |

### Pre-caching the Driver

To cache the driver without running any other operation, use `project defaults set`:

```bash
scai project defaults set -s <CONNECTION_NAME> --driver-path ./Teradata.Client.Provider.nupkg
```

Note: `--driver-path` alone is not sufficient — it must accompany another flag like `-s`.

## Connection Options

### Required Parameters

| Parameter | Flag | Description |
|-----------|------|-------------|
| Connection name | `-s, --source-connection` | Unique identifier for this connection |
| Authentication | `--auth` | Authentication method: `standard` or `ldap` |
| Host | `--host` | Teradata hostname or IP address |
| Database | `--database` | Teradata database name |
| Username | `--user` | Teradata database username |
| Password | `--password` | Teradata password (prompted securely if omitted) |

### Optional Parameters

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Port | `--port` | 1025 | Teradata server port number |
| Connection timeout | `--connection-timeout` | 30 | Timeout in seconds |

## Authentication Methods

### Standard Authentication (Username/Password)

```bash
scai connection add-teradata \
  --source-connection my-teradata \
  --auth standard \
  --host teradata-server.example.com \
  --database MY_DB \
  --user dbc
```

Password will be prompted securely.

**When to use:**
- Direct Teradata authentication with database credentials

### LDAP Authentication

```bash
scai connection add-teradata \
  --source-connection my-teradata \
  --auth ldap \
  --host teradata-server.example.com \
  --database MY_DB \
  --user ldapuser
```

**When to use:**
- Organization uses LDAP-backed authentication for Teradata
- Credentials are managed by Active Directory or similar LDAP provider

**Full inline example with all options:**
```bash
scai connection add-teradata \
  --source-connection my-teradata \
  --auth standard \
  --host teradata-server.example.com \
  --port 1025 \
  --database MY_DB \
  --user dbc \
  --password mypassword \
  --connection-timeout 60
```

## Connection String Format

For reference, SCAI builds Teradata connection strings in this format:

```
Data Source=<host>;Database=<db>;User ID=<user>;Password=***;Port Number=<port>;
```

For LDAP authentication, an additional segment is appended:

```
Data Source=<host>;Database=<db>;User ID=<user>;Password=***;Authentication Mechanism=LDAP;Port Number=<port>;
```

## Port Configuration

### Default Port (1025)

Most Teradata instances use the default port:

```bash
scai connection add-teradata \
  --source-connection my-teradata \
  --auth standard \
  --host teradata-server.example.com \
  --database MY_DB \
  --user dbc
```

### Non-Default Port

For Teradata instances on custom ports:

```bash
scai connection add-teradata \
  --source-connection my-teradata \
  --auth standard \
  --host teradata-server.example.com \
  --port 1026 \
  --database MY_DB \
  --user dbc
```

## Data Exchange Worker (cloud migration / validation)

The Data Exchange Agent worker connects with **`teradatasql`** (preferred) or Teradata ODBC using the same host, port, database, and credentials as `scai connection add-teradata`. (SCAI code extraction uses the separate .NET `Teradata.Client.Provider` NuGet package — that driver is not used by the worker.) Ensure the Teradata user can:

- `SELECT` on tables (and views) being migrated or validated
- Read catalog/metadata needed for schema extraction (typical: `DBC` dictionary access or explicit grants as required by your security model)

Network: the worker host must reach the Teradata listener (`host`:`port`, default 1025). For SPCS workers, configure `EXTERNAL_ACCESS_INTEGRATIONS` for the database host and the NuGet driver download endpoint (see [`../../data-infrastructure/worker-spcs/SKILL.md`](../../data-infrastructure/worker-spcs/SKILL.md)).

Worker TOML `[connections.source.teradata].database` must be the **database name**, matching `source.databaseName` in migration/validation workflow YAML.

## Troubleshooting

### Driver Not Found

**Symptoms:**
- "Driver resolution failed"
- "No driver found for Teradata"

**Solutions:**
1. Download the NuGet package (see Driver Setup above)
2. Provide the path: `--driver-path ./Teradata.Client.Provider.nupkg`
3. Verify the file exists and has a `.nupkg` or `.dll` extension
4. Check if a cached driver exists: `ls ~/.snowflake/scai/drivers/teradata/`

### Socket Closed / Connection Refused

**Symptoms:**
- `Socket closed` or `Connection refused`

**Solutions:**
1. Verify the host is correct and reachable: `ping <host>`
2. Check the port number (default 1025)
3. Test network connectivity: `nc -zv <host> 1025`
4. Ensure Teradata Gateway is running on the target host

### Logon Failed

**Symptoms:**
- `Logon failed` or `Authentication failed`

**Solutions:**
1. Verify username and password are correct
2. Check if the account is locked
3. For LDAP auth: verify LDAP credentials with your admin
4. Verify the user has appropriate access to the specified database

### Database Does Not Exist

**Symptoms:**
- `Database does not exist` or `Object does not exist`

**Solutions:**
1. Verify the database name is correct (case-sensitive)
2. Check with `SELECT DatabaseName FROM DBC.DatabasesV WHERE DatabaseName = '<DB>'`
3. Ensure the user has access to the specified database

### Connection Timeout

**Symptoms:**
- Connection hangs then times out
- "Connection timeout expired"

**Solutions:**
1. **Check VPN** — Teradata databases are often in private networks
2. Verify firewall rules allow port 1025 (or custom port)
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
   traceroute <teradata-host>
   ```

2. **If VPN is connected but still failing:**
   - Check if split tunneling excludes the Teradata subnet
   - Ask IT/network team to verify VPN routes
   - Try connecting from the office network to confirm it's a VPN issue

### Insufficient Privileges

**Symptoms:**
- Extraction returns no objects or partial results
- `Access denied` errors

**Solutions:**
1. The user needs SELECT access to DBC dictionary views
2. Minimum grants for extraction:
   ```sql
   GRANT SELECT ON DBC.DatabasesV TO <username>;
   GRANT SELECT ON DBC.TablesV TO <username>;
   GRANT SELECT ON DBC.FunctionsV TO <username>;
   GRANT SHOW PROCEDURE ON <database> TO <username>;
   ```

## Verifying Connectivity

### Test with scai

```bash
scai connection test -l teradata -s <CONNECTION_NAME> --json
```

### Manual Network Test

```bash
# Test TCP connectivity to Teradata
nc -zv <host> 1025

# Or with telnet
telnet <host> 1025
```

### Check Teradata Status (if you have access)

```sql
-- Verify connection
SELECT * FROM DBC.DBCInfoV;
SELECT DATABASE;
SELECT SESSION;
```

## Finding Teradata Connection Details

### From the DBA

Ask the Teradata DBA for:
- **Host** — server hostname or IP (COP or Unity Director address)
- **Port** — server port (usually 1025)
- **Database** — the default database name
- **User credentials** — username with appropriate read access
- **Authentication method** — standard or LDAP

### From Existing Tools

If you already connect to Teradata via other tools (BTEQ, Teradata Studio, SQL Assistant):
- **Host** is the server name or IP used in those tools
- **Database** is the default database specified in the connection
- **Port** defaults to 1025 unless explicitly configured

## Stored Connection Format

SCAI stores Teradata connections in TOML format with these fields:

| TOML key | Description |
|----------|-------------|
| `auth_method` | `standard` or `ldap` |
| `user` | Teradata username |
| `host` | Teradata hostname or IP |
| `database` | Teradata database name |
| `port` | Port number (if non-default) |
| `password` | Encrypted password |
| `connection_timeout` | Timeout in seconds (if set) |
