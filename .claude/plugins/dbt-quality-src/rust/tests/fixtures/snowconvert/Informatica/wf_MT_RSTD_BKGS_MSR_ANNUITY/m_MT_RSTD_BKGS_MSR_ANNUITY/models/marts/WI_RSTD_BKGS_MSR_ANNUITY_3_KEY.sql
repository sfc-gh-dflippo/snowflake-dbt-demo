{{ config(materialized='table') }}
-- Pre/Post SQL hooks: the orchestration task may override these defaults at runtime via dbt --vars.
{% set pre_sql = var('m_MT_RSTD_BKGS_MSR_ANNUITY_wi_rstd_bkgs_msr_annuity_3_key_pre_sql', '') %}
{% set post_sql = var('m_MT_RSTD_BKGS_MSR_ANNUITY_wi_rstd_bkgs_msr_annuity_3_key_post_sql', '') %}
{% if pre_sql != '' and post_sql != '' %}
  {{ config(pre_hook=pre_sql, post_hook=post_sql) }}
{% elif pre_sql != '' %}
  {{ config(pre_hook=pre_sql) }}
{% elif post_sql != '' %}
  {{ config(post_hook=post_sql) }}
{% endif %}
--** SSC-FDM-INF0058 - TABLE 'WI_RSTD_BKGS_MSR_ANNUITY_3_KEY' IS USED AS BOTH SOURCE AND TARGET IN THIS MAPPING. DBT EXECUTION ORDER HAS BEEN ADJUSTED TO PREVENT CIRCULAR DATA CORRUPTION: SEE STAGING AND MART MODELS FOR DETAILS. **
WITH source_data AS
(
   SELECT
      BOOKINGS_MEASURE_KEY,
      BKGS_MEASURE_TRANS_TYPE_CODE,
      BOOKINGS_PROCESS_DATE,
      SALES_TERRITORY_KEY,
      SALES_REP_NUMBER,
      ANNUITY_TYPE,
      DV_FMV_FLG,
      ADJUSTMENT_CODE
   FROM
      {{ ref('stg_raw__SQ_4_WI_RSTD_BKGS_MSR_ANNUITY_3_KEY') }}
)
SELECT
   sd.BOOKINGS_MEASURE_KEY AS BOOKINGS_MEASURE_KEY,
   sd.BKGS_MEASURE_TRANS_TYPE_CODE AS BKGS_MEASURE_TRANS_TYPE_CODE,
   sd.BOOKINGS_PROCESS_DATE AS BOOKINGS_PROCESS_DATE,
   sd.SALES_TERRITORY_KEY AS SALES_TERRITORY_KEY,
   sd.SALES_REP_NUMBER AS SALES_REP_NUMBER,
   sd.ANNUITY_TYPE AS ANNUITY_TYPE,
   sd.DV_FMV_FLG AS DV_FMV_FLG,
   sd.ADJUSTMENT_CODE AS ADJUSTMENT_CODE
FROM
   source_data AS sd