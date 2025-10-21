# Snapshots (SCD Type 2) Guide

## Overview

Snapshots implement Slowly Changing Dimension (SCD) Type 2 logic, capturing historical changes to mutable data over time. They're essential for tracking dimensional attribute changes and compliance requirements.

## When to Use Snapshots

✅ **Historical Tracking** - Track changes to customer, product, or employee attributes  
✅ **Point-in-Time Analysis** - Report on historical state of dimensions  
✅ **Audit Requirements** - Maintain change history for compliance  
✅ **Trend Analysis** - Analyze how attributes change over time  
✅ **SCD Type 2** - Implement slowly changing dimensions  

## Basic Snapshot Structure

```sql
-- snapshots/dim_customers_scd.sql
{% snapshot dim_customers_scd %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['customer_name', 'customer_email', 'customer_status'],
        invalidate_hard_deletes=True
    )
}}

select * from {{ ref('stg_customers') }}

{% endsnapshot %}
```

## Snapshot Strategies

### Timestamp Strategy

Tracks changes based on an `updated_at` timestamp column.

```sql
{% snapshot orders_snapshot_timestamp %}

{{
    config(
        target_schema='snapshots',
        unique_key='order_id',
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deletes=True
    )
}}

select
    order_id,
    customer_id,
    order_status,
    order_total,
    updated_at
from {{ ref('stg_orders') }}

{% endsnapshot %}
```

**When to Use:**
- Source system has reliable `updated_at` timestamps
- Changes are always captured with timestamp updates
- Simpler logic, better performance

**Pros:**
- ✅ More efficient (only checks timestamp)
- ✅ Clearer change tracking
- ✅ Faster execution

**Cons:**
- ❌ Requires reliable timestamp column
- ❌ Misses changes without timestamp updates

### Check Strategy

Compares specified columns to detect changes.

```sql
{% snapshot customers_snapshot_check %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['customer_name', 'customer_email', 'customer_tier', 'customer_status'],
        invalidate_hard_deletes=True
    )
}}

select
    customer_id,
    customer_name,
    customer_email,
    customer_tier,
    customer_status
from {{ ref('stg_customers') }}

{% endsnapshot %}
```

**When to Use:**
- No reliable `updated_at` column
- Need to track specific column changes
- Source changes don't update timestamps

**Pros:**
- ✅ Works without timestamp column
- ✅ Explicit about what changes to track
- ✅ Catches all specified column changes

**Cons:**
- ❌ Slower (compares all check columns)
- ❌ Misses changes to non-checked columns

### Check All Columns

```sql
{% snapshot products_snapshot_all %}

{{
    config(
        target_schema='snapshots',
        unique_key='product_id',
        strategy='check',
        check_cols='all',  -- Check all columns
        invalidate_hard_deletes=True
    )
}}

select * from {{ ref('stg_products') }}

{% endsnapshot %}
```

**When to Use:**
- Need to track all attribute changes
- Unsure which columns will change
- Comprehensive audit requirements

## Generated SCD Columns

Snapshots automatically add these columns:

```sql
-- Metadata columns added by dbt
dbt_scd_id              -- Surrogate key (hash of natural key + timestamp)
dbt_updated_at          -- When the row was updated in snapshot
dbt_valid_from          -- When this version became valid
dbt_valid_to            -- When this version expired (NULL = current)
```

## Querying Snapshots

### Get Current Records

```sql
select *
from {{ ref('dim_customers_scd') }}
where dbt_valid_to is null
```

### Get Point-in-Time Records

```sql
select *
from {{ ref('dim_customers_scd') }}
where '2024-01-15' between dbt_valid_from and coalesce(dbt_valid_to, '9999-12-31')
```

### Get Change History

```sql
select
    customer_id,
    customer_tier,
    dbt_valid_from,
    dbt_valid_to,
    datediff('day', dbt_valid_from, coalesce(dbt_valid_to, current_date())) as days_in_tier
from {{ ref('dim_customers_scd') }}
where customer_id = 12345
order by dbt_valid_from
```

### Join with Facts

```sql
-- Point-in-time joins
select
    f.order_id,
    f.order_date,
    c.customer_tier  -- Customer tier at order date
from {{ ref('fct_orders') }} f
join {{ ref('dim_customers_scd') }} c
    on f.customer_id = c.customer_id
    and f.order_date between c.dbt_valid_from 
        and coalesce(c.dbt_valid_to, '9999-12-31')
```

## Advanced Snapshot Patterns

### Pre-Snapshot Transformation

```sql
{% snapshot customers_snapshot_transformed %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['customer_name', 'customer_email', 'customer_tier']
    )
}}

with source as (
    select * from {{ ref('stg_customers') }}
),

transformed as (
    select
        customer_id,
        upper(customer_name) as customer_name,  -- Normalize before snapshot
        lower(customer_email) as customer_email,
        customer_tier
    from source
)

select * from transformed

{% endsnapshot %}
```

### Snapshot with Business Keys

```sql
{% snapshot employees_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='employee_id',
        strategy='check',
        check_cols=['department', 'job_title', 'salary_band', 'manager_id']
    )
}}

select
    employee_id,
    employee_number,  -- Business key (immutable)
    employee_name,
    department,
    job_title,
    salary_band,
    manager_id,
    hire_date
from {{ ref('stg_employees') }}

{% endsnapshot %}
```

## Hard Deletes

The `invalidate_hard_deletes` configuration handles records deleted from source:

```sql
{{
    config(
        invalidate_hard_deletes=true  -- Close out deleted records
    )
}}
```

**Behavior:**
- `true`: Sets `dbt_valid_to` when record disappears from source
- `false`: Deleted records remain open (default)

## Running Snapshots

### Command Line

```bash
# Run all snapshots
dbt snapshot

# Run specific snapshot
dbt snapshot --select dim_customers_scd

# Run snapshots with specific tag
dbt snapshot --select tag:daily
```

### Scheduling

```yaml
# Schedule snapshots in dbt Cloud or orchestration tool
# Recommended: Daily at consistent time
# Example: Every day at 2 AM UTC
```

## Testing Snapshots

### Test Current Records

```yaml
# snapshots/_snapshots.yml
snapshots:
  - name: dim_customers_scd
    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - customer_id
            - dbt_valid_from
```

### Test for Gaps

```sql
-- tests/singular/test_customer_snapshot_gaps.sql
-- Ensure no gaps in customer history

with snapshot_history as (
    select
        customer_id,
        dbt_valid_from,
        coalesce(dbt_valid_to, '9999-12-31'::date) as dbt_valid_to,
        lead(dbt_valid_from) over (partition by customer_id order by dbt_valid_from) as next_valid_from
    from {{ ref('dim_customers_scd') }}
)

select *
from snapshot_history
where next_valid_from is not null
  and dbt_valid_to != next_valid_from  -- Gap detected
```

## Snapshot Best Practices

### 1. Choose Appropriate Strategy

```sql
-- ✅ Good: Use timestamp when available
strategy='timestamp',
updated_at='updated_at'

-- ✅ Good: Use check for specific columns
strategy='check',
check_cols=['name', 'email', 'status']

-- ⚠️ Caution: Check all columns is expensive
strategy='check',
check_cols='all'
```

### 2. Limit Columns in Snapshots

```sql
-- ✅ Good: Only snapshot tracked attributes
select
    customer_id,
    customer_name,
    customer_email,
    customer_tier,
    customer_status
from source

-- ❌ Bad: Unnecessary columns increase storage/processing
select * from source
```

### 3. Snapshot Schedule Consistency

```bash
# ✅ Good: Consistent daily schedule
# Run at 2 AM every day

# ❌ Bad: Irregular schedule
# Sporadic manual runs
```

### 4. Handle NULL Values

```sql
-- Handle NULLs before snapshot
select
    customer_id,
    coalesce(customer_name, 'Unknown') as customer_name,
    coalesce(customer_email, 'no-email@domain.com') as customer_email
from source
```

## Creating Snapshot Views

### Current Values View

```sql
-- models/gold/dim_customers.sql
{{ config(materialized='view') }}

select
    customer_id,
    customer_name,
    customer_email,
    customer_tier,
    customer_status,
    dbt_valid_from as customer_effective_date
from {{ ref('dim_customers_scd') }}
where dbt_valid_to is null
```

### Change History View

```sql
-- models/gold/customer_change_history.sql
{{ config(materialized='view') }}

select
    customer_id,
    customer_name,
    customer_tier,
    dbt_valid_from as changed_from_date,
    coalesce(dbt_valid_to, current_date()) as changed_to_date,
    datediff('day', dbt_valid_from, coalesce(dbt_valid_to, current_date())) as days_active
from {{ ref('dim_customers_scd') }}
order by customer_id, dbt_valid_from
```

## Snapshot Monitoring

### Track Snapshot Size

```sql
select
    'dim_customers_scd' as snapshot_name,
    count(*) as total_records,
    count(distinct customer_id) as unique_keys,
    count(case when dbt_valid_to is null then 1 end) as current_records,
    max(dbt_updated_at) as last_snapshot_run
from {{ ref('dim_customers_scd') }}
```

### Identify Frequent Changes

```sql
-- Customers with many changes
select
    customer_id,
    count(*) as change_count,
    min(dbt_valid_from) as first_seen,
    max(coalesce(dbt_valid_to, current_date())) as last_changed
from {{ ref('dim_customers_scd') }}
group by customer_id
having count(*) > 10
order by change_count desc
```

## Troubleshooting

### Issue: Snapshot table growing too large
**Solution:** Review check_cols, ensure only necessary columns tracked

### Issue: Missing changes in snapshot
**Solution:** 
- Check source data has changes
- Verify strategy configuration
- Ensure snapshot runs after source updates

### Issue: Duplicate records
**Solution:** Verify unique_key is truly unique

### Issue: Performance degradation
**Solution:**
- Add clustering on (unique_key, dbt_valid_from)
- Limit check_cols to essential columns
- Run snapshots during off-peak hours

## Alternative to Snapshots

### Using Incremental Models

For some use cases, incremental models with merge strategy can be simpler:

```sql
-- Alternative to snapshots for simple change tracking
{{ config(
    materialized='incremental',
    unique_key='customer_id',
    incremental_strategy='merge'
) }}
```

**When to Use Incremental Instead:**
- Don't need full SCD Type 2 history
- Only care about current state
- Simpler change tracking sufficient

---

**Related Documentation:**
- `MARTS_MODELS.md` - Using snapshots in dimensions
- `INCREMENTAL_MODELS.md` - Alternative strategies
- `TESTING_STRATEGY.md` - Testing snapshots
- Official: [dbt Snapshots](https://docs.getdbt.com/docs/build/snapshots)

