-- name: Performance Regression Detection
-- description: Identify performance degradation by comparing current execution times against historical baselines
-- Usage: snow sql -f performance_regression_detection.sql -c default

WITH recent_runs AS (
    SELECT
        m.name AS model_name,
        AVG(me.total_node_runtime) AS recent_avg_runtime
    FROM model_executions me
    JOIN models m ON me.node_id = m.node_id AND me.command_invocation_id = m.command_invocation_id
    JOIN invocations i ON me.command_invocation_id = i.command_invocation_id
    WHERE i.run_started_at >= DATEADD(day, -7, CURRENT_TIMESTAMP())
      AND me.status = 'success'
    GROUP BY m.name
),
baseline_runs AS (
    SELECT
        m.name AS model_name,
        AVG(me.total_node_runtime) AS baseline_avg_runtime
    FROM model_executions me
    JOIN models m ON me.node_id = m.node_id AND me.command_invocation_id = m.command_invocation_id
    JOIN invocations i ON me.command_invocation_id = i.command_invocation_id
    WHERE i.run_started_at >= DATEADD(day, -30, CURRENT_TIMESTAMP())
      AND i.run_started_at < DATEADD(day, -7, CURRENT_TIMESTAMP())
      AND me.status = 'success'
    GROUP BY m.name
)
SELECT
    r.model_name,
    ROUND(r.recent_avg_runtime, 2) AS recent_avg_seconds,
    ROUND(b.baseline_avg_runtime, 2) AS baseline_avg_seconds,
    ROUND(r.recent_avg_runtime - b.baseline_avg_runtime, 2) AS runtime_diff_sec,
    ROUND(100.0 * (r.recent_avg_runtime - b.baseline_avg_runtime) / b.baseline_avg_runtime, 2) AS pct_change
FROM recent_runs r
JOIN baseline_runs b ON r.model_name = b.model_name
WHERE r.recent_avg_runtime > b.baseline_avg_runtime * 1.2  -- 20% slower
ORDER BY pct_change DESC;
