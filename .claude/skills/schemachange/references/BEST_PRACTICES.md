# Schemachange Best Practices

Comprehensive guidance for using schemachange effectively in Snowflake projects.

## Script Types & When to Use Them

### Versioned Scripts (V__)

**Purpose:** One-time structural changes that should never be re-executed

**Keeping the version numbers unique can be a challenge for teams so we only use V__ scripts when we are unable to use R__ scripts.**

**Use for:**
- `CREATE TABLE` (new tables)
- `ALTER TABLE ADD COLUMN` (structural changes)
- `CREATE SCHEMA` / `CREATE DATABASE`
- One-time data migrations
- Any change that should run exactly once

**Format:** `V<major>.<minor>.<patch>__<description>.sql`

**Examples:**
```sql
-- V1.0.0__initial_setup.sql
CREATE SCHEMA IF NOT EXISTS RECONCILIATION;

-- V1.1.0__create_base_tables.sql
CREATE TABLE IF NOT EXISTS SOURCE_CONNECTIONS (
    CONNECTION_ID NUMBER AUTOINCREMENT PRIMARY KEY,
    CONNECTION_NAME VARCHAR(255) NOT NULL UNIQUE,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- V1.2.0__add_customer_columns.sql
ALTER TABLE CUSTOMERS ADD COLUMN EMAIL VARCHAR(255);
ALTER TABLE CUSTOMERS ADD COLUMN PHONE VARCHAR(20);
```

