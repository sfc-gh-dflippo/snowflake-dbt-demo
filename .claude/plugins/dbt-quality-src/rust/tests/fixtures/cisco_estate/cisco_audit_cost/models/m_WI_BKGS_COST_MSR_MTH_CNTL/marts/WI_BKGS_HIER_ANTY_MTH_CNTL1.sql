{{ config(
    tags=['m_WI_BKGS_COST_MSR_MTH_CNTL'],
    database=var('sc_override_wi_bkgs_hier_anty_mth_cntl1_db'),
    schema=var('sc_override_wi_bkgs_hier_anty_mth_cntl1_schema'),
    alias=var('sc_override_wi_bkgs_hier_anty_mth_cntl1_table')
) }}
{{ config(materialized='table') }}
-- Pre/Post SQL hooks: the orchestration task may override these defaults at runtime via dbt --vars.
{% set pre_sql = var('m_WI_BKGS_COST_MSR_MTH_CNTL_wi_bkgs_hier_anty_mth_cntl1_pre_sql', '') %}
{% set post_sql = var('m_WI_BKGS_COST_MSR_MTH_CNTL_wi_bkgs_hier_anty_mth_cntl1_post_sql', '') %}
{% if pre_sql != '' and post_sql != '' %}
  {{ config(pre_hook=pre_sql, post_hook=post_sql) }}
{% elif pre_sql != '' %}
  {{ config(pre_hook=pre_sql) }}
{% elif post_sql != '' %}
  {{ config(post_hook=post_sql) }}
{% endif %}
--** SSC-FDM-INF0058 - TABLE 'WI_BKGS_HIER_ANTY_MTH_CNTL' IS USED AS BOTH SOURCE AND TARGET IN THIS MAPPING. DBT EXECUTION ORDER HAS BEEN ADJUSTED TO PREVENT CIRCULAR DATA CORRUPTION: SEE STAGING AND MART MODELS FOR DETAILS. **
WITH source_data AS
(
   SELECT
      FISCAL_YEAR_MTH_NUMBER_INT,
      RUN_BATCH_ID,
      INC_FLAG
   FROM
      {{ ref('stg_raw__SQ_1_WI_BKGS_HIER_ANTY_MTH_CNTL') }}
)
SELECT
   sd.FISCAL_YEAR_MTH_NUMBER_INT AS FISCAL_YEAR_MTH_NUMBER_INT,
   sd.RUN_BATCH_ID AS RUN_BATCH_ID,
   sd.INC_FLAG AS INC_FLAG
FROM
   source_data AS sd