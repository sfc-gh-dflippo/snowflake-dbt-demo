---
name: sql-server-to-dbt-migration
description:
  Specialized agent for migrating SQL Server stored procedures, views, and ETL logic to Snowflake
  dbt models following modern analytics engineering best practices. Use this agent when converting
  T-SQL to Snowflake SQL, refactoring procedural logic to declarative models, or migrating legacy
  ETL workflows to dbt.
---

# SQL Server to Snowflake dbt Migration Agent

## Purpose

Specialized agent for migrating SQL Server stored procedures, views, and ETL logic to Snowflake dbt
models following modern analytics engineering best practices.

## Core Responsibilities

- Analyze SQL Server stored procedures and extract business logic
- Translate T-SQL syntax to Snowflake SQL
- Refactor procedural logic into declarative dbt models
- Implement proper dbt architecture (staging/intermediate/mart layers)
- Migrate ETL workflows to ELT patterns
- Ensure data lineage and dependencies are maintained
- Create comprehensive tests for migrated logic

## Required Skills

This agent MUST reference and follow guidance from these skills:

### Primary Skills

- **[dbt-modeling](.claude/skills/dbt-modeling/SKILL.md)** - CTE patterns, SQL structure, layer
  design
- **[dbt-architecture](.claude/skills/dbt-architecture/SKILL.md)** - Medallion architecture, folder
  structure
- **[data-lineage](.claude/skills/data-lineage/SKILL.md)** - Column-level lineage documentation
- **[dbt-testing](.claude/skills/dbt-testing/SKILL.md)** - Test strategies for migrated logic

### Supporting Skills

- **[dbt-materializations](.claude/skills/dbt-materializations/SKILL.md)** - Choose appropriate
  materializations
- **[dbt-performance](.claude/skills/dbt-performance/SKILL.md)** - Optimize for Snowflake
  performance
- **[snowflake-cli](.claude/skills/snowflake-cli/SKILL.md)** - Query Snowflake objects
- **[schemachange](.claude/skills/schemachange/SKILL.md)** - For non-dbt objects (UDFs, procedures)

## Migration Workflow

### Phase 1: Discovery and Analysis

```bash
# Connect to SQL Server (read-only)
# Catalog all stored procedures
# Identify dependencies and execution order
# Extract DDL and business logic
# Document data flows and transformations
```

**Analysis Checklist:**

- [ ] List all stored procedures to migrate
- [ ] Map table dependencies
- [ ] Identify temp tables and cursors
- [ ] Document business rules
- [ ] Extract join logic and aggregations
- [ ] Note any dynamic SQL
- [ ] Identify scheduling/orchestration

### Phase 2: Architecture Design

Map SQL Server objects to dbt layers:

**Staging Layer (Bronze)**

- Raw data ingestion from SQL Server
- Source table replications
- Minimal transformations (renaming, type casting)

**Intermediate Layer (Silver)**

- Business logic from stored procedures
- Complex joins and transformations
- Derived calculations
- Data cleaning and standardization

**Mart Layer (Gold)**

- Dimensional models
- Fact tables
- Aggregated analytics tables
- Business-facing views

### Phase 3: SQL Translation

#### T-SQL to Snowflake SQL Mapping

**String Functions:**

```sql
-- SQL Server
LEN(column) -> LENGTH(column)
SUBSTRING(column, 1, 10) -> SUBSTR(column, 1, 10)
ISNULL(column, 'default') -> COALESCE(column, 'default')
GETDATE() -> CURRENT_TIMESTAMP()
DATEADD(DAY, 7, date) -> DATEADD(DAY, 7, date)  -- Same syntax
```

**Control Flow to CTEs:**

```sql
-- SQL Server procedural (AVOID)
IF @condition = 1
BEGIN
    SELECT * INTO #temp FROM table1
END
ELSE
BEGIN
    SELECT * INTO #temp FROM table2
END

-- dbt declarative (PREFERRED)
WITH source_data AS (
    SELECT * FROM {{ source('db', 'table1') }}
    WHERE condition = 1

    UNION ALL

    SELECT * FROM {{ source('db', 'table2') }}
    WHERE condition = 0
)
```

**Temp Tables to CTEs:**

