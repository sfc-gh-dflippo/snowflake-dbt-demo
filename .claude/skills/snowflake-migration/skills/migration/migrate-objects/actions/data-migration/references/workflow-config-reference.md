# Workflow YAML Configuration Reference

> **Field naming:** Use **camelCase** for all workflow YAML keys (for example `targetPartitionSizeMb`, `whereClauseCriteria`, `trackDeletions`). The orchestrator accepts snake_case as a fallback for migration configs, but generated files and this reference use camelCase only.

## Top-Level Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `schemaVersion` | String | No | Semantic version of this config shape (for example `"1"`, `"1.2"`). Omit for current defaults. |
| `tables` | `TableConfiguration[]` | Yes | Tables to migrate |
| `defaultTableConfiguration` | `TableConfiguration` | No | Shared defaults inherited by all tables |
| `affinity` | String | No | Only orchestrator and worker instances with a matching affinity will process this workflow. If the SPCS orchestrator was started with a specific affinity (visible in service logs as `Orchestrator affinity: <value>`), the workflow **must** set the same value or it will be silently skipped. The worker's `[application].affinity` must also match. Omit from all sides for fresh setups. |
| `preflight` | Boolean | No | When `true`, cap each table to one partition and run against a transient `PREFLIGHT_<workflowId>` schema (bounded dry-run). Default `false`. |
| `preflightKeepSchema` | Boolean | No | When `preflight` is `true`, skip cleanup so the transient schema remains for manual inspection. Default `false`. |
| `cleanUpTransientResources` | `"never"` \| `"on-success"` \| `"always"` | No | Delete intermediate stage files for this workflow after it finishes (`TASK_RESULTS` and any external stages used by extraction). Default `"on-success"`. Underscores are accepted (`on_success`). Set `"never"` to retain stage files for debugging. When the orchestrator runs in Iceberg metadata mode, the omitted-key default may be `"always"` instead — check your deployment profile if you rely on the default. |
| `intervalHandling` | `"interval"` \| `"varchar"` | No | How PostgreSQL/BigQuery mixed-family interval columns are mapped. Default `"interval"`. Can be overridden per table. |

## Preflight (bounded dry-run)

Set top-level `preflight: true` for a **migration smoke test**: each table runs as a single partition; loads go to transient schema `PREFLIGHT_<workflowId>`, not the configured production target. Optional `preflightKeepSchema: true` retains the schema after the workflow for inspection.

**Not the same as** Preliminary migration type (`whereClauseCriteria` loads to real targets) or `scai data doctor` (infra health checks).

