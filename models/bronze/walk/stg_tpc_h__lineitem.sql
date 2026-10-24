/*
    dbt Feature Demonstration: COMPLEX STAGING MODEL

    This model demonstrates:
    - ✅ Staging layer best practices (1:1 with source)
    - ✅ Ephemeral materialization (inherited from dbt_project.yml)
    - ✅ Complex schema with composite primary keys
    - ✅ Multiple foreign key relationships
    - ✅ Extensive column renaming and standardization
    - ✅ Source function usage
    - ✅ CTE pattern for readability

    Complexity: 🥈 WALK (Intermediate)
    Layer: Bronze - Complex Staging
*/

{{ config(
    tags=['staging', 'tpc_h']
) }}

-- Staging model for TPC-H LINEITEM source
-- One-to-one relationship with source, basic cleaning and renaming

with source as (
    select * from {{ source('TPC_H', 'LINEITEM') }}
),

renamed as (
    select
        -- Composite primary key
        l_orderkey as order_key,
        l_linenumber as line_number,

        -- Foreign keys
        l_partkey as part_key,
        l_suppkey as supplier_key,

        -- Quantities and prices
        l_quantity as quantity,
        l_extendedprice as extended_price,
        l_discount as discount,
        l_tax as tax,

        -- Status and dates
        l_returnflag as return_flag,
        l_linestatus as line_status,
        l_shipdate as ship_date,
        l_commitdate as commit_date,
        l_receiptdate as receipt_date,

        -- Instructions and comments
        l_shipinstruct as ship_instruct,
        l_shipmode as ship_mode,
        l_comment as line_comment,

        -- Audit columns
        -- Stable watermark: the receipt date does not change between runs.
        -- current_timestamp() would be the run time and defeat incremental filters.
        l_receiptdate::timestamp_ntz as _loaded_at

    from source
)

select * from renamed
