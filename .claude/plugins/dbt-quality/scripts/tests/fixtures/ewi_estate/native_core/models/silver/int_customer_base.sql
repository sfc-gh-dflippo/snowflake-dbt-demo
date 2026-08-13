-- SQL009: generic CTE name (t1)
-- SQL010: unused CTE (dead_cte)
with t1 as (
    select customer_id, first_name
    from {{ ref('stg_customers') }}
),
dead_cte as (
    select order_id from {{ ref('stg_orders') }}
)
select * from t1
