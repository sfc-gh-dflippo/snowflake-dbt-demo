# Gold Layer: Marts Models Guide

## Purpose

Marts models (gold layer) are business-ready data products optimized for consumption by BI tools, analysts, and business users. They represent the final transformation layer with complete business logic, documentation, and quality enforcement.

## Core Principles

✅ **Business-ready data products** for end users  
✅ **Fully tested and documented** with dbt_constraints  
✅ **Optimized for query performance** (clustering, partitioning)  
✅ **Reference staging, intermediate, and other marts**  
✅ **Named for business clarity** (`dim_` for dimensions, `fct_` for facts)  

## Model Types

### Dimensions (`dim_`)

Slowly changing attributes about business entities.

**Characteristics:**
- One row per entity
- Descriptive attributes
- Foreign keys to other dimensions
- SCD Type 1 or Type 2
- Table materialization

### Facts (`fct_`)

Measurable events or transactions.

**Characteristics:**
- Many rows (potentially millions+)
- Foreign keys to dimensions
- Numeric measures
- Date/time stamps
- Incremental materialization for large tables

## Naming Convention

```
dim_{entity}.sql  # Dimensions
fct_{process}.sql # Facts
```

**Examples:**
- `dim_customers.sql` - Customer dimension
- `dim_products.sql` - Product catalog
- `dim_calendar_day.sql` - Date dimension
- `fct_orders.sql` - Order transactions
- `fct_order_lines.sql` - Order line items

## Dimension Model Patterns

### Simple Dimension (Type 1)

```sql
-- models/gold/dim_customers.sql
{{ config(materialized='table') }}

with customers as (
    select * from {{ ref('int_customers__with_orders') }}
),

final as (
    select
        -- Primary key
        customer_id,
        
        -- Attributes
        customer_name,
        customer_email,
        customer_phone,
        customer_address,
        customer_city,
        customer_state,
        customer_country,
        
        -- Metrics
        total_orders,
        lifetime_value,
        avg_order_value,
        
        -- Business segments
        customer_tier,
        customer_status,
        
        -- Dates
        first_order_date,
        most_recent_order_date,
        signup_date,
        
        -- Metadata
        current_timestamp() as dbt_updated_at
        
    from customers
)

select * from final
```

### SCD Type 2 Dimension (See SNAPSHOTS.md)

For tracking historical changes, use dbt snapshots instead of complex SQL logic.

### Dimension with Ghost Keys

```sql
-- models/gold/dim_calendar_day.sql
{{ config(
    materialized='table',
    pre_hook="delete from {{ this }} where date_day = '1900-01-01'"
) }}

with date_spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="to_date('2020-01-01', 'YYYY-MM-DD')",
        end_date="dateadd(year, 1, current_date())"
    ) }}
),

final as (
    select
        cast(date_day as date) as date_day,
        extract(year from date_day) as year_number,
        extract(month from date_day) as month_number,
        extract(day from date_day) as day_of_month,
        extract(dayofweek from date_day) as day_of_week,
        extract(quarter from date_day) as quarter_number,
        case when extract(dayofweek from date_day) in (0, 6) then true else false end as is_weekend
    from date_spine
    
    union all
    
    -- Ghost key for missing dates
    select
        cast('1900-01-01' as date) as date_day,
        1900 as year_number,
        1 as month_number,
        1 as day_of_month,
        0 as day_of_week,
        1 as quarter_number,
        false as is_weekend
)

select * from final
```

## Fact Model Patterns

### Fact Table (Incremental)

```sql
-- models/gold/fct_orders.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    cluster_by=['order_date', 'customer_id']
) }}

with orders as (
    select * from {{ ref('stg_orders') }}
    
    {% if is_incremental() %}
        where order_date >= (select max(order_date) from {{ this }})
    {% endif %}
),

final as (
    select
        -- Primary key
        order_id,
        
        -- Foreign keys
        customer_id,
        product_id,
        sales_rep_id,
        
        -- Degenerate dimensions
        order_number,
        order_status,
        payment_method,
        
        -- Measures
        order_quantity,
        unit_price,
        discount_amount,
        tax_amount,
        order_total,
        
        -- Dates
        order_date,
        ship_date,
        delivery_date,
        
        -- Metadata
        current_timestamp() as dbt_updated_at
        
    from orders
)

select * from final
```

