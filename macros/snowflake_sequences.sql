{# Simple macro to create a sequence if it does not exist #}
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


{# Provided the name of the column to store the values in, this macro will ensure that your sequence exists and is above the high watermark. #}
{%- macro sequence_nextval_as_surrogate_key(column_name, sequence_name=( (this.alias or this.name) ~ "_SEQ") ) -%}
    {%- set sequence = api.Relation.create(
            database = this.database,
            schema = this.schema,
            identifier = sequence_name) -%}
    {% if execute %}

        {% set start_with_val = 1 %}

        {% if is_incremental()  %}

            {# This query does not require compute and will respond immediately from cloud services #}
            {%- set high_watermark_statement -%}
            select max({{ column_name }}) as "high_watermark" from {{ this }}
            {%- endset -%}
            {%- set high_watermark_result = run_query(high_watermark_statement) -%}
            {%- set high_watermark = high_watermark_result.columns["high_watermark"].values() | first -%}

            {%- if high_watermark > 0 -%}
                {%- set start_with_val = high_watermark + 1 -%}
            {%- endif -%}

        {%- endif -%}

        {%- do log("Create or replace the " ~ sequence ~ " sequence above the high watermark", info=false) -%}
        {%- set sequence_create_statement -%}
        create or replace sequence {{ sequence }} start with {{ start_with_val }}
        {%- endset -%}
        {%- do run_query(sequence_create_statement) -%}

    {%- endif -%}

    {{ return( sequence ~ ".nextval as " ~ column_name ) }}

{%- endmacro -%}
