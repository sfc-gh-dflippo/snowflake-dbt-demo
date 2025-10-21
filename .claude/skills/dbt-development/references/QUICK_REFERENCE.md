# dbt Quick Reference

## Essential Commands

### Setup & Installation
```bash
# Install dbt packages
dbt deps

# Test connection
dbt debug

# Initialize new project (interactive)
dbt init
```

### Building Models
```bash
# Build everything (run + test)
dbt build

# Full refresh (rebuild incremental models)
dbt build --full-refresh

# Run all models
dbt run

# Test all models
dbt test

# Load seed files
dbt seed
```

### Model Selection Syntax
```bash
# Run specific model
dbt run --select model_name
dbt run --select dim_customers

# Run model and all upstream dependencies
dbt run --select +model_name
dbt run --select +dim_customers

# Run model and all downstream dependencies  
dbt run --select model_name+
dbt run --select dim_customers+

# Run model and ALL dependencies (up and down)
dbt run --select +model_name+
dbt run --select +dim_customers+

# Run model, dependencies, and dependencies of dependencies
dbt run --select @model_name
dbt run --select @dim_customers
```

### Selection by Attribute
```bash
# Run by tag
dbt run --select tag:bronze
dbt run --select tag:gold tag:critical

# Run by folder
dbt run --select bronze.crawl
dbt run --select gold.dimensions

# Run by materialization
dbt run --select config.materialized:incremental

# Run by package
dbt run --select dbt_utils
```

### Excluding Models
```bash
# Run all except specific model
dbt run --exclude model_name

# Run all except tag
dbt run --exclude tag:deprecated

# Run all except folder
dbt run --exclude bronze.archive
```

### Testing
```bash
# Test everything
dbt test

# Test specific model
dbt test --select dim_customers

# Test by type
dbt test --select test_type:generic
dbt test --select test_type:singular

# Store test failures for analysis
dbt test --store-failures

# Test with specific severity
dbt test --select config.severity:error
```

### Documentation
```bash
# Generate documentation
dbt docs generate

# Generate static documentation (single HTML file)
dbt docs generate --static

# Serve documentation locally
dbt docs serve

# Serve on custom port
dbt docs serve --port 8001
```

### Compilation
```bash
# Compile models without running
dbt compile

# Compile specific model
dbt compile --select model_name

# View compiled SQL
cat target/compiled/your_project/models/model_name.sql
```

### Debugging
```bash
# Debug with verbose logging
dbt run --select model_name --debug

# Parse project only
dbt parse

# List available models
dbt list

# List available tests
dbt list --resource-type test

# Show model dependencies
dbt list --select +dim_customers+
```

### Environment & Targets
```bash
# Run against specific target
dbt run --target prod
dbt test --target staging

# Use specific profile
dbt run --profile my_profile

# Use specific profiles directory
dbt run --profiles-dir /path/to/profiles
```

### Cleaning
```bash
# Clean compiled files and logs
dbt clean

# Clean and rebuild
dbt clean && dbt deps && dbt build
```

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
),
final as (
    select
        c.customer_id,
        count(o.order_id) as order_count
    from customers c
    left join orders o on c.customer_id = o.customer_id
    group by c.customer_id
)
select * from final
```

### Gold Layer (Marts)
```sql
-- models/gold/dim_customers.sql
{{ config(materialized='table') }}

select * from {{ ref('int_customers__enriched') }}
```

## Incremental Models
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge'
) }}

select * from {{ ref('stg_orders') }}

{% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

## Testing Patterns

### Primary Key
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
```

### Foreign Key
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
      - not_null
      - unique
      - accepted_values:
          values: ['active', 'inactive']
```

### Singular Test
```sql
-- tests/singular/test_order_totals.sql
select *
from {{ ref('fct_orders') }}
where order_total < 0
```

## Jinja Patterns

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

select
    {{ cents_to_dollars('amount_cents') }} as amount_dollars
from {{ ref('stg_payments') }}
```

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
      +tags: ["silver", "intermediate"]
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

## Common dbt_utils Functions

```sql
-- Generate surrogate key
{{ dbt_utils.generate_surrogate_key(['col1', 'col2']) }}

-- Get column names
{{ dbt_utils.get_column_values(ref('model'), 'column') }}

-- Pivot data
{{ dbt_utils.pivot(
    column='status',
    values=dbt_utils.get_column_values(ref('orders'), 'status'),
    then_value='count(*)'
) }}

-- Union relations
{{ dbt_utils.union_relations(
    relations=[ref('orders_2020'), ref('orders_2021')]
) }}

-- Date spine
{{ dbt_utils.date_spine(
    datepart="day",
    start_date="to_date('01/01/2020', 'mm/dd/yyyy')",
    end_date="current_date()"
) }}
```

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

## Environment Variables

