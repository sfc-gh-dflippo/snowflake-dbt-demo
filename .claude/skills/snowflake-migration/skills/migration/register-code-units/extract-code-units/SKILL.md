---
name: extract-code-units
description: Extract DDL and source code from a connected source database using scai CLI. Pulls tables, views, procedures, functions, and other objects. Triggers: extract, pull ddl, extract code, get source code.
parent_skill: register-code-units
license: Proprietary. See License-Skills for complete terms
---

# Code Extraction

## On Entry

Tell the user:
> **Extracting from source database.**
>
> Here's what I'll do:
> 1. Connect to your source database using the configured connection.
> 2. Run read-only queries to enumerate the objects in scope.
> 3. Extract the DDL and code for each one, and save them under `source/`.

## Prerequisites

- Migration project initialized (`scai init`)
- `configure()` called at session start — validates the source connection and, for Oracle/Teradata, seeds the driver cache via [`../../connection/references/driver-bootstrap.md`](../../connection/references/driver-bootstrap.md)
- Network access to source database

## Workflow

### Step 1: Ask What to Extract

Ask the user what they want to extract. Present the available object types for their source dialect:

- **SqlServer:** TABLE, VIEW, FUNCTION, PROCEDURE, SEQUENCE, TABLE_TYPE, TRIGGER
- **Redshift:** TABLE, VIEW, MATERIALIZED_VIEW, FUNCTION, PROCEDURE
- **Oracle:** TABLE, VIEW, MATERIALIZED_VIEW, FUNCTION, PROCEDURE, PACKAGE, PACKAGE_BODY, TRIGGER, SEQUENCE, TYPE, TYPE_BODY, SYNONYM
- **Teradata:** TABLE, VIEW, FUNCTION, PROCEDURE
- **Postgresql:** TABLE, VIEW, MATERIALIZED_VIEW, FUNCTION, PROCEDURE

Ask the user via `ask_user_question` (`multiSelect = false`):

> "What would you like to extract? You can choose:"
> 1. **All objects** - Extract everything from the source database
> 2. **Specific object types** - e.g. just tables and views, or just procedures
> 3. **Specific schemas** - Limit to one or more schemas
> 4. **Name filter** - Exact object name, or a wildcard with `*` (e.g. `Employees` or `Get*Data`)

Allow combining options (e.g. specific types within a specific schema).

If the source server hosts several databases and the user wants more than the connection's
own, also ask **which databases** — see the multi-database flow in Step 2.

> **Name matching:** `-n` / `--name` is an **exact** case-insensitive match unless the
> pattern contains `*`. Do **not** pass a bare prefix expecting substring match —
> that used to pull sibling objects (e.g. `FOO` matching `FOO_SWTCH`). For partial
> matches use wildcards: `FOO*`, `*Employee*`. When the user lists specific table
> names, pass each exact name or extract by schema/type and let them confirm the
> catalog count.

### Step 2: Run Extraction

Build the `scai code extract` command based on user selections:

```bash
# Base command
scai code extract -s <CONNECTION_NAME> --json

# Add flags based on user choices:
#   -d, --database <DATABASE> extract from a specific database on the server,
#                             overriding the connection's own database
#   --schema <SCHEMA>        filter by schema
#   -t TYPE1,TYPE2           filter by object type
#   -n "Name"                exact name (case-insensitive); use * for wildcards
#   --driver-path <PATH>     path to driver .nupkg (Oracle only, first use)
```

