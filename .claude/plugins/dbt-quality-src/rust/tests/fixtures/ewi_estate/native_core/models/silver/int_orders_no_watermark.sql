-- INC009: is_incremental() branch without {{ this }}
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id'
) }}

select order_id, customer_id, amount, updated_at
from {{ ref('stg_orders') }}
{% if is_incremental() %}
where updated_at >= dateadd(day, -3, current_date())
{% endif %}
