---
name: dbt-projects-on-snowflake
description:
  Deploying, managing, executing, and monitoring dbt projects natively within Snowflake using dbt
  PROJECT objects and event tables. Use this skill when you want to set up dbt development
  workspaces, deploy projects to Snowflake, schedule automated runs, monitor execution with event
  tables, or enable team collaboration directly in Snowflake.
---

# dbt Projects on Snowflake

Deploy, manage, and monitor dbt projects natively within Snowflake using web-based workspaces,
schema-level DBT PROJECT objects, and comprehensive event table telemetry.

## Quick Start

**Three Ways to Use dbt Projects:**

1. **Snowsight Workspaces** - Web-based IDE for interactive development
2. **DBT PROJECT Objects** - Deployed projects for production execution
3. **Snowflake CLI** - Command-line deployment and execution

## Setup

Complete setup instructions including prerequisites, external access integration, Git API
integration, and event table configuration are in `references/SETUP.md`.

## Deployment Methods

### Method 1: Snowflake CLI (Recommended)

```bash
# Deploy project
snow dbt deploy my_project --source .

# Execute commands
snow dbt execute my_project run
snow dbt execute my_project build
```

### Method 2: Snowsight

- Navigate to Projects → My Workspace
- Create new project from Git repository
- Configure profiles.yml
- Deploy as DBT PROJECT object

### Method 3: SQL Execution

Execute directly in SQL:

```sql
EXECUTE DBT PROJECT <db>.<schema>.<project> args='build';
EXECUTE DBT PROJECT <db>.<schema>.<project> args='build --full-refresh';
EXECUTE DBT PROJECT <db>.<schema>.<project> args='build --select tag:gold';
```

## Scheduling & Automation

For automated scheduling with Snowflake Tasks, see the "Optional: Schedule Automated Runs" section
in `references/SETUP.md`.

## Event Table Monitoring

### Setup

Configure event tables following the Event Table Monitoring Configuration section in
`references/SETUP.md`. This enables OpenTelemetry-based monitoring of dbt project executions.

### Monitoring Queries

All monitoring scripts use parameterized event table references. Specify your event table location
when running:

```bash
# Example: Query recent executions
snow sql -f scripts/recent_executions.sql --enable-templating JINJA \
  -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG

# Example: Check for errors
snow sql -f scripts/execution_errors.sql --enable-templating JINJA \
  -D event_table=LOGS_DB.PUBLIC.DBT_EVENTS

# Example: Performance metrics
snow sql -f scripts/performance_metrics.sql --enable-templating JINJA \
  -D event_table=MY_DATABASE.MY_SCHEMA.EVENT_LOG
```

**Core Monitoring:**

- **`recent_executions.sql`** - Lists recent dbt project executions with severity
- **`execution_errors.sql`** - Query ERROR logs to identify failures
- **`performance_metrics.sql`** - Query CPU and memory usage metrics
- **`trace_spans.sql`** - Query execution spans for timing analysis
- **`execution_summary.sql`** - Summarize executions by project with error counts

**Advanced Use Cases:**

- **`alert_failures.sql`** - Alert trigger for execution failures (returns error count)
- **`performance_regression.sql`** - Week-over-week performance comparison
- **`resource_usage.sql`** - CPU and memory consumption by project
- **`audit_trail.sql`** - Complete execution audit trail for compliance

### Event Table Structure

