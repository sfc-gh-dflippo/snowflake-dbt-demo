---
name: dbt-modeling
description:
  Writing dbt models with proper CTE patterns, SQL structure, and layer-specific templates. Use this
  skill when writing or refactoring dbt models, implementing CTE patterns, creating
  staging/intermediate/mart models, or ensuring proper SQL structure and dependencies.
---

# dbt Modeling

## Purpose

Transform AI agents into experts on writing production-quality dbt models, providing guidance on CTE
patterns, SQL structure, and best practices for creating maintainable and performant data models
across all medallion architecture layers.

## When to Use This Skill

Activate this skill when users ask about:

- Writing or refactoring dbt models
- Implementing CTE (Common Table Expression) patterns
- Creating staging, intermediate, or mart models
- Structuring SQL for readability and maintainability
- Implementing proper model dependencies with ref() and source()
- Converting existing SQL to dbt model format
- Debugging model SQL structure issues

---

## CTE Pattern Structure

All dbt models should follow this consistent CTE pattern for readability and maintainability:

```sql
-- Import CTEs (staging and intermediate models)
with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

-- Logical CTEs (business logic)
customer_metrics as (
    select
        customer_id,
        count(*) as order_count,
        sum(order_amount) as lifetime_value
    from orders
    group by customer_id
),

-- Final CTE (column selection and standardization)
final as (
    select
        -- Primary key
        customers.customer_id,

        -- Attributes
        customers.customer_name,
        customers.customer_email,

        -- Metrics
        coalesce(customer_metrics.order_count, 0) as lifetime_orders,
        coalesce(customer_metrics.lifetime_value, 0) as lifetime_value,

        -- Metadata
        current_timestamp() as dbt_updated_at

    from customers
    left join customer_metrics
        on customers.customer_id = customer_metrics.customer_id
)

select * from final
```

