{{ config(
    tags=['m_MT_PRODUCT_HWSW_ANNUITY']
) }}
{{ config(materialized='table') }}
-- Self-referencing table(s): 'WI_PRODUCT_HWSW_MONTH_CTRL' used as both source and target in this mapping.
-- Materialized as TABLE to snapshot source data before the target model overwrites it.
SELECT
   CASE
      WHEN CURRENT_DATE() < FISCAL_MONTH_START_DATE + 5
         THEN FISCAL_MONTH_AGO_MONTH_NUMBER
      ELSE FISCAL_YEAR_MONTH_INT
   END AS FISCAL_YEAR_MONTH_INT
FROM
   {{ var('m_MT_PRODUCT_HWSW_ANNUITY_COMREFVWDB') }}.R_FISCAL_MONTH_TO_YEAR
WHERE
   FISCAL_MONTH_AGE = 0