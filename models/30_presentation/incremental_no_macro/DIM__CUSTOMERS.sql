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
        coalesce(c_custkey::varchar, '') as {{ scd_integration_key }},
        hash(
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

),

existing_data as (

    {% if is_incremental() -%}

        select
            {{ scd_surrogate_key }},
            {{ scd_integration_key }},
            {{ scd_cdc_hash_key }},
            {{ scd_dbt_inserted_at }}
        from {{ this }}

    {%- else -%}

    select
        null::integer {{ scd_surrogate_key }},
        null::varchar {{ scd_integration_key }},
        null::integer {{ scd_cdc_hash_key }},
        null::timestamp_ntz {{ scd_dbt_inserted_at }}
    limit 0

    {%- endif %}

),

inserts as (
    select
        {{ sequence_get_nextval() }} as {{ scd_surrogate_key }},
        source_data.*,
        sysdate() as {{ scd_dbt_inserted_at }},
        sysdate() as {{ scd_dbt_updated_at }}
    from source_data
    left outer join existing_data on source_data.{{ scd_integration_key }} = existing_data.{{ scd_integration_key }}
    where existing_data.{{ scd_integration_key }} is null
),

updates as (
    select
        existing_data.{{ scd_surrogate_key }},
        source_data.*,
        existing_data.{{ scd_dbt_inserted_at }},
        sysdate() as {{ scd_dbt_updated_at }}
    from source_data
    join existing_data on source_data.{{ scd_integration_key }} = existing_data.{{ scd_integration_key }}
    where source_data.{{ scd_cdc_hash_key }} != existing_data.{{ scd_cdc_hash_key }}
)

select * from inserts
union all
select * from updates
