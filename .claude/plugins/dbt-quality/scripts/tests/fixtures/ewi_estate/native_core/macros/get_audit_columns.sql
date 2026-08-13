{% macro get_audit_columns() %}
    current_timestamp() as _loaded_at,
    current_user() as _loaded_by
{% endmacro %}
