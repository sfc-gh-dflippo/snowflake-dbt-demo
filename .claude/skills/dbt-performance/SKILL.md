---
name: dbt-performance
description:
  Optimizing dbt and Snowflake performance through materialization choices, clustering keys,
  warehouse sizing, and query optimization. Use this skill when addressing slow model builds,
  optimizing query performance, sizing warehouses, implementing clustering strategies, or
  troubleshooting performance issues.
---

# dbt Performance Optimization

## Purpose

Transform AI agents into experts on dbt and Snowflake performance optimization, providing guidance
on choosing optimal materializations, leveraging Snowflake-specific features, and implementing query
optimization patterns for production-grade performance.

## When to Use This Skill

Activate this skill when users ask about:

- Optimizing slow dbt model builds
- Choosing appropriate materializations for performance
- Implementing Snowflake clustering keys
- Sizing warehouses appropriately
- Converting models to incremental for performance
- Optimizing query patterns and SQL
- Troubleshooting performance bottlenecks
- Using Snowflake performance features (Gen2, query acceleration, search optimization)

**Official Snowflake Documentation**:
[Query Performance](https://docs.snowflake.com/en/user-guide/performance-query)

---

## Materialization Performance

### Choose the Right Materialization

| Materialization | Build Time | Query Time | Best For                       |
| --------------- | ---------- | ---------- | ------------------------------ |
| **ephemeral**   | Fast       | Varies     | Staging, reusable logic        |
| **view**        | Instant    | Slow       | Always-fresh simple transforms |
| **table**       | Slow       | Fast       | Dimensions, complex logic      |
| **incremental** | Fast       | Fast       | Large facts (millions+ rows)   |

**Guidelines**:

- Use `ephemeral` for staging (fast, no storage)
- Use `table` for dimensions
- Use `incremental` for large facts

---

### When to Change Materializations

#### Change Ephemeral/View to Table When:

**1. Memory Constraints**

Queries failing or running slowly due to memory limitations:

```sql
-- Change from ephemeral to table
{{ config(materialized='table') }}
```

**2. CTE Reuse**

Same intermediate model referenced multiple times downstream:

```sql
-- If int_customers__metrics is used by 3+ downstream models
{{ config(materialized='table') }}  -- Materialize to avoid re-computation
```

**3. Functions on Join Columns**

Transformations in JOIN conditions prevent optimization:

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

**Performance Impact**: Ephemeral → Table trades storage for compute efficiency

---

#### Change Table to Incremental When:

**1. Large Data Volumes**

Table has millions+ rows and full refreshes take too long:

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

**2. Append-Only Data**

Event logs, clickstreams, transaction history

**3. Time-Based Updates**

Daily/hourly data loads with time-based filtering

**Performance Impact**: Table → Incremental reduces build time at cost of added complexity

---

## Snowflake-Specific Optimizations

### Clustering Keys

**Improve query performance on large tables:**

```sql
{{ config(
    materialized='table',
    cluster_by=['order_date', 'customer_id']
) }}
```

**Best Practices**:

- Use 1-4 columns maximum
- Order columns by cardinality (low to high)
- Include common WHERE clause columns
- Include JOIN key columns
- Monitor cluster usage: `SYSTEM$CLUSTERING_INFORMATION()`

**Example with Multiple Keys:**

```sql
{{ config(
    materialized='incremental',
    unique_key='event_id',
    cluster_by=['event_date', 'event_type', 'user_id']
) }}
```

**Official Snowflake Docs**:
[Clustering Keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)

---

### Warehouse Sizing

```sql
{{ config(
    snowflake_warehouse='LARGE_WH'  -- For complex transformations
) }}
```

**Optimal Sizing Goal: ~500 Micropartitions (MPs) per Node**

Snowflake stores data in micropartitions (~16MB compressed). The warehouse sizing goal is to
maintain approximately 500 MPs scanned per node for optimal performance. Too few MPs per node
underutilizes the warehouse; too many causes compute skew and spilling.

**Sizing Formula:**

```
Warehouse Size Needed = Total MPs Scanned / 500
```

**Quick Reference Table** (MPs scanned → Recommended warehouse):

| MPs Scanned | Warehouse Size | Nodes | MPs per Node |
| ----------- | -------------- | ----- | ------------ |
| 500         | XS             | 1     | 500          |
| 1,000       | S              | 2     | 500          |
| 2,000       | M              | 4     | 500          |
| 4,000       | L              | 8     | 500          |
| 8,000       | XL             | 16    | 500          |
| 16,000      | 2XL            | 32    | 500          |
| 32,000      | 3XL            | 64    | 500          |
| 64,000      | 4XL            | 128   | 500          |

**How to Find MPs Scanned:**

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

**Official Snowflake Docs**:
[Warehouse Considerations](https://docs.snowflake.com/en/user-guide/warehouses-considerations)

---

### Generation 2 Standard Warehouses

Gen2 standard warehouses offer improved performance for most dbt workloads.

**Why Gen2 is Better for dbt Projects**:

- **Faster transformations**: Enhanced DELETE, UPDATE, MERGE, and table scan operations (critical
  for incremental models and snapshots)
- **Delta Micropartitions**: Snowflake does not rewrite entire micropartitions for changed data
- **Faster Underlying Hardware**: Majority of queries finish faster, can do more work simultaneously
- **Analytics optimization**: Purpose-built for data engineering and analytics workloads

**Converting to Gen2:**

```sql
-- Run directly in Snowflake
ALTER WAREHOUSE TRANSFORMING_WH
SET RESOURCE_CONSTRAINT = STANDARD_GEN_2;
```

**Official Snowflake Docs**:
[Gen2 Standard Warehouses](https://docs.snowflake.com/en/user-guide/warehouses-gen2)

---

### Search Optimization Service

**For point lookups and selective filters on large tables:**

```sql
{{ config(
    post_hook=[
        "alter table {{ this }} add search optimization on equality(customer_id, email)"
    ]
) }}
```

**When to Use**:

- Point lookups (WHERE customer_id = ?)
- Selective filters on large tables
- High-cardinality columns

**Official Snowflake Docs**:
[Search Optimization](https://docs.snowflake.com/en/user-guide/search-optimization-service)

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
- Variable query complexity

**Official Snowflake Docs**:
[Query Acceleration](https://docs.snowflake.com/en/user-guide/query-acceleration-service)

---

### Result Caching

Snowflake automatically caches query results for 24 hours.

**Best Practices**:

- Use consistent query patterns to leverage cache
- Avoid unnecessary `current_timestamp()` in WHERE clauses (breaks cache)
- Identical queries return cached results instantly

**Example to Preserve Cache:**

```sql
-- ❌ Breaks cache every run
where created_at > current_timestamp() - interval '7 days'

-- ✅ Preserves cache (use dbt variables)
where created_at > '{{ var("lookback_date") }}'
```

---

## Incremental Model Performance

### Efficient WHERE Clauses

```sql
{% if is_incremental() %}
    -- ✅ Good: Partition pruning
    where order_date >= (select max(order_date) from {{ this }})

    -- ✅ Good: With lookback for late data
    where order_date >= dateadd(day, -3, (select max(order_date) from {{ this }}))

    -- ✅ Good: Limit source scan
    where order_date >= dateadd(day, -30, current_date())
      and order_date > (select max(order_date) from {{ this }})
{% endif %}
```

### Incremental Strategy Performance

| Strategy          | Speed   | Use Case             |
| ----------------- | ------- | -------------------- |
| **append**        | Fastest | Immutable event data |
| **merge**         | Medium  | Updateable records   |
| **delete+insert** | Fast    | Partitioned data     |

**Choose based on data characteristics:**

- Append: Event logs, clickstreams (never update)
- Merge: Orders, customers (updates possible)
- Delete+Insert: Date-partitioned aggregations

---

## Query Optimization Tips

### Filter Before Joining

```sql
-- ✅ Good: Filter before joining
with filtered_orders as (
    select * from {{ ref('stg_orders') }}
    where order_date >= '2024-01-01'
)

select
    c.customer_id,
    count(o.order_id) as order_count
from {{ ref('dim_customers') }} c
join filtered_orders o on c.customer_id = o.customer_id
group by c.customer_id
```

**Why It Works**: Reduces join size, improves memory efficiency

---

### Use QUALIFY for Window Functions

```sql
-- ✅ Good: Snowflake QUALIFY clause (cleaner & faster)
select
    customer_id,
    order_date,
    order_amount,
    row_number() over (partition by customer_id order by order_date desc) as rn
from {{ ref('stg_orders') }}
qualify rn <= 5  -- Top 5 orders per customer

-- ❌ Slower: Subquery approach
select * from (
    select
        customer_id,
        order_date,
        row_number() over (partition by customer_id order by order_date desc) as rn
    from {{ ref('stg_orders') }}
)
where rn <= 5
```

**Why QUALIFY is Better**: Single scan, no subquery overhead

---

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

select
    c.*,
    coalesce(m.order_count, 0) as order_count,
    coalesce(m.lifetime_value, 0) as lifetime_value
from {{ ref('dim_customers') }} c
left join order_metrics m on c.customer_id = m.customer_id
```

**Why It Works**: Reduces join size dramatically, avoids repeated aggregation

---

### Avoid SELECT \*

```sql
-- ❌ Bad: Reads all columns
select *
from {{ ref('fct_orders') }}
where order_date = current_date()

-- ✅ Good: Select only needed columns
select
    order_id,
    customer_id,
    order_date,
    order_amount
from {{ ref('fct_orders') }}
where order_date = current_date()
```

**Why It Matters**: Column pruning reduces data scanned and network transfer

---

## Development vs Production

### Limit Data in Development

**Create macro for dev data limiting:**

```sql
-- macros/limit_data_in_dev.sql
{% macro limit_data_in_dev(column_name, dev_days_of_data=3) %}
    {% if target.name == 'dev' %}
        where {{ column_name }} >= dateadd(day, -{{ dev_days_of_data }}, current_date())
    {% endif %}
{% endmacro %}
```

**Usage:**

```sql
select * from {{ ref('stg_orders') }}
{{ limit_data_in_dev('order_date', 7) }}
```

---

### Target-Specific Configuration

```yaml
# dbt_project.yml
models:
  your_project:
    gold:
      # Use views in dev, tables in prod
      +materialized: "{{ 'view' if target.name == 'dev' else 'table' }}"
```

**Benefits**:

- Faster dev builds
- Lower dev costs
- Prod stays optimized

---

## Query Profiling

### Snowflake Query Profile

**View in Snowflake UI:**

1. Go to Query History
2. Select your query
3. Click "Query Profile" tab
4. Analyze execution plan

**Query history with performance metrics:**

```sql
select
    query_id,
    query_text,
    execution_time,
    bytes_scanned,
    warehouse_name,
    partitions_scanned
from snowflake.account_usage.query_history
where user_name = current_user()
  and start_time >= dateadd(day, -7, current_date())
order by execution_time desc
limit 100;
```

---

### dbt Timing Information

```bash
# Run with timing details
dbt run --select model_name --log-level debug

# View run timing
cat target/run_results.json | jq '.results[].execution_time'
```

**Analyze slow models:**

```bash
# Find slowest models
cat target/run_results.json | jq -r '.results[] | [.execution_time, .unique_id] | @tsv' | sort -rn | head -10
```

---

## Performance Checklist

### Model-Level Optimization

- [ ] Appropriate materialization chosen (ephemeral/table/incremental)
- [ ] Clustering keys applied for large tables (1-4 columns)
- [ ] Incremental strategy optimized (append/merge/delete+insert)
- [ ] WHERE clauses filter early (before joins)
- [ ] JOINs are necessary and optimized (filter before join)
- [ ] SELECT only needed columns (no SELECT \*)
- [ ] Window functions use QUALIFY when possible

### Project-Level Optimization

- [ ] Staging models are ephemeral (no storage overhead)
- [ ] Large facts are incremental (faster builds)
- [ ] Dev environment uses limited data (faster iteration)
- [ ] Warehouse sizing appropriate per model complexity
- [ ] Gen2 warehouses enabled for transformations
- [ ] Regular performance reviews scheduled
- [ ] Clustering monitored and maintained

---

## Helping Users with Performance

### Strategy for Assisting Users

When users report performance issues:

1. **Identify the bottleneck**: Build time? Query time? Both?
2. **Check materialization**: Is it appropriate for model size/purpose?
3. **Review query patterns**: Are there obvious inefficiencies?
4. **Assess warehouse sizing**: Using appropriate compute for workload?
5. **Recommend optimizations**: Specific, actionable improvements
6. **Provide examples**: Working code with performance comparisons

### Common User Questions

**"My model is slow to build"**

- Check materialization: Should it be incremental?
- Review warehouse size: Appropriate for data volume?
- Analyze query: Are there inefficient patterns?
- Check clustering: Would it help query performance?

**"How do I make this faster?"**

- Change ephemeral to table if reused multiple times
- Convert table to incremental for large datasets
- Add clustering keys for frequently filtered columns
- Pre-aggregate before joining
- Use QUALIFY instead of subqueries

**"What warehouse size should I use?"**

- Profile the query to see MPs scanned
- Aim for ~500 MPs per warehouse node
- Start small, scale up based on actual metrics
- Use `snowflake_warehouse` config for model-specific sizing

---

## Related Official Documentation

- [Snowflake Docs: Query Performance](https://docs.snowflake.com/en/user-guide/performance-query)
- [Snowflake Docs: Clustering](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)
- [Snowflake Docs: Gen2 Warehouses](https://docs.snowflake.com/en/user-guide/warehouses-gen2)
- [dbt Docs: Best Practices](https://docs.getdbt.com/guides/best-practices)

---

**Goal**: Transform AI agents into expert dbt performance optimizers who identify bottlenecks,
recommend appropriate optimizations, and implement Snowflake-specific features for production-grade
performance.
