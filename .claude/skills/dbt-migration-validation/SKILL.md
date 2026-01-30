---
name: dbt-migration-validation
description:
  Comprehensive validation skill for dbt models and schema YAML files. Defines validation rules,
  common anti-patterns to detect, and auto-fix suggestions. Integrates with Claude Code hooks to
  enforce quality standards during migration.
---

# dbt Migration Validation Skill

## Purpose

Define and enforce validation rules for dbt models during migration. This skill provides
comprehensive validation rules, common anti-patterns to detect, and auto-fix suggestions that are
implemented by the validation hooks.

## When to Use This Skill

Activate this skill when:

- Reviewing dbt models for quality issues
- Diagnosing validation hook failures
- Understanding validation rules and their rationale
- Looking up auto-fix suggestions for common issues
- Configuring validation thresholds

---

## Validation Rules Reference

### Schema YAML Rules

#### YAML001: Model Description Required

**Severity:** Error

**Description:** Every model must have a description in the schema YAML file.

**Rationale:** Descriptions are essential for documentation, lineage understanding, and team
collaboration. They appear in dbt docs and help stakeholders understand data assets.

**Detection:** Model entry exists but `description` field is missing or empty.

**Fix:**

```yaml
## Before
models:
  - name: dim_customers
    columns:
      - name: customer_id

## After
models:
  - name: dim_customers
    description: |
      Customer dimension containing customer attributes, contact info,
      and segmentation. Updated daily from CRM system.

      Source: CRM Database
      Owner: Analytics Team
    columns:
      - name: customer_id
```

---

#### YAML002: Primary Key Test Required

**Severity:** Error

**Description:** Columns that appear to be primary keys (ending in `_id`, `_key`, `_sk`) must have a
`dbt_constraints.primary_key` test.

**Rationale:** Primary key validation ensures data integrity. The `dbt_constraints` package creates
actual database constraints for validation.

**Detection:** Column name matches primary key pattern but lacks required test.

**Primary Key Patterns:**

- `*_id` (e.g., `customer_id`, `order_id`)
- `*_key` (e.g., `surrogate_key`, `natural_key`)
- `*_sk` (e.g., `customer_sk`)
- `id` (exact match)

**Fix:**

```yaml
## Before
columns:
  - name: customer_id
    description: "Unique customer identifier"

## After
columns:
  - name: customer_id
    description: "Unique customer identifier"
    data_type: integer
    tests:
      - dbt_constraints.primary_key
```

---

#### YAML003: Foreign Key Relationship Test

**Severity:** Warning

**Description:** Columns that appear to be foreign keys should have a `relationships` or
`dbt_constraints.foreign_key` test.

**Rationale:** Relationship tests validate referential integrity between tables.

**Detection:** Column name matches foreign key pattern but lacks relationship test.

**Foreign Key Patterns:**

- `fk_*` (e.g., `fk_customer`)
- `*_fk` (e.g., `customer_fk`)

**Fix:**

```yaml
## Before
columns:
  - name: fk_customer_id
    description: "Reference to customer"

## After
columns:
  - name: fk_customer_id
    description: "Reference to customer"
    tests:
      - relationships:
          to: ref('dim_customers')
          field: customer_id
```

---

#### YAML004: Column Description

**Severity:** Warning

**Description:** All columns should have descriptions.

**Rationale:** Column descriptions improve documentation and make data assets more discoverable.

**Fix:**

```yaml
## Before
columns:
  - name: signup_date

## After
columns:
  - name: signup_date
    description: "Date the customer signed up for service"
```

---

#### YAML005: Model Naming Convention

**Severity:** Error

**Description:** Model names must follow layer-specific naming conventions.

**Conventions by Layer:**

| Layer               | Prefix                          | Pattern                       | Example                      |
| ------------------- | ------------------------------- | ----------------------------- | ---------------------------- |
| Bronze/Staging      | `stg_`                          | `stg_{source}__{table}`       | `stg_sqlserver__customers`   |
| Silver/Intermediate | `int_`, `lookup_`               | `int_{entity}__{description}` | `int_customers__with_orders` |
| Gold/Mart           | `dim_`, `fct_`, `mart_`, `agg_` | `dim_{entity}`                | `dim_customers`              |

