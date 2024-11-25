{#- You can skip using a sequence based surrogate key if you set config->unique_key to your integration key and pass None to surrogate_key  -#}

{% macro get_scd_sql(scd_source_sql, surrogate_key=config.get("surrogate_key")) -%}

{%- set integration_key = config.get("integration_key", var("default_integration_id", "integration_id")) -%}
{%- set cdc_hash_key = config.get("cdc_hash_key", var("default_cdc_hash_key", "cdc_hash_key")) -%}
{%- set updated_at_column = config.get("updated_at_column", var("default_updated_at_column", "dbt_updated_ts")) -%}
{%- set inserted_at_column = config.get("inserted_at_column", var("default_inserted_at_column", "dbt_inserted_ts")) -%}

with source_data as (

    {{ scd_source_sql }}

),

existing_data as (

    {% if is_incremental() -%}

    select
        {% if surrogate_key -%}  {{ surrogate_key }},  {%- endif %}
        {{ integration_key }},
        {{ cdc_hash_key }},
        {{ inserted_at_column }}
    from {{ this }}

    {%- else -%}

    select
        {% if surrogate_key -%} null::integer as {{ surrogate_key }},  {%- endif %}
        null::varchar as {{ integration_key }},
        null::integer as {{ cdc_hash_key }},
        null::timestamp_ntz as {{ inserted_at_column }}
    limit 0

    {%- endif %}

),

inserts as (
    select
        {% if surrogate_key -%}  {{ sequence_get_nextval() }} as {{ surrogate_key }},  {%- endif %}
        source_data.*,
        sysdate() as {{ inserted_at_column }},
        sysdate() as {{ updated_at_column }}
    from source_data
    left outer join existing_data on source_data.{{ integration_key }} = existing_data.{{ integration_key }}
    where existing_data.{{ integration_key }} is null
),

updates as (
    select
        {% if surrogate_key -%}  existing_data.{{ surrogate_key }},  {%- endif %}
        source_data.*,
        existing_data.{{ inserted_at_column }},
        sysdate() as {{ updated_at_column }}
    from source_data
    join existing_data on source_data.{{ integration_key }} = existing_data.{{ integration_key }}
    where source_data.{{ cdc_hash_key }} <> existing_data.{{ cdc_hash_key }}
)

select * from inserts
union all
select * from updates

{% endmacro %}
