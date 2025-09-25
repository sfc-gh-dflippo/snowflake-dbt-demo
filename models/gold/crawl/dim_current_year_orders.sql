/*
    Simulate a query for the last year of sales orders
*/

{{ config(
    materialized = 'dynamic_table',
    target_lag = 'DOWNSTREAM',
    alias='DIM_CURRENT_YEAR_ORDERS'
) }}

select *
from {{ ref('dim_orders') }}

-- This filter will limit rows to the last year of orders in the table
where order_date >= (
        select dateadd(year, -1, date_trunc('DAY', max(order_date)))
        from {{ ref('dim_orders') }}
    )

order by order_key
