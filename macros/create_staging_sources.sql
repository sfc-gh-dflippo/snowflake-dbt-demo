{#-
  Create the STAGING source tables declared in models/bronze/_sources.yml.
  Input: target.database. Output: STAGING.CUSTOMER and STAGING.SALESORDER.
  Side effect: creates each table from TPC-H sample data only when it is missing.
  Simplification: a fixed 10,000-order slice. Replace with a real ETL load for production.
-#}
{% macro create_staging_sources() %}
  {% if execute %}
    {% set db = target.database %}
    {% do run_query("create schema if not exists " ~ db ~ ".STAGING") %}
    {% do run_query("
      create table if not exists " ~ db ~ ".STAGING.CUSTOMER as
      select
          c.c_custkey as customerid,
          c.c_name as customername,
          c.c_mktsegment as customersegment,
          r.r_name as region,
          n.n_name as country,
          lower(replace(c.c_name, '#', '')) || '@example.com' as email,
          c.c_phone as phone
      from snowflake_sample_data.tpch_sf1.customer as c
      inner join snowflake_sample_data.tpch_sf1.nation as n on c.c_nationkey = n.n_nationkey
      inner join snowflake_sample_data.tpch_sf1.region as r on n.n_regionkey = r.r_regionkey
    ") %}
    {% do run_query("
      create table if not exists " ~ db ~ ".STAGING.SALESORDER as
      select
          o.o_orderkey as sourceorderid,
          'SO-' || o.o_orderkey as ordernumber,
          l.l_linenumber as orderlinenumber,
          o.o_orderdate as orderdate,
          l.l_shipdate as shipdate,
          o.o_custkey as customerid,
          l.l_partkey as productid,
          l.l_suppkey as storeid,
          l.l_quantity as quantity,
          round(l.l_extendedprice / l.l_quantity, 2) as unitprice,
          round(l.l_extendedprice / l.l_quantity * 0.7, 2) as unitcost,
          round(l.l_extendedprice * l.l_discount, 2) as discountamount,
          1 as batchid
      from snowflake_sample_data.tpch_sf1.orders as o
      inner join snowflake_sample_data.tpch_sf1.lineitem as l on o.o_orderkey = l.l_orderkey
      where o.o_orderkey <= 40000
    ") %}
  {% endif %}
{% endmacro %}
