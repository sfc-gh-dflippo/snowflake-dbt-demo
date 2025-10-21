# dbt Materializations Guide

## Choosing the Right Materialization

Materialization determines how dbt builds models in the warehouse. Choose based on model purpose, size, update frequency, and downstream dependencies.

## Materialization Decision Matrix

| Materialization | Use Case | Build Time | Storage | Query Speed | Freshness |
|-----------------|----------|------------|---------|-------------|-----------|
| **ephemeral** | Staging, reusable logic | Fast (CTE) | None | N/A | Real-time |
| **view** | Simple transforms, small data | Fast | Minimal | Slow | Real-time |
| **table** | Complex logic, frequently queried | Slow | High | Fast | Batch |
| **incremental** | Large datasets, append/merge | Fast | Medium | Fast | Near real-time |
| **dynamic_table** | Real-time streaming | N/A | High | Fast | Real-time |

## Ephemeral Materialization

**When to Use:**
- ✅ Staging models (bronze layer)
- ✅ Reusable intermediate logic (silver layer)
- ✅ Models that are always referenced by other models
- ✅ Small, fast transformations

**Configuration:**
```sql
{{ config(materialized='ephemeral') }}

select
    customer_id,
    customer_name,
    customer_email
from {{ source('crm', 'customers') }}
```

**How It Works:**
- Compiled as CTE in downstream models
- No physical table or view created
- Fastest for small transformations
- Reduces storage footprint

**Best Practices:**
- Use for all staging models (bronze layer)
- Use for intermediate models that are always joined
- Avoid for models queried directly
- Keep logic simple (no complex joins or aggregations)

**Example Use Cases:**
- `stg_customers` - One-to-one source relationship
- `stg_orders` - Clean and standardize raw orders
- `int_customer_base` - Reusable customer logic

---

## View Materialization

**When to Use:**
- ✅ Simple transformations
- ✅ Always need fresh data
- ✅ Lightweight aggregations
- ✅ Development/testing

**Configuration:**
```sql
{{ config(materialized='view') }}

select
    customer_id,
    count(*) as order_count
from {{ ref('stg_orders') }}
group by customer_id
```

**How It Works:**
- Creates a database view
- Query runs every time view is queried
- No data stored (minimal storage)
- Always returns latest data

**Best Practices:**
- Use when freshness is critical
- Avoid for complex queries (slow performance)
- Good for lightweight aggregations
- Not recommended for production fact tables

**Example Use Cases:**
- Simple customer summaries
- Lightweight reference data
- Development prototypes

---

## Table Materialization

**When to Use:**
- ✅ Complex transformations
- ✅ Frequently queried models
- ✅ Dimension tables (gold layer)
- ✅ Models with joins and aggregations

**Configuration:**
```sql
{{ config(
    materialized='table',
    cluster_by=['order_date']  -- Optional: for large tables
) }}

with customer_metrics as (
    select
        customer_id,
        count(*) as lifetime_orders,
        sum(total_price) as lifetime_value,
        min(order_date) as first_order_date
    from {{ ref('stg_orders') }}
    group by customer_id
)

select * from customer_metrics
```

**How It Works:**
- Drops and recreates table on every run
- Stores data physically in warehouse
- Fast query performance
- Full refresh on each run

**Best Practices:**
- Use for dimension tables
- Use for complex business logic
- Add clustering keys for large tables
- Consider incremental for very large tables

**Performance Optimizations:**
```sql
{{ config(
    materialized='table',
    cluster_by=['date_column', 'customer_id'],
    snowflake_warehouse='TRANSFORM_WH'
) }}
```

**Example Use Cases:**
- `dim_customers` - Customer dimension
- `dim_products` - Product catalog
- `int_fx_rates__daily` - Complex FX rate calculations

---

## Incremental Materialization

**When to Use:**
- ✅ Large fact tables (millions+ rows)
- ✅ Append-only or merge update patterns
- ✅ Time-series data
- ✅ Event logs and clickstreams

**Basic Configuration:**
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail'
) }}

select
    order_id,
    customer_id,
    order_date,
    order_amount,
    current_timestamp() as dbt_updated_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
    -- Only process new/updated records
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

**How It Works:**
- First run: Full table load
- Subsequent runs: Insert/update only new records
- Uses unique_key for merge/delete+insert
- Significantly faster than full refresh

**Incremental Strategies:**

### 1. Append (Default)
Best for immutable event data:
```sql
{{ config(
    materialized='incremental',
    incremental_strategy='append'
) }}

select * from {{ ref('stg_events') }}
{% if is_incremental() %}
    where event_timestamp > (select max(event_timestamp) from {{ this }})
{% endif %}
```

### 2. Merge (Most Common)
Best for updateable records:
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    merge_exclude_columns=['dbt_inserted_at']
) }}

select
    order_id,
    order_status,  -- Can be updated
    order_amount,  -- Can be updated
    current_timestamp() as dbt_updated_at,
    {% if not is_incremental() %}
        current_timestamp() as dbt_inserted_at
    {% else %}
        dbt_inserted_at  -- Preserve original insert time
    {% endif %}
from {{ ref('stg_orders') }}

{% if is_incremental() %}
    where dbt_updated_at > (select max(dbt_updated_at) from {{ this }})
{% endif %}
```

### 3. Delete+Insert
Best for partitioned data:
```sql
{{ config(
    materialized='incremental',
    unique_key='order_date',
    incremental_strategy='delete+insert'
) }}

