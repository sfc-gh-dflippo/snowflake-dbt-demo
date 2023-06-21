{% macro get_snapshot_config() -%}
    {%- set config = model['config'] -%}
    {%- set surrogate_key = config.get("surrogate_key") -%}
    {% if surrogate_key %}
        {%- set surrogate_key_sequence = config.get("surrogate_key_sequence", surrogate_key ~ "_SEQ") -%}
        {%- set surrogate_key_sequence_relation = api.Relation.create(
            database = this.database,
            schema = this.schema,
            identifier = surrogate_key_sequence) -%}
    {%- else %}
        {%- set surrogate_key_sequence = none -%}
        {%- set surrogate_key_sequence_relation = none -%}
    {%- endif %}
    {% do return({
            "unique_key": config.get("unique_key"),
            "dbt_updated_at_column": config.get("dbt_updated_at_column", "dbt_updated_at"),
            "dbt_valid_from_column": config.get("dbt_valid_from_column", "dbt_valid_from"),
            "dbt_valid_to_column": config.get("dbt_valid_to_column", "dbt_valid_to"),
            "dbt_scd_id_column": config.get("dbt_scd_id_column", "dbt_scd_id"),
            "dbt_current_flag_column": config.get("dbt_current_flag_column"),
            "surrogate_key": surrogate_key,
            "surrogate_key_sequence_relation": surrogate_key_sequence_relation
        }) %}
{% endmacro %}


{% macro snapshot_hash_arguments(args) -%}
    hash({{ args | join(", ")}})
{%- endmacro %}


{% macro snapshot_staging_table(strategy, source_sql, target_relation) -%}
    {%- set config = get_snapshot_config() -%}
    {% if config.surrogate_key_sequence_relation and execute %}
        {%- set sequence_create_statement -%}
        create sequence if not exists {{config.surrogate_key_sequence_relation}}
        {%- endset -%}
        {%- do run_query(sequence_create_statement) -%}
        {%- set sequence_nextval_stmt = config.surrogate_key_sequence_relation ~ ".nextval, " -%}
    {%- endif %}

    with snapshot_query as (

        {{ source_sql }}

    ),

    snapshotted_data as (

        select *,
            {{ strategy.unique_key }} as dbt_unique_key

        from {{ target_relation }}
        where {{config.dbt_scd_id_column}} is null

    ),

    insertions_source_data as (

        select
            *,
            {{ strategy.unique_key }} as dbt_unique_key,
            {{ strategy.updated_at }} as {{config.dbt_updated_at_column}},
            {{ strategy.updated_at }} as {{config.dbt_valid_from_column}},
            nullif({{ strategy.updated_at }}, {{ strategy.updated_at }}) as {{config.dbt_valid_to_column}},
            {% if config.dbt_current_flag_column %}'Y' as {{config.dbt_current_flag_column}},{% endif %}
            {{ strategy.scd_id }} as {{ config.dbt_scd_id_column }}

        from snapshot_query
    ),

    updates_source_data as (

        select
            *,
            {{ strategy.unique_key }} as dbt_unique_key
        from snapshot_query
    ),

    {%- if strategy.invalidate_hard_deletes %}

    deletes_source_data as (

        select
            *,
            {{ strategy.unique_key }} as dbt_unique_key
        from snapshot_query
    ),
    {% endif %}

    insertions as (

        select
            'insert' as dbt_change_type,
            {% if config.surrogate_key %}{{config.surrogate_key_sequence_relation}}.nextval as {{config.surrogate_key}},{% endif %}
            source_data.*

        from insertions_source_data as source_data
        left outer join snapshotted_data on snapshotted_data.dbt_unique_key = source_data.dbt_unique_key
        where snapshotted_data.dbt_unique_key is null
           or (
                snapshotted_data.dbt_unique_key is not null
            and (
                {{ strategy.row_changed }}
            )
        )

    ),

    updates as (

        select
            'update' as dbt_change_type,
            {% if config.surrogate_key %}null as {{config.surrogate_key}},{% endif %}
            source_data.*,
            snapshotted_data.{{config.dbt_updated_at_column}},
            snapshotted_data.{{config.dbt_valid_from_column}},
            snapshotted_data.{{config.dbt_valid_to_column}},
            {% if config.dbt_current_flag_column %}'N' as {{config.dbt_current_flag_column}},{% endif %}
            snapshotted_data.{{config.dbt_scd_id_column}}

        from updates_source_data as source_data
        join snapshotted_data on snapshotted_data.dbt_unique_key = source_data.dbt_unique_key
        where (
            {{ strategy.row_changed }}
        )
    )

    {%- if strategy.invalidate_hard_deletes -%}
    ,

    deletes as (

        select
            'delete' as dbt_change_type,
            {% if config.surrogate_key %}null as {{config.surrogate_key}},{% endif %}
            source_data.*,
            {{ snapshot_get_time() }} as {{config.dbt_valid_from_column}},
            {{ snapshot_get_time() }} as {{config.dbt_updated_at_column}},
            {{ snapshot_get_time() }} as {{config.dbt_valid_to_column}},
            {% if config.dbt_current_flag_column %}'N' as {{config.dbt_current_flag_column}},{% endif %}
            snapshotted_data.{{config.dbt_scd_id_column}}

        from snapshotted_data
        left join deletes_source_data as source_data on snapshotted_data.dbt_unique_key = source_data.dbt_unique_key
        where source_data.dbt_unique_key is null
    )
    {%- endif %}

    select * from insertions
    union all
    select * from updates
    {%- if strategy.invalidate_hard_deletes %}
    union all
    select * from deletes
    {%- endif %}

