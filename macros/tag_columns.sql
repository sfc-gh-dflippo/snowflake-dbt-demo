{# This is a simple post-hook macro that can be added to tag columns on tables and views #}
{% macro get_tag_cache(tag_database='COMMON_UTILITY', tag_schema='SECURITY') -%}
    {% if execute %}

        {%- set current_tag_objects = api.Relation.create(
            database = tag_database,
            schema = tag_schema,
            identifier = 'CURRENT_TAG_OBJECTS') -%}

        {%- set current_tag_columns = api.Relation.create(
            database = tag_database,
            schema = tag_schema,
            identifier = 'CURRENT_TAG_COLUMNS') -%}

        {%- set lookup_object_tags -%}
            SELECT * FROM {{ current_tag_objects }}
        {%- endset -%}

        {%- set lookup_column_tags -%}
            SELECT * FROM {{ current_tag_columns }}
        {%- endset -%}

        {%- set tag_object_statements = run_query(lookup_object_tags) -%}
        {%- set tag_column_statements = run_query(lookup_column_tags) -%}
        {%- do return({tag_object_statements: tag_object_statements, tag_column_statements: tag_column_statements}) -%}

    {%- else -%}

        {%- do return({tag_object_statements: none, tag_column_statements: none}) -%}

    {%- endif -%}
{%- endmacro %}

{# This is a post-hook macro that can be added to tag columns on tables and views #}
{% macro tag_columns(tag_cache = var('tag_cache', None)) -%}
    {% if execute and model %}

        {%- if tag_cache
            and tag_cache.tag_column_statements
            and tag_cache.tag_column_statements.rows -%}

            {%- for row in column_tags_to_apply.rows
                if row['OBJECT_DATABASE'] == model.database
                    and row['OBJECT_SCHEMA'] == model.schema
                    and row['OBJECT_NAME'] == model.name -%}

                {%- do run_query(row['STMT']) -%}
            {%- endfor -%}

        {%- endif -%}

        {%- if tag_cache
            and tag_cache.tag_object_statements
            and tag_cache.tag_object_statements.rows -%}

            {%- for stmt in object_tags_to_apply.rows
                if row['OBJECT_DATABASE'] == model.database
                    and row['OBJECT_SCHEMA'] == model.schema
                    and row['OBJECT_NAME'] == model.name -%}

                {%- do run_query(row['STMT']) -%}
            {%- endfor -%}

        {%- endif -%}

    {%- endif -%}
{%- endmacro %}
