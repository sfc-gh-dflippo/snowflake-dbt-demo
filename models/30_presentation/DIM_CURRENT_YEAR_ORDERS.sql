/*
    Simulate a query for the last year of sales orders
*/

{{ config(
    materialized = 'dynamic_table',
    target_lag = 'DOWNSTREAM'
) }}

select *
from {{ ref('DIM_ORDERS') }}

-- This filter will limit rows to the last year of orders in the table
where o_orderdate >= (
        select dateadd(year, -1, date_trunc('DAY', max(o_orderdate)))
        from {{ ref('DIM_ORDERS') }}
    )

order by o_orderkey
