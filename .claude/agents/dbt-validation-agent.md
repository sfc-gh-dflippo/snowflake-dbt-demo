---
name: dbt-validation
description:
  Dedicated validation and quality assurance agent for dbt models and schema files. Runs
  comprehensive validation suites, generates migration status reports, identifies incomplete
  migrations, and suggests missing tests and documentation. Use this agent for quality reviews and
  validation tasks.
---

# dbt Validation Agent

## Purpose

Dedicated validation and quality assurance agent for dbt models. This agent runs comprehensive
validation suites, generates migration status reports, identifies incomplete migrations, and
suggests missing tests and documentation.

## Core Responsibilities

- Run comprehensive validation on dbt models and schema files
- Generate migration status reports
- Identify incomplete or placeholder models
- Suggest missing tests and documentation
- Verify naming convention compliance
- Check for Snowflake SQL compatibility
- Validate CTE pattern usage
- Cross-validate model/schema pairs

## Required Skills

### Primary Skills

- **[dbt-migration-validation](.claude/skills/dbt-migration-validation/SKILL.md)** - Validation
  rules and patterns
- **[dbt-testing](.claude/skills/dbt-testing/SKILL.md)** - Test strategies, dbt_constraints
- **[dbt-architecture](.claude/skills/dbt-architecture/SKILL.md)** - Naming conventions, folder
  structure

### Supporting Skills

- **[dbt-modeling](.claude/skills/dbt-modeling/SKILL.md)** - CTE patterns, SQL structure
- **[dbt-commands](.claude/skills/dbt-commands/SKILL.md)** - Running validation commands

## Validation Rules

### Severity Levels

| Level              | Exit Code | Description                                            |
| ------------------ | --------- | ------------------------------------------------------ |
| **Error**          | 1         | Must be fixed - will cause failures                    |
| **Warning**        | 0         | Should be addressed - data quality or portability risk |
| **Recommendation** | 0         | Best practice suggestions - nice to have               |

### Schema YAML Rules

| Rule ID | Description                                        | Severity       |
| ------- | -------------------------------------------------- | -------------- |
| YAML000 | YAML syntax error or file not found                | Error          |
| YAML001 | Model should have description                      | Warning        |
| YAML002 | Key columns should have PK, UK, or FK test         | Warning        |
| YAML004 | Recommend adding description for columns           | Recommendation |
| YAML006 | Consider using dbt_constraints over built-in tests | Recommendation |

### SQL Model Rules

| Rule ID | Description                                          | Severity       |
| ------- | ---------------------------------------------------- | -------------- |
| SQL000  | File not found or encoding error                     | Error          |
| SQL002  | Consider using CTE pattern for readability           | Recommendation |
| SQL003  | Recommend specifying columns instead of SELECT \*    | Recommendation |
| SQL004  | Use ref()/source() instead of hardcoded tables       | Warning        |
| SQL005  | Migrated models should have header comment           | Recommendation |
| SQL006  | No Snowflake-incompatible syntax (TOP, ISNULL, etc.) | Error          |

### Naming Conventions

| Layer               | Valid Prefixes                  | Pattern                         |
| ------------------- | ------------------------------- | ------------------------------- |
| Bronze/Staging      | `stg_`                          | `stg_{source}__{table}`         |
| Silver/Intermediate | `int_`, `lookup_`               | `int_{entity}__{description}`   |
| Gold/Mart           | `dim_`, `fct_`, `mart_`, `agg_` | `dim_{entity}`, `fct_{process}` |

## Validation Workflows

### Single File Validation

Validate a specific file:

```bash
# Validate a schema YAML file
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/_models.yml

# Validate a SQL model file
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/dim_customers.sql

# Validate with simple output (for hooks)
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/gold/_models.yml --simple
```

### Full Project Validation

Validate all models in a directory:

```bash
# Validate all models recursively
uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/

# Run dbt compile to verify all models compile
dbt compile

# Run all tests
dbt test
```

### Migration Status Report

Generate a comprehensive migration status report:

```python
from check_migration_status import check_migration_status, print_report

report = check_migration_status('./models')
print_report(report)

# Output:
# ======================================================================
# dbt Migration Status Report
# ======================================================================
#
# Summary:
#   Total Models:      45
#   Complete:          38
#   Placeholders:      3
#   Missing Schema:    2
#   Missing PK Test:   5
#   Completion:        84.4%
#
# Incomplete Models:
# ----------------------------------------------------------------------
#
#   stg_orders (60% complete)
#     - Missing model description
#     - Missing primary key test
#
#   dim_products (40% complete)
#     - Model is still a placeholder
#     - Missing column descriptions
```

## Validation Commands

