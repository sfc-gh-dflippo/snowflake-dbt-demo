-- name: Failure Alert Query
-- description: Generate alerts for failed executions with error details and affected resources
-- Usage: snow sql -f alert_failures.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT COUNT(*) AS error_count
FROM {{ event_table }}
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND RECORD['severity_text']::VARCHAR = 'ERROR'
  AND TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
HAVING error_count > 0;
