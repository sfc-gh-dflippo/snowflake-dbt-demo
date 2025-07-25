/*
The Shipping Priority Query retrieves the shipping priority and potential revenue, defined as the sum of
l_extendedprice * (1-l_discount), of the orders having the largest revenue among those that had not been shipped as
of a given date. Orders are listed in decreasing order of revenue. If more than 10 unshipped orders exist, only the 10
orders with the largest revenue are listed.
 */

{% set random_interval = range(0,30) | list | random %}
with random_segment as (
    -- Randomly select a market segment from the CUSTOMER table
    select c_mktsegment as random_segment from {{ source('TPC_H', 'CUSTOMER') }} SAMPLE ROW (1 ROWS)
)
select
    lineitem.l_orderkey,
    sum(lineitem.l_extendedprice * (1 - lineitem.l_discount)) as revenue,
    orders.o_orderdate,
    orders.o_shippriority
from {{ source('TPC_H', 'CUSTOMER') }} as customer,
    {{ source('TPC_H', 'ORDERS') }} as orders,
    {{ source('TPC_H', 'LINEITEM') }} as lineitem,
    random_segment
where customer.c_mktsegment = random_segment.random_segment
    and customer.c_custkey = orders.o_custkey
    and lineitem.l_orderkey = orders.o_orderkey
    and orders.o_orderdate < date '1995-03-01' + interval '{{ random_interval }} DAYS'
    and lineitem.l_shipdate > date '1995-03-01' + interval '{{ random_interval }} DAYS'
group by
    lineitem.l_orderkey,
    orders.o_orderdate,
    orders.o_shippriority
order by
    revenue desc,
    orders.o_orderdate
limit 10
