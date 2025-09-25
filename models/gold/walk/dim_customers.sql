/*
    dbt Feature Demonstration: MARTS MODEL - DIMENSION TABLE
    
    This model demonstrates:
    - ✅ Marts layer best practices (business-ready data)
    - ✅ Incremental materialization for performance
    - ✅ Unique key configuration for incremental updates
    - ✅ Model aliasing for backward compatibility
    - ✅ References to staging and intermediate models only
    - ✅ Business logic enrichment (flags, categorization)
    - ✅ Complex joins across multiple models
    - ✅ Proper dimension table structure
    
    Complexity: 🥈 WALK (Intermediate)
    Layer: Gold - Dimensions
*/

{{ config(
    materialized='incremental',
    unique_key='customer_key',
    tags=['marts', 'core', 'dimensions'],
    alias='DIM_CUSTOMERS'
) }}

-- Dimension: Customers with enriched business attributes
-- Following best practices: marts layer contains business-ready data
-- No direct source references - only staging and intermediate models

with customers_base as (
    select * from {{ ref('stg_tpc_h__customers') }}
),

customer_orders as (
    select * from {{ ref('int_customers__with_orders') }}
),

nations as (
    select * from {{ ref('stg_tpc_h__nations') }}
),

enriched_customers as (
    select
        -- Primary key
        customers_base.customer_key,
        
        -- Customer attributes
        customers_base.customer_name,
        customers_base.customer_address,
        customers_base.customer_phone,
        customers_base.account_balance,
        customers_base.market_segment,
        customers_base.customer_comment,
        
        -- Geographic attributes
        customers_base.nation_key,
        nations.nation_name,
        nations.region_key,
        
        -- Order statistics (business logic)
        coalesce(customer_orders.order_count, 0) as total_orders,
        coalesce(customer_orders.open_order_count, 0) as open_orders,
        
        -- Business flags
        case 
            when coalesce(customer_orders.order_count, 0) > 0 then 'Y'
            else 'N'
        end as has_orders_flag,
        
        case 
            when coalesce(customer_orders.open_order_count, 0) > 0 then 'Y'
            else 'N'
        end as has_open_orders_flag,
        
        -- Customer segmentation
        case 
            when customers_base.account_balance >= 5000 then 'High Value'
            when customers_base.account_balance >= 1000 then 'Medium Value'
            else 'Standard'
        end as value_segment,
        
        -- Audit columns
        customers_base._loaded_at,
        current_timestamp() as _updated_at

    from customers_base
    left join customer_orders 
        on customers_base.customer_key = customer_orders.customer_key
    left join nations 
        on customers_base.nation_key = nations.nation_key
)

select * from enriched_customers

{% if is_incremental() %}
    where _loaded_at > (select max(_loaded_at) from {{ this }})
{% endif %}