When a customer asks for a dry-run or pipeline test before full migration, offer preflight at Step 2a. Full agent guidance: [Advanced operations reference](../../../../data-infrastructure/references/advanced-operations-reference.md#preflight-workflows-bounded-migration-dry-run).

## Teradata: mixed charsets and `onUntranslatable`

**When:** Teradata extraction fails with **6701** / **5355** (mixed charsets in one row), or the customer asks how to handle **untranslatable** non-Unicode bytes during migration.

**Default:** omit `onUntranslatable` or set `"substitute"` under `defaultTableConfiguration` — untranslatable bytes become **U+FFFD** and migration continues.

**Strict mode:** per-table `"onUntranslatable": "fail"` when any untranslatable byte must abort the partition (Teradata **6706**).

Applies to **`regular`**, worker-side **TPT**, and **`write_nos`** (orchestrator-built `SELECT`; no DEA TOML keys). Detail: `dmvf/docs/data-migration-orchestrator/teradata-charset-extraction.md`.

```yaml
defaultTableConfiguration:
  onUntranslatable: substitute
  extraction:
    strategy: regular   # or write_nos + externalStage
tables:
  - source: { databaseName: ecommerce, tableName: mixed_charset_orders }
    target: { databaseName: TARGET_DB, schemaName: ECOMMERCE_TD, tableName: MIXED_CHARSET_ORDERS }
    columnNamesToPartitionBy: [order_id]
  - source: { databaseName: ecommerce, tableName: strict_audit }
    target: { databaseName: TARGET_DB, schemaName: ECOMMERCE_TD, tableName: STRICT_AUDIT }
    columnNamesToPartitionBy: [id]
    onUntranslatable: fail
```

```yaml
preflight: true
preflightKeepSchema: false
```

## TableConfiguration

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `source` | `SourceTargetIdentifier` | Yes | Source table location |
| `target` | `TargetIdentifier` | Yes | Target table location in Snowflake |
| `columnNamesToPartitionBy` | `String[]` | Yes (native) | Columns used to partition data during extraction. **Not used for Iceberg loading** (see Iceberg section below). |
| `extraction` | `ExtractionStrategy` | No | How data is extracted from source |
| `synchronization` | `SynchronizationStrategy` | No | Incremental sync settings. **Does not apply to Iceberg migrations.** |
| `columnTypeMappings` | `ColumnTypeMapping[]` | No | Type conversions during migration |
| `columnNameMappings` | `ColumnNameMapping[]` | No | Column renaming mappings |
| `primaryKeyColumns` | `String[]` | No | Required for `watermark` sync with `trackModifications`; also used for incremental key tracking |
| `whereClauseCriteria` | String | No | SQL filter appended after `WHERE` in the extraction query (e.g., `"is_deleted = 0"`, `"c_custkey <= 1000"`). **Do not use** `TOP` (SQL Server) or `LIMIT` (Redshift/Oracle) here — they are not valid WHERE clause syntax and cause extraction errors. Teradata: use normal predicates (e.g. `"id <= 1000"`). |
| `targetPartitionSizeMb` | Integer | No | Target partition size in MB. Mutually exclusive with `targetPartitionSizeRows`. Omit both for auto sizing. |
| `targetPartitionSizeRows` | Integer | No | Target partition size in rows. Mutually exclusive with `targetPartitionSizeMb`. Omit both for auto sizing. |
| `loadSegmentation` | Object | No | Post-upload load segmentation — splits a single `COPY INTO` into multiple statements grouped by `targetSegmentSizeMb`. |
| `loading` | Object | No | Loading strategy: `warehouse` (default, `COPY INTO`) or `snowpipe`. |
| `queryModifiers` | Object | No | SQL hints to reduce locking on busy source tables during extraction (see [Query modifiers](#query-modifiers)). |
| `intervalHandling` | `"interval"` \| `"varchar"` | No | Per-table override of top-level `intervalHandling`. |
| `onUntranslatable` | `"substitute"` \| `"fail"` | No | **Teradata only.** How non-Unicode string columns handle untranslatable bytes during extraction. Default `"substitute"`. Set under `defaultTableConfiguration` for a workflow-wide default, or per table to override. Use `"fail"` when untranslatable non-Unicode bytes must abort the partition (Error 6706) instead of substituting U+FFFD. Detail: `dmvf/docs/data-migration-orchestrator/teradata-charset-extraction.md`. |
| `executionTimeoutMinutes` | Integer | No | Wall-clock timeout in minutes for the **Analyze boundaries** DEA task only (orchestrator default is **20** when omitted). Does **not** apply to extraction or load. Use per table for large/slow boundary queries, or under `defaultTableConfiguration` to apply to all tables. |

## SourceTargetIdentifier

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `databaseName` | String | Yes | Database name |
| `schemaName` | String | Yes\* | Schema name |
| `tableName` | String | Yes | Table name. Case-sensitive names must be quoted: `"\"MyCaseSensitiveTable\""` |

\* For **Teradata** sources, omit `source.schemaName` — Teradata is `database.table` (no schema layer). Align `databaseName` with `[connections.source.teradata].database` in worker TOML. Snowflake **target** still requires `schemaName`.

## TargetIdentifier

Extends `SourceTargetIdentifier` with optional Iceberg fields.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `databaseName` | String | Yes | Database name |
| `schemaName` | String | Yes | Schema name (always required on Snowflake targets, including Teradata migrations) |
| `tableName` | String | Yes | Table name |
| `tableType` | `"native"` \| `"iceberg"` | No | Target table format. Defaults to `"native"`. **`"iceberg"` is Redshift-source only today** (partial support). |
| `icebergConfig` | `IcebergConfig` | When `tableType` is `"iceberg"` | Iceberg-specific configuration (see below) |

## IcebergConfig

> **Scope:** End-to-end Iceberg migration is **Redshift-only** (native → UNLOAD → `copy_files`, or Glue-catalog `catalog_link` / `convert_to_managed`). Do not set `tableType: iceberg` for other source dialects unless product support expands.

Configuration for Iceberg table targets. Required when `tableType` is `"iceberg"`.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `catalog` | String | No | `"SNOWFLAKE"` (default) for Snowflake-managed Iceberg, or the name of a catalog integration (e.g. a Glue integration) |
| `externalVolume` | String | When `catalog` is `"SNOWFLAKE"` | Name of the Snowflake external volume |
| `baseLocationPrefix` | String | No | Prefix for the table's `BASE_LOCATION` path. Only applies when `catalog` is `"SNOWFLAKE"`. |
| `catalogTableName` | String | When `catalog` is not `"SNOWFLAKE"` | Table name in the external catalog. **If the catalog integration has `CATALOG_NAMESPACE` set, use the bare table name only** (e.g., `"customer"`). The namespace is prepended automatically. Using `"namespace.table"` will cause a double-prefix error. |
| `catalogSync` | String | No | Catalog integration name to sync Snowflake-managed metadata back to (for dual-engine access) |
| `sourceDataStage` | String | No | Stage path (must start with `@`) pointing to existing Parquet files. Only applies when `catalog` is `"SNOWFLAKE"`. |
| `migrationStrategy` | `"catalog_link"` \| `"convert_to_managed"` \| `"copy_files"` | No | Iceberg migration strategy. Auto-detected when omitted (see below). |

### Strategy Auto-Detection

When `migrationStrategy` is omitted, the orchestrator resolves it based on the `catalog` value:

| `catalog` Value | Auto-Detected Strategy |
|-----------------|------------------------|
| Not `"SNOWFLAKE"` (e.g. a Glue integration) | `catalog_link` |
| `"SNOWFLAKE"` | `copy_files` |

> To use `convert_to_managed`, you **must** set `migrationStrategy` explicitly — auto-detection defaults to `catalog_link` for external catalogs.

### IcebergConfig Validation Rules

| Rule | Error When Violated |
|------|---------------------|
| `tableType` must be `"native"` or `"iceberg"` | `ConfigurationError` |
| `icebergConfig` is required when `tableType` is `"iceberg"` | `ConfigurationError` |
| `externalVolume` is required when `catalog` is `"SNOWFLAKE"` | `ConfigurationError` |
| `catalogTableName` is required when `catalog` is not `"SNOWFLAKE"` | `ConfigurationError` |
| `migrationStrategy` must be one of the three valid values | `ValueError` |

### IcebergConfig Inheritance

The `icebergConfig` at the table level is **merged** with `defaultTableConfiguration.target.icebergConfig`. Table-level keys override default keys. Set common values (like `externalVolume`) in the defaults and only specify per-table values (like `catalogTableName`) on each table entry.

### Iceberg Strategy Comparison

| Strategy | Data Movement | DML on Target | Primary Use Case |
|----------|---------------|---------------|------------------|
| `catalog_link` | None (zero-copy) | Read-only | Quick access to existing Iceberg data without copying |
| `convert_to_managed` | None (zero-copy) | Full DML | Take ownership of existing Iceberg data without rewriting files |
| `copy_files` | Server-side binary copy | Full DML | Create a new Snowflake-managed Iceberg table from staged Parquet files |

## ExtractionStrategy

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `strategy` | `"regular"` \| `"unload"` \| `"tpt"` \| `"write_nos"` \| `"dbms_cloud"` | Yes | `"regular"` is the default. `"unload"` is Redshift-only. `"tpt"` and `"write_nos"` are Teradata-only. `"dbms_cloud"` is Oracle-only. See [extraction-strategies-reference.md](./extraction-strategies-reference.md) and [`worker-config-reference.md`](../../../../data-infrastructure/references/worker-config-reference.md). |
| `externalStage` | String | UNLOAD / WRITE_NOS / DBMS_CLOUD | Snowflake external stage (e.g. `MY_DB.MY_SCHEMA.S3_STAGE`) |

```yaml
extraction:
  strategy: regular

extraction:
  strategy: unload
  externalStage: MY_DB.MY_SCHEMA.S3_EXTERNAL_STAGE

extraction:
  strategy: dbms_cloud
  externalStage: MY_DB.MY_SCHEMA.S3_EXTERNAL_STAGE
```

## SynchronizationStrategy

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `strategy` | `"none"` \| `"checksum"` \| `"watermark"` | Yes | Sync strategy (default `none`) |
| `checksumExpression` | String | When `strategy` is `checksum` | Source SQL expression used to detect changed partitions (for example `MAX(ORA_ROWSCN)`). Must not contain `;`. |
| `watermarkColumn` | String | When `strategy` is `watermark` | Monotonic column used for incremental filtering |
| `trackModifications` | Boolean | No | When `true` with `watermark`, detect updated rows (requires `primaryKeyColumns`) |
| `trackDeletions` | Boolean | No | When `true` with `watermark`, detect deleted rows (requires `primaryKeyColumns`) |

| Strategy | Description | Best for |
|----------|-------------|----------|
| `none` (default) | Full extraction every run | One-time loads, or tables you will not re-migrate without clearing the target first |
| `checksum` | Hash all column values per partition; re-extract changed partitions only | Dimension tables without a monotonic column. **Oracle:** built-in partition checksum is supported (`STANDARD_HASH` over normalized columns); optional `checksumExpression` (for example `MAX(ORA_ROWSCN)`) overrides the default hash. Some Oracle types are excluded from the default hash — see checksum type coverage below. |
| `watermark` | Track a monotonic column; sync only rows newer than the last observed value | Fact tables, event logs with a reliable `UPDATED_AT` / ID column |

> **Re-running without incremental sync:** With `strategy: none` (or no `synchronization` block), every migration run extracts and loads **all** matching rows again. Re-running the same workflow against a target that already holds data from a prior run **appends duplicate rows** (or loads more data than expected). Use `watermark` or `checksum` for repeatable incremental runs. Do **not** `TRUNCATE` or bulk-`DELETE` the target without explicit user confirmation — the table may legitimately contain pre-existing or expected rows.

> **Checksum type coverage:** Built-in partition checksums **skip or normalize** some types (SQL Server `text`/`ntext`/`image`; Oracle LOBs/`LONG`/`XMLTYPE`/`VECTOR`; float rounding; spatial WKT; Redshift `HLLSKETCH`). Changes only in those columns may **not** change the checksum — no re-extract on the next run. Custom `checksumExpression` (for example `MAX(ORA_ROWSCN)`) only reflects what that expression measures. See [Advanced operations reference](../../../../data-infrastructure/references/advanced-operations-reference.md#checksum--incremental-sync--types-that-may-not-trigger-re-sync).

```yaml
synchronization:
  strategy: none

synchronization:
  strategy: checksum
  checksumExpression: MAX(ORA_ROWSCN)

synchronization:
  strategy: watermark
  watermarkColumn: UPDATED_AT

synchronization:
  strategy: watermark
  watermarkColumn: UPDATED_AT
  trackModifications: true
  trackDeletions: true
  primaryKeyColumns:
    - CUSTOMER_ID
```

## LoadSegmentation

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `targetSegmentSizeMb` | Integer | Yes | Maximum staged-file group size (MB) per `COPY INTO` statement |

## Loading

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `strategy` | `"warehouse"` \| `"snowpipe"` | No | `warehouse` uses `COPY INTO` (default). `snowpipe` uses Snowpipe auto-ingest. |

## Query modifiers

Reduce locking on busy source tables during extraction. Can be set at the connection layer (worker TOML), workflow default (`defaultTableConfiguration.queryModifiers`), or per table (`tables[].queryModifiers`). Modifiers apply to source queries only — Snowflake target queries never receive them.

| Property | Type | Description |
|----------|------|-------------|
| `objectModifier` | String | Hint applied after the source table in `FROM` (for example ` WITH (NOLOCK)` on SQL Server) |
| `selectModifier` | String | String rendered immediately after `SELECT` in every source query for that table or connection (for example `"/*+ INDEX(t idx_orders_created_at) */"`). Use `"NONE"` to disable (see below). |

```yaml
queryModifiers:
  objectModifier: " WITH (NOLOCK)"
  selectModifier: " /*+ FIRST_ROWS(100) */"
```

### selectModifier

#### Configured value

`selectModifier` is a string literal that DMVF renders immediately after `SELECT` in every source query for that table or connection. The resolver ensures a leading space separator between `SELECT` and the modifier; you do not need to include one in the configured value.

```yaml
# Per-table: apply an Oracle index hint on every extraction SELECT for this table.
# Rendered: SELECT /*+ INDEX(t idx_orders_created_at) */ "COL1", ... FROM "HR"."ORDERS" t ...
tables:
  - source:
      databaseName: ORCL
      schemaName: HR
      tableName: ORDERS
    queryModifiers:
      selectModifier: " /*+ INDEX(t idx_orders_created_at) */"
```

On the DM base-path (extraction, partition-boundary, checksum, watermark probes), DMVF aliases the source table as `t`. Hints referencing the alias should use `t` on this path. Some DV Jinja templates use other aliases (`src`, `rw`) — check the template context if configuring a hint that references the alias.

#### Oracle auto-hint

When all three conditions hold, DMVF auto-generates `/*+ PARALLEL(t, N) */` after `SELECT`:

1. The source platform is Oracle.
2. `selectModifier` is not configured at any layer (connection, workflow default, or per-table).
3. The estimated row count yields a computed parallel degree greater than 2.

The degree formula:

```text
N = min(2 ^ max(floor(log10(row_count + 1)) - 6, 0), 16)
```

The hint fires only when the computed degree exceeds 2. In practice this means tables of ~100 million rows or more; smaller tables produce degree 1 or 2, which the resolver treats as "no auto-hint" and renders a plain `SELECT`. When the row-count estimate is unavailable (None) the hint also does not fire.

```yaml
# Oracle source, selectModifier omitted, estimated rows = 120M → degree 4
# Rendered: SELECT /*+ PARALLEL(t, 4) */ "COL1", ... FROM "HR"."ORDERS" t
tables:
  - source:
      databaseName: ORCL
      schemaName: HR
      tableName: ORDERS
    # queryModifiers omitted → Oracle auto-hint fires if row count is large enough
```

Auto-hint fires on every DM source-SELECT path: extraction, DV checksum probes, DV watermark probes, and partition-boundary queries. It does not fire on Snowflake-target queries.

#### `"NONE"` opt-out sentinel

Setting `selectModifier: "NONE"` (exact, case-sensitive, upper-case) disables both the configured modifier and the Oracle auto-hint for that table or connection. The rendered `SELECT` has no modifier token.

The sentinel is case-sensitive. `"none"` and `"None"` are **not** opt-outs — they become literal `selectModifier` values rendered into the SQL as-is.

```yaml
# Disable Oracle auto-hint on one table while leaving other tables unrestricted.
tables:
  - source:
      databaseName: ORCL
      schemaName: HR
      tableName: NO_PARALLEL_TABLE
    queryModifiers:
      selectModifier: "NONE"
      # Rendered: SELECT "COL1", ... FROM "HR"."NO_PARALLEL_TABLE" t
```

#### Precedence

The most-specific non-null value wins across the three config layers:

| Layer | Most specific? | Set in |
|-------|----------------|--------|
| `tables[].queryModifiers.selectModifier` | Highest | Workflow YAML per-table |
| `defaultTableConfiguration.queryModifiers.selectModifier` | Middle | Workflow YAML default |
| Connection `query_modifiers.selectModifier` | Lowest | Worker TOML (see [`worker-config-reference.md`](../../../../data-infrastructure/references/worker-config-reference.md)) |

An explicit `null` at a higher-specificity layer falls through to the next layer — it does **not** clear an upstream value. To override a connection-layer or workflow-default `selectModifier` for a specific table, set the per-table `selectModifier` to the desired value (or to `"NONE"` to opt out entirely). Setting it to `null` leaves the upstream value in effect.

```yaml
# Connection layer (worker TOML): selectModifier = " /*+ INDEX(t idx_orders_created_at) */"
# Workflow default: unset (null) → falls through to connection
# Per-table override on ORDERS: "NONE" → opt out for this table only
defaultTableConfiguration:
  queryModifiers:
    selectModifier: null          # falls through; connection-layer value applies to most tables

tables:
  - source:
      databaseName: ORCL
      schemaName: HR
      tableName: ORDERS
    queryModifiers:
      selectModifier: "NONE"      # opts out; plain SELECT for this table
  - source:
      databaseName: ORCL
      schemaName: HR
      tableName: EMPLOYEES
    # queryModifiers omitted → connection-layer hint applies
```

See also: `dmvf/docs/data-migration-orchestrator/features/QueryModifiersAntiLockingSpec.md` §8 for the DMVA parity degree formula.

## Partition sizing and key selection

- **Auto mode:** omit both `targetPartitionSizeMb` and `targetPartitionSizeRows`. The orchestrator picks platform-appropriate defaults.
- **Explicit sizing:** set exactly one of `targetPartitionSizeMb` or `targetPartitionSizeRows`.
- **`columnNamesToPartitionBy`:** required by the CLI validator. Use a monotonic integer/timestamp column for large tables, or `[]` only for very small tables (single full-table partition). When omitted from user input, scai may infer keys from registry metadata — review `partition_key_findings` from setup.
- **`executionTimeoutMinutes`:** optional wall-clock limit for **Analyze boundaries** only (default 20). Raise it when NTILE/boundary analysis on large tables exceeds 20 minutes; prefer a cheaper partition key when possible.
- **Deprecated:** do not use legacy `partitionSize: auto` — use the flat `targetPartitionSizeMb` / `targetPartitionSizeRows` fields instead.

## ColumnTypeMapping

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `sourceType` | String | Yes | Type name in the source system |
| `targetType` | String | Yes | Target type name in Snowflake |

## ColumnNameMapping

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `sourceName` | String | Yes | Column name in source |
| `targetName` | String | Yes | Column name in Snowflake |

---

## Iceberg Workflow Examples

### Example: Catalog Link (Zero-Copy, Read-Only)

```yaml
defaultTableConfiguration:
  columnNamesToPartitionBy:
    - "1"    # Required by CLI validator, not used for Iceberg loading
  source:
    schemaName: iceberg_tpch
    databaseName: ecommerce_db
  target:
    schemaName: public
    databaseName: TARGET_DB
    tableType: iceberg
    icebergConfig:
      catalog: my_glue_catalog_integration
      externalVolume: my_iceberg_ext_vol

tables:
  - source:
      tableName: region
    target:
      tableName: region
      icebergConfig:
        catalogTableName: region    # Bare name — namespace prepended from CATALOG_NAMESPACE
  - source:
      tableName: nation
    target:
      tableName: nation
      icebergConfig:
        catalogTableName: nation    # Bare name — namespace prepended from CATALOG_NAMESPACE
```

Generated DDL (per table):

```sql
CREATE OR REPLACE ICEBERG TABLE TARGET_DB.PUBLIC.region
  CATALOG = 'my_glue_catalog_integration'
  CATALOG_TABLE_NAME = 'iceberg_tpch.region'
  EXTERNAL_VOLUME = 'my_iceberg_ext_vol'
```

### Example: Convert to Managed (Zero-Copy, Full DML)

```yaml
defaultTableConfiguration:
  columnNamesToPartitionBy:
    - "1"    # Required by CLI validator, not used for Iceberg loading
  source:
    schemaName: iceberg_tpch
    databaseName: ecommerce_db
  target:
    schemaName: public
    databaseName: TARGET_DB
    tableType: iceberg
    icebergConfig:
      catalog: my_glue_catalog_integration
      externalVolume: my_iceberg_ext_vol

tables:
  - source:
      tableName: orders
    target:
      tableName: orders
      icebergConfig:
        catalogTableName: orders    # Bare name — namespace prepended automatically
        migrationStrategy: convert_to_managed
```

Generated DDL:

```sql
-- Step 1: Create catalog-linked table
CREATE OR REPLACE ICEBERG TABLE TARGET_DB.PUBLIC.orders
  CATALOG = 'my_glue_catalog_integration'
  CATALOG_TABLE_NAME = 'iceberg_tpch.orders'
  EXTERNAL_VOLUME = 'my_iceberg_ext_vol'

-- Step 2: Convert to Snowflake-managed
ALTER ICEBERG TABLE TARGET_DB.PUBLIC.orders CONVERT TO MANAGED
```

> You **must** set `migrationStrategy: convert_to_managed` explicitly — auto-detection defaults to `catalog_link` for external catalogs.

### Example: Copy Files (Server-Side Binary Copy)

```yaml
defaultTableConfiguration:
  columnNamesToPartitionBy:
    - "1"    # Required by CLI validator, not used for Iceberg loading
  source:
    schemaName: public
    databaseName: analytics_db
  target:
    schemaName: public
    databaseName: TARGET_DB
    tableType: iceberg
    icebergConfig:
      catalog: SNOWFLAKE
      externalVolume: my_iceberg_ext_vol
      baseLocationPrefix: migrations/redshift
      sourceDataStage: "@TARGET_DB.PUBLIC.ICEBERG_SOURCE_STAGE"
  extraction:
    strategy: unload
    externalStage: TARGET_DB.PUBLIC.S3_EXTERNAL_STAGE
  targetPartitionSizeMb: 512

tables:
  - source:
      tableName: customers
    target:
      tableName: customers
```

Generated DDL and DML:

```sql
-- Step 1: Infer schema from Parquet files
SELECT * FROM TABLE(
  INFER_SCHEMA(
    LOCATION => '@TARGET_DB.PUBLIC.ICEBERG_SOURCE_STAGE',
    FILE_FORMAT => 'PARQUET'
  )
);

-- Step 2: Create the Iceberg table
CREATE ICEBERG TABLE TARGET_DB.PUBLIC.customers (col1 NUMBER(38,0), col2 VARCHAR, ...)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_iceberg_ext_vol'
  BASE_LOCATION = 'migrations/redshift/TARGET_DB/PUBLIC/customers'

-- Step 3: Binary copy of Parquet files
COPY INTO TARGET_DB.PUBLIC.customers
  FROM '@TARGET_DB.PUBLIC.ICEBERG_SOURCE_STAGE'
  LOAD_MODE = ADD_FILES_COPY
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
  PATTERN = '.*\.parquet'
```

### Example: Mixed Strategies (Native + Iceberg in One Workflow)

```yaml
defaultTableConfiguration:
  columnNamesToPartitionBy:
    - "1"    # Required by CLI validator
  source:
    schemaName: public
    databaseName: analytics_db
  target:
    schemaName: public
    databaseName: TARGET_DB
    tableType: iceberg
    icebergConfig:
      catalog: SNOWFLAKE
      externalVolume: my_iceberg_ext_vol
      baseLocationPrefix: migrations/redshift
      sourceDataStage: "@TARGET_DB.PUBLIC.ICEBERG_SOURCE_STAGE"
  targetPartitionSizeMb: 512

tables:
  # copy_files — inherits default icebergConfig (catalog=SNOWFLAKE)
  - source:
      tableName: customers
    target:
      tableName: customers

  # catalog_link — overrides to external catalog
  - source:
      tableName: events
    target:
      tableName: events
      tableType: iceberg
      icebergConfig:
        catalog: my_glue_catalog_integration
        externalVolume: my_iceberg_ext_vol
        catalogTableName: events    # Bare name — namespace prepended from CATALOG_NAMESPACE

  # convert_to_managed — explicit strategy override
  - source:
      tableName: orders
    target:
      tableName: orders
      tableType: iceberg
      icebergConfig:
        catalog: my_glue_catalog_integration
        externalVolume: my_iceberg_ext_vol
        catalogTableName: orders    # Bare name — namespace prepended automatically
        migrationStrategy: convert_to_managed
```

---

## Iceberg Data Type Mapping Reference

### Redshift Native → Snowflake Iceberg

| Redshift Native Type | Parquet Type (UNLOAD) | Snowflake Iceberg Type |
|---|---|---|
| `SMALLINT` | `INT32` | `INT` |
| `INTEGER` | `INT32` | `INT` |
| `BIGINT` | `INT64` | `LONG` |
| `DECIMAL(p,s)` | `FIXED_LEN_BYTE_ARRAY` | `DECIMAL(p,s)` |
| `REAL` | `FLOAT` | `FLOAT` |
| `DOUBLE PRECISION` | `DOUBLE` | `DOUBLE` |
| `BOOLEAN` | `BOOLEAN` | `BOOLEAN` |
| `CHAR(n)` | `BYTE_ARRAY (UTF8)` | `STRING` |
| `VARCHAR(n)` | `BYTE_ARRAY (UTF8)` | `STRING` |
| `DATE` | `INT32 (DATE)` | `DATE` |
| `TIMESTAMP` | `INT96` or `INT64` | `TIMESTAMP_NTZ` |
| `TIMESTAMPTZ` | `INT96` or `INT64` | `TIMESTAMP_LTZ` |
| `TIME` | N/A (cast to VARCHAR) | `STRING` |
| `VARBYTE` | N/A (cast via TO_HEX) | `STRING` |
| `GEOMETRY` | N/A (cast via ST_AsText) | `STRING` |
| `SUPER` | `BYTE_ARRAY (UTF8)` | `STRING` |

### Redshift Iceberg (Glue) → Snowflake Iceberg

| Glue/Iceberg Type | Snowflake Iceberg Type | Notes |
|---|---|---|
| `boolean` | `BOOLEAN` | |
| `int` | `NUMBER(10,0)` | 32-bit integer |
| `bigint` / `long` | `NUMBER(19,0)` | 64-bit integer |
| `float` | `FLOAT` | |
| `double` | `DOUBLE` | |
| `decimal(p,s)` | `DECIMAL(p,s)` | |
| `string` | `VARCHAR` | |
| `binary` | `BINARY` | |
| `date` | `DATE` | |
| `timestamp` | `TIMESTAMP_NTZ` | |
| `timestamptz` | `TIMESTAMP_LTZ` | |
| `list<T>` | Not supported | Flatten or convert to `VARCHAR` (JSON) |
| `map<K,V>` | Not supported | Convert to `VARCHAR` (JSON) |
| `struct<...>` | Not supported | Convert to `VARCHAR` (JSON) |

### Supported Iceberg Column Types

| Type | Notes |
|---|---|
| `BOOLEAN` | |
| `INT` | 32-bit integer |
| `LONG` | 64-bit integer |
| `FLOAT` | Single precision |
| `DOUBLE` | Double precision |
| `DECIMAL(p,s)` | Exact numeric |
| `DATE` | Date only |
| `TIME` | Time only |
| `TIMESTAMP_NTZ` | Timestamp without timezone |
| `TIMESTAMP_LTZ` | Timestamp with timezone |
| `STRING` / `VARCHAR` | Variable-length text |
| `BINARY` | Variable-length binary |
| `FIXED(n)` | Fixed-length binary |

### Unsupported Types in Iceberg Tables

The following Snowflake types are **not supported** in Iceberg tables and must be mapped to `STRING`/`VARCHAR` using `columnTypeMappings`:

- `VARIANT`
- `OBJECT`
- `ARRAY`
- `GEOGRAPHY`
- `GEOMETRY`

```yaml
columnTypeMappings:
  - sourceType: SUPER
    targetType: VARCHAR
  - sourceType: GEOMETRY
    targetType: VARCHAR
  - sourceType: VARIANT
    targetType: VARCHAR
```
