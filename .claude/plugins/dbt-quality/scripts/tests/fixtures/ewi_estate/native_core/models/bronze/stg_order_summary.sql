-- ARC006: staging model with join and aggregation
select
    o.customer_id,
    c.first_name,
    count(*) as order_count,
    sum(o.amount) as total_amount
from {{ source('raw', 'orders') }} o
join {{ source('raw', 'customers') }} c
    on o.customer_id = c.customer_id
group by o.customer_id, c.first_name
