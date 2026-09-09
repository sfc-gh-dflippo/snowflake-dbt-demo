---
name: worker-local-setup
description: Install and start the Data Exchange Worker on a user-managed machine (laptop, cloud VM, or on-prem server).
parent_skill: data-infrastructure-setup
license: Proprietary. See License-Skills for complete terms
---

# Worker Local Setup

Set up and run the Data Exchange Worker on whatever machine will execute it: a laptop, a cloud VM, an on-premises server, or one host per worker when scaling out. The steps are the same on each host.

## Prerequisites

> **Note:** Ensure the host can reach both the source database and your Snowflake account (and meets any corporate firewall or proxy rules when applicable).

Prerequisites depend on the **source dialect** and the **extraction strategy** chosen in data migration setup. Load [extraction-strategies-reference.md](../../migrate-objects/actions/data-migration/references/extraction-strategies-reference.md) for the full matrix; complete the matching section below before Step 1.

### SQL Server — `regular` (ODBC)

The Data Exchange Worker connects to SQL Server via the Microsoft ODBC Driver. Before starting the worker, verify it is installed:

```bash
odbcinst -q -d 2>/dev/null | grep -i "ODBC Driver"
```

**If the command returns a driver name** (e.g. `[ODBC Driver 18 for SQL Server]`), the driver is present — continue to Step 1.

**If the command returns nothing**, the driver is missing. **Stop here and ask the user to install it** — do not attempt installation yourself, as it requires `sudo` and interactive steps that cannot be automated.

Tell the user:

> The Data Exchange Worker requires the Microsoft ODBC Driver for SQL Server to connect to your source database. Please install it and then resume.
>
> **macOS — Homebrew (recommended):**
> ```bash
> brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
> brew update
> HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18
> ```
> The `brew tap` step may ask you to confirm adding a third-party repository — this is expected.
>
> **macOS — without Homebrew:**
> Download and install the `.pkg` from the [Microsoft ODBC Driver download page](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server). Choose the macOS package matching your architecture (`arm64` for Apple Silicon, `x86_64` for Intel).
>
> **After installing**, verify with:
> ```bash
> odbcinst -q -d | grep -i "ODBC Driver"
> ```
> Then resume the setup.

Once the user confirms the driver is installed, re-run the check and continue.

### PostgreSQL — `regular` (COPY)

No ODBC driver. The worker uses bundled Npgsql with `use_copy = true`. Skip the ODBC pre-flight above.

### Oracle — `regular` (ODP.NET)

No SQL Server ODBC check. Ensure the worker can reach Oracle with the service name in TOML `database` (same as scai connection).

### Oracle — `dbms_cloud`

Configure `dbms_cloud_credential_name` and `dbms_cloud_file_uri_prefix` in `[connections.source.oracle]` after generate-config. Oracle must grant `EXECUTE` on `DBMS_CLOUD` and a credential for the HTTPS prefix. Set `extraction.strategy: dbms_cloud` and `externalStage` in workflow YAML. See extraction-strategies reference and `dmvf/data-exchange-agent/docs/oracle-dbms-cloud-local-setup.md`.

### Redshift — `unload`

Add `unload_s3_bucket` and `unload_iam_role_arn` to `[connections.source.redshift]`. Set `extraction.strategy: unload` and `externalStage` in workflow YAML.

### Teradata — `tpt`

Install Teradata TTU on the worker host (`tbuild`). Optional `tpt_*` fields in TOML. Workflow may use `extraction.strategy: tpt`.

### Teradata — `write_nos`

Configure `write_nos_*` fields in `[connections.source.teradata]`. Set `extraction.strategy: write_nos` and `externalStage` in workflow YAML.

## Step 1 — Generate the Worker Config

> **Skip this step** for Iceberg migration strategies that don't use a Worker (`catalog_link`, `convert_to_managed`, `copy_files` with `sourceDataStage`).

