# Windows Authentication from WSL / Linux

The Microsoft ODBC driver for SQL Server (`msodbcsql18`) supports Windows Authentication (`Integrated Security=True` / `Trusted_Connection=Yes`) on Linux and WSL **only via Kerberos**. WSL is not domain-joined the way a native Windows host is, so the driver cannot silently reuse your Windows session — it needs a Kerberos ticket in the WSL user's credentials cache.

On Windows, `Microsoft.Data.SqlClient` uses **SSPI**, which transparently pulls the logged-in user's existing TGT from LSA. On Linux/WSL there is no SSPI; the driver falls back to **GSSAPI / MIT Kerberos**, which will not invent credentials — a TGT must already exist (typically in `/tmp/krb5cc_<uid>`). Until you provide one, every connection attempt fails at handshake time.

When that ticket is missing or misconfigured, you typically see one of:

- `[Microsoft][ODBC Driver 18 for SQL Server]SSPI Provider: No credentials cache found`
- `[Microsoft][ODBC Driver 18 for SQL Server]Cannot generate SSPI context`
- `[Microsoft][ODBC Driver 18 for SQL Server]SSPI Provider: Realm not local to KDC`
- `The target principal name is incorrect. Cannot generate SSPI context.`
- `UnknownCredentials` (raised by `scai connection test` when the underlying SSPI error has no ticket to use)
- `Error Code: CNX0025` from `scai` — the wrapper error code for this whole class of SSPI failure

> **Note on the `user` / `--user` field.** When `--auth windows`, the `user` value stored in `sqlserver.toml` is just a label for the connection profile. It does **not** supply credentials and is **not** how the driver picks a principal. Prefixing it with a NetBIOS domain (e.g. `DOMAIN\user`) has no effect on auth. The principal that gets used is whoever ran `kinit` most recently in your shell.

You have two paths forward. Pick whichever fits the environment:

## Option A — Switch to Standard (username/password) authentication

If the SQL Server instance has SQL authentication enabled (Mixed Mode), this is by far the simplest path from WSL/Linux. No Kerberos setup is required.

```bash
scai connection add-sql-server \
  --source-connection my-sqlserver \
  --auth standard \
  --server-url <SERVER_URL> \
  --database <DATABASE> \
  --user <SQL_LOGIN>
```

The password is prompted securely. Confirm with the DBA that a SQL login exists for you (or request one) before going this route. If the server is configured for Windows-only authentication, this option will not be available and you must use Option B.

## Option B — Set up Kerberos in WSL to use Windows Authentication

This requires cooperation with the AD/SQL Server team because the exact realm, KDC hostnames, and SPN configuration vary per customer environment. The steps below are the generic shape — fill in the specifics for your domain.

### 1. Install the required packages

Ubuntu does not ship with the Microsoft ODBC driver or `sqlcmd`. Add the Microsoft apt repository, then install the Kerberos client and SQL Server tooling. The repo `.deb` is versioned by Ubuntu release — substitute your release number (`22.04`, `24.04`, etc.):

```bash
curl -sSL -O https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y \
  krb5-user \
  unixodbc-dev \
  msodbcsql18 \
  mssql-tools18

echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
export PATH="$PATH:/opt/mssql-tools18/bin"
```

Role of each package:

| Package         | Purpose |
|-----------------|---------|
| `krb5-user`     | `kinit`, `klist`, `kdestroy` — manages the TGT cache; ships `/etc/krb5.conf`. On RHEL/Fedora the equivalent is `krb5-workstation`. |
| `msodbcsql18`   | Microsoft ODBC driver; the component that performs the GSSAPI handshake. |
| `unixodbc-dev`  | ODBC driver manager + headers; required by many Python ODBC bindings (e.g. `pyodbc`). |
| `mssql-tools18` | `sqlcmd` and `bcp` — essential for isolating OS-layer vs `scai`-layer failures. |

