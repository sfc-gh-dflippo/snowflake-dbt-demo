{{ config(
    tags=['m_MT_RSTD_BKGS_MSR_ANNUITY']
) }}
{{ config(materialized='table') }}
-- Self-referencing table(s): 'WI_MT_RSTD_BKGS_MEASURE' used as both source and target in this mapping.
-- Materialized as TABLE to snapshot source data before the target model overwrites it.
{% if var('m_MT_RSTD_BKGS_MSR_ANNUITY_sq_1_wi_mt_rstd_bkgs_measure_sql_override', '') != '' %}
{{ var('m_MT_RSTD_BKGS_MSR_ANNUITY_sq_1_wi_mt_rstd_bkgs_measure_sql_override') }}
{% else %}
-- Mapping-level SQL Query override (from Source Qualifier 'Sql Query' property)
SELECT
   BOOKINGS_MEASURE_KEY,
   MT.BKGS_MEASURE_TRANS_TYPE_CODE,
   BOOKINGS_PROCESS_DATE,
   SALES_TERRITORY_KEY,
   SALES_REP_NUMBER,
   RU_SERVICE_CONTRACT_START_DTM,
   RU_SERVICE_CONTRACT_END_DTM,
   DV_CONTRACT_DURATION,
   DV_ANNUALIZED_FLG,
   DV_ANNUALIZED_US_NET_AMT,
   DV_MULTIYEAR_US_NET_AMT,
   CASE
      WHEN DV_CONTRACT_DURATION <> 0
         THEN DD_COMP_US_NET_PRICE_AMOUNT / DV_CONTRACT_DURATION
      ELSE 0
   END AS PER_MONTH_AMT,
   CAST(TRUNC(DV_CONTRACT_DURATION / 12) AS INTEGER) CONTRACT_TERM,
   RSTART.FISCAL_YEAR_MONTH_INT CONTRACT_START_MONTH,
   RBKGS.FISCAL_YEAR_MONTH_INT BOOKINGS_PROCESS_MONTH,
   CASE
      WHEN COLLATE(DV_ANNUALIZED_FLG, 'en-ci-rtrim') = 'N'
         THEN CASE
            WHEN COLLATE(MT.BKGS_MEASURE_TRANS_TYPE_CODE, 'en-ci-rtrim') <> 'POS'
            OR (COLLATE(MT.BKGS_MEASURE_TRANS_TYPE_CODE, 'en-ci-rtrim') = 'POS'
            AND DV_CONTRACT_DURATION IS NOT NULL)
               THEN CASE
                  WHEN DV_CONTRACT_DURATION IS NOT NULL
                  AND MT.RU_SERVICE_CONTRACT_START_DTM IS NOT NULL
                  AND MT.RU_SERVICE_CONTRACT_END_DTM IS NOT NULL
                     THEN CASE
                        WHEN RSTART.FISCAL_YEAR_MONTH_INT IS NOT NULL
                           THEN CASE
                              WHEN ((CAST((CAST(MT.RU_SERVICE_CONTRACT_END_DTM AS DATE) - CAST(MT.BOOKINGS_PROCESS_DATE AS DATE)) AS INTEGER)) <= 0)
                              AND (CAST((CAST(MT.RU_SERVICE_CONTRACT_START_DTM AS DATE) - CAST(MT.BOOKINGS_PROCESS_DATE AS DATE)) AS INTEGER)) < 0
                                 THEN 'ANNUITY1'
                              WHEN ((CAST((CAST(MT.RU_SERVICE_CONTRACT_START_DTM AS DATE) - CAST(MT.BOOKINGS_PROCESS_DATE AS DATE)) AS INTEGER)) BETWEEN 1 AND 335)
                                 THEN 'ANNUITY2'
                              WHEN (CAST((CAST(MT.RU_SERVICE_CONTRACT_START_DTM AS DATE) - CAST(MT.BOOKINGS_PROCESS_DATE AS DATE)) AS INTEGER)) > 335
                                 THEN 'ANNUITY2'
                              WHEN ((CAST((CAST(MT.RU_SERVICE_CONTRACT_START_DTM AS DATE) - CAST(MT.BOOKINGS_PROCESS_DATE AS DATE)) AS INTEGER)) BETWEEN -364 AND -1)
                              AND (CAST((CAST(MT.RU_SERVICE_CONTRACT_END_DTM AS DATE) - CAST(MT.BOOKINGS_PROCESS_DATE AS DATE)) AS INTEGER)) > 0
                                 THEN 'ANNUITY2'
                              WHEN ((CAST((CAST(MT.RU_SERVICE_CONTRACT_START_DTM AS DATE) - CAST(MT.BOOKINGS_PROCESS_DATE AS DATE)) AS INTEGER)) <= -365)
                              AND (CAST((CAST(MT.RU_SERVICE_CONTRACT_END_DTM AS DATE) - CAST(MT.BOOKINGS_PROCESS_DATE AS DATE)) AS INTEGER)) > 0
                                 THEN 'ANNUITY3'
                              WHEN (CAST((CAST(MT.RU_SERVICE_CONTRACT_START_DTM AS DATE) - CAST(MT.BOOKINGS_PROCESS_DATE AS DATE)) AS INTEGER)) = 0
                                 THEN 'ANNUITY2'
                              ELSE 'NA'
                           END
                        ELSE 'NA'
                     END
                  WHEN DV_CONTRACT_DURATION IS NOT NULL
                  AND (MT.RU_SERVICE_CONTRACT_START_DTM IS NULL
                  OR MT.RU_SERVICE_CONTRACT_END_DTM IS NULL)
                     THEN 'ANNUITY6'
                  ELSE 'NA'
               END
            WHEN COLLATE(MT.BKGS_MEASURE_TRANS_TYPE_CODE, 'en-ci-rtrim') = 'POS'
            AND DV_CONTRACT_DURATION IS NULL
               THEN 'ANNUITY5' /*   for  DISTI POS ratio Transaction having only duration  no start date and end date */
            ELSE 'NA'
         END
      ELSE NULL
   END ANNUITY_TYPE,
   MT.DV_FMV_FLG,
   MT.ADJUSTMENT_CODE
