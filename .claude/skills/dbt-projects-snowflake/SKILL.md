---
name: dbt Projects on Snowflake
description: Deploy, manage, execute, and monitor dbt projects natively within Snowflake using dbt PROJECT objects and event tables. Use this skill when you want to set up dbt development workspaces, deploy projects to Snowflake, schedule automated runs, monitor execution with event tables, or enable team collaboration directly in Snowflake.
---

# dbt Projects on Snowflake

Deploy, manage, and monitor dbt projects natively within Snowflake using web-based workspaces, schema-level DBT PROJECT objects, and comprehensive event table telemetry.

## Quick Start

**Three Ways to Use dbt Projects:**

1. **Snowsight Workspaces** - Web-based IDE for interactive development
2. **DBT PROJECT Objects** - Deployed projects for production execution
3. **Snowflake CLI** - Command-line deployment and execution

## Setup

### Prerequisites
- Snowflake account (ACCOUNTADMIN for initial setup)
- Personal database enabled (default for new accounts)
- External access integration for `dbt deps` (if using packages)
- Git API integration for repository access

## Complete Setup Steps

Execute the setup scripts in order with Snowflake CLI:

```bash
# Run setup scripts (requires ACCOUNTADMIN)
snow sql -f scripts/01_enable_personal_database.sql -c default
snow sql -f scripts/02_create_external_access.sql -c default
snow sql -f scripts/03_create_git_api_integration.sql -c default
```

### Step 1: Enable Personal Database

Run **scripts/01_enable_personal_database.sql** to enable personal database feature.

### Step 2: Create External Access Integration

**scripts/02_create_external_access.sql**

For `dbt deps` to work, allow external access to dbt packages:
- Creates network rule for hub.getdbt.com and codeload.github.com
- Creates external access integration

### Step 3: Create Git API Integration

**scripts/03_create_git_api_integration.sql**

Connect to GitHub repositories:
- Update `API_ALLOWED_PREFIXES` with your organization URLs before running

### Step 4: Create Workspace in Snowsight

1. Navigate to Projects → My Workspace
2. Click My Workspace → Create Workspace → From Git repository
3. Enter:
   - Repository URL
   - API integration name
   - Authentication (PAT or OAuth)

### Step 5: Configure profiles.yml

```yaml
my_dbt_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: ""  # Uses current account context
      user: ""     # Uses current user context
      warehouse: MY_WAREHOUSE
      database: MY_DATABASE
      schema: MY_SCHEMA
      role: MY_ROLE
```

### Step 6: Deploy as DBT PROJECT Object

Use Deploy button in workspace or Snowflake CLI:

```bash
snow dbt deploy my_project --source .
```

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

**scripts/execute_dbt_project.sql**

Execute with variables:
```bash
snow sql -f scripts/execute_dbt_project.sql -c default \
  -D db=MY_DB -D schema=MY_SCHEMA -D project=MY_PROJECT
```

Or execute directly in SQL:
```sql
EXECUTE DBT PROJECT <db>.<schema>.<project> args='build';
EXECUTE DBT PROJECT <db>.<schema>.<project> args='build --full-refresh';
EXECUTE DBT PROJECT <db>.<schema>.<project> args='build --select tag:gold';
```

## Scheduling & Automation

**scripts/create_scheduled_task.sql**

Create a daily scheduled task to run dbt:

```bash
# Update warehouse, schedule, and project path in the file, then run:
snow sql -f scripts/create_scheduled_task.sql -c default
```

The script creates a task that runs daily at 6 AM UTC. Customize as needed:
- Warehouse name
- Schedule (CRON expression)
- Project database/schema/name
- dbt command arguments

## Event Table Monitoring

For comprehensive monitoring guidance including event table setup, monitoring queries, best practices, and troubleshooting, see `references/MONITORING.md`.

Key monitoring capabilities:
- Real-time telemetry via event tables (logs, traces, metrics)
- OpenTelemetry data model structure
- Pre-built monitoring queries
- Performance optimization patterns
- Alerting strategies

## Supported dbt Commands

| Command | Workspaces | EXECUTE DBT PROJECT | snow dbt execute |
|---------|------------|-------------------|------------------|
| build   | ✅         | ✅                | ✅               |
| run     | ✅         | ✅                | ✅               |
| test    | ✅         | ✅                | ✅               |
| compile | ✅         | ✅                | ✅               |
| seed    | ✅         | ✅                | ✅               |
| snapshot| ✅         | ✅                | ✅               |
| deps    | ✅ (workspace only) | ❌        | ❌               |

## Team Collaboration

**Flexibility:** Team members can use different development approaches simultaneously:
- Developer A: dbt Projects on Snowflake workspaces
- Developer B: dbt Cloud
- Developer C: Local VS Code with dbt CLI
- All check into the same Git repository

## Key Commands

| Command | Purpose |
|---------|---------|
| `snow dbt deploy <name>` | Deploy project to Snowflake |
| `snow dbt execute <name> run` | Run dbt models |
| `snow dbt execute <name> build` | Run and test models |
| `snow dbt execute <name> test` | Run tests only |
| `snow dbt list` | List all dbt projects |

## Troubleshooting

**Setup Issues:**
- SSH/Network Issues: Ensure external access integration is created
- Authentication Failures: Verify PAT has correct scopes
- Package Installation: Run `dbt deps` in workspace before deployment

**Monitoring Issues:**
- No events captured: Verify event table set at DATABASE level
- Too many events: Adjust LOG_LEVEL/TRACE_LEVEL/METRIC_LEVEL
- Slow queries: Always filter by TIMESTAMP first

## Related Skills

**Complementary Observability:**
- **[dbt-artifacts](../dbt-artifacts/SKILL.md)** - For cross-platform execution logging and historical trend analysis

**When to use both together:**
- **dbt Projects on Snowflake** for real-time monitoring with OpenTelemetry event tables
- **dbt Artifacts** for cross-platform historical analysis and long-term metrics

**When to use one vs the other:**
- Use **dbt Projects on Snowflake** alone if you exclusively run dbt within Snowflake
- Use **dbt Artifacts** alone if you run dbt outside Snowflake (dbt Cloud, Airflow, local)
- Use **both** for comprehensive enterprise monitoring (real-time + historical)

---

## Resources

- **Setup Scripts**: `scripts/` - SQL scripts for setup, execution, and scheduling
- **Setup Guide**: `references/SETUP.md` - Complete setup and monitoring configuration
- **Monitoring Guide**: `references/MONITORING.md` - Event table monitoring guide
- dbt Projects Documentation: https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake
- Monitoring Guide: https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability
