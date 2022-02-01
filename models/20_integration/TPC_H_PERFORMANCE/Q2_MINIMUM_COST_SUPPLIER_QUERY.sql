/*
 The Minimum Cost Supplier Query finds, in a given region, for each part of a certain type and size, the supplier who
 can supply it at minimum cost. If several suppliers in that region offer the desired part type and size at the same
 (minimum) cost, the query lists the parts from suppliers with the 100 highest account balances. For each supplier,
 the query lists the supplier's account balance, name and nation; the part's number and manufacturer; the supplier's
 address, phone number and comment information.
 */
 {% set random_size = range(1, 50) | random  %}
 {% set random_type = dbt_utils.get_column_values(table=source('TPC_H', 'PART'),column='p_type') | random %}
 {% set random_region = dbt_utils.get_column_values(table=source('TPC_H', 'REGION'),column='r_name') | random %}
select s_acctbal,
    s_name,
    n_name,
    p_partkey,
    p_mfgr,
    s_address,
    s_phone,
    s_comment
from {{ source('TPC_H', 'PART') }},
    {{ source('TPC_H', 'SUPPLIER') }},
    {{ source('TPC_H', 'PARTSUPP') }},
    {{ source('TPC_H', 'NATION') }},
    {{ source('TPC_H', 'REGION') }}
where p_partkey = ps_partkey
    and s_suppkey = ps_suppkey
    and p_size = {{random_size}}
    and p_type like '%{{random_type}}'
    and s_nationkey = n_nationkey
    and n_regionkey = r_regionkey
    and r_name = '{{random_region}}'
    and ps_supplycost = (
        select min(ps_supplycost)
        from {{ source('TPC_H', 'PARTSUPP') }},
            {{ source('TPC_H', 'SUPPLIER') }},
            {{ source('TPC_H', 'NATION') }},
            {{ source('TPC_H', 'REGION') }}
        where p_partkey = ps_partkey
            and s_suppkey = ps_suppkey
            and s_nationkey = n_nationkey
            and n_regionkey = r_regionkey
            and r_name = '{{random_region}}'
    )
order by s_acctbal desc,
    n_name,
    s_name,
    p_partkey
LIMIT 100