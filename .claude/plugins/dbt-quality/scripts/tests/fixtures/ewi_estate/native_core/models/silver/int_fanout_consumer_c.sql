-- MAT001 fanout consumer C
select *
from {{ ref('stg_shared_view') }}
