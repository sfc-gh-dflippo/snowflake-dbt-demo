# SQL Server Connection Reference

Detailed reference for SQL Server connection options, authentication methods, and troubleshooting.

## Connection Options

### Required Parameters

| Parameter | Flag | Description |
|-----------|------|-------------|
| Source connection name | `-s, --source-connection` | Unique identifier for this source connection |
| Server URL | `--server-url` | Hostname, IP address, or FQDN of SQL Server |
| Database | `--database` | Target database name |
| Authentication | `--auth` | Authentication method: `standard` or `windows` |

### Optional Parameters

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Port | `--port` | 1433 | SQL Server port number |
| Username | `--user` | - | SQL Server login (required for standard auth) |
| Password | `--password` | - | SQL Server password (prompted if not provided) |
| Connection timeout | `--connection-timeout` | 30 | Timeout in seconds |
| Encrypt | `--encrypt` | true | Enable TLS/SSL encryption |
| Trust server certificate | `--trust-server-certificate` | false | Skip certificate validation |

## Authentication Methods

### Standard Authentication (SQL Authentication)

Uses SQL Server username and password credentials.

```bash
scai connection add-sql-server \
  --source-connection my-sqlserver \
  --auth standard \
  --server-url myserver.database.windows.net \
  --database AdventureWorks \
  --user myuser
```

**When to use:**
- Connecting to Azure SQL Database
- Connecting to SQL Server with SQL authentication enabled
- CI/CD pipelines and automation

### Windows Authentication (Integrated Security)

Uses the current Windows domain credentials.

```bash
scai connection add-sql-server \
  --source-connection my-sqlserver \
  --auth windows \
  --server-url myserver.corp.local \
  --database AdventureWorks
```

**When to use:**
- On-premises SQL Server with Active Directory
- When running from a domain-joined machine
- When SQL authentication is disabled

**Requirements:**
- Must be running on Windows or have Kerberos configured
- Current user must have access to the SQL Server

## SSL/TLS Configuration

### Azure SQL Database

Azure SQL Database requires encrypted connections:

```bash
scai connection add-sql-server \
  --source-connection azure-sql \
  --auth standard \
  --server-url myserver.database.windows.net \
  --database mydb \
  --user myuser \
  --encrypt true
```

### Self-Signed Certificates

For development environments with self-signed certificates:

```bash
scai connection add-sql-server \
  --source-connection dev-sql \
  --auth standard \
  --server-url dev-server.local \
  --database mydb \
  --user sa \
  --encrypt true \
  --trust-server-certificate true
```

**Warning:** Only use `--trust-server-certificate true` in development environments. Never use in production.

## Port Configuration

### Default Port (1433)

Most SQL Server instances use the default port:

```bash
scai connection add-sql-server \
  --source-connection my-sqlserver \
  --server-url myserver.example.com \
  --database mydb \
  --auth standard \
  --user myuser
```

### Non-Default Port

For SQL Server instances on custom ports:

```bash
scai connection add-sql-server \
  --source-connection my-sqlserver \
  --server-url myserver.example.com \
  --port 1434 \
  --database mydb \
  --auth standard \
  --user myuser
```

### Named Instances

For named instances, use the instance name in the server URL:

```bash
scai connection add-sql-server \
  --source-connection my-sqlserver \
  --server-url myserver.example.com\\INSTANCENAME \
  --database mydb \
  --auth standard \
  --user myuser
```

## Troubleshooting

### VPN Connection Required

Some SQL Server instances require VPN access before connecting.

**Symptoms:**
- "Connection timeout expired" when server URL is correct
- Unable to ping or reach the server
- Works from office network but not remotely

**Solutions:**

1. **Ask the user** which VPN client they use:
   - Cisco AnyConnect
   - GlobalProtect (Palo Alto)
   - OpenVPN
   - WireGuard
   - Corporate VPN client

2. **Verify VPN is connected:**
   ```bash
   # Check if VPN interface exists
   ifconfig | grep -E "utun|tun|ppp"
   
   # Check routing to server
   traceroute <server-url>
   ```

3. **Common VPN commands:**
   ```bash
   # Cisco AnyConnect (macOS)
   /opt/cisco/anyconnect/bin/vpn connect <vpn-host>
   /opt/cisco/anyconnect/bin/vpn status
   
   # GlobalProtect (macOS)
   # Usually connected via menu bar app
   
   # OpenVPN
   sudo openvpn --config <config-file>.ovpn
   ```

