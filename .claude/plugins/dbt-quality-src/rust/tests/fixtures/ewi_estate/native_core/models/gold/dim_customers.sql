-- TST003: dim without dbt_constraints PK
-- DOC001: model missing description (gold layer = MEDIUM)
-- MAC009: hashed FK field
{{ config(materialized='table') }}

select
    md5(customer_id) as customer_sk,
    hash(customer_id) as hashed_customer_id,
    first_name,
    last_name,
    email,
    created_at
from {{ ref('stg_customers') }}