Reference docs:
- MIT Kerberos admin guide: <https://web.mit.edu/kerberos/krb5-latest/doc/admin/index.html>
- `krb5.conf` man page: <https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html>
- Microsoft ODBC driver on Linux: <https://learn.microsoft.com/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server>
- Kerberos auth with the ODBC driver: <https://learn.microsoft.com/sql/connect/odbc/linux-mac/using-integrated-authentication>

### 2. Determine your real Kerberos realm

This step burns the most time when skipped. **Your Kerberos realm is not always the same as your email-style UPN suffix.** AD supports alternate UPN suffixes that look like DNS domains but aren't the actual AD domain — and MIT Kerberos only accepts the *real* realm (the one encoded in the `DC=` components of your distinguished name).

From inside WSL (with Windows interop enabled), the most reliable way to find the real realm is:

```bash
cmd.exe /c "whoami /fqdn"
# Example output:
# CN=alice,OU=Vendors-Users,OU=Partner,DC=partner,DC=example
#                                       ^^^^^^^^^^^^^^^^^^^
#   AD DNS domain = partner.example  →  Kerberos realm = PARTNER.EXAMPLE
```

`cmd.exe /c "echo %USERDNSDOMAIN%"` also returns this value on most AD-joined machines and is a quick sanity check.

Typical failure signatures when the wrong realm is used with `kinit`:

| `kinit ...@WRONG_REALM` output | What it means |
|-------------------------------|---------------|
| `Client not found in Kerberos database` | The realm is real but the principal doesn't exist there. Wrong realm for *this* user. |
| `Realm not local to KDC` | The realm name itself doesn't exist on the KDC you reached. Often happens when you `kinit` against a UPN suffix that is only a UPN alias, not a real AD domain. |
| `Cannot resolve KDC for realm` | DNS SRV lookup for `_kerberos._tcp.<realm>` returned nothing. Either the realm is wrong, or you need explicit `kdc = ...` entries in `krb5.conf`. |

If `cmd.exe` interop is not available (pure Linux host, locked-down WSL), ask the AD team directly for: the realm name, the KDC hostnames, and — if the SQL Server lives in a different realm than your user account — the trusted realm name and its KDCs.

### 3. Configure `/etc/krb5.conf`

The default `krb5.conf` that ships with Ubuntu contains only MIT demo realms (`ATHENA.MIT.EDU`, etc.). Add an explicit block for the corporate realm — DNS-SRV autodiscovery alone is unreliable when multiple realms are in play.

Ask the AD/SQL Server team for:

- The Kerberos **realm** (uppercased AD domain, e.g. `PARTNER.EXAMPLE`)
- One or more **KDC** hostnames (domain controllers)
- The **admin server** hostname (often the same as a KDC)
- The DNS suffixes that should map to the realm
- If SQL Server lives in a different (trusted) realm: that realm's name and KDCs too

A minimal `/etc/krb5.conf` shape for the common single-realm case:

```ini
[libdefaults]
    default_realm = PARTNER.EXAMPLE
    dns_lookup_realm = false
    dns_lookup_kdc = true
    ticket_lifetime = 24h
    renew_lifetime = 7d
    forwardable = true
    rdns = false

[realms]
    PARTNER.EXAMPLE = {
        kdc = dc1.partner.example
        kdc = dc2.partner.example
        admin_server = dc1.partner.example
        default_domain = partner.example
    }

[domain_realm]
    .partner.example = PARTNER.EXAMPLE
    partner.example  = PARTNER.EXAMPLE
```

**Cross-realm case.** If the user account lives in `PARTNER.EXAMPLE` but the SQL Server's DNS suffix is `co.example.org` (a different, trusted realm), add the second realm and map its hostnames:

