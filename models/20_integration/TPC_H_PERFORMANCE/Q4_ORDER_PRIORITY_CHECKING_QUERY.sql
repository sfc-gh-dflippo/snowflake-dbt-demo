/*
 The Order Priority Checking Query counts the number of orders ordered in a given quarter of a given year in which
 at least one lineitem was received by the customer later than its committed date. The query lists the count of such
 orders for each order priority sorted in ascending priority order.
 */
 {% set random_interval = range(0,106) | random %}
select o_orderpriority,
    count(*) as order_count
from {{ source('TPC_H', 'ORDERS') }}
where o_orderdate >= date '1993-01-01' + interval '{{random_interval}} months'
    and o_orderdate < date '1993-01-01' + interval '{{random_interval}} months' + interval '3 months'
    and exists (
        select *
        from {{ source('TPC_H', 'LINEITEM') }}
        where l_orderkey = o_orderkey
            and l_commitdate < l_receiptdate
    )
group by o_orderpriority
order by o_orderpriority
