-- MAC011: macro defined inside models directory
{% macro my_inline_helper() %}
    current_timestamp()
{% endmacro %}

select {{ my_inline_helper() }} as load_ts
from {{ ref('stg_customers') }}
