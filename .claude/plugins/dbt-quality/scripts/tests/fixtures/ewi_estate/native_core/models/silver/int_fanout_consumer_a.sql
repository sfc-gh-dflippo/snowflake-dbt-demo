-- MAT001 fanout consumer A
select *
from {{ ref('stg_shared_view') }}
