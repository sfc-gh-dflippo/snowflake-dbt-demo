-- MAT001 trigger: view model with 3 consumers exceeds ephemeral_fanout_threshold
{{ config(materialized='view') }}
select customer_id, name, region
from {{ source('raw', 'customers') }}
