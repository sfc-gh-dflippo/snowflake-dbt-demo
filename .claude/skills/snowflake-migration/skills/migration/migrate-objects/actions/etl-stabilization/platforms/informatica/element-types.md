# Informatica Element Type Reference

Quick reference for understanding what each Informatica element type does and how it maps to Snowflake. Read this when encountering an unfamiliar element type in the `---- Start` tags or assessment data.

## Workflow Tasks

These appear as `TASK` elements inside a `WORKFLOW` and control execution order.

| Element Type | Description | Snowflake Equivalent | Notes |
|-------------|-------------|---------------------|-------|
| **Session** | Executes a mapping (data transformation pipeline) | `CREATE TASK ... AS BEGIN EXECUTE DBT PROJECT ...; END` | Primary workflow unit — each session binds to one mapping |
| **Command** | Runs shell commands or OS scripts | `EXECUTE IMMEDIATE` / external | May be external dependency — verify if needed |
| **Email** | Sends email notification | `SYSTEM$SEND_EMAIL` / external | External dependency — typically skipped |
| **Timer** | Wait/delay between tasks | Not supported | EWI `SSC-EWI-INF0003` emitted |
| **Assignment** | Sets workflow variable value | Variable assignment in task SQL | |
| **Decision** | Conditional branching based on variable | Conditional task chaining | Evaluates condition to route execution |
| **Control (Stop/Abort)** | Stops or aborts workflow | Error handling / `SYSTEM$ABORT_SESSION` | |
| **Start** | Workflow entry point | Root task (no `AFTER` clause) | Every workflow has exactly one Start task |

## Workflow Containers (Worklets)

| Element Type | Description | Snowflake Equivalent | Notes |
|-------------|-------------|---------------------|-------|
| **Worklet** | Reusable sub-workflow containing tasks and links | Flattened task chain (tasks expanded into parent DAG) | Internal tasks are prefixed with `{workflow}_{worklet}_{task}`. See `workflow-guide.md` for expansion details. |

## Mapping Transformations

These appear as `TRANSFORMATION` elements inside a `MAPPING` and define data processing logic. Each typically maps to one dbt model.

### Source/Target

| Element Type | Description | dbt Layer | Snowflake Equivalent |
|-------------|-------------|-----------|---------------------|
| **Source Qualifier** | Reads from source tables with optional SQL override | Staging (`stg_raw__*`) | `SELECT ... FROM {{ source('raw', 'table') }}` |
| **Target Definition** | Writes to target table | Mart | `{{ config(materialized='table') }}` |

### Row-Level Transformations (Passive)

One output row per input row — do not change row count.

| Element Type | Description | dbt Layer | Snowflake Equivalent |
|-------------|-------------|-----------|---------------------|
| **Expression** | Calculated/derived columns via Informatica expression language | Intermediate (`int_*`) | `SELECT expr AS col` in CTE |
| **Lookup Procedure** (connected, static cache) | Reference table join for enrichment; cache loaded once at session start | Intermediate (`int_*`) | `LEFT OUTER JOIN` on reference table |
| **Lookup Procedure** (connected, dynamic cache) | Reference table join with cache updates during session (SCD Type 1) | Intermediate (`int_*`) | `MERGE` with incremental update logic |
| **Lookup Procedure** (unconnected) | Scalar value lookup via `:LKP.LOOKUP(args)` | N/A (inlined) | Scalar subquery |
| **Sequence** (Sequence Generator) | Generates sequential integer values (NEXTVAL/CURRVAL ports) | Intermediate (`int_*`) | `ROW_NUMBER() OVER (ORDER BY 1) + offset` |
| **Stored Procedure** (connected, Normal) | Calls DB procedure once per row | Intermediate (`int_*`) | Inline UDF call with VARIANT extraction |
| **Update Strategy** | Flags rows for INSERT/UPDATE/DELETE/REJECT | Intermediate (`int_*`) or ephemeral | `etl_dml_operation__` column or inlined WHERE |

### Row-Level Transformations (Active)

Can change row count (filter, route, or generate rows).

| Element Type | Description | dbt Layer | Snowflake Equivalent |
|-------------|-------------|-----------|---------------------|
| **Filter** | Drops rows not matching boolean condition | Intermediate (`int_*`) | `WHERE condition` |
| **Router** | Routes rows to multiple output groups by condition | Intermediate (`int_*`) | Multiple models with `WHERE` per group + `DEFAULT1` for unmatched |

