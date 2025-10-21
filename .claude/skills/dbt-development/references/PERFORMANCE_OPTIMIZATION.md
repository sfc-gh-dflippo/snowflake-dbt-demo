# Performance Optimization Guide for Snowflake

## Core Optimization Strategies

Performance optimization in dbt involves choosing the right materializations, optimizing SQL queries, and leveraging Snowflake-specific features.

## Materialization Performance

### Choose the Right Materialization

| Materialization | Build Time | Query Time | Storage | Best For |
|-----------------|------------|------------|---------|----------|
| **ephemeral** | Fast | Varies | None | CTEs, staging, reusable logic |
| **view** | Instant | Slow | Minimal | Simple transformations, always-fresh |
| **table** | Slow | Fast | High | Complex logic, frequent queries |
| **incremental** | Fast | Fast | Medium | Large datasets, append patterns |

### Materialization Guidelines

```sql
-- Use ephemeral for staging (fast, no storage)
{{ config(materialized='ephemeral') }}

-- Use table for complex intermediate models
{{ config(materialized='table') }}

-- Use incremental for large facts (millions+ rows)
{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}
```

## Query Optimization

### 1. Efficient Joins

```sql
-- ✅ Good: Filter before joining
with filtered_orders as (
    select * 
    from {{ ref('stg_orders') }}
    where order_date >= '2024-01-01'
),

customers as (
    select * from {{ ref('dim_customers') }}
)

select
    c.customer_id,
    count(o.order_id) as order_count
from customers c
join filtered_orders o on c.customer_id = o.customer_id
group by c.customer_id
```

```sql
-- ❌ Bad: Join then filter
select
    c.customer_id,
    count(o.order_id) as order_count
from {{ ref('dim_customers') }} c
join {{ ref('stg_orders') }} o on c.customer_id = o.customer_id
where o.order_date >= '2024-01-01'
group by c.customer_id
```

### 2. Window Function Optimization

```sql
-- ✅ Good: Single window function
select
    customer_id,
    order_date,
    row_number() over (partition by customer_id order by order_date desc) as order_rank
from {{ ref('stg_orders') }}
qualify order_rank <= 5  -- Snowflake/Databricks QUALIFY clause
```

```sql
-- ❌ Bad: Subquery for ranking
select *
from (
    select
        customer_id,
        order_date,
        row_number() over (partition by customer_id order by order_date desc) as order_rank
    from {{ ref('stg_orders') }}
) ranked
where order_rank <= 5
```

### 3. Aggregation Optimization

```sql
-- ✅ Good: Pre-aggregate before joining
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

## Snowflake-Specific Optimizations

### Clustering Keys
```sql
{{ config(
    materialized='table',
    cluster_by=['order_date', 'customer_id']
) }}
```

**Best Practices:**
- Use 1-4 columns
- Order columns by cardinality (low to high)
- Include common WHERE clause columns
- Include JOIN key columns

### Warehouse Sizing
```sql
{{ config(
    snowflake_warehouse='LARGE_WH'  -- For complex transformations
) }}
```

**Sizing Guidelines:**
- **X-Small**: Simple queries, small datasets
- **Small**: Standard development
- **Medium**: Larger dimensions, smaller facts
- **Large**: Complex transformations, large facts and very large dimensions
- **X-Large+**: Heavy aggregations, very large datasets

### Search Optimization Service
```sql
{{ config(
    post_hook=[
        "alter table {{ this }} add search optimization on equality(customer_id)"
    ]
) }}
```

### Query Acceleration Service

```sql
{{ config(
    post_hook=[
        "alter table {{ this }} set enable_query_acceleration = true"
    ]
) }}
```

**When to Use:**
- Queries with unpredictable data volume
- Ad-hoc analytics workloads
- Queries that scan large portions of tables

### Result Caching

Snowflake automatically caches query results for 24 hours.

**Best Practices:**
- Use consistent query patterns to leverage cache
- Avoid unnecessary `current_timestamp()` in WHERE clauses
- Use `RESULT_SCAN()` for repeated queries

### Zero-Copy Cloning

```sql
{{ config(
    post_hook=[
        "create or replace table {{ this }}_backup clone {{ this }}"
    ]
) }}
```

**Use Cases:**
- Testing schema changes
- Creating dev/test environments
- Quick backups before major changes

## Incremental Model Performance

### Efficient Incremental WHERE Clauses

```sql
{% if is_incremental() %}
    -- ✅ Good: Partition pruning
    where order_date >= (select max(order_date) from {{ this }})
    
    -- ✅ Good: With lookback for late data
    where order_date >= dateadd(day, -3, (select max(order_date) from {{ this }}))
    
    -- ✅ Good: Updated timestamp
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

### Incremental Strategy Performance

| Strategy | Speed | Use Case |
|----------|-------|----------|
| **append** | Fastest | Immutable event data |
| **merge** | Medium | Updateable records |
| **delete+insert** | Fast | Partitioned data |
| **insert_overwrite** | Fastest | Full partition refresh |

