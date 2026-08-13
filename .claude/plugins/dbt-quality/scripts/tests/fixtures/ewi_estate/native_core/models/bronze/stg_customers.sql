-- stg_customers: staging model for raw.customers
select
    customer_id,
    first_name,
    last_name,
    email,
    created_at
from {{ source('raw', 'customers') }}
