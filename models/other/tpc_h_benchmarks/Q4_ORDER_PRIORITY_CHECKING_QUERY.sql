/*
    dbt Feature Demonstration: TPC-H BENCHMARK QUERY Q4

    This model demonstrates:
    - ✅ Official TPC-H Query 4 (Order Priority Checking)
    - ✅ EXISTS subqueries for complex filtering
    - ✅ Advanced Jinja templating with random intervals
    - ✅ Date range filtering and comparisons
    - ✅ Performance benchmarking patterns
    - ⚠️  INTENTIONAL direct source usage (TPC-H standard requires raw data)
    - ✅ GROUP BY with aggregations

    Complexity: 🥇 RUN (Advanced)
    Layer: Bronze - Performance Benchmarking

    NOTE: This query intentionally uses source() directly to match official TPC-H
    specifications for accurate performance benchmarking.

    The Order Priority Checking Query counts the number of orders ordered in a given quarter of a given year in which
    at least one lineitem was received by the customer later than its committed date. The query lists the count of such
    orders for each order priority sorted in ascending priority order.
*/
{% set random_interval = range(0,106) | list | random %}

select
    orders.o_orderpriority,
    count(*) as order_count
from {{ source('TPC_H', 'ORDERS') }} as orders
where orders.o_orderdate >= date '1993-01-01' + interval '{{ random_interval }} months'
    and orders.o_orderdate < date '1993-01-01' + interval '{{ random_interval }} months' + interval '3 months'
    and exists (
        select null
        from {{ source('TPC_H', 'LINEITEM') }} as lineitem
        where lineitem.l_orderkey = orders.o_orderkey
            and lineitem.l_commitdate < lineitem.l_receiptdate
    )
group by orders.o_orderpriority
order by orders.o_orderpriority
