select
    order_id,
    current_timestamp() as _dbt_loaded_at,
    current_user() as _dbt_loaded_by,
    'native_core' as _dbt_source,
    null as _dbt_batch_id
from {{ ref('stg_orders') }}
