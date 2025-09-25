/*
    dbt Feature Demonstration: MARTS MODEL - FACT TABLE
    
    This model demonstrates:
    - ✅ Marts layer best practices (business-ready data)
    - ✅ Incremental materialization for large datasets
    - ✅ Composite unique key for incremental updates
    - ✅ Model aliasing for backward compatibility
    - ✅ Complex fact table with multiple dimensions
    - ✅ Business metrics calculation
    - ✅ References to staging models (proper layering)
    - ✅ Proper fact table structure with measures
    
    Complexity: 🥇 RUN (Advanced)
    Layer: Gold - Facts
*/

{{ config(
    materialized='incremental',
    unique_key=['order_key', 'line_number'],
    tags=['marts', 'core', 'facts'],
    alias='FACT_ORDER_LINE'
) }}

-- Fact: Order lines with all business metrics
-- Following best practices: facts reference dimensions, not sources directly

with line_items as (
    select * from {{ ref('stg_tpc_h__lineitem') }}
),

orders as (
    select 
        order_key,
        customer_key,
        order_date,
        order_status_desc
    from {{ ref('dim_orders') }}
),

fx_rates as (
    select * from {{ ref('int_fx_rates__daily') }}
),

fact_order_lines as (
    select
        -- Composite primary key
        line_items.order_key,
        line_items.line_number,
        
        -- Foreign keys
        line_items.part_key,
        line_items.supplier_key,
        orders.customer_key,
        
        -- Measures
        line_items.quantity,
        line_items.extended_price,
        line_items.discount,
        line_items.tax,
        
        -- Calculated measures
        line_items.extended_price * (1 - line_items.discount) as discounted_price,
        line_items.extended_price * (1 - line_items.discount) * (1 + line_items.tax) as final_price,
        
        -- FX conversion (business logic)
        coalesce(fx_rates.conversion_rate, 1.0) as eur_conversion_rate,
        (line_items.extended_price * (1 - line_items.discount) * (1 + line_items.tax)) * 
        coalesce(fx_rates.conversion_rate, 1.0) as final_price_eur,
        
        -- Attributes
        line_items.return_flag,
        line_items.line_status,
        line_items.ship_date,
        line_items.commit_date,
        line_items.receipt_date,
        line_items.ship_instruct,
        line_items.ship_mode,
        line_items.line_comment,
        
        -- Order context
        orders.order_date,
        orders.order_status_desc,
        
        -- Audit columns
        line_items._loaded_at,
        current_timestamp() as _updated_at

    from line_items
    inner join orders 
        on line_items.order_key = orders.order_key
    left join fx_rates 
        on fx_rates.from_currency = 'USD'
        and fx_rates.to_currency = 'EUR'
        and orders.order_date between fx_rates.day_dt and fx_rates.end_date
)

select * from fact_order_lines

{% if is_incremental() %}
    where _loaded_at > (select max(_loaded_at) from {{ this }})
{% endif %}
