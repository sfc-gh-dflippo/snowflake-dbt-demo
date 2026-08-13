{% macro trivial_fmt(col) %}coalesce({{ col }}, 0){% endmacro %}
