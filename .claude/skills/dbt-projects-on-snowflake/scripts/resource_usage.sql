-- Resource Usage Tracking
-- Query METRIC records to understand CPU and memory consumption by project
--
-- Usage: snow sql -f resource_usage.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT 
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RECORD['metric']['name']::VARCHAR AS metric_name,
    AVG(VALUE::FLOAT) AS avg_value,
    MAX(VALUE::FLOAT) AS max_value
FROM {{ event_table }}
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'METRIC'
  AND TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY project_name, metric_name
ORDER BY project_name, metric_name;

