{% macro get_scd_sql(scd_source_sql, scd_surrogate_key, scd_integration_key, scd_cdc_hash_key, scd_dbt_updated_at="dbt_updated_at", scd_dbt_inserted_at="dbt_inserted_at") -%}

{#- You can skip using a sequence based surrogate key if you set config->unique_key to your integration key and pass None to scd_surrogate_key  -#}

with source_data as (

    {{ scd_source_sql }}

),

existing_data as (

    {% if is_incremental() -%}

    select
        {% if scd_surrogate_key -%}  {{ scd_surrogate_key }},  {%- endif %}
        {{ scd_integration_key }},
        {{ scd_cdc_hash_key }},
        {{ scd_dbt_inserted_at }}
    from {{ this }}

    {%- else -%}

    select
        {% if scd_surrogate_key -%}  null::integer {{ scd_surrogate_key }},  {%- endif %}
        null::varchar {{ scd_integration_key }},
        null::integer {{ scd_cdc_hash_key }},
        null::timestamp_ntz {{ scd_dbt_inserted_at }}
    limit 0

    {%- endif %}

),

inserts as (
    select
        {% if scd_surrogate_key -%}  {{ sequence_get_nextval() }} as {{ scd_surrogate_key }},  {%- endif %}
        source_data.*,
        sysdate() as {{ scd_dbt_inserted_at }},
        sysdate() as {{ scd_dbt_updated_at }}
    from source_data
    left outer join existing_data on source_data.{{ scd_integration_key }} = existing_data.{{ scd_integration_key }}
    where existing_data.{{ scd_integration_key }} is null
),

updates as (
    select
        {% if scd_surrogate_key -%}  existing_data.{{ scd_surrogate_key }},  {%- endif %}
        source_data.*,
        existing_data.{{ scd_dbt_inserted_at }},
        sysdate() as {{ scd_dbt_updated_at }}
    from source_data
    join existing_data on source_data.{{ scd_integration_key }} = existing_data.{{ scd_integration_key }}
    where source_data.{{ scd_cdc_hash_key }} <> existing_data.{{ scd_cdc_hash_key }}
)

select * from inserts
union all
select * from updates

{% endmacro %}