**Official dbt Documentation**:
[How we structure our dbt projects](https://docs.getdbt.com/guides/best-practices/how-we-structure/1-guide-overview)

---

## Bronze Layer: Staging Model Template

**Purpose**: One-to-one with source tables. Clean and standardize only.

**Materialization**: `ephemeral` (set at folder level in dbt_project.yml)

### Basic Staging Model

```sql
-- models/bronze/stg_salesforce__accounts.sql

select
    -- Primary key
    id as account_id,

    -- Attributes
    name as account_name,
    type as account_type,
    industry,

    -- Standardized fields
    upper(trim(email)) as email_clean,
    cast(annual_revenue as number) as annual_revenue,

    -- Metadata
    current_timestamp() as dbt_loaded_at

from {{ source('salesforce', 'accounts') }}
```

### Staging Model with Light Cleaning

```sql
-- models/bronze/stg_ecommerce__customers.sql

select
    -- Primary key
    customer_id,

    -- Attributes (cleaned)
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    lower(trim(email)) as email,

    -- Phone standardization
    regexp_replace(phone, '[^0-9]', '') as phone_clean,

    -- Boolean conversions
    case
        when status = 'active' then true
        else false
    end as is_active,

    -- Date standardization
    cast(created_at as timestamp) as created_at,

    -- Metadata
    current_timestamp() as dbt_loaded_at

from {{ source('ecommerce', 'customers') }}
```

### Staging Rules

✅ **DO**:

- Use `{{ source() }}` for source references
- Rename columns to standard naming conventions
- Cast data types explicitly
- Clean data (trim, upper/lower, standardize formats)
- Add metadata columns (dbt_loaded_at, dbt_updated_at)

❌ **DON'T**:

- Join multiple sources
- Add business logic or calculations
- Aggregate or group data
- Filter rows (except for obvious bad data)
- Hard-code table names

---

## Silver Layer: Intermediate Model Template

**Purpose**: Reusable business logic, enrichment, and complex transformations.

**Materialization**: `ephemeral` or `table` (set at folder level, override if needed)

### Basic Intermediate Model

```sql
-- models/silver/int_customers__with_orders.sql

with customers as (
    select * from {{ ref('stg_salesforce__customers') }}
),

orders as (
    select * from {{ ref('stg_ecommerce__orders') }}
),

customer_order_metrics as (
    select
        customer_id,
        count(distinct order_id) as total_orders,
        sum(order_amount) as lifetime_value,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date
    from orders
    group by customer_id
),

final as (
    select
        c.customer_id,
        c.customer_name,
        c.customer_email,

        coalesce(m.total_orders, 0) as total_orders,
        coalesce(m.lifetime_value, 0) as lifetime_value,
        m.first_order_date,
        m.last_order_date,

        datediff(day, m.first_order_date, m.last_order_date) as customer_tenure_days

    from customers c
    left join customer_order_metrics m
        on c.customer_id = m.customer_id
)

select * from final
```

### Complex Intermediate Model with Business Logic

```sql
-- models/silver/int_customers__segmented.sql

with customer_metrics as (
    select * from {{ ref('int_customers__with_orders') }}
),

rfm_scores as (
    select
        customer_id,

        -- Recency (days since last order)
        datediff(day, last_order_date, current_date()) as recency_days,

        -- Frequency
        total_orders as frequency,

        -- Monetary
        lifetime_value as monetary,

        -- Quartile scoring
        ntile(4) over (order by datediff(day, last_order_date, current_date()) desc) as recency_score,
        ntile(4) over (order by total_orders) as frequency_score,
        ntile(4) over (order by lifetime_value) as monetary_score

    from customer_metrics
    where last_order_date is not null
),

final as (
    select
        customer_id,
        recency_days,
        frequency,
        monetary,
        recency_score,
        frequency_score,
        monetary_score,

        -- RFM segment
        case
            when recency_score >= 3 and frequency_score >= 3 and monetary_score >= 3 then 'Champions'
            when recency_score >= 3 and frequency_score >= 2 then 'Loyal Customers'
            when recency_score >= 3 and monetary_score >= 3 then 'Big Spenders'
            when recency_score <= 2 and frequency_score >= 3 then 'At Risk'
            when recency_score <= 1 then 'Lost'
            else 'Regular'
        end as customer_segment

    from rfm_scores
)

select * from final
```

### Intermediate Rules

✅ **DO**:

- Reference staging and other intermediate models with `{{ ref() }}`
- Add business logic and calculations
- Create reusable components
- Use descriptive CTE names
- Group related logic into CTEs

❌ **DON'T**:

- Reference `{{ source() }}` directly
- Add presentation-layer logic (save for marts)
- Create one-off transformations (ensure reusability)

---

## Gold Layer: Dimension Model Template

**Purpose**: Business entities ready for BI tools.

**Materialization**: `table` (set at folder level)

### Basic Dimension

```sql
-- models/gold/dim_customers.sql

with customers as (
    select * from {{ ref('int_customers__segmented') }}
)

select
    -- Primary key
    customer_id,

    -- Attributes
    customer_name,
    customer_email,

    -- Metrics
    total_orders,
    lifetime_value,
    first_order_date,
    last_order_date,
    customer_tenure_days,

    -- Segmentation
    customer_segment,

    -- Business classification
    case
        when customer_segment = 'Champions' then 'High Value'
        when customer_segment in ('Loyal Customers', 'Big Spenders') then 'Medium Value'
        else 'Low Value'
    end as customer_value_tier,

    -- Flags
    case when last_order_date >= dateadd(day, -90, current_date()) then true else false end as is_active_90d,
    case when total_orders = 1 then true else false end as is_one_time_buyer,

    -- Metadata
    current_timestamp() as dbt_updated_at

from customers
```

### Dimension with Type 0 SCD (Ghost Records)

```sql
-- models/gold/dim_products.sql
-- Includes ghost key for unknown/missing products

with products as (
    select * from {{ ref('int_products__enriched') }}
),

ghost_key as (
    select
        -1 as product_id,
        'Unknown' as product_name,
        'Unknown' as product_category,
        0.00 as product_price,
        false as is_active,
        current_timestamp() as dbt_updated_at
),

final as (
    select * from products
    union all
    select * from ghost_key
)

select * from final
```

### Dimension Rules

✅ **DO**:

- Include primary key as first column
- Add business-friendly attributes
- Include calculated flags and classifications
- Add metadata columns
- Document all columns in schema.yml
- Test with `dbt_constraints.primary_key`

❌ **DON'T**:

- Include transaction-level data (that's for facts)
- Create overly wide tables (be selective)

---

## Gold Layer: Fact Model Template

**Purpose**: Business processes and transactions.

**Materialization**: `table` or `incremental` (override at model level for incremental)

### Basic Fact Table

```sql
-- models/gold/fct_orders.sql

with orders as (
    select * from {{ ref('stg_ecommerce__orders') }}
),

customers as (
    select customer_id from {{ ref('dim_customers') }}
),

products as (
    select product_id from {{ ref('dim_products') }}
)

select
    -- Primary key
    orders.order_id,

    -- Foreign keys
    coalesce(customers.customer_id, -1) as customer_id,  -- Ghost key for unknown
    coalesce(products.product_id, -1) as product_id,

    -- Attributes
    orders.order_date,
    orders.order_status,

    -- Metrics
    orders.order_quantity,
    orders.order_amount,
    orders.discount_amount,
    orders.tax_amount,
    orders.total_amount,

    -- Metadata
    current_timestamp() as dbt_updated_at

from orders
left join customers on orders.customer_id = customers.customer_id
left join products on orders.product_id = products.product_id
```

### Incremental Fact Table

```sql
-- models/gold/fct_order_lines.sql
{{ config(
    materialized='incremental',
    unique_key='order_line_id',
    incremental_strategy='merge',
    merge_exclude_columns=['dbt_inserted_at'],
    cluster_by=['order_date']
) }}

with order_lines as (
    select * from {{ ref('stg_ecommerce__order_lines') }}
)

select
    -- Primary key
    order_line_id,

    -- Foreign keys
    order_id,
    product_id,
    customer_id,

    -- Attributes
    order_date,
    line_number,

    -- Metrics
    quantity,
    unit_price,
    discount_percent,
    line_total,

    -- Metadata
    {% if is_incremental() %}
        dbt_inserted_at,  -- Preserve from merge_exclude_columns
    {% else %}
        current_timestamp() as dbt_inserted_at,
    {% endif %}
    current_timestamp() as dbt_updated_at

from order_lines

{% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

### Fact Rules

✅ **DO**:

- Include all foreign keys to dimensions
- Use ghost keys (-1) for unknown/missing references
- Include metrics and measures
- Use incremental for large tables (millions+ rows)
- Add clustering keys for large tables
- Test with `dbt_constraints.foreign_key`

❌ **DON'T**:

- Denormalize dimension attributes into facts (use foreign keys)
- Skip foreign key tests

---

## Model Configuration Strategy

### Folder-Level First (in dbt_project.yml)

Most configuration should be at the folder level:

```yaml
models:
  your_project:
    bronze:
      +materialized: ephemeral
      +tags: ["bronze", "staging"]
    silver:
      +materialized: ephemeral
      +tags: ["silver"]
    gold:
      +materialized: table
      +tags: ["gold", "marts"]
```

### Model-Level Only for Unique Requirements

Add `{{ config() }}` ONLY when overriding folder defaults:

```sql
-- Only for incremental-specific settings
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    cluster_by=['order_date']
) }}
```

---

## Common Modeling Patterns

### Handling NULL Values

```sql
-- Use COALESCE for safety
select
    customer_id,
    coalesce(total_orders, 0) as total_orders,
    coalesce(lifetime_value, 0.00) as lifetime_value
