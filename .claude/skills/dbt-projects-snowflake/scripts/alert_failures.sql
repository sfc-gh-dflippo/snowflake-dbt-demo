-- Alert on Execution Failures
-- Monitor ERROR severity logs and send alerts when executions fail
-- Returns count of errors in the last hour - use in alerting systems
--
-- Usage: snow sql -f alert_failures.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT COUNT(*) AS error_count
FROM {{ event_table }}
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND RECORD['severity_text']::VARCHAR = 'ERROR'
  AND TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
HAVING error_count > 0;