FROM
   {{ var('m_MT_RSTD_BKGS_MSR_ANNUITY_SLSORDVWDB') }}.MT_RSTD_BKGS_MEASURE MT
   LEFT OUTER JOIN
      {{ var('m_MT_RSTD_BKGS_MSR_ANNUITY_COMREFVWDB') }}.R_FISCAL_DAY_TO_YEAR RSTART /*Performance Recommendation*/
      ON CAST(MT.RU_SERVICE_CONTRACT_START_DTM AS DATE) = RSTART.CALENDAR_DATE
   INNER JOIN
      {{ var('m_MT_RSTD_BKGS_MSR_ANNUITY_COMREFVWDB') }}.R_FISCAL_DAY_TO_YEAR RBKGS
      ON MT.BOOKINGS_PROCESS_DATE = RBKGS.CALENDAR_DATE
WHERE
   COLLATE(SERVICE_FLG, 'en-ci-rtrim') = 'Y'
   AND COLLATE(EDW_UPDATE_DATETIME, 'en-ci-rtrim') > '{{ var('m_MT_RSTD_BKGS_MSR_ANNUITY_LastExtractDate') }}'
   AND MT.DV_FISCAL_YEAR_MTH_NUMBER_INT IN (
      SELECT
         FISCAL_YEAR_MTH_NUMBER_INT
      FROM
         {{ var('m_MT_RSTD_BKGS_MSR_ANNUITY_ETLVWDB') }}.BKG_PROCESS_DT_CNTRL
   )
   /* Added as part of Q3FY18 goponnus */
   AND RTRIM(MT.BKGS_MEASURE_TRANS_TYPE_CODE) NOT IN (COLLATE('XAAS', 'en-ci-rtrim')) /* END Q3FY18 */
{% endif %}