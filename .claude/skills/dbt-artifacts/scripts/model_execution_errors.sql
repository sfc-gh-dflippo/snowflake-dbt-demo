-- name: Model Execution Errors
-- description: Track models that failed to execute with detailed error messages
-- Usage: snow sql -f model_execution_errors.sql -c default

SELECT
    i.run_started_at,
    i.target_name,
    i.dbt_command,
    m.name AS model_name,
    m.materialization,
    m.path AS model_path,
    me.status,
    me.total_node_runtime AS execution_seconds,
    me.rows_affected,
    me.message
FROM model_executions me
JOIN invocations i
    ON me.command_invocation_id = i.command_invocation_id
JOIN models m
    ON me.node_id = m.node_id
    AND me.command_invocation_id = m.command_invocation_id
WHERE i.run_started_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND me.status != 'success'
ORDER BY i.run_started_at DESC;