### Fact Line Items (Incremental with Surrogate Key)

```sql
-- models/gold/fct_order_lines.sql
{{ config(
    materialized='incremental',
    unique_key='order_line_id',
    cluster_by=['order_date', 'customer_id']
) }}

with order_lines as (
    select * from {{ ref('stg_order_lines') }}
    
    {% if is_incremental() %}
        where order_date >= dateadd(day, -3, (select max(order_date) from {{ this }}))
    {% endif %}
),

final as (
    select
        -- Surrogate key
        {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_id,
        
        -- Natural key
        order_id,
        line_number,
        
        -- Foreign keys
        customer_id,
        product_id,
        warehouse_id,
        
        -- Measures
        quantity,
        unit_price,
        discount_pct,
        line_total,
        
        -- Calculated measures
        quantity * unit_price as gross_amount,
        quantity * unit_price * discount_pct as discount_amount,
        quantity * unit_price * (1 - discount_pct) as net_amount,
        
        -- Dates
        order_date,
        ship_date,
        
        -- Metadata
        current_timestamp() as dbt_updated_at
        
    from order_lines
)

select * from final
```

### Aggregated Fact (Snapshot Fact)

```sql
-- models/gold/fct_daily_sales_summary.sql
{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('fct_orders') }}
),

daily_summary as (
    select
        order_date as fact_date,
        
        -- Dimensions for drill-down
        customer_id,
        product_category_id,
        sales_region_id,
        
        -- Aggregated measures
        count(distinct order_id) as order_count,
        count(distinct customer_id) as customer_count,
        sum(order_total) as total_revenue,
        avg(order_total) as avg_order_value,
        sum(quantity) as total_units_sold,
        
        current_timestamp() as dbt_updated_at
        
    from orders
    group by order_date, customer_id, product_category_id, sales_region_id
)

select * from daily_summary
```

## Testing Marts with dbt_constraints

### Dimension Testing

```yaml
# models/gold/_models.yml
models:
  - name: dim_customers
    description: "Customer dimension table"
    columns:
      - name: customer_id
        description: "Primary key"
        tests:
          - dbt_constraints.primary_key
      
      - name: customer_email
        description: "Customer email (business unique key)"
        tests:
          - dbt_constraints.unique_key
      
      - name: customer_tier
        tests:
          - accepted_values:
              values: ['bronze', 'silver', 'gold', 'platinum']
      
      - name: customer_status
        tests:
          - accepted_values:
              values: ['active', 'inactive', 'suspended']
```

### Fact Testing

```yaml
models:
  - name: fct_orders
    description: "Order fact table"
    columns:
      - name: order_id
        description: "Primary key"
        tests:
          - dbt_constraints.primary_key
      
      - name: customer_id
        description: "Foreign key to dim_customers"
        tests:
          - not_null
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_customers')
              pk_column_name: customer_id
      
      - name: product_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_products')
              pk_column_name: product_id
      
      - name: order_total
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

## Performance Optimization

### Clustering Keys

```sql
{{ config(
    materialized='table',
    cluster_by=['order_date', 'customer_id']
) }}
```

**Best Practices:**
- Use 1-4 columns
- Order by cardinality (low to high)
- Include common filter columns
- Include join key columns

### Partitioning (BigQuery/Databricks)

```sql
{{ config(
    materialized='table',
    partition_by={
        'field': 'order_date',
        'data_type': 'date',
        'granularity': 'day'
    }
) }}
```

## Data Contracts

```yaml
models:
  - name: dim_customers
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: number
        constraints:
          - type: not_null
          - type: primary_key
      
      - name: customer_name
        data_type: varchar(255)
        constraints:
          - type: not_null
      
      - name: lifetime_value
        data_type: number(10,2)
