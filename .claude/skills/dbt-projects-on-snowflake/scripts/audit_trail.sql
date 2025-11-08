-- name: Audit Trail Logging
-- description: Track all execution events with timestamps, users, and changes for compliance and debugging
-- Usage: snow sql -f audit_trail.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT 
    TIMESTAMP,
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RESOURCE_ATTRIBUTES['db.user']::VARCHAR AS executed_by,
    RESOURCE_ATTRIBUTES['snow.session.role.primary.name']::VARCHAR AS role,
    RESOURCE_ATTRIBUTES['snow.warehouse.name']::VARCHAR AS warehouse,
    RECORD['severity_text']::VARCHAR AS severity,
    VALUE::VARCHAR AS message
FROM {{ event_table }}
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC;