```ini
[realms]
    PARTNER.EXAMPLE = { ... as above ... }
    CO.EXAMPLE.ORG = {
        kdc = dc1.co.example.org
        admin_server = dc1.co.example.org
        default_domain = co.example.org
    }

[domain_realm]
    .partner.example   = PARTNER.EXAMPLE
    partner.example    = PARTNER.EXAMPLE
    .co.example.org    = CO.EXAMPLE.ORG
    co.example.org     = CO.EXAMPLE.ORG
```

The `[domain_realm]` mappings are what let libkrb5 know which realm a given SQL Server FQDN belongs to. Without them, the cross-realm referral step in section 5 cannot run.

Notes:

- Realm names are case-sensitive and conventionally uppercase. `Realm not local to KDC` almost always means the realm in `[realms]` does not match the realm the KDC actually serves, or your principal's realm does not match `default_realm`.
- If the AD environment publishes KDCs via DNS SRV records (`_kerberos._tcp.<domain>`), `dns_lookup_kdc = true` lets you omit the explicit `kdc =` entries. Otherwise list them.

### 4. Acquire a Kerberos ticket

```bash
kinit <username>@PARTNER.EXAMPLE
```

You will be prompted for your AD password. The username **must** match an AD principal that has been granted SQL Server access; the realm must match what is configured above (uppercase).

Verify the ticket:

```bash
klist
# Default principal: alice@PARTNER.EXAMPLE
# Valid starting     Expires            Service principal
# ...                ...                krbtgt/PARTNER.EXAMPLE@PARTNER.EXAMPLE
```

For scripted checks, `klist -s` exits 0 if a valid TGT is present and non-zero otherwise — useful when wrapping `scai` in CI/CD or pre-flight scripts.

To clear tickets (useful when debugging realm mismatches):

```bash
kdestroy
```

**Ticket lifetime and renewal.** Default ticket lifetime is typically 10 hours and the renew-until window 7 days. For routine interactive use, expect to re-`kinit` once a day. While still within the renew-until window you can refresh without re-entering your password:

```bash
kinit -R
```

**For automation / unattended use,** request a keytab from your AD admin and skip the password prompt entirely:

```bash
kinit -kt /path/to/user.keytab <username>@PARTNER.EXAMPLE
```

Keytabs are credential files — treat them like private keys (`chmod 600`, never check into source control).

### 5. Verify with `sqlcmd` before retrying scai

This isolates Kerberos issues from anything `scai` is doing — by far the fastest way to debug:

```bash
sqlcmd -S "<SERVER_FQDN>" -d <DATABASE> -E -C \
       -Q "SELECT SUSER_SNAME(), @@SERVERNAME;"
```

- `-E` requests integrated (Kerberos) auth.
- `-C` trusts the server certificate (matches `trust_server_certificate = true` in `sqlserver.toml`).

If this fails, the problem is **below** `scai` — fix the Kerberos setup first.

After a successful query, `klist` will often show a chain of tickets that makes the cross-realm trust visible. For example, with the user in `PARTNER.EXAMPLE` and SQL Server in `CO.EXAMPLE.ORG`:

```
krbtgt/PARTNER.EXAMPLE@PARTNER.EXAMPLE
krbtgt/CO.EXAMPLE.ORG@PARTNER.EXAMPLE          <-- cross-realm referral
MSSQLSvc/sql1.co.example.org:1433@CO.EXAMPLE.ORG
```

That is the underlying mechanism of Windows authentication made visible: you `kinit` into your own realm, libkrb5 transparently requests referrals when contacting a server in another trusted realm.

### 6. Named instances and the SQL Browser caveat

Connection profiles often look like `server_url = "HOST\\INSTANCE"`. On WSL/Linux that syntax depends on the **SQL Server Browser service** answering on **UDP 1434** to resolve the instance name to a port. UDP 1434 is frequently blocked on corporate VPNs and is inconsistent over WSL networking, which leads to `Login timeout expired` failures that look like a Kerberos issue but aren't.

**Prefer the explicit `HOST,PORT` form on WSL/Linux:**

