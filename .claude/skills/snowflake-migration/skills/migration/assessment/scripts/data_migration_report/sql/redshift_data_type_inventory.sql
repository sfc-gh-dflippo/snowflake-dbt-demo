-- Data type inventory -- Amazon Redshift
--
-- Run once per source cluster or workgroup. Catalog metadata only.
--
-- svv_columns covers local, external, and datashared tables, and reports the
-- spelled-out type names Redshift stores ("character varying", "timestamp
-- without time zone"), which are the names the migration type map is keyed on.

SELECT
    LOWER(c.data_type)                                    AS source_type,
    COUNT(*)                                              AS column_count,
    COUNT(DISTINCT c.table_schema || '.' || c.table_name) AS table_count,
    MAX(c.character_maximum_length)                       AS max_declared_length,
    MAX(c.numeric_precision)                              AS max_precision,
    MAX(c.numeric_scale)                                  AS max_scale
FROM svv_columns AS c
WHERE c.table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_internal')
GROUP BY LOWER(c.data_type)
ORDER BY column_count DESC;
