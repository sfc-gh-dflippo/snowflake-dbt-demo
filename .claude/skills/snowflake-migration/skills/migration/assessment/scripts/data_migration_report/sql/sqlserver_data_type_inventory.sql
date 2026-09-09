-- Data type inventory -- Microsoft SQL Server
--
-- Run once per source database, connected to that database. Catalog metadata
-- only. Requires nothing beyond read access to the system catalog views.
--
-- Joins on user_type_id rather than system_type_id so an alias or user-defined
-- type reports its own name instead of collapsing to its base type.

SELECT
    UPPER(ty.name)              AS source_type,
    COUNT(*)                    AS column_count,
    COUNT(DISTINCT c.object_id) AS table_count,
    MAX(c.max_length)           AS max_declared_length,
    MAX(c.precision)            AS max_precision,
    MAX(c.scale)                AS max_scale
FROM sys.columns AS c
JOIN sys.tables  AS t  ON t.object_id    = c.object_id
JOIN sys.types   AS ty ON ty.user_type_id = c.user_type_id
WHERE t.is_ms_shipped = 0
GROUP BY UPPER(ty.name)
ORDER BY column_count DESC;
