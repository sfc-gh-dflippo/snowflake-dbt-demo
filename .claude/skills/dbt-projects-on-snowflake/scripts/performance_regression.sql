-- name: Performance Regression Detection
-- description: Identify performance degradation by comparing current execution times against historical baselines
-- Usage: snow sql -f performance_regression.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT
    DATE_TRUNC('week', TIMESTAMP)::DATE AS week,
    AVG(TIMESTAMPDIFF(milliseconds, start_timestamp, timestamp) / 1000.0 / 60.0) AS avg_minutes
FROM {{ event_table }}
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'SPAN'
GROUP BY week
ORDER BY week DESC;
