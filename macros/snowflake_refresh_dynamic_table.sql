{#
    This script replaces the out of the box materialization and will cause dbt to automatically
    refresh dynamic tables when there are no other changes. Without this, a dynamic table may not
    be up to date when queried in a downstream model.
#}
{% macro snowflake__dynamic_table_get_build_sql(existing_relation, target_relation) %}

    {% set full_refresh_mode = should_full_refresh() %}

    -- determine the scenario we're in: create, full_refresh, alter, refresh data
    {% if existing_relation is none %}
        {% set build_sql = get_create_sql(target_relation, sql) %}
    {% elif full_refresh_mode or not existing_relation.is_dynamic_table %}
        {% set build_sql = get_replace_sql(existing_relation, target_relation, sql) %}
    {% else %}

        -- get config options
        {% set on_configuration_change = config.get('on_configuration_change') %}
        {% set configuration_changes = snowflake__get_dynamic_table_configuration_changes(existing_relation, config) %}

        {% if configuration_changes is none %}
            {% set build_sql = snowflake__refresh_dynamic_table(target_relation) %}
            {{ exceptions.warn("No configuration changes were identified on: `" ~ target_relation ~ "`. Refreshing.") }}

        {% elif on_configuration_change == 'apply' %}
            {% set build_sql = snowflake__get_alter_dynamic_table_as_sql(existing_relation, configuration_changes, target_relation, sql) %}
        {% elif on_configuration_change == 'continue' %}
            {% set build_sql = snowflake__refresh_dynamic_table(target_relation) %}
            {{ exceptions.warn("Configuration changes were identified and `on_configuration_change` was set to `continue` for `" ~ target_relation ~ "`. Refreshing.") }}
        {% elif on_configuration_change == 'fail' %}
            {{ exceptions.raise_fail_fast_error("Configuration changes were identified and `on_configuration_change` was set to `fail` for `" ~ target_relation ~ "`") }}

        {% else %}
            -- this only happens if the user provides a value other than `apply`, 'continue', 'fail'
            {{ exceptions.raise_compiler_error("Unexpected configuration scenario: `" ~ on_configuration_change ~ "`") }}

        {% endif %}

    {% endif %}

    {% do return(build_sql) %}

{% endmacro %}

{% macro snowflake__get_alter_dynamic_table_as_sql(
    existing_relation,
    configuration_changes,
    target_relation,
    sql
) -%}
    {{- log('Applying ALTER to: ' ~ existing_relation) -}}

    {% if configuration_changes.requires_full_refresh %}
        {{- get_replace_sql(existing_relation, target_relation, sql) -}}

    {% else %}

        {%- set target_lag = configuration_changes.target_lag -%}
        {%- if target_lag -%}{{- log('Applying UPDATE TARGET_LAG to: ' ~ existing_relation) -}}{%- endif -%}
        {%- set snowflake_warehouse = configuration_changes.snowflake_warehouse -%}
        {%- if snowflake_warehouse -%}{{- log('Applying UPDATE WAREHOUSE to: ' ~ existing_relation) -}}{%- endif -%}

        alter dynamic table {{ existing_relation }} set
            {% if target_lag %}target_lag = '{{ target_lag.context }}'{% endif %}
            {% if snowflake_warehouse %}warehouse = {{ snowflake_warehouse.context }}{% endif %}
        ;
        {{ snowflake__refresh_dynamic_table(target_relation) }}

    {%- endif -%}

{%- endmacro %}
