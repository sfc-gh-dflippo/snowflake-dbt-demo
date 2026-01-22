---
name: dbt-migration
description:
  Complete workflow for migrating legacy database DDL (views, tables, stored procedures) to dbt
  projects on Snowflake. This skill orchestrates the full migration lifecycle including discovery,
  planning, placeholder model creation, view conversion, stored procedure transformation, end-to-end
  testing, and deployment. Use this skill when planning or executing database migrations to dbt,
  delegating platform-specific syntax translation to source-specific skills.
---

# Database to dbt Migration Workflow

## Purpose

Guide AI agents through the complete migration lifecycle from legacy database systems (SQL Server,
Oracle, Teradata, etc.) to production-quality dbt projects on Snowflake. This skill defines a
structured, repeatable process while delegating platform-specific syntax translation to dedicated
source-specific skills.

## When to Use This Skill

Activate this skill when users ask about:

- Planning a database migration to dbt
- Organizing legacy scripts for migration
- Creating placeholder models with correct datatypes
- Converting views and stored procedures to dbt models
- Testing migration results against source systems
- Deploying migrated dbt projects to production
- Understanding the overall migration workflow

For **platform-specific syntax translation**, delegate to:

- `dbt-migration-ms-sql-server` - SQL Server / Azure Synapse T-SQL
- `dbt-migration-oracle` - Oracle PL/SQL
- `dbt-migration-teradata` - Teradata SQL and BTEQ
- `dbt-migration-bigquery` - Google BigQuery
- `dbt-migration-redshift` - Amazon Redshift
- `dbt-migration-postgres` - PostgreSQL / Greenplum / Netezza
- `dbt-migration-db2` - IBM DB2
- `dbt-migration-hive` - Hive / Spark / Databricks
- `dbt-migration-vertica` - Vertica
- `dbt-migration-sybase` - Sybase IQ

---

# Migration Workflow Overview

The migration process follows seven phases, each with specific deliverables and validation criteria:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATABASE TO DBT MIGRATION                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Phase 1          Phase 2          Phase 3          Phase 4                 │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐           │
│  │DISCOVERY │ ──► │PLANNING  │ ──► │PLACEHOLDER│ ──► │  VIEWS   │           │
│  │& ASSESS  │     │& ORGANIZE│     │  MODELS  │     │CONVERSION│           │
│  └──────────┘     └──────────┘     └──────────┘     └──────────┘           │
│       │                │                │                │                  │
│       ▼                ▼                ▼                ▼                  │
│  - Inventory      - Folder         - NULL casts     - Syntax              │
│  - Dependencies     structure      - _models.yml      translation         │
│  - Volumes        - Layer mapping  - Compile test   - CTE patterns        │
│  - Complexity     - Naming rules   - Schema docs    - dbt tests           │
│                                                                             │
│  Phase 5          Phase 6          Phase 7                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                            │
│  │  TABLE   │ ──► │END-TO-END│ ──► │DEPLOYMENT│                            │
│  │  LOGIC   │     │ TESTING  │     │& CUTOVER │                            │
│  └──────────┘     └──────────┘     └──────────┘                            │
│       │                │                │                                   │
│       ▼                ▼                ▼                                   │
│  - SP analysis    - Row counts     - Deploy to dev                         │
│  - Declarative    - Checksums      - Full validation                       │
│    SQL            - Business       - Cutover plan                          │
│  - Incremental      rules          - Production                            │
│    patterns       - Mock data      - Monitoring                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# Phase 1: Discovery and Assessment

## Objective

Create a complete inventory of source database objects and understand dependencies, volumes, and
complexity to inform migration planning.

## Activities

### 1.1 Inventory Source Objects

Query system catalogs to extract all objects in scope:

**SQL Server Example:**

```sql
-- Tables and Views
SELECT
    s.name AS schema_name,
    o.name AS object_name,
    o.type_desc AS object_type,
    p.rows AS row_count
FROM sys.objects o
JOIN sys.schemas s ON o.schema_id = s.schema_id
LEFT JOIN sys.partitions p ON o.object_id = p.object_id AND p.index_id IN (0, 1)
WHERE o.type IN ('U', 'V')  -- Tables and Views
ORDER BY s.name, o.name;

-- Stored Procedures and Functions
SELECT
    s.name AS schema_name,
    o.name AS object_name,
    o.type_desc AS object_type,
    m.definition AS source_code
FROM sys.objects o
JOIN sys.schemas s ON o.schema_id = s.schema_id
JOIN sys.sql_modules m ON o.object_id = m.object_id
WHERE o.type IN ('P', 'FN', 'IF', 'TF')  -- Procedures and Functions
ORDER BY s.name, o.name;
```

