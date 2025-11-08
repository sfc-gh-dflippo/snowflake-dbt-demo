-- name: Execution Summary Report
-- description: Comprehensive overview of execution history including success rates, duration statistics, and error patterns
-- Usage: snow sql -f execution_summary.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT 
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RESOURCE_ATTRIBUTES['snow.database.name']::VARCHAR AS database_name,
    RESOURCE_ATTRIBUTES['snow.schema.name']::VARCHAR AS schema_name,
    COUNT(DISTINCT RESOURCE_ATTRIBUTES['snow.query.id']::VARCHAR) AS execution_count,
    MIN(TIMESTAMP) AS first_execution,
    MAX(TIMESTAMP) AS last_execution,
    COUNT(CASE WHEN RECORD['severity_text']::VARCHAR = 'ERROR' THEN 1 END) AS error_count,
    COUNT(CASE WHEN RECORD['severity_text']::VARCHAR = 'WARN' THEN 1 END) AS warning_count
FROM {{ event_table }}
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY project_name, database_name, schema_name
ORDER BY last_execution DESC;