## CTE Optimization

### Proper CTE Structure

```sql
-- ✅ Good: Reusable CTEs with clear purpose
with
-- Import CTEs
customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

-- Logical CTEs
customer_metrics as (
    select
        customer_id,
        count(*) as order_count
    from orders
    group by customer_id
),

-- Final CTE
final as (
    select
        c.customer_id,
        c.customer_name,
        m.order_count
    from customers c
    left join customer_metrics m on c.customer_id = m.customer_id
)

select * from final
```

## Development vs Production Optimization

### Limit Data in Development

```sql
-- Macro: macros/limit_data_in_dev.sql
{% macro limit_data_in_dev(column_name, dev_days_of_data=3) %}
    {% if target.name == 'dev' %}
        where {{ column_name }} >= dateadd(day, -{{ dev_days_of_data }}, current_date())
    {% endif %}
{% endmacro %}
```

**Usage:**
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

## Query Profiling

### Analyze Query Plans in Snowflake

```sql
-- View query profile in Snowflake UI
-- Query History → Select query → Query Profile tab

-- Use EXPLAIN to see query plan
explain select * from {{ ref('dim_customers') }};

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

## Monitoring Performance

### Track Model Run Times

```sql
-- Query dbt_artifacts for slow models
select
    model_name,
    avg(total_node_runtime) as avg_runtime_seconds,
    max(total_node_runtime) as max_runtime_seconds
from {{ ref('model_executions') }}
where run_started_at >= dateadd(day, -30, current_date())
group by model_name
having avg(total_node_runtime) > 60  -- Models taking > 1 minute
order by avg_runtime_seconds desc
```

## Common Performance Anti-Patterns

### ❌ Anti-Pattern 1: Cartesian Joins

```sql
-- ❌ Bad: Cartesian join
select *
from {{ ref('customers') }} c,
     {{ ref('products') }} p

-- ✅ Good: Explicit join condition
select *
from {{ ref('customers') }} c
cross join {{ ref('products') }} p
where c.segment = 'VIP'  -- Add appropriate filters
```

### ❌ Anti-Pattern 2: Nested Subqueries

```sql
-- ❌ Bad: Multiple nested subqueries
select
    customer_id,
    (select max(order_date) from orders o where o.customer_id = c.customer_id) as last_order
from customers c

-- ✅ Good: Use CTEs and joins
with customer_orders as (
    select
        customer_id,
        max(order_date) as last_order
    from orders
    group by customer_id
)

select
    c.customer_id,
    co.last_order
from customers c
left join customer_orders co on c.customer_id = co.customer_id
```

### ❌ Anti-Pattern 3: DISTINCT Without Analysis

```sql
-- ❌ Bad: DISTINCT to hide data quality issues
select distinct
    customer_id,
    customer_name
from {{ ref('some_model') }}

-- ✅ Good: Fix root cause, add unique test
select
    customer_id,
    customer_name
from {{ ref('some_model') }}
-- Add test: unique customer_id
```

## Performance Checklist

### Model-Level
- [ ] Appropriate materialization chosen
- [ ] Clustering/partitioning applied for large tables
- [ ] Incremental strategy optimized for use case
- [ ] CTEs structured efficiently
- [ ] WHERE clauses filter early
- [ ] JOINs are necessary and optimized

### Project-Level
- [ ] Staging models are ephemeral
- [ ] Large facts are incremental
- [ ] Dev environment uses limited data
- [ ] Warehouse sizing appropriate
- [ ] dbt_artifacts monitoring in place
- [ ] Regular performance reviews scheduled

## Snowflake-Specific Best Practices

### Micro-Partitions

Snowflake automatically partitions data into micro-partitions.

**Optimization Tips:**
- Data is automatically sorted within micro-partitions
- Clustering keys optimize micro-partition pruning
- Smaller micro-partitions = better pruning

### Multi-Cluster Warehouses

```yaml
# Use multi-cluster warehouses for concurrent workloads
warehouse: TRANSFORMING_WH  # Configured with min=1, max=5 clusters
```

**Benefits:**
- Automatic scaling for concurrent queries
- Queue management
- Cost control with min/max clusters

## Resources

### Snowflake Documentation
- [Query Performance](https://docs.snowflake.com/en/user-guide/performance-query)
- [Warehouse Considerations](https://docs.snowflake.com/en/user-guide/warehouses-considerations)
- [Clustering Keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)
- [Search Optimization](https://docs.snowflake.com/en/user-guide/search-optimization-service)

---

**Related Documentation:**
- `MATERIALIZATIONS.md` - Choosing materializations
- `INCREMENTAL_MODELS.md` - Incremental strategies
- `PROJECT_STRUCTURE.md` - Architectural patterns
- `QUICK_REFERENCE.md` - Performance commands

