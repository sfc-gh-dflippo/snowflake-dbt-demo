-- INC011: merge_exclude_columns referencing absent column
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id',
    merge_exclude_columns=['created_at_never_here']
) }}

select order_id, customer_id, amount
from {{ ref('stg_orders') }}
{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }})
  and updated_at >= dateadd(day, -7, current_date())
{% endif %}
