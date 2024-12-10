{#
    Either of these macros will cause dbt to automatically refresh dynamic tables. Without this, a dynamic table may not
    be up to date when queried in a downstream model.
#}


{# This is a simple post-hook macro that can be added to cause dynamic tables to automatically refresh if they are not up to date. #}
{% macro dynamic_table_refresh_hook() -%}
    {% if execute and model.config.materialized == "dynamic_table" %}
        {% do run_query( snowflake__refresh_dynamic_table(this) ) %}
    {% endif %}
{%- endmacro %}


{#
    This macro extends the out of the box materialization and will cause dbt to automatically
    refresh dynamic tables when there are no other changes. Without this, a dynamic table may not
    be up to date when queried in a downstream model.
#}
{% macro dynamic_table_get_build_sql(existing_relation, target_relation) -%}
    {% set refresh_sql = snowflake__refresh_dynamic_table(target_relation) %}
    {% set new_build_sql -%}
    {# Get the existing SQL, remove the refresh if it already exists, and remove any trailing white space and semi-colons #}
    {{ dbt.dynamic_table_get_build_sql(existing_relation, target_relation) | replace(refresh_sql, "") | trim | trim(";") }};
    {{ refresh_sql }}
    {%- endset %}
    {% do log("Setting dynamic table to refresh: " ~ target_relation, info=false) %}
    {% do return(new_build_sql) %}
{%- endmacro %}
