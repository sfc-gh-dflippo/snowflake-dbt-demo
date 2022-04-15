{%- macro surrogate_key(field_list) -%}

{%- set fields = [] -%}

{%- for field in field_list -%}

    {%- set _ = fields.append(
        "COALESCE(" ~ field ~ "::VARCHAR, '')"
    ) -%}

{%- endfor -%}

{{ fields|join(" || '~' || ") }}

{%- endmacro -%}
