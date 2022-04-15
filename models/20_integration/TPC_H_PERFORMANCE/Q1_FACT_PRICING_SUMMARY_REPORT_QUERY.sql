/*
 The Pricing Summary Report Query provides a summary pricing report for all lineitems shipped as of a given date.
 The date is within 60 - 120 days of the greatest ship date contained in the database. The query lists totals for
 extended price, discounted extended price, discounted extended price plus tax, average quantity, average extended
 price, and average discount. These aggregates are grouped by RETURNFLAG and LINESTATUS, and listed in
 ascending order of RETURNFLAG and LINESTATUS. A count of the number of lineitems in each group is
 included.
 */
 {% set random_interval = range(60,120) | random %}
select l_returnflag,
    l_linestatus,
    sum(l_quantity) as sum_qty,
    sum(l_extendedprice) as sum_base_price,
    sum(l_extendedprice *(1 - l_discount)) as sum_disc_price,
    sum(l_extendedprice *(1 - l_discount) *(1 + l_tax)) as sum_charge,
    avg(l_quantity) as avg_qty,
    avg(l_extendedprice) as avg_price,
    avg(l_discount) as avg_disc,
    count(*) as count_order
from {{ source('TPC_H', 'LINEITEM') }}
where l_shipdate <= date '1998-12-01' - interval '{{random_interval}} DAYS'
group by l_returnflag,
    l_linestatus
order by l_returnflag,
    l_linestatus
