{%- macro get_stream(table, stream_name=( (this.alias or this.name) ~ '_ST' )) -%}
    {%- set stream = api.Relation.create(
            database=this.database,
            schema=this.schema,
            identifier=stream_name ) -%}

    {% if execute %}
        {%- set stream_lookup_query -%}
        show streams like '{{stream.identifier}}' in schema {{stream.database}}.{{stream.schema}}
        {%- endset -%}
        {%- set stream_list = run_query(stream_lookup_query) -%}

        {%- if stream_list
            and 'false' in stream_list.columns["stale"].values() -%}

            {# Stream exists and is not stale #}

        {%- else -%}

            {# Stream should be recreated #}
            {%- set stream_create_statement -%}
            create or replace stream {{stream}} on table {{table}} show_initial_rows = true
            {%- endset -%}
            {%- do log("Creating stream: " ~ stream, info=true) -%}
            {%- do run_query(stream_create_statement) -%}

        {%- endif -%}
    {%- endif -%}

    {{ return(stream) }}

{%- endmacro -%}

{%- macro get_new_stream(table, stream_name=( (this.alias or this.name) ~ '_ST' )) -%}
    {%- set stream = api.Relation.create(
            database=this.database,
            schema=this.schema,
            identifier=stream_name ) -%}

    {% if execute %}

        {# Stream should be recreated #}
        {%- set stream_create_statement -%}
        create or replace stream {{stream}} on table {{table}} show_initial_rows = true
        {%- endset -%}
        {%- do log("Creating stream: " ~ stream, info=true) -%}
        {%- do run_query(stream_create_statement) -%}

    {%- endif -%}

    {{ return(stream) }}

{%- endmacro -%}
