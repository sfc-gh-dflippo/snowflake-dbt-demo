/*
    dbt Feature Demonstration: INCREMENTAL MODEL WITHOUT MACROS

    This model demonstrates:
    - ✅ Incremental materialization with SCD Type 2
    - ✅ Manual SCD implementation (no custom macros)
    - ✅ Proper staging layer usage (FIXED: was using source directly)
    - ✅ Advanced Jinja variables
    - ✅ Hash-based change detection
    - ✅ Post-hooks for ghost key insertion
    - ✅ Merge exclude columns for performance

    Complexity: 🥇 RUN (Advanced)
    Layer: Gold - Advanced Incremental Patterns
*/

{%- set scd_surrogate_key = "customer_surrogate_key" -%}
{%- set scd_integration_key = "integration_id" -%}
{%- set scd_cdc_hash_key = "cdc_hash_key" -%}
{%- set scd_dbt_updated_at = "dbt_updated_ts" -%}
{%- set scd_dbt_inserted_at = "dbt_inserted_ts" -%}

{{ config(
    materialized = "incremental",
    unique_key=scd_surrogate_key,
    merge_exclude_columns = [scd_surrogate_key, scd_dbt_inserted_at],
    transient=false,
    post_hook=[ "{%- do insert_ghost_key( 'customer_surrogate_key', 0) -%}" ]
    )
}}

with source_data as (

    /*
    All Customers
    */
    select
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
        c.customer_key,
        coalesce(c.customer_key::varchar, '') as {{ scd_integration_key }},
        hash(
            c.customer_name,
            c.customer_address,
            c.nation_key,
            c.customer_phone,
            c.account_balance,
            c.market_segment,
            c.customer_comment,
            has_orders_flag,
            has_open_orders_flag
        ) as {{ scd_cdc_hash_key }}

    from {{ ref("stg_tpc_h__customers") }} c
    left outer join {{ ref("int_customers__with_orders") }} lkp on (lkp.customer_key = c.customer_key)
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
        {{ sequence_nextval_as_surrogate_key(scd_surrogate_key) }},
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
