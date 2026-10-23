{#- dbt-quality: ignore-file SSC-EWI-DBTARC0004 -#}
{#- ARC0004 waived: the other bronze models that read this source each demo one feature (hooks, CDC stream, incremental). This is the canonical staging model. -#}
{{ config(
    tags=['staging', 'tpc_h']
) }}

-- Staging model for TPC-H CUSTOMER source
-- One-to-one relationship with source, basic cleaning and renaming
-- Following dbt best practices: each source should have exactly one staging model

with source as (
    select * from {{ source('TPC_H', 'CUSTOMER') }}
),

renamed as (
    select
        -- Primary key
        c_custkey as customer_key,

        -- Attributes
        c_name as customer_name,
        c_address as customer_address,
        c_nationkey as nation_key,
        c_phone as customer_phone,
        c_acctbal as account_balance,
        c_mktsegment as market_segment,
        c_comment as customer_comment,

        -- Audit columns
        current_timestamp() as _loaded_at

    from source
)

select * from renamed