select * from {{ ref('stg_daily_summary') }}
{% if is_incremental() %}
    where order_date >= dateadd(day, -7, current_date())
{% endif %}
```

**Best Practices:**
- Always define unique_key for merge strategy
- Use merge_exclude_columns to preserve metadata
- Add clustering keys for query performance
- Test with small data before full refresh
- Monitor incremental logic carefully

**Performance Optimizations:**
```sql
{{ config(
    materialized='incremental',
    unique_key='order_line_id',
    cluster_by=['order_date', 'customer_id'],
    incremental_strategy='merge',
    on_schema_change='fail'
) }}
```

**Common Patterns:**

**Time-based incremental:**
```sql
{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

**Date-based incremental:**
```sql
{% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

**Safe fallback incremental:**
```sql
{% if is_incremental() %}
    where updated_at > (
        select coalesce(max(updated_at), '1900-01-01'::timestamp)
        from {{ this }}
    )
{% endif %}
```

**Example Use Cases:**
- `fct_orders` - Order fact table
- `fct_clickstream` - Web event logs
- `fct_transactions` - Financial transactions

---

## Dynamic Table Materialization

**When to Use:**
- ✅ Real-time streaming pipelines
- ✅ Low-latency analytics
- ✅ Event-driven architectures
- ✅ Snowflake-specific optimization

**Configuration:**
```sql
{{ config(
    materialized='dynamic_table',
    target_lag='1 hour',
    snowflake_warehouse='STREAMING_WH',
    on_configuration_change='apply'
) }}

select
    order_id,
    customer_id,
    order_date,
    sum(order_amount) as total_amount
from {{ ref('stg_orders') }}
group by order_id, customer_id, order_date
```

**How It Works:**
- Snowflake automatically refreshes based on target_lag
- More efficient than incremental for real-time needs
- Native Snowflake feature (not available on all platforms)
- Continuous refresh without dbt runs

**Best Practices:**
- Use for time-sensitive analytics
- Set appropriate target_lag (minutes to hours)
- Requires Snowflake Enterprise or higher
- More expensive than traditional incremental

**Example Use Cases:**
- Real-time dashboards
- Streaming data pipelines
- Event-driven analytics

---

## Choosing by Layer

### Bronze Layer (Staging)
**Recommendation:** `ephemeral`
- One-to-one source relationships
- Fast compilation as CTEs
- No storage overhead
- Always referenced by downstream models

```sql
-- models/bronze/stg_customers.sql
{{ config(materialized='ephemeral') }}

select
    c_custkey as customer_id,
    c_name as customer_name,
    c_address as customer_address
from {{ source('tpc_h', 'customer') }}
```

### Silver Layer (Intermediate)
**Recommendation:** `ephemeral` (reusable logic) or `table` (complex transformations)

**Ephemeral for reusable logic:**
```sql
-- models/silver/int_customer_base.sql
{{ config(materialized='ephemeral') }}

select
    customer_id,
    customer_name,
    -- Shared business logic
from {{ ref('stg_customers') }}
```

**Table for complex transformations:**
```sql
-- models/silver/int_fx_rates__daily.sql
{{ config(materialized='table') }}

with daily_rates as (
    -- Complex window functions
    -- Multiple joins
    -- Heavy aggregations
)
select * from daily_rates
```

### Gold Layer (Marts)
**Recommendation:** `table` (dimensions) or `incremental` (large facts)

**Table for dimensions:**
```sql
-- models/gold/dim_customers.sql
{{ config(materialized='table') }}

select * from {{ ref('int_customers__enriched') }}
```

**Incremental for facts:**
```sql
-- models/gold/fct_orders.sql
{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

select * from {{ ref('int_orders__with_metrics') }}
{% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

---

## Configuration Best Practices

### Folder-Level Configuration (Recommended)
```yaml
# dbt_project.yml
models:
  your_project:
    bronze:
      +materialized: ephemeral
    silver:
      +materialized: ephemeral  # Override for specific models
    gold:
      +materialized: table
      run:
        +materialized: incremental  # Large facts
```

### Model-Level Configuration (Unique Cases Only)
```sql
-- Only override for special requirements
{{ config(
    materialized='incremental',
    unique_key='composite_key',
    cluster_by=['date_column']
) }}
```

---

## Troubleshooting

### Issue: Incremental model not updating
**Solution:** Check is_incremental() logic and unique_key

### Issue: Views are too slow
**Solution:** Change to table materialization

### Issue: Table rebuilds take too long
**Solution:** Change to incremental materialization

### Issue: Storage costs are high
**Solution:** Use ephemeral or view for intermediate models

---

## Quick Reference

| Model Type | Bronze | Silver | Gold Dims | Gold Facts |
|------------|--------|--------|-----------|------------|
| **Materialization** | ephemeral | ephemeral/table | table | incremental |
| **Storage** | None | None/Medium | Medium | High |
| **Build Time** | Fast | Fast/Medium | Medium | Fast |
| **Query Speed** | N/A | N/A | Fast | Fast |

---

For more details on specific patterns, see:
- `STAGING_MODELS.md` - Bronze layer patterns
- `INTERMEDIATE_MODELS.md` - Silver layer patterns
- `MARTS_MODELS.md` - Gold layer patterns
- `INCREMENTAL_MODELS.md` - Deep dive on incremental strategies

