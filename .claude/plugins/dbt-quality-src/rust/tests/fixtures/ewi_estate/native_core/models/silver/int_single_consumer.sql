-- MAT002 trigger: silver model with exactly one consumer and no tests or description
select
    id,
    name
from {{ ref('stg_customers') }}
where id is not null