from {{ ref('customer_metrics') }}
```

### Window Functions for Ranking

```sql
-- Use QUALIFY in Snowflake for cleaner code
select
    customer_id,
    order_date,
    order_amount,
    row_number() over (partition by customer_id order by order_date desc) as order_rank
from {{ ref('stg_orders') }}
qualify order_rank <= 5  -- Top 5 orders per customer
```

### Conditional Aggregation

```sql
select
    customer_id,
    count(*) as total_orders,
    sum(case when order_status = 'completed' then 1 else 0 end) as completed_orders,
    sum(case when order_status = 'cancelled' then 1 else 0 end) as cancelled_orders
from {{ ref('stg_orders') }}
group by customer_id
```

---

## Helping Users with Modeling

### Strategy for Assisting Users

When users ask for modeling help:

1. **Understand the goal**: What business question does this answer?
2. **Identify the layer**: Bronze/silver/gold based on purpose
3. **Recommend structure**: CTEs, column organization, logic flow
4. **Apply naming conventions**: Proper prefixes and column names
5. **Provide complete example**: Working code they can adapt
6. **Suggest tests**: Appropriate constraints and validations

### Common User Questions

**"How do I write this model?"**

- Identify source data (staging models)
- Break logic into CTEs (import → logic → final)
- Apply column naming standards
- Add appropriate tests

**"How do I join these tables?"**

- Use CTE pattern (import CTEs at top)
- Perform joins in logical CTEs
- Select final columns in final CTE
- Use `ref()` for all dbt model references

**"Should this be ephemeral or table?"**

- Ephemeral: Staging, reusable intermediate logic
- Table: Dimensions, complex silver, production marts
- Incremental: Large facts (millions+ rows)

---

## Related Official Documentation

- [dbt Best Practices: How We Structure Our dbt Projects](https://docs.getdbt.com/guides/best-practices/how-we-structure/1-guide-overview)
- [dbt Docs: Building Models](https://docs.getdbt.com/docs/build/models)
- [dbt Docs: Jinja & Macros](https://docs.getdbt.com/docs/build/jinja-macros)

---

**Goal**: Transform AI agents into expert dbt modelers who write clean, maintainable,
production-quality SQL that follows industry best practices and is easy for teams to understand and
extend.
