{{
    config(
        materialized='incremental',
        transient=false
    )
}}
/*
Log of changes made to the DIM_CUSTOMERS table utilizing a stream
 */
SELECT
    {% if is_incremental() %} {{- sequence_get_nextval() -}}
    {% else %} {{- recreate_sequence_get_nextval() -}}
    {% endif %} AS LOG_ID,
    D.*,
    IFF(METADATA$ACTION = 'DELETE', 'Y', 'N') AS DELETE_FLAG
FROM
    {% if is_incremental() %} {{- get_stream( ref('DIM_CUSTOMERS') ) -}}
    {% else %} {{- get_new_stream( ref('DIM_CUSTOMERS') ) -}}
    {% endif %} AS D

-- We do not want the DELETE rows from the stream for updates
WHERE NOT (METADATA$ACTION = 'DELETE' AND METADATA$ISUPDATE)

-- It is possible the same key was deleted and inserted
-- The following will deduplicate records, keeping the newest record and keeping INSERT over DELETE
qualify 1 = row_number() over (partition by C_CUSTKEY order by dbt_last_update_ts DESC, METADATA$ACTION DESC)