```

## Folder Organization

```
gold/
├── dimensions/
│   ├── dim_customers.sql
│   ├── dim_products.sql
│   └── dim_calendar_day.sql
├── facts/
│   ├── fct_orders.sql
│   ├── fct_order_lines.sql
│   └── fct_transactions.sql
└── aggregates/
    ├── fct_daily_sales_summary.sql
    └── fct_monthly_customer_summary.sql
```

## Complexity Levels

### Crawl (Simple Aggregations)

```sql
-- models/gold/crawl/dim_current_year_orders.sql
{{ config(materialized='table') }}

select
    order_id,
    customer_id,
    order_date,
    order_total
from {{ ref('stg_orders') }}
where extract(year from order_date) = extract(year from current_date())
```

### Walk (Complete Dimensions/Facts)

Complete dimension and fact examples shown above.

### Run (Advanced Analytics)

```sql
-- models/gold/run/executive_dashboard.sql
{{ config(
    materialized='table',
    cluster_by=['report_date']
) }}

with orders as (
    select * from {{ ref('fct_orders') }}
),

customers as (
    select * from {{ ref('dim_customers') }}
),

kpis as (
    select
        current_date() as report_date,
        
        -- Revenue metrics
        sum(order_total) as total_revenue,
        avg(order_total) as avg_order_value,
        count(distinct order_id) as order_count,
        
        -- Customer metrics
        count(distinct customer_id) as active_customers,
        sum(order_total) / nullif(count(distinct customer_id), 0) as revenue_per_customer,
        
        -- Growth metrics
        sum(case when order_date >= dateadd(day, -30, current_date()) then order_total else 0 end) as revenue_last_30_days,
        sum(case when order_date >= dateadd(day, -60, current_date()) 
                  and order_date < dateadd(day, -30, current_date()) 
             then order_total else 0 end) as revenue_prior_30_days
        
    from orders
)

select
    *,
    (revenue_last_30_days - revenue_prior_30_days) / nullif(revenue_prior_30_days, 0) * 100 as revenue_growth_pct
from kpis
```

## Best Practices

### 1. Document for Business Users

```yaml
models:
  - name: dim_customers
    description: |
      **Customer Dimension Table**
      
      Contains one row per customer with their current attributes and lifetime metrics.
      
      **Grain**: One row per customer
      **Refresh**: Daily at 6 AM UTC
      **Use Cases**: Customer analysis, segmentation, lifetime value reporting
```

### 2. Include Business Metrics

```sql
-- Add calculated business metrics in gold layer
case 
    when lifetime_value >= 10000 then 'VIP'
    when lifetime_value >= 5000 then 'High Value'
    when lifetime_value >= 1000 then 'Medium Value'
    else 'Low Value'
end as value_segment
```

### 3. Add Audit Columns

```sql
select
    *,
    current_timestamp() as dbt_updated_at,
    '{{ run_started_at }}' as dbt_run_started_at,
    '{{ invocation_id }}' as dbt_invocation_id
from final
```

### 4. Use Descriptive Aliases

```sql
-- ✅ Good: Business-friendly names
total_orders as order_count,
lifetime_value as customer_ltv_usd,
first_order_date as customer_since_date

-- ❌ Bad: Technical abbreviations
tot_ord as tc,
ltv as lv,
f_ord_dt as fod
```

## Troubleshooting

### Issue: Fact table growing too large
**Solution:** Use incremental materialization with appropriate unique_key

### Issue: Query performance degrading
**Solution:** Add clustering keys, review join patterns, consider aggregated facts

### Issue: Foreign key test failures
**Solution:** Check for orphaned records, ensure dimension is populated first

---

**Related Documentation:**
- `STAGING_MODELS.md` - Bronze layer patterns
- `INTERMEDIATE_MODELS.md` - Silver layer patterns
- `INCREMENTAL_MODELS.md` - Incremental strategies
- `TESTING_STRATEGY.md` - dbt_constraints testing
- `PERFORMANCE_OPTIMIZATION.md` - Query optimization