{%- endmacro %}


{% macro build_snapshot_table(strategy, sql) %}
    {%- set config = get_snapshot_config() -%}

    select
        {% if config.surrogate_key %}{{config.surrogate_key_sequence_relation}}.nextval as {{config.surrogate_key}},{% endif %}
        *,
        {{ strategy.scd_id }} as {{config.dbt_scd_id_column}},
        {{ strategy.updated_at }} as {{config.dbt_updated_at_column}},
        {{ strategy.updated_at }} as {{config.dbt_valid_from_column}},
        nullif({{ strategy.updated_at }}, {{ strategy.updated_at }}) as {{config.dbt_valid_to_column}}
        {%- if config.dbt_current_flag_column -%},
        'Y' AS {{ config.dbt_current_flag_column }}
        {%- endif %}
    from (
        {{ sql }}
    ) sbq

{% endmacro %}


{%- macro snapshot_sequence_get_nextval(surrogate_key_sequence_relation) -%}

    {% if execute %}

        {%- set sequence_create_statement -%}
        create sequence if not exists {{sesurrogate_key_sequence_relationquence}}
        {%- endset -%}
        {%- do run_query(sequence_create_statement) -%}

    {%- endif -%}

    {{ return(sequence ~ ".nextval") }}

{%- endmacro -%}


{% macro snapshot_merge_sql(target, source, insert_cols) -%}
    {%- set config = get_snapshot_config() -%}
    {%- set insert_cols_csv = insert_cols | join(', ') -%}

    merge into {{ target }} as DBT_INTERNAL_DEST
    using {{ source }} as DBT_INTERNAL_SOURCE
    on DBT_INTERNAL_SOURCE.{{config.dbt_scd_id_column}} = DBT_INTERNAL_DEST.{{config.dbt_scd_id_column}}
        and DBT_INTERNAL_SOURCE.{{config.unique_key}} = DBT_INTERNAL_DEST.{{config.unique_key}}
        and DBT_INTERNAL_SOURCE.{{config.dbt_valid_from_column}} = DBT_INTERNAL_DEST.{{config.dbt_valid_from_column}}
    when matched
     and DBT_INTERNAL_DEST.{{config.dbt_valid_to_column}} is null
     and DBT_INTERNAL_SOURCE.dbt_change_type in ('update', 'delete')
        then update
        set {{config.dbt_valid_to_column}} = DBT_INTERNAL_SOURCE.{{config.dbt_valid_to_column}}
        {%- if config.dbt_current_flag_column -%},
        {{ config.dbt_current_flag_column }} = DBT_INTERNAL_SOURCE.{{config.dbt_current_flag_column}}
        {%- endif %}
    when not matched
     and DBT_INTERNAL_SOURCE.dbt_change_type = 'insert'
        then insert ({{ insert_cols_csv }})
        values ({{ insert_cols_csv }})

{% endmacro %}
