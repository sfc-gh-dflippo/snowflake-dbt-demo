# Informatica Mapping and Transformation Guide

Reference for navigating Informatica PowerCenter XML exports to extract mapping and transformation information used during dbt test generation.

## XML Structure

Mappings define data transformation pipelines within a `FOLDER`:

```
FOLDER
└── MAPPING (NAME="m_CustomerLoad")
    ├── TRANSFORMATION (reusable transformation definitions)
    │   └── TRANSFORMFIELD (port definitions with expressions)
    │   └── TABLEATTRIBUTE (transformation properties)
    ├── INSTANCE (runtime references to transformations)
    ├── CONNECTOR (port-to-port data wiring)
    └── TARGETLOADORDER (target write sequence)
```

## Finding Mappings

Mappings are `MAPPING` elements with `NAME` and `ISVALID` attributes:

```xml
<MAPPING NAME="m_CustomerLoad" ISVALID="YES" ...>
  <!-- TRANSFORMATIONs, INSTANCEs, CONNECTORs -->
</MAPPING>
```

Each mapping corresponds to one dbt project (or sub-project) in the converted output.

## Inside a Mapping

### TRANSFORMATION Elements

Define the logic. Each transformation has a `TYPE` attribute, `TRANSFORMFIELD` port definitions, and `TABLEATTRIBUTE` properties.

```xml
<TRANSFORMATION NAME="EXP_CalcTotal" TYPE="Expression" ...>
  <TRANSFORMFIELD NAME="total_amount" DATATYPE="decimal"
    PORTTYPE="OUTPUT" EXPRESSION="unit_price * quantity"
    EXPRESSIONTYPE="GENERAL" PRECISION="18" SCALE="2"/>
  <TRANSFORMFIELD NAME="unit_price" DATATYPE="decimal"
    PORTTYPE="INPUT" PRECISION="18" SCALE="2"/>
  <TRANSFORMFIELD NAME="quantity" DATATYPE="integer"
    PORTTYPE="INPUT" PRECISION="10" SCALE="0"/>
  <TABLEATTRIBUTE NAME="Tracing Level" VALUE="Normal"/>
</TRANSFORMATION>
```

### INSTANCE Elements

Runtime references to transformations, linking a transformation definition to the mapping's DAG:

```xml
<INSTANCE NAME="EXP_CalcTotal" TRANSFORMATION_NAME="EXP_CalcTotal"
  TRANSFORMATION_TYPE="Expression" TYPE="TRANSFORMATION"/>
<INSTANCE NAME="SQ_Customers" TRANSFORMATION_NAME="SQ_Customers"
  TRANSFORMATION_TYPE="Source Qualifier" TYPE="TRANSFORMATION"/>
```

### CONNECTOR Elements

Wire ports between instances — these define the data flow path:

```xml
<CONNECTOR FROMINSTANCE="SQ_Customers" FROMFIELD="customer_id"
  TOINSTANCE="EXP_CalcTotal" TOFIELD="customer_id"/>
```

### TARGETLOADORDER

Specifies which target is loaded in what order:

```xml
<TARGETLOADORDER TARGETINSTANCE="TargetTable" ORDER="1"/>
```

## Common Transformation Types

