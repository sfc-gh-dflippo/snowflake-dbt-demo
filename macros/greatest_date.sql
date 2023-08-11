{%- macro greatest_timestamp(field_list) -%}
{%- set fields = [] -%}
{%- for field in field_list -%}
    {%- set _ = fields.append(
        "coalesce(" ~ field ~ ", '1900-01-01'::timestamp)"
    ) -%}
{%- endfor -%}

greatest ( {{ fields|join(", ") }} )

{%- endmacro -%}


{%- macro greatest_date(field_list) -%}
{%- set fields = [] -%}
{%- for field in field_list -%}
    {%- set _ = fields.append(
        "coalesce(" ~ field ~ ", '1900-01-01'::date)"
    ) -%}
{%- endfor -%}

greatest ( {{ fields|join(", ") }} )

{%- endmacro -%}
