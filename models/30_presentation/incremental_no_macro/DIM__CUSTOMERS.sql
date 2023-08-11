{%- set scd_surrogate_key = "c_cust_wid" -%}
{%- set scd_integration_key = "integration_id" -%}
{%- set scd_cdc_hash_key = "cdc_hash_key" -%}
{%- set scd_dbt_updated_at = "dbt_updated_ts" -%}
{%- set scd_dbt_inserted_at = "dbt_inserted_ts" -%}

{{ config(
    materialized = "incremental",
    unique_key=scd_surrogate_key,
    merge_exclude_columns = [scd_surrogate_key, scd_dbt_inserted_at],
    transient=false,
    post_hook=[ "{%- do insert_ghost_key( 'c_cust_wid', 0) -%}" ]
    )
}}

with source_data as (

    /*
    All Customers
    */
    SELECT
        C_NAME,
        C_ADDRESS,
        C_NATIONKEY,
        C_PHONE,
        C_ACCTBAL,
        C_MKTSEGMENT,
        C_COMMENT,
        CASE
            WHEN LKP.ORDER_COUNT > 0 THEN 'Y'
            ELSE 'N'
        END AS C_ACTIVE_CUSTOMER_FLAG,
        CASE
            WHEN LKP.OPEN_ORDER_COUNT > 0 THEN 'Y'
            ELSE 'N'
        END AS C_OPEN_ORDER_CUSOTMER_FLAG,
        C_CUSTKEY,
        COALESCE(C_CUSTKEY::varchar, '') AS {{scd_integration_key}},
        HASH(C_NAME,
            C_ADDRESS,
            C_NATIONKEY,
            C_PHONE,
            C_ACCTBAL,
            C_MKTSEGMENT,
            C_COMMENT,
            C_ACTIVE_CUSTOMER_FLAG,
            C_OPEN_ORDER_CUSOTMER_FLAG) AS {{scd_cdc_hash_key}}

    FROM {{ source("TPC_H", "CUSTOMER") }} C
    LEFT OUTER JOIN {{ ref("LKP_CUSTOMERS_WITH_ORDERS") }} LKP ON ( LKP.O_CUSTKEY = C.C_CUSTKEY )
    -- Ideally we would have a filter here to limit changes based on a source table timestamp

),

existing_data as (

    {% if is_incremental() -%}

    select
        {{scd_surrogate_key}},
        {{scd_integration_key}},
        {{scd_cdc_hash_key}},
        {{scd_dbt_inserted_at}}
    from {{ this }}

    {%- else -%}

    select
        null::integer {{scd_surrogate_key}},
        null::varchar {{scd_integration_key}},
        null::integer {{scd_cdc_hash_key}},
        null::timestamp_ntz {{scd_dbt_inserted_at}}
    limit 0

    {%- endif %}

),

inserts as (
    select
        {{ sequence_get_nextval() }} as {{scd_surrogate_key}},
        source_data.*,
        sysdate() as {{scd_dbt_inserted_at}},
        sysdate() as {{scd_dbt_updated_at}}
    from source_data
    left outer join existing_data on source_data.{{scd_integration_key}} = existing_data.{{scd_integration_key}}
    where existing_data.{{scd_integration_key}} is null
),

updates as (
    select
        existing_data.{{scd_surrogate_key}},
        source_data.*,
        existing_data.{{scd_dbt_inserted_at}},
        sysdate() as {{scd_dbt_updated_at}}
    from source_data
    join existing_data on source_data.{{scd_integration_key}} = existing_data.{{scd_integration_key}}
    where source_data.{{scd_cdc_hash_key}} <> existing_data.{{scd_cdc_hash_key}}
)

select * from inserts
union all
select * from updates
