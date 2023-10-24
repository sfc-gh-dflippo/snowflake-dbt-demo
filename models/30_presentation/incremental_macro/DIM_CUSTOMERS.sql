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
    post_hook=[ "{%- do insert_ghost_key( 'c_cust_wid', 0,
        {'C_CUSTKEY': '0',
         'C_NAME': \"'Unknown'\",
         'C_ACTIVE_CUSTOMER_FLAG': \"'N'\",
         'C_OPEN_ORDER_CUSOTMER_FLAG': \"'N'\"}
    ) -%}" ]
    )
}}

{%- set scd_source_sql -%}
    /*
    All Customers
    */
    select
        c_name,
        c_address,
        c_nationkey,
        c_phone,
        c_acctbal,
        c_mktsegment,
        c_comment,
        case
            when lkp.order_count > 0 then 'Y'
            else 'N'
        end as c_active_customer_flag,
        case
            when lkp.open_order_count > 0 then 'Y'
            else 'N'
        end as c_open_order_cusotmer_flag,
        c_custkey,
        COALESCE(c_custkey::varchar, '') as {{ scd_integration_key }},
        HASH(
            c_name,
            c_address,
            c_nationkey,
            c_phone,
            c_acctbal,
            c_mktsegment,
            c_comment,
            c_active_customer_flag,
            c_open_order_cusotmer_flag
        ) as {{ scd_cdc_hash_key }}

    from {{ source("TPC_H", "CUSTOMER") }} c
    left outer join {{ ref("LKP_CUSTOMERS_WITH_ORDERS") }} lkp on (lkp.o_custkey = c.c_custkey)
    -- Ideally we would have a filter here to limit changes based on a source table timestamp

{%- endset -%}

{{ get_scd_sql(scd_source_sql, scd_surrogate_key, scd_integration_key, scd_cdc_hash_key, scd_dbt_updated_at, scd_dbt_inserted_at) }}
