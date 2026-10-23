{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_key',
    tags=['marts', 'core', 'dimensions'],
    alias='DIM_ORDERS'
) }}

-- Dimension: Orders with enriched business attributes
-- Following best practices: marts layer contains business-ready data
-- No direct source references - only staging models

with orders_base as (
    select * from {{ ref('stg_tpc_h__orders') }}
),

customers as (
    select
        customer_key,
        customer_name,
        nation_key,
        value_segment
    from {{ ref('dim_customers') }}
),

enriched_orders as (
    select
        -- Primary key
        orders_base.order_key,

        -- Foreign keys
        orders_base.customer_key,

        -- Order attributes
        orders_base.order_status,
        orders_base.total_price,
        orders_base.order_date,
        orders_base.order_priority,
        orders_base.clerk,
        orders_base.ship_priority,
        orders_base.order_comment,

        -- Customer attributes (denormalized for performance)
        customers.customer_name,
        customers.nation_key,
        customers.value_segment,

        -- Business logic
        case
            when orders_base.order_status = 'O' then 'Open'
            when orders_base.order_status = 'F' then 'Fulfilled'
            when orders_base.order_status = 'P' then 'Partial'
            else 'Unknown'
        end as order_status_desc,

        -- Date dimensions
        extract(year from orders_base.order_date) as order_year,
        extract(quarter from orders_base.order_date) as order_quarter,
        extract(month from orders_base.order_date) as order_month,

        -- Audit columns
        orders_base._loaded_at,
        current_timestamp() as _updated_at

    from orders_base
    left join customers
        on orders_base.customer_key = customers.customer_key
),

-- cdc_hash_key detects changed rows. It excludes _loaded_at and _updated_at: both are the run time.
-- A filter on _loaded_at selected every row, so the merge rewrote every row.
final as (
    select
        enriched_orders.*,
        hash(
            customer_key, order_status, total_price, order_date, order_priority, clerk,
            ship_priority, order_comment, customer_name, nation_key, value_segment
        ) as cdc_hash_key
    from enriched_orders
)

select final.*
from final

{% if is_incremental() %}
-- Keep only new orders and orders whose business columns changed.
left join {{ this }} as existing
    on final.order_key = existing.order_key
where existing.order_key is null
    or final.cdc_hash_key != existing.cdc_hash_key
{% endif %}
