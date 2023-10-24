{{ config(materialized = 'ephemeral') }}
/*
 List of customers and how many orders they have
 */
select
    orders.o_custkey,
    count(*) as order_count,
    sum(
        case
            when orders.o_orderstatus = 'O' then 1
            else 0
        end
    ) as open_order_count
from {{ source('TPC_H', 'ORDERS') }} orders
group by 1