**Oracle Example:**

```sql
-- Tables and Views
SELECT
    owner AS schema_name,
    object_name,
    object_type,
    created,
    last_ddl_time
FROM all_objects
WHERE object_type IN ('TABLE', 'VIEW')
  AND owner NOT IN ('SYS', 'SYSTEM')
ORDER BY owner, object_name;

-- Row counts (run separately for large schemas)
SELECT table_name, num_rows FROM all_tables WHERE owner = 'YOUR_SCHEMA';
```

### 1.2 Document Dependencies

Map object dependencies to determine migration order:

```sql
-- SQL Server dependency query
SELECT DISTINCT
    OBJECT_SCHEMA_NAME(referencing_id) AS referencing_schema,
    OBJECT_NAME(referencing_id) AS referencing_object,
    referenced_schema_name AS referenced_schema,
    referenced_entity_name AS referenced_object
FROM sys.sql_expression_dependencies
WHERE referenced_entity_name IS NOT NULL
ORDER BY referenced_schema, referenced_object;
```

### 1.3 Assess Complexity

Categorize objects by migration complexity:

| Complexity | Criteria                                              | Examples                      |
| ---------- | ----------------------------------------------------- | ----------------------------- |
| **Low**    | Simple SELECT, no joins or minimal joins              | Lookup tables, simple views   |
| **Medium** | Multiple joins, aggregations, CASE statements         | Summary views, report queries |
| **High**   | Procedural logic, cursors, temp tables, complex ETL   | SCD procedures, bulk loads    |
| **Custom** | Platform-specific features requiring manual review    | Wrapped code, CLR functions   |

### 1.4 Create Migration Tracker

Document each object in a tracking spreadsheet or issue tracker:

| Object Name | Type | Schema | Complexity | Row Count | Dependencies | Status | Assignee |
| ----------- | ---- | ------ | ---------- | --------- | ------------ | ------ | -------- |
| dim_customer | SP | dbo | High | 1.2M | stg_customer | Pending | - |
| vw_active_orders | View | sales | Low | - | orders, customers | Pending | - |

## Phase 1 Checklist

- [ ] All tables inventoried with row counts
- [ ] All views inventoried
- [ ] All stored procedures and functions inventoried
- [ ] Object dependencies mapped
- [ ] Complexity assessment complete
- [ ] Migration tracker created
- [ ] Data volumes documented
- [ ] Refresh frequencies identified

---

# Phase 2: Planning and Organization

## Objective

Organize legacy scripts, map objects to the dbt medallion architecture, and establish naming
conventions before any conversion begins.

## Activities

### 2.1 Organize Legacy Scripts

Create a folder structure to hold source DDL for reference:

```
legacy_scripts/
├── tables/
│   ├── dim_customer.sql
│   ├── fact_orders.sql
│   └── ...
├── views/
│   ├── vw_active_customers.sql
│   ├── vw_order_summary.sql
│   └── ...
├── stored_procedures/
│   ├── usp_load_dim_customer.sql
│   ├── usp_load_fact_orders.sql
│   └── ...
└── functions/
    ├── fn_calculate_tax.sql
    └── ...
```

### 2.2 Map to Medallion Layers

Assign each source object to a target dbt layer:

| Source Object Type | Target Layer | dbt Prefix | Materialization |
| ------------------ | ------------ | ---------- | --------------- |
| Source tables (raw) | Bronze | `stg_` | ephemeral |
| Simple views | Bronze | `stg_` | ephemeral |
| Complex views with logic | Silver | `int_` | ephemeral/table |
| Dimension load procedures | Gold | `dim_` | table |
| Fact load procedures | Gold | `fct_` | incremental |
| Lookup/reference tables | Silver | `lookup_` | table |

### 2.3 Define Naming Conventions

Establish consistent naming aligned with `dbt-architecture` skill:

**Model Naming:**

- Bronze: `stg_{source}__{table}` (e.g., `stg_sqlserver__customers`)
- Silver: `int_{entity}__{description}` (e.g., `int_customers__with_orders`)
- Gold: `dim_{entity}` or `fct_{process}` (e.g., `dim_customers`, `fct_order_lines`)

**Column Naming:**

- Primary keys: `{entity}_id` (e.g., `customer_id`)
- Foreign keys: Same as referenced primary key
- Booleans: `is_{condition}` or `has_{attribute}`
- Dates: `{event}_date` or `{event}_at`
- Amounts: `{metric}_amount` with currency suffix if needed

### 2.4 Create Dependency Graph

Visualize migration order based on dependencies:

