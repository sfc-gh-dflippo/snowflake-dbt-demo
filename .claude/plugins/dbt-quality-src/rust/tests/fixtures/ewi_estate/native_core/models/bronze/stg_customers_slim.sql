-- ARC004: duplicate staging model over same source
select
    customer_id,
    email
from {{ source('raw', 'customers') }}
