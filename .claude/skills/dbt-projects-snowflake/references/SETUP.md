# dbt Projects on Snowflake Setup

## Complete Setup Instructions

This guide walks through setting up dbt Projects on Snowflake from beginning to end.

### Prerequisites

1. **Snowflake Account**
   - Account with ACCOUNTADMIN permissions for initial setup
   - Personal database enabled (default for new accounts)

2. **Git Repository**
   - GitHub, GitLab, or Azure DevOps repository
   - Personal Access Token (PAT) for authentication

### Step 1: Enable Personal Database

```sql
ALTER ACCOUNT SET ENABLE_PERSONAL_DATABASE = TRUE;
```

### Step 2: Create External Access Integration

For `dbt deps` to work, allow external access to dbt packages:

```sql
-- Create NETWORK RULE
CREATE OR REPLACE NETWORK RULE dbt_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    'hub.getdbt.com',
    'codeload.github.com'
  );

-- Create EXTERNAL ACCESS INTEGRATION
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dbt_ext_access
  ALLOWED_NETWORK_RULES = (dbt_network_rule)
  ENABLED = TRUE;
```

### Step 3: Create Git API Integration

**GitHub:**
```sql
CREATE OR REPLACE API INTEGRATION git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = (
    'https://github.com/',
    'https://github.com/organization/'
  );
```

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

---

## Event Table Monitoring Configuration (Optional but Recommended)

Monitor dbt Projects execution using event tables that capture telemetry data (logs, traces, metrics) via the [OpenTelemetry data model](https://opentelemetry.io/).

### Critical Pattern: Database-Level Configuration

Always set event tables at the **DATABASE** level (not schema, not account-wide):

```sql
-- Step 1: Create event table (can be in different database)
CREATE EVENT TABLE IF NOT EXISTS MY_LOGGING_DATABASE.MY_LOGGING_SCHEMA.EVENT_LOG;

-- Step 2: Set event table where dbt Projects are deployed at DATABASE level
ALTER DATABASE MY_DBT_PROJECT_DATABASE 
  SET EVENT_TABLE = MY_LOGGING_DATABASE.MY_LOGGING_SCHEMA.EVENT_LOG;

-- Step 3: Configure logging levels for the schema where dbt Project is deployed
ALTER SCHEMA MY_DBT_PROJECT_DATABASE.MY_DBT_PROJECT_SCHEMA SET LOG_LEVEL = 'INFO';
ALTER SCHEMA MY_DBT_PROJECT_DATABASE.MY_DBT_PROJECT_SCHEMA SET TRACE_LEVEL = 'ALWAYS';
ALTER SCHEMA MY_DBT_PROJECT_DATABASE.MY_DBT_PROJECT_SCHEMA SET METRIC_LEVEL = 'ALL';
```

**Why DATABASE level?**
- Captures all dbt Project executions in that database
- Avoids account-wide noise
- Provides project-level isolation

### Verify Event Capture

After configuration, verify events are being captured:

```sql
-- Check recent events
SELECT 
    TIMESTAMP,
    RESOURCE_ATTRIBUTES['snow.executable.name']::VARCHAR AS project_name,
    RECORD_TYPE,
    RECORD['severity_text']::VARCHAR AS severity,
    VALUE::VARCHAR AS message
FROM MY_LOGGING_DATABASE.MY_LOGGING_SCHEMA.EVENT_LOG
WHERE RESOURCE_ATTRIBUTES['snow.executable.type']::VARCHAR = 'DBT_PROJECT'
  AND TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC
LIMIT 10;
```

See `SKILL.md` for complete monitoring guide with ready-to-use SQL scripts, best practices, and troubleshooting.

---

## Common Issues

**SSH/Network Issues:**
- Ensure external access integration is created
- Check network rules include required hosts

**Authentication Failures:**
- Verify PAT has correct scopes
- Check API integration is created

**Package Installation Issues:**
- Run `dbt deps` in workspace before deployment
- Ensure external access integration is enabled

---

## Optional: Schedule Automated Runs

Create a Snowflake task to run dbt on a schedule:

```sql
CREATE OR REPLACE TASK my_dbt_daily_task
  WAREHOUSE = 'MY_WAREHOUSE'
  SCHEDULE = 'USING CRON 0 6 * * * UTC'  -- Daily at 6 AM UTC
AS
  EXECUTE DBT PROJECT MY_DATABASE.MY_SCHEMA.MY_DBT_PROJECT
    args='build';

-- Enable the task
ALTER TASK my_dbt_daily_task RESUME;
```

Customize:
- Task name (`my_dbt_daily_task`)
- Warehouse name
- Schedule (CRON expression)
- Database, schema, and project name
- dbt command arguments (default: `build`)
