# Medallion Architecture Project Structure

## Three-Layer Medallion Architecture

The medallion architecture organizes data models into three layers of increasing refinement:

### Bronze Layer: Staging Models

**Purpose**: One-to-one relationship with source systems, basic data cleaning

**Naming**: `stg_{source_name}__{table_name}`

**Materialization**: `ephemeral` (compiled as CTEs)

**Examples**:
```
bronze/
├── crawl/
│   ├── stg_tpc_h__customers.sql
│   ├── stg_tpc_h__orders.sql
│   └── stg_tpc_h__nations.sql
├── walk/
│   ├── stg_tpc_h__lineitem.sql
│   └── stg_salesforce__accounts.sql
└── run/
    └── stg_orders_incremental.sql
```

**Rules**:
- ✅ One source → One staging model
- ✅ Light transformations only (rename, cast, clean)
- ❌ No joins between sources
- ❌ No business logic

### Silver Layer: Intermediate Transformations

**Purpose**: Reusable business logic and complex transformations

**Naming**: `int_{entity}__{description}`

**Materialization**: `ephemeral` (reusable logic) or `table` (complex computations)

**Examples**:
```
silver/
├── crawl/
│   └── clean_nations.sql
├── walk/
│   ├── int_customers__with_orders.sql
│   └── customer_segments.sql
└── run/
    ├── int_fx_rates__daily.sql
    └── customer_clustering.py
```

**Rules**:
- ✅ Reference staging + other intermediates
- ✅ Contains business logic and aggregations
- ✅ Reusable across multiple marts
- ❌ No direct source references

### Gold Layer: Business-Ready Marts

**Purpose**: Final data products for consumption

**Naming**: `dim_{entity}` (dimensions), `fct_{process}` (facts)

**Materialization**: `table` (dimensions) or `incremental` (facts)

**Examples**:
```
gold/
├── crawl/
│   ├── dim_current_year_orders.sql
│   └── nation_summary.sql
├── walk/
│   ├── dim_customers.sql
│   ├── dim_orders.sql
│   └── customer_insights.sql
└── run/
    ├── fct_order_lines.sql
    └── executive_dashboard.sql
```

**Rules**:
- ✅ Reference staging, intermediate, other marts
- ✅ Contains final business logic
- ✅ Optimized for query performance
- ✅ Well-documented for business users

## Complexity Levels

Each layer contains models at three complexity levels:

**🥉 Crawl (Beginner)**
- Basic staging and simple transformations
- Simple aggregations and summaries
- Few dependencies
- Easy to understand

**🥈 Walk (Intermediate)**
- Complex staging with composite keys
- Business logic and enrichment
- Multiple joins and aggregations
- Some advanced SQL features

**🥇 Run (Advanced)**
- Complex transformations and analytics
- Incremental loading and snapshots
- Python models and ML features
- Advanced Jinja and macros

## Configuration in dbt_project.yml

```yaml
models:
  your_project:
    +materialized: view
    
    bronze:
      +materialized: ephemeral
      +tags: ["bronze", "staging"]
      +schema: bronze
    
    silver:
      +tags: ["silver"]
      +schema: silver
    
    gold:
      +materialized: table
      +tags: ["gold", "marts"]
      +schema: gold
```

## Critical Architectural Rules

Always enforce these rules:

1. ✅ **No Direct Joins to Source** - Models reference staging (`ref('stg_*')`), never `source()` directly
2. ✅ **One-to-One Staging** - Each source table has exactly ONE staging model
3. ✅ **Proper Layering** - Clear flow: staging → intermediate → marts
4. ✅ **Standardized Naming** - Consistent `stg_`, `int_`, `dim_`, `fct_` prefixes
5. ✅ **Use ref() and source()** - No hard-coded table references
6. ✅ **Folder-Level Configuration** - Set common settings in dbt_project.yml

## Code Examples by Layer

### Bronze Layer Example
```sql
-- models/bronze/stg_tpc_h__customers.sql
{{ config(materialized='ephemeral') }}

with source as (
    select * from {{ source('tpc_h', 'customer') }}
),

renamed as (
    select
        c_custkey as customer_id,
        c_name as customer_name,
        c_address as customer_address,
        c_nationkey as nation_id,
        c_phone as phone_number,
        c_acctbal as account_balance,
        current_timestamp() as dbt_loaded_at
    from source
)

select * from renamed
```