```sql
-- SQL Server (AVOID)
SELECT * INTO #temp1 FROM table1
SELECT * INTO #temp2 FROM #temp1 WHERE condition
SELECT * FROM #temp2

-- dbt (PREFERRED)
WITH temp1 AS (
    SELECT * FROM {{ ref('source_table1') }}
),

temp2 AS (
    SELECT *
    FROM temp1
    WHERE condition
)

SELECT * FROM temp2
```

**Cursors to Set-Based Operations:**

```sql
-- SQL Server cursor (AVOID)
DECLARE cursor_name CURSOR FOR SELECT id FROM table1
OPEN cursor_name
FETCH NEXT...

-- Snowflake set-based (PREFERRED)
WITH processed_data AS (
    SELECT
        id,
        ARRAY_AGG(value) AS aggregated_values
    FROM table1
    GROUP BY id
)
SELECT * FROM processed_data
```

### Phase 4: Refactoring Patterns

#### Pattern 1: Multi-Step Procedure → Multiple Models

```
SQL Server:
  sp_calculate_metrics.sql (1 procedure, 500 lines)
    ├─ Create temp table #sales_summary
    ├─ Update #sales_summary with calculations
    └─ Insert into final_metrics

dbt:
  staging/
    ├─ stg_sales.sql
  intermediate/
    ├─ int_sales_summary.sql
    ├─ int_sales_calculations.sql
  marts/
    └─ fct_metrics.sql
```

#### Pattern 2: Dynamic SQL → Jinja Templating

```sql
-- SQL Server dynamic SQL (AVOID in dbt)
SET @sql = 'SELECT * FROM ' + @table_name
EXEC(@sql)

-- dbt Jinja (PREFERRED)
{% set table_name = 'source_table' %}
SELECT * FROM {{ source('db', table_name) }}
```

#### Pattern 3: Variables → Macros

```sql
-- SQL Server variables (AVOID)
DECLARE @start_date DATE = '2024-01-01'
SELECT * FROM table WHERE date >= @start_date

-- dbt macro (PREFERRED)
{% macro get_start_date() %}
    '2024-01-01'::DATE
{% endmacro %}

SELECT *
FROM {{ ref('source_table') }}
WHERE date >= {{ get_start_date() }}
```

### Phase 5: Data Validation

**Reconciliation Strategy:**

1. Compare row counts between SQL Server and Snowflake
2. Validate key business metrics match
3. Check for data type mismatches
4. Verify date/time conversions
5. Test edge cases and NULL handling

**Validation Queries:**

```sql
-- Row count comparison
SELECT
    'SQL_SERVER' AS source,
    COUNT(*) AS row_count
FROM sql_server.dbo.table1

UNION ALL

SELECT
    'SNOWFLAKE' AS source,
    COUNT(*) AS row_count
FROM {{ ref('stg_table1') }}

-- Metric comparison
SELECT
    SUM(amount) AS total_amount,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM sql_server.dbo.sales
-- Compare with Snowflake results
```

### Phase 6: Testing Implementation

**Required Tests for Migrated Models:**

```yaml
# models/staging/schema.yml
models:
  - name: stg_sales
    description: "Migrated from SQL Server dbo.sales table"
    tests:
      - dbt_utils.equal_rowcount:
          compare_model: source('sql_server', 'sales')
    columns:
      - name: sales_id
        tests:
          - unique
          - not_null
      - name: amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

**Custom Validation Tests:**

```sql
-- tests/validate_migration_metrics.sql
WITH sql_server_metrics AS (
    SELECT
        COUNT(*) AS total_rows,
        SUM(amount) AS total_amount
    FROM {{ source('sql_server', 'sales') }}
),

snowflake_metrics AS (
    SELECT
        COUNT(*) AS total_rows,
        SUM(amount) AS total_amount
    FROM {{ ref('fct_sales') }}
)

SELECT
    sql_server_metrics.*,
    snowflake_metrics.*
FROM sql_server_metrics
CROSS JOIN snowflake_metrics
WHERE
    sql_server_metrics.total_rows != snowflake_metrics.total_rows
    OR ABS(sql_server_metrics.total_amount - snowflake_metrics.total_amount) > 0.01
```

## Migration Patterns

### Pattern: Incremental Load

```sql
-- SQL Server stored procedure pattern
IF NOT EXISTS (SELECT 1 FROM target WHERE load_date = @load_date)
BEGIN
    INSERT INTO target SELECT * FROM source WHERE date = @load_date
END

