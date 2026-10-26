# snowflake-dbt-migration

A plugin for **Cortex Code CLI** and **Claude Code CLI** that provides dbt migration skills for
converting source database SQL to dbt models on Snowflake.

## Routing Boundary

- **"migrate"** / **"migration to Snowflake"** (bare, no "dbt") → use the `snowflake-migration`
  plugin (SnowConvert-based end-to-end migration)
- **"dbt migration"** / **"convert to dbt"** / **"dbt migrate"** → use **this plugin** (dbt-focused
  source-to-model conversion)

If SnowConvert has not been run yet and a user asks for dbt migration, suggest running `/migrate`
first to handle initial conversion, then use the `dbt-migrate` skill for dbt-specific modeling.

## Included Skills (15)

| Skill                       | Description                                                        |
| --------------------------- | ------------------------------------------------------------------ |
| dbt-migrate                 | Entry point: routes a dbt migration request to the right skill     |
| dbt-migration               | Orchestrator: discovery, planning, conversion, testing, deployment |
| dbt-migration-snowflake     | Convert Snowflake DDL to dbt models                                |
| dbt-migration-bigquery      | Convert BigQuery DDL to dbt models                                 |
| dbt-migration-db2           | Convert IBM DB2 DDL to dbt models                                  |
| dbt-migration-hive          | Convert Hive/Spark/Databricks DDL to dbt models                    |
| dbt-migration-ms-sql-server | Convert SQL Server/Azure Synapse T-SQL to dbt models               |
| dbt-migration-oracle        | Convert Oracle PL/SQL DDL to dbt models                            |
| dbt-migration-postgres      | Convert PostgreSQL/Greenplum/Netezza DDL to dbt models             |
| dbt-migration-redshift      | Convert Amazon Redshift DDL to dbt models                          |
| dbt-migration-sybase        | Convert Sybase IQ DDL to dbt models                                |
| dbt-migration-teradata      | Convert Teradata DDL to dbt models                                 |
| dbt-migration-vertica       | Convert Vertica DDL to dbt models                                  |
| dbt-modeling                | Writing dbt models with CTE patterns and SQL structure             |
| dbt-architecture            | dbt project structure using medallion architecture                 |

## Installation

### Cortex Code CLI

```bash
cortex plugin install <path-to-repo>/.claude/plugins/snowflake-dbt-migration
```

Or from GitHub:

```bash
cortex plugin install https://github.com/sfc-gh-dflippo/snowflake-dbt-demo/tree/main/.claude/plugins/snowflake-dbt-migration
```

### Claude Code CLI

Claude Code installs plugins from a marketplace. This repository is one
(`.claude-plugin/marketplace.json`). Add it from GitHub or from a local clone, then install:

```bash
claude plugin marketplace add sfc-gh-dflippo/snowflake-dbt-demo   # or: <path-to-repo>
claude plugin install snowflake-dbt-migration@snowflake-dbt-demo
```

## Usage

After installation, use the `dbt-migrate` skill to start a dbt migration workflow. It routes to the
appropriate source-platform skill based on your source database. Static checks and audits of the
converted models come from the separate `dbt-quality` plugin (`dbt-quality:dbt-quality`); they do
not run warehouse-backed equivalence tests.

In Claude Code, the plugin namespaces its skills, so the entry point is
`/snowflake-dbt-migration:dbt-migrate`. In Cortex Code, ask for the `dbt-migrate` skill by name (for
example "use the dbt-migrate skill to convert this Oracle procedure").

## Version

See [VERSION](./VERSION) for current version.
