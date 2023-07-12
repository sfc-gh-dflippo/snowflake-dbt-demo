{%- macro sequence_get_nextval(sequence_name=( (this.alias or this.name) ~ "_SEQ") ) -%}
    {%- set sequence = api.Relation.create(
            database = this.database,
            schema = this.schema,
            identifier = sequence_name) -%}

    {% if execute %}

            {%- set sequence_create_statement -%}
            create sequence if not exists {{sequence}}
            {%- endset -%}
            {%- do log(sequence_create_statement, info=false) -%}
            {%- do run_query(sequence_create_statement) -%}

    {%- endif -%}

    {{ return(sequence ~ ".nextval") }}

{%- endmacro -%}
