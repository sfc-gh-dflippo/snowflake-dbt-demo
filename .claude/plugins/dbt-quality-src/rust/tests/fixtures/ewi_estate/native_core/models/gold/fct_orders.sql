-- TST004: fact without FK tests
-- MAT004: clustering over-specified (>4 columns)
{{ config(
    materialized='table',
    cluster_by=['order_date', 'customer_id', 'product_id', 'region_id', 'channel_id']
) }}

select
    order_id,
    customer_id,
    product_id,
    region_id,
    channel_id,
    order_date,
    amount
from {{ ref('int_customer_orders') }}
