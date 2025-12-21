---
name: dbt-commands
description:
  dbt command-line operations, model selection syntax, Jinja patterns, troubleshooting, and
  debugging. Use this skill when running dbt commands, selecting specific models, debugging
  compilation errors, using Jinja macros, or troubleshooting dbt execution issues.
---

# dbt Commands & Operations

## Purpose

Transform AI agents into experts on dbt command-line operations, model selection patterns, Jinja
templating, and troubleshooting techniques for efficient dbt development and debugging.

## When to Use This Skill

Activate this skill when users ask about:

- Running dbt commands (build, run, test, compile)
- Model selection syntax and patterns
- Debugging compilation or execution errors
- Using Jinja macros and templates
- Troubleshooting dbt issues
- Command-line flags and options
- Generating and serving documentation
- Understanding dbt command output

**Official dbt Documentation**:
[dbt Command Reference](https://docs.getdbt.com/reference/dbt-commands)

---

## Essential Commands

### Setup & Installation

```bash
# Install dbt packages
dbt deps

# Test connection and configuration
dbt debug

# Clean compiled files and logs
dbt clean
```

---

### Building Models

```bash
# Build everything (run + test) - RECOMMENDED
dbt build

# Build with full refresh of incremental models
dbt build --full-refresh

# Run all models (no tests)
dbt run

# Run and test separately
dbt run
dbt test
```

**Best Practice**: Use `dbt build` instead of separate `run` + `test` commands.

---

## Model Selection Syntax

### Basic Selection

```bash
# Specific model
dbt run --select model_name
dbt run --select dim_customers

# Multiple models
dbt run --select dim_customers fct_orders dim_products
```

---

### Dependency Selection

```bash
# Model + upstream dependencies (parents)
dbt run --select +model_name
dbt run --select +dim_customers

# Model + downstream dependencies (children)
dbt run --select model_name+
dbt run --select dim_customers+

# Model + all dependencies (both directions)
dbt run --select +model_name+
dbt run --select +dim_customers+
```

**Visualization**:

```
+model_name    = model + all parents
model_name+    = model + all children
+model_name+   = model + all parents + all children
```

---

### Selection by Tag

```bash
# Single tag
dbt run --select tag:bronze
dbt run --select tag:gold

# Multiple tags (AND logic - must have both)
dbt run --select tag:gold tag:critical

# Multiple tags (OR logic - has either)
dbt run --select tag:gold,tag:silver
```

**Common tags:**

- `tag:bronze` - All staging models
- `tag:silver` - All intermediate models
- `tag:gold` - All mart models

---

### Selection by Folder

```bash
# All models in folder
dbt run --select bronze
dbt run --select gold

# Subfolder
dbt run --select bronze.crawl
dbt run --select gold.run

# Multiple folders
dbt run --select bronze silver
```

---

### Exclude Models

```bash
# Exclude specific models
dbt run --exclude model_name

# Exclude by tag
dbt run --exclude tag:deprecated

# Exclude folder
dbt run --exclude bronze

# Complex: Run gold, but exclude certain models
dbt run --select tag:gold --exclude fct_large_table
```

---

### Advanced Selection

```bash
# Models modified in current git branch
dbt run --select state:modified --state ./prod-manifest/

# Models by package
dbt run --select package:dbt_utils

# Models by resource type
dbt test --select test_type:generic
dbt test --select test_type:singular

# Intersection (models matching multiple criteria)
dbt run --select tag:gold,tag:critical  # Has gold OR critical
```

**Official dbt Docs**:
[Node Selection Syntax](https://docs.getdbt.com/reference/node-selection/syntax)

---

## Testing Commands

```bash
# Run all tests
dbt test

# Test specific model
dbt test --select dim_customers

# Test specific column
dbt test --select dim_customers,column:customer_id

# Test by type
dbt test --select test_type:generic    # Generic tests only
dbt test --select test_type:singular   # Singular tests only

# Test with dependencies
dbt test --select +dim_customers+

# Store test failures for analysis
dbt test --store-failures

# Test by layer
dbt test --select tag:gold
```

---

## Documentation Commands

```bash
# Generate documentation
dbt docs generate

# Serve documentation locally (default port 8080)
dbt docs serve

# Custom port
dbt docs serve --port 8001

# Generate static HTML (for hosting)
dbt docs generate --static
```

**Accessing docs**: Navigate to `http://localhost:8080` after running `dbt docs serve`

---

## Debugging Commands

```bash
# Check SQL compilation without running
dbt compile --select model_name

# View compiled SQL
cat target/compiled/your_project/models/path/to/model.sql

# Run with verbose logging
dbt run --select model_name --debug

# Run with detailed log level
dbt run --select model_name --log-level debug

# List all models (useful for understanding project)
dbt list

# List models with selection
dbt list --select tag:gold

# Show dependency graph
dbt list --select +dim_customers+ --output path
```

---

## Jinja Patterns

**Official dbt Documentation**: [Jinja & Macros](https://docs.getdbt.com/docs/build/jinja-macros)

### Loops

```sql
-- Generate columns for each status
{% for status in ['pending', 'shipped', 'delivered', 'cancelled'] %}
    sum(case when status = '{{ status }}' then 1 else 0 end) as {{ status }}_count
    {%- if not loop.last -%},{%- endif %}
{% endfor %}
```

**Output:**

```sql
sum(case when status = 'pending' then 1 else 0 end) as pending_count,
sum(case when status = 'shipped' then 1 else 0 end) as shipped_count,
sum(case when status = 'delivered' then 1 else 0 end) as delivered_count,
sum(case when status = 'cancelled' then 1 else 0 end) as cancelled_count
```

---

### Conditionals

```sql
{% if target.name == 'prod' %}
    where is_active = true
{% else %}
    where order_date >= dateadd(day, -7, current_date())
    limit 1000
{% endif %}
```

---

### Macros

**Define macro:**

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name) %}
    round({{ column_name }} / 100.0, 2)
{% endmacro %}
```

**Use macro:**

```sql
select
    {{ cents_to_dollars('amount_cents') }} as amount_dollars
from {{ ref('stg_payments') }}
```

---

### Built-in Jinja Variables

```sql
{{ target.name }}           -- 'dev', 'prod', etc.
{{ target.schema }}         -- Current schema
{{ target.database }}       -- Current database
{{ run_started_at }}        -- Run start timestamp
{{ invocation_id }}         -- Unique run identifier
{{ this }}                  -- Current model reference
{{ flags.FULL_REFRESH }}    -- True if --full-refresh flag used
```

**Example usage:**

```sql
-- Add metadata
select
    *,
    '{{ target.name }}' as target_environment,
    '{{ run_started_at }}' as dbt_run_timestamp,
    '{{ invocation_id }}' as dbt_invocation_id
from {{ ref('stg_customers') }}
```

---

### Variables

**Define in dbt_project.yml:**

```yaml
vars:
  lookback_days: 7
  default_currency: "USD"
```

**Use in models:**

```sql
select *
from {{ ref('stg_orders') }}
where order_date >= dateadd(day, -{{ var('lookback_days') }}, current_date())
```

**Override via command line:**

```bash
dbt run --vars '{"lookback_days": 30}'
```

---

## dbt_utils Functions

**Official dbt_utils Documentation**: [dbt_utils](https://github.com/dbt-labs/dbt-utils)

```sql
-- Generate surrogate key
{{ dbt_utils.generate_surrogate_key(['customer_id', 'order_id']) }}

-- Get column values as list
{{ dbt_utils.get_column_values(ref('dim_products'), 'product_category') }}

-- Date spine (generate date series)
{{ dbt_utils.date_spine(
    datepart="day",
    start_date="to_date('2020-01-01', 'yyyy-mm-dd')",
    end_date="current_date()"
) }}

-- Union tables
{{ dbt_utils.union_relations(
    relations=[ref('orders_2023'), ref('orders_2024')]
) }}

-- Star (select all except certain columns)
select
    {{ dbt_utils.star(ref('stg_customers'), except=['internal_id', 'ssn']) }}
from {{ ref('stg_customers') }}
```

---

## Troubleshooting

### Connection Issues

**Symptom**: `dbt debug` fails

**Solution:**

```bash
# Verify connection
dbt debug

# Check profiles.yml location
ls ~/.dbt/profiles.yml

# Verify environment variables
echo $SNOWFLAKE_ACCOUNT
echo $DBT_ENV_SECRET_SNOWFLAKE_PAT
```

---

### Compilation Errors

**Symptom**: Model fails to compile with Jinja/SQL errors

**Solution:**

```bash
# Compile without running to see SQL
dbt compile --select modelname

# View compiled SQL
cat target/compiled/your_project/models/path/to/modelname.sql

# Check for syntax errors
dbt run --select modelname --debug
```

**Common issues:**

- Missing `{% endif %}` or `{% endfor %}`
- Unclosed Jinja blocks
- Invalid ref() or source() references

---

### Execution Errors

**Symptom**: Model compiles but fails to run

**Solution:**

```bash
# Run with verbose logging
dbt run --select modelname --debug

# Check Snowflake query history
# (Query History tab in Snowflake UI)

# View full error
cat logs/dbt.log | grep ERROR
cat logs/dbt.log | grep modelname
```

**Common issues:**

- Invalid SQL syntax
- Division by zero
- Data type mismatches
- Permission errors

---

### Dependency Errors

**Symptom**: Model can't find upstream dependencies

**Solution:**

```bash
# List dependencies
dbt list --select +modelname

# Verify model exists
dbt list --select upstream_model_name

# Check ref() spelling
dbt compile --select modelname
```

---

### Test Failures

**Symptom**: Tests fail unexpectedly

**Solution:**

```bash
# Store failures for analysis
dbt test --select modelname --store-failures

# Query failure records
# select * from dbt_test_failures.test_name

# Run single test
dbt test --select modelname,column:column_name

# Check test definition
cat models/path/_models.yml
```

---

### Performance Issues

**Symptom**: Model runs very slowly

**Solution:**

```bash
# Run with debug logging
dbt run --select modelname --debug --log-level debug

# Check compiled SQL
cat target/compiled/your_project/models/path/to/modelname.sql

# Profile in Snowflake
# Query History → Query Profile tab

# Check for:
# - Missing WHERE clauses in incremental models
# - Inefficient joins
# - Missing clustering keys
```

---

## Common Commands Cheatsheet

| Task                     | Command                           |
| ------------------------ | --------------------------------- |
| Build one model          | `dbt build --select model_name`   |
| Build with dependencies  | `dbt build --select +model_name+` |
| Full refresh incremental | `dbt build --full-refresh`        |
| Test one model           | `dbt test --select model_name`    |
| Run by tag               | `dbt run --select tag:bronze`     |
| Generate docs            | `dbt docs generate`               |
| Debug connection         | `dbt debug`                       |
| Clean project            | `dbt clean`                       |
| Compile without running  | `dbt compile --select model_name` |
| List models              | `dbt list`                        |

---

## Target-Specific Execution

```bash
# Run against dev target (default)
dbt run --target dev

# Run against production target
dbt run --target prod

# Build specific models in prod
dbt build --select tag:gold --target prod
```

**Define targets in ~/.dbt/profiles.yml:**

```yaml
your_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      schema: dbt_dev
      # ... other settings

    prod:
      type: snowflake
      schema: analytics
      # ... other settings
```

---

## Helping Users with Commands

### Strategy for Assisting Users

When users ask about dbt commands:

1. **Understand the goal**: What are they trying to accomplish?
2. **Recommend appropriate command**: build vs run vs test
3. **Provide selection syntax**: Specific models, tags, or folders
4. **Include relevant flags**: --full-refresh, --debug, --store-failures
5. **Show expected output**: What success looks like
6. **Offer troubleshooting**: Common issues and solutions

### Common User Questions

**"How do I run just this model?"**

```bash
dbt build --select model_name
```

**"How do I run this model and everything it depends on?"**

```bash
dbt build --select +model_name
```

**"How do I test all my gold layer models?"**

```bash
dbt test --select tag:gold
```

**"How do I debug why my model won't compile?"**

```bash
dbt compile --select model_name --debug
cat target/compiled/your_project/models/path/to/model.sql
```

**"How do I see what SQL dbt generated?"**

```bash
dbt compile --select model_name
cat target/compiled/your_project/models/path/to/model.sql
```

---

## Related Official Documentation

- [dbt Docs: Command Reference](https://docs.getdbt.com/reference/dbt-commands)
- [dbt Docs: Node Selection Syntax](https://docs.getdbt.com/reference/node-selection/syntax)
- [dbt Docs: Jinja & Macros](https://docs.getdbt.com/docs/build/jinja-macros)
- [dbt_utils Package](https://github.com/dbt-labs/dbt-utils)

---

**Goal**: Transform AI agents into expert dbt operators who efficiently execute commands, select
appropriate models, debug issues, and leverage Jinja patterns for dynamic SQL generation.
