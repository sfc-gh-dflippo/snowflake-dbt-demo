-- SQL002 trigger: identical CTE body appears in int_shared_cte_a and int_shared_cte_b
with customer_stats as (
    select
        customer_id,
        count(*) as order_count,
        sum(amount) as total_spent,
        max(order_date) as last_order_date
    from {{ ref('stg_orders') }}
    group by customer_id
)
select *
from customer_stats