**✅ DO:**
- Use semantic versioning (major.minor.patch)
- Use `IF NOT EXISTS` for safety during debugging
- Group related changes logically
- Include comprehensive comments
- Test thoroughly before deployment (can't be re-run)

**❌ DON'T:**
- Modify scripts after they've been deployed
- Use `CREATE OR REPLACE` (not idempotent)
- Mix unrelated changes in one script
- Skip version numbers in sequence
- Use the same version number on two different scripts

---

### Repeatable Scripts (R__)

**Purpose:** Objects that can be safely recreated or altered on every change. 

**This is our preferred script type whenever we can write a script that can be written declaratively.**

**Use for:**
- Views
- Functions
- Procedures
- Dynamic tables
- File formats
- Stages
- Tasks

**Format:** `R__<description>.sql` or `R__Phase_<N>_<description>.sql` (for ordering)

**Key Principle:** Scripts run whenever new or modified (checksum-based detection)

#### Preferred: CREATE OR ALTER

**Use when available** - Preserves metadata, tags, policies, and grants:

```sql
-- R__Phase_01_create_views.sql
USE SCHEMA RECONCILIATION;

-- ✅ CREATE OR ALTER preserves all object metadata
CREATE OR ALTER VIEW VW_CUSTOMER_SUMMARY AS
SELECT 
    CUSTOMER_ID,
    COUNT(*) AS ORDER_COUNT,
    SUM(TOTAL_AMOUNT) AS LIFETIME_VALUE
FROM ORDERS
GROUP BY CUSTOMER_ID;

CREATE OR ALTER VIEW VW_PRODUCT_METRICS AS
SELECT 
    PRODUCT_ID,
    AVG(UNIT_PRICE) AS AVG_PRICE,
    SUM(QUANTITY) AS TOTAL_SOLD
FROM ORDER_ITEMS
GROUP BY PRODUCT_ID;

-- ✅ Groups related views together
-- ✅ Can be modified freely
-- ✅ Maintains row access policies, column masking, tags
```

#### Alternative: CREATE OR REPLACE

**Use only when CREATE OR ALTER is not available:**

```sql
-- R__Phase_02_streams.sql
USE SCHEMA RECONCILIATION;

-- ✅ Streams require CREATE OR REPLACE (CREATE OR ALTER not available)
CREATE OR REPLACE STREAM CUSTOMER_CHANGES
ON TABLE CUSTOMERS
APPEND_ONLY = FALSE;

CREATE OR REPLACE STREAM ORDER_CHANGES
ON TABLE ORDERS
APPEND_ONLY = FALSE;

-- ⚠️ Note: This recreates the stream (resets offset)
```

**Supported by CREATE OR ALTER:**
- AUTHENTICATION POLICY
- DATABASE (parameters only)
- DATABASE ROLE
- **DYNAMIC TABLE** ✅
- FILE FORMAT
- FUNCTION
- PROCEDURE
- ROLE
- SCHEMA (parameters only)
- STAGE
- **TABLE** ✅ (for incremental updates)
- TASK
- **VIEW** ✅
- WAREHOUSE

**Requires CREATE OR REPLACE:**
- STREAM
- PIPE
- SEQUENCE

**✅ DO:**
- Use naming conventions for execution order (`R__Phase_01_`, `R__Phase_02_`)
- Group related objects in single scripts
- Prefer `CREATE OR ALTER` to preserve metadata
- Make scripts fully idempotent
- Test modifications with `--dry-run` first

**❌ DON'T:**
- Use version numbers in filenames
- Use `CREATE OR REPLACE` when `CREATE OR ALTER` is available
- Forget to `ALTER TASK ... SUSPEND` before modifying tasks

---

### Always Scripts (A__)

**Purpose:** Scripts that run on every deployment, regardless of changes

**Use for:**
- Permission grants/revokes
- Configuration updates
- Cache refreshes
- Administrative tasks

**Format:** `A__<description>.sql` or `A__Phase_<N>_<description>.sql` (for ordering)

**Examples:**
```sql
-- A__Phase_01_refresh_permissions.sql
GRANT SELECT ON ALL TABLES IN SCHEMA RECONCILIATION TO ROLE ANALYST;
GRANT SELECT ON FUTURE TABLES IN SCHEMA RECONCILIATION TO ROLE ANALYST;

-- A__Phase_02_update_config.sql
UPDATE CONFIG_TABLE 
SET LAST_DEPLOYMENT = CURRENT_TIMESTAMP()
WHERE CONFIG_KEY = 'DEPLOYMENT_STATUS';
```

**✅ DO:**
- Ensure scripts are truly idempotent
- Use for admin tasks that should always run
- Use naming conventions for execution order

**❌ DON'T:**
- Overuse (most scripts should be versioned or repeatable)
- Include expensive operations
- Assume specific state (always check first)

---

## Execution Order & Naming Conventions

**Execution sequence:**
1. Versioned scripts (V__) - in version order
2. Repeatable scripts (R__) - in alphabetical order
3. Always scripts (A__) - in alphabetical order

**Naming strategy for R__ and A__ scripts:**

```
R__Phase_01_file_formats.sql
R__Phase_01_utility_functions.sql
R__Phase_02_base_views.sql
R__Phase_02_base_tables.sql
R__Phase_03_aggregation_views.sql
R__Phase_04_reporting_views.sql
```

Benefits:
- Explicit control over execution order
- Clear dependencies between scripts
- Easy to understand sequence at a glance
- Consistent numbering allows insertions

---

## Idempotency Patterns

### Tables (Versioned Scripts)

```sql
-- ✅ Safe for re-running during debugging
CREATE TABLE IF NOT EXISTS CUSTOMERS (
    CUSTOMER_ID NUMBER AUTOINCREMENT PRIMARY KEY,
    NAME VARCHAR(255) NOT NULL
);

-- ❌ Not safe for re-running
CREATE TABLE CUSTOMERS (...);  -- Fails if exists
CREATE OR REPLACE TABLE CUSTOMERS (...);  -- Destroys data
```

### Views (Repeatable Scripts)

```sql
-- ✅ BEST: Preserves metadata
CREATE OR ALTER VIEW VW_SUMMARY AS SELECT ...;

-- ✅ OK: Simple recreation
CREATE OR REPLACE VIEW VW_SUMMARY AS SELECT ...;

-- ❌ Not idempotent
CREATE VIEW VW_SUMMARY AS SELECT ...;  -- Fails if exists
```

### Functions & Procedures (Repeatable Scripts)

```sql
-- ✅ BEST: Preserves grants and tags
CREATE OR ALTER FUNCTION CALCULATE_TOTAL(QTY NUMBER, PRICE NUMBER)
RETURNS NUMBER
AS
$$
    QTY * PRICE
$$;

-- ✅ OK: Simple recreation  
CREATE OR REPLACE FUNCTION CALCULATE_TOTAL(...)
RETURNS NUMBER
AS $$ ... $$;
```

### Tasks (Repeatable Scripts)

```sql
-- ✅ Must suspend before modifying
ALTER TASK IF EXISTS DAILY_REFRESH SUSPEND;

CREATE OR ALTER TASK DAILY_REFRESH
    WAREHOUSE = COMPUTE_WH
    SCHEDULE = 'USING CRON 0 2 * * * UTC'
AS
    CALL REFRESH_METRICS();

ALTER TASK DAILY_REFRESH RESUME;
```

---

## Variable Management

### Using Jinja Variables

```sql
-- In schemachange-config.yml:
vars:
  tgt_database: PRODUCTION_DB
  tgt_schema: ANALYTICS
  src_database: RAW_DB
  src_schema: INGESTION

-- In script:
USE SCHEMA {{ tgt_database }}.{{ tgt_schema }};

CREATE OR ALTER VIEW VW_CUSTOMER_SUMMARY AS
SELECT *
FROM {{ src_database }}.{{ src_schema }}.CUSTOMERS;
```

### Command-Line Variables

```bash
# Override config vars
schemachange deploy \
  --config-folder . \
  --vars '{"tgt_database":"STAGING_DB","env":"staging"}'
```

### Environment-Specific Configs

```yaml
# schemachange-config-dev.yml
vars:
  env: dev
  database: DEV_DB
  schema: DEV_SCHEMA

# schemachange-config-prod.yml
vars:
  env: prod
  database: PROD_DB
  schema: PROD_SCHEMA
```

---

## Transaction Handling

### Default Behavior

Schemachange runs each script in its own transaction:
- Success → COMMIT
- Error → ROLLBACK

### Autocommit Mode

```yaml
# schemachange-config.yml
autocommit: true  # Each statement commits immediately
```

**Use cases:**
- Scripts with multiple independent operations
- When you need statement-level commits

**Caution:** Reduces ability to rollback partial changes

---

## Error Handling & Recovery

### Handling Failed Deployments

**Check failure:**
```sql
SELECT * FROM <DATABASE>.SCHEMACHANGE.CHANGE_HISTORY
WHERE STATUS != 'Success'
ORDER BY INSTALLED_ON DESC
LIMIT 1;
```

**Recovery options:**

1. **Fix and redeploy** (versioned scripts):
   - Create new versioned script with fixes
   - Increment version number
   - Deploy again

2. **Fix and redeploy** (repeatable scripts):
   - Fix the script
   - Redeploy (checksum will differ, script reruns)

3. **Manual intervention:**
   - Fix issue manually in Snowflake
   - Mark script as successful in change history (if needed)

### Preventing Issues

```bash
# Always test first
schemachange deploy --dry-run --verbose

# Test in dev environment
schemachange deploy --config-folder . --vars '{"env":"dev"}'

# Then prod
schemachange deploy --config-folder . --vars '{"env":"prod"}'
```

---

## Multi-Environment Deployment

### Strategy 1: Separate Config Files

```bash
schemachange deploy --config-folder config/dev
schemachange deploy --config-folder config/staging  
schemachange deploy --config-folder config/prod
```

### Strategy 2: Environment Variables

```bash
export SNOWFLAKE_DATABASE=DEV_DB
export SNOWFLAKE_SCHEMA=DEV_SCHEMA
schemachange deploy --vars '{"database":"$SNOWFLAKE_DATABASE"}'
```

### Strategy 3: CI/CD with Vars

```yaml
# .github/workflows/deploy.yml
- name: Deploy to Dev
  run: |
    schemachange deploy --vars '{"env":"dev","database":"DEV_DB"}'

- name: Deploy to Prod
  if: github.ref == 'refs/heads/main'
  run: |
    schemachange deploy --vars '{"env":"prod","database":"PROD_DB"}'
```

---

## Testing & Validation

### Pre-Deployment Testing

```bash
# 1. Dry run
schemachange deploy --dry-run --verbose

# 2. Check which scripts would run
schemachange render migrations/R__views.sql

# 3. Deploy to dev
schemachange deploy --vars '{"env":"dev"}'

# 4. Validate in dev
snow sql -c dev -q "SELECT COUNT(*) FROM VW_CUSTOMER_SUMMARY"

# 5. Deploy to prod
schemachange deploy --vars '{"env":"prod"}'
```

### Post-Deployment Validation

```sql
-- Verify deployment
SELECT 
    VERSION,
    DESCRIPTION,
    SCRIPT_TYPE,
    STATUS,
    EXECUTION_TIME,
    INSTALLED_ON
FROM <DATABASE>.SCHEMACHANGE.CHANGE_HISTORY
WHERE INSTALLED_ON > DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
ORDER BY INSTALLED_ON DESC;

-- Check for failures
SELECT * 
FROM <DATABASE>.SCHEMACHANGE.CHANGE_HISTORY
WHERE STATUS != 'Success'
AND INSTALLED_ON > DATEADD(DAY, -7, CURRENT_TIMESTAMP());
```

---

## CI/CD Integration Patterns

### GitHub Actions Example

```yaml
name: Deploy Database Changes

on:
  push:
    branches: [main]
    paths:
      - 'migrations/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install schemachange
        run: pip install schemachange
      
      - name: Deploy to Production
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
          SNOWFLAKE_ROLE: ${{ secrets.SNOWFLAKE_ROLE }}
          SNOWFLAKE_DATABASE: ${{ secrets.SNOWFLAKE_DATABASE }}
          SNOWFLAKE_WAREHOUSE: ${{ secrets.SNOWFLAKE_WAREHOUSE }}
        run: |
          schemachange deploy \
            --config-folder . \
            --create-change-history-table \
            --verbose
```

---

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| Modified versioned script fails | Create new versioned script (never modify deployed V__ scripts) |
| Repeatable script doesn't re-run | Check if file actually changed (checksum-based detection) |
| Lost row access policies | Use `CREATE OR ALTER` instead of `CREATE OR REPLACE` |
| Task modification fails | Always `ALTER TASK ... SUSPEND` before modifying |
| Scripts run in wrong order | Use naming convention: `R__Phase_01_`, `R__Phase_02_` |
| Autocommit causes partial failures | Use default transaction mode (autocommit: false) |
| Deployment hangs | Check for locks in Snowflake; use `--verbose` to debug |

---

## Quick Reference

**✅ Best Practices Summary:**
- Use `V__` for one-time structural changes
- Use `R__` for objects that can be recreated
- Prefer `CREATE OR ALTER` over `CREATE OR REPLACE`
- Use naming conventions for execution order
- Always test with `--dry-run` first
- Never modify deployed `V__` scripts
- Keep scripts small and focused
- Document complex logic with comments
- Use Jinja variables for environment-specific values

**❌ Common Mistakes to Avoid:**
- Modifying versioned scripts post-deployment
- Using `CREATE OR REPLACE` when `CREATE OR ALTER` exists
- Skipping dry-run testing
- Mixing unrelated changes in one script
- Hardcoding environment-specific values
- Creating tables in repeatable scripts
- Forgetting to suspend tasks before modification

---

**Additional Resources:**
- [Schemachange Documentation](https://github.com/Snowflake-Labs/schemachange)
- [Snowflake CREATE OR ALTER Reference](https://docs.snowflake.com/en/sql-reference/sql/create-or-alter)
- [Snowflake Change Management Guide](https://docs.snowflake.com/en/user-guide/admin-change-management)