**Multiple databases on one server (SqlServer, AzureSynapse, Redshift, Postgresql, Teradata).**
A source connection points at one database, but its server may host several. To migrate more
than one, pass a comma-separated list with `-d` — the CLI loops internally, continues past a
single database's failure, and returns one JSON envelope with per-database counts plus the
aggregate. Do **not** re-run without `-d`; that only re-pulls the connection's own database.
(Oracle and BigQuery don't bind a swappable database in the connection, so `-d` is rejected there —
use the connection's own database / schemas.)

1. **List the databases** on the connection's server with `query_source` (dialect-specific):
   - **SqlServer / AzureSynapse:** `SELECT name FROM sys.databases WHERE database_id > 4` (excludes the
     `master`/`tempdb`/`model`/`msdb` system databases).
   - **Redshift / Postgresql:** `SELECT datname FROM pg_database WHERE datistemplate = false`.
   - **Teradata:** `SELECT DatabaseName FROM DBC.DatabasesV WHERE DBKind = 'D'`.
2. **Ask which to extract** via `ask_user_question` (`multiSelect = true`), defaulting to the
   connection's own database.
3. **Run one extraction** with every selected database:

```bash
scai code extract -s <CONNECTION_NAME> -d Sales,Inventory --json
```

Output nests each under `source/<database>/…`, and the Code Unit Registry is regenerated once
after the run (the command re-scans the whole `source/` tree), so all coexist in one project.
Omit `-d` when the connection's own database is the only target.

**Driver note (Oracle / Teradata):** `configure()` seeds the driver cache, so `--driver-path` is normally not needed here. If the cache was missed for any reason, pass `--driver-path <PATH_TO_NUPKG>` on first use; SCAI persists the path machine-wide and reuses it across projects.

**Examples:**
```bash
# All objects
scai code extract -s <CONNECTION_NAME> --json

# All objects from a specific database on the server
scai code extract -s <CONNECTION_NAME> --database Sales --json

# Only tables and views in the dbo schema
scai code extract -s <CONNECTION_NAME> --schema dbo -t TABLE,VIEW --json

# Exact table name
scai code extract -s <CONNECTION_NAME> -t TABLE -n "SNAPM_EDB_MODEL_GROUPING" --json

# Procedures matching a wildcard pattern
scai code extract -s <CONNECTION_NAME> -t PROCEDURE -n "Get*Data" --json

# Oracle: first extraction with driver path
scai code extract -s <CONNECTION_NAME> --driver-path ./Oracle.ManagedDataAccess.Core.nupkg --json

# Oracle: extract only packages and procedures from a schema
scai code extract -s <CONNECTION_NAME> --schema HR -t PACKAGE,PROCEDURE --json

# Teradata: first extraction with driver path
scai code extract -s <CONNECTION_NAME> --driver-path ./Teradata.Client.Provider.nupkg --json

# Teradata: extract only procedures from a database
scai code extract -s <CONNECTION_NAME> --schema MY_DB -t PROCEDURE --json
```

### Step 3: Verify Extraction

After extraction completes, verify the results: count `.sql` files under `source/` and list its sub-directories by object type. Use whichever portable form fits the host:

```bash
# macOS / Linux
find source/ -name "*.sql" | wc -l
ls -la source/*/
```

```powershell
# Windows PowerShell
(Get-ChildItem -Recurse -Filter *.sql source/).Count
Get-ChildItem source/ -Directory | ForEach-Object { Get-ChildItem $_ }
```

## Output Structure

```
source/
└── <database>/
    └── <schema>/
        ├── table/
        │   └── *.sql
        ├── view/
        │   └── *.sql
        ├── procedure/
        │   └── *.sql
        └── function/
            └── *.sql
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Failed to test credentials" | Check VPN, firewall rules, or credential validity |
| "IP not allowed" | Add your IP to database firewall (Azure Portal for Azure SQL) |
| "Connection timeout" | Verify network connectivity, increase timeout |
| Empty extraction | Verify schema names, check user permissions |
| `ORA-12154: TNS:could not resolve the connect identifier` | Verify Oracle host, port, and service name |
| `ORA-01017: invalid username/password` | Check Oracle credentials |
| `Socket closed` (Teradata) | Verify Teradata host and port (default 1025) |
| `Logon failed` (Teradata) | Check Teradata credentials |
| `Driver not found` | Re-download the NuGet package and pass `--driver-path` again |

## CHECKPOINT

Confirm with user:
- [ ] Extraction completed without errors
- [ ] Expected number of objects extracted
- [ ] Source files appear in `source/` directory

## On Completion

After the CHECKPOINT passes, tell the user. Fill placeholders from the JSON envelope returned by `scai code extract --json` (`catalog.{discovered,extracted,failed}`, `byType`, `databases[]`, `failures[]`, `executionTimeSeconds`). When you extracted several databases, read per-database counts from `databases[]` and the aggregate from `catalog` — do not sum envelopes across runs.

> **Extraction complete.** `<extracted>/<discovered>` objects extracted in `<duration>`, broken down by type (filled from `byType`). Files saved under `source/`.
> *If `failed > 0`:* `<failed>` failed. Most common error: `<top_failure_reason>`. Full list in the reports.

Then ask via `ask_user_question` (`multiSelect = false`):

> "Do you have any ETL code (SSIS or Informatica Power Center) to include?"
>
> 1. **Yes**
> 2. **No**

- If **no**, say that next we'll convert these to Snowflake SQL.
- If **yes**, ask for the ETL folder path and run (do **not** pass `--overwrite` — the extracted SQL is already in `source/`):

```bash
scai code add -i <ETL_PATH> --json
```

This arranges the packages into `source/_etl/`, where `convert` finds them without an external path flag.

Then return to the calling skill.
