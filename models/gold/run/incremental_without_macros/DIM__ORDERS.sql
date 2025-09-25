{%- set scd_surrogate_key = "order_surrogate_key" -%}
{%- set scd_integration_key = "integration_id" -%}
{%- set scd_cdc_hash_key = "cdc_hash_key" -%}
{%- set scd_dbt_updated_at = "dbt_updated_ts" -%}
{%- set scd_dbt_inserted_at = "dbt_inserted_ts" -%}

{{ config(
    materialized = "incremental",
    unique_key=scd_surrogate_key,
    merge_exclude_columns = [scd_surrogate_key, scd_dbt_inserted_at],
    transient=false,
    post_hook=[ "{%- do insert_ghost_key( 'order_surrogate_key', 0) -%}" ]
    )
}}

with source_data as (

    /*
        Simulate a query for the sales orders
    */
    select
        coalesce(c.customer_key, 0) as customer_key,
        o.order_status,
        o.total_price,
        o.order_date,
        o.order_priority,
        o.clerk,
        o.ship_priority,
        o.order_comment,
        o.customer_key as order_customer_key,
        o.order_key,
        coalesce(o.order_key::varchar, '') as {{ scd_integration_key }},
        hash(
            coalesce(c.customer_key, 0),
            o.order_status,
            o.total_price,
            o.order_date,
            o.order_priority,
            o.clerk,
            o.ship_priority,
            o.order_comment,
            o.customer_key
        ) as {{ scd_cdc_hash_key }}
    from
        {{ ref("stg_tpc_h__orders") }} o
    left outer join {{ ref("dim_customers") }} c on c.customer_key = o.customer_key

    {%- if is_incremental() %}
    -- this filter will only be applied on an incremental run
        where o.order_date >= dateadd(day, -90, sysdate())
            or o.order_status = 'O'
    {%- endif %}


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