| TYPE Value | Category | Description | dbt Layer | Snowflake Equivalent |
|------------|----------|-------------|-----------|---------------------|
| `Source Qualifier` | Source | Reads from source tables; optional SQL override | Staging (`stg_raw__*`) | `SELECT ... FROM {{ source() }}` |
| `Expression` | Transform | Row-level calculations via expressions | Intermediate (`int_*`) | `SELECT expr AS col` in CTE |
| `Filter` | Transform | Row-level filtering via boolean condition | Intermediate (`int_*`) | `WHERE condition` |
| `Router` | Transform | Conditional routing to multiple output groups | Intermediate (`int_*`) | Multiple models with `WHERE` per group |
| `Lookup Procedure` | Transform | Reference table join (connected/unconnected); cache mode affects translation — see Lookup details below | Intermediate (`int_*`) | `LEFT OUTER JOIN`, `MERGE`, or scalar subquery |
| `Joiner` | Transform | Two-pipeline join with configurable join type | Intermediate (`int_*`) | `INNER JOIN` / `LEFT OUTER JOIN` etc. |
| `Aggregator` | Transform | GROUP BY with aggregate functions | Intermediate (`int_*`) | `GROUP BY` + aggregate functions, or window functions + `QUALIFY` (see Aggregator details below) |
| `Sorter` | Transform | Row ordering | Passthrough | Ordering absorbed into downstream operations |
| `Union` | Transform | Merge multiple pipelines | Intermediate (`int_*`) | `UNION ALL` |
| `Normalizer` | Transform | Pivot rows to columns | Intermediate (`int_*`) | `UNPIVOT` |
| `Sequence` | Transform | Generate sequential integers | Intermediate (`int_*`) | `ROW_NUMBER() OVER (ORDER BY 1)` |
| `Stored Procedure` | Transform | Call database procedure | Intermediate (`int_*`) or `DbtFolderHook` | Inline UDF call (connected) or `CALL` in pre/post-hook (disconnected) |
| `Update Strategy` | Transform | Flag rows for INSERT/UPDATE/DELETE/REJECT | Intermediate (`int_*`) | `etl_dml_operation__` control column or inlined WHERE |
| `Target Definition` | Target | Write to target table | Mart | `{{ config(materialized='...') }}` |

## Extracting Column Information

Column definitions come from `TRANSFORMFIELD` elements:

| Attribute | Description |
|-----------|-------------|
| `NAME` | Column/port name |
| `DATATYPE` | Informatica data type (see mapping table below) |
| `PORTTYPE` | `INPUT`, `OUTPUT`, `INPUT/OUTPUT`, `RETURN/OUTPUT` |
| `PRECISION` | Total digits / string length |
| `SCALE` | Decimal places |
| `EXPRESSION` | Informatica expression (for Expression, Filter, Router, Aggregator, Update Strategy) |
| `EXPRESSIONTYPE` | `GENERAL` (computed) or `GROUPBY` (aggregation key) |
| `DEFAULTVALUE` | Default when NULL |

## Extracting Expressions

Expressions are in the `EXPRESSION` attribute of `TRANSFORMFIELD` elements:

- **Expression transformation**: Computed columns (`PORTTYPE="OUTPUT"`, `EXPRESSIONTYPE="GENERAL"`)
- **Filter transformation**: Single OUTPUT port with boolean `EXPRESSION` as the filter condition; also check `TABLEATTRIBUTE NAME="Filter Condition"`
- **Router transformation**: `TRANSFORMFIELD` per group with group condition in `EXPRESSION`; `DEFAULT1` group catches unmatched rows
- **Aggregator**: Aggregate expressions like `SUM(SALARY)`, `COUNT(*)` on OUTPUT ports; `EXPRESSIONTYPE="GROUPBY"` marks group keys
- **Update Strategy**: `TABLEATTRIBUTE NAME="Update Strategy Expression"` contains the DD_ expression (e.g., `DD_INSERT`, `IIF(...)`)

## Source Qualifier SQL Overrides

The Source Qualifier's SQL can be overridden at the **session level**, not in the `TRANSFORMATION` element. This is a common source of confusion when debugging converted dbt staging models.

When `ATTRIBUTE NAME="Sql Query"` exists inside a `SESSTRANSFORMATIONINST` for a Source Qualifier:

- **Takes precedence** over the table-based source definition in the `TRANSFORMATION` element
- The override SQL appears directly in the dbt staging model's `FROM` clause
- May contain complex `WHERE`, `JOIN`, or subquery logic **not visible** in the `TRANSFORMATION` element
- Always check the `SESSION` element, not just `TRANSFORMATION`, when tracing source SQL

```xml
<!-- Found in SESSION, NOT in MAPPING/TRANSFORMATION -->
<SESSION NAME="s_mapping_customers" ...>
  <SESSTRANSFORMATIONINST TRANSFORMATIONNAME="SQ_Customer"
    TRANSFORMATIONTYPE="Source Qualifier" ...>
    <ATTRIBUTE NAME="Sql Query"
      VALUE="SELECT c.*, o.last_order_date FROM customers c
             LEFT JOIN order_summary o ON c.id = o.customer_id
             WHERE c.active = 1"/>
  </SESSTRANSFORMATIONINST>
</SESSION>
```

