{#-
    Materialization is inherited from dbt_project.yml: models/gold/run/ sets
    +materialized: incremental (NOT table).

    unique_key is the grain of the pivot output, so reprocessing restates a
    supplier/part row rather than appending a second copy of it.

    on_schema_change is required here: the pivot column list is generated at parse
    time from the ship years present in the source, so it grows over time, and a
    merge against a changed column set fails without it.
-#}

{{ config(
    alias='FACT_ORDER_LINE_PIVOT',
    unique_key=['supplier_key', 'part_key'],
    on_schema_change='sync_all_columns'
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
