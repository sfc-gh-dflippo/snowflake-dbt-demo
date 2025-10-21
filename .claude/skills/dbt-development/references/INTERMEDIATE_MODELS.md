# Silver Layer: Intermediate Models Guide

## Purpose

Intermediate models (silver layer) contain reusable business logic and complex transformations. They sit between staging (bronze) and marts (gold), transforming cleaned data into enriched, business-ready components.

## Core Principles

✅ **Reference staging or other intermediate models** (never sources)  
✅ **Contain business logic** (aggregations, joins, calculations)  
✅ **Reusable across multiple marts** (DRY principle)  
✅ **Ephemeral for logic, table for complex computations**  
✅ **Named with int_ prefix** (`int_{entity}__{description}`)  

## Naming Convention

```
int_{entity}__{description}.sql
```

**Examples:**
- `int_customers__with_orders.sql` - Customer enrichment with order metrics
- `int_fx_rates__daily.sql` - Foreign exchange daily transformations
- `customer_segments.sql` - Business segmentation logic
- `int_orders__enriched.sql` - Orders with additional calculated fields

## Materialization Strategy

### Ephemeral (Recommended for Reusable Logic)

```sql
-- models/silver/int_customers__base.sql
{{ config(materialized='ephemeral') }}

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customer_metrics as (
    select
        customer_id,
        count(*) as order_count,
        sum(order_total) as lifetime_value
    from orders
    group by customer_id
),

final as (
    select
        c.customer_id,
        c.customer_name,
        coalesce(m.order_count, 0) as order_count,
        coalesce(m.lifetime_value, 0) as lifetime_value
    from customers c
    left join customer_metrics m
        on c.customer_id = m.customer_id
)

select * from final
```

**When to Use:**
- Model is always referenced by other models
- Fast computation (< 1 minute)
- Logic is reused across multiple marts
- Part of a multi-step transformation pipeline

### Table (for Complex Transformations)

```sql
-- models/silver/int_fx_rates__daily.sql
{{ config(materialized='table') }}

with rates as (
    select * from {{ ref('stg_fx_rates') }}
),

daily_rates as (
    select
        date_trunc('day', rate_timestamp) as rate_date,
        currency_pair,
        avg(exchange_rate) as avg_rate,
        min(exchange_rate) as min_rate,
        max(exchange_rate) as max_rate,
        -- Complex window functions
        avg(exchange_rate) over (
            partition by currency_pair
            order by date_trunc('day', rate_timestamp)
            rows between 7 preceding and current row
        ) as rolling_7day_avg
    from rates
    group by date_trunc('day', rate_timestamp), currency_pair
)

select * from daily_rates
```

**When to Use:**
- Complex window functions or CTEs
- Long-running computations (> 1 minute)
- Heavy aggregations
- Referenced by multiple downstream models
- Needs to be queried independently

## Common Patterns

### Pattern 1: Customer Enrichment

```sql
-- models/silver/int_customers__with_orders.sql
{{ config(materialized='ephemeral') }}

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

order_metrics as (
    select
        customer_id,
        count(*) as total_orders,
        sum(order_total) as lifetime_value,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        avg(order_total) as avg_order_value
    from orders
    group by customer_id
),

final as (
    select
        c.customer_id,
        c.customer_name,
        c.customer_email,
        c.customer_status,
        
        -- Order metrics (with safe defaults)
        coalesce(m.total_orders, 0) as total_orders,
        coalesce(m.lifetime_value, 0) as lifetime_value,
        coalesce(m.avg_order_value, 0) as avg_order_value,
        m.first_order_date,
        m.most_recent_order_date,
        
        -- Calculated fields
        case 
            when m.total_orders is null then 'No Orders'
            when m.total_orders = 1 then 'Single Order'
            else 'Multiple Orders'
        end as order_frequency_segment,
        
        datediff('day', m.most_recent_order_date, current_date()) as days_since_last_order
        
    from customers c
    left join order_metrics m
        on c.customer_id = m.customer_id
)

select * from final
```

### Pattern 2: Product Performance Metrics

```sql
-- models/silver/int_products__performance.sql
{{ config(materialized='table') }}

with products as (
    select * from {{ ref('stg_products') }}
),

order_lines as (
    select * from {{ ref('stg_order_lines') }}
),

product_sales as (
    select
        product_id,
        count(distinct order_id) as orders_containing_product,
        sum(quantity) as total_units_sold,
        sum(line_total) as total_revenue,
        avg(unit_price) as avg_selling_price,
        min(order_date) as first_sold_date,
        max(order_date) as last_sold_date
    from order_lines
    group by product_id
),

final as (
    select
        p.product_id,
        p.product_name,
        p.category,
        p.unit_cost,
        
        coalesce(s.orders_containing_product, 0) as orders_count,
        coalesce(s.total_units_sold, 0) as units_sold,
        coalesce(s.total_revenue, 0) as revenue,
        coalesce(s.avg_selling_price, 0) as avg_price,
        s.first_sold_date,
        s.last_sold_date,
        
        -- Profitability
        s.avg_selling_price - p.unit_cost as gross_margin_per_unit,
        s.total_revenue - (s.total_units_sold * p.unit_cost) as total_gross_margin
        
    from products p
    left join product_sales s
        on p.product_id = s.product_id
)

select * from final
```

### Pattern 3: Time-Based Aggregations