Event tables follow the [OpenTelemetry data model](https://opentelemetry.io/) with these key
columns:

| Column                  | Description                                                                 |
| ----------------------- | --------------------------------------------------------------------------- |
| **TIMESTAMP**           | UTC timestamp when event was created (end of time span for span events)     |
| **START_TIMESTAMP**     | For span events, the start of the time span                                 |
| **TRACE**               | Tracing context with `trace_id` and `span_id`                               |
| **RESOURCE_ATTRIBUTES** | Source identification: database, schema, user, warehouse, etc.              |
| **SCOPE**               | Event scopes (e.g., class names for logs)                                   |
| **RECORD_TYPE**         | Event type: `LOG`, `SPAN`, `SPAN_EVENT`, `EVENT`, `METRIC`                  |
| **RECORD**              | JSON object with record-specific data (severity, metric type, span details) |
| **RECORD_ATTRIBUTES**   | Event metadata set by Snowflake or code                                     |
| **VALUE**               | Actual log message, metric value, or null for spans                         |

### Best Practices

**Performance Optimization:**

- **Always filter by TIMESTAMP** to limit scanned data (reduces cost)
- **Use RESOURCE_ATTRIBUTES** for efficient filtering by project/database/schema
- **Archive old event table data** (>90 days) to separate tables

**Monitoring Strategy:**

1. Set event tables at **DATABASE level**, not account or schema
2. Configure appropriate log/trace/metric levels per schema
3. Always filter by `TIMESTAMP` to avoid scanning large event tables
4. Use `snow.executable.type = 'DBT_PROJECT'` to isolate dbt events
5. Leverage `RESOURCE_ATTRIBUTES` for filtering by project/database/schema
6. Monitor ERROR severity logs for immediate alerts
7. Use SPAN records to analyze execution timing and bottlenecks

**Alerting Priorities:**

- **High**: Any ERROR in execution, execution >2x historical avg, warehouse credit anomalies
- **Medium**: WARNING logs, test/model failures on critical models, performance trending down
- **Low**: INFO logs, scheduled job confirmations, performance metrics for analysis

### Troubleshooting

| Issue                   | Solution                                                       |
| ----------------------- | -------------------------------------------------------------- |
| No events captured      | Verify event table set at DATABASE level with `ALTER DATABASE` |
| Too many events         | Adjust `LOG_LEVEL`/`TRACE_LEVEL`/`METRIC_LEVEL` per schema     |
| Slow monitoring queries | Always filter by TIMESTAMP first; consider archiving old data  |
| Missing metrics         | Set `METRIC_LEVEL = 'ALL'` for schema                          |
| Missing traces          | Set `TRACE_LEVEL = 'ALWAYS'` for schema                        |
| Cannot see project name | Verify `snow.executable.type = 'DBT_PROJECT'` filter           |

## Supported dbt Commands

| Command  | Workspaces          | EXECUTE DBT PROJECT | snow dbt execute |
| -------- | ------------------- | ------------------- | ---------------- |
| build    | ✅                  | ✅                  | ✅               |
| run      | ✅                  | ✅                  | ✅               |
| test     | ✅                  | ✅                  | ✅               |
| compile  | ✅                  | ✅                  | ✅               |
| seed     | ✅                  | ✅                  | ✅               |
| snapshot | ✅                  | ✅                  | ✅               |
| deps     | ✅ (workspace only) | ❌                  | ❌               |

## Team Collaboration

**Flexibility:** Team members can use different development approaches simultaneously:

- Developer A: dbt Projects on Snowflake workspaces
- Developer B: dbt Cloud
- Developer C: Local VS Code with dbt CLI
- All check into the same Git repository

## Key Commands

| Command                         | Purpose                     |
| ------------------------------- | --------------------------- |
| `snow dbt deploy <name>`        | Deploy project to Snowflake |
| `snow dbt execute <name> run`   | Run dbt models              |
| `snow dbt execute <name> build` | Run and test models         |
| `snow dbt execute <name> test`  | Run tests only              |
| `snow dbt list`                 | List all dbt projects       |

## Troubleshooting

For setup and deployment issues, see `references/SETUP.md`.

For monitoring issues, see the Troubleshooting table in the Event Table Monitoring section above.

## Related Skills

**Complementary Observability:**

- `dbt-artifacts` skill - For cross-platform execution logging and historical trend analysis

**When to use both together:**

- **dbt Projects on Snowflake** for real-time monitoring with OpenTelemetry event tables
- **dbt Artifacts** for cross-platform historical analysis and long-term metrics

**When to use one vs the other:**

- Use **dbt Projects on Snowflake** alone if you exclusively run dbt within Snowflake
- Use **dbt Artifacts** alone if you run dbt outside Snowflake (dbt Cloud, Airflow, local)
- Use **both** for comprehensive enterprise monitoring (real-time + historical)

---

## Resources

### Local Files

- **Monitoring Scripts**: `scripts/` - Ready-to-use parameterized SQL scripts for monitoring
  - Core Monitoring: `recent_executions.sql`, `execution_errors.sql`, `performance_metrics.sql`,
    `trace_spans.sql`, `execution_summary.sql`
  - Advanced Monitoring: `alert_failures.sql`, `performance_regression.sql`, `resource_usage.sql`,
    `audit_trail.sql`
- **Setup Guide**: `references/SETUP.md` - Complete step-by-step setup including event table
  configuration and task scheduling

### Official Documentation

- dbt Projects Documentation:
  https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake
- Monitoring Guide:
  https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability
