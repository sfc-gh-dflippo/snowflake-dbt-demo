# Snowflake CLI Variables & Templating

Complete guide to variable substitution and templating in Snowflake CLI.

**Reference:** [Snowflake CLI - Using variables for SQL templates](https://docs.snowflake.com/en/developer-guide/snowflake-cli/sql/execute-sql)

---

## Three Types of Variables

### 1. Bash Variables (Shell Expansion)

Bash variables are expanded by your shell **before** the command reaches Snowflake CLI.

```bash
# Define bash variables
DB="PROD_DB"
SCHEMA="SALES"

# Bash expands ${var} before snow cli sees it
snow sql -c default -i <<EOF
SELECT * FROM ${DB}.${SCHEMA}.orders;
EOF
```

**Use for:** Connection names, file paths, environment selection, control flow

---

### 2. Snowflake CLI Standard Syntax `<% %>`

Default client-side templating syntax. Enabled by default, resolved by Snowflake CLI before sending to Snowflake.

```bash
# Single-line with <% %> syntax
snow sql -c default -q "SELECT * FROM <% db %>.<% schema %>.orders" \
  -D db=PROD_DB -D schema=SALES

# Heredoc with <% %> variables (default syntax)
snow sql -c default -i -D db=PROD_DB -D schema=SALES <<EOF
SELECT * FROM <% db %>.<% schema %>.orders
WHERE created_date >= '<% start_date %>';
EOF
```

**Use for:** SQL templating with `snow sql` command (recommended default)

---

### 3. Jinja Syntax `{{ }}`

May be explicitly enabled with `--enable-templating JINJA`. Used automatically for `snow stage execute` with SQL files.

```bash
# Enable Jinja templating for snow sql
snow sql --enable-templating JINJA -c default \
  -q "SELECT * FROM {{ db }}.{{ schema }}.orders" \
  -D db=PROD_DB -D schema=SALES

# Jinja is DEFAULT for stage execute (no flag needed)
snow stage execute @my_stage/script.sql -c default \
  -D db=PROD_DB \
  -D schema=SALES
```

**Use for:** 
- SQL files executed from stage with `snow stage execute`
- When you prefer Jinja syntax (must enable explicitly)

---

## Template Syntax Control

Control which syntaxes are enabled with `--enable-templating`:

```bash
# STANDARD (default): <% var %> only
snow sql -q "SELECT <% var %>" -D var=value

# JINJA: {{ var }} only  
snow sql --enable-templating JINJA -q "SELECT {{ var }}" -D var=value

# LEGACY: &var or &{var} (SnowSQL compatibility)
snow sql --enable-templating LEGACY -q "SELECT &var" -D var=value

# ALL: Enable all syntaxes
snow sql --enable-templating ALL -q "SELECT <% var %> {{ var }}" -D var=value

# NONE: Disable templating (useful for queries containing template-like text)
snow sql --enable-templating NONE -q "SELECT '<% not_a_var %>'"
```

**Default:** `STANDARD` and `LEGACY` are enabled by default

---

## Combining Variable Types

```bash
# Bash for environment, <% %> for SQL
ENV="prod"
CONNECTION="${ENV}_connection"

snow sql -c ${CONNECTION} -i -D db=PROD_DB -D schema=SALES <<EOF
-- Use <% %> syntax (default)
CREATE TABLE <% db %>.<% schema %>.new_table AS
SELECT * FROM <% db %>.<% schema %>.source_table;
EOF
```

---

## Stage Execute (Jinja Default)

When using `snow stage execute` for SQL files, Jinja is the default template syntax:

```bash
# Upload SQL file with Jinja templates
cat > script.sql <<EOF
CREATE TABLE {{ db }}.{{ schema }}.my_table (
    id INT,
    name STRING
);
INSERT INTO {{ db }}.{{ schema }}.my_table VALUES (1, 'test');
EOF

snow stage copy script.sql @my_stage/ -c default

# Execute with Jinja variables (default for stage execute)
snow stage execute @my_stage/script.sql -c default \
  -D db=PROD_DB \
  -D schema=SALES
```

---

## Best Practices

### Use Bash variables for:
- ✅ Connection names: `-c ${CONNECTION}`
- ✅ File paths: `-f ${SCRIPT_DIR}/script.sql`
- ✅ Environment selection: `${ENV}_warehouse`
- ✅ Shell control flow: `if/then/else`

### Use `<% %>` Standard Syntax for:
- ✅ Inline SQL with `snow sql -q`
- ✅ Heredoc SQL with `snow sql -i`
- ✅ Default behavior (no flag needed)

### Use `{{ }}` Jinja for:
- ✅ SQL files executed with `snow stage execute` (automatic)
- ✅ Client script templating with `--enable-templating JINJA`
- ✅ When you prefer Jinja syntax over `<% %>`

### Always quote string values:
```bash
# ✅ CORRECT: Strings in quotes
snow sql -D name="'John'" -D date="'2024-01-01'"

# ❌ WRONG: No quotes for strings
snow sql -D name=John -D date=2024-01-01
```

---

## Comparison Table

| Feature | Bash Variables | Standard `<% %>` | Jinja `{{ }}` |
|---------|---------------|------------------|---------------|
| **Resolved by** | Shell | Snowflake CLI | Snowflake CLI |
| **When resolved** | Before CLI runs | Before sent to Snowflake | Before sent to Snowflake |
| **Define with** | `VAR=value` | `-D var=value` | `-D var=value` |
| **Use in command** | `${VAR}` | `<% var %>` | `{{ var }}` |
| **Default enabled** | Always | Yes | No (except stage execute) |
| **Enable flag** | N/A | `--enable-templating STANDARD` | `--enable-templating JINJA` |
| **Best for** | Shell operations | SQL templating | SQL files on stage |

---

## Common Patterns

### Multi-Environment Deployment

```bash
#!/bin/bash

# Environment configuration
ENV="${1:-dev}"  # Default to dev

case $ENV in
  dev)
    DB="DEV_DB"
    SCHEMA="DEV_SCHEMA"
    WAREHOUSE="DEV_WH"
    ;;
  prod)
    DB="PROD_DB"
    SCHEMA="PROD_SCHEMA"
    WAREHOUSE="PROD_WH"
    ;;
esac

# Deploy using variables
snow sql -c default -i -D db=$DB -D schema=$SCHEMA <<EOF
USE WAREHOUSE <% warehouse %>;
CREATE OR REPLACE TABLE <% db %>.<% schema %>.my_table AS
SELECT * FROM <% db %>.<% schema %>.source_table;
EOF
```

### Dynamic SQL Generation

```bash
# Generate table list dynamically
TABLES=$(snow sql -c default -q "SHOW TABLES IN SCHEMA MY_DB.MY_SCHEMA" --format json | jq -r '.[].name')

# Process each table
for TABLE in $TABLES; do
  snow sql -c default -i -D table=$TABLE <<EOF
  GRANT SELECT ON TABLE MY_DB.MY_SCHEMA.<% table %> TO ROLE ANALYST;
  EOF
done
```

### CI/CD Integration

```bash
# GitHub Actions example
snow sql -c default -i \
  -D database="${GITHUB_REF##*/}_DB" \
  -D schema="PUBLIC" <<EOF
CREATE OR REPLACE VIEW <% database %>.<% schema %>.my_view AS
SELECT * FROM <% database %>.<% schema %>.source;
EOF
```

---

## Troubleshooting

### Variable Not Substituted

**Problem:** Variable appears literally in SQL

```sql
-- Output: SELECT * FROM <% db %>.orders
```

**Solutions:**
1. Check syntax matches enabled template type
2. Verify `-D` flag is before SQL
3. Ensure proper quoting for string values

### Syntax Conflicts

**Problem:** Query contains template-like text

```bash
# This fails if templating enabled
snow sql -q "SELECT '<% not_a_variable %>'"
```

**Solution:** Disable templating
```bash
snow sql --enable-templating NONE -q "SELECT '<% not_a_variable %>'"
```

### Stage Execute Variables

**Problem:** Variables not working with `snow stage execute`

**Solution:** Use Jinja `{{ }}` syntax (default for stage execute)
```bash
# ✅ CORRECT
snow stage execute @stage/script.sql -D var=value

# In script.sql: SELECT * FROM {{ var }}.table
```

---

## Quick Reference

```bash
# Bash variables (shell expansion)
DB="PROD"
snow sql -c default -q "USE ${DB}_DATABASE"

# Standard syntax (default)
snow sql -c default -q "USE <% db %>" -D db=PROD

# Jinja syntax (explicit)
snow sql --enable-templating JINJA -c default -q "USE {{ db }}" -D db=PROD

# Stage execute (Jinja automatic)
snow stage execute @stage/script.sql -D db=PROD

# Disable templating
snow sql --enable-templating NONE -q "SELECT '<% literal %>'"

# String values need quotes
snow sql -D name="'John'" -D date="'2024-01-01'"
```

---

**Related Documentation:**
- `STAGE_OPERATIONS.md` - Stage management and execution
- **[snowflake-connections](../../snowflake-connections/SKILL.md)** - Connection configuration and authentication