```
stg_customers ──┐
                ├──► int_customers__with_orders ──► dim_customers
stg_orders ─────┘                                        │
                                                         ▼
stg_line_items ──────────────────────────────────► fct_order_lines
```

### 2.5 Establish Validation Criteria

Define how success will be measured for each object:

- Row count tolerance (exact match or ± n%)
- Column-level checksum comparison
- Business rule verification queries
- Performance benchmarks (query time)

## Phase 2 Checklist

- [ ] Legacy scripts organized in folders
- [ ] All objects mapped to medallion layers
- [ ] Naming conventions documented
- [ ] Dependency graph created
- [ ] Migration order established
- [ ] Validation criteria defined per object
- [ ] dbt project structure planned

---

# Phase 3: Create Placeholder Models

## Objective

Create empty dbt models with correct column names, data types, and schema documentation **before**
adding any transformation logic. This establishes the contract for downstream consumers.

## Activities

### 3.1 Generate Placeholder Models

Create a model file for each target table with explicit datatype casting:

```sql
-- models/bronze/stg_sqlserver__customers.sql
-- Placeholder model - columns and datatypes only
-- Source: OLTP_DB.dbo.Customers
-- Status: Placeholder - awaiting logic conversion

select
    null::integer as customer_id,
    null::varchar(100) as customer_name,
    null::varchar(50) as first_name,
    null::varchar(50) as last_name,
    null::varchar(255) as email,
    null::varchar(20) as phone,
    null::varchar(500) as address_line_1,
    null::varchar(500) as address_line_2,
    null::varchar(100) as city,
    null::varchar(50) as state,
    null::varchar(20) as postal_code,
    null::varchar(50) as country,
    null::number(18,2) as account_balance,
    null::date as signup_date,
    null::timestamp_ntz as created_at,
    null::timestamp_ntz as updated_at,
    null::boolean as is_active

-- This model intentionally returns no rows
-- Update with actual source reference after validation
where false
```

### 3.2 Data Type Mapping Reference

Use explicit Snowflake types with precision:

| Source Type (SQL Server) | Snowflake Type | Example Cast |
| ------------------------ | -------------- | ------------ |
| INT, BIGINT | INTEGER | `null::integer` |
| VARCHAR(n), NVARCHAR(n) | VARCHAR(n) | `null::varchar(100)` |
| CHAR(n), NCHAR(n) | CHAR(n) | `null::char(10)` |
| DECIMAL(p,s), NUMERIC(p,s) | NUMBER(p,s) | `null::number(18,2)` |
| MONEY | NUMBER(19,4) | `null::number(19,4)` |
| FLOAT, REAL | FLOAT | `null::float` |
| DATE | DATE | `null::date` |
| DATETIME, DATETIME2 | TIMESTAMP_NTZ | `null::timestamp_ntz` |
| DATETIMEOFFSET | TIMESTAMP_TZ | `null::timestamp_tz` |
| BIT | BOOLEAN | `null::boolean` |
| UNIQUEIDENTIFIER | VARCHAR(36) | `null::varchar(36)` |
| VARBINARY, IMAGE | BINARY | `null::binary` |

> For other source platforms, refer to the platform-specific migration skills.

### 3.3 Create Schema Documentation

Generate `_models.yml` for each model with column descriptions:

```yaml
# models/bronze/_models.yml
version: 2

models:
  - name: stg_sqlserver__customers
    description: |
      Staging model for customer data from SQL Server OLTP database.
      Source: OLTP_DB.dbo.Customers
      Status: Placeholder - awaiting logic conversion
    columns:
      - name: customer_id
        description: "Primary key - unique customer identifier"
        tests:
          - dbt_constraints.primary_key

      - name: customer_name
        description: "Full name of the customer"
        tests:
          - not_null

      - name: first_name
        description: "Customer first name"

      - name: last_name
        description: "Customer last name"

      - name: email
        description: "Customer email address"
        tests:
          - dbt_constraints.unique_key

      - name: phone
        description: "Customer phone number"

      - name: account_balance
        description: "Current account balance in USD"

      - name: signup_date
        description: "Date customer signed up"

      - name: is_active
        description: "Flag indicating if customer account is active"
        tests:
          - accepted_values:
              values: [true, false]
```

### 3.4 Validate Placeholder Compilation

Run dbt to ensure all placeholder models compile:

```bash
# Compile all placeholder models
dbt compile --select tag:placeholder

# Or compile all bronze models
dbt compile --select bronze.*
```

### 3.5 Track Placeholder Status

Add a tag to identify placeholder models for tracking:

```sql
-- In each placeholder model
{{ config(
    materialized='ephemeral',
    tags=['placeholder', 'bronze']
) }}
```

## Phase 3 Checklist