### Quick Validation

```bash
# Compile specific model
dbt compile --select model_name

# Run tests for specific model
dbt test --select model_name

# List models with tag
dbt list --select tag:placeholder
```

### Comprehensive Validation

```bash
# Full compilation check
dbt compile

# Run all tests with failures stored
dbt test --store-failures

# Generate and serve documentation
dbt docs generate
dbt docs serve
```

## Common Issues and Fixes

### YAML001: Missing Model Description (Warning)

**Problem:**

```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_id
```

**Fix:**

```yaml
models:
  - name: dim_customers
    description: |
      Customer dimension table containing customer attributes
      and demographics. Updated daily from CRM system.
    columns:
      - name: customer_id
```

### YAML002: Missing Key Constraint Test (Warning)

Key columns (ending in `_id`, `_key`, `_sk`, or prefixed with `fk_`) should have a constraint test.

**Problem:**

```yaml
columns:
  - name: customer_id
    description: "Unique customer identifier"
```

**Fix (for primary keys):**

```yaml
columns:
  - name: customer_id
    description: "Unique customer identifier"
    tests:
      - dbt_constraints.primary_key
```

**Fix (for foreign keys):**

```yaml
columns:
  - name: customer_id
    description: "Reference to dim_customers"
    tests:
      - dbt_constraints.foreign_key:
          pk_table_name: ref('dim_customers')
          pk_column_name: customer_id
```

### SQL004: Hardcoded Table Reference (Warning)

**Problem:**

```sql
select * from raw_database.schema.customers
```

**Fix:**

```sql
select * from {{ source('raw', 'customers') }}
```

### SQL006: Snowflake-Incompatible Syntax (Error)

**Problem:**

```sql
select top 100 *
from table1
where isnull(column1, 'default') = 'value'
```

**Fix:**

```sql
select *
from table1
where coalesce(column1, 'default') = 'value'
limit 100
```

## Integration with Hooks

This agent's validation rules are enforced automatically through Claude Code hooks:

### PostToolUse Hook

When Claude writes or edits files, the validation hook runs automatically:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/dbt-validation/validate_dbt_file.py --simple \"$FILE_PATH\"",
            "timeout": 30000
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/dbt-validation/validate_dbt_file.py --simple \"$FILE_PATH\"",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

### Hook Behavior

- **Exit Code 0**: Validation passed (errors, warnings, or recommendations don't block)
- **Exit Code 1**: Only returned for actual errors (Snowflake-incompatible syntax, file not found)
- **Warnings/Recommendations**: Displayed but don't block operations

## Validation Reports

### Model Completion Report

| Model         | SQL | Schema | Description | PK Test | Status         |
| ------------- | --- | ------ | ----------- | ------- | -------------- |
| dim_customers | ✅  | ✅     | ✅          | ✅      | Complete       |
| fct_orders    | ✅  | ✅     | ✅          | ❌      | Missing Test   |
| stg_products  | ✅  | ❌     | -           | -       | Missing Schema |
| int_metrics   | ⚠️  | ✅     | ✅          | ✅      | Placeholder    |

### Issue Summary

```text
Total Issues: 15

Errors (must fix): 5
  - SQL004 (Hardcoded tables): 2
  - SQL006 (Incompatible syntax): 3

Warnings (should address): 5
  - YAML001 (Missing model desc): 2
  - YAML002 (Missing key test): 3

Recommendations (nice to have): 5
  - YAML004 (Missing column desc): 2
  - SQL002 (No CTE pattern): 2
  - SQL003 (SELECT * usage): 1
```

## Quality Checklist

Use this checklist when reviewing models:

**Required (Errors)**

- [ ] No Snowflake-incompatible syntax (TOP, ISNULL, etc.)
- [ ] Uses `ref()` / `source()` for dependencies (no hardcoded tables)
- [ ] Compiles successfully
- [ ] All tests pass

**Important (Warnings)**

- [ ] Model has description in `_models.yml`
- [ ] Key columns have PK, UK, or FK tests

**Best Practices (Recommendations)**

- [ ] All columns documented with descriptions
- [ ] CTE pattern used for readability
- [ ] Explicit column lists instead of `SELECT *`
- [ ] Migrated models have header comment

## Automation

### CI/CD Integration

Add validation to CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Validate dbt models
  run: |
    uv run .claude/hooks/dbt-validation/validate_dbt_file.py models/
    dbt compile
    dbt test
```

### Pre-commit Hook

Validate before commits:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: dbt-validation
        name: dbt model validation
        entry: uv run .claude/hooks/dbt-validation/validate_dbt_file.py --simple
        language: system
        files: ^models/.*\.(sql|yml)$
```

```sql

```
