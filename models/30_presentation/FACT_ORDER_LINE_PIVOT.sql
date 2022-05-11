{% set shipping_years = dbt_utils.get_column_values(table=ref('FACT_ORDER_LINE'), column="extract('year', l_shipdate)") %}

with fol as (
    select
        L_SUPPKEY,
        L_PARTKEY,
        extract('year', l_shipdate) AS SHIP_YEAR,
        L_QUANTITY
    from {{ ref('FACT_ORDER_LINE') }}
)
select *
from FOL
    pivot(
        sum(L_QUANTITY) for SHIP_YEAR in (
            {{ "'" ~ shipping_years | join("', '") ~ "'" }}
        )
    ) as p (
        L_SUPPKEY, L_PARTKEY,
        {{ "shipped_" ~ shipping_years | join(', shipped_') }}
    )
