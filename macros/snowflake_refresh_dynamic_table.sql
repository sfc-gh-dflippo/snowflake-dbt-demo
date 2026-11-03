{#- dbt-quality: ignore-file SSC-EWI-DBTMAC0003 -#}
{#- MAC0003 waived. Project-level post-hook dynamic_table_refresh_hook(), enabled in dbt_project.yml. -#}
{#
    dbt does not refresh an existing dynamic table when its config is unchanged.
    This post-hook refreshes each dynamic table when dbt runs or builds it.
    Side effect: runs ALTER DYNAMIC TABLE <this> REFRESH in Snowflake.
#}


{% macro dynamic_table_refresh_hook() -%}
    {% if execute and flags.WHICH in ('run', 'build') and model.config.materialized == "dynamic_table"%}
        {% do run_query( snowflake__refresh_dynamic_table(this) ) %}
    {% endif %}
{%- endmacro %}
