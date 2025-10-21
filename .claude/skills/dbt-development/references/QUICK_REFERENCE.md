# dbt Quick Reference

## Essential Commands

**Official dbt Documentation**: [dbt Command Reference](https://docs.getdbt.com/reference/dbt-commands)

### Setup & Installation
```bash
dbt deps              # Install dbt packages
dbt debug             # Test connection
```

### Building Models
```bash
dbt build             # Run + test everything
dbt build --full-refresh  # Rebuild incremental models
dbt run               # Run all models
dbt test              # Test all models
```

### Model Selection
```bash
# Specific model
dbt run --select model_name

# Model + upstream dependencies
dbt run --select +model_name

# Model + downstream dependencies  
dbt run --select model_name+

# Model + all dependencies
dbt run --select +model_name+

# By tag
dbt run --select tag:bronze
dbt run --select tag:gold tag:critical

# By folder
dbt run --select bronze.subfolder

# Exclude models
dbt run --exclude tag:deprecated
```

### Testing
```bash
dbt test              # All tests
dbt test --select dim_customers  # Specific model
dbt test --select test_type:generic  # By type
dbt test --store-failures  # Store failures for analysis
```

### Documentation
```bash
dbt docs generate     # Generate docs
dbt docs serve        # Serve docs locally (port 8080)
dbt docs serve --port 8001  # Custom port
```

### Debugging
```bash
dbt compile --select model_name  # Check SQL compilation
dbt run --select model_name --debug  # Verbose logging
dbt list              # List available models
```

---

## Medallion Architecture Patterns

### Bronze Layer (Staging)
```sql
-- models/bronze/stg_customers.sql
{{ config(materialized='ephemeral') }}

select
    c_custkey as customer_id,
    c_name as customer_name
from {{ source('tpc_h', 'customer') }}
```

### Silver Layer (Intermediate)
```sql
-- models/silver/int_customers__enriched.sql
{{ config(materialized='ephemeral') }}

with customers as (
    select * from {{ ref('stg_customers') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
)

select
    c.customer_id,
    count(o.order_id) as order_count
from customers c
left join orders o on c.customer_id = o.customer_id
group by c.customer_id
```

### Gold Layer (Marts)
```sql
-- models/gold/dim_customers.sql
{{ config(materialized='table') }}

select * from {{ ref('int_customers__enriched') }}
```

---

## Incremental Models

```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    cluster_by=['order_date']
) }}

select * from {{ ref('stg_orders') }}

{% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

---

## Testing Patterns

### Primary Key (dbt_constraints)
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
```

### Foreign Key (dbt_constraints)
```yaml
models:
  - name: fct_orders
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_customers')
              pk_column_name: customer_id
```

### Generic Tests
```yaml
columns:
  - name: customer_email
    tests:
      - dbt_constraints.unique_key
      - accepted_values:
          values: ['active', 'inactive']
```

---

## Jinja Patterns

**Official dbt Documentation**: [Jinja & Macros](https://docs.getdbt.com/docs/build/jinja-macros)

### Loops
```sql
{% for status in ['pending', 'shipped', 'delivered'] %}
    sum(case when status = '{{ status }}' then 1 else 0 end) as {{ status }}_count
    {%- if not loop.last -%},{%- endif %}
{% endfor %}
```

### Conditionals
```sql
{% if target.name == 'prod' %}
    where is_active = true
{% else %}
    limit 1000
{% endif %}
```

### Macros
```sql
{% macro cents_to_dollars(column_name) %}
    round({{ column_name }} / 100.0, 2)
{% endmacro %}

-- Usage:
select {{ cents_to_dollars('amount_cents') }} as amount_dollars
from {{ ref('stg_payments') }}
```

### Built-in Jinja Variables
```sql
{{ target.name }}           -- 'dev', 'prod', etc.
{{ run_started_at }}        -- Run start timestamp
{{ invocation_id }}         -- Unique run identifier
{{ this }}                  -- Current model reference
{{ flags.FULL_REFRESH }}    -- True if --full-refresh
```

---

## Configuration Patterns

### Folder-Level Configuration
```yaml
# dbt_project.yml
models:
  your_project:
    bronze:
      +materialized: ephemeral
      +tags: ["bronze", "staging"]
    silver:
      +materialized: ephemeral
      +tags: ["silver"]
    gold:
      +materialized: table
      +tags: ["gold", "marts"]
```

### Model-Level Configuration
```sql
{{ config(
    materialized='incremental',
    unique_key='customer_id',
    tags=['daily', 'critical'],
    cluster_by=['order_date']
) }}
```

---

## dbt_utils Functions

**Official dbt_utils Documentation**: [dbt_utils](https://github.com/dbt-labs/dbt-utils)

```sql
-- Generate surrogate key
{{ dbt_utils.generate_surrogate_key(['col1', 'col2']) }}

-- Get column values
{{ dbt_utils.get_column_values(ref('model'), 'column') }}

-- Date spine
{{ dbt_utils.date_spine(
    datepart="day",
    start_date="to_date('01/01/2020', 'mm/dd/yyyy')",
    end_date="current_date()"
) }}
```

---

## Naming Conventions

### Models
- **Staging**: `stg_{source}__{table}`
- **Intermediate**: `int_{entity}__{description}`
- **Dimensions**: `dim_{entity}`
- **Facts**: `fct_{process}`

### Columns
- **IDs**: `{entity}_id`
- **Booleans**: `is_{condition}` or `has_{attribute}`
- **Dates**: `{event}_date` or `{event}_at`
- **Counts**: `{metric}_count`
- **Amounts**: `{metric}_amount`

See `NAMING_CONVENTIONS.md` for complete standards.

---

## Project-Specific Variables

```yaml
# dbt_project.yml
vars:
  prune_days: 2
  default_integration_key: integration_id
```

**Usage**:
```sql
where order_date >= dateadd(day, -{{ var('prune_days') }}, current_date())
```

---

## Common Commands Cheatsheet

| Task | Command |
|------|---------|
| Build one model | `dbt build --select model_name` |
| Build with dependencies | `dbt build --select +model_name+` |
| Full refresh | `dbt build --full-refresh` |
| Test one model | `dbt test --select model_name` |
| Run by tag | `dbt run --select tag:bronze` |
| Generate docs | `dbt docs generate` |
| Debug connection | `dbt debug` |
| Clean project | `dbt clean` |

---

## Troubleshooting

### Connection Issues
```bash
dbt debug  # Verify credentials and connection
```

### Compilation Errors
```bash
dbt compile --select modelname  # Check SQL compilation
cat target/compiled/your_project/models/path/to/modelname.sql
```

### Performance Issues
```bash
dbt run --select modelname --debug  # Verbose output
# Check Snowflake query history for execution plans
```

---

## Related Documentation

- [Official dbt Docs: Command Reference](https://docs.getdbt.com/reference/dbt-commands)
- [Official dbt Docs: Jinja & Macros](https://docs.getdbt.com/docs/build/jinja-macros)
- [dbt_utils Package](https://github.com/dbt-labs/dbt-utils)
- `PROJECT_STRUCTURE.md` - Folder organization
- `MATERIALIZATIONS.md` - Choosing materializations
- `TESTING_STRATEGY.md` - Test patterns
