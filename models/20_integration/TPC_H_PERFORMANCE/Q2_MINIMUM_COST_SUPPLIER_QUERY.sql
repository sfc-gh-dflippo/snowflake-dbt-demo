/*
 The Minimum Cost Supplier Query finds, in a given region, for each part of a certain type and size, the supplier who
 can supply it at minimum cost. If several suppliers in that region offer the desired part type and size at the same
 (minimum) cost, the query lists the parts from suppliers with the 100 highest account balances. For each supplier,
 the query lists the supplier's account balance, name and nation; the part's number and manufacturer; the supplier's
 address, phone number and comment information.
 */
 {% set random_size = range(1, 50) | list | random %}
select s_acctbal,
    s_name,
    n_name,
    p_partkey,
    p_mfgr,
    s_address,
    s_phone,
    s_comment
from {{ source('TPC_H', 'PART') }} AS RANDOM_PART SAMPLE ROW (1 ROWS),
    {{ source('TPC_H', 'SUPPLIER') }},
    {{ source('TPC_H', 'PARTSUPP') }},
    {{ source('TPC_H', 'NATION') }},
    {{ source('TPC_H', 'REGION') }} AS RANDOM_REGION SAMPLE ROW (1 ROWS)
where p_partkey = ps_partkey
    and s_suppkey = ps_suppkey
    and p_size = {{random_size}}
    and s_nationkey = n_nationkey
    and n_regionkey = r_regionkey
    and ps_supplycost = (
        select min(ps_supplycost)
        from {{ source('TPC_H', 'PARTSUPP') }},
            {{ source('TPC_H', 'SUPPLIER') }},
            {{ source('TPC_H', 'NATION') }},
            {{ source('TPC_H', 'REGION') }} R
        where p_partkey = ps_partkey
            and s_suppkey = ps_suppkey
            and s_nationkey = n_nationkey
            and n_regionkey = r_regionkey
            and R.r_name = RANDOM_REGION.r_name
    )
order by s_acctbal desc,
    n_name,
    s_name,
    p_partkey
LIMIT 100
