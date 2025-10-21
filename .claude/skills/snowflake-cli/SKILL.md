---
name: Snowflake CLI
description: Execute SQL, manage Snowflake objects, deploy applications, and orchestrate data pipelines using the Snowflake CLI (snow) command. Use this skill when you need to run SQL scripts, deploy Streamlit apps, execute Snowpark procedures, manage stages, or automate Snowflake operations from CI/CD pipelines.
---

# Snowflake CLI (snow)

Execute SQL, manage Snowflake objects, and deploy applications using the Snowflake CLI command-line tool.

## Quick Start

**Three Main Use Cases:**

1. **SQL Execution** - Run queries and scripts
2. **Deployments** - Deploy Streamlit apps and Snowpark objects
3. **Object Management** - Create, list, and manage database objects

## SQL Execution

```bash
# Inline query
snow sql -q "SELECT * FROM my_table" -c default

# Execute file
snow sql -f script.sql -c default

# With variables (Jinja {{ }} or <% %> syntax)
snow sql -q "SELECT * FROM {{db}}.{{schema}}.table" \
  -D db=PROD_DB -D schema=SALES -c default
```

## Variables & Templating

**Three Syntax Types:**

1. **Bash Variables** - Shell expansion (environment control)
   ```bash
   DB="PROD_DB" && snow sql -q "SELECT * FROM ${DB}.orders"
   ```

2. **Jinja Syntax** - `{{ var }}` (recommended for SQL files)
   ```bash
   snow stage execute @my_stage/script.sql -D db=PROD_DB
   ```

3. **Standard Syntax** - `<% var %>` (default for snow sql)
   ```bash
   snow sql -q "SELECT * FROM <% db %>.orders" -D db=PROD_DB
   ```

See `VARIABLES_TEMPLATING.md` for complete guide.

## Deployments

### Streamlit Apps
```bash
snow streamlit deploy --replace -c default
snow streamlit list -c default
snow streamlit get-url my_app -c default
```

### Snowpark (UDFs/Procedures)
```bash
snow snowpark build -c default
snow snowpark deploy --replace -c default
```

### Project Creation
See `PROJECT_CREATION.md` for:
- How to create app projects
- Streamlit project structures
- Snowpark object projects

## Stage Operations

```bash
# Upload/download files
snow stage copy ./local/ @my_stage/ -c default
snow stage copy @my_stage/ ./downloads/ -c default

# Execute SQL/Python from stage
snow stage execute @my_stage/script.sql -c default
snow stage execute @my_stage/script.py -c default
```

## Object Management

```bash
# List objects
snow object list warehouse -c default
snow object list table -c default

# Describe object
snow object describe table my_table -c default

# Create object
snow object create warehouse my_wh --size SMALL -c default
```

## Connection Configuration

Configure `~/.snowflake/connections.toml`:
```toml
[default]
account = your_account
user = your_user
password = your_password
warehouse = COMPUTE_WH
database = MY_DB
```

See `references/CONNECTION_CONFIG.md` for authentication methods.

## Resources

- `VARIABLES_TEMPLATING.md` - Variable substitution guide (coming soon)
- `PROJECT_CREATION.md` - Creating apps and objects (coming soon)
- `STAGE_OPERATIONS.md` - Stage file management (coming soon)
- `references/CONNECTION_CONFIG.md` - Connection setup
