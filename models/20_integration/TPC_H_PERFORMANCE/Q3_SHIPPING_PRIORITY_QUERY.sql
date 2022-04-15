/*
The Shipping Priority Query retrieves the shipping priority and potential revenue, defined as the sum of
l_extendedprice * (1-l_discount), of the orders having the largest revenue among those that had not been shipped as
of a given date. Orders are listed in decreasing order of revenue. If more than 10 unshipped orders exist, only the 10
orders with the largest revenue are listed.
 */
 {% set random_segment = dbt_utils.get_column_values(table=source('TPC_H', 'CUSTOMER'),column='c_mktsegment') | random %}
 {% set random_interval = range(0,30) | random %}
select l_orderkey,
    sum(l_extendedprice *(1 - l_discount)) as revenue,
    o_orderdate,
    o_shippriority
from {{ source('TPC_H', 'CUSTOMER') }},
    {{ source('TPC_H', 'ORDERS') }},
    {{ source('TPC_H', 'LINEITEM') }}
where c_mktsegment = '{{random_segment}}'
    and c_custkey = o_custkey
    and l_orderkey = o_orderkey
    and o_orderdate < date '1995-03-01' + interval '{{random_interval}} DAYS'
    and l_shipdate > date '1995-03-01' + interval '{{random_interval}} DAYS'
group by l_orderkey,
    o_orderdate,
    o_shippriority
order by revenue desc,
    o_orderdate
LIMIT 10