**Fix:**

```yaml
## Before (in gold layer)
models:
  - name: customers

## After
models:
  - name: dim_customers
```

---

#### YAML006: Column Data Type

**Severity:** Warning

**Description:** All columns should have `data_type` specified.

**Rationale:** Explicit data types improve documentation and enable contract testing.

**Fix:**

```yaml
## Before
columns:
  - name: amount
    description: "Order amount"

## After
columns:
  - name: amount
    description: "Order amount in USD"
    data_type: number(18,2)
```

---

### SQL Model Rules

#### SQL001: Config Block

**Severity:** Warning

**Description:** Models should have a config block specifying materialization.

**Rationale:** Explicit configuration makes materialization strategy clear and enables per-model
customization.

**Fix:**

```sql
-- Before
select * from {{ ref('stg_customers') }}

-- After
{{ config(
    materialized='table',
    tags=['gold', 'customer']
) }}

select * from {{ ref('stg_customers') }}
```

---

#### SQL002: CTE Pattern

**Severity:** Warning

**Description:** Models should use the standard CTE pattern for readability.

**Pattern:**

1. Import CTEs - Reference source data
2. Logical CTEs - Apply transformations
3. Final CTE - Prepare output
4. Final SELECT from final CTE

**Fix:**

```sql
-- Before
select
    c.customer_id,
    c.customer_name,
    count(o.order_id) as order_count
from {{ ref('stg_customers') }} c
left join {{ ref('stg_orders') }} o on c.customer_id = o.customer_id
group by 1, 2

-- After
with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customer_orders as (
    select
        c.customer_id,
        c.customer_name,
        count(o.order_id) as order_count
    from customers c
    left join orders o on c.customer_id = o.customer_id
    group by c.customer_id, c.customer_name
),

final as (
    select
        customer_id,
        customer_name,
        order_count
    from customer_orders
)

select * from final
```

---

#### SQL003: No SELECT \* in Final Output

**Severity:** Error

**Description:** The final query should explicitly list columns, not use `SELECT *`.

**Rationale:** Explicit columns make the contract clear, prevent accidental exposure of new columns,
and improve query performance.

**Exception:** `SELECT * FROM final` is acceptable when `final` CTE explicitly lists columns.

**Fix:**

```sql
-- Before (problematic)
select * from {{ ref('stg_customers') }}

-- After
select
    customer_id,
    customer_name,
    email,
    signup_date
from {{ ref('stg_customers') }}
```

---

#### SQL004: Use ref() and source()

**Severity:** Error

**Description:** All table references must use `{{ ref() }}` or `{{ source() }}`, not hardcoded
table names.

**Rationale:** Using ref() and source() enables:

- Automatic dependency tracking
- Environment-aware table resolution
- Proper lineage documentation

**Detection:** Pattern `FROM schema.table` or `JOIN database.schema.table` without Jinja braces.

**Fix:**

```sql
-- Before
select * from raw_data.customers

-- After (for source tables)
select * from {{ source('raw_data', 'customers') }}

-- After (for dbt models)
select * from {{ ref('stg_customers') }}
```

---

#### SQL005: Migration Header Comment

**Severity:** Warning

**Description:** Migrated models should include a header comment documenting the original source and
conversion notes.

**Detection:** Model contains migration indicators but lacks proper header.

**Required Header Elements:**

- Original object name and schema
- Source platform
- Migration date
- Conversion notes
- Breaking changes (if any)

**Template:**

```sql
/* Original Object: {schema}.{object_name}
   Source Platform: {SQL Server|Oracle|Teradata|etc.}
   Original Type: {Stored Procedure|View|Function}
   Migration Date: YYYY-MM-DD

   Conversion Notes:
   - Replaced ISNULL() with COALESCE()
   - Converted TOP to LIMIT
   - Removed NOLOCK hints

   Breaking Changes:
   - Output column 'old_name' renamed to 'new_name'
*/

{{ config(materialized='table') }}

-- Model implementation
```

---

#### SQL006: Snowflake-Incompatible Syntax

**Severity:** Error

**Description:** Model contains SQL syntax that is not compatible with Snowflake.

**Common Issues:**

