{{
    config(
        materialized="incremental",
        transient=false
    )
}}
/*
Log of changes made to the DIM_CUSTOMERS table utilizing a stream
 */
select
    {{ sequence_get_nextval() }} as log_id,
    d.*,
    iff(metadata$action = 'DELETE', 'Y', 'N') as delete_flag
from
    {{ get_stream( ref("DIM_CUSTOMERS") ) }} as d

-- We do not want the DELETE rows from the stream for updates
where not (metadata$action = 'DELETE' and metadata$isupdate)

-- It is possible the same key was deleted and inserted
-- The following will deduplicate records, keeping the newest record and keeping INSERT over DELETE
qualify 1 = row_number() over (partition by c_custkey order by dbt_updated_ts desc, metadata$action desc)
