{% macro snowflake__create_table_as(temporary, relation, compiled_code, language='sql') -%}
  {%- set transient = config.get('transient', default=true) -%}

  {#- Provide more generic support for a table_type parameter and add Iceberg support -#}
  {%- set table_type = config.get('table_type', default="") -%}
  {%- set iceberg = (table_type.lower() == "iceberg") %}
  {% set iceberg_parameters = [
    ("external_volume", config.get('external_volume', default=none)),
    ("catalog", config.get('catalog', default=none)),
    ("catalog_table_name", config.get('catalog_table_name', default=none)),
    ("catalog_namespace", config.get('catalog_namespace', default=none)),
    ("metadata_file_path", config.get('metadata_file_path', default=none)),
    ("base_location", config.get('base_location', default=none))
   ] %}

  {% if temporary and table_type == "" -%}
    {%- set create_table_type = "temporary" -%}
    {%- set alter_table_type = "" -%}
  {%- elif transient and table_type == "" -%}
    {%- set create_table_type = "transient" -%}
    {%- set alter_table_type = "" -%}
  {%- else -%}
    {%- set create_table_type = table_type -%}
    {%- set alter_table_type = table_type -%}
  {%- endif %}

  {%- if language == 'sql' -%}
    {%- set cluster_by_keys = config.get('cluster_by', default=none) -%}
    {%- set enable_automatic_clustering = config.get('automatic_clustering', default=false) -%}
    {%- set copy_grants = config.get('copy_grants', default=false) -%}

    {%- if cluster_by_keys is not none and cluster_by_keys is string -%}
      {%- set cluster_by_keys = [cluster_by_keys] -%}
    {%- endif -%}
    {%- if cluster_by_keys is not none -%}
      {%- set cluster_by_string = cluster_by_keys|join(", ")-%}
    {% else %}
      {%- set cluster_by_string = none -%}
    {%- endif -%}
    {%- set sql_header = config.get('sql_header', none) -%}

    {{ sql_header if sql_header is not none }}

        create or replace {{ create_table_type }} table {{ relation }}
        {%- set contract_config = config.get('contract') -%}
        {%- if contract_config.enforced -%}
          {{ get_assert_columns_equivalent(sql) }}
          {{ get_table_columns_and_constraints() }}
          {% set compiled_code = get_select_subquery(compiled_code) %}
        {% endif %}
        {% for parameter_name, parameter_value in iceberg_parameters if parameter_value is not none -%}
          {{ parameter_name }} = '{{ parameter_value }}'
        {% endfor %}
        {% if copy_grants and not temporary -%} copy grants {%- endif %} as
        (
          {%- if cluster_by_string is not none -%}
            select * from (
              {{ compiled_code }}
              ) order by ({{ cluster_by_string }})
          {%- else -%}
            {{ compiled_code }}
          {%- endif %}
        );
      {% if cluster_by_string is not none and not temporary -%}
        alter {{ alter_table_type }} table {{relation}} cluster by ({{cluster_by_string}});
      {%- endif -%}
      {% if enable_automatic_clustering and cluster_by_string is not none and not temporary  -%}
        alter {{ alter_table_type }} table {{relation}} resume recluster;
      {%- endif -%}

  {%- elif language == 'python' -%}
    {{ py_write_table(compiled_code=compiled_code, target_relation=relation, table_type=table_type) }}
  {%- else -%}
      {% do exceptions.raise_compiler_error("snowflake__create_table_as macro didn't get supported language, it got %s" % language) %}
  {%- endif -%}

{% endmacro %}
