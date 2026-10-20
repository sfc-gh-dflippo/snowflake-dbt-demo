-- MAT002 trigger: sole consumer of int_single_consumer
select *
from {{ ref('int_single_consumer') }}