```sql
-- models/silver/int_daily_sales__summary.sql
{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('stg_orders') }}
),

daily_summary as (
    select
        date_trunc('day', order_date) as sale_date,
        count(distinct order_id) as order_count,
        count(distinct customer_id) as unique_customers,
        sum(order_total) as daily_revenue,
        avg(order_total) as avg_order_value,
        
        -- Running totals
        sum(count(distinct order_id)) over (
            order by date_trunc('day', order_date)
            rows between unbounded preceding and current row
        ) as cumulative_orders,
        
        sum(sum(order_total)) over (
            order by date_trunc('day', order_date)
            rows between unbounded preceding and current row
        ) as cumulative_revenue
        
    from orders
    group by date_trunc('day', order_date)
)

select * from daily_summary
```

### Pattern 4: Business Segmentation

```sql
-- models/silver/customer_segments.sql
{{ config(materialized='ephemeral') }}

with customer_metrics as (
    select * from {{ ref('int_customers__with_orders') }}
),

segments as (
    select
        customer_id,
        customer_name,
        total_orders,
        lifetime_value,
        
        -- RFM Segmentation
        case 
            when days_since_last_order <= 30 then 'Recent'
            when days_since_last_order <= 90 then 'Active'
            when days_since_last_order <= 180 then 'At Risk'
            else 'Churned'
        end as recency_segment,
        
        case 
            when total_orders >= 10 then 'Frequent'
            when total_orders >= 5 then 'Regular'
            when total_orders >= 2 then 'Occasional'
            else 'One-Time'
        end as frequency_segment,
        
        case 
            when lifetime_value >= 5000 then 'High Value'
            when lifetime_value >= 1000 then 'Medium Value'
            else 'Low Value'
        end as monetary_segment,
        
        -- Combined tier
        case 
            when days_since_last_order <= 30 
                and total_orders >= 10 
                and lifetime_value >= 5000 then 'VIP'
            when days_since_last_order <= 90 
                and total_orders >= 5 
                and lifetime_value >= 1000 then 'Loyal'
            when days_since_last_order <= 180 then 'Active'
            else 'At Risk'
        end as customer_tier
        
    from customer_metrics
)

select * from segments
```

## What Belongs in Silver Layer

### ✅ Include in Intermediate Models

- **Joins between staging models**
- **Aggregations and calculations**
- **Business logic and rules**
- **Data enrichment**
- **Window functions**
- **Complex transformations**
- **Reusable components**

### ❌ Don't Include in Intermediate Models

- **Direct source references** (use staging instead)
- **Final presentation logic** (belongs in gold)
- **Simple pass-through** (use ephemeral staging)
- **BI tool-specific formatting** (belongs in gold)

## Testing Intermediate Models

```yaml
# models/silver/_models.yml
models:
  - name: int_customers__with_orders
    description: "Customer enrichment with order metrics"
    columns:
      - name: customer_id
        description: "Primary key"
        tests:
          - not_null
          - unique
      
      - name: total_orders
        description: "Count of customer orders"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
      
      - name: lifetime_value
        description: "Total customer spend"
        tests:
          - not_null
```

## Complexity Levels

### Crawl (Simple Transformations)

**Characteristics:**
- Basic aggregations
- Simple joins
- Minimal business logic

**Example:**
```sql
-- models/silver/crawl/clean_nations.sql
{{ config(materialized='ephemeral') }}

with nations as (
    select * from {{ ref('stg_nations') }}
),

regions as (
    select * from {{ ref('stg_regions') }}
),

final as (
    select
        n.nation_id,
        n.nation_name,
        r.region_name,
        n.nation_comment
    from nations n
    join regions r on n.region_id = r.region_id
)

select * from final
```

### Walk (Business Logic)

**Characteristics:**
- Multiple joins
- Aggregations with CTEs
- Business rules
- Calculated metrics

**Example:** See Pattern 1 (Customer Enrichment) above

### Run (Complex Transformations)

**Characteristics:**
- Window functions
- Complex CTEs
- Advanced analytics
- Python models

**Example:** See Pattern 3 (Time-Based Aggregations) above

## Best Practices

### 1. Use CTE Pattern

```sql
with
import_cte as (
    select * from {{ ref('stg_source') }}
),

logical_cte as (
    -- Business logic here
),

final as (
    select * from logical_cte
)

select * from final
```

### 2. Add Metadata

```sql
select
    *,
    current_timestamp() as dbt_updated_at,
    '{{ run_started_at }}' as dbt_run_started_at
from final
```

### 3. Use Descriptive Names

```sql
-- ✅ Good: Clear purpose
int_customers__with_order_metrics.sql
int_products__performance_summary.sql

-- ❌ Bad: Vague naming
int_customer_data.sql
intermediate_products.sql
```

### 4. Document Complex Logic

```sql
-- Calculate customer lifetime value using all completed orders
-- Excludes cancelled and returned orders
-- Currency conversion applied at order date exchange rate
with customer_ltv as (
    select
        customer_id,
        sum(order_total * exchange_rate) as lifetime_value_usd
    from orders
    where order_status not in ('cancelled', 'returned')
    group by customer_id
)
```

## Troubleshooting

### Issue: Model takes too long to run
**Solution:** Change from ephemeral to table materialization

### Issue: Circular dependency detected
**Solution:** Review model dependencies, ensure proper layer separation

### Issue: Business logic duplicated across models
**Solution:** Extract common logic into reusable intermediate model

---

**Related Documentation:**
- `STAGING_MODELS.md` - Bronze layer patterns
- `MARTS_MODELS.md` - Gold layer patterns
- `MATERIALIZATIONS.md` - Choosing materializations
- `PROJECT_STRUCTURE.md` - Medallion architecture

