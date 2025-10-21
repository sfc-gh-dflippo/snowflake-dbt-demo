-- Recent dbt Project Executions
-- Lists recent executions with basic information and log severity
--
-- Usage: snow sql -f recent_executions.sql --enable-templating JINJA -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

SELECT 
    TIMESTAMP,
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RESOURCE_ATTRIBUTES['snow.database.name']::VARCHAR AS database_name,
    RESOURCE_ATTRIBUTES['snow.schema.name']::VARCHAR AS schema_name,
    RESOURCE_ATTRIBUTES['db.user']::VARCHAR AS user_name,
    RESOURCE_ATTRIBUTES['snow.owner.name']::VARCHAR AS owner_name,
    RESOURCE_ATTRIBUTES['snow.query.id']::VARCHAR AS query_id,
    RESOURCE_ATTRIBUTES['snow.session.role.primary.name']::VARCHAR AS primary_role_name,
    RESOURCE_ATTRIBUTES['snow.warehouse.name']::VARCHAR AS warehouse_name,
    RECORD['severity_text']::VARCHAR AS severity,
    VALUE::VARCHAR AS message
FROM {{ event_table }}
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND RECORD['severity_text']::VARCHAR IN ('ERROR', 'WARN', 'INFO')
  AND TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC;

