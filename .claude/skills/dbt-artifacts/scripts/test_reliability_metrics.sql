-- Test Reliability Metrics
-- Calculate pass/fail rates to identify flaky or unreliable tests
-- Usage: snow sql -f test_reliability_metrics.sql -c default

SELECT
    t.name AS test_name,
    t.test_path,
    COUNT(*) AS total_executions,
    SUM(CASE WHEN te.status = 'pass' THEN 1 ELSE 0 END) AS passes,
    SUM(CASE WHEN te.status = 'fail' THEN 1 ELSE 0 END) AS failures,
    SUM(CASE WHEN te.status = 'warn' THEN 1 ELSE 0 END) AS warnings,
    SUM(CASE WHEN te.status = 'error' THEN 1 ELSE 0 END) AS errors,
    ROUND(100.0 * SUM(CASE WHEN te.status = 'fail' THEN 1 ELSE 0 END) / COUNT(*), 2) AS failure_rate_pct,
    AVG(te.total_node_runtime) AS avg_runtime_sec,
    MAX(te.failures) AS max_failing_rows
FROM test_executions te
JOIN tests t ON te.node_id = t.node_id
WHERE te.run_started_at >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY t.name, t.test_path
HAVING COUNT(*) >= 5
ORDER BY failure_rate_pct DESC, failures DESC;
