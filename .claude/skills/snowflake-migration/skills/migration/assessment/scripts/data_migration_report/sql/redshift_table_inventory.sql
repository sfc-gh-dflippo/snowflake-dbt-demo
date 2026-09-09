-- Table volume inventory -- Amazon Redshift
--
-- Run once per source cluster or workgroup. Reads catalog metadata only: no
-- table scan, no locks on user data.
--
-- svv_table_info returns only the tables the current user can see; run as a
-- superuser, or grant SELECT on the tables in scope, or the result will be
-- silently short.
--
-- tbl_rows is Redshift's own estimate, including rows marked for deletion.
-- size is reported in 1 MB blocks.

SELECT
    TRIM(ti."schema")   AS schema_name,
    TRIM(ti."table")    AS table_name,
    ti.tbl_rows         AS estimated_row_count,
    ti.size             AS size_mb,
    ti.diststyle        AS dist_style,
    ti.sortkey1         AS first_sort_key,
    ti.pct_used         AS pct_of_allocated_space_used,
    ti.unsorted         AS pct_unsorted
FROM svv_table_info AS ti
WHERE ti."schema" NOT IN ('pg_catalog', 'information_schema', 'pg_internal')
ORDER BY ti.size DESC;