```toml
# Instead of:
server_url = "<HOST>\\<INSTANCE>"
# Prefer:
server_url = "<host.fqdn>,<PORT>"
```

Ask the DBA for the static TCP port the named instance listens on (it is fixed per instance and listed in SQL Server Configuration Manager → TCP/IP properties).

If you're seeing `Login timeout expired` with a named-instance `server_url`, this is almost certainly the cause — not Kerberos.

### 7. Retry the scai connection test

```bash
scai connection test -l sqlserver -s <SOURCE_CONNECTION_NAME> --json
```

If `klist` shows a valid TGT and `sqlcmd -E` succeeds but `scai` still reports `UnknownCredentials` / `CNX0025`, double-check that the connection was added with `--auth windows` and that the `<SERVER_FQDN>` matches the SPN registered for the SQL Server service (typically `MSSQLSvc/<host>:<port>` or `MSSQLSvc/<host>:<instance>`). SPN mismatches are the most common cause of `Cannot generate SSPI context` *after* a TGT is in place.

## Common Failure Modes

| Error | Most likely cause |
|-------|-------------------|
| `No credentials cache found` | `kinit` was never run, or the ticket has expired. Run `kinit <user>@<REALM>` and retry. |
| `Client not found in Kerberos database` | The realm exists but your principal doesn't live there. Wrong realm for this user — re-derive the realm from `whoami /fqdn` `DC=` components. |
| `Realm not local to KDC` | Realm in `krb5.conf` doesn't match what the KDC actually serves, or the principal's realm doesn't match `default_realm`. Often happens when you `kinit` against a UPN alias instead of the real AD domain. |
| `Cannot resolve KDC for realm` | DNS SRV lookup failed. Add explicit `kdc = ...` lines under `[realms]` or fix DNS resolution to the domain controllers. |
| `Cannot generate SSPI context` (TGT present) | TGT exists but no service ticket can be obtained for the SQL Server SPN. Usually a missing or duplicate SPN on the SQL Server service account. Requires AD admin to fix `MSSQLSvc/...` SPNs. |
| `The target principal name is incorrect` | SPN registration issue, or the `server_url` doesn't match the host that owns the SPN (e.g. using a CNAME alias when the SPN is registered to the A-record host). |
| `UnknownCredentials` / `CNX0025` (from scai) | Generic wrapper for any of the above when the driver returns no usable credential. Run `klist`, then `sqlcmd -E` to localize the failure. |
| `Login timeout expired` on a `HOST\INSTANCE` server_url | Not Kerberos. SQL Browser (UDP 1434) is blocked or unreachable from WSL. Switch to `HOST,PORT` form (see section 6). |

## Troubleshooting Checklist

When debugging from scratch, run these in order. The first failure is the one to fix:

1. `which kinit klist sqlcmd` — all three must resolve.
2. `klist -s && echo OK` — must print `OK` (valid TGT in cache).
3. `getent hosts <your DC>` — domain controllers must be resolvable from WSL.
4. `sqlcmd -S "<host-or-host,port>" -d <db> -E -C -Q "SELECT 1"` — must succeed before blaming `scai`.
5. `scai connection test -l sqlserver -s <profile> --json` — retry.

If step 4 succeeds but step 5 fails, the issue is in the `scai`-layer config (most often `--auth windows` not actually set, or the wrong `server_url` saved in the profile).

## When to fall back to Option A

If any of the following are true, Option A (standard auth) will save you significant time:

- The AD/SQL Server team cannot quickly provide realm/KDC/SPN details.
- The SQL Server SPN is broken or duplicated and you don't have AD admin rights.
- The migration is short-lived and a temporary SQL login is acceptable.
- You're running in CI/CD where maintaining a Kerberos ticket (or even a keytab) is impractical.

Otherwise, Kerberos (Option B) is the right long-term setup for environments that mandate Windows-only authentication.
