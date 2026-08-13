-- MAC002: another single caller
{% macro apply_scd_logic(key_col, date_col) %}
    , {{ key_col }} as scd_key
    , {{ date_col }} as scd_date
{% endmacro %}
