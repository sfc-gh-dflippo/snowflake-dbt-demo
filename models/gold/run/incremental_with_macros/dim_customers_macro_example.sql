/*
    dbt Feature Demonstration: INCREMENTAL MODEL WITH CUSTOM MACROS
    
    This model demonstrates:
    - ✅ Incremental materialization with SCD Type 2
    - ✅ Custom macro usage (insert_ghost_key, get_scd_sql)
    - ✅ Advanced configuration options
    - ✅ Post-hooks for data quality
    - ✅ Merge exclude columns for performance
    - ✅ Surrogate key generation
    - ✅ Ghost key insertion for unknown records
    - ✅ Complex Jinja templating
    
    Complexity: 🥇 RUN (Advanced)
    Layer: Gold - Advanced Incremental Patterns
*/

{#- The following config will use the default variable values
    default_integration_key = "integration_id",
    default_scd_cdc_hash_key = "cdc_hash_key",
    default_updated_at_column = "dbt_updated_ts",
    default_inserted_at_column = "dbt_inserted_ts" -#}

{{ config(
    materialized = "incremental",
    unique_key="customer_surrogate_key",
    merge_exclude_columns = ["customer_surrogate_key", "integration_id", "dbt_inserted_ts"],
    transient=false,
    post_hook=[ "{%- do insert_ghost_key( 'customer_surrogate_key', 0,
        {'customer_key': '0',
         'customer_name': \"'Unknown'\",
         'has_orders_flag': \"'N'\",
         'has_open_orders_flag': \"'N'\"}
    ) -%}" ],
    surrogate_key = "customer_surrogate_key",
    alias='DIM_CUSTOMERS_INCREMENTAL_MACRO'
    )
}}

{%- set scd_source_sql -%}
    /*
    All Customers
    */
    select
        c.customer_key,
        c.customer_name,
        c.customer_address,
        c.nation_key,
        c.customer_phone,
        c.account_balance,
        c.market_segment,
        c.customer_comment,
        case
            when lkp.order_count > 0 then 'Y'
            else 'N'
        end as has_orders_flag,
        case
            when lkp.open_order_count > 0 then 'Y'
            else 'N'
        end as has_open_orders_flag,
        {{ integration_key( ["c.customer_key"] ) }} as integration_id,
        HASH( c.customer_name, c.customer_address, c.nation_key, c.customer_phone, c.account_balance, c.market_segment, c.customer_comment ) as cdc_hash_key

    from {{ ref("stg_tpc_h__customers") }} c
    left outer join {{ ref("int_customers__with_orders") }} lkp on (lkp.customer_key = c.customer_key)
    -- Ideally we would have a filter here to limit changes based on a source table timestamp

{%- endset -%}

{{ get_scd_sql(scd_source_sql) }}
