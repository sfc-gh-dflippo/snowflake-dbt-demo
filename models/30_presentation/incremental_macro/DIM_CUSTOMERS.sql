{#- The following config will use the default variable values
    default_integration_key = "integration_id",
    default_scd_cdc_hash_key = "cdc_hash_key",
    default_updated_at_column = "dbt_updated_ts",
    default_inserted_at_column = "dbt_inserted_ts" -#}

{{ config(
    materialized = "incremental",
    unique_key="c_cust_wid",
    merge_exclude_columns = ["c_cust_wid", "integration_id", "dbt_inserted_ts"],
    transient=false,
    post_hook=[ "{%- do insert_ghost_key( 'c_cust_wid', 0,
        {'C_CUSTKEY': '0',
         'C_NAME': \"'Unknown'\",
         'C_ACTIVE_CUSTOMER_FLAG': \"'N'\",
         'C_OPEN_ORDER_CUSTOMER_FLAG': \"'N'\"}
    ) -%}" ],
    surrogate_key = "c_cust_wid"
    )
}}

{%- set scd_source_sql -%}
    /*
    All Customers
    */
    select
        {{ dbt_utils.star(from=source("TPC_H", "CUSTOMER")) }},
        case
            when lkp.order_count > 0 then 'Y'
            else 'N'
        end as c_active_customer_flag,
        case
            when lkp.open_order_count > 0 then 'Y'
            else 'N'
        end as c_open_order_customer_flag,
        {{ integration_key( ["c_custkey"] ) }} as integration_id,
        HASH( {{ dbt_utils.star(from=source("TPC_H", "CUSTOMER"), except=["c_custkey"]) }} ) as cdc_hash_key

    from {{ source("TPC_H", "CUSTOMER") }} c
    left outer join {{ ref("LKP_CUSTOMERS_WITH_ORDERS") }} lkp on (lkp.o_custkey = c.c_custkey)
    -- Ideally we would have a filter here to limit changes based on a source table timestamp

{%- endset -%}

{{ get_scd_sql(scd_source_sql) }}
