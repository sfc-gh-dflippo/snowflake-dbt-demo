---
name: snowflake-to-dbt
description:
  Convert Snowflake DDL to dbt models compatible with Snowflake. This skill should be used when
  converting Snowflake views, tables, or stored procedures to dbt code, generating schema.yml files
  with tests and documentation, or migrating existing Snowflake SQL to follow dbt best practices.
---

# Snowflake DDL to dbt Model Conversion

## Purpose

Transform Snowflake DDL (views, tables, stored procedures) into production-quality dbt models
compatible with Snowflake, maintaining the same business logic and data transformation steps while
following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting Snowflake views or tables to dbt models
- Migrating Snowflake stored procedures to dbt
- Generating schema.yml files with tests and documentation
- Transforming existing Snowflake SQL to follow dbt patterns

---

# Task Description

You are a database engineer working for a hospital system. You need to convert Snowflake DDL to
equivalent dbt code compatible with Snowflake, maintaining the same business logic and data
transformation steps while following dbt best practices.

# Input Requirements

I will provide you the Snowflake DDL to convert.

# Audience

The code will executed by data engineers who are learning Snowflake and dbt

# Output Requirements

Generate the following:

1. One or more dbt models with complete SQL for every column
2. A corresponding schema.yml file with appropriate tests and documentation
3. A config block with materialization strategy
4. Explanation of key changes and architectural decisions

# Conversion Guidelines

## General Principles

- Replace procedural logic with declarative SQL where possible
- Break down complex procedures into multiple modular dbt models
- Implement appropriate incremental processing strategies
- Maintain data quality checks through dbt tests

## Sample Response Format

```sql
-- dbt model: models/[domain]/[target_schema_name]/model_name.sql
{{ config(materialized='view') }}

/* Original SP: [sp_name]
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
        COLUMN1 AS COLUMN1_ALIAS,
        COLUMN2 AS COLUMN2_ALIAS,
        COLUMN3 AS COLUMN3_ALIAS,
        COLUMN4 AS COLUMN4_ALIAS
    FROM {{ ref('upstream_model') }}
),
transformed_data AS (
    SELECT
        UPPER(COLUMN1) AS COLUMN_ALIAS1,
        LOWER(COLUMN2) AS COLUMN_ALIAS2,
        COLUMN3 || COLUMN4 AS COLUMN_ALIAS3
    FROM source_data
)
SELECT
    COLUMN_ALIAS1,
    COLUMN_ALIAS2,
    COLUMN_ALIAS3
FROM transformed_data
```

```yaml
# models/[domain]/[target_schema_name]/schema.yml
version: 2

models:
  - name: model_name
    description: "Table description; converted from [Original database].[Original object name]"
    columns:
      - name: COLUMN_ALIAS1
        description: "Column description; Primary key"
        tests:
          - unique
          - not_null
      - name: COLUMN_ALIAS2
        description: "Column description; Foreign key to OTHER_TABLE"
        tests:
          - relationships:
              to: ref('OTHER_TABLE')
              field: OTHER_TABLE_KEY
      - name: COLUMN_ALIAS3
        description: "Column description"
```

```yaml
# dbt_project.yml
models:
  my_project:
    [domain]:
      [target_schema_name]:
        +schema: [target_schema_name]
```

## Specific Translation Rules

### dbt Specific Requirements:

- If the source is a view, use a view materialization in dbt
- Include appropriate dbt model configuration (materialization type)
- Add documentation blocks for a schema.yml
- Add descriptions for tables and columns
- Include relevant tests
- Define primary keys and relationships
- Assume that upstream objects are models
- Comprehensively provide all the columns in the output
- Break complex procedures into multiple models if needed
- Implement appropriate incremental strategies for large tables
- Use Snowflake SQL functions rather than macros whenever possible

### Performance Optimization:

- Suggest clustering keys if needed
- Recommend materialization strategy (view vs table)
- Identify potential performance improvements

### Dependencies:

- List any upstream dependencies
- Suggest model organization in dbt project

# Validation Checklist

- [ ] Every Snowflake DDL statement has been accounted for in the dbt models
- [ ] SQL in models is compatible with Snowflake
- [ ] All business logic preserved
- [ ] All columns included in output
- [ ] Materialization strategy selected
- [ ] Tests added
- [ ] SQL logic description complete
- [ ] Table descriptions added
- [ ] Column descriptions added
- [ ] Dependencies correctly mapped
- [ ] Incremental logic (if applicable) verified

---

## Related Skills

- **dbt-modeling**: For CTE patterns and SQL structure guidance
- **dbt-testing**: For implementing comprehensive dbt tests
- **dbt-architecture**: For project organization and folder structure
- **dbt-materializations**: For choosing materialization strategies (view, table, incremental,
  snapshots)
- **dbt-performance**: For clustering keys, warehouse sizing, and query optimization
- **dbt-commands**: For running dbt commands and model selection syntax
- **dbt-core**: For dbt installation, configuration, and package management
- **snowflake-cli**: For executing SQL and managing Snowflake objects
