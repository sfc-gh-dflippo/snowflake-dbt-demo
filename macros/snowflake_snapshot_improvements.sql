{#
    Overrides of three dbt snapshot macros for Snowflake.

    1. Merge on dbt_valid_from. The snapshot MERGE matches on dbt_valid_from as well as
       dbt_scd_id. Snowflake prunes micro-partitions on dbt_valid_from because it grows
       with load time. It cannot prune on dbt_scd_id because that column is a hash.
       - default__snapshot_staging_table: 'update' and 'delete' rows carry the
         dbt_valid_from of the target row. The MERGE uses this value only in the join.
       - default__snapshot_merge_sql: the ON clause adds a null-safe dbt_valid_from match.
         New 'insert' rows have a new dbt_scd_id, so they still go to "when not matched".

    2. Optional sequence-based surrogate key. Set it in the snapshot config:
           meta={'surrogate_key': 'my_dim_wid'}   or   surrogate_key='my_dim_wid'
       - The key is the first column of the snapshot table.
       - 'insert' rows get the next value of the sequence <snapshot name>_SEQ.
         sequence_nextval_as_surrogate_key creates the sequence above the high watermark.
       - 'update' and 'delete' rows carry the key of the target row.
       - The MERGE also matches on the key.

    dbt Core (dbt-adapters) and dbt Fusion 2.0 ship the same text for these macros.
    snowflake__snapshot_merge_sql calls default__snapshot_merge_sql and adds the explicit
    transaction, so this override keeps that behavior.
    It is compatible with snowflake__snapshot_hash_arguments in
    snowflake_optimized_snapshot_hash_arguments.sql. Either file works without the other.

    The macros copy the upstream body. Compare them with upstream after each dbt upgrade.
    Changed lines are marked "merge_on_valid_from" or "surrogate_key".
    "union all" matches columns by position, so every CTE must list the columns in the
    same order: dbt_change_type, surrogate key, source columns, dbt metadata columns.
#}

{#- surrogate_key: return the configured surrogate key column name, or none. -#}
{% macro snapshot_surrogate_key() -%}
    {%- set meta = config.get('meta') or {} -%}
    {{ return(config.get('surrogate_key') or meta.get('surrogate_key')) }}
{%- endmacro %}

{% macro default__snapshot_staging_table(strategy, source_sql, target_relation) -%}
    {% set columns = config.get('snapshot_table_column_names') or get_snapshot_table_column_names() %}
    {#- surrogate_key: optional sequence-based key column. #}
    {% set surrogate_key = snapshot_surrogate_key() %}
    {% if surrogate_key %}
        {% set surrogate_key_seq = sequence_nextval_as_surrogate_key(surrogate_key) %}
    {% endif %}
    {% if strategy.hard_deletes == 'new_record' %}
        {% set new_scd_id = snapshot_hash_arguments([columns.dbt_scd_id, snapshot_get_time()]) %}
    {% endif %}
    with snapshot_query as (

        {{ source_sql }}

    ),

    snapshotted_data as (

        select *, {{ unique_key_fields(strategy.unique_key) }}
        from {{ target_relation }}
        where
            {% if config.get('dbt_valid_to_current') %}
                {% set source_unique_key = columns.dbt_valid_to | trim %}
                {% set target_unique_key = config.get('dbt_valid_to_current') | trim %}
                ( {{ equals(source_unique_key, target_unique_key) }} or {{ source_unique_key }} is null )
            {% else %}
                {{ columns.dbt_valid_to }} is null
            {% endif %}

    ),

    insertions_source_data as (

        select *, {{ unique_key_fields(strategy.unique_key) }},
            {{ strategy.updated_at }} as {{ columns.dbt_updated_at }},
            {{ strategy.updated_at }} as {{ columns.dbt_valid_from }},
            {{ get_dbt_valid_to_current(strategy, columns) }},
            {{ strategy.scd_id }} as {{ columns.dbt_scd_id }}

        from snapshot_query
    ),

    updates_source_data as (

        {#- merge_on_valid_from: the updates CTE adds dbt_valid_from and dbt_valid_to. #}
        select *, {{ unique_key_fields(strategy.unique_key) }},
            {{ strategy.updated_at }} as {{ columns.dbt_updated_at }}

        from snapshot_query
    ),

    {%- if strategy.hard_deletes == 'invalidate' or strategy.hard_deletes == 'new_record' %}

    deletes_source_data as (

        select *, {{ unique_key_fields(strategy.unique_key) }}
        from snapshot_query
    ),
    {% endif %}

    insertions as (

        select
            'insert' as dbt_change_type,
            {%- if surrogate_key %}
            {{ surrogate_key_seq }},
            {%- endif %}
            source_data.*
          {%- if strategy.hard_deletes == 'new_record' -%}
            ,'False' as {{ columns.dbt_is_deleted }}
          {%- endif %}

        from insertions_source_data as source_data
        left outer join snapshotted_data
            on {{ unique_key_join_on(strategy.unique_key, "snapshotted_data", "source_data") }}
            where {{ unique_key_is_null(strategy.unique_key, "snapshotted_data") }}
            or ({{ unique_key_is_not_null(strategy.unique_key, "snapshotted_data") }} and (
               {{ strategy.row_changed }} {%- if strategy.hard_deletes == 'new_record' -%} or snapshotted_data.{{ columns.dbt_is_deleted }} = 'True' {% endif %}
            )

        )

    ),

    updates as (

        select
            'update' as dbt_change_type,
            {%- if surrogate_key %}
            snapshotted_data.{{ surrogate_key }},
            {%- endif %}
            {#- merge_on_valid_from: take dbt_valid_from from the target row. #}
            source_data.*,
            snapshotted_data.{{ columns.dbt_valid_from }} as {{ columns.dbt_valid_from }},
            source_data.{{ columns.dbt_updated_at }} as {{ columns.dbt_valid_to }},
            snapshotted_data.{{ columns.dbt_scd_id }}
          {%- if strategy.hard_deletes == 'new_record' -%}
            , snapshotted_data.{{ columns.dbt_is_deleted }}
          {%- endif %}

        from updates_source_data as source_data
        join snapshotted_data
            on {{ unique_key_join_on(strategy.unique_key, "snapshotted_data", "source_data") }}
        where (
            {{ strategy.row_changed }}  {%- if strategy.hard_deletes == 'new_record' -%} or snapshotted_data.{{ columns.dbt_is_deleted }} = 'True' {% endif %}
        )
    )

    {%- if strategy.hard_deletes == 'invalidate' or strategy.hard_deletes == 'new_record' %}
    ,
    deletes as (

        select
            'delete' as dbt_change_type,
            {%- if surrogate_key %}
            snapshotted_data.{{ surrogate_key }},
            {%- endif %}
            source_data.*,
            {#- merge_on_valid_from: take dbt_valid_from from the target row. #}
            {{ snapshot_get_time() }} as {{ columns.dbt_updated_at }},
            snapshotted_data.{{ columns.dbt_valid_from }} as {{ columns.dbt_valid_from }},
            {{ snapshot_get_time() }} as {{ columns.dbt_valid_to }},
            snapshotted_data.{{ columns.dbt_scd_id }}
          {%- if strategy.hard_deletes == 'new_record' -%}
            , snapshotted_data.{{ columns.dbt_is_deleted }}
          {%- endif %}
        from snapshotted_data
        left join deletes_source_data as source_data
            on {{ unique_key_join_on(strategy.unique_key, "snapshotted_data", "source_data") }}
            where {{ unique_key_is_null(strategy.unique_key, "source_data") }}

            {%- if strategy.hard_deletes == 'new_record' %}
            and not (
                --avoid updating the record's valid_to if the latest entry is marked as deleted
                snapshotted_data.{{ columns.dbt_is_deleted }} = 'True'
                and
                {% if config.get('dbt_valid_to_current') -%}
                    snapshotted_data.{{ columns.dbt_valid_to }} = {{ config.get('dbt_valid_to_current') }}
                {%- else -%}
                    snapshotted_data.{{ columns.dbt_valid_to }} is null
                {%- endif %}
            )
            {%- endif %}
    )
    {%- endif %}

    {%- if strategy.hard_deletes == 'new_record' %}
        {% set snapshotted_cols = get_list_of_column_names(get_columns_in_relation(target_relation)) %}
        {% set source_col_names = get_columns_in_query(source_sql) %}
    ,

    deletion_records as (

        select
            'insert' as dbt_change_type,
            {%- if surrogate_key %}
            {{ surrogate_key_seq }},
            {%- endif %}
            {%- for col_name in source_col_names -%}
            {%- if col_name in snapshotted_cols -%}
            snapshotted_data.{{ adapter.quote(col_name) }},
            {%- else -%}
            source_data.{{ adapter.quote(col_name) }},
            {%- endif -%}
            {% endfor -%}
            {%- if strategy.unique_key | is_list -%}
                {%- for key in strategy.unique_key -%}
            snapshotted_data.{{ key }} as dbt_unique_key_{{ loop.index }},
                {% endfor -%}
            {%- else -%}
            snapshotted_data.dbt_unique_key as dbt_unique_key,
            {% endif -%}
            {{ snapshot_get_time() }} as {{ columns.dbt_valid_from }},
            {{ snapshot_get_time() }} as {{ columns.dbt_updated_at }},
            snapshotted_data.{{ columns.dbt_valid_to }} as {{ columns.dbt_valid_to }},
            {{ new_scd_id }} as {{ columns.dbt_scd_id }},
            'True' as {{ columns.dbt_is_deleted }}
        from snapshotted_data
        left join deletes_source_data as source_data
            on {{ unique_key_join_on(strategy.unique_key, "snapshotted_data", "source_data") }}
        where {{ unique_key_is_null(strategy.unique_key, "source_data") }}
        and not (
            --avoid inserting a new record if the latest one is marked as deleted
            snapshotted_data.{{ columns.dbt_is_deleted }} = 'True'
            and
            {% if config.get('dbt_valid_to_current') -%}
                snapshotted_data.{{ columns.dbt_valid_to }} = {{ config.get('dbt_valid_to_current') }}
            {%- else -%}
                snapshotted_data.{{ columns.dbt_valid_to }} is null
            {%- endif %}
            )

    )
    {%- endif %}

    select * from insertions
    union all
    select * from updates
    {%- if strategy.hard_deletes == 'invalidate' or strategy.hard_deletes == 'new_record' %}
    union all
    select * from deletes
    {%- endif %}
    {%- if strategy.hard_deletes == 'new_record' %}
    union all
    select * from deletion_records
    {%- endif %}

{%- endmacro %}

{#- surrogate_key: only the optional key column differs from upstream. #}
{% macro default__build_snapshot_table(strategy, sql) %}
    {% set columns = config.get('snapshot_table_column_names') or get_snapshot_table_column_names() %}
    {% set surrogate_key = snapshot_surrogate_key() %}

    select
        {%- if surrogate_key %}
        {{ sequence_nextval_as_surrogate_key(surrogate_key) }},
        {%- endif %}
        *,
        {{ strategy.scd_id }} as {{ columns.dbt_scd_id }},
        {{ strategy.updated_at }} as {{ columns.dbt_updated_at }},
        {{ strategy.updated_at }} as {{ columns.dbt_valid_from }},
        {{ get_dbt_valid_to_current(strategy, columns) }}
      {%- if strategy.hard_deletes == 'new_record' -%}
        , 'False' as {{ columns.dbt_is_deleted }}
      {% endif -%}
    from (
        {{ sql }}
    ) sbq

{% endmacro %}

{#- merge_on_valid_from and surrogate_key: only the ON clause differs from upstream. #}
{% macro default__snapshot_merge_sql(target, source, insert_cols) -%}
    {%- set insert_cols_csv = insert_cols | join(', ') -%}

    {%- set columns = config.get("snapshot_table_column_names") or get_snapshot_table_column_names() -%}
    {%- set surrogate_key = snapshot_surrogate_key() -%}

    merge into {{ target.render() }} as DBT_INTERNAL_DEST
    using {{ source }} as DBT_INTERNAL_SOURCE
    on DBT_INTERNAL_SOURCE.{{ columns.dbt_scd_id }} = DBT_INTERNAL_DEST.{{ columns.dbt_scd_id }}
        {#- merge_on_valid_from: null-safe match. Snowflake still prunes on "is not distinct from". #}
        and DBT_INTERNAL_SOURCE.{{ columns.dbt_valid_from }} is not distinct from DBT_INTERNAL_DEST.{{ columns.dbt_valid_from }}
        {%- if surrogate_key %}
        {#- surrogate_key: null-safe match, so rows from before the key existed still close. #}
        and DBT_INTERNAL_SOURCE.{{ surrogate_key }} is not distinct from DBT_INTERNAL_DEST.{{ surrogate_key }}
        {%- endif %}

    when matched
     {% if config.get("dbt_valid_to_current") %}
        {% set source_unique_key = ("DBT_INTERNAL_DEST." ~ columns.dbt_valid_to) | trim %}
        {% set target_unique_key = config.get('dbt_valid_to_current') | trim %}
        and ({{ equals(source_unique_key, target_unique_key) }} or {{ source_unique_key }} is null)
     {% else %}
       and DBT_INTERNAL_DEST.{{ columns.dbt_valid_to }} is null
     {% endif %}
     and DBT_INTERNAL_SOURCE.dbt_change_type in ('update', 'delete')
        then update
        set {{ columns.dbt_valid_to }} = DBT_INTERNAL_SOURCE.{{ columns.dbt_valid_to }}

    when not matched
     and DBT_INTERNAL_SOURCE.dbt_change_type = 'insert'
        then insert ({{ insert_cols_csv }})
        values ({{ insert_cols_csv }})

{%- endmacro %}
