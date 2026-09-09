# Extraction strategies by source dialect

**Extraction strategy** controls *how* data leaves the source system. It is separate from **migration type** (preliminary / incremental / full) and **sync strategy** (none / checksum / watermark).

The `data-migration-setup` state machine (`progress_setup(mode="data_migration")`) asks the user to pick a strategy when the dialect supports more than one option. For dialects with a single option, the machine still confirms the mechanism so Coco does not assume ODBC for every source.

After the user chooses, persist via `configure(data_migration_extraction_strategy=...)` and pass `extraction_strategy=` to `migrate_data(mode="setup", ...)`. Set `defaultTableConfiguration.extraction` in the workflow YAML (see [workflow-config-reference.md](./workflow-config-reference.md)).

---

## SQL Server (`SqlServer`)

| Strategy | How data moves | When to use |
|----------|----------------|-------------|
| **`regular`** (only option) | Data Exchange Worker reads via **Microsoft ODBC Driver** → Snowflake internal stage | Default for all table sizes |

**Setup required**

- [worker-local-setup/SKILL.md](../../../../data-infrastructure/worker-local-setup/SKILL.md) — ODBC driver pre-flight (`odbcinst -q -d`)
- Worker TOML `[connections.source.sqlserver]` — standard host/port/database/credentials from `scai data worker generate-config`
- Workflow YAML: `extraction.strategy: regular` (default)

---

## PostgreSQL (`Postgresql`)

| Strategy | How data moves | When to use |
|----------|----------------|-------------|
| **`regular`** (only option) | Worker uses **Npgsql + native COPY protocol** (`use_copy = true`) — **not ODBC** | Default; higher throughput than row-by-row ODBC reads |

**Setup required**

- No ODBC driver on the worker host
- Worker TOML `[connections.source.postgresql]` with `use_copy = true` (set by generate-config)
- Workflow YAML: `extraction.strategy: regular`

---

## Oracle (`Oracle`)

| Strategy | How data moves | When to use |
|----------|----------------|-------------|
| **`regular`** | Worker reads via **Oracle ODP.NET** (`Oracle.ManagedDataAccess`) → Snowflake internal stage | Smaller tables, simpler setup |
| **`dbms_cloud`** | Oracle runs **`DBMS_CLOUD.EXPORT_DATA`** to HTTPS object storage (e.g. S3) → Snowflake **external stage** | Large tables; reduces data through the worker machine |

**Setup — `regular`**

- Worker TOML `[connections.source.oracle]` — `database` = **service name** (same as scai connection)
- Workflow: `extraction.strategy: regular`

**Setup — `dbms_cloud`**

- Oracle DBA: `EXECUTE` on `DBMS_CLOUD`, credential via `DBMS_CLOUD.CREATE_CREDENTIAL` for the target bucket/prefix
- Worker TOML under `[connections.source.oracle]`:
  - `dbms_cloud_credential_name` — credential object name in Oracle
  - `dbms_cloud_file_uri_prefix` — `https://` URI prefix for exported objects (e.g. S3 bucket path)
- Workflow YAML:
  ```yaml
  extraction:
    strategy: dbms_cloud
    externalStage: MY_DB.MY_SCHEMA.S3_EXTERNAL_STAGE
  ```
- Snowflake external stage must point at the same object-storage prefix Oracle writes to

See DMVF doc `dmvf/data-exchange-agent/docs/oracle-dbms-cloud-local-setup.md` for local dev details.

---

## Redshift (`Redshift`)

| Strategy | How data moves | When to use |
|----------|----------------|-------------|
| **`regular`** | Worker reads via **ODBC** → Snowflake internal stage | Smaller tables, simpler networking |
| **`unload`** | Redshift **`UNLOAD`** to **S3** → Snowflake **external stage** | Large tables; avoids pulling full result sets through the worker |

**Setup — `regular`**

- Worker TOML `[connections.source.redshift]` — standard ODBC connection fields

**Setup — `unload`**

- Worker TOML adds:
  ```toml
  unload_s3_bucket = "my-migrations-bucket"
  unload_iam_role_arn = "arn:aws:iam::123456789012:role/MyRole"
  ```
- Workflow YAML:
  ```yaml
  extraction:
    strategy: unload
    externalStage: MY_DB.MY_SCHEMA.S3_EXTERNAL_STAGE
  ```
- IAM role must trust Redshift and allow writes to the bucket; Snowflake stage uses the same S3 path

See [worker-config-reference.md](../../../../data-infrastructure/references/worker-config-reference.md#advanced-redshift-unload).

### Iceberg target (Redshift only — partial support)

**`target_table_type=iceberg` is only supported for Redshift sources today.** Other dialects should use `native` (default). Do not offer Iceberg unless `source_language` is Redshift and the user explicitly wants it.

Iceberg is a **target** choice (`tableType: iceberg` + `icebergConfig`), separate from extraction. Supported paths:

| Path | Extraction | `migrationStrategy` | Worker? |
|------|------------|---------------------|---------|
| Redshift native tables → Snowflake Iceberg | `unload` (typical) | `copy_files` | UNLOAD on Redshift; Snowflake loads from stage |
| Redshift / Glue Iceberg tables → Snowflake Iceberg | none (metadata only) | `catalog_link` or `convert_to_managed` | Often **no worker** — orchestrator issues Snowflake DDL |

Prerequisites and AWS/Snowflake setup: [iceberg-setup-reference.md](./iceberg-setup-reference.md). Workflow fields and type mappings: [workflow-config-reference.md](./workflow-config-reference.md#icebergconfig). Orchestrator detail: `dmvf/docs/data-migration-orchestrator/iceberg-migration-support.md`.

---

## Teradata (`Teradata`)

| Strategy | How data moves | When to use |
|----------|----------------|-------------|
| **`regular`** | Worker reads via **`teradatasql`** (preferred) or Teradata ODBC → Snowflake internal stage | Most tables |
| **`tpt`** | **Teradata Parallel Transporter** bulk export on the worker host → Snowflake internal stage | Very large bulk loads (orchestrator uses `regular`; worker selects TPT from TOML) |
| **`write_nos`** | Teradata **`WRITE_NOS`** table function → cloud storage → Snowflake **external stage** | Large tables; server-side export |

**Setup — `regular`**

- Worker TOML `[connections.source.teradata]` — `database` matches workflow `source.databaseName`
- LDAP: `authentication = "LDAP"` when scai connection uses `--auth ldap`

**Setup — `tpt`**

- Teradata **TTU** installed on worker host (`tbuild` available)
- Optional TOML: `tpt_delimiter`, `tpt_max_sessions`
- Workflow: `extraction.strategy: tpt` (accepted as alias for `regular` at orchestrator; TPT enabled via worker config)

**Setup — `write_nos`**

- TOML `write_nos_*` fields under `[connections.source.teradata]` (see worker-config reference)
- Workflow:
  ```yaml
  extraction:
    strategy: write_nos
    externalStage: MY_DB.MY_SCHEMA.TD_NOS_STAGE
  ```

See DMVF docs: `teradata-odbc-extraction.md`, `tpt-extraction.md`, `write-nos-extraction.md` under `dmvf/docs/data-migration-orchestrator/`.

---

## After choosing a strategy

1. Complete any strategy-specific worker TOML / cloud / Oracle grant setup **before** `migrate_data(mode="run")`.
2. Ensure `defaultTableConfiguration.extraction` in the workflow YAML matches the choice.
3. Run [Data Doctor Level 2](../../../../data-infrastructure/references/data-doctor-reference.md#level-2-migration-workflow-yaml-ready) with `--config` before run.
