{{ config(
    materialized='table',
    tags=['bronze', 'walk', 'data_quality']
) }}

-- BRONZE WALK: Source data with quality checks and hooks
-- Complexity: Intermediate - Hooks, variables, basic transformations
-- Features demonstrated: pre/post hooks, variables, data quality patterns

select
    c_custkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone,
    c_acctbal,
    c_mktsegment,
    c_comment,

    -- Data quality flags
    case
        when c_name is null or trim(c_name) = '' then 'INVALID_NAME'
        when c_acctbal < 0 then 'NEGATIVE_BALANCE'
        else 'VALID'
    end as data_quality_flag,

    -- Audit columns
    current_timestamp() as extracted_at,
    '{{ var("default_integration_key") }}' as integration_source,
    {{ var("prune_days") }} as retention_days

from {{ source('TPC_H', 'CUSTOMER') }}
where c_custkey is not null
