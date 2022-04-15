/*
    Simulate a query for the current year sales orders
    This demonstrates some of the Snowflake specific options
*/

{{ config(
    materialized='incremental',
    unique_key='INTEGRATION_ID',
    transient=false,
    cluster_by=['ROUND(L_ORDERKEY, -4)']
    )
}}

SELECT
  LINEITEM.*,
  LKP_EXCHANGE_RATES.CONVERSION_RATE AS EUR_CONVERSION_RATE,
  {{ surrogate_key(['L_ORDERKEY', 'L_LINENUMBER']) }} AS INTEGRATION_ID
FROM {{ source('TPC_H', 'LINEITEM') }} LINEITEM
JOIN {{ source('TPC_H', 'ORDERS') }} ORDERS ON L_ORDERKEY = O_ORDERKEY
LEFT OUTER JOIN {{ ref('LKP_EXCHANGE_RATES') }} LKP_EXCHANGE_RATES ON
  LKP_EXCHANGE_RATES.FROM_CURRENCY = 'USD'
  AND LKP_EXCHANGE_RATES.TO_CURRENCY = 'EUR'
  AND LKP_EXCHANGE_RATES.DAY_DT = O_ORDERDATE

{% if is_incremental() %}
 -- this filter will only be applied on an incremental run
-- the filter uses a global variable to know how many days to reprocess
WHERE L_SHIPDATE >=
    DATEADD(
      DAY,
      -{{ var('prune_days') }},
      ( SELECT DATE_TRUNC('DAY', MAX(L_SHIPDATE)) FROM {{ this }} )
    )
  OR O_ORDERSTATUS = 'O'
{% endif %}
