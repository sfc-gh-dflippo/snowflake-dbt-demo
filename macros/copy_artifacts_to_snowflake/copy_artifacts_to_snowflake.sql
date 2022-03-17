{%- macro copy_artifacts_to_snowflake() -%}

  {% set dbt_artifacts_database = var('dbt_artifacts_database', 'COMMON_LOGGING') -%}
  {% set dbt_artifacts_schema = var('dbt_artifacts_schema', 'DBT_ARTIFACTS') -%}
  {% set dbt_artifacts_stage = api.Relation.create(dbt_artifacts_database, dbt_artifacts_schema, var('dbt_artifacts_stage', 'TMP_DBT_ARTIFACTS_STAGE')) -%}
  {% set dbt_artifacts_procedure = api.Relation.create(dbt_artifacts_database, dbt_artifacts_schema, var('dbt_artifacts_procedure', 'LOG_DBT_ARTIFACTS')) -%}

  {%- set query -%}
  
  CREATE TEMPORARY STAGE IF NOT EXISTS {{dbt_artifacts_stage}} FILE_FORMAT=(TYPE='JSON')
  
  {%- endset -%}
  {%- do log("Create temporary stage: " ~ query, info=True) -%}
  {%- do run_query(query) -%}

  {%- set query -%}
  
  PUT file://target/*.json @{{dbt_artifacts_stage}}
  
  {#- Uploading dbt artifacts to stage */ -#}
  {%- endset -%}
  {%- do log("Upload JSON files: " ~ query, info=True) -%}
  {%- do run_query(query) -%}

  {%- set query -%}
  
  CALL {{dbt_artifacts_procedure}}( '{{dbt_artifacts_stage}}' )
  
  {%- endset -%}
  {%- do log("Load JSON files into DBT_ARTIFACTS: " ~ query, info=True) -%}
  {%- do run_query(query) -%}

{%- endmacro -%}