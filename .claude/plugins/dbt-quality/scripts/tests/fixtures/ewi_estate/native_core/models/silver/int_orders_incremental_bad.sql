-- triggers: INC006 (no guard), INC007 (no unique_key), INC008 (no strategy)
{{ config(materialized='incremental') }}

select
    order_id,
    customer_id,
    amount,
    updated_at
from {{ ref('stg_orders') }}
