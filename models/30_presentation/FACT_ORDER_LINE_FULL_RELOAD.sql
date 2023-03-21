/*
    Simulate a query for the current year sales orders
    This demonstrates some of the Snowflake specific options
*/
{{ config(
    materialized='incremental',
    pre_hook="{% if is_incremental() %} DELETE FROM {{this}} WHERE SOURCE_SYSTEM_CODE = '{{ env_var('SOURCE_SYSTEM_CODE', 'UNKNOWN') }}' {% endif %}"
    )
}}

SELECT
  '{{ env_var("SOURCE_SYSTEM_CODE", "UNKNOWN") }}' AS SOURCE_SYSTEM_CODE,
  LINEITEM.*,
  LKP_EXCHANGE_RATES.CONVERSION_RATE AS EUR_CONVERSION_RATE,
  {{ surrogate_key(['L_ORDERKEY', 'L_LINENUMBER']) }} AS INTEGRATION_ID,
  SYSDATE() as dbt_last_update_ts
FROM {{ source('TPC_H', 'LINEITEM') }} LINEITEM
JOIN {{ source('TPC_H', 'ORDERS') }} ORDERS ON L_ORDERKEY = O_ORDERKEY
LEFT OUTER JOIN {{ ref('LKP_EXCHANGE_RATES') }} LKP_EXCHANGE_RATES ON
  LKP_EXCHANGE_RATES.FROM_CURRENCY = 'USD'
  AND LKP_EXCHANGE_RATES.TO_CURRENCY = 'EUR'
  AND LKP_EXCHANGE_RATES.DAY_DT = O_ORDERDATE
