-- name: Execution Error Analysis
-- description: Analyze and categorize execution errors with frequency counts and remediation suggestions
-- Usage: snow sql -f execution_errors.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT 
    TIMESTAMP,
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RESOURCE_ATTRIBUTES['snow.database.name']::VARCHAR AS database_name,
    RESOURCE_ATTRIBUTES['snow.schema.name']::VARCHAR AS schema_name,
    RESOURCE_ATTRIBUTES['snow.query.id']::VARCHAR AS query_id,
    RECORD['severity_text']::VARCHAR AS severity,
    VALUE::VARCHAR AS error_message
FROM {{ event_table }}
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND RECORD['severity_text']::VARCHAR IN ('ERROR')
  AND TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC;

