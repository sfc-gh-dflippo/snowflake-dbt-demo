{{ config(
    alias='FACT_ORDER_LINE_PIVOT'
) }}

{%- set shipping_years = dbt_utils.get_column_values(table=ref('fct_order_lines'), column="extract('year', ship_date)") -%}

with fol as (
    select
        supplier_key,
        part_key,
        extract('year', ship_date) as ship_year,
        quantity
    from {{ ref('fct_order_lines') }}
)

select
    *,
    sysdate() as dbt_last_update_ts
from fol
pivot (
    sum(quantity) for ship_year in (
        {{ "'" ~ shipping_years | sort | join("', '") ~ "'" }}
    )
) as p (
    supplier_key, part_key,
    {{ "shipped_" ~ shipping_years | sort | join(', shipped_') }}
)
