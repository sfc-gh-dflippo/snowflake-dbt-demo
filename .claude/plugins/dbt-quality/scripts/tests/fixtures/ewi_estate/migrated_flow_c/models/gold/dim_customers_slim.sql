-- PRJ001: micro-project (only 2 models)
-- PRJ002: shares source raw.customers with migrated_flow_a
select customer_id, email
from {{ source('raw', 'customers') }}
