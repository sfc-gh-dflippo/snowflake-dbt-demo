-- MAC004: trivial wrapper macro (one expression, no logic)
{% macro trivial_wrapper(col) %}
    upper({{ col }})
{% endmacro %}
