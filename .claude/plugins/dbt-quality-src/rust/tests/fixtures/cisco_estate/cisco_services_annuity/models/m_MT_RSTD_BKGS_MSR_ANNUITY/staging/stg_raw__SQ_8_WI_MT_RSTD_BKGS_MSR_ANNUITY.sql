{{ config(
    tags=['m_MT_RSTD_BKGS_MSR_ANNUITY']
) }}
{{ config(materialized='table') }}
-- Self-referencing table(s): 'WI_MT_RSTD_BKGS_MSR_ANNUITY5' used as both source and target in this mapping.
-- Materialized as TABLE to snapshot source data before the target model overwrites it.
SELECT
   MT.BOOKINGS_MEASURE_KEY,
   MT.BKGS_MEASURE_TRANS_TYPE_CODE,
   MT.BOOKINGS_PROCESS_DATE,
   MT.SALES_TERRITORY_KEY,
   MT.SALES_REP_NUMBER,
   MT.DV_CONTRACT_DURATION,
   MT.DV_ANNUALIZED_FLG,
   MT.RU_SERVICE_CONTRACT_START_DTM,
   MT.RU_SERVICE_CONTRACT_END_DTM,
   MT.ANNUITY_TYPE ANNUITY_TYPE,
   CASE
      WHEN COLLATE(MT.DV_ANNUALIZED_FLG, 'en-ci-rtrim') <> 'N'
         THEN NULL
      ELSE MT.BOOKINGS_PROCESS_MONTH
   END ANNUITY_MONTH,
   CASE
      WHEN COLLATE(MT.DV_ANNUALIZED_FLG, 'en-ci-rtrim') <> 'N'
         THEN NULL
      ELSE MT.DV_MULTIYEAR_US_NET_AMT
   END ANNUITY_AMT,
   MT.DV_FMV_FLG,
   MT.ADJUSTMENT_CODE
FROM
   {{ var('m_MT_RSTD_BKGS_MSR_ANNUITY_STGDB') }}.WI_MT_RSTD_BKGS_MEASURE MT
WHERE
   COLLATE(MT.DV_ANNUALIZED_FLG, 'en-ci-rtrim') <> 'N'
   OR (COLLATE(DV_ANNUALIZED_FLG, 'en-ci-rtrim') = 'N'
   AND COLLATE(ANNUITY_TYPE, 'en-ci-rtrim') = 'NA')