- [ ] Placeholder model created for each target table
- [ ] All columns have explicit datatype casts
- [ ] Column names follow naming conventions
- [ ] `_models.yml` created with column descriptions
- [ ] Primary key tests defined
- [ ] Foreign key relationships documented
- [ ] All placeholder models compile successfully
- [ ] Placeholder tag applied for tracking

---

# Phase 4: Convert Views

## Objective

Convert source database views to dbt models, starting with simple views before tackling complex
ones. Views are typically easier than stored procedures as they contain declarative SQL.

## Activities

### 4.1 Prioritize View Conversion

Order views by complexity and dependencies:

1. **Simple views** - Single table, no joins
2. **Join views** - Multiple tables, straightforward joins
3. **Aggregate views** - GROUP BY, window functions
4. **Complex views** - Nested subqueries, CTEs, CASE logic

### 4.2 Apply Syntax Translation

Delegate platform-specific syntax to source skills. For example:

**SQL Server View (Before):**

```sql
CREATE VIEW dbo.vw_active_customers AS
SELECT TOP 1000
    c.CustomerID,
    c.CustomerName,
    ISNULL(c.Email, 'unknown@example.com') AS Email,
    CONVERT(VARCHAR(10), c.SignupDate, 120) AS SignupDateStr,
    DATEDIFF(day, c.SignupDate, GETDATE()) AS DaysSinceSignup
FROM dbo.Customers c WITH (NOLOCK)
WHERE c.IsActive = 1
ORDER BY c.SignupDate DESC;
```

**dbt Model (After):**

```sql
-- models/bronze/stg_sqlserver__active_customers.sql
{{ config(materialized='view') }}

/* Original Object: dbo.vw_active_customers
   Source Platform: SQL Server
   Conversion Notes:
   - TOP → LIMIT
   - ISNULL → COALESCE
   - CONVERT → TO_VARCHAR with format
   - GETDATE() → CURRENT_TIMESTAMP()
   - WITH (NOLOCK) hint removed
*/

with source_data as (
    select
        customer_id,
        customer_name,
        email,
        signup_date,
        is_active
    from {{ ref('stg_sqlserver__customers') }}
),

transformed as (
    select
        customer_id,
        customer_name,
        -- ISNULL converted to COALESCE
        coalesce(email, 'unknown@example.com') as email,
        -- CONVERT to TO_VARCHAR
        to_varchar(signup_date, 'YYYY-MM-DD') as signup_date_str,
        -- DATEDIFF and GETDATE() converted
        datediff(day, signup_date, current_timestamp()) as days_since_signup
    from source_data
    where is_active = true
)

select *
from transformed
order by signup_date desc
limit 1000
```

### 4.3 Apply CTE Patterns

Structure all models using the standard CTE pattern from `dbt-modeling` skill:

```sql
-- Import CTEs
with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

-- Logical CTEs (business logic)
customer_orders as (
    select
        c.customer_id,
        c.customer_name,
        count(o.order_id) as order_count
    from customers c
    left join orders o on c.customer_id = o.customer_id
    group by c.customer_id, c.customer_name
),

-- Final CTE
final as (
    select
        customer_id,
        customer_name,
        order_count
    from customer_orders
)

select * from final
```

### 4.4 Add dbt Tests

Define appropriate tests for each converted view:

```yaml
models:
  - name: stg_sqlserver__active_customers
    description: "Active customers with signup metrics"
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
      - name: email
        tests:
          - not_null
      - name: days_since_signup
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
```

### 4.5 Update Placeholder with Real Logic

Replace the placeholder SELECT with actual logic:

```sql
-- Before (placeholder)
select
    null::integer as customer_id,
    ...
where false

-- After (converted)
with source_data as (
    select * from {{ source('sqlserver', 'customers') }}
),
...
select * from final
```

## Phase 4 Checklist

- [ ] Views prioritized by complexity
- [ ] Simple views converted first
- [ ] Platform-specific syntax translated (delegate to source skills)
- [ ] CTE pattern applied consistently
- [ ] dbt tests added for each view
- [ ] Placeholder models updated with real logic
- [ ] Converted views compile successfully
- [ ] Inline comments document syntax changes

---

# Phase 5: Convert Table Logic from Stored Procedures

## Objective

Transform procedural stored procedure logic into declarative dbt models, selecting appropriate
materializations for different ETL patterns.

## Activities

### 5.1 Analyze Stored Procedure Patterns

Identify common ETL patterns in source procedures:

| Pattern | Source Characteristics | dbt Approach |
| ------- | ---------------------- | ------------ |
| **Full Refresh** | TRUNCATE + INSERT | `materialized='table'` |
| **SCD Type 1** | UPDATE existing + INSERT new | `materialized='incremental'` with merge |
| **SCD Type 2** | Expire + INSERT new version | `dbt snapshot` or custom incremental |
| **Append Only** | INSERT only, no updates | `materialized='incremental'` append |
| **Delete + Insert** | DELETE range + INSERT | `incremental` with `delete+insert` strategy |

### 5.2 Convert SCD Type 1 (Upsert)

**SQL Server Procedure (Before):**

```sql
CREATE PROCEDURE dbo.usp_Load_DimProduct AS
BEGIN
    -- Update existing products
    UPDATE dim
    SET dim.ProductName = src.ProductName,
        dim.Price = src.Price,
        dim.UpdatedAt = GETDATE()
    FROM dbo.DimProduct dim
    INNER JOIN staging.Products src ON dim.ProductID = src.ProductID
    WHERE dim.ProductName <> src.ProductName
       OR dim.Price <> src.Price;

    -- Insert new products
    INSERT INTO dbo.DimProduct (ProductID, ProductName, Price, CreatedAt)
    SELECT src.ProductID, src.ProductName, src.Price, GETDATE()
    FROM staging.Products src
    WHERE NOT EXISTS (
        SELECT 1 FROM dbo.DimProduct dim WHERE dim.ProductID = src.ProductID
    );
END;
```

**dbt Model (After):**

```sql
-- models/gold/dim_products.sql
{{ config(
    materialized='incremental',
    unique_key='product_id',
    incremental_strategy='merge',
    merge_update_columns=['product_name', 'price', 'updated_at']
) }}

with source_products as (
    select * from {{ ref('stg_sqlserver__products') }}
),

final as (
    select
        product_id,
        product_name,
        price,
        {% if is_incremental() %}
            current_timestamp() as updated_at,
            created_at  -- Preserve original created_at
        {% else %}
            current_timestamp() as updated_at,
            current_timestamp() as created_at
        {% endif %}
    from source_products
)

select * from final
```

### 5.3 Convert SCD Type 2 (History Tracking)

For SCD Type 2, use dbt snapshots:

```sql
-- snapshots/snap_customers.sql
{% snapshot snap_customers %}

{{ config(
    target_schema='snapshots',
    unique_key='customer_id',
    strategy='check',
    check_cols=['customer_name', 'customer_segment', 'region', 'country']
) }}

select
    customer_id,
    customer_name,
    customer_segment,
    region,
    country,
    email,
    phone
from {{ ref('stg_sqlserver__customers') }}

{% endsnapshot %}
```

Or use custom incremental for more control:

```sql
-- models/gold/dim_customers_scd2.sql
{{ config(
    materialized='incremental',
    unique_key='customer_surrogate_key'
) }}

with source as (
    select * from {{ ref('stg_sqlserver__customers') }}
),

{% if is_incremental() %}
-- Expire changed records
expired_records as (
    select
        dim.customer_surrogate_key,
        dim.customer_id,
        current_timestamp() as effective_end_date,
        false as is_current
    from {{ this }} dim
    inner join source src on dim.customer_id = src.customer_id
    where dim.is_current = true
      and (
          dim.customer_name != src.customer_name
          or dim.customer_segment != src.customer_segment
      )
),
{% endif %}

new_records as (
    select
        {{ dbt_utils.generate_surrogate_key(['customer_id', 'current_timestamp()']) }} as customer_surrogate_key,
        customer_id,
        customer_name,
        customer_segment,
        current_timestamp() as effective_start_date,
        '9999-12-31'::timestamp as effective_end_date,
        true as is_current
    from source
    {% if is_incremental() %}
    where customer_id in (select customer_id from expired_records)
       or customer_id not in (select customer_id from {{ this }})
    {% endif %}
)

select * from new_records
```

### 5.4 Break Complex Procedures into Models

A single stored procedure often maps to multiple dbt models:

```
usp_Load_CustomerAnalytics
├── int_customers__order_metrics      (aggregate orders per customer)
├── int_customers__rfm_scores         (calculate RFM scores)
├── int_customers__segments           (assign segments)
└── dim_customers                     (final dimension)
```

### 5.5 Handle Procedural Constructs

Convert procedural patterns to declarative SQL:

| Procedural Pattern | dbt Equivalent |
| ------------------ | -------------- |
| CURSOR loop | Window function or recursive CTE |
| Temp tables | CTEs or intermediate models |
| Variables | Jinja variables or macros |
| IF/ELSE branches | CASE expressions or `{% if %}` |
| TRY/CATCH | Pre-validation tests |
| WHILE loops | Recursive CTEs (with caution) |

### 5.6 Document Conversion Decisions

Add header comments explaining the conversion:

```sql
/* Original Procedure: dbo.usp_Load_DimCustomer
   Source Platform: SQL Server
   Original Pattern: SCD Type 2 with cursor-based updates

   Conversion Notes:
   - Cursor loop replaced with window function ROW_NUMBER()
   - Temp table #Changes converted to CTE
   - Transaction handling replaced with dbt's atomic model execution
   - Error handling replaced with pre-run dbt tests

   Breaking Changes:
   - Batch ID parameter removed (use dbt invocation_id instead)
   - RowsAffected output removed (use dbt run results)
*/
```

## Phase 5 Checklist

- [ ] All stored procedures analyzed for patterns
- [ ] ETL patterns mapped to dbt materializations
- [ ] Procedural logic converted to declarative SQL
- [ ] Complex procedures broken into multiple models
- [ ] SCD Type 2 implemented with snapshots or custom incremental
- [ ] Cursor loops eliminated
- [ ] Temp tables converted to CTEs
- [ ] Conversion decisions documented
- [ ] All converted models compile successfully

---

# Phase 6: End-to-End Testing and Validation

## Objective

Verify that migrated dbt models produce identical results to source system, using multiple
validation techniques to ensure data integrity.

## Activities

### 6.1 Row Count Validation

Compare total row counts between source and target:

```sql
-- Validation query: Row count comparison
-- Run in Snowflake after dbt build

with source_count as (
    select count(*) as row_count
    from SOURCE_DATABASE.SCHEMA.TABLE_NAME  -- Linked server or external table
),

target_count as (
    select count(*) as row_count
    from {{ ref('model_name') }}
)

select
    'source' as system,
    row_count,
    case when row_count = (select row_count from target_count) then 'PASS' else 'FAIL' end as status
from source_count
union all
select
    'target' as system,
    row_count,
    case when row_count = (select row_count from source_count) then 'PASS' else 'FAIL' end as status
from target_count;
```

### 6.2 Column Checksum Validation

Compare row-level hashes to identify differences:

```sql
-- Generate row hash for comparison
-- Source system (SQL Server)
SELECT
    CustomerID,
    HASHBYTES('SHA2_256',
        CONCAT(
            ISNULL(CAST(CustomerID AS VARCHAR), ''),
            ISNULL(CustomerName, ''),
            ISNULL(CAST(AccountBalance AS VARCHAR), '')
        )
    ) AS row_hash
FROM dbo.DimCustomer;

-- Target system (Snowflake)
select
    customer_id,
    sha2(concat_ws('|',
        coalesce(cast(customer_id as varchar), ''),
        coalesce(customer_name, ''),
        coalesce(cast(account_balance as varchar), '')
    ), 256) as row_hash
from {{ ref('dim_customers') }};
```

### 6.3 Business Rule Validation

Verify calculated fields and business logic:

```sql
-- tests/singular/test_customer_tier_logic.sql
-- Verify customer tier calculation matches source business rules

with tier_validation as (
    select
        customer_id,
        lifetime_value,
        customer_tier,
        case
            when lifetime_value >= 10000 then 'platinum'
            when lifetime_value >= 5000 then 'gold'
            when lifetime_value >= 1000 then 'silver'
            else 'bronze'
        end as expected_tier
    from {{ ref('dim_customers') }}
)

select *
from tier_validation
where customer_tier != expected_tier
```

### 6.4 Aggregate Validation

Compare summary metrics between systems:

```sql
-- Validate aggregate metrics match
select
    'source' as system,
    sum(order_amount) as total_revenue,
    count(distinct customer_id) as unique_customers,
    avg(order_amount) as avg_order_value
from SOURCE_DATABASE.dbo.FactOrders
where order_date between '2024-01-01' and '2024-12-31'

union all

select
    'target' as system,
    sum(order_amount) as total_revenue,
    count(distinct customer_id) as unique_customers,
    avg(order_amount) as avg_order_value
from {{ ref('fct_orders') }}
where order_date between '2024-01-01' and '2024-12-31';
```

### 6.5 Mock Data Testing

For complex transformations, create test fixtures:

```sql
-- seeds/test_customers_input.csv
customer_id,customer_name,signup_date,total_orders,total_revenue
1,John Doe,2023-01-15,5,500.00
2,Jane Smith,2023-06-20,12,2500.00
3,Bob Wilson,2024-01-01,1,50.00

-- seeds/test_customers_expected.csv (expected output)
customer_id,customer_name,customer_tier,is_active
1,John Doe,bronze,true
2,Jane Smith,silver,true
3,Bob Wilson,bronze,true
```

Then create a test that compares actual vs expected:

```sql
-- tests/singular/test_customer_transformation.sql
with actual as (
    select customer_id, customer_tier, is_active
    from {{ ref('dim_customers') }}
    where customer_id in (select customer_id from {{ ref('test_customers_input') }})
),

expected as (
    select customer_id, customer_tier, is_active
    from {{ ref('test_customers_expected') }}
)

select a.*
from actual a
full outer join expected e on a.customer_id = e.customer_id
where a.customer_tier != e.customer_tier
   or a.is_active != e.is_active
   or a.customer_id is null
   or e.customer_id is null
```

### 6.6 Incremental Validation

For incremental models, validate both initial load and incremental runs:

```bash
# Full refresh validation
dbt run --select fct_orders --full-refresh
dbt test --select fct_orders

# Incremental validation
dbt run --select fct_orders
dbt test --select fct_orders

# Compare row counts after incremental
```

### 6.7 Document Test Results

Create a validation report for each migrated object:

| Model | Row Count Match | Checksum Match | Business Rules | Performance | Status |
| ----- | --------------- | -------------- | -------------- | ----------- | ------ |
| dim_customers | PASS (1.2M) | PASS | PASS | 45s → 12s | Ready |
| fct_orders | PASS (50M) | 3 mismatches | PASS | 5min → 2min | Review |
| dim_products | PASS (10K) | PASS | PASS | 2s → 1s | Ready |

## Phase 6 Checklist

- [ ] Row count validation queries created
- [ ] Column checksum comparison implemented
- [ ] Business rule validation tests written
- [ ] Aggregate metrics compared
- [ ] Mock data test fixtures created (for complex logic)
- [ ] Incremental models tested (full refresh + incremental)
- [ ] All validation queries pass
- [ ] Discrepancies documented and resolved
- [ ] Validation report completed

---

# Phase 7: Deployment and Cutover

## Objective

Deploy validated dbt models to production with a clear cutover plan and monitoring strategy.

## Activities

### 7.1 Deploy to Development

```bash
# Deploy to dev environment
python deploy_dbt_project.py -n migration_project -d DEV_DB -s ANALYTICS -c dev_connection

# Run full build
dbt build --target dev

# Generate documentation
dbt docs generate
```

### 7.2 Deploy to Test/UAT

```bash
# Deploy to test environment
python deploy_dbt_project.py -n migration_project -d TEST_DB -s ANALYTICS -c test_connection -f

# Run full validation suite
dbt build --target test
dbt test --target test --store-failures
```

### 7.3 Create Cutover Plan

Document the production cutover sequence:

```markdown
## Cutover Plan: Customer Analytics Migration

### Pre-Cutover (T-1 day)
1. [ ] Final validation in TEST environment
2. [ ] Stakeholder sign-off obtained
3. [ ] Rollback procedure documented
4. [ ] Communication sent to users

### Cutover (T-0)
1. [ ] Disable source system ETL jobs
2. [ ] Run final source data sync
3. [ ] Deploy dbt project to production
4. [ ] Execute dbt build --target prod
5. [ ] Run validation queries
6. [ ] Update BI tool connections

### Post-Cutover (T+1)
1. [ ] Monitor query performance
2. [ ] Verify scheduled runs
3. [ ] Confirm user access
4. [ ] Close out migration tickets

### Rollback Procedure
If critical issues found:
1. Re-enable source ETL jobs
2. Revert BI connections to source
3. Document issues for remediation
```

### 7.4 Deploy to Production

```bash
# Deploy to production with validation
python deploy_dbt_project.py -n migration_project -d PROD_DB -s ANALYTICS -c prod_connection -f

# Full build with production data
dbt build --target prod

# Verify deployment
snow dbt list -c prod_connection
```

### 7.5 Configure Scheduled Runs

Set up automated execution using dbt Projects on Snowflake or external scheduler:

```sql
-- Create task for scheduled dbt runs
CREATE OR REPLACE TASK analytics_dbt_daily
  WAREHOUSE = ANALYTICS_WH
  SCHEDULE = 'USING CRON 0 6 * * * America/New_York'
AS
  CALL SYSTEM$DBT_RUN('migration_project', 'build --select tag:daily');
```

### 7.6 Monitor Post-Deployment

Set up monitoring for:

- **Run duration** - Track execution time trends
- **Row counts** - Alert on unexpected changes
- **Test failures** - Notify on data quality issues
- **Query performance** - Monitor downstream report latency

```sql
-- Query dbt run history (if using dbt_artifacts)
select
    model_name,
    status,
    execution_time_seconds,
    rows_affected,
    run_started_at
from {{ ref('model_executions') }}
where run_started_at > dateadd(day, -7, current_date())
order by run_started_at desc;
```

## Phase 7 Checklist