If the project's `.scai/config/dew_configuration.toml` (path relative to the SCAI project root) already exists with no `<PLACEHOLDER>` tokens, report "Worker config already complete" and continue to Step 2.

Otherwise, run:

```bash
scai data worker generate-config
```

Run inside the project (no path argument) — scai writes the project-default `.scai/config/dew_configuration.toml`.

This pre-fills `[connections.source.<engine>]` from the project's scai source connection (host, user, database, port, and engine-specific fields like SQL Server's `trust_server_certificate` and `encrypt`, or Teradata `authentication = "LDAP"` when `--auth ldap`). The CLI will prompt before overwriting an existing file; pass `-y` to overwrite without prompting.

> **Affinity:** when this flow is driven through the plugin, `data_infrastructure(mode="up")` generates this config. With no explicit override, scai applies the same stable project default used by workflow generation. If `configure(affinity="<label>")` set an override, the plugin passes that label to both generators and regenerates a stale DEW config whose affinity differs. When running `generate-config` yourself, omit `--affinity` to use the project default or pass the same explicit `--affinity <label>` as the workflow. See the [Affinity Reference](../references/affinity-reference.md).

After running, handle the result:

- **No placeholders remain** — show the user the pre-filled values from the scai connection (`[connections.source.*]` host, port, user, database) and ask them to confirm. Only edit if something is wrong; do **not** re-prompt for fields that already have real values.
- **Placeholders remain** — open the file and replace each `<PLACEHOLDER>` token. If the scai connection lacked a field (e.g., no `port`), ask the user for just that one field.

> The scai connection populates `[connections.source.*].database`. This value **must match** `source.databaseName` in the migration workflow YAML / validation JSON. A mismatch causes the orchestrator to report "table does not exist in the source database." If the user wants to migrate a different database than the one in their scai connection, update it here and use the same value in the workflow YAML.
>
> **Oracle:** `database` in the worker TOML is the Oracle **service name** (from `--service-name` on `scai connection add-oracle`), not a SQL Server–style database name. Use the same service name in workflow YAML `source.databaseName`.
>
> **Teradata:** `database` in the worker TOML is the Teradata **database name** (from `--database` on `scai connection add-teradata`). Use the same value in workflow YAML `source.databaseName`. For LDAP connections, confirm `authentication = "LDAP"` is present when the scai connection uses `--auth ldap`.
>
> **PostgreSQL:** The worker uses PostgreSQL's native COPY protocol (`use_copy = true`) for all data extraction. The `database` field is the actual PostgreSQL database name. No special driver is required — Npgsql is bundled with the worker.

See [`../references/worker-config-reference.md`](../references/worker-config-reference.md) for the field reference and advanced options (e.g., Redshift UNLOAD, Teradata TPT / WRITE_NOS).

## Step 2 — Start the Worker

Run:

```bash
scai data worker start --local
```

This command installs the worker if it is not already present, then starts it using the project-default configuration at `.scai/config/dew_configuration.toml`.

Use the status printed by this command. **Never add a Bash `sleep` or shell
polling loop after startup**; if startup does not report a healthy worker,
diagnose that result directly.

Tell the user:

> **Cost note:** The local Data Exchange Worker polls Snowflake on an interval and can accrue warehouse credits even when no migration tasks are running. Stop the worker when data work for this wave is done (teardown skill), or when ending the session if it was started outside MCP.

## Step 3 — Verify the Worker Is Running

The CLI prints worker status on startup. Confirm the output shows the worker has connected to the orchestrator and is polling for tasks.

If the worker fails to start, check:
- **SQL Server only:** ODBC driver installed (`odbcinst -q -d | grep -i "ODBC Driver"`) — if missing, follow the pre-flight instructions in the Prerequisites section above
- Source database credentials in the TOML config
- Network connectivity to the source database from the host
- Snowflake connection details in `~/.snowflake/config.toml` (or `%USERPROFILE%\.snowflake\config.toml` on Windows)

## Done

The worker is running on the host. Return control to the parent skill, which runs Level 1 Data Doctor before proceeding.
