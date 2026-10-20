-- INC004: table materialization with hand-rolled date window
{{ config(materialized='table') }}

select
    order_id,
    customer_id,
    order_date,
    amount
from {{ ref('stg_orders') }}
where order_date >= dateadd(day, -30, current_date())
