{%- macro sequence_get_nextval(sequence_name=( (this.alias or this.name) ~ '_SEQ' )) -%}
    {%- set sequence = api.Relation.create(
            database = this.database,
            schema = this.schema,
            identifier = sequence_name) -%}

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

{%- macro recreate_sequence_get_nextval(sequence_name=( (this.alias or this.name) ~ '_SEQ' )) -%}
    {%- set sequence = api.Relation.create(
            database = this.database,
            schema = this.schema,
            identifier = sequence_name) -%}

    {% if execute %}

        {# create sequence if not exists #}
        {%- set sequence_create_statement -%}
        create or replace sequence {{sequence}}
        {%- endset -%}
        {%- do log("Creating sequence: " ~ sequence, info=true) -%}
        {%- do run_query(sequence_create_statement) -%}

    {%- endif -%}

    {{ return(sequence ~ ".nextval") }}

{%- endmacro -%}
