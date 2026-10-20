{{ config(
    alias='WI_AUD_RSTD_BKG_THRSHLD_VALUES'
) }}
{{ config(materialized='table') }}
-- Pre/Post SQL hooks: the orchestration task may override these defaults at runtime via dbt --vars.
{% set post_sql = var('m_WI_AUD_RSTD_BKGS_MEASURE_ORDER_MTH_wi_aud_rstd_bkg_thrshld_values1_post_sql', '') %}
{% if post_sql != '' %}
  {{ config(post_hook=post_sql) }}
{% endif %}
--** SSC-FDM-INF0058 - TABLE 'WI_AUD_RSTD_BKG_THRSHLD_VALUES' IS USED AS BOTH SOURCE AND TARGET IN THIS MAPPING. DBT EXECUTION ORDER HAS BEEN ADJUSTED TO PREVENT CIRCULAR DATA CORRUPTION: SEE STAGING AND MART MODELS FOR DETAILS. **
WITH source_data AS
(
   SELECT
      AUDIT_TABLE_NAME,
      AUDIT_COLUMN_NAME
   FROM
      {{ ref('int_FILTRANS') }}
)
SELECT
   sd.AUDIT_TABLE_NAME AS AUDIT_TABLE_NAME,
   sd.AUDIT_COLUMN_NAME AS AUDIT_COLUMN_NAME
FROM
   source_data AS sd