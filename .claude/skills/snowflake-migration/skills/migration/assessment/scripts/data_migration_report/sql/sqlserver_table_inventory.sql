-- Table volume inventory -- Microsoft SQL Server
--
-- Run once per source database, connected to that database. Reads catalog
-- metadata only: no table scan, no locks on user data, safe on a busy system.
--
-- Requires VIEW DATABASE STATE on the database (or db_datareader plus
-- VIEW DATABASE STATE). Ask for it read-only; nothing here writes.
--
-- Row counts come from partition statistics and are accurate for committed
-- data, not transactionally consistent with an in-flight load.

SELECT
    DB_NAME()                                                       AS database_name,
    s.name                                                          AS schema_name,
    t.name                                                          AS table_name,
    SUM(CASE WHEN p.index_id IN (0, 1) THEN p.row_count ELSE 0 END) AS row_count,
    CAST(SUM(p.reserved_page_count) * 8.0 / 1024 AS DECIMAL(18, 2)) AS reserved_mb,
    CAST(SUM(p.used_page_count)     * 8.0 / 1024 AS DECIMAL(18, 2)) AS used_mb,
    COUNT(DISTINCT p.partition_number)                              AS partition_count
FROM sys.tables                  AS t
JOIN sys.schemas                 AS s ON s.schema_id = t.schema_id
JOIN sys.dm_db_partition_stats   AS p ON p.object_id = t.object_id
WHERE t.is_ms_shipped = 0
GROUP BY s.name, t.name
ORDER BY reserved_mb DESC;
