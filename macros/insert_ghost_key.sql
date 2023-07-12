{%- macro insert_ghost_key(key_column_name, key_column_value, additional_column_dict = {} ) -%}

    {%- set full_column_name_array = [key_column_name] -%}
    {%- set full_column_value_array = [key_column_value] -%}

    {% if additional_column_dict %}
        {%- for column_name, column_value in additional_column_dict.items() -%}
            {{ full_column_name_array.append(column_name) }}
            {{ full_column_value_array.append(column_value) }}
        {%- endfor -%}
    {%- endif -%}

    {%- set full_column_name_list = full_column_name_array | join(', ') -%}
    {%- set full_column_value_list = full_column_value_array | join(', ') -%}

    {%- set insert_statement -%}

    insert into {{this}} ( {{ full_column_name_list }} )
    select {{ full_column_value_list }}
    from ( select {{key_column_value}} as ghost_val ) as ghost_row
    left outer join {{this}} t on
        {{key_column_name}} = ghost_row.ghost_val
    where {{key_column_name}} is null
    limit 1

    {%- endset -%}
    {%- do run_query(insert_statement) -%}
    {{ return("") }}

{%- endmacro -%}
