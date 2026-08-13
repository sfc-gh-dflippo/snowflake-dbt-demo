-- MAC002: single caller macro (only called from int_transactions_jinja)
{% macro add_audit_fields(pk_col) %}
    , current_timestamp() as _loaded_at
    , '{{ pk_col }}' as _pk_column
{% endmacro %}
