{% macro m_update_control_variable(variable_name, new_value_sql, variable_scope) %}
  UPDATE public.control_variables
  SET
    variable_value = ({{new_value_sql}}),
    last_updated_at = CURRENT_TIMESTAMP()
  WHERE
    variable_name = '{{ variable_name }}'
    AND variable_scope = '{{ variable_scope }}';
{% endmacro %}