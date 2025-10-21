# dbt Projects on Snowflake - Monitoring & Observability

Comprehensive guide for monitoring dbt Projects using Snowflake's native event tables and OpenTelemetry telemetry capture.

## Overview

Monitoring is performed through event tables that capture detailed telemetry data including logs, traces, and metrics during dbt project execution. Event tables use the [OpenTelemetry data model](https://opentelemetry.io/).

**Reference**: [dbt Projects Monitoring](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability)

## Event Table Setup

### Critical Pattern: Database-Level Configuration

Always set event tables at the **DATABASE** level (not schema, not account-wide):

```sql
-- 1. Create event table (can be in different database)
CREATE EVENT TABLE IF NOT EXISTS MY_LOGGING_DATABASE.MY_LOGGING_SCHEMA.EVENT_LOG;

-- 2. Set event table where dbt Projects are deployed at DATABASE level
ALTER DATABASE MY_DBT_PROJECT_DATABASE 
  SET EVENT_TABLE = MY_LOGGING_DATABASE.MY_LOGGING_SCHEMA.EVENT_LOG;

-- 3. Configure logging levels for the schema where dbt Project is deployed
ALTER SCHEMA MY_DBT_PROJECT_DATABASE.MY_DBT_PROJECT_SCHEMA SET LOG_LEVEL = 'INFO';
ALTER SCHEMA MY_DBT_PROJECT_DATABASE.MY_DBT_PROJECT_SCHEMA SET TRACE_LEVEL = 'ALWAYS';
ALTER SCHEMA MY_DBT_PROJECT_DATABASE.MY_DBT_PROJECT_SCHEMA SET METRIC_LEVEL = 'ALL';
```

**Why DATABASE level?**
- Captures all dbt Project executions in that database
- Avoids account-wide noise
- Provides project-level isolation

## Event Table Structure (OpenTelemetry)

Event tables follow the OpenTelemetry data model with these key columns:

| Column | Description |
|--------|-------------|
| **TIMESTAMP** | UTC timestamp when event was created (end of time span for span events) |
| **START_TIMESTAMP** | For span events, the start of the time span |
| **TRACE** | Tracing context with `trace_id` and `span_id` |
| **RESOURCE_ATTRIBUTES** | Source identification: database, schema, user, warehouse, etc. |
| **SCOPE** | Event scopes (e.g., class names for logs) |
| **RECORD_TYPE** | Event type: `LOG`, `SPAN`, `SPAN_EVENT`, `EVENT`, `METRIC` |
| **RECORD** | JSON object with record-specific data (severity, metric type, span details) |
| **RECORD_ATTRIBUTES** | Event metadata set by Snowflake or code |
| **VALUE** | Actual log message, metric value, or null for spans |

## Monitoring Queries

### Recent dbt Project Executions

Lists recent executions with basic information and log severity:

```sql
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
FROM MY_DATABASE.MY_SCHEMA.EVENT_LOG
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND RECORD['severity_text']::VARCHAR IN ('ERROR', 'WARN', 'INFO')
  AND TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC;
```

### dbt Project Execution Errors

Query for ERROR level logs to identify failures:

```sql
SELECT 
    TIMESTAMP,
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RESOURCE_ATTRIBUTES['snow.database.name']::VARCHAR AS database_name,
    RESOURCE_ATTRIBUTES['snow.schema.name']::VARCHAR AS schema_name,
    RESOURCE_ATTRIBUTES['snow.query.id']::VARCHAR AS query_id,
    RECORD['severity_text']::VARCHAR AS severity,
    VALUE::VARCHAR AS error_message
FROM MY_DATABASE.MY_SCHEMA.EVENT_LOG
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND RECORD['severity_text']::VARCHAR IN ('ERROR')
  AND TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC;
```

### dbt Project Performance Metrics

Query performance metrics (CPU, memory usage):

```sql
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
FROM MY_DATABASE.MY_SCHEMA.EVENT_LOG
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'METRIC'
  AND TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC;
```

### dbt Project Trace Spans

Query execution spans for detailed tracing and duration analysis:

```sql
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
FROM MY_DATABASE.MY_SCHEMA.EVENT_LOG l
WHERE l.RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND l.RECORD_TYPE = 'SPAN'
  AND l.TIMESTAMP >= DATEADD(hour, -12, CURRENT_TIMESTAMP())
ORDER BY l.TIMESTAMP DESC;
```

### dbt Execution Summary by Project

Summarize executions by project with error counts:

```sql
SELECT 
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RESOURCE_ATTRIBUTES['snow.database.name']::VARCHAR AS database_name,
    RESOURCE_ATTRIBUTES['snow.schema.name']::VARCHAR AS schema_name,
    COUNT(DISTINCT RESOURCE_ATTRIBUTES['snow.query.id']::VARCHAR) AS execution_count,
    MIN(TIMESTAMP) AS first_execution,
    MAX(TIMESTAMP) AS last_execution,
    COUNT(CASE WHEN RECORD['severity_text']::VARCHAR = 'ERROR' THEN 1 END) AS error_count,
    COUNT(CASE WHEN RECORD['severity_text']::VARCHAR = 'WARN' THEN 1 END) AS warning_count
FROM MY_DATABASE.MY_SCHEMA.EVENT_LOG
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY project_name, database_name, schema_name
ORDER BY last_execution DESC;
```

## Best Practices for Monitoring

### Performance Optimization

**Always filter by TIMESTAMP** to limit scanned data:
```sql
-- ✅ Good: Filter reduces data scanned
WHERE TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())

-- ❌ Avoid: Scanning all time periods
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
```

**Use RESOURCE_ATTRIBUTES for filtering** by project/database/schema:
```sql
-- ✅ Good: Efficient filtering
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR = 'my_project'
```

### Monitoring Strategy

1. **Set event tables at DATABASE level**, not account or schema
2. **Configure appropriate log/trace/metric levels** per schema
3. **Always filter by TIMESTAMP** to avoid scanning large event tables
4. **Use `snow.executable.type = 'DBT_PROJECT'`** to isolate dbt events
5. **Leverage RESOURCE_ATTRIBUTES** for filtering by project/database/schema
6. **Monitor ERROR severity logs** for immediate alerts
7. **Use SPAN records** to analyze execution timing and bottlenecks
8. **Archive old event table data** (>90 days) to separate tables

### Alerting Strategy

**High Priority:**
- Any ERROR in dbt project execution
- Execution > 2x historical average
- Warehouse credit usage anomalies

**Medium Priority:**
- WARNING level logs
- Test or model failures on critical models
- Performance metrics trending down

**Low Priority:**
- INFO level logs
- Scheduled job completion confirmation
- Performance metrics for analysis

## Common Use Cases

### Alert on Execution Failures

Monitor ERROR severity logs and send alerts when executions fail:

```sql
-- Alert trigger example
SELECT COUNT(*) AS error_count
FROM MY_DATABASE.MY_SCHEMA.EVENT_LOG
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND RECORD['severity_text']::VARCHAR = 'ERROR'
  AND TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
HAVING error_count > 0;
```

### Performance Regression Detection

Compare span durations over time to detect performance degradation:

```sql
-- Compare average execution time week-over-week
SELECT 
    DATE_TRUNC('week', TIMESTAMP)::DATE AS week,
    AVG(TIMESTAMPDIFF(milliseconds, start_timestamp, timestamp) / 1000.0 / 60.0) AS avg_minutes
FROM MY_DATABASE.MY_SCHEMA.EVENT_LOG
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'SPAN'
GROUP BY week
ORDER BY week DESC;
```

### Resource Usage Tracking

Query METRIC records to understand CPU and memory consumption:

```sql
-- Track resource usage by project
SELECT 
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RECORD['metric']['name']::VARCHAR AS metric_name,
    AVG(VALUE::FLOAT) AS avg_value,
    MAX(VALUE::FLOAT) AS max_value
FROM MY_DATABASE.MY_SCHEMA.EVENT_LOG
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'METRIC'
  AND TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY project_name, metric_name
ORDER BY project_name, metric_name;
```

### Execution Audit Trail

Use RESOURCE_ATTRIBUTES to track who executed what and when:

```sql
-- Complete audit trail
SELECT 
    TIMESTAMP,
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RESOURCE_ATTRIBUTES['db.user']::VARCHAR AS executed_by,
    RESOURCE_ATTRIBUTES['snow.session.role.primary.name']::VARCHAR AS role,
    RESOURCE_ATTRIBUTES['snow.warehouse.name']::VARCHAR AS warehouse,
    RECORD['severity_text']::VARCHAR AS severity,
    VALUE::VARCHAR AS message
FROM MY_DATABASE.MY_SCHEMA.EVENT_LOG
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND RECORD_TYPE = 'LOG'
  AND TIMESTAMP >= DATEADD(day, -30, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC;
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No events captured | Verify event table set at DATABASE level with `ALTER DATABASE` |
| Too many events | Adjust `LOG_LEVEL`/`TRACE_LEVEL`/`METRIC_LEVEL` per schema |
| Slow monitoring queries | Always filter by TIMESTAMP first; consider archiving old data |
| Missing metrics | Set `METRIC_LEVEL = 'ALL'` for schema |
| Missing traces | Set `TRACE_LEVEL = 'ALWAYS'` for schema |
| Cannot see project name | Verify `snow.executable.type = 'DBT_PROJECT'` filter |

## References

- [dbt Projects on Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake)
- [dbt Projects Monitoring](https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability)
- [Event Table Setup](https://docs.snowflake.com/en/developer-guide/logging-tracing/event-table-setting-up)
- [OpenTelemetry Data Model](https://opentelemetry.io/)
