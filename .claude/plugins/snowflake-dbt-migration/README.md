# snowflake-dbt-migration

A plugin for **Cortex Code CLI** and **Claude Code CLI** that provides dbt migration skills for
converting source database SQL to dbt models on Snowflake.

## Routing Boundary

- **"migrate"** / **"migration to Snowflake"** (bare, no "dbt") → use the `snowflake-migration`
  plugin (SnowConvert-based end-to-end migration)
- **"dbt migration"** / **"convert to dbt"** / **"dbt migrate"** → use **this plugin** (dbt-focused
  source-to-model conversion)

If SnowConvert has not been run yet and a user asks for dbt migration, suggest running `/migrate`
first to handle initial conversion, then use `/dbt-migrate` for dbt-specific modeling.

## Included Skills (15)

Static quality checks (single model or whole project) come from the separate `dbt-quality` plugin,
through the skill `dbt-quality:dbt-quality`. Those checks do not run dbt and do not compare data
with the source warehouse.

| Skill                       | Description                                                        |
| --------------------------- | ------------------------------------------------------------------ |
| dbt-migration               | Orchestrator: discovery, planning, conversion, testing, deployment |
| dbt-migrate                 | Entry point: routes to the right source-platform skill             |
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

### Cortex Code Desktop (project scope)

To share the plugin with a team, copy it into the project at
`.cortex/plugins/snowflake-dbt-migration` and check it in. Do the same for `dbt-quality` if you want
static quality checks. Paths in the plugin are relative, so no machine-specific edits are needed.

## Usage

After installation, use the `dbt-migrate` skill (`/dbt-migrate`) to start a dbt migration workflow.
The skill routes to the appropriate source-platform skill based on your source database.

## Troubleshooting (Windows)

- **MCP error `spawn ... ENOENT` for `dbt-quality`:** The old plugin cannot start on Windows. Update
  `dbt-quality` to a later plugin release that includes the Windows launcher, then restart the app.
- **`curl: (35)` on first-run download behind a proxy:** Set `HTTPS_PROXY` or `SCAI_PROXY` to your
  proxy URL, then run again. Keep TLS and SHA-256 verification on. Do not disable them.

## Version

See [VERSION](./VERSION) for current version.
