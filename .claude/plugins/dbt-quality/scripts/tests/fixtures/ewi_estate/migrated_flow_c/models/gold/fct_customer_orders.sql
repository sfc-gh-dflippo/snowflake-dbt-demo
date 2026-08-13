select customer_id, count(*) as order_count
from {{ source('raw', 'customers') }}
group by customer_id
