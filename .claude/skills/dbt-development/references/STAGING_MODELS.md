# Bronze Layer: Staging Models Guide

## Purpose

Staging models (bronze layer) create a one-to-one relationship with source tables, performing basic cleaning and standardization. They are the **only** models that reference sources directly.

## Core Principles

✅ **One source → One staging model** (no fanout)  
✅ **Ephemeral materialization** (compiled as CTEs)  
✅ **Minimal transformations** (renaming, casting, basic cleaning)  
✅ **No joins** between sources  
✅ **No business logic** or calculations  
✅ **All downstream models reference staging, never sources**

## Naming Convention

```
stg_{source_name}__{table_name}.sql
```

**Examples:**
- `stg_tpc_h__customers.sql` ← Source: tpc_h.customer
- `stg_tpc_h__orders.sql` ← Source: tpc_h.orders
- `stg_salesforce__accounts.sql` ← Source: salesforce.accounts
- `stg_stripe__payments.sql` ← Source: stripe.payments

## Standard Template

```sql
-- models/bronze/stg_{source}__{table}.sql
-- Bronze layer: One-to-one source relationship with {source}.{table}

{{ config(materialized='ephemeral') }}

select
    -- Primary key (renamed)
    original_id as clean_id,
    
    -- Foreign keys (renamed)
    original_fk as clean_fk,
    
    -- Attributes (cast and renamed)
    original_col::varchar as clean_column,
    original_date::date as clean_date,
    
    -- Metadata (preserve or add)
    created_at,
    updated_at
    
from {{ source('source_name', 'table_name') }}
```

## Common Transformations

### Column Renaming
```sql
select
    c_custkey as customer_id,
    c_name as customer_name,
    c_address as customer_address,
    c_phone as customer_phone
from {{ source('tpc_h', 'customer') }}
```

### Type Casting
```sql
select
    order_id,
    order_date::date as order_date,
    order_total::numeric(10,2) as order_total,
    order_status::varchar(20) as order_status
from {{ source('ecommerce', 'orders') }}
```

### Basic Cleaning
```sql
select
    customer_id,
    trim(upper(customer_name)) as customer_name,
    regexp_replace(phone_number, '[^0-9]', '') as phone_number_clean,
    lower(email_address) as email_address
from {{ source('crm', 'customers') }}
```

### Null Handling
```sql
select
    product_id,
    coalesce(product_name, 'Unknown') as product_name,
    coalesce(product_category, 'Uncategorized') as product_category,
    coalesce(unit_price, 0.00) as unit_price
from {{ source('inventory', 'products') }}
```

## Complexity Levels

### Crawl (Simple Staging)

**Characteristics:**
- Simple column renaming
- Basic type casting
- Minimal transformations

**Example:**
```sql
-- models/bronze/crawl/stg_tpc_h__customers.sql
{{ config(materialized='ephemeral') }}

select
    c_custkey as customer_id,
    c_name as customer_name,
    c_address as customer_address,
    c_nationkey as nation_id,
    c_phone as phone_number,
    c_acctbal as account_balance,
    c_mktsegment as market_segment,
    c_comment as comment
from {{ source('tpc_h', 'customer') }}
```

### Walk (Complex Staging)

**Characteristics:**
- Composite keys
- Multiple sources
- Data quality fixes
- More complex transformations

**Example:**
```sql
-- models/bronze/walk/stg_tpc_h__lineitem.sql
{{ config(materialized='ephemeral') }}

select
    -- Composite key
    {{ dbt_utils.generate_surrogate_key(['l_orderkey', 'l_linenumber']) }} as order_line_id,
    
    -- Foreign keys
    l_orderkey as order_id,
    l_partkey as part_id,
    l_suppkey as supplier_id,
    
    -- Line details
    l_linenumber as line_number,
    l_quantity as quantity,
    l_extendedprice as extended_price,
    l_discount as discount_pct,
    l_tax as tax_pct,
    
    -- Calculated fields (keep simple)
    l_extendedprice * (1 - l_discount) as net_price,
    l_extendedprice * (1 - l_discount) * (1 + l_tax) as total_price,
    
    -- Attributes
    l_returnflag as return_flag,
    l_linestatus as line_status,
    l_shipdate::date as ship_date,
    l_commitdate::date as commit_date,
    l_receiptdate::date as receipt_date,
    l_shipinstruct as ship_instructions,
    l_shipmode as ship_mode,
    l_comment as comment
    
from {{ source('tpc_h', 'lineitem') }}
```

### Run (Advanced Staging)

**Characteristics:**
- Incremental loading
- Change data capture (CDC)
- Stream processing
- Advanced data quality

**Example - Incremental Staging:**
```sql
-- models/bronze/run/stg_orders_incremental.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail'
) }}

select
    order_id,
    customer_id,
    order_date::date as order_date,
    order_status,
    order_total::numeric(10,2) as order_total,
    created_at,
    updated_at
    
from {{ source('ecommerce', 'orders') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

**Example - CDC Stream:**
```sql
-- models/bronze/run/customer_cdc_stream.sql
{{ config(
    materialized='table',
    pre_hook="create or replace stream {{ this }}_stream on table {{ source('crm', 'customers') }}"
) }}

select
    customer_id,
    customer_name,
    customer_email,
    metadata$action as dbt_change_type,
    metadata$isupdate as dbt_is_update,
    metadata$row_id as dbt_row_id
