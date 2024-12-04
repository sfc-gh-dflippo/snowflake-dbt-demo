{#
    This script replaces the out of the box materialization and adds the ability for users to
    customize the names of dbt columns, specify a sequence based surrogate key, and it improves the
    performance of merges into snapshots by including the dbt_valid_from in the merge. It will also
    use the surrogate key in the merge if it is available. It is compatible with the optimized
    snowflake__snapshot_hash_arguments macro but either macro can be deployed independently.
#}

{% macro get_snapshot_config() -%}
    {% set columns = config.get("snapshot_meta_column_names", {}) %}
    {% do return({
            "dbt_valid_from": columns.dbt_valid_from or config.get("dbt_valid_from_column", "dbt_valid_from"),
            "dbt_valid_to": columns.dbt_valid_to or config.get("dbt_valid_to_column", "dbt_valid_to"),
            "dbt_scd_id": columns.dbt_scd_id or config.get("dbt_scd_id_column", "dbt_scd_id"),
            "dbt_updated_at": columns.dbt_updated_at or config.get("dbt_updated_at_column", "dbt_updated_at"),
            "dbt_is_deleted": columns.dbt_is_deleted or config.get("dbt_is_deleted_column", "dbt_is_deleted")
        }) %}
{% endmacro %}


{% macro unique_key_fields(unique_key) %}
    {% if unique_key is not string %}
        {% for key in unique_key %}
            {{ key }} as dbt_unique_key_{{ loop.index }}
            {%- if not loop.last %} , {%- endif %}
        {% endfor %}
    {% else %}
        {{ unique_key }} as dbt_unique_key
    {% endif %}
{% endmacro %}


{% macro unique_key_join_on(unique_key, identifier, from_identifier) %}
    {% if unique_key is not string %}
        {% for key in unique_key %}
            {{ identifier }}.dbt_unique_key_{{ loop.index }} = {{ from_identifier }}.dbt_unique_key_{{ loop.index }}
            {%- if not loop.last %} and {%- endif %}
        {% endfor %}
    {% else %}
        {{ identifier }}.dbt_unique_key = {{ from_identifier }}.dbt_unique_key
    {% endif %}
{% endmacro %}

{% macro get_dbt_valid_to_current(strategy, columns) %}
  {% set dbt_valid_to_current = config.get('dbt_valid_to_current') or "null" %}
  coalesce(nullif({{ strategy.updated_at }}, {{ strategy.updated_at }}), {{dbt_valid_to_current}})
  as {{ columns.dbt_valid_to }}
{% endmacro %}

{% macro unique_key_is_null(unique_key, identifier) %}
    {% if unique_key is not string %}
        {{ identifier }}.dbt_unique_key_1 is null
    {% else %}
        {{ identifier }}.dbt_unique_key is null
    {% endif %}
{% endmacro %}

{% macro unique_key_is_not_null(unique_key, identifier) %}
    {% if unique_key is not string %}
        {{ identifier }}.dbt_unique_key_1 is not null
    {% else %}
        {{ identifier }}.dbt_unique_key is not null
    {% endif %}
{% endmacro %}

{% macro snapshot_get_sequence() -%}
    {% if config.get("surrogate_key") %}
        {% set sequence_relation = api.Relation.create(
            database = this.database,
            schema = this.schema,
            identifier = config.get("surrogate_key_sequence", this.identifier ~ "_SEQ") ) %}

        {% if execute %}
            {% set sequence_create_statement -%}
            create sequence if not exists {{sequence_relation}}
            {%- endset %}
            {% do run_query(sequence_create_statement) %}
        {% endif %}

        {% do return(sequence_relation) %}
    {% endif %}
{% endmacro %}


{% macro snowflake__snapshot_staging_table(strategy, source_sql, target_relation) -%}
    {%- set columns = (config.get("snapshot_table_column_names") or get_snapshot_table_column_names() or get_snapshot_config() ) -%}
    {%- set surrogate_key = config.get("surrogate_key") -%}
    {%- set surrogate_key_seq = snapshot_get_sequence() -%}
    {%- if strategy.invalidate_hard_deletes -%}
        {%- do strategy.update({'hard_deletes': 'invalidate' }) -%}
    {%- endif -%}

    with snapshot_query as (

        {{ source_sql }}

    ),

    snapshotted_data as (

        select *, {{ unique_key_fields(strategy.unique_key) }}
        from {{ target_relation }}
        where
            {% if config.get('dbt_valid_to_current') %}
               {# Check for either dbt_valid_to_current OR null, in order to correctly update records with nulls #}
               ( {{ columns.dbt_valid_to }} = {{ config.get('dbt_valid_to_current') }} or {{ columns.dbt_valid_to }} is null)
            {% else %}
                {{ columns.dbt_valid_to }} is null
            {% endif %}

    ),

    insertions_source_data as (

        select *, {{ unique_key_fields(strategy.unique_key) }},
            {{ strategy.updated_at }} as {{ columns.dbt_updated_at }},
            {{ strategy.updated_at }} as {{ columns.dbt_valid_from }},
            {{ get_dbt_valid_to_current(strategy, columns) }},

            {% if config.get("dbt_current_flag_column") -%}
                'Y' as {{ config.get("dbt_current_flag_column") }},
            {%- endif %}

            {{ strategy.scd_id }} as {{ columns.dbt_scd_id }}

        from snapshot_query
    ),

    updates_source_data as (

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

            {% if surrogate_key -%}
                -- Surrogate key from sequence
                {{ surrogate_key_seq }}.nextval as {{ surrogate_key }},
            {%- endif %}

            source_data.*
          {%- if strategy.hard_deletes == 'new_record' -%}
            ,'False' as {{ columns.dbt_is_deleted }}
          {%- endif %}

        from insertions_source_data as source_data
        left outer join snapshotted_data
            on {{ unique_key_join_on(strategy.unique_key, "snapshotted_data", "source_data") }}
            where {{ unique_key_is_null(strategy.unique_key, "snapshotted_data") }}
            or ({{ unique_key_is_not_null(strategy.unique_key, "snapshotted_data") }} and ({{ strategy.row_changed }})

        )

    ),

    updates as (

        select
            'update' as dbt_change_type,

            {% if surrogate_key -%}
                -- Surrogate key from target
                snapshotted_data.{{ surrogate_key }},
            {% endif %}

            source_data.*,
            snapshotted_data.{{ columns.dbt_valid_from }},
            {{ strategy.updated_at }} as {{ columns.dbt_valid_to }},

            {% if config.get("dbt_current_flag_column") -%}
                'N' as {{ config.get("dbt_current_flag_column") }},
            {%- endif %}

            snapshotted_data.{{ columns.dbt_scd_id }}
          {%- if strategy.hard_deletes == 'new_record' -%}
            , snapshotted_data.{{ columns.dbt_is_deleted }}
          {%- endif %}

        from updates_source_data as source_data
        join snapshotted_data
            on {{ unique_key_join_on(strategy.unique_key, "snapshotted_data", "source_data") }}
        where (
            {{ strategy.row_changed }}
        )
    )

    {%- if strategy.hard_deletes == 'invalidate' or strategy.hard_deletes == 'new_record' %}
    ,

    deletes as (

        select
            'delete' as dbt_change_type,

            {% if surrogate_key -%}
                -- Surrogate key from target
                snapshotted_data.{{ surrogate_key }},
            {%- endif %}

            source_data.*,
            {{ snapshot_get_time() }} as {{ columns.dbt_updated_at }},
            snapshotted_data.{{ columns.dbt_valid_from }},
            {{ snapshot_get_time() }} as {{ columns.dbt_valid_to }},

            {% if config.get("dbt_current_flag_column") -%}
                'N' as {{ config.get("dbt_current_flag_column") }},
            {%- endif %}

            snapshotted_data.{{ columns.dbt_scd_id }}
          {%- if strategy.hard_deletes == 'new_record' -%}
            , snapshotted_data.{{ columns.dbt_is_deleted }}
          {%- endif %}
        from snapshotted_data
        left join deletes_source_data as source_data
            on {{ unique_key_join_on(strategy.unique_key, "snapshotted_data", "source_data") }}
            where {{ unique_key_is_null(strategy.unique_key, "source_data") }}
    )
    {%- endif %}

    {%- if strategy.hard_deletes == 'new_record' %}
        {% set source_sql_cols = get_column_schema_from_query(source_sql) %}
    ,
    deletion_records as (

        select
            'insert' as dbt_change_type,

            {% if surrogate_key -%}
                -- Surrogate key from sequence
                {{ surrogate_key_seq }}.nextval as {{ surrogate_key }},
            {%- endif %}

            {%- for col in source_sql_cols -%}
            snapshotted_data.{{ adapter.quote(col.column) }},
            {% endfor -%}
            {%- if strategy.unique_key is not string -%}
                {%- for key in strategy.unique_key -%}
            snapshotted_data.{{ key }} as dbt_unique_key_{{ loop.index }},
                {% endfor -%}
            {%- else -%}
            snapshotted_data.dbt_unique_key as dbt_unique_key,
            {% endif -%}
            {{ snapshot_get_time() }} as {{ columns.dbt_valid_from }},
            {{ snapshot_get_time() }} as {{ columns.dbt_updated_at }},
            snapshotted_data.{{ columns.dbt_valid_to }} as {{ columns.dbt_valid_to }},
            snapshotted_data.{{ columns.dbt_scd_id }},
            'True' as {{ columns.dbt_is_deleted }}
        from snapshotted_data
        left join deletes_source_data as source_data
            on {{ unique_key_join_on(strategy.unique_key, "snapshotted_data", "source_data") }}
            where {{ unique_key_is_null(strategy.unique_key, "source_data") }}
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


{% macro snowflake__build_snapshot_table(strategy, sql) -%}
    {%- set columns = config.get("snapshot_table_column_names") or get_snapshot_table_column_names() or get_snapshot_config() -%}
    {%- set surrogate_key = config.get("surrogate_key") -%}
    {%- set surrogate_key_seq = snapshot_get_sequence() -%}

    select
        {% if surrogate_key -%}
            {{ surrogate_key_seq }}.nextval as {{ surrogate_key }},
        {%- endif %}
        *,
        {{ strategy.scd_id }} as {{ columns.dbt_scd_id }},
        {{ strategy.updated_at }} as {{ columns.dbt_updated_at }},
        {{ strategy.updated_at }} as {{ columns.dbt_valid_from }},
        {{ get_dbt_valid_to_current(strategy, columns) }}
        {%- if config.get("dbt_current_flag_column") -%},
        'Y' AS {{ config.get("dbt_current_flag_column") }}
        {%- endif %}
        {%- if strategy.hard_deletes == 'new_record' -%}
        , 'False' as {{ columns.dbt_is_deleted }}
        {% endif -%}
    from (
        {{ sql }}
    ) sbq

{% endmacro %}


{% macro snowflake__snapshot_merge_sql(target, source, insert_cols) -%}
    {%- set insert_cols_csv = insert_cols | join(', ') -%}

    {%- set columns = config.get("snapshot_table_column_names") or get_snapshot_table_column_names() or get_snapshot_config() -%}

    merge into {{ target.render() }} as DBT_INTERNAL_DEST
    using {{ source }} as DBT_INTERNAL_SOURCE
    on DBT_INTERNAL_SOURCE.{{ columns.dbt_scd_id }} = DBT_INTERNAL_DEST.{{ columns.dbt_scd_id }}

        -- Snowflake is likely to prune better on the dbt_valid_from column
        and DBT_INTERNAL_SOURCE.{{ columns.dbt_valid_from }} = DBT_INTERNAL_DEST.{{ columns.dbt_valid_from }}

        {% if config.get("surrogate_key") -%}
        -- Snowflake is also likely to prune well on a sequence-based surrogate key
        and DBT_INTERNAL_SOURCE.{{ config.get("surrogate_key") }} = DBT_INTERNAL_DEST.{{ config.get("surrogate_key") }}
        {%- endif %}

    when matched
     {% if config.get("dbt_valid_to_current") %}
       and (DBT_INTERNAL_DEST.{{ columns.dbt_valid_to }} = {{ config.get('dbt_valid_to_current') }} or
            DBT_INTERNAL_DEST.{{ columns.dbt_valid_to }} is null)
     {% else %}
       and DBT_INTERNAL_DEST.{{ columns.dbt_valid_to }} is null
     {% endif %}
     and DBT_INTERNAL_SOURCE.dbt_change_type in ('update', 'delete')
        then update
        set {{ columns.dbt_valid_to }} = DBT_INTERNAL_SOURCE.{{ columns.dbt_valid_to }}

        {%- if config.get("dbt_current_flag_column") -%},
            {{ config.get("dbt_current_flag_column") }} = DBT_INTERNAL_SOURCE.{{ config.get("dbt_current_flag_column") }}
        {%- endif %}

    when not matched
     and DBT_INTERNAL_SOURCE.dbt_change_type = 'insert'
        then insert ({{ insert_cols_csv }})
        values ({{ insert_cols_csv }})

{% endmacro %}