If the dbt staging model has unexpected SQL that doesn't match the `TRANSFORMATION` definition, check for a session-level override.

## Session/Mapping Location Overrides

A session or mapping can repoint a source/target at a different database, schema, or table than the one in its `TRANSFORMATION`/`TARGET` definition. SnowConvert preserves this as a runtime-configurable **location-override layer** in the dbt project.

When present, SnowConvert emits four coordinated pieces:

| Piece | Where | Purpose |
|-------|-------|---------|
| `sc_override_<inst>_db` / `_schema` / `_table` vars | `dbt_project.yml` | Per-instance override values; ship with **placeholder defaults** (e.g. `YOUR_DB`) |
| `generate_database_name` / `generate_schema_name` macros | `macros/` | Apply the var value **verbatim** (dbt's default would emit `<target>_<custom>`) |
| Var-driven `sources.yml` | `models/` | Overridden source instances point at `{{ var('sc_override_..._schema') }}` etc. |
| `config(database=…, schema=…, alias=…)` header | mart `.sql` | Repoints the materialized target via the same vars |

**Signal:** the layer exists iff `dbt_project.yml` declares `sc_override_*` vars. Informatica-only today, but key off the var prefix, not the platform.

**Gotchas:**
- Don't resolve a database-/schema-not-found error on a mart by deleting its `config()` header or hardcoding the var defaults — the placeholders are intentional; the layer is meant to be repointed at runtime. Deleting it silently strips the feature.
- To build these marts in a test/dev environment, supply real values via `--vars` (e.g. `--vars '{"sc_override_dim_customer_db": "MY_DB"}'`), as with variable-controlled branching.

## Aggregator Translation Details

The Informatica Aggregator has two modes that map to different SQL patterns:

| Aggregator Mode | TABLEATTRIBUTE | SQL Translation |
|----------------|----------------|-----------------|
| Standard (`Sorted Input = NO`) | Default | `GROUP BY` with aggregate functions (`SUM`, `COUNT`, `MAX`, `MIN`, `AVG`) |
| Incremental (`Sorted Input = YES`) | `Sorted Input = YES` | Window functions with `QUALIFY ROW_NUMBER() = 1` for running/incremental aggregation |

**Standard mode** (most common): Straightforward `GROUP BY` with aggregate functions:
```sql
SELECT
   DEPARTMENT,
   SUM(SALARY) AS total_salary,
   COUNT(*) AS employee_count
FROM {{ ref('stg_raw__SQ_EMPLOYEE') }}
GROUP BY DEPARTMENT
```

**Incremental mode** with non-aggregate passthrough columns: Uses window functions + `QUALIFY` to select one row per group while computing aggregates:
```sql
WITH source_data AS (
   SELECT * FROM {{ ref('stg_raw__SQ_EMPLOYEE') }}
),
aggregation AS (
   SELECT
      LAST_VALUE(NAME) OVER (PARTITION BY DEPARTMENT ORDER BY NAME, SALARY) AS NAME,
      SUM(SALARY) OVER (PARTITION BY DEPARTMENT) AS total_salary,
      DEPARTMENT
   FROM source_data
   QUALIFY ROW_NUMBER() OVER (PARTITION BY DEPARTMENT ORDER BY NAME, SALARY) = 1
)
SELECT * FROM aggregation
```

The window function pattern is used when the Aggregator has **both** aggregate output ports (e.g., `SUM(SALARY)`) and non-aggregate passthrough ports (e.g., `NAME`) that need `LAST_VALUE` semantics.

## Lookup Cache Types

Informatica Lookup transformations have cache modes that fundamentally change the SQL translation:

| Cache Mode | TABLEATTRIBUTE | Behavior | SQL Translation |
|-----------|----------------|----------|-----------------|
| **Static** (default) | `Lookup Caching Enabled = YES`, `Lookup policy on multiple match = Use First Value` | Cache loaded once at session start; read-only during execution | `LEFT OUTER JOIN` on reference table with `QUALIFY ROW_NUMBER() = 1` for dedup |
| **Dynamic** | `Lookup Caching Enabled = YES`, `Dynamic Lookup Cache = YES` | Cache updated during session as new rows flow through (SCD Type 1 pattern) | `MERGE` with incremental update logic — the lookup target is both read and written |
| **Persistent** | `Lookup Caching Enabled = YES`, `Lookup Cache Persistent = YES` | Cache file reused across sessions (avoids reload) | No direct SQL equivalent — translate as static join; the performance optimization is N/A in Snowflake |
| **Uncached** | `Lookup Caching Enabled = NO` | Queries database per row (no cache) | `LEFT OUTER JOIN` (same as static — SQL is set-based) |
| **Unconnected** | No incoming CONNECTORs; called via `:LKP.LOOKUP(args)` | Returns a single value via expression | Scalar subquery inlined in the calling transformation |

**Dynamic Lookup** is the most complex — verify that the converted `MERGE` logic correctly handles the insert/update/unchanged row routing.

## Tracing Transformation Paths

Follow `CONNECTOR` elements to trace data lineage through the mapping:

1. Start from SOURCE `INSTANCE` elements
2. Follow `CONNECTOR` where `FROMINSTANCE` matches current instance
3. `TOINSTANCE` + `TOFIELD` identifies the downstream port
4. Continue until reaching a TARGET `INSTANCE`

Example data path:
```
Source (SQ_Customers)
  → CONNECTOR → Expression (EXP_CalcTotal)
    → CONNECTOR → Filter (FIL_Active)
      → CONNECTOR → Target (TargetTable)
```

Each transformation in the path maps to a dbt model that `{{ ref() }}`s its upstream.

## Informatica-to-dbt Layer Mapping

| Informatica Component | dbt Layer | Naming Convention | Materialization |
|----------------------|-----------|-------------------|-----------------|
| Source Qualifier | Staging | `stg_raw__<SQ_Name>` | `view` |
| Expression / Filter / Router / Lookup / Joiner / Aggregator / etc. | Intermediate | `int_<TransformName>` | `view` (default) or `table`/`ephemeral` |
| Target Definition | Mart | Named after target table | `table` or `incremental` |
| Stored Procedure (disconnected) | Folder Hook | N/A (in `dbt_project.yml`) | N/A |

## Informatica Data Types to Snowflake / Seed Values

| Informatica Type | Snowflake Type | Seed Value Example |
|-----------------|----------------|-------------------|
| `int` / `integer` | `NUMBER(10,0)` | `42` |
| `bigint` | `NUMBER(19,0)` | `9999999999` |
| `smallint` | `NUMBER(5,0)` | `100` |
| `decimal(p,s)` | `NUMBER(p,s)` | `123.45` |
| `double` | `FLOAT` | `3.14159` |
| `varchar(n)` / `nstring` | `VARCHAR(n)` | `'sample text'` |
| `date/time` | `TIMESTAMP_NTZ` | `'2024-01-15 10:30:00'` |
| `binary` | `BINARY` | `X'48454C4C4F'` |

## EWI Codes (Informatica-Specific)

Key EWI codes encountered in Informatica conversions:

| Code | Description |
|------|-------------|
| `SSC-EWI-INF0003` | Workflow element cannot be converted (Timer, unsupported task) |
| `SSC-EWI-INF0038` | Stored procedure uses named connection (not `$Source`/`$Target`) |
| `SSC-EWI-INF0039` | dbt folder hooks execute per-model, not per-session |
| `SSC-EWI-INF0040` | Connected SP translated assuming UDF conversion |
| `SSC-EWI-INF0041` | Port DEFAULTVALUE uses Informatica-specific ERROR() function |
| `SSC-FDM-INF0002` | Aggregator input column ordering is non-deterministic in SQL |
| `SSC-FDM-INF0015` | Update Strategy logic moved to target model |
| `SSC-FDM-INF0016` | Sequence Generator ordering is non-deterministic |
