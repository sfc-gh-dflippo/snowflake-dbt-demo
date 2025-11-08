-- name: Test Execution Trends
-- description: Visualize test execution patterns including duration trends and flakiness indicators
-- Usage: snow sql -f test_execution_trends.sql -c default

SELECT
    DATE_TRUNC('day', i.run_started_at) AS execution_date,
    COUNT(DISTINCT te.node_id) AS unique_tests,
    COUNT(*) AS total_test_runs,
    SUM(CASE WHEN te.status = 'pass' THEN 1 ELSE 0 END) AS pass_count,
    SUM(CASE WHEN te.status = 'fail' THEN 1 ELSE 0 END) AS fail_count,
    SUM(CASE WHEN te.status = 'error' THEN 1 ELSE 0 END) AS error_count,
    ROUND(100.0 * SUM(CASE WHEN te.status = 'fail' THEN 1 ELSE 0 END) / COUNT(*), 2) AS fail_rate_pct,
    AVG(te.total_node_runtime) AS avg_runtime_sec
FROM test_executions te
JOIN invocations i ON te.command_invocation_id = i.command_invocation_id
WHERE i.run_started_at >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY execution_date
ORDER BY execution_date DESC;
