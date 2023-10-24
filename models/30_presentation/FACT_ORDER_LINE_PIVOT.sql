{%- set shipping_years = dbt_utils.get_column_values(table=ref('FACT_ORDER_LINE'), column="extract('year', l_shipdate)") -%}

with fol as (
    select
        l_suppkey,
        l_partkey,
        extract('year', l_shipdate) as ship_year,
        l_quantity
    from {{ ref('FACT_ORDER_LINE') }}
)

select
    *,
    sysdate() as dbt_last_update_ts
from fol
pivot (
    sum(l_quantity) for ship_year in (
        {{ "'" ~ shipping_years | sort | join("', '") ~ "'" }}
    )
) as p (
    l_suppkey, l_partkey,
    {{ "shipped_" ~ shipping_years | sort | join(', shipped_') }}
)
