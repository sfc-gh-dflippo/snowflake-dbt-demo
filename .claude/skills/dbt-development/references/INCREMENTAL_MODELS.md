# Incremental Models Deep Dive

## When to Use Incremental Models

Use incremental materialization for:
✅ Large fact tables (millions+ rows)  
✅ Time-series data and event logs  
✅ Append-only or merge update patterns  
✅ Models that take >5 minutes to build  
✅ Data that changes incrementally over time  

## Basic Incremental Pattern

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

## Incremental Strategies

### 1. Append Strategy (Default)

**Best For:** Immutable event data, logs, clickstreams

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='append'
) }}

select
    event_id,
    event_timestamp,
    user_id,
    event_type,
    event_data
from {{ ref('stg_events') }}

{% if is_incremental() %}
    where event_timestamp > (select max(event_timestamp) from {{ this }})
{% endif %}
```

**How It Works:**
- New rows are inserted
- No updates or deletes
- Fastest strategy
- Ideal for immutable data

**Limitations:**
- Cannot update existing rows
- Duplicate prevention relies on WHERE clause

---

### 2. Merge Strategy (Most Common)

**Best For:** Updateable records, SCD Type 1, fact tables with late-arriving data

```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    merge_exclude_columns=['dbt_inserted_at']
) }}

select
    order_id,
    customer_id,
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

**How It Works:**
- New rows are inserted
- Existing rows (by unique_key) are updated
- Uses MERGE/UPSERT statement
- Preserves columns in merge_exclude_columns

**Best Practices:**
- Always define unique_key
- Use merge_exclude_columns for metadata
- Add WHERE clause to limit scanned rows

---

### 3. Delete+Insert Strategy

**Best For:** Partitioned data, date-based updates

```sql
{{ config(
    materialized='incremental',
    unique_key='order_date',
    incremental_strategy='delete+insert'
) }}

select
    order_date,
    count(*) as order_count,
    sum(order_amount) as daily_revenue
from {{ ref('stg_orders') }}
where order_date >= dateadd(day, -7, current_date())
group by order_date

{% if is_incremental() %}
    -- Reprocess last 7 days
    where order_date >= dateadd(day, -7, current_date())
{% endif %}
```

**How It Works:**
1. Delete rows matching unique_key
2. Insert all new rows
3. Efficient for partitioned data

**Use Cases:**
- Daily aggregations
- Rolling window calculations
- Partitioned data refreshes

---

### 4. Insert Overwrite Strategy

**Best For:** Partitioned tables with complete partition refreshes

```sql
{{ config(
    materialized='incremental',
    unique_key='date_day',
    incremental_strategy='insert_overwrite',
    partition_by={
        'field': 'date_day',
        'data_type': 'date'
    }
) }}

select
    date_day,
    metric_value
from {{ ref('stg_metrics') }}

{% if is_incremental() %}
    where date_day >= dateadd(day, -3, current_date())
{% endif %}
```

**How It Works:**
- Replaces entire partitions
- Platform-specific (BigQuery, Spark)
- Most efficient for partitioned data

---

## Advanced Patterns

### Pattern 1: Safe Fallback Logic

```sql
{% if is_incremental() %}
    where updated_at > (
        select coalesce(max(updated_at), '1900-01-01'::timestamp)
        from {{ this }}
    )
{% endif %}
```

**Why:** Handles empty tables gracefully

---

### Pattern 2: Lookback Window

```sql
{% if is_incremental() %}
    -- Reprocess last 3 days to catch late-arriving data
    where order_date >= (
        select dateadd(day, -3, max(order_date))
        from {{ this }}
    )
{% endif %}
```

**Why:** Catches late-arriving or updated records

---

### Pattern 3: Composite Unique Key

```sql
{{ config(
    materialized='incremental',
    unique_key=['order_id', 'line_number'],
    incremental_strategy='merge'
) }}

select
    order_id,
    line_number,
    product_id,
    quantity
from {{ ref('stg_order_lines') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

**Why:** Multiple columns form the unique identifier

---

### Pattern 4: Surrogate Key for Merge

```sql
{{ config(
    materialized='incremental',
    unique_key='order_line_id',
    incremental_strategy='merge'
) }}

select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_id,
    order_id,
    line_number,
    product_id
from {{ ref('stg_order_lines') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

**Why:** Single column unique key simplifies merge logic

---

### Pattern 5: Full Refresh Override

```sql
{% if is_incremental() and not var('full_refresh', false) %}
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

**Usage:**
```bash
# Force full refresh without --full-refresh flag
dbt run --select fct_orders --vars '{"full_refresh": true}'
```

---

### Pattern 6: Delete Handling

```sql
{{ config(
    materialized='incremental',
    unique_key='customer_id',
    incremental_strategy='merge'
) }}

select
    customer_id,
    customer_name,
    is_deleted,
    case 
        when is_deleted = true then current_timestamp()
        else null 
    end as deleted_at
from {{ ref('stg_customers') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
       or is_deleted = true  -- Capture deleted records
{% endif %}
```

**Why:** Soft deletes tracked in dimension tables

---

## Performance Optimization

### Add Clustering Keys

```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    cluster_by=['order_date', 'customer_id']
) }}
```

**Impact:** Faster queries and incremental runs

---

### Partition Your Data

```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    partition_by={
        'field': 'order_date',
        'data_type': 'date',
        'granularity': 'day'
    }
) }}
```

**Impact:** Reduced scan sizes and costs

---

### Limit Incremental Scans

```sql
{% if is_incremental() %}
    -- Only scan last 30 days of source data
    where order_date >= dateadd(day, -30, current_date())
      and updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

