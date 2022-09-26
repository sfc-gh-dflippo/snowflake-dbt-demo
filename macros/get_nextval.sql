{%- macro get_nextval(sequence_name, schema_name=this.schema, database_name=this.database) -%}
    {{ return(adapter.dispatch('get_nextval')(sequence_name)) }}
{%- endmacro -%}

{%- macro snowflake__get_nextval(sequence_name, schema_name=this.schema, database_name=this.database) -%}
    {%- set sequence = api.Relation.create(
            database = database_name,
            schema = schema_name,
            identifier = sequence_name -%}

    {% if execute %}

        {# create sequence if not exists #}
        {%- set sequence_create_statement -%}
        create sequence if not exists {{sequence}}
        {%- endset -%}
        {%- do log("Creating sequence: " ~ sequence, info=false) -%}
        {%- do run_query(sequence_create_statement) -%}

    {%- endif -%}

    {{ return(sequence ~ ".nextval") }}

{%- endmacro -%}
