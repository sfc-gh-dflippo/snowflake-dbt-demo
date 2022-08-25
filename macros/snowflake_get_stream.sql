{%- macro snowflake_get_stream(table) -%}
    {%- set stream = adapter.get_relation(
            database=table.database,
            schema=table.schema,
            identifier= (table.name ~ '_ST') ) -%}

    {%- set stream_lookup_query -%}
    show streams like '{{stream.identifier}}' in schema {{stream.database}}.{{stream.schema}}
    {%- endset -%}

    {%- set stream_create_statement -%}
    create or replace stream {{stream}} on table {{table}} show_initial_rows = true
    {%- endset -%}

    {%- set stream_list = run_query(stream_lookup_query) -%}
    {%- if 'FALSE' in stream_list.columns["stale"].values() -%}

        {# Stream exists and is not stale #}
        {{ return(stream) }}

    {%- else -%}

        {# Stream should be recreated #}
        {%- do run_query(stream_create_statement) -%}
        {{ return(stream) }}

    {%- endif -%}
{%- endmacro -%}