**Impact:** Faster source queries

---

## Testing Incremental Models

### Test Incremental Logic

```sql
-- tests/singular/test_fct_orders_incremental_logic.sql
with max_date_in_model as (
    select max(order_date) as max_date
    from {{ ref('fct_orders') }}
),

recent_orders as (
    select count(*) as order_count
    from {{ ref('stg_orders') }}
    where order_date > (select max_date from max_date_in_model)
)

-- Fail if we're missing recent orders
select *
from recent_orders
where order_count = 0
  and (select max_date from max_date_in_model) < current_date() - 1
```

### Test Unique Key Enforcement

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
```

---

## Troubleshooting

### Issue: Duplicate Records

**Cause:** Unique key not properly defined

**Solution:**
```sql
-- Check for duplicates
select
    unique_key,
    count(*)
from {{ ref('fct_orders') }}
group by unique_key
having count(*) > 1
```

---

### Issue: Missing Recent Data

**Cause:** Incremental WHERE clause too restrictive

**Solution:**
```sql
-- Add lookback window
{% if is_incremental() %}
    where order_date >= dateadd(day, -3, (select max(order_date) from {{ this }}))
{% endif %}
```

---

### Issue: Slow Incremental Runs

**Cause:** Full table scan on source or target

**Solution:**
- Add clustering keys
- Partition tables
- Limit source scan with date filters
- Use indexes (if available)

---

### Issue: Schema Changes Breaking Builds

**Configuration:**
```sql
{{ config(
    materialized='incremental',
    on_schema_change='append_new_columns'  -- or 'sync_all_columns'
) }}
```

**Options:**
- `fail` - Stop build on schema change (default, safest)
- `ignore` - Continue without syncing schema
- `append_new_columns` - Add new columns only
- `sync_all_columns` - Sync all column changes

---

## Full Refresh Strategies

### Command-Line Full Refresh
```bash
# Full refresh specific model
dbt run --select fct_orders --full-refresh

# Full refresh all incremental models
dbt run --full-refresh
```

### Code-Based Full Refresh
```sql
{% if is_incremental() and not flags.FULL_REFRESH %}
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

### Scheduled Full Refresh
```yaml
# dbt_project.yml
models:
  your_project:
    gold:
      facts:
        fct_orders:
          +full_refresh: false  # Prevent accidental full refresh
```

---

## Best Practices Checklist

- [ ] Define unique_key for merge strategy
- [ ] Use merge_exclude_columns for metadata
- [ ] Add WHERE clause to limit source scans
- [ ] Include lookback window for late data
- [ ] Add clustering/partitioning for performance
- [ ] Test incremental logic
- [ ] Document incremental strategy
- [ ] Handle schema changes appropriately
- [ ] Monitor incremental run times
- [ ] Plan for periodic full refreshes

---

## Example: Production-Ready Incremental Model

```sql
-- models/gold/fct_order_lines.sql
{{ config(
    materialized='incremental',
    unique_key='order_line_id',
    incremental_strategy='merge',
    merge_exclude_columns=['dbt_inserted_at'],
    cluster_by=['order_date', 'customer_id'],
    on_schema_change='fail'
) }}

with source as (
    select
        {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_id,
        order_id,
        line_number,
        customer_id,
        product_id,
        order_date,
        quantity,
        unit_price,
        discount_pct,
        updated_at
    from {{ ref('stg_order_lines') }}
    
    {% if is_incremental() %}
        -- Reprocess last 3 days to catch late-arriving data
        where order_date >= dateadd(day, -3, (
            select max(order_date) 
            from {{ this }}
        ))
        or updated_at > (
            select coalesce(max(updated_at), '1900-01-01'::timestamp)
            from {{ this }}
        )
    {% endif %}
),

final as (
    select
        order_line_id,
        order_id,
        line_number,
        customer_id,
        product_id,
        order_date,
        quantity,
        unit_price,
        discount_pct,
        -- Calculate extended price
        quantity * unit_price * (1 - discount_pct) as extended_price,
        
        -- Metadata
        current_timestamp() as dbt_updated_at,
        {% if not is_incremental() %}
            current_timestamp() as dbt_inserted_at
        {% else %}
            coalesce(
                (select dbt_inserted_at from {{ this }} where order_line_id = source.order_line_id),
                current_timestamp()
            ) as dbt_inserted_at
        {% endif %}
    from source
)

select * from final
```

---

**Related Documentation:**
- `MATERIALIZATIONS.md` - Complete materialization guide
- `MARTS_MODELS.md` - Gold layer fact table patterns
- `PERFORMANCE_OPTIMIZATION.md` - Query optimization
- `TESTING_STRATEGY.md` - Testing incremental models