### Set-Based Transformations

Operate on groups of rows.

| Element Type | Description | dbt Layer | Snowflake Equivalent |
|-------------|-------------|-----------|---------------------|
| **Aggregator** (Sorted Input = NO) | Standard GROUP BY with aggregate functions | Intermediate (`int_*`) | `GROUP BY` + `SUM`/`COUNT`/`MAX`/`MIN`/`AVG` |
| **Aggregator** (Sorted Input = YES) | Incremental aggregation with passthrough columns | Intermediate (`int_*`) | Window functions + `QUALIFY ROW_NUMBER() = 1` |
| **Joiner** | Joins two input pipelines | Intermediate (`int_*`) | `INNER JOIN` / `LEFT OUTER JOIN` / `RIGHT OUTER JOIN` / `FULL OUTER JOIN` |
| **Sorter** | Sorts rows by specified columns | Passthrough | No separate model — ordering absorbed downstream |
| **Union** | Merges multiple input pipelines | Intermediate (`int_*`) | `UNION ALL` |
| **Normalizer** (Pipeline) | Unpivots repeating column groups into rows | Intermediate (`int_*`) | `UNPIVOT` |
| **Normalizer** (VSAM) | Expands repeating groups within a single record into multiple rows | Intermediate (`int_*`) | `LATERAL FLATTEN` on nested/array data |
| **Rank** | Selects top/bottom N rows per group | Intermediate (`int_*`) | Window function with `QUALIFY` |

### Special Transformations

| Element Type | Description | dbt Layer | Snowflake Equivalent |
|-------------|-------------|-----------|---------------------|
| **Stored Procedure** (disconnected) | Pre/post-session database procedure call | N/A (folder hook) | `CALL proc()` in `dbt_project.yml` `+pre-hook`/`+post-hook` |
| **Java Transformation** | Custom Java code | N/A | Unsupported — EWI emitted |
| **XML** transformations | XML parsing/generation | N/A | Unsupported — EWI emitted |
| **Mapplet** | Reusable transformation group (expanded inline at conversion time — not invoked like a macro at runtime) | dbt Macro | Mapplet transformations are **inlined** into the parent mapping during conversion. The dbt Macro analogy is structural only — mapplets act like template instantiation, not function calls. |

## Passthrough vs Model-Generating

Not all transformations produce a dbt model:

| Behavior | Transformation Types | dbt Artifact |
|----------|---------------------|-------------|
| **Generates model** | Expression, Filter, Router, Aggregator, Joiner, Lookup (connected), Union, Normalizer, Sequence, Stored Procedure (connected), Update Strategy | `int_*.sql` or `stg_raw__*.sql` |
| **Passthrough** (no model) | Sorter, Lookup (unconnected — inlined as scalar), Source Qualifier passthrough | No separate `.sql` file |
| **Folder hook** (not a model) | Stored Procedure (disconnected) | Entry in `dbt_project.yml` |
| **Unsupported** | Java Transformation, XML, Custom | EWI emitted — no output |

## Key Differences from SSIS

| Concept | SSIS | Informatica |
|---------|------|-------------|
| Source definition | OLE DB Source component | Source Qualifier transformation |
| Expression language | SSIS expression syntax | Informatica expression language (IIF, DECODE, etc.) |
| Conditional routing | Conditional Split | Router (with named groups + DEFAULT1) |
| Merge join | Merge Join component | Joiner transformation |
| Data type metadata | In component XML | `TRANSFORMFIELD` attributes (DATATYPE, PRECISION, SCALE) |
| Disabled detection | `Disabled="True"` on executable | `ENABLED="NO"` on transformation or `ISENABLED="NO"` on workflow/task |
| Package variables | `DTS:Variable` | `MAPPINGVARIABLE` with `$$` prefix |
| Pipeline/container model | Control Flow + Data Flow | Workflow + Mapping (separate concerns) |
| Reusable sub-workflow | Sequence Container (inline only) | Worklet (reusable, flattened into parent DAG at conversion) |
| Reusable transformation group | N/A | Mapplet (expanded inline during conversion) |
| Lookup cache | N/A (always full cache) | Static, Dynamic, or Persistent cache modes |
