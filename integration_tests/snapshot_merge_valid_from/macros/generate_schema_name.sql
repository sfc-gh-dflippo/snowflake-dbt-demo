{#- Use the configured schema name as is, so each test arm gets a fixed schema. -#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {{ custom_schema_name or target.schema }}
{%- endmacro %}
