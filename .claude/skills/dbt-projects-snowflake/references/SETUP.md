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

## Team Collaboration

Teams can use different development approaches simultaneously:
- Some developers: dbt Projects on Snowflake workspaces
- Some developers: dbt Cloud IDE
- Some developers: VS Code + local dbt CLI
- All: Check code into same Git repository
