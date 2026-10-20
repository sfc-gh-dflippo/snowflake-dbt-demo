{{ config(
    alias='WI_PRODUCT_HWSW_MONTH_CTRL'
) }}
{{ config(materialized='table') }}
-- Pre/Post SQL hooks: the orchestration task may override these defaults at runtime via dbt --vars.
{% set pre_sql = var('m_MT_PRODUCT_HWSW_ANNUITY_wi_product_hwsw_month_ctrl1_pre_sql', '') %}
{% set post_sql = var('m_MT_PRODUCT_HWSW_ANNUITY_wi_product_hwsw_month_ctrl1_post_sql', '') %}
{% if pre_sql != '' and post_sql != '' %}
  {{ config(pre_hook=pre_sql, post_hook=post_sql) }}
{% elif pre_sql != '' %}
  {{ config(pre_hook=pre_sql) }}
{% elif post_sql != '' %}
  {{ config(post_hook=post_sql) }}
{% endif %}
--** SSC-FDM-INF0058 - TABLE 'WI_PRODUCT_HWSW_MONTH_CTRL' IS USED AS BOTH SOURCE AND TARGET IN THIS MAPPING. DBT EXECUTION ORDER HAS BEEN ADJUSTED TO PREVENT CIRCULAR DATA CORRUPTION: SEE STAGING AND MART MODELS FOR DETAILS. **
WITH source_data AS
(
   SELECT
      FISCAL_YEAR_MONTH_INT
   FROM
      {{ ref('stg_raw__SQ_WI_PRODUCT_HWSW_MONTH_CTRL') }}
)
SELECT
   sd.FISCAL_YEAR_MONTH_INT AS FISCAL_YEAR_MONTH_INT
FROM
   source_data AS sd