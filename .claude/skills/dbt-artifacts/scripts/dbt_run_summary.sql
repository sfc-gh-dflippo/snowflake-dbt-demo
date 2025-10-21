-- dbt Run Summary
-- High-level overview of all dbt run executions
-- Usage: snow sql -f dbt_run_summary.sql -c default

SELECT
    run_started_at,
    dbt_version,
    dbt_command,
    target_name,
    target_schema,
    full_refresh_flag,
    target_threads,
    command_invocation_id
FROM invocations
WHERE run_started_at >= DATEADD(day, -30, CURRENT_TIMESTAMP())
ORDER BY run_started_at DESC;
