-- INC012: append strategy on mutable data
{{ config(
    materialized='incremental',
    incremental_strategy='append'
) }}

select
    order_id,
    customer_id,
    order_status,
    updated_at
from {{ ref('stg_orders') }}
{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }})
  and updated_at >= dateadd(day, -7, current_date())
{% endif %}