| Pattern              | Platform   | Snowflake Equivalent     |
| -------------------- | ---------- | ------------------------ |
| `TOP N`              | SQL Server | `LIMIT N`                |
| `ISNULL(a, b)`       | SQL Server | `COALESCE(a, b)`         |
| `GETDATE()`          | SQL Server | `CURRENT_TIMESTAMP()`    |
| `LEN(s)`             | SQL Server | `LENGTH(s)`              |
| `CHARINDEX(a, b)`    | SQL Server | `POSITION(a IN b)`       |
| `CONVERT(type, val)` | SQL Server | `CAST(val AS type)`      |
| `WITH (NOLOCK)`      | SQL Server | (remove)                 |
| `@@ROWCOUNT`         | SQL Server | (use different approach) |
| `ROWNUM`             | Oracle     | `ROW_NUMBER() OVER()`    |
| `DECODE(...)`        | Oracle     | `CASE WHEN...`           |
| `CONNECT BY`         | Oracle     | Recursive CTE            |
| `SYSDATE`            | Oracle     | `CURRENT_DATE()`         |
| `SEL`                | Teradata   | `SELECT`                 |
| Backticks            | MySQL      | Double quotes            |

**Fix Examples:**

```sql
-- SQL Server Before
SELECT TOP 100 *
FROM customers WITH (NOLOCK)
WHERE ISNULL(email, '') = ''
  AND GETDATE() > signup_date

-- Snowflake After
SELECT *
FROM customers
WHERE COALESCE(email, '') = ''
  AND CURRENT_TIMESTAMP() > signup_date
LIMIT 100
```

---

## Anti-Patterns to Detect

### Common Anti-Patterns

#### 1. Direct Source References

**Problem:** Using hardcoded table names instead of `source()` or `ref()`.

**Impact:** Breaks dependency tracking, environment portability, and lineage.

#### 2. Generic Column Names

**Problem:** Columns named `col1`, `field1`, `temp`, etc.

**Impact:** Poor documentation, confusing for consumers.

#### 3. Mixed Naming Conventions

**Problem:** Inconsistent casing or naming patterns within a model.

**Impact:** Confusion, maintenance difficulty.

#### 4. Missing Tests on Key Columns

**Problem:** Primary/foreign keys without uniqueness or relationship tests.

**Impact:** Data quality issues may go undetected.

#### 5. Overly Complex Models

**Problem:** Models with excessive CTEs, complex logic, or doing too much.

**Impact:** Hard to maintain, test, and understand.

#### 6. Platform-Specific Syntax

**Problem:** SQL syntax from source database that won't work in Snowflake.

**Impact:** Runtime errors, compilation failures.

---

## Hook Integration

### Validation Hook Configuration

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
            "command": "python3 .claude/hooks/dbt-validation/validate_file.py \"$FILE_PATH\"",
            "timeout": 30000
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/dbt-validation/validate_file.py \"$FILE_PATH\"",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

### Exit Codes

- **Exit 0**: Validation passed (or file not in scope)
- **Exit 1**: Validation failed with errors

Warnings are reported but don't cause exit code 1.

### File Scope

Validation runs only on files matching:

- `models/**/_models.yml` - Schema YAML validation
- `models/**/_sources.yml` - Source YAML validation
- `models/**/*.sql` - SQL model validation

Other files are skipped (exit 0).

---

## Validation Scripts

Validation is implemented in `.claude/hooks/dbt-validation/`:

| Script                        | Purpose                                      |
| ----------------------------- | -------------------------------------------- |
| `validate_file.py`            | Entry point, routes to appropriate validator |
| `validate_schema_yaml.py`     | YAML rule validation                         |
| `validate_dbt_model.py`       | SQL rule validation                          |
| `check_migration_status.py`   | Cross-validation and reporting               |
| `rules/naming_conventions.py` | Naming convention checks                     |
| `rules/cte_patterns.py`       | CTE structure validation                     |
| `rules/snowflake_syntax.py`   | Platform syntax detection                    |

---

## Related Skills

- $dbt-migration - Migration workflow
- $dbt-testing - Test strategies
- $dbt-architecture - Naming conventions
- $dbt-modeling - CTE patterns
