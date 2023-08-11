{%- set scd_surrogate_key = "O_ORDER_WID" -%}
{%- set scd_integration_key = "integration_id" -%}
{%- set scd_cdc_hash_key = "cdc_hash_key" -%}
{%- set scd_dbt_updated_at = "dbt_updated_ts" -%}
{%- set scd_dbt_inserted_at = "dbt_inserted_ts" -%}

{{ config(
    materialized = "incremental",
    unique_key=scd_surrogate_key,
    merge_exclude_columns = [scd_surrogate_key, scd_dbt_inserted_at],
    transient=false,
    post_hook=[ "{%- do insert_ghost_key( 'O_ORDER_WID', 0) -%}" ]
    )
}}

with source_data as (

    /*
        Simulate a query for the sales orders
    */
    SELECT
        COALESCE(C_CUST_WID, 0) AS O_CUST_WID,
        O_ORDERSTATUS,
        O_TOTALPRICE,
        O_ORDERDATE,
        O_ORDERPRIORITY,
        O_CLERK,
        O_SHIPPRIORITY,
        O_COMMENT,
        O_CUSTKEY,
        O_ORDERKEY,
        COALESCE(O_ORDERKEY::varchar, '') AS {{scd_integration_key}},
        HASH(O_CUST_WID,
            O_ORDERSTATUS,
            O_TOTALPRICE,
            O_ORDERDATE,
            O_ORDERPRIORITY,
            O_CLERK,
            O_SHIPPRIORITY,
            O_COMMENT,
            O_CUSTKEY) AS {{scd_cdc_hash_key}}
    FROM
    {{ source("TPC_H", "ORDERS") }} O
    LEFT OUTER JOIN {{ ref("DIM_CUSTOMERS") }} C on C.C_CUSTKEY = O.O_CUSTKEY

    {%- if is_incremental() %}
    -- this filter will only be applied on an incremental run
    WHERE O_ORDERDATE >= DATEADD(DAY, -90, SYSDATE() )
        OR O_ORDERSTATUS = 'O'
    {%- endif %}


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
