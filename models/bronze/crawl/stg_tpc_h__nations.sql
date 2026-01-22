/*
    dbt Feature Demonstration: BASIC STAGING MODEL

    This model demonstrates:
    - ✅ Staging layer best practices (1:1 with source)
    - ✅ Ephemeral materialization (inherited from dbt_project.yml)
    - ✅ Basic column renaming and standardization
    - ✅ Source function usage
    - ✅ CTE pattern for readability
    - ✅ Audit column addition

    Complexity: 🥉 CRAWL (Beginner)
    Layer: Bronze - Basic Staging
*/

{{ config(
    tags=['staging', 'tpc_h']
) }}

-- Staging model for TPC-H NATION source
-- One-to-one relationship with source, basic cleaning and renaming

with source as (
    select * from {{ source('TPC_H', 'NATION') }}
),

renamed as (
    select
        -- Primary key
        n_nationkey as nation_key,

        -- Foreign keys
        n_regionkey as region_key,

        -- Attributes
        n_name as nation_name,
        n_comment as nation_comment,

        -- Audit columns
        current_timestamp() as _loaded_at

    from source
)

select * from renamed
