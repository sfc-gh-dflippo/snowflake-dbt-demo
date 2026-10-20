{% macro m_update_row_count_variable(variable_name, target_relation, variable_scope) %}
  {# Step 1: Construct the specific SQL string for counting rows. #}
  {% set count_sql = "SELECT COUNT(*) FROM " ~ target_relation %}
  {{ log("m_update_row_count_variable started. Received value: " ~ count_sql, info=True) }}

  {# Step 2: Call m_update_control_variable with the COUNT query. #}
  {{ m_update_control_variable(variable_name, count_sql, variable_scope) }}
{% endmacro %}