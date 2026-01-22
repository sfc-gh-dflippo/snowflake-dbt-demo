/*
    dbt Feature Demonstration: DYNAMIC TABLE - REAL-TIME ANALYTICS

    This model demonstrates:
    - ✅ Dynamic table materialization (Snowflake-specific)
    - ✅ Real-time data refresh with target_lag
    - ✅ Warehouse configuration for compute
    - ✅ Advanced Jinja templating with variables
    - ✅ Complex aggregations and window functions
    - ✅ Configuration change handling
    - ✅ Time-based partitioning and analytics
    - ✅ Business metrics calculation

    Complexity: 🥇 RUN (Advanced)
    Layer: Silver - Real-time Analytics
*/

{{ config(
    materialized='dynamic_table',
    snowflake_warehouse=target.warehouse,
    target_lag='1 hour',
    tags=['silver', 'run', 'real_time'],
    on_configuration_change='apply'
) }}

-- SILVER RUN: Real-time order analytics with dynamic tables
-- Complexity: Advanced - Dynamic tables, complex aggregations, advanced Jinja
-- Features demonstrated: Dynamic table materialization, advanced analytics

{% set order_statuses = ['O', 'F', 'P'] %}
{% set priority_levels = ['1-URGENT', '2-HIGH', '3-MEDIUM', '4-NOT SPECIFIED', '5-LOW'] %}

select
    -- Time dimensions
    date_trunc('day', o_orderdate) as order_date,
    extract(year from o_orderdate) as order_year,
    extract(month from o_orderdate) as order_month,
    extract(quarter from o_orderdate) as order_quarter,
    extract(dayofweek from o_orderdate) as day_of_week,

    -- Customer dimension
    o_custkey as customer_key,

    -- Order attributes
    o_orderstatus as order_status,
    o_orderpriority as order_priority,

    -- Metrics
    count(*) as order_count,
    sum(o_totalprice) as total_order_value,
    avg(o_totalprice) as avg_order_value,
    min(o_totalprice) as min_order_value,
    max(o_totalprice) as max_order_value,
    stddev(o_totalprice) as order_value_stddev,

    -- Advanced analytics
    count(distinct o_custkey) as unique_customers,
    sum(o_totalprice) / count(distinct o_custkey) as revenue_per_customer,

    {% for status in order_statuses %}
    sum(case when o_orderstatus = '{{ status }}' then o_totalprice else 0 end) as revenue_{{ status.lower() }}_status,
    count(case when o_orderstatus = '{{ status }}' then 1 end) as count_{{ status.lower() }}_status,
    {% endfor %}

    -- Priority analysis
    {% for priority in priority_levels %}
    sum(case when o_orderpriority = '{{ priority }}' then o_totalprice else 0 end) as revenue_priority_{{ loop.index }},
    {% endfor %}

    -- Real-time processing metadata
    current_timestamp() as last_updated,
    '{{ run_started_at }}' as run_started_at,
    '{{ invocation_id }}' as invocation_id

from {{ ref('stg_orders_incremental') }}
where processing_type in ('RECENT', 'FULL_LOAD')
group by
    date_trunc('day', o_orderdate),
    extract(year from o_orderdate),
    extract(month from o_orderdate),
    extract(quarter from o_orderdate),
    extract(dayofweek from o_orderdate),
    o_custkey,
    o_orderstatus,
    o_orderpriority
