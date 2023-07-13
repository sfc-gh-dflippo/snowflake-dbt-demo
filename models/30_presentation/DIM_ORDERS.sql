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
    post_hook=[ "{%- do insert_ghost_key( 'O_ORDER_WID', 0,
        {'O_CUST_WID': '0'}
    ) -%}" ]
    )
}}

{%- set scd_source_sql -%}

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
    {{ surrogate_key(["O_ORDERKEY"]) }} AS {{scd_integration_key}},
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


-- Uncomment this line to cause a FK violation
--LIMIT 100

{% endset -%}

{{ get_scd_sql(scd_source_sql, scd_surrogate_key, scd_integration_key, scd_cdc_hash_key, scd_dbt_updated_at, scd_dbt_inserted_at) -}}
