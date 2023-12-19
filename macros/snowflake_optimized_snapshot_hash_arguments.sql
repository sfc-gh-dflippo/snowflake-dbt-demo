
{#
    This macro returns the concatenated string without the MD5 function applied.
    This improves performance because dbt joins on these columns when it merges data
    and Snowflake is unable to prune on hashed values. Unless this macro is added
    before a snapshot is created, a new record will be created for every incoming
    record becase the hash will have changed.

    You can avoid this issue by adding the following to your dbt_project.yml before your first execution.
    You will want to remove this afterwards because the one-time update is relatively expensive.

snapshots:
    pre-hook: "{{ refresh_dbt_scd_id() }}"

#}


{% macro snowflake__snapshot_hash_arguments(args) -%}
    ({%- for arg in args -%}
        coalesce(cast({{ arg }} as varchar ), '')
        {% if not loop.last %} || '|' || {% endif %}
    {%- endfor -%})::varchar
{%- endmacro %}


{% macro refresh_dbt_scd_id() -%}
    {% set config = model['config'] %}
    {% set unique_key = config.get('unique_key') %}
    {% set relation_exists = load_relation(this) is not none %}
    {% if relation_exists %}
        {{- log("Updating any dbt_scd_id keys that have changed in snapshot " ~ this, info=true) -}}
        update {{ this }}
        set dbt_scd_id = {{ snapshot_hash_arguments([unique_key, 'dbt_valid_from']) }}
        where dbt_scd_id != {{ snapshot_hash_arguments([unique_key, 'dbt_valid_from']) }}
    {% endif %}
{%- endmacro %}
