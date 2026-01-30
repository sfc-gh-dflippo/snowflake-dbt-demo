# dbt Migration Skills - User Guide

This guide provides instructions for Snowflake customers on how to use the dbt migration skills to
convert legacy database objects to dbt models compatible with Snowflake.

## Table of Contents

- [Overview](#overview)
- [Setting Up Skills for Cortex Code CLI](#setting-up-skills-for-cortex-code-cli)
- [Migration Approaches](#migration-approaches)
- [Preparing Your Code](#preparing-your-code)
- [Available Skills](#available-skills)
- [Example 1: Migrating Snowflake Objects After SnowConvert](#example-1-migrating-snowflake-objects-after-snowconvert)
- [Example 2: Direct SQL Server to dbt Migration](#example-2-direct-sql-server-to-dbt-migration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

The dbt migration skills help AI agents convert database objects (views, tables, stored procedures)
from various source platforms into production-quality dbt models. The skills provide:

- **Syntax translation** from source platforms to Snowflake SQL
- **dbt best practices** including CTE patterns, naming conventions, and testing
- **Schema documentation** generation with `_models.yml` files
- **Validation rules** to ensure quality and consistency

---

## Setting Up Skills for Cortex Code CLI

These dbt migration skills can be imported directly from this GitHub repository using the native
Cortex Code CLI skill management features.

### Prerequisites

- **Cortex Code CLI** installed and configured
- **Git** installed on your system

### Import Skills from GitHub

Use the `cortex skill add` command to import skills directly from this GitHub repository. You must
specify the full path to the skills folder using the GitHub tree URL format:

```bash
cortex skill add https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/.claude/skills
```

This command automatically:

- Clones the repository to `~/.snowflake/cortex/remote_cache/`
- Discovers all skills in the specified `.claude/skills/` directory
- Makes them available in all future Cortex Code sessions

### Using the Interactive Skill Manager

Within a Cortex Code session, you can use the `/skill` command to open an interactive manager where
you can:

- View all skills by location (Project, Global, Remote, Bundled)
- Add skill directories or remote repositories
- Sync project skills to global
- Delete skills
- View skill details and conflicts

```text
/skill                    # Opens interactive skill manager
$$                        # Quick list of available skills
```

### Verify Installation

List all installed skills to confirm the import:

```bash
cortex skill list
```

You should see the dbt migration skills listed under "Remote skills", including:

- `dbt-migration` - Main orchestration workflow
- `dbt-migration-snowflake` - Convert Snowflake DDL to dbt
- `dbt-migration-ms-sql-server` - Convert SQL Server/Azure Synapse T-SQL
- `dbt-migration-oracle` - Convert Oracle PL/SQL
- And other platform-specific skills

### Remove Skills

Use the `/skill` interactive manager within Cortex Code to remove skills. The manager allows you to
view, delete, and manage skills across all locations.

For manual removal of remote skills, edit `~/.snowflake/cortex/skills.json` and remove the entry
from the `"remote"` array.

### Updating Skills

> **Note:** The `/skill` interactive manager's "refresh" option re-reads existing cached files but
> does **not** pull new changes from GitHub. To get the latest updates from the remote repository,
> you must manually remove and re-add the skills as described below.

To update skills with the latest changes from GitHub:

1. Edit the skills configuration file and remove the remote entry
2. Delete the cached repository
3. Re-add the skills

**Windows (PowerShell):**

```powershell
# Step 1: Edit skills.json - remove the remote entry for snowflake-dbt-demo
notepad $env:USERPROFILE\.snowflake\cortex\skills.json

# Step 2: Delete the cached repository
Remove-Item -Recurse -Force "$env:USERPROFILE\.snowflake\cortex\remote_cache\github_sfc-gh-dflippo_snowflake-dbt-demo*"

# Step 3: Re-add the skills
cortex skill add https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/tree/main/.claude/skills
```

**Linux/macOS:**

```bash
# Step 1: Edit skills.json - remove the remote entry for snowflake-dbt-demo
# Use your preferred editor (nano, vim, code, etc.)
nano ~/.snowflake/cortex/skills.json

# Step 2: Delete the cached repository
rm -rf ~/.snowflake/cortex/remote_cache/github_sfc-gh-dflippo_snowflake-dbt-demo*

# Step 3: Re-add the skills
cortex skill add https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/tree/main/.claude/skills
```

### Available dbt Skills

After setup, these skills will be available:

#### Migration Skills

| Skill Name                    | Source Platform                  | Key Features                       |
| ----------------------------- | -------------------------------- | ---------------------------------- |
| `dbt-migration`               | All platforms                    | Main orchestration (7-phase)       |
| `dbt-migration-snowflake`     | Snowflake                        | Native Snowflake to dbt patterns   |
| `dbt-migration-ms-sql-server` | SQL Server / Azure Synapse       | T-SQL, IDENTITY, TOP, #temp tables |
| `dbt-migration-oracle`        | Oracle                           | PL/SQL, ROWNUM, CONNECT BY         |
| `dbt-migration-teradata`      | Teradata                         | QUALIFY, BTEQ, volatile tables     |
| `dbt-migration-bigquery`      | BigQuery                         | UNNEST, STRUCT/ARRAY               |
| `dbt-migration-redshift`      | Redshift                         | DISTKEY/SORTKEY, COPY/UNLOAD       |
| `dbt-migration-postgres`      | PostgreSQL / Greenplum / Netezza | Array expressions                  |
| `dbt-migration-db2`           | IBM DB2                          | SQL PL, FETCH FIRST                |
| `dbt-migration-hive`          | Hive / Spark / Databricks        | External tables, PARTITIONED BY    |
| `dbt-migration-vertica`       | Vertica                          | Projections, flex tables           |
| `dbt-migration-sybase`        | Sybase IQ                        | T-SQL variant                      |
| `dbt-migration-validation`    | All platforms                    | Validate models against rules      |

#### Core dbt Skills

| Skill Name             | Description                                                         |
| ---------------------- | ------------------------------------------------------------------- |
| `dbt-core`             | Installation, configuration, project setup, package management      |
| `dbt-commands`         | Command-line operations, model selection syntax, Jinja patterns     |
| `dbt-architecture`     | Project structure, medallion architecture (bronze/silver/gold)      |
| `dbt-modeling`         | Writing models with CTE patterns, SQL structure, layer templates    |
| `dbt-materializations` | Choosing materializations (view, table, incremental, snapshots)     |
| `dbt-testing`          | Testing strategies with dbt_constraints, generic and singular tests |
| `dbt-artifacts`        | Monitor execution using dbt Artifacts package                       |
| `dbt-performance`      | Optimization through clustering, warehouse sizing, query tuning     |

#### Snowflake Integration Skills

| Skill Name                     | Description                                            |
| ------------------------------ | ------------------------------------------------------ |
| `dbt-projects-on-snowflake`    | Deploy and run dbt projects natively in Snowflake      |
| `dbt-projects-snowflake-setup` | Step-by-step setup guide for dbt Projects on Snowflake |

### Using Skills in Cortex Code

Once installed, invoke skills using the `$skill-name` syntax in your Cortex Code session:

```text
$dbt-migration-ms-sql-server Convert this stored procedure to a dbt model:

[paste your SQL Server code here]
```

Or use the `@` syntax to include a file directly:

```text
$dbt-migration-snowflake Convert @migration_source/views/vw_customer_orders.sql to a dbt model
following the medallion architecture pattern.
```

You can also reference Snowflake tables directly with `#`:

```text
$dbt-migration-snowflake Convert the view #MY_DB.MY_SCHEMA.VW_CUSTOMER_ORDERS to a dbt model
```

### Troubleshooting Setup

| Issue                         | Solution                                                |
| ----------------------------- | ------------------------------------------------------- |
| Skills not appearing          | Run `cortex skill list` to verify installation          |
| "No valid skills found" error | Ensure you use the full tree URL with branch and path   |
| Git clone fails               | Check your network connection and GitHub access         |
| Command not found             | Verify Cortex Code CLI is installed: `cortex --version` |

---

## Migration Approaches

### Approach 1: Two-Step Migration (Recommended for Complex Migrations)

1. **Convert to Snowflake first** using
   [SnowConvert AI](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/about)
2. **Then convert to dbt** using `$dbt-migration-snowflake`

This approach is recommended when:

- Migrating from fully-supported SnowConvert platforms (SQL Server, Oracle, Teradata, Redshift)
- Complex stored procedures require AI-assisted conversion
- You want to validate Snowflake compatibility before adding dbt patterns

### Approach 2: Direct Migration

Convert source DDL directly to dbt models using platform-specific skills (e.g.,
`$dbt-migration-ms-sql-server`).

This approach works well when:

- Migrating simple to medium complexity views
- You have strong dbt expertise
- The source platform has limited SnowConvert support

---

## Preparing Your Code

### Step 1: Organize Source DDL

Create a folder structure for your source objects similar to the following:

```text
migration_source/
├── tables/
│   ├── customers.sql
│   └── orders.sql
├── views/
│   ├── vw_customer_summary.sql
│   └── vw_order_metrics.sql
├── stored_procedures/
│   ├── sp_load_customers.sql
│   └── sp_calculate_metrics.sql
└── functions/
    └── fn_format_date.sql
```

### Step 2: Extract DDL from Source Database

#### SQL Server

```sql
-- Extract view definitions
SELECT
    SCHEMA_NAME(v.schema_id) + '.' + v.name AS view_name,
    OBJECT_DEFINITION(v.object_id) AS view_definition
FROM sys.views v
WHERE SCHEMA_NAME(v.schema_id) = 'dbo';

-- Extract stored procedure definitions
SELECT
    SCHEMA_NAME(p.schema_id) + '.' + p.name AS proc_name,
    OBJECT_DEFINITION(p.object_id) AS proc_definition
FROM sys.procedures p
WHERE SCHEMA_NAME(p.schema_id) = 'dbo';
```

#### Snowflake

```sql
-- Extract view definitions
SHOW VIEWS IN SCHEMA my_database.my_schema;
SELECT GET_DDL('VIEW', 'my_database.my_schema.my_view');

-- Extract stored procedure definitions
SHOW PROCEDURES IN SCHEMA my_database.my_schema;
SELECT GET_DDL('PROCEDURE', 'my_database.my_schema.my_procedure(arg1 STRING, arg2 INT)');
```

### Step 3: Document Dependencies

Create a dependency mapping showing which objects depend on others:

**migration_tracker.csv**

| Object Name         | Object Type | Source Schema | Depends On        | Complexity | Target Layer |
| ------------------- | ----------- | ------------- | ----------------- | ---------- | ------------ |
| customers           | TABLE       | dbo           | -                 | Low        | Bronze       |
| orders              | TABLE       | dbo           | customers         | Low        | Bronze       |
| vw_customer_summary | VIEW        | dbo           | customers, orders | Medium     | Silver       |
| sp_load_customers   | PROCEDURE   | dbo           | customers         | High       | Gold         |

---

## Example 1: Migrating Snowflake Objects After SnowConvert

This example demonstrates the recommended two-step approach: using SnowConvert to convert SQL Server
to Snowflake, then using the AI agent to convert Snowflake objects to dbt.

### Scenario

You have a SQL Server view that was converted to Snowflake using SnowConvert. Now you want to
convert it to a dbt model.

### Source: Snowflake View (Post-SnowConvert)

```sql
-- File: migration_source/views/vw_customer_orders.sql
-- This was converted from SQL Server [dbo].[vw_CustomerOrders] by SnowConvert

CREATE OR REPLACE VIEW analytics.vw_customer_orders AS
SELECT
    c.customer_id,
    c.customer_name,
    c.email,
    COUNT(o.order_id) AS total_orders,
    SUM(o.order_amount) AS total_spent,
    MAX(o.order_date) AS last_order_date,
    CASE
        WHEN SUM(o.order_amount) > 10000 THEN 'Premium'
        WHEN SUM(o.order_amount) > 1000 THEN 'Standard'
        ELSE 'Basic'
    END AS customer_tier
FROM raw_data.customers c
LEFT JOIN raw_data.orders o ON c.customer_id = o.customer_id
WHERE c.is_active = TRUE
GROUP BY c.customer_id, c.customer_name, c.email;
```

### AI Agent Prompt for Snowflake Conversion

```text
$dbt-migration-snowflake Convert this Snowflake view to a dbt model. The view was originally
converted from SQL Server [dbo].[vw_CustomerOrders] using SnowConvert.

Requirements:
- Place it in the silver layer with an `int_` prefix
- Use the standard CTE pattern
- Create the corresponding _models.yml with appropriate tests
- Add explicit type casts for all columns

@migration_source/views/vw_customer_orders.sql
```

### Expected Output

The AI agent will generate:

#### 1. dbt Model (models/silver/customers/int_customer_orders.sql)

```sql
{{ config(materialized='view', tags=['silver', 'customer']) }}

/* Original Object: analytics.vw_customer_orders
   Source Platform: Snowflake (converted from SQL Server dbo.vw_CustomerOrders)
   Purpose: Customer order aggregation with tier classification
   Conversion Notes:
   - Added source() references for raw tables
   - Implemented standard CTE pattern
   - Added explicit type casts */

WITH customers AS (
    SELECT * FROM {{ source('raw_data', 'customers') }}
),

orders AS (
    SELECT * FROM {{ source('raw_data', 'orders') }}
),

customer_orders AS (
    SELECT
        c.customer_id::INTEGER AS customer_id,
        c.customer_name::VARCHAR(100) AS customer_name,
        c.email::VARCHAR(255) AS email,
        COUNT(o.order_id)::INTEGER AS total_orders,
        COALESCE(SUM(o.order_amount), 0)::NUMBER(18,2) AS total_spent,
        MAX(o.order_date)::DATE AS last_order_date,
        CASE
            WHEN SUM(o.order_amount) > 10000 THEN 'Premium'
            WHEN SUM(o.order_amount) > 1000 THEN 'Standard'
            ELSE 'Basic'
        END::VARCHAR(20) AS customer_tier
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.is_active = TRUE
    GROUP BY c.customer_id, c.customer_name, c.email
),

final AS (
    SELECT
        customer_id,
        customer_name,
        email,
        total_orders,
        total_spent,
        last_order_date,
        customer_tier
    FROM customer_orders
)

SELECT * FROM final
```

#### 2. Schema YAML (models/silver/customers/\_models.yml)

```yaml
version: 2

models:
  - name: int_customer_orders
    description: |
      Customer order aggregation with tier classification.
      Converted from SQL Server [dbo].[vw_CustomerOrders] via SnowConvert.

      Business Logic:
      - Premium tier: total_spent > $10,000
      - Standard tier: total_spent > $1,000
      - Basic tier: all others
    columns:
      - name: customer_id
        description: "Primary key - unique customer identifier"
        data_type: integer
        tests:
          - dbt_constraints.primary_key
      - name: customer_name
        description: "Customer full name"
        data_type: varchar(100)
      - name: email
        description: "Customer email address"
        data_type: varchar(255)
      - name: total_orders
        description: "Count of all orders placed by customer"
        data_type: integer
      - name: total_spent
        description: "Sum of all order amounts in USD"
        data_type: number(18,2)
      - name: last_order_date
        description: "Most recent order date"
        data_type: date
      - name: customer_tier
        description: "Customer segment based on total spending"
        data_type: varchar(20)
        tests:
          - accepted_values:
              values: ["Premium", "Standard", "Basic"]
```

---

## Example 2: Direct SQL Server to dbt Migration

This example demonstrates direct conversion from SQL Server T-SQL to dbt without using SnowConvert
first.

### Use Case

You have a SQL Server stored procedure that loads customer dimension data. You want to convert it
directly to a dbt incremental model.

### Source: SQL Server Stored Procedure

```sql
-- File: migration_source/stored_procedures/sp_load_dim_customer.sql

CREATE PROCEDURE [dbo].[sp_LoadDimCustomer]
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -- Merge customer changes
        MERGE INTO dw.dim_customer AS target
        USING (
            SELECT TOP 100 PERCENT
                c.customer_id,
                c.customer_name,
                ISNULL(c.email, 'unknown@email.com') AS email,
                c.phone,
                a.address_line1,
                a.city,
                a.state,
                a.postal_code,
                GETDATE() AS effective_date,
                1 AS is_current
            FROM staging.customers c
            LEFT JOIN staging.addresses a ON c.address_id = a.address_id
            WHERE c.modified_date > DATEADD(day, -1, GETDATE())
        ) AS source
        ON target.customer_id = source.customer_id
        WHEN MATCHED AND target.is_current = 1 THEN
            UPDATE SET
                customer_name = source.customer_name,
                email = source.email,
                phone = source.phone,
                address_line1 = source.address_line1,
                city = source.city,
                state = source.state,
                postal_code = source.postal_code,
                effective_date = source.effective_date
        WHEN NOT MATCHED THEN
            INSERT (customer_id, customer_name, email, phone,
                    address_line1, city, state, postal_code,
                    effective_date, is_current)
            VALUES (source.customer_id, source.customer_name, source.email,
                    source.phone, source.address_line1, source.city,
                    source.state, source.postal_code,
                    source.effective_date, source.is_current);

        PRINT 'Rows affected: ' + CAST(@@ROWCOUNT AS VARCHAR);

    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;
```

### AI Agent Prompt for SQL Server Conversion

```text
$dbt-migration-ms-sql-server Convert this SQL Server stored procedure to a dbt incremental model.

Requirements:
- Convert T-SQL syntax to Snowflake-compatible SQL
- Implement the MERGE logic as a dbt incremental model
- Place it in the gold layer as a dimension model with `dim_` prefix
- Create the _models.yml with primary key tests
- Add inline comments for any syntax conversions

@migration_source/stored_procedures/sp_load_dim_customer.sql
```

### Generated Output

The AI agent will generate:

#### 1. dbt Model (models/gold/customers/dim_customer.sql)

```sql
{{ config(
    materialized='incremental',
    unique_key='customer_id',
    merge_update_columns=['customer_name', 'email', 'phone', 'address_line1',
                          'city', 'state', 'postal_code', 'effective_date'],
    tags=['gold', 'customer', 'dimension']
) }}

/* Original Object: [dbo].[sp_LoadDimCustomer]
   Source Platform: SQL Server
   Original Type: Stored Procedure
   Migration Date: {{ run_started_at.strftime('%Y-%m-%d') }}

   Conversion Notes:
   - MERGE statement converted to dbt incremental with merge strategy
   - ISNULL() converted to COALESCE()
   - GETDATE() converted to CURRENT_TIMESTAMP()
   - DATEADD() syntax compatible with Snowflake
   - TOP 100 PERCENT removed (unnecessary)
   - TRY...CATCH replaced with dbt's built-in error handling
   - @@ROWCOUNT tracking handled by dbt run results */

WITH stg_customers AS (
    SELECT * FROM {{ ref('stg_sqlserver__customers') }}
),

stg_addresses AS (
    SELECT * FROM {{ ref('stg_sqlserver__addresses') }}
),

-- Join customers with addresses and apply business logic
customer_with_address AS (
    SELECT
        c.customer_id::INTEGER AS customer_id,
        c.customer_name::VARCHAR(100) AS customer_name,
        -- ISNULL converted to COALESCE
        COALESCE(c.email, 'unknown@email.com')::VARCHAR(255) AS email,
        c.phone::VARCHAR(20) AS phone,
        a.address_line1::VARCHAR(200) AS address_line1,
        a.city::VARCHAR(100) AS city,
        a.state::VARCHAR(50) AS state,
        a.postal_code::VARCHAR(20) AS postal_code,
        -- GETDATE() converted to CURRENT_TIMESTAMP()
        CURRENT_TIMESTAMP()::TIMESTAMP_NTZ AS effective_date,
        1::BOOLEAN AS is_current,
        c.modified_date::TIMESTAMP_NTZ AS modified_date
    FROM stg_customers c
    LEFT JOIN stg_addresses a ON c.address_id = a.address_id
    {% if is_incremental() %}
    -- DATEADD syntax compatible with Snowflake
    WHERE c.modified_date > DATEADD(day, -1, CURRENT_TIMESTAMP())
    {% endif %}
),

final AS (
    SELECT
        customer_id,
        customer_name,
        email,
        phone,
        address_line1,
        city,
        state,
        postal_code,
        effective_date,
        is_current
    FROM customer_with_address
)

SELECT * FROM final
```

#### 2. Schema YAML (models/gold/customers/\_models.yml)

```yaml
version: 2

models:
  - name: dim_customer
    description: |
      Customer dimension containing customer attributes and current address.
      Converted from SQL Server stored procedure [dbo].[sp_LoadDimCustomer].

      Incremental Strategy:
      - Uses MERGE on customer_id
      - Processes only records modified in the last day
      - Updates existing customers, inserts new ones

      Source: Staging customers and addresses tables
      Refresh: Daily incremental
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        description: "Primary key - unique customer identifier from source system"
        data_type: integer
        tests:
          - dbt_constraints.primary_key
      - name: customer_name
        description: "Customer full name"
        data_type: varchar(100)
        tests:
          - not_null
      - name: email
        description: "Customer email address; defaults to 'unknown@email.com' if null in source"
        data_type: varchar(255)
        tests:
          - not_null
      - name: phone
        description: "Customer phone number"
        data_type: varchar(20)
      - name: address_line1
        description: "Primary address street line"
        data_type: varchar(200)
      - name: city
        description: "Address city"
        data_type: varchar(100)
      - name: state
        description: "Address state/province"
        data_type: varchar(50)
      - name: postal_code
        description: "Address postal/ZIP code"
        data_type: varchar(20)
      - name: effective_date
        description: "Date/time when this record version became effective"
        data_type: timestamp_ntz
        tests:
          - not_null
      - name: is_current
        description: "Flag indicating if this is the current version of the customer record"
        data_type: boolean
        tests:
          - not_null
          - accepted_values:
              values: [true, false]
```

#### 3. Staging Models (Prerequisites)

The agent will also recommend creating staging models for the source tables:

```sql
-- models/bronze/sqlserver/stg_sqlserver__customers.sql
{{ config(materialized='ephemeral', tags=['bronze', 'sqlserver']) }}

SELECT * FROM {{ source('sqlserver_staging', 'customers') }}
```

```sql
-- models/bronze/sqlserver/stg_sqlserver__addresses.sql
{{ config(materialized='ephemeral', tags=['bronze', 'sqlserver']) }}

SELECT * FROM {{ source('sqlserver_staging', 'addresses') }}
```

---

## Best Practices

### 1. Start with Simple Objects

Begin with simple views before tackling complex stored procedures. This helps you:

- Understand the migration patterns
- Build confidence with the tooling
- Establish naming conventions early

### 2. Use Tags for Tracking

Add tags to track migration progress:

```sql
{{ config(
    materialized='view',
    tags=['migrated', 'sqlserver', 'phase1']
) }}
```

### 3. Validate Incrementally

Run `dbt build` after each conversion to catch issues early:

```bash
# Build a single model
dbt build --select dim_customer

# Build all models with a specific tag
dbt build --select tag:migrated
```

### 4. Compare Results

Create validation queries to compare source and target:

```sql
-- Validation query to compare row counts
SELECT
    'source' AS system,
    COUNT(*) AS row_count
FROM source_database.schema.table
UNION ALL
SELECT
    'dbt' AS system,
    COUNT(*) AS row_count
FROM {{ ref('target_model') }}
```

### 5. Document Conversion Decisions

Always include header comments explaining:

- Original object name and location
- Key syntax conversions made
- Business logic preserved or modified
- Any breaking changes

---

## Troubleshooting

### Common Issues

| Issue                           | Solution                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------- |
| "Syntax error" after conversion | Check for platform-specific syntax not converted (see skill translation tables) |
| Missing columns in output       | Ensure `SELECT *` was expanded to explicit columns                              |
| Type mismatch errors            | Add explicit type casts using `::TYPE` syntax                                   |
| ref() not found                 | Create staging models for source tables first                                   |
| Test failures                   | Review primary key uniqueness and null handling                                 |

### Getting Help

1. **Check the skill documentation**: Each `dbt-migration-*` skill contains detailed syntax
   conversion tables
2. **Review translation references**: Located in `translation-references/` folders within each skill
3. **Run validation**: Use `dbt compile` to catch syntax errors before running
4. **Use dbt docs**: Generate documentation with `dbt docs generate` to visualize lineage

---

## Related Documentation

- [SKILL.md](SKILL.md) - Main migration workflow skill
- [dbt-migration-validation](../dbt-migration-validation/SKILL.md) - Validation rules and quality
  checks
- [dbt-modeling](../dbt-modeling/SKILL.md) - CTE patterns and SQL structure
- [dbt-testing](../dbt-testing/SKILL.md) - Testing strategies with dbt_constraints
- [dbt-architecture](../dbt-architecture/SKILL.md) - Project organization and naming conventions
