# Performance Optimization Guide for Snowflake

## Overview

Performance optimization in dbt involves choosing the right materializations, leveraging Snowflake-specific features, and optimizing query patterns.

**Official Snowflake Documentation**: [Query Performance](https://docs.snowflake.com/en/user-guide/performance-query)

---

## Materialization Performance

### Choose the Right Materialization

| Materialization | Build Time | Query Time | Best For |
|-----------------|------------|------------|----------|
| **ephemeral** | Fast | Varies | Staging, reusable logic |
| **view** | Instant | Slow | Always-fresh simple transforms |
| **table** | Slow | Fast | Dimensions, complex logic |
| **incremental** | Fast | Fast | Large facts (millions+ rows) |

**Guidelines**:
- Use `ephemeral` for staging (fast, no storage)
- Use `table` for dimensions
- Use `incremental` for large facts

See `MATERIALIZATIONS.md` for details.

---

### When to Change Materializations

**Change ephemeral/view to table when:**

1. **Memory Constraints**: Queries are failing or running slowly due to memory limitations
   ```sql
   -- Change from ephemeral to table
   {{ config(materialized='table') }}
   ```

2. **CTE Reuse**: The same intermediate model is referenced multiple times downstream
   ```sql
   -- If int_customers__metrics is used by 3+ downstream models
   {{ config(materialized='table') }}  -- Materialize to avoid re-computation
   ```

3. **Functions on Join Columns**: Using transformations in JOIN conditions that prevent optimization
   ```sql
   -- ❌ BAD: Functions on join columns (forces full table scans)
   select *
   from {{ ref('stg_customers') }} c
   join {{ ref('stg_orders') }} o
     on upper(trim(c.customer_email)) = upper(trim(o.customer_email))
   
   -- ✅ GOOD: Materialize cleaned columns as a table first
   {{ config(materialized='table') }}
   
   select
     customer_id,
     upper(trim(customer_email)) as customer_email_clean  -- Pre-compute once
   from {{ ref('stg_customers') }}
   ```

**Change table to incremental when:**

1. **Large Data Volumes**: Table has millions+ rows and full refreshes take too long
2. **Append-Only Data**: Event logs, clickstreams, transaction history
3. **Time-Based Updates**: Daily/hourly data loads with time-based filtering

```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    cluster_by=['order_date']
) }}

select * from {{ ref('stg_orders') }}

{% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

**Performance Impact**:
- Ephemeral → Table: Trades storage for compute efficiency
- Table → Incremental: Reduces build time at cost of added complexity

---

## Snowflake-Specific Optimizations

### Clustering Keys

```sql
{{ config(
    materialized='table',
    cluster_by=['order_date', 'customer_id']
) }}
```

**Best Practices**:
- Use 1-4 columns
- Order columns by cardinality (low to high)
- Include common WHERE clause columns
- Include JOIN key columns

**Official Snowflake Docs**: [Clustering Keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)

---

### Warehouse Sizing

```sql
{{ config(
    snowflake_warehouse='LARGE_WH'  -- For complex transformations
) }}
```

**Optimal Sizing Goal: ~500 Micropartitions (MPs) per Node**

Snowflake stores data in micropartitions (~16MB compressed). The warehouse sizing goal is to maintain approximately 500 MPs scanned per node for optimal performance. Too few MPs per node underutilizes the warehouse; too many causes compute skew and spilling.

**Sizing Formula**:
```
Warehouse Size Needed = Total MPs Scanned / 500
```

**Quick Reference Table** (MPs scanned → Recommended warehouse):

| MPs Scanned | Warehouse Size | Nodes | MPs per Node |
|-------------|---------------|-------|--------------|
| 500 | XS | 1 | 500 |
| 1,000 | S | 2 | 500 |
| 2,000 | M | 4 | 500 |
| 4,000 | L | 8 | 500 |
| 8,000 | XL | 16 | 500 |
| 16,000 | 2XL | 32 | 500 |
| 32,000 | 3XL | 64 | 500 |
| 64,000 | 4XL | 128 | 500 |

**How to Find MPs Scanned**:
```sql
-- Check query profile after running model
SELECT 
    query_id,
    total_elapsed_time,
    partitions_scanned
FROM snowflake.account_usage.query_history
WHERE start_time >= dateadd(day, -1, current_timestamp())
and query_text ILIKE '%your_model_name%'
ORDER BY start_time DESC
LIMIT 1;
```

**Practical Guidelines**:
- **Under-sized**: If MPs per node > 1000, consider larger warehouse
- **Over-sized**: If MPs per node < 250, consider smaller warehouse  
- **Development**: Start with XS-S, profile, then adjust
- **Production**: Size based on actual MP scan metrics from query history

**Official Snowflake Docs**: [Warehouse Considerations](https://docs.snowflake.com/en/user-guide/warehouses-considerations)

---

### Generation 2 Standard Warehouses

Gen2 standard warehouses offer improved performance for most dbt workloads.

**Why Gen2 is Better for dbt Projects**:
- **Faster transformations**: Enhanced DELETE, UPDATE, MERGE, adnd table scan operations (critical for incremental models and snapshots)
- **Delta Micropartitions**: Snowflake does not rewrite entire micropartitions for changed data.
- **Faster Underlying Hardware**: You can expect the majority of queries finish faster, and you can do more work at the same time. 
- **Analytics optimization**: Purpose-built for data engineering and analytics workloads

**Converting to Gen2**:
```sql
-- Run directly in Snowflake
ALTER WAREHOUSE TRANSFORMING_WH 
SET RESOURCE_CONSTRAINT = STANDARD_GEN_2;
```

**Official Snowflake Docs**: [Gen2 Standard Warehouses](https://docs.snowflake.com/en/user-guide/warehouses-gen2)

---

### Search Optimization Service

```sql
{{ config(
    post_hook=[
        "alter table {{ this }} add search optimization on equality(customer_id)"
    ]
) }}
```

**When to Use**: Point lookups, selective filters on large tables

**Official Snowflake Docs**: [Search Optimization](https://docs.snowflake.com/en/user-guide/search-optimization-service)

---

### Query Acceleration Service

Query Acceleration is configured at the warehouse level, not in dbt models:

```sql
-- Run directly in Snowflake
ALTER WAREHOUSE TRANSFORMING_WH 
SET ENABLE_QUERY_ACCELERATION = TRUE;

-- Set scale factor (optional)
ALTER WAREHOUSE TRANSFORMING_WH 
SET QUERY_ACCELERATION_MAX_SCALE_FACTOR = 8;
```

**When to Use**:
- Queries with unpredictable data volume
- Ad-hoc analytics workloads
- Queries that scan large portions of tables

**Official Snowflake Docs**: [Query Acceleration](https://docs.snowflake.com/en/user-guide/query-acceleration-service)

---

### Result Caching

Snowflake automatically caches query results for 24 hours.

**Best Practices**:
- Use consistent query patterns to leverage cache
- Avoid unnecessary `current_timestamp()` in WHERE clauses

---

## Incremental Model Performance

### Efficient WHERE Clauses

```sql
{% if is_incremental() %}
    -- ✅ Good: Partition pruning
    where order_date >= (select max(order_date) from {{ this }})
    
    -- ✅ Good: With lookback for late data
    where order_date >= dateadd(day, -3, (select max(order_date) from {{ this }}))
{% endif %}
```

### Incremental Strategy Performance

| Strategy | Speed | Use Case |
|----------|-------|----------|
| **append** | Fastest | Immutable event data |
| **merge** | Medium | Updateable records |
| **delete+insert** | Fast | Partitioned data |

---

## Query Optimization Tips

### Filter Before Joining

```sql
-- ✅ Good: Filter before joining
with filtered_orders as (
    select * from {{ ref('stg_orders') }}
    where order_date >= '2024-01-01'
)

select c.customer_id, count(o.order_id)
from {{ ref('dim_customers') }} c
join filtered_orders o on c.customer_id = o.customer_id
group by c.customer_id
```

### Use QUALIFY for Window Functions

```sql
-- ✅ Good: Snowflake QUALIFY clause
select
    customer_id,
    order_date,
    row_number() over (partition by customer_id order by order_date desc) as rn
from {{ ref('stg_orders') }}
qualify rn <= 5
```

### Pre-Aggregate Before Joining

```sql
-- ✅ Good: Aggregate first, then join
with order_metrics as (
    select
        customer_id,
        count(*) as order_count,
        sum(order_total) as lifetime_value
    from {{ ref('stg_orders') }}
    group by customer_id
)

select c.*, coalesce(m.order_count, 0) as order_count
from {{ ref('dim_customers') }} c
left join order_metrics m on c.customer_id = m.customer_id
```

---

## Development vs Production

### Limit Data in Development

```sql
-- Macro: macros/limit_data_in_dev.sql
{% macro limit_data_in_dev(column_name, dev_days_of_data=3) %}
    {% if target.name == 'dev' %}
        where {{ column_name }} >= dateadd(day, -{{ dev_days_of_data }}, current_date())
    {% endif %}
{% endmacro %}
```

**Usage**:
```sql
select * from {{ ref('stg_orders') }}
{{ limit_data_in_dev('order_date') }}
```

### Target-Specific Configuration

```yaml
# dbt_project.yml
models:
  your_project:
    gold:
      +materialized: "{{ 'view' if target.name == 'dev' else 'table' }}"
```

---

## Query Profiling

### Snowflake Query Profile

```sql
-- View query profile in Snowflake UI:
-- Query History → Select query → Query Profile tab

-- Query history with performance metrics
select
    query_id,
    query_text,
    execution_time,
    bytes_scanned,
    warehouse_name
from snowflake.account_usage.query_history
where user_name = current_user()
  and start_time >= dateadd(day, -7, current_date())
order by execution_time desc
limit 100;
```

### dbt Timing Information

```bash
# Run with timing details
dbt run --select model_name --log-level debug

# View run timing
cat target/run_results.json | jq '.results[].execution_time'
```

---

## Performance Checklist

### Model-Level
- [ ] Appropriate materialization chosen
- [ ] Clustering/partitioning applied for large tables
- [ ] Incremental strategy optimized
- [ ] WHERE clauses filter early
- [ ] JOINs are necessary and optimized

### Project-Level
- [ ] Staging models are ephemeral
- [ ] Large facts are incremental
- [ ] Dev environment uses limited data
- [ ] Warehouse sizing appropriate
- [ ] Regular performance reviews scheduled

---

## Related Documentation

- [Official Snowflake Docs: Query Performance](https://docs.snowflake.com/en/user-guide/performance-query)
- [Official Snowflake Docs: Clustering](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)
- [Official dbt Docs: Best Practices](https://docs.getdbt.com/guides/best-practices)
- `MATERIALIZATIONS.md` - Choosing materializations
- `PROJECT_STRUCTURE.md` - Architectural patterns
