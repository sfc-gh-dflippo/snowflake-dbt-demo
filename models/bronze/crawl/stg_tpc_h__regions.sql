{{ config(
    tags=['staging', 'tpc_h']
) }}

-- Staging model for TPC-H REGION source
-- One-to-one relationship with source, basic cleaning and renaming

with source as (
    select * from {{ source('TPC_H', 'REGION') }}
),

renamed as (
    select
        -- Primary key
        r_regionkey as region_key,
        
        -- Attributes
        r_name as region_name,
        r_comment as region_comment,
        
        -- Audit columns
        current_timestamp() as _loaded_at

    from source
)

select * from renamed
