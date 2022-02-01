/*
    This model will figure out the exchange rates between many different currencies
*/
{{ config(
    materialized='table'
) }}
WITH EXCH_RATES AS(
  SELECT 
  "Currency Unit" as CURRENCY,
  "Value" as FROM_USD,
  (1/FROM_USD) as TO_USD,
  -- The start date is the day after the previous close
  NVL(LAG(DATEADD(DAY, 1, "Date"), 1) OVER (PARTITION BY CURRENCY ORDER BY "Date" ASC), '1900-01-01'::DATE) AS START_DATE,
  CASE -- when it is the last row, make the end date tomorrow to ensure we can't lose same-day records
  WHEN LAG(DATEADD(DAY, 1, "Date"), -1) OVER (PARTITION BY CURRENCY ORDER BY "Date" ASC) IS NULL THEN SYSDATE()::DATE + 1
  ELSE "Date" 
  END AS END_DATE
  FROM {{ source('KNOEMA_ECONOMY', 'EXRATESCC2018') }}
  WHERE
  ("Currency Unit" IN ('EUR', 'MAD', 'CNY', 'GBP', 'JPY', 'PLN', 'MKD', 'CZK', 'MDL', 'RON')
   --OR "Currency Unit" IN (SELECT EN_CURR FROM QAD_VIEWS.EN_MSTR_V)
  )
  AND "Indicator Name" = 'Close'
  AND "Frequency" = 'D'
UNION ALL -- JUST IN CASE THE LOCAL CURRENCY IS USD
  SELECT 'USD', 1, 1, '1900-01-01'::DATE, SYSDATE()::DATE + 1
)
select d.DAY_DT,
    FIRST_RATE.CURRENCY FROM_currency,
    SECOND_RATE.CURRENCY TO_CURRENCY,
    FIRST_RATE.to_usd * SECOND_RATE.from_usd as CONVERSION_RATE,
    FIRST_RATE.FROM_usd * SECOND_RATE.to_usd as INVERSE_CONVERSION_RATE
from {{ ref('DIM_CALENDAR_DAY') }} d
    join exch_rates FIRST_RATE on d.day_dt between FIRST_RATE.start_date and FIRST_RATE.end_date
    join exch_rates SECOND_RATE on d.day_dt between SECOND_RATE.start_date and SECOND_RATE.end_date
order by 1, 2, 3