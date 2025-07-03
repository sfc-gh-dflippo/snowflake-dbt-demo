{#
    Either of these macros will cause dbt to automatically refresh dynamic tables. Without this, a dynamic table may not
    be up to date when queried in a downstream model.
#}


{# This is a simple post-hook macro that can be added to cause dynamic tables to automatically refresh if they are not up to date. #}
{% macro dynamic_table_refresh_hook() -%}
    {% if execute and flags.WHICH in ('run', 'build') and model.config.materialized == "dynamic_table"%}
        {% do run_query( snowflake__refresh_dynamic_table(this) ) %}
    {% endif %}
{%- endmacro %}


