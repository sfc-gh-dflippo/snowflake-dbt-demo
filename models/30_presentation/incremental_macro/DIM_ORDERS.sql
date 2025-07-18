{#- The following config will use the default variable values
    default_integration_key = "integration_id",
    default_scd_cdc_hash_key = "cdc_hash_key",
    default_updated_at_column = "dbt_updated_ts",
    default_inserted_at_column = "dbt_inserted_ts" -#}

{{ config(
    materialized = "incremental",
    unique_key='o_order_wid',
    merge_exclude_columns = ["o_order_wid", "integration_id", "dbt_inserted_ts"],
    transient=false,
    post_hook=[ "{%- do insert_ghost_key( 'o_order_wid', 0,
        {'O_CUST_WID': '0'}
    ) -%}" ],
    surrogate_key = "o_order_wid"
    )
}}


{%- set scd_source_sql -%}

/*
    Simulate a query for the sales orders
*/
SELECT
    {{ dbt_utils.star(from=source("TPC_H", "ORDERS")) }},
    COALESCE(C_CUST_WID, 0) AS O_CUST_WID, -- If the lookup fails, use zero
    {{ integration_key( ["O_ORDERKEY"] ) }} AS integration_id,
    HASH(
        {{ dbt_utils.star(from=source("TPC_H", "ORDERS"), except=["O_ORDERKEY"]) }},
        O_CUST_WID) AS cdc_hash_key
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

{{- get_scd_sql(scd_source_sql) -}}
