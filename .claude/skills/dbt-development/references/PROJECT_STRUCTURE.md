# dbt Project Structure & Layer Models

## Overview

The medallion architecture organizes data models into three layers of increasing refinement: Bronze (staging), Silver (intermediate), and Gold (marts). Each layer has specific naming conventions, materialization strategies, and transformation patterns.

**Official dbt Documentation**: [How we structure our dbt projects](https://docs.getdbt.com/guides/best-practices/how-we-structure/1-guide-overview)

---

## Critical Architectural Rules

Always enforce these patterns:

1. ✅ **No Direct Joins to Source** - Models reference staging (`ref('stg_*')`), never `source()` directly
2. ✅ **One-to-One Staging** - Each source table has exactly ONE staging model
3. ✅ **Proper Layering** - Clear flow: staging → intermediate → marts
4. ✅ **Standardized Naming** - Consistent `stg_`, `int_`, `dim_`, `fct_` prefixes
5. ✅ **Use ref() and source()** - No hard-coded table references
6. ✅ **Folder-Level Configuration** - Set common settings in dbt_project.yml

---

## Bronze Layer: Staging Models

**Purpose**: One-to-one relationship with source tables. Light cleaning and standardization only.

**Materialization**: `ephemeral` (compiled as CTEs)

**Naming**: `stg_{source}__{table}.sql`

### Template
```sql
-- models/bronze/stg_tpc_h__customers.sql
{{ config(materialized='ephemeral') }}

select
    -- Primary key (renamed)
    c_custkey as customer_id,
    
    -- Attributes (cast and renamed)
    c_name as customer_name,
    c_address as customer_address,
    c_phone as phone_number,
    c_acctbal as account_balance,
    
    -- Metadata
    current_timestamp() as dbt_loaded_at
    
from {{ source('tpc_h', 'customer') }}
```

### Rules

✅ **DO**:
- One source table → One staging model
- Reference sources using `{{ source() }}`
- Rename columns to standard naming
- Cast data types
- Basic cleaning (trim, upper/lower)

❌ **DON'T**:
- Join between sources
- Add business logic
- Aggregate data
- Hard-code table names

### Testing
```yaml
models:
  - name: stg_tpc_h__customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
```

---

## Silver Layer: Intermediate Models

**Purpose**: Reusable business logic and complex transformations. Sits between staging and marts.

**Materialization**: `ephemeral` (reusable logic) or `table` (complex computations)

**Naming**: `int_{entity}__{description}.sql`

### Template
```sql
-- models/silver/int_customers__with_orders.sql
{{ config(materialized='ephemeral') }}

with customers as (
    select * from {{ ref('stg_tpc_h__customers') }}
),

orders as (
    select * from {{ ref('stg_tpc_h__orders') }}
),

customer_metrics as (
    select
        customer_id,
        count(*) as total_orders,
        sum(order_total) as lifetime_value,
        min(order_date) as first_order_date
    from orders
    group by customer_id
)

select
    c.customer_id,
    c.customer_name,
    coalesce(m.total_orders, 0) as total_orders,
    coalesce(m.lifetime_value, 0) as lifetime_value,
    m.first_order_date
from customers c
left join customer_metrics m on c.customer_id = m.customer_id
```

### Rules

✅ **DO**:
- Reference staging + other intermediate models
- Add business logic and aggregations
- Create reusable components
- Use CTEs for clarity

❌ **DON'T**:
- Reference sources directly
- Add final presentation logic
- Create one-time-use models

### Testing
```yaml
models:
  - name: int_customers__with_orders
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
      - name: total_orders
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
```

---

## Gold Layer: Marts Models

**Purpose**: Business-ready data products optimized for BI tools and end users.

**Materialization**: `table` (dimensions) or `incremental` (large facts)

**Naming**: `dim_{entity}` (dimensions), `fct_{process}` (facts)

### Dimension Template
```sql
-- models/gold/dim_customers.sql
{{ config(materialized='table') }}

with customers as (
    select * from {{ ref('int_customers__with_orders') }}
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
    
    -- Business classification
    case 
        when lifetime_value >= 5000 then 'gold'
        when lifetime_value >= 1000 then 'silver'
        else 'bronze'
    end as customer_tier,
    
    -- Metadata
    current_timestamp() as dbt_updated_at
from customers
```

### Fact Template
```sql
-- models/gold/fct_orders.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    cluster_by=['order_date', 'customer_id']
) }}

select
    order_id,
    customer_id,
    order_date,
    order_status,
    order_total,
    current_timestamp() as dbt_updated_at
from {{ ref('stg_tpc_h__orders') }}

{% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

### Rules

✅ **DO**:
- Reference staging, intermediate, and other marts
- Add final business logic
- Optimize for query performance (clustering)
- Test with dbt_constraints
- Document for business users

❌ **DON'T**:
- Reference sources directly
- Create unnecessary complexity

### Testing (with dbt_constraints)
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key

  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - dbt_constraints.primary_key
      - name: customer_id
        tests:
          - dbt_constraints.foreign_key:
              pk_table_name: ref('dim_customers')
              pk_column_name: customer_id
```

---

## Naming Conventions Summary

| Layer | Prefix | Example | Purpose |
|-------|--------|---------|---------|
| **Bronze** | `stg_` | `stg_tpc_h__customers` | Clean source data |
| **Silver** | `int_` | `int_customers__with_orders` | Business logic |
| **Gold - Dimensions** | `dim_` | `dim_customers` | Business entities |
| **Gold - Facts** | `fct_` | `fct_orders` | Business events |

---

## Configuration in dbt_project.yml

```yaml
models:
  your_project:
    bronze:
      +materialized: ephemeral
      +tags: ["bronze", "staging"]
      +schema: bronze
    
    silver:
      +materialized: ephemeral
      +tags: ["silver"]
      +schema: silver
    
    gold:
      +materialized: table
      +tags: ["gold", "marts"]
      +schema: gold
```

---

## Tag Inheritance Strategy

✅ **LEVERAGE**: dbt's additive tag inheritance

Tags accumulate hierarchically per the [dbt documentation](https://docs.getdbt.com/reference/resource-configs/tags). Child folders inherit all parent tags automatically.

```yaml
# ✅ GOOD: Avoid duplicate tags
bronze:
  +tags: ["bronze", "staging"]
  subfolder:
    +tags: ["subfolder"]  # Inherits: bronze, staging, subfolder

# ❌ BAD: Redundant parent tags
bronze:
  +tags: ["bronze", "staging"] 
  subfolder:
    +tags: ["bronze", "staging", "subfolder"]  # Duplicates parent tags
```

**Common Selection Patterns**:
```bash
dbt run --select tag:bronze     # All bronze models
dbt run --select tag:gold       # All gold models
dbt run --select tag:staging    # Alternative to bronze
```

---

## Folder Structure

```
models/
├── bronze/          # Staging layer - one-to-one with sources
│   ├── stg_tpc_h__customers.sql
│   ├── stg_tpc_h__orders.sql
│   └── stg_tpc_h__lineitem.sql
├── silver/         # Intermediate layer - business logic
│   ├── int_customers__with_orders.sql
│   ├── int_fx_rates__daily.sql
│   └── customer_segments.sql
└── gold/           # Marts layer - business-ready analytics
    ├── dim_customers.sql
    ├── dim_products.sql
    ├── fct_orders.sql
    └── fct_order_lines.sql
```

---

## Related Documentation

- [Official dbt Docs: Best Practices](https://docs.getdbt.com/guides/best-practices)
- `MATERIALIZATIONS.md` - Choosing the right materialization
- `TESTING_STRATEGY.md` - dbt_constraints testing
- `NAMING_CONVENTIONS.md` - Complete naming standards
- `PERFORMANCE_OPTIMIZATION.md` - Snowflake optimizations
