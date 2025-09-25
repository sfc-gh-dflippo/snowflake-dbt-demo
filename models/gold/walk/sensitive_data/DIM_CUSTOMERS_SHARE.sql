/*
 Queries in the sensitive folder will be created as secure views
 */
select
    customer_key,
    customer_name,
    market_segment,
    customer_comment,
    has_orders_flag,
    has_open_orders_flag
from {{ ref('dim_customers') }}
