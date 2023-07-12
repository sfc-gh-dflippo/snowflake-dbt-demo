/*
    Simulate a query for the current year sales orders
    This demonstrates some of the Snowflake specific options
*/
{{ config(
    materialized="incremental",
    merge_exclude_columns = ["DBT_INSERT_TS"],
    pre_hook="{% if is_incremental() %} DELETE FROM {{this}} WHERE SOURCE_SYSTEM_CODE = '{{ env_var('SOURCE_SYSTEM_CODE', 'UNKNOWN') }}' {% endif %}"
    )
}}

SELECT
    '{{ env_var("SOURCE_SYSTEM_CODE", "UNKNOWN") }}' AS SOURCE_SYSTEM_CODE,
    -- Lookup the surrogate keys for orders and customers
    COALESCE(ORDERS.O_ORDER_WID, 0) AS L_ORDER_WID,
    COALESCE(ORDERS.O_CUST_WID, 0) AS L_CUST_WID,
    LINEITEM.*,
    LKP_EXCHANGE_RATES.CONVERSION_RATE AS EUR_CONVERSION_RATE,
    {{ surrogate_key(["L_ORDERKEY", "L_LINENUMBER"]) }} AS INTEGRATION_ID,
    SYSDATE() as DBT_INSERT_TS,
    SYSDATE() as DBT_LAST_UPDATE_TS
FROM {{ source("TPC_H", "LINEITEM") }} LINEITEM
-- Joining on the integration key for orders
LEFT OUTER JOIN {{ ref("DIM_ORDERS") }} ORDERS ON L_ORDERKEY = O_ORDERKEY
LEFT OUTER JOIN {{ ref("LKP_EXCHANGE_RATES") }} LKP_EXCHANGE_RATES ON
    LKP_EXCHANGE_RATES.FROM_CURRENCY = 'USD'
    AND LKP_EXCHANGE_RATES.TO_CURRENCY = 'EUR'
    AND LKP_EXCHANGE_RATES.DAY_DT = ORDERS.O_ORDERDATE
