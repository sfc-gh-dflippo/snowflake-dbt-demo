-- Slowest Models
-- Identify models with longest execution times (average and peak)
-- Usage: snow sql -f slowest_models.sql -c default

SELECT
    m.name AS model_name,
    m.materialization,
    m.schema,
    COUNT(DISTINCT i.command_invocation_id) AS run_count,
    AVG(me.total_node_runtime) AS avg_runtime_sec,
    MAX(me.total_node_runtime) AS max_runtime_sec,
    MIN(me.total_node_runtime) AS min_runtime_sec,
    AVG(me.rows_affected) AS avg_rows_affected,
    SUM(CASE WHEN me.status = 'error' THEN 1 ELSE 0 END) AS error_count
FROM model_executions me
JOIN models m
    ON me.node_id = m.node_id
    AND me.command_invocation_id = m.command_invocation_id
JOIN invocations i
    ON me.command_invocation_id = i.command_invocation_id
WHERE i.run_started_at >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY m.name, m.materialization, m.schema
HAVING COUNT(*) >= 5
ORDER BY avg_runtime_sec DESC
LIMIT 20;