### profiles.yml
```yaml
your_project:
  target: dev
  outputs:
    dev:
      type: snowflake  # or bigquery, databricks, etc.
      account: "{{ env_var('DBT_ACCOUNT') }}"
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      database: "{{ env_var('DBT_DATABASE') }}"
      warehouse: "{{ env_var('DBT_WAREHOUSE') }}"
      schema: dev
```

### Using Variables
```bash
# Set variable for run
dbt run --vars '{"key": "value"}'

# Use in model
{{ var('key') }}
```

## Performance Tips

### Clustering
```sql
{{ config(
    materialized='table',
    cluster_by=['date_column', 'category']
) }}
```

### Partitioning
```sql
{{ config(
    materialized='incremental',
    partition_by={
        'field': 'order_date',
        'data_type': 'date'
    }
) }}
```

### Limiting Dev Queries
```sql
{{ limit_data_in_dev(column_name='created_at', dev_days_of_data=3) }}
```

## Troubleshooting Quick Fixes

### Connection Issues
```bash
# Verify connection
dbt debug

# Check profiles.yml path
echo $DBT_PROFILES_DIR
```

### Compilation Errors
```bash
# Compile to see generated SQL
dbt compile --select model_name

# View compiled model
cat target/compiled/your_project/models/model_name.sql
```

### Test Failures
```bash
# Run tests with failure storage
dbt test --store-failures

# Query failed tests
select * from dbt_test_failures.test_name
```

### Performance Issues
```bash
# Check compiled SQL
dbt compile --select model_name

# Run with timing info
dbt run --select model_name --debug
```

## Package Management

### packages.yml
```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]
  
  - package: Snowflake-Labs/dbt_constraints
    version: [">=0.8.0", "<1.0.0"]
  
  - package: calogica/dbt_expectations
    version: [">=0.10.0", "<1.0.0"]
  
  - git: https://github.com/org/repo.git
    revision: main
```

### Install Packages
```bash
# Install all packages
dbt deps

# Upgrade packages
dbt deps --upgrade
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-model

# Make changes and commit
git add models/
git commit -m "feat: add new customer dimension"

# Run tests before push
dbt build

# Push and create PR
git push origin feature/new-model
```

## CI/CD Commands

```bash
# Slim CI - only modified models
dbt build --select state:modified+ --state ./prod-artifacts/

# Test source freshness
dbt source freshness

# Generate and upload docs
dbt docs generate
```

## Common Patterns Cheatsheet

| Task | Command |
|------|---------|
| Build one model | `dbt build --select model_name` |
| Build with dependencies | `dbt build --select +model_name+` |
| Full refresh | `dbt build --full-refresh` |
| Test one model | `dbt test --select model_name` |
| Run by tag | `dbt run --select tag:bronze` |
| Run by folder | `dbt run --select bronze.crawl` |
| Exclude models | `dbt run --exclude tag:deprecated` |
| Generate docs | `dbt docs generate` |
| Debug connection | `dbt debug` |
| Clean project | `dbt clean` |

---

## Troubleshooting

### Connection Issues
```bash
# Verify credentials and connection
dbt debug

# Check profile configuration
cat ~/.dbt/profiles.yml

# Test specific target
dbt debug --target prod
```

### Compilation Errors
```bash
# Check SQL compilation
dbt compile --select modelname

# View compiled SQL
cat target/compiled/your_project/models/path/to/modelname.sql
```

### Runtime Debugging
```bash
# Verbose logging
dbt run --select modelname --log-level debug

# Check logs for errors
cat logs/dbt.log | grep ERROR

# Find specific model logs
cat logs/dbt.log | grep modelname
```

### Performance Issues
```bash
# Profile execution time
dbt run --select modelname --debug

# Check Snowflake query history
# Run in Snowflake:
select * from snowflake.account_usage.query_history 
where query_text ilike '%model_name%' 
order by start_time desc limit 10;
```

### Constraint Validation (dbt_constraints)
```bash
# Validate primary key constraint
dbt run-operation primary_key --args '{model_name: dim_customers}'

# Check constraint failures
dbt test --store-failures
select * from your_database.dbt_test__audit.failed_test_name;
```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `Could not find profile` | Check profiles.yml path and profile name in dbt_project.yml |
| `Compilation Error` | Run `dbt compile --select modelname` to see exact error |
| `Target database/schema not found` | Verify target configuration in profiles.yml |
| `Incremental model not updating` | Check `is_incremental()` logic and try `--full-refresh` |
| `Test failures` | Use `--store-failures` flag to examine failing rows |
| `Dependency cycle detected` | Check `ref()` calls for circular dependencies |

---

**Related Documentation:**
- `PROJECT_STRUCTURE.md` - Folder organization
- `MATERIALIZATIONS.md` - Choosing materializations
- `TESTING_STRATEGY.md` - Test patterns
- `INCREMENTAL_MODELS.md` - Incremental strategies

