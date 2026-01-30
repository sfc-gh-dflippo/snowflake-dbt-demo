# dbt Migration Skills - User Guide

This guide provides instructions for Snowflake customers on how to use the dbt migration skills to
convert legacy database objects to dbt models compatible with Snowflake.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Migration Approaches](#migration-approaches)
- [Preparing Your Code](#preparing-your-code)
- [Example 1: Migrating Snowflake Objects After SnowConvert](#example-1-migrating-snowflake-objects-after-snowconvert)
- [Example 2: Direct SQL Server to dbt Migration](#example-2-direct-sql-server-to-dbt-migration)
- [Example 3: Batch Migration Using Specification-Driven Development](#example-3-batch-migration-using-specification-driven-development)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Appendix: Skills and Cortex Code CLI Setup](#appendix-skills-and-cortex-code-cli-setup)
- [Appendix: Creating Subagents](#appendix-creating-subagents)

---

## Overview

The dbt migration skills help AI agents convert database objects (views, tables, stored procedures)
from various source platforms into production-quality dbt models. The skills provide:

- **Syntax translation** from source platforms to Snowflake SQL
- **dbt best practices** including CTE patterns, naming conventions, and testing
- **Schema documentation** generation with `_models.yml` files
- **Validation rules** to ensure quality and consistency

---

## Quick Start

Add the migration skills to Cortex Code CLI:

```bash
cortex skill add https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/.claude/skills
```

Invoke skills in your prompts using `$skill-name`:

```text
Convert @migration_source/views/my_view.sql to a dbt model using the $dbt-migration-snowflake skill
```

> **Tip:** Use the platform-specific skill for single objects (e.g., `$dbt-migration-snowflake`).
> For batch migrations, combine with `$dbt-migration` for workflow orchestration.

See [Appendix: Skills and Cortex Code CLI Setup](#appendix-skills-and-cortex-code-cli-setup) for
detailed installation, available skills, and troubleshooting.

---

## Migration Approaches

### Approach 1: Two-Step Migration (Recommended for Complex Migrations)

1. **Convert to Snowflake first** using
   [SnowConvert AI](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/about)
2. **Then convert to dbt** using `$dbt-migration-snowflake`

This approach is recommended when:

- Migrating from fully-supported SnowConvert platforms (SQL Server, Oracle, Teradata, Redshift)
- Complex stored procedures require AI-assisted conversion
- You want to validate Snowflake compatibility before adding dbt patterns

### Approach 2: Direct Migration

Convert source DDL directly to dbt models using platform-specific skills (e.g.,
`$dbt-migration-ms-sql-server`).

This approach works well when:

- Migrating simple to medium complexity views
- You have strong dbt expertise
- The source platform has limited SnowConvert support

---

## Preparing Your Code

Before migrating, extract your source DDL into files. For batch migrations with multiple objects,
see [Example 3: Batch Migration with Plan Mode](#example-3-batch-migration-with-plan-mode) for
folder organization and inventory templates.

### Extract DDL from Source Database

#### SQL Server

```sql
-- Extract view definitions
SELECT
    SCHEMA_NAME(v.schema_id) + '.' + v.name AS view_name,
    OBJECT_DEFINITION(v.object_id) AS view_definition
FROM sys.views v
WHERE SCHEMA_NAME(v.schema_id) = 'dbo';

-- Extract stored procedure definitions
SELECT
    SCHEMA_NAME(p.schema_id) + '.' + p.name AS proc_name,
    OBJECT_DEFINITION(p.object_id) AS proc_definition
FROM sys.procedures p
WHERE SCHEMA_NAME(p.schema_id) = 'dbo';
```

#### Snowflake

```sql
-- Extract view definitions
SHOW VIEWS IN SCHEMA my_database.my_schema;
SELECT GET_DDL('VIEW', 'my_database.my_schema.my_view');

-- Extract stored procedure definitions
SHOW PROCEDURES IN SCHEMA my_database.my_schema;
SELECT GET_DDL('PROCEDURE', 'my_database.my_schema.my_procedure(arg1 STRING, arg2 INT)');
```

### Document Dependencies

For complex migrations, create a dependency mapping showing which objects depend on others:

| Object Name         | Object Type | Source Schema | Depends On        | Complexity | Target Layer |
| ------------------- | ----------- | ------------- | ----------------- | ---------- | ------------ |
| customers           | TABLE       | dbo           | -                 | Low        | Bronze       |
| orders              | TABLE       | dbo           | customers         | Low        | Bronze       |
| vw_customer_summary | VIEW        | dbo           | customers, orders | Medium     | Silver       |
| sp_load_customers   | PROCEDURE   | dbo           | customers         | High       | Gold         |

---

## Example 1: Migrating Snowflake Objects After SnowConvert

This example demonstrates the recommended two-step approach: using SnowConvert to convert SQL Server
to Snowflake, then using the AI agent to convert Snowflake objects to dbt.

### Scenario

You have a SQL Server view that was converted to Snowflake using SnowConvert. Now you want to
convert it to a dbt model.

### Source: Snowflake View (Post-SnowConvert)

```sql
-- File: migration_source/views/vw_customer_orders.sql
-- This was converted from SQL Server [dbo].[vw_CustomerOrders] by SnowConvert

CREATE OR REPLACE VIEW analytics.vw_customer_orders AS
SELECT
    c.customer_id,
    c.customer_name,
    c.email,
    COUNT(o.order_id) AS total_orders,
    SUM(o.order_amount) AS total_spent,
    MAX(o.order_date) AS last_order_date,
    CASE
        WHEN SUM(o.order_amount) > 10000 THEN 'Premium'
        WHEN SUM(o.order_amount) > 1000 THEN 'Standard'
        ELSE 'Basic'
    END AS customer_tier
FROM raw_data.customers c
LEFT JOIN raw_data.orders o ON c.customer_id = o.customer_id
WHERE c.is_active = TRUE
GROUP BY c.customer_id, c.customer_name, c.email;
```

### AI Agent Prompt for Snowflake Conversion

```text
Convert this Snowflake view to a dbt model using the $dbt-migration-snowflake skill.
The view was originally converted from SQL Server [dbo].[vw_CustomerOrders] using SnowConvert.

Requirements:
- Place it in the silver layer with an `int_` prefix
- Use the standard CTE pattern
- Create the corresponding _models.yml with appropriate tests
- Add explicit type casts for all columns

@migration_source/views/vw_customer_orders.sql
```

The agent will generate a dbt model with CTE pattern, explicit type casts, and a corresponding
`_models.yml` with column documentation and tests.

---

## Example 2: Direct SQL Server to dbt Migration

This example demonstrates direct conversion from SQL Server T-SQL to dbt without using SnowConvert
first.

### Use Case

You have a SQL Server stored procedure that loads customer dimension data. You want to convert it
directly to a dbt incremental model.

### Source: SQL Server Stored Procedure

```sql
-- File: migration_source/stored_procedures/sp_load_dim_customer.sql

CREATE PROCEDURE [dbo].[sp_LoadDimCustomer]
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -- Merge customer changes
        MERGE INTO dw.dim_customer AS target
        USING (
            SELECT TOP 100 PERCENT
                c.customer_id,
                c.customer_name,
                ISNULL(c.email, 'unknown@email.com') AS email,
                c.phone,
                a.address_line1,
                a.city,
                a.state,
                a.postal_code,
                GETDATE() AS effective_date,
                1 AS is_current
            FROM staging.customers c
            LEFT JOIN staging.addresses a ON c.address_id = a.address_id
            WHERE c.modified_date > DATEADD(day, -1, GETDATE())
        ) AS source
        ON target.customer_id = source.customer_id
        WHEN MATCHED AND target.is_current = 1 THEN
            UPDATE SET
                customer_name = source.customer_name,
                email = source.email,
                phone = source.phone,
                address_line1 = source.address_line1,
                city = source.city,
                state = source.state,
                postal_code = source.postal_code,
                effective_date = source.effective_date
        WHEN NOT MATCHED THEN
            INSERT (customer_id, customer_name, email, phone,
                    address_line1, city, state, postal_code,
                    effective_date, is_current)
            VALUES (source.customer_id, source.customer_name, source.email,
                    source.phone, source.address_line1, source.city,
                    source.state, source.postal_code,
                    source.effective_date, source.is_current);

        PRINT 'Rows affected: ' + CAST(@@ROWCOUNT AS VARCHAR);

    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;
```

### AI Agent Prompt for SQL Server Conversion

```text
Convert this SQL Server stored procedure to a dbt incremental model using the
$dbt-migration-ms-sql-server skill.

Requirements:
- Convert T-SQL syntax to Snowflake-compatible SQL
- Implement the MERGE logic as a dbt incremental model
- Place it in the gold layer as a dimension model with `dim_` prefix
- Create the _models.yml with primary key tests
- Add inline comments for any syntax conversions

@migration_source/stored_procedures/sp_load_dim_customer.sql
```

The agent will generate a dbt incremental model with T-SQL syntax converted to Snowflake, staging
model recommendations, and a `_models.yml` with column documentation and tests.

---

## Example 3: Batch Migration Using Specification-Driven Development

For migrating multiple objects, follow the Specification-Driven Development (SDD) approach: create a
PRD first, review it, then generate a task list to guide execution.

### When to Use This Approach

- Migrating 5+ objects at once
- Objects have dependencies on each other
- You want stakeholder review before implementation
- You need a documented plan with clear acceptance criteria

### Step 1: Create the Migration PRD

Start by asking the agent to analyze your database and create a Product Requirements Document:

```text
/plan

I need to migrate MY_DATABASE to dbt models using the $dbt-migration and $dbt-migration-snowflake skills.
Run this query to extract all DDL: SELECT GET_DDL('DATABASE', 'MY_DATABASE');
Use the output to create a Migration PRD at docs/MY_DATABASE_migration_prd.md using the $dbt-migration workflow.
Please make the plan specific down to the object level.
Do not begin development until I have completed my review.
```

### Step 2: Review the PRD

Review the generated `docs/MY_DATABASE_migration_prd.md` and verify:

- All objects are inventoried correctly
- Dependencies are accurately mapped
- Layer assignments (bronze/silver/gold) are consistent with your goal

Ask your agent to make any necessary edits to the PRD before proceeding.

### Step 3: Generate the Task List

Once the PRD is approved, ask the agent to create a detailed task list:

```text
/plan

First, use the $dbt-migration and $dbt-migration-snowflake skills with the
`docs/MY_DATABASE_migration_prd.md` PRD to generate a task list document named
`docs/MY_DATABASE_migration_tasks.md` that breaks down the migration into actionable tasks.

Ensure each task follows these rules:
- Be atomic and perform one activity for one object
- Include a detailed task description and acceptance criteria
- Identify dependencies (which tasks must complete first)
- Include estimated complexity (simple/medium/complex)
    - Medium and complex tasks should be broken down into sub-tasks
- Specify agent skills the task should utilize
- Specify the subagent to perform the task

Second, create any necessary subagents in this project's `.claude/agents/` directory to perform
the tasks and subtasks.

Wait for my approval before starting implementation.
```

See [Appendix: Creating Subagents](#appendix-creating-subagents) for details on how subagents work
and how to create custom ones for your migration.

### Step 4: Execute the Migration

After you have reviewed the task list, you can begin the migration:

```text
/plan

Please begin implementing docs/MY_DATABASE_migration_tasks.md. Please execute tasks and sub-tasks in parallel sub-agents whenever possible.
```

---

## Best Practices

### 1. Start with Simple Objects

Begin with simple views before tackling complex stored procedures. This helps you:

- Understand the migration patterns
- Build confidence with the tooling
- Establish naming conventions early

### 2. Use Tags for Tracking

Add tags to track migration progress:

```sql
{{ config(
    materialized='view',
    tags=['migrated', 'sqlserver', 'phase1']
) }}
```

### 3. Validate Incrementally

Run `dbt build` after each conversion to catch issues early:

```bash
# Build a single model
dbt build --select dim_customer

# Build all models with a specific tag
dbt build --select tag:migrated
```

### 4. Compare Results

Create validation queries to compare source and target data. Run the source query against your
legacy database and the target query against Snowflake to verify the migration.

**SQL Server (Source Query):**

```sql
-- Run this against SQL Server to get source metrics
SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT customer_id) AS distinct_customers,
    SUM(CAST(total_amount AS DECIMAL(18,2))) AS total_amount_sum,
    MIN(order_date) AS min_order_date,
    MAX(order_date) AS max_order_date,
    SUM(CASE WHEN status IS NULL THEN 1 ELSE 0 END) AS null_status_count
FROM dbo.orders
WHERE order_date >= '2024-01-01';
```

**Snowflake (Target Query):**

```sql
-- Run this against Snowflake to compare with source metrics
SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT customer_id) AS distinct_customers,
    SUM(total_amount::DECIMAL(18,2)) AS total_amount_sum,
    MIN(order_date) AS min_order_date,
    MAX(order_date) AS max_order_date,
    SUM(IFF(status IS NULL, 1, 0)) AS null_status_count
FROM analytics.silver.int_orders
WHERE order_date >= '2024-01-01';
```

Compare the results from both queries to ensure row counts, aggregates, and date ranges match.

#### Snowflake Data Validation CLI

For automated, large-scale data validation, use Snowflake's official **Data Validation CLI**
(`snowflake-data-validation`). This tool supports schema validation, metrics comparison, and CI/CD
integration for SQL Server, Teradata, and Redshift migrations.

```bash
# Install the CLI
pip install snowflake-data-validation

# Generate config template for SQL Server
sdv sqlserver init-config

# Run validation
sdv sqlserver validate --config validation_config.yaml
```

See [resources/data-validation-cli.md](resources/data-validation-cli.md) for detailed documentation
and configuration examples, or visit the
[official documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/index).

### 5. Document Conversion Decisions

Always include header comments explaining:

- Original object name and location
- Key syntax conversions made
- Business logic preserved or modified
- Any breaking changes

---

## Troubleshooting

### Common Issues

| Issue                           | Solution                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------- |
| "Syntax error" after conversion | Check for platform-specific syntax not converted (see skill translation tables) |
| Missing columns in output       | Ensure `SELECT *` was expanded to explicit columns                              |
| Type mismatch errors            | Add explicit type casts using `::TYPE` syntax                                   |
| ref() not found                 | Create staging models for source tables first                                   |
| Test failures                   | Review primary key uniqueness and null handling                                 |

### Getting Help

1. **Check the skill documentation**: Each `dbt-migration-*` skill contains detailed syntax
   conversion tables
2. **Review translation references**: Located in `translation-references/` folders within each skill
3. **Run validation**: Use `dbt compile` to catch syntax errors before running
4. **Use dbt docs**: Generate documentation with `dbt docs generate` to visualize lineage

---

## Related Documentation

- $dbt-migration - Main migration workflow skill
- $dbt-migration-validation - Validation rules and quality checks
- $dbt-modeling - CTE patterns and SQL structure
- $dbt-testing - Testing strategies with dbt_constraints
- $dbt-architecture - Project organization and naming conventions

---

## Appendix: Skills and Cortex Code CLI Setup

Detailed instructions for setting up and managing dbt migration skills in Cortex Code CLI.

### What Are Skills?

Skills are markdown files that teach AI agents how to complete specific tasks. They provide
structured guidance, tool references, decision logic, and checkpoints—transforming agents into
domain experts for specialized workflows.

#### How Skills Work

When you invoke a skill (e.g., `$dbt-migration-snowflake`), Cortex Code loads the skill's markdown
content into its context. This gives the agent:

1. **Structured workflows** - Step-by-step instructions for completing tasks
2. **Domain knowledge** - Platform-specific syntax translations, best practices, patterns
3. **Tool guidance** - Which tools to use and when
4. **Quality checks** - Validation rules and stopping points for user review

#### Skill File Structure

Skills are stored in `.claude/skills/` directories and follow this structure:

```text
my-skill/
├── SKILL.md              # Main skill file (required)
├── pyproject.toml        # Python dependencies (if scripts)
├── scripts/              # Executable code (optional)
├── references/           # Supporting documentation (optional)
```

Every skill has YAML frontmatter with `name` and `description`, followed by markdown content:

```markdown
---
name: skill-name
description: "What it does + when to use it. Include trigger phrases."
---

# Skill Title

## When to Use

[Criteria for activation]

## Workflow

[Step-by-step instructions]

## Output

[What the skill produces]
```

#### Skills vs Subagents

| Concept       | Purpose                                            | Invocation                        |
| ------------- | -------------------------------------------------- | --------------------------------- |
| **Skills**    | Domain knowledge and workflows loaded into context | `$skill-name` in prompts          |
| **Subagents** | Autonomous agents that run tasks in parallel       | Task tool or automatic delegation |

Skills provide **knowledge**; subagents provide **execution capability**. Subagents typically
reference skills in their system prompts to gain domain expertise.

#### Invoking Skills

Use the `$skill-name` prefix in prompts:

```text
Convert this view to a dbt model using $dbt-migration-snowflake
```

The agent loads the skill and follows its workflow to complete the task.

For more details on skill development and best practices, see the
[Cortex Code Skill Development documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-code).

### Prerequisites

- **Cortex Code CLI** installed and configured
- **Git** installed on your system

### Import Skills from GitHub

Use the `cortex skill add` command to import skills directly from this GitHub repository:

```bash
cortex skill add https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/.claude/skills
```

This command automatically:

- Clones the repository to `~/.snowflake/cortex/remote_cache/`
- Discovers all skills in the specified `.claude/skills/` directory
- Makes them available in all future Cortex Code sessions

### Interactive Skill Manager

Within a Cortex Code session, use the `/skill` command to open an interactive manager:

```text
/skill                    # Opens interactive skill manager
$$                        # Quick list of available skills
```

The manager allows you to view, add, sync, and delete skills across all locations.

### Verify Installation

```bash
cortex skill list
```

You should see skills listed under "Remote skills", including `dbt-migration`,
`dbt-migration-snowflake`, `dbt-migration-ms-sql-server`, and others.

### Updating Skills

> **Note:** The `/skill` manager's "refresh" option re-reads cached files but does **not** pull new
> changes from GitHub. To get updates, remove and re-add the skills.

**Linux/macOS:**

```bash
# Edit skills.json - remove the remote entry for snowflake-dbt-demo
nano ~/.snowflake/cortex/skills.json

# Delete the cached repository
rm -rf ~/.snowflake/cortex/remote_cache/github_sfc-gh-dflippo_snowflake-dbt-demo*

# Re-add the skills
cortex skill add https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/tree/main/.claude/skills
```

**Windows (PowerShell):**

```powershell
notepad $env:USERPROFILE\.snowflake\cortex\skills.json
Remove-Item -Recurse -Force "$env:USERPROFILE\.snowflake\cortex\remote_cache\github_sfc-gh-dflippo_snowflake-dbt-demo*"
cortex skill add https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/tree/main/.claude/skills
```

### Available dbt Skills

#### Migration Skills

| Skill Name                    | Source Platform                  | Key Features                       |
| ----------------------------- | -------------------------------- | ---------------------------------- |
| `dbt-migration`               | All platforms                    | Main orchestration (7-phase)       |
| `dbt-migration-snowflake`     | Snowflake                        | Native Snowflake to dbt patterns   |
| `dbt-migration-ms-sql-server` | SQL Server / Azure Synapse       | T-SQL, IDENTITY, TOP, #temp tables |
| `dbt-migration-oracle`        | Oracle                           | PL/SQL, ROWNUM, CONNECT BY         |
| `dbt-migration-teradata`      | Teradata                         | QUALIFY, BTEQ, volatile tables     |
| `dbt-migration-bigquery`      | BigQuery                         | UNNEST, STRUCT/ARRAY               |
| `dbt-migration-redshift`      | Redshift                         | DISTKEY/SORTKEY, COPY/UNLOAD       |
| `dbt-migration-postgres`      | PostgreSQL / Greenplum / Netezza | Array expressions                  |
| `dbt-migration-db2`           | IBM DB2                          | SQL PL, FETCH FIRST                |
| `dbt-migration-hive`          | Hive / Spark / Databricks        | External tables, PARTITIONED BY    |
| `dbt-migration-vertica`       | Vertica                          | Projections, flex tables           |
| `dbt-migration-sybase`        | Sybase IQ                        | T-SQL variant                      |
| `dbt-migration-validation`    | All platforms                    | Validate models against rules      |

#### Core dbt Skills

| Skill Name             | Description                                                         |
| ---------------------- | ------------------------------------------------------------------- |
| `dbt-core`             | Installation, configuration, project setup, package management      |
| `dbt-commands`         | Command-line operations, model selection syntax, Jinja patterns     |
| `dbt-architecture`     | Project structure, medallion architecture (bronze/silver/gold)      |
| `dbt-modeling`         | Writing models with CTE patterns, SQL structure, layer templates    |
| `dbt-materializations` | Choosing materializations (view, table, incremental, snapshots)     |
| `dbt-testing`          | Testing strategies with dbt_constraints, generic and singular tests |
| `dbt-artifacts`        | Monitor execution using dbt Artifacts package                       |
| `dbt-performance`      | Optimization through clustering, warehouse sizing, query tuning     |

#### Snowflake Integration Skills

| Skill Name                     | Description                                            |
| ------------------------------ | ------------------------------------------------------ |
| `dbt-projects-on-snowflake`    | Deploy and run dbt projects natively in Snowflake      |
| `dbt-projects-snowflake-setup` | Step-by-step setup guide for dbt Projects on Snowflake |

### Using Skills in Prompts

Invoke skills using the `$skill-name` syntax:

```text
Convert this stored procedure to a dbt model using $dbt-migration-ms-sql-server:

[paste your SQL Server code here]
```

Use `@` to include files directly:

```text
Convert @migration_source/views/vw_customer_orders.sql to a dbt model following the
medallion architecture pattern using $dbt-migration-snowflake.
```

Reference Snowflake objects with `#`:

```text
Convert the view #MY_DB.MY_SCHEMA.VW_CUSTOMER_ORDERS to a dbt model using $dbt-migration-snowflake.
```

### Troubleshooting Setup

| Issue                         | Solution                                                |
| ----------------------------- | ------------------------------------------------------- |
| Skills not appearing          | Run `cortex skill list` to verify installation          |
| "No valid skills found" error | Ensure you use the full tree URL with branch and path   |
| Git clone fails               | Check your network connection and GitHub access         |
| Command not found             | Verify Cortex Code CLI is installed: `cortex --version` |

---

## Appendix: Creating Subagents

Subagents are autonomous agents that can be spawned to handle specific tasks in the background. They
enable parallel execution of migration tasks and provide specialized behavior for different workflow
phases.

### Subagent File Locations

Subagents can be defined in two locations:

| Location          | Path                              | Scope                | Use Case                                     |
| ----------------- | --------------------------------- | -------------------- | -------------------------------------------- |
| **Project-level** | `.claude/agents/*.md`             | Current project only | Project-specific workflows, migration agents |
| **Global**        | `~/.snowflake/cortex/agents/*.md` | All projects         | Reusable agents across multiple projects     |

Both locations are automatically discovered by Cortex Code and made available via the Task tool.

### Subagent File Structure

Subagent files are Markdown documents with YAML frontmatter that define the agent's identity,
capabilities, and system prompt.

```markdown
---
name: agent-name
description:
  A concise description of what the agent does and when it should be used. This appears in the Task
  tool's agent list and helps the orchestrator decide when to invoke this agent.
tools: Read, Grep, Glob, Write, Bash
skills: skill-name-1, skill-name-2
---

# Agent Title

The body of the file becomes the agent's system prompt. Include:

- Purpose and responsibilities
- Required skills to reference
- Workflow phases or steps
- Quality checklists
- Error handling guidance
```

### Frontmatter Fields

| Field         | Required | Description                                                                                           |
| ------------- | -------- | ----------------------------------------------------------------------------------------------------- |
| `name`        | Yes      | Unique identifier used to invoke the agent (e.g., `dbt-migration`)                                    |
| `description` | Yes      | One-paragraph description shown in the Task tool's available agents list                              |
| `tools`       | No       | Comma-separated list of tools the agent can use: `Read`, `Grep`, `Glob`, `Write`, `Bash`, `WebSearch` |
| `skills`      | No       | Comma-separated list of skills the agent should load                                                  |

### Invoking Subagents

**Automatic invocation:** Cortex Code's orchestrator automatically selects appropriate agents based
on task descriptions and agent capabilities.

**Explicit invocation:** Reference agents by name in your prompts:

```text
Use the dbt-migration agent to convert @migration_source/stored_procedures/sp_load_customers.sql
```

**Via Task tool:** The parent agent can spawn subagents using the Task tool:

```text
Launch the dbt-validation agent to validate all models in models/gold/
```

### Monitoring Subagents

Use these commands to monitor running agents:

| Command             | Description                                   |
| ------------------- | --------------------------------------------- |
| `/agents`           | Interactive list of running background agents |
| `cortex agent list` | CLI command to list all agents                |

### Best Practices for Subagent Design

1. **Single Responsibility**: Each agent should have a focused purpose (validation, migration,
   deployment)

2. **Skill References**: List required skills in the agent body so it loads the right context

3. **Quality Checklists**: Include explicit checklists the agent must verify before marking tasks
   complete

4. **Error Handling**: Document how the agent should handle common failure scenarios

5. **Completion Policy**: Define what "done" means - agents should never mark tasks complete with
   outstanding issues

### Existing Agents in This Repository

| Agent         | Purpose                                                                                     |
| ------------- | ------------------------------------------------------------------------------------------- |
| dbt-migrator  | Migrates legacy database objects (stored procedures, views, ETL) to dbt models on Snowflake |
| dbt-validator | Validates dbt models and schema files for quality, completeness, and best practices         |
| dbt-developer | Writes dbt models, implements tests, and follows analytics engineering best practices       |
| dbt-deployer  | Deploys local dbt projects to dbt Projects on Snowflake and manages CI/CD pipelines         |

### Creating Custom Agents for Your Migration

For large migrations, consider creating project-specific agents:

1. **Object-type agents**: Separate agents for views vs. stored procedures
2. **Complexity agents**: Different agents for simple vs. complex conversions
3. **Layer agents**: Agents specialized for bronze, silver, or gold layer patterns

Example prompt to generate custom agents:

```text
Create a subagent in .claude/agents/ for migrating SQL Server stored procedures that follow
the SCD Type 2 pattern. The agent should use the $dbt-migration-ms-sql-server skill and
output incremental models with snapshot-like behavior.
```