- [ ] Development deployment successful
- [ ] Test/UAT deployment successful
- [ ] Full validation suite passes in TEST
- [ ] Cutover plan documented
- [ ] Rollback procedure documented
- [ ] Stakeholder sign-off obtained
- [ ] Production deployment successful
- [ ] Scheduled runs configured
- [ ] Monitoring dashboards set up
- [ ] Source system ETL disabled
- [ ] BI connections updated
- [ ] Post-cutover validation complete
- [ ] Migration marked complete

---

# Related Skills

## Workflow Skills

- **dbt-architecture**: Project structure, medallion layers, naming conventions
- **dbt-modeling**: CTE patterns, SQL structure, layer-specific templates
- **dbt-testing**: Data quality tests, dbt_constraints, singular tests
- **dbt-materializations**: Incremental strategies, snapshots, Python models
- **dbt-performance**: Clustering keys, warehouse sizing, query optimization
- **dbt-commands**: dbt CLI operations, model selection syntax
- **dbt-core**: Installation, configuration, package management
- **snowflake-cli**: Snowflake operations, deployment commands

## Platform-Specific Translation Skills

For syntax translation, delegate to the appropriate source-specific skill:

| Source Platform | Skill Name | Key Considerations |
| --------------- | ---------- | ------------------ |
| SQL Server / Azure Synapse | `dbt-migration-ms-sql-server` | T-SQL, IDENTITY, TOP, #temp tables |
| Oracle | `dbt-migration-oracle` | PL/SQL, ROWNUM, CONNECT BY, packages |
| Teradata | `dbt-migration-teradata` | QUALIFY, BTEQ, volatile tables |
| BigQuery | `dbt-migration-bigquery` | UNNEST, STRUCT/ARRAY, backticks |
| Redshift | `dbt-migration-redshift` | DISTKEY/SORTKEY, COPY/UNLOAD |
| PostgreSQL | `dbt-migration-postgres` | Array expressions, psql commands |
| DB2 | `dbt-migration-db2` | SQL PL, FETCH FIRST, handlers |
| Hive/Spark | `dbt-migration-hive` | External tables, PARTITIONED BY |
| Vertica | `dbt-migration-vertica` | Projections, flex tables |
| Sybase | `dbt-migration-sybase` | T-SQL variant, SELECT differences |

---

# Quick Reference: Phase Summary

| Phase | Key Deliverable | Primary Skill |
| ----- | --------------- | ------------- |
| 1. Discovery | Object inventory, dependency map | This skill |
| 2. Planning | Folder structure, naming conventions | dbt-architecture |
| 3. Placeholders | Models with datatypes, schema.yml | This skill |
| 4. Views | Converted view models | dbt-migration-{source} |
| 5. Table Logic | Converted procedure models | dbt-materializations |
| 6. Testing | Validation queries, test results | dbt-testing |
| 7. Deployment | Production deployment, monitoring | dbt-core, snowflake-cli |

---

# Validation Hook Integration

## Automatic Quality Enforcement

The migration process is integrated with validation hooks that automatically run when models
are written or edited by Claude. This ensures quality standards are enforced throughout the
migration process.

### Hook Configuration

Hooks are configured in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/dbt-validation/validate_dbt_file.py --simple \"$FILE_PATH\"",
            "timeout": 30000
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/dbt-validation/validate_dbt_file.py --simple \"$FILE_PATH\"",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

### Validation Rules

**Schema YAML Files (`_models.yml`, `_sources.yml`):**
- Model descriptions present
- Primary key columns have appropriate tests
- Column documentation
- Naming convention compliance

**SQL Model Files (`.sql`):**
- CTE pattern structure
- No `SELECT *` in final output
- `ref()`/`source()` usage (no hardcoded tables)
- Snowflake-compatible syntax (no TOP, ISNULL, GETDATE, etc.)
- Migration header comments for converted models

### Phase-Specific Validation

| Phase | Validation Focus |
| ----- | ---------------- |
| Phase 3 (Placeholders) | YAML structure, column definitions, naming |
| Phase 4 (Views) | Syntax translation, CTE patterns, ref() usage |
| Phase 5 (Procedures) | Complex logic patterns, incremental configs |
| Phase 6 (Testing) | Test coverage, constraint definitions |

### Quality Gates

Before advancing to the next phase, ensure:

1. **All models compile**: `dbt compile`
2. **Validation hooks pass**: Check Claude Code output for errors
3. **Tests pass**: `dbt test`
4. **Documentation complete**: `dbt docs generate`

For detailed validation rules and auto-fix suggestions, see:
**[dbt-migration-validation](.claude/skills/dbt-migration-validation/SKILL.md)**
