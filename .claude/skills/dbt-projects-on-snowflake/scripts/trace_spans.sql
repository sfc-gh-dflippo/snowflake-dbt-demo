-- name: Execution Trace Spans
-- description: Detailed tracing data for execution spans showing timing breakdowns and dependencies
-- Usage: snow sql -f trace_spans.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RESOURCE_ATTRIBUTES['snow.database.name']::VARCHAR AS database_name,
    RESOURCE_ATTRIBUTES['snow.schema.name']::VARCHAR AS schema_name,
    start_timestamp,
    TIMESTAMP,
    TIMESTAMPDIFF(milliseconds, start_timestamp, timestamp)::INTEGER AS milliseconds_duration,
    ROUND(milliseconds_duration / 1000, 3) AS seconds_duration,
    ROUND(milliseconds_duration / 60000, 2) AS minutes_duration,
    RECORD['name']::VARCHAR AS span_name,
    TRACE['trace_id']::VARCHAR AS trace_id,
    TRACE['span_id']::VARCHAR AS span_id,
    RESOURCE_ATTRIBUTES,
    RECORD,
    RECORD_ATTRIBUTES,
    SCOPE
FROM {{ event_table }} l
WHERE l.RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND l.RECORD_TYPE = 'SPAN'
  AND l.TIMESTAMP >= DATEADD(hour, -12, CURRENT_TIMESTAMP())
ORDER BY l.TIMESTAMP DESC;