### Silver Layer Example
```sql
-- models/silver/int_customers__with_orders.sql
{{ config(materialized='ephemeral') }}

with customers as (
    select * from {{ ref('stg_tpc_h__customers') }}
),

orders as (
    select * from {{ ref('stg_tpc_h__orders') }}
),

aggregated as (
    select
        customers.customer_id,
        customers.customer_name,
        count(orders.order_id) as total_orders,
        sum(orders.total_price) as lifetime_value,
        min(orders.order_date) as first_order_date,
        max(orders.order_date) as most_recent_order_date
    from customers
    left join orders on customers.customer_id = orders.customer_id
    group by customers.customer_id, customers.customer_name
)

select * from aggregated
```

### Gold Layer Example (Dimension)
```sql
-- models/gold/dim_customers.sql
{{ config(materialized='table') }}

with customers as (
    select * from {{ ref('int_customers__with_orders') }}
),

final as (
    select
        customers.customer_id,
        customers.customer_name,
        customers.total_orders,
        customers.lifetime_value,
        customers.first_order_date,
        customers.most_recent_order_date,
        
        -- Business classification
        case 
            when customers.lifetime_value >= 5000 then 'gold'
            when customers.lifetime_value >= 1000 then 'silver'
            else 'bronze'
        end as customer_tier,
        
        current_timestamp() as dbt_updated_at
        
    from customers
)

select * from final
```

### Gold Layer Example (Fact - Incremental)
```sql
-- models/gold/fct_orders.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail'
) }}

with orders as (
    select * from {{ ref('stg_tpc_h__orders') }}
    
    {% if is_incremental() %}
        where order_date >= (select max(order_date) from {{ this }})
    {% endif %}
)

select
    order_id,
    customer_id,
    order_date,
    order_status,
    total_price,
    priority,
    current_timestamp() as dbt_updated_at
from orders
```

## Testing by Layer

### Bronze Layer Testing
```yaml
# models/bronze/_models.yml
models:
  - name: stg_tpc_h__customers
    columns:
      - name: customer_id
        tests:
          - not_null
          - unique
```

### Silver Layer Testing
```yaml
# models/silver/_models.yml
models:
  - name: int_customers__with_orders
    columns:
      - name: customer_id
        tests:
          - not_null
          - unique
      - name: total_orders
        tests:
          - not_null
```

### Gold Layer Testing (with dbt_constraints)
```yaml
# models/gold/_models.yml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - dbt_constraints.primary_key
      
      - name: customer_tier
        tests:
          - accepted_values:
              values: ['bronze', 'silver', 'gold']
  
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

## Tag Inheritance Strategy

**✅ LEVERAGE: dbt's additive tag inheritance**

Tags accumulate hierarchically per the [dbt documentation](https://docs.getdbt.com/reference/resource-configs/tags). Child folders inherit all parent tags automatically.

```yaml
# ✅ GOOD: Avoid duplicate tags
bronze:
  +tags: ["bronze", "staging"]
  crawl:
    +tags: ["crawl", "beginner"]  # Inherits: bronze, staging, crawl, beginner

# ❌ BAD: Redundant parent tags
bronze:
  +tags: ["bronze", "staging"] 
  crawl:
    +tags: ["bronze", "staging", "crawl", "beginner"]  # Duplicates parent tags
```

**Common Selection Patterns:**
```bash
dbt run --select tag:bronze tag:crawl  # Beginner bronze models
dbt run --select tag:gold tag:run      # Advanced gold models
```

**Best Practices:**
- Only define tags at the folder level where they're introduced
- Let child folders inherit parent tags automatically
- Use tag combinations for precise model selection
- Avoid repeating inherited tags in child configurations

---

## Additional Resources

- **`STAGING_MODELS.md`** - Detailed bronze layer patterns
- **`INTERMEDIATE_MODELS.md`** - Silver layer transformation patterns
- **`MARTS_MODELS.md`** - Gold layer dimension and fact patterns
- **`MATERIALIZATIONS.md`** - Choosing the right materialization
- **`TESTING_STRATEGY.md`** - Comprehensive testing guide
