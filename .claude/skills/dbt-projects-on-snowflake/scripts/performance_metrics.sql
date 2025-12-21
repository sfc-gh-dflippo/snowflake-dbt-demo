-- name: Performance Metrics Analysis
-- description: Track and analyze key performance indicators including execution time, data volume, and resource efficiency
-- Usage: snow sql -f performance_metrics.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT
    TIMESTAMP,
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RESOURCE_ATTRIBUTES['snow.database.name']::VARCHAR AS database_name,
    RESOURCE_ATTRIBUTES['snow.schema.name']::VARCHAR AS schema_name,
    RESOURCE_ATTRIBUTES['snow.query.id']::VARCHAR AS query_id,
    RECORD['metric']['name']::VARCHAR AS metric_name,
    RECORD['metric']['unit']::VARCHAR AS metric_unit,
    RECORD['metric_type']::VARCHAR AS metric_type,
    RECORD['value_type']::VARCHAR AS value_type,
    VALUE::FLOAT AS metric_value,
    RESOURCE_ATTRIBUTES
FROM {{ event_table }}
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'METRIC'
  AND TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC;
