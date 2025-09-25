{{ config(
    tags=['staging', 'tpc_h']
) }}

-- Staging model for TPC-H ORDERS source
-- One-to-one relationship with source, basic cleaning and renaming

with source as (
    select * from {{ source('TPC_H', 'ORDERS') }}
),

renamed as (
    select
        -- Primary key
        o_orderkey as order_key,
        
        -- Foreign keys
        o_custkey as customer_key,
        
        -- Attributes
        o_orderstatus as order_status,
        o_totalprice as total_price,
        o_orderdate as order_date,
        o_orderpriority as order_priority,
        o_clerk as clerk,
        o_shippriority as ship_priority,
        o_comment as order_comment,
        
        -- Audit columns
        current_timestamp() as _loaded_at

    from source
)

select * from renamed
