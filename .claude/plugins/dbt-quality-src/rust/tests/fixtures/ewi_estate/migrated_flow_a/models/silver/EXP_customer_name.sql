-- MIG007: ETL instance name (EXP_ prefix)
select
    customer_id,
    first_name || ' ' || last_name as full_name
from {{ ref('SQ_customers') }}
