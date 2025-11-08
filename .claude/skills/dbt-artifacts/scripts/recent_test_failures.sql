-- name: Recent Test Failures
-- description: Identify recently failed tests with failure reasons and historical pass/fail trends
-- Usage: snow sql -f recent_test_failures.sql -c default

SELECT
    i.run_started_at,
    i.dbt_command,
    i.target_name,
    i.target_schema,
    t.name AS test_name,
    t.test_path,
    t.depends_on_nodes,
    te.status,
    te.failures,
    te.total_node_runtime AS execution_seconds,
    te.message
FROM test_executions te
JOIN invocations i
    ON te.command_invocation_id = i.command_invocation_id
JOIN tests t
    ON te.node_id = t.node_id
    AND te.command_invocation_id = t.command_invocation_id
WHERE i.run_started_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  AND te.status IN ('fail', 'error')
ORDER BY i.run_started_at DESC;
