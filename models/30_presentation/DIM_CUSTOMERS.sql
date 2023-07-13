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

    {{ surrogate_key(["C_CUSTKEY"]) }} AS {{scd_integration_key}},

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

{% endset -%}

{{ get_scd_sql(scd_source_sql, scd_surrogate_key, scd_integration_key, scd_cdc_hash_key, scd_dbt_updated_at, scd_dbt_inserted_at) -}}