4. **If VPN is connected but still can't reach server:**
   - Check if split tunneling is enabled (some traffic may bypass VPN)
   - Verify the SQL Server is accessible from VPN network
   - Ask IT/network team to confirm VPN routes include the SQL Server subnet

**Tip:** If VPN connection is required, document it in the project so other team members know.

---

### Connection Timeout

**Symptoms:**
- "Connection timeout expired"
- "A network-related or instance-specific error occurred"

**Solutions:**
1. Verify network connectivity: `ping <server-url>`
2. Check firewall rules allow port 1433 (or custom port)
3. Increase timeout: `--connection-timeout 60`
4. Verify SQL Server is running and accepting connections

### Authentication Failures

**Symptoms:**
- "Login failed for user"
- "Cannot open database requested by the login"

**Solutions:**
1. Verify username and password are correct
2. Confirm user has access to the specified database
3. Check SQL Server authentication mode (Mixed Mode required for SQL auth)
4. For Windows auth, verify domain connectivity

### Windows auth from WSL/Linux

**Symptoms** (any of these from `scai connection test` or the underlying ODBC driver when `--auth windows` is used):
- `UnknownCredentials`
- `Cannot generate SSPI context`
- `The target principal name is incorrect. Cannot generate SSPI context.`
- `SSPI Provider: Realm not local to KDC`
- `SSPI Provider: No credentials cache found`
- `Client not found in Kerberos database`
- `Error Code: CNX0025` (the `scai` wrapper error code for this whole class of failure)

**Cause:** The Microsoft ODBC driver for SQL Server requires a Kerberos ticket to perform Windows Authentication from WSL or Linux — there is no implicit "current Windows user" the way there is on a domain-joined Windows host. The `user` field in `sqlserver.toml` is just a label and does **not** supply credentials when `--auth windows`.

**Solutions:**
1. If SQL authentication is enabled on the server, switch the connection to `--auth standard` (username/password). This is the fastest fix and avoids Kerberos entirely.
2. Otherwise, set up Kerberos in WSL (install `krb5-user`, determine your real AD realm from `cmd.exe /c "whoami /fqdn"`, configure `/etc/krb5.conf` for that realm and its KDCs, then `kinit <user>@<REALM>`) and retry the test.

> Tip: if `server_url` uses `HOST\INSTANCE` syntax and you see `Login timeout expired`, that's a separate problem — SQL Browser (UDP 1434) is usually blocked on WSL/VPN. Prefer `HOST,PORT` form.

See [`./wsl-windows-auth.md`](./wsl-windows-auth.md) for the full walkthrough of both options, including package list, how to find the correct realm, `krb5.conf` shape (single-realm and cross-realm), keytab use for automation, and how to verify with `klist` and `sqlcmd -E` before retrying `scai`.

### SSL/TLS Errors

**Symptoms:**
- "SSL Provider: The certificate chain was issued by an authority that is not trusted"
- "A connection was successfully established with the server, but then an error occurred during the pre-login handshake"

**Solutions:**
1. For self-signed certs in dev: `--trust-server-certificate true`
2. Install the server's CA certificate on your machine
3. Verify the server URL matches the certificate's CN/SAN

### Named Instance Not Found

**Symptoms:**
- "SQL Server Browser service is not running"
- "Cannot connect to named instance"

**Solutions:**
1. Use explicit port instead of instance name
2. Ensure SQL Server Browser service is running on the server
3. Verify UDP port 1434 is open for SQL Server Browser

### Azure SQL Specific Issues

**Symptoms:**
- "Cannot open server requested by the login"
- "Client IP address is not authorized"

**Solutions:**
1. Add your IP to Azure SQL firewall rules
2. Verify the server name includes `.database.windows.net`
3. Ensure Azure AD authentication is configured if using AAD

## Connection String Formats

For reference, the `scai` CLI generates connection strings in this format:

**Standard Authentication:**
```
Server=myserver.database.windows.net,1433;Database=mydb;User Id=myuser;Password=***;Encrypt=True;TrustServerCertificate=False;
```

**Windows Authentication:**
```
Server=myserver.corp.local;Database=mydb;Integrated Security=True;Encrypt=True;
```

## Verifying Connectivity

### Test with scai

```bash
scai connection test -l sqlserver -s <CONNECTION_NAME> --json
```

### Manual Network Test

Test basic network connectivity:

```bash
# Test TCP connectivity
nc -zv <server-url> 1433

# Or with telnet
telnet <server-url> 1433
```

### Check SQL Server Status

If you have direct access to the SQL Server machine:

```sql
-- Check if SQL Server is accepting connections
SELECT @@VERSION;
SELECT @@SERVERNAME;
```