from {{ this }}_stream
```

## Testing Strategy

### Primary Key Tests
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

### Referential Integrity (Optional at Bronze)
```yaml
models:
  - name: stg_tpc_h__orders
    columns:
      - name: customer_id
        tests:
          - relationships:
              to: ref('stg_tpc_h__customers')
              field: customer_id
```

### Data Quality Tests
```yaml
models:
  - name: stg_tpc_h__customers
    columns:
      - name: account_balance
        tests:
          - not_null
      - name: market_segment
        tests:
          - accepted_values:
              values: ['AUTOMOBILE', 'BUILDING', 'FURNITURE', 'HOUSEHOLD', 'MACHINERY']
```

## Common Patterns

### Pattern 1: Simple Source Renaming
```sql
select
    original_col_1 as new_col_1,
    original_col_2 as new_col_2
from {{ source('db', 'table') }}
```

### Pattern 2: Type Standardization
```sql
select
    id::bigint as id,
    name::varchar(100) as name,
    created::timestamp as created_at,
    amount::numeric(10,2) as amount
from {{ source('db', 'table') }}
```

### Pattern 3: Composite Key Generation
```sql
select
    {{ dbt_utils.generate_surrogate_key(['col1', 'col2']) }} as composite_id,
    col1,
    col2
from {{ source('db', 'table') }}
```

### Pattern 4: Conditional Cleaning
```sql
select
    customer_id,
    case
        when trim(customer_name) = '' then null
        else trim(customer_name)
    end as customer_name,
    case
        when email like '%@%' then lower(email)
        else null
    end as email_validated
from {{ source('crm', 'customers') }}
```

## What NOT to Do in Staging

❌ **No joins between sources:**
```sql
-- BAD: Don't join sources in staging
select 
    c.*,
    o.order_count
from {{ source('crm', 'customers') }} c
join {{ source('orders', 'order_summary') }} o  -- ❌ Join in staging
  on c.customer_id = o.customer_id
```

❌ **No complex business logic:**
```sql
-- BAD: Complex calculations belong in silver/gold
select
    customer_id,
    sum(order_total) as lifetime_value,  -- ❌ Business logic
    count(*) as order_count,              -- ❌ Aggregation
    case
        when sum(order_total) > 10000 then 'VIP'  -- ❌ Business rule
        else 'Standard'
    end as customer_tier
from {{ source('orders', 'orders') }}
group by customer_id
```

❌ **No hard-coded table names:**
```sql
-- BAD: Always use source() macro
select * from raw.crm.customers  -- ❌ Hard-coded

-- GOOD: Use source() macro
select * from {{ source('crm', 'customers') }}  -- ✅
```

## Best Practices

### 1. Document Source Relationships
```yaml
# models/bronze/_sources.yml
sources:
  - name: tpc_h
    description: TPC-H benchmark data
    database: snowflake_sample_data
    schema: tpch_sf1
    tables:
      - name: customer
        description: Customer master data
        columns:
          - name: c_custkey
            description: Primary key
            tests:
              - not_null
              - unique
```

### 2. Keep Staging Ephemeral
```yaml
# dbt_project.yml
models:
  your_project:
    bronze:
      +materialized: ephemeral  # All staging as CTEs
```

### 3. Use Consistent Naming
```sql
-- Standardize column naming patterns
{entity}_id      -- For primary/foreign keys
{entity}_name    -- For name fields
{entity}_date    -- For date fields
is_{condition}   -- For booleans
{metric}_count   -- For counts
```

### 4. Preserve Raw Values When Needed
```sql
select
    customer_id,
    customer_name,
    customer_name as customer_name_raw,  -- Keep original
    trim(upper(customer_name)) as customer_name_clean
from {{ source('crm', 'customers') }}
```

### 5. Add Metadata
```sql
select
    *,
    current_timestamp() as dbt_loaded_at,
    '{{ run_started_at }}' as dbt_run_started_at
from {{ source('db', 'table') }}
```

## Source Configuration

### Define Sources in _sources.yml
```yaml
# models/bronze/_sources.yml
version: 2

sources:
  - name: tpc_h
    description: "TPC-H sample data"
    database: snowflake_sample_data
    schema: tpch_sf1
    
    tables:
      - name: customer
        description: "Customer master table"
        columns:
          - name: c_custkey
            description: "Customer primary key"
            tests:
              - not_null
              - unique
```

### Use source() Macro
```sql
-- Reference source tables
select * from {{ source('tpc_h', 'customer') }}

-- NOT this
select * from snowflake_sample_data.tpch_sf1.customer
```

## Folder Organization

```
models/bronze/
├── _models.yml          # Model documentation and tests
├── _sources.yml         # Source definitions
├── crawl/               # Simple staging models
│   ├── stg_tpc_h__customers.sql
│   ├── stg_tpc_h__orders.sql
│   └── stg_tpc_h__nations.sql
├── walk/                # Complex staging with composite keys
│   ├── stg_tpc_h__lineitem.sql
│   └── stg_economic__fx_rates.sql
└── run/                 # Advanced staging with CDC/streams
    ├── customer_cdc_stream.sql
    └── stg_orders_incremental.sql
```

## Troubleshooting

### Issue: Source not found
**Solution:** Check source definition in _sources.yml and verify database/schema names

### Issue: Staging model too slow
**Solution:** Keep it ephemeral; move complex logic to silver layer

### Issue: Column name conflicts
**Solution:** Use consistent renaming pattern with prefixes/suffixes

---

**Next Steps:**
- After staging, build intermediate models: See `INTERMEDIATE_MODELS.md`
- For testing strategy: See `TESTING_STRATEGY.md`
- For source freshness: See `SETUP_GUIDE.md`

