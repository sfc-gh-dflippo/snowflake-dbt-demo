{% set result_a = chain_top('x') %}
{% set result_b = chain_mid('y') %}
{% set result_c = chain_bot('z') %}
{% set result_d = trivial_fmt('w') %}
select
    {{ get_audit_columns() }},
    {{ chain_top('x') }}
from {{ ref('stg_orders') }}
