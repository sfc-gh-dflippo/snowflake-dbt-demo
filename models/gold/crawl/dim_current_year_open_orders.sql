{{ config(
    alias='DIM_CURRENT_YEAR_OPEN_ORDERS'
) }}

/*
    Use the `ref` function to select from other models
    Because we aren't overriding the materialization, it will be a view by default
*/
select *
from {{ ref('dim_current_year_orders') }}
where order_status = 'O'
