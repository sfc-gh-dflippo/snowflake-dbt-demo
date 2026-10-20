-- MAT001 fanout consumer B
select *
from {{ ref('stg_shared_view') }}
