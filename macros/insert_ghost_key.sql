{#-
    Builds the SQL that inserts one "ghost" row (unknown member) into a table.
    The row is added only when key_column_name has no row with that value.

    relation:                the table to insert into, as text or a Relation
    key_column_name:         the key column
    key_column_value:        a SQL literal for the key, for example 0
    additional_column_dict:  optional dict of column name to SQL literal.
                             Pass {} or none to set only the key column.
-#}
{%- macro insert_ghost_key_sql(relation, key_column_name, key_column_value, additional_column_dict = {}) -%}

    {%- set full_column_name_array = [key_column_name] -%}
    {%- set full_column_value_array = [key_column_value] -%}

    {%- if additional_column_dict -%}
        {%- for column_name, column_value in additional_column_dict.items() -%}
            {%- do full_column_name_array.append(column_name) -%}
            {%- do full_column_value_array.append(column_value) -%}
        {%- endfor -%}
    {%- endif -%}

    {%- set full_column_name_list = full_column_name_array | join(', ') -%}
    {%- set full_column_value_list = full_column_value_array | join(', ') -%}

    insert into {{ relation }} ( {{ full_column_name_list }} )
    select {{ full_column_value_list }}
    from ( select {{ key_column_value }} as ghost_val ) as ghost_row
    left outer join {{ relation }} t on
        {{ key_column_name }} = ghost_row.ghost_val
    where {{ key_column_name }} is null
    limit 1

{%- endmacro -%}


{#- Post-hook wrapper. See insert_ghost_key_sql for the arguments. -#}
{%- macro insert_ghost_key(key_column_name, key_column_value, additional_column_dict = {} ) -%}
    {%- do run_query(insert_ghost_key_sql(this, key_column_name, key_column_value, additional_column_dict)) -%}
    {{ return("") }}
{%- endmacro -%}
