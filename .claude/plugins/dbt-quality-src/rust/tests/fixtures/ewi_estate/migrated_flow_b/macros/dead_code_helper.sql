-- MAC003: unused macro (never called anywhere)
{% macro dead_code_helper(x, y) %}
    {{ x }} + {{ y }}
{% endmacro %}