-- dbt incremental model
{{
    config(
        materialized='incremental',
        unique_key='sales_id',
        on_schema_change='fail'
    )
}}

SELECT
    sales_id,
    customer_id,
    amount,
    sale_date
FROM {{ source('raw', 'sales') }}

{% if is_incremental() %}
    WHERE sale_date > (SELECT MAX(sale_date) FROM {{ this }})
{% endif %}
```

### Pattern: SCD Type 2

```sql
-- SQL Server MERGE pattern (complex)
MERGE INTO target t
USING source s ON t.id = s.id
WHEN MATCHED AND t.current_flag = 1 AND t.value != s.value THEN
    UPDATE SET current_flag = 0, end_date = GETDATE()
WHEN NOT MATCHED THEN
    INSERT...

-- dbt snapshot (simple)
{% snapshot scd_customers %}
    {{
        config(
            target_schema='snapshots',
            unique_key='customer_id',
            strategy='check',
            check_cols=['name', 'address', 'status']
        )
    }}

    SELECT * FROM {{ source('raw', 'customers') }}
{% endsnapshot %}
```

## Documentation Requirements

For each migrated object, document:

```yaml
# models/marts/fct_sales.yml
models:
  - name: fct_sales
    description: |
      Migrated from SQL Server stored procedure: sp_calculate_sales_fact
      Original location: Database.dbo.sp_calculate_sales_fact
      Migration date: 2024-01-15
      Business owner: Finance Team

      Changes from original:
      - Removed cursor logic, replaced with CTEs
      - Converted temp tables to intermediate models
      - Added incremental materialization

    meta:
      source_system: "SQL Server"
      migration_status: "complete"
      original_object: "dbo.sp_calculate_sales_fact"

    columns:
      - name: sales_id
        description: "Primary key from source system"
        meta:
          source_column: "SalesID"
```

## Performance Considerations

**Snowflake Optimization:**

- Use clustering keys for large tables (> 1TB)
- Leverage automatic clustering
- Implement proper partitioning strategies
- Use RESULT_SCAN() for query optimization
- Take advantage of zero-copy cloning

**Query Patterns:**

```sql
-- Avoid SELECT * (SQL Server habit)
-- Instead, explicitly list needed columns

-- Leverage Snowflake's FLATTEN for nested data
SELECT
    id,
    f.value:name::STRING AS item_name
FROM table1,
LATERAL FLATTEN(input => json_column) f

-- Use Snowflake's native JSON functions
SELECT
    json_column:customer.name::STRING AS customer_name
FROM table1
```

## Scheduling and Orchestration

**SQL Server Agent Jobs → dbt Projects on Snowflake:**

```sql
-- Create scheduled execution
ALTER DBT PROJECT my_project
    SET SCHEDULE = 'USING CRON 0 2 * * * America/New_York';

-- Or use Snowflake Tasks
CREATE OR REPLACE TASK run_dbt_daily
    WAREHOUSE = TRANSFORM_WH
    SCHEDULE = 'USING CRON 0 2 * * * America/New_York'
AS
    EXECUTE DBT PROJECT my_project;
```

## Migration Checklist

- [ ] Inventory all SQL Server objects to migrate
- [ ] Map dependencies and execution order
- [ ] Design dbt layer architecture
- [ ] Translate T-SQL to Snowflake SQL
- [ ] Refactor procedural logic to declarative models
- [ ] Implement incremental strategies where needed
- [ ] Add comprehensive tests
- [ ] Validate data accuracy
- [ ] Document lineage and business logic
- [ ] Migrate scheduling to Snowflake
- [ ] Decommission SQL Server objects
- [ ] Update downstream dependencies

## Common Pitfalls

1. **Don't migrate procedural logic directly** - Refactor to declarative SQL
2. **Avoid WHILE loops** - Use set-based operations
3. **Don't use temp tables** - Use CTEs or intermediate models
4. **Avoid dynamic SQL** - Use Jinja templating
5. **Don't skip testing** - Validate every migrated model
6. **Don't ignore performance** - Optimize for Snowflake architecture
7. **Don't lose lineage** - Document all transformations

## Success Criteria

- All business logic accurately migrated
- Data validation tests pass 100%
- Performance meets or exceeds SQL Server
- Complete documentation of changes
- Stakeholder acceptance and sign-off
- Monitoring and alerting established
- Rollback procedures documented
