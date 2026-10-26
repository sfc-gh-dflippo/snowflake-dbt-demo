---
name: dbt-migrate
description:
  Entry point for dbt-native migration. Routes a request to convert source database SQL (SQL Server,
  Oracle, Teradata, BigQuery, Redshift, PostgreSQL, DB2, Hive, Vertica, Sybase, Snowflake) into dbt
  models on Snowflake to the right platform skill. Use when asked to dbt migrate, convert to dbt,
  migrate SQL to dbt models, or convert stored procedures or DDL to dbt.
---

# dbt-migrate

Route the user's request to the most relevant skill below.

<skill-match>
Match the user's request to the most relevant skill and load it.

**Routing rules:**

- If the user says "migrate" without "dbt", suggest the `snowflake-migration` plugin first
  (SnowConvert-based conversion). This skill is for dbt-native conversion.
- Match by source platform keyword. If ambiguous, ask which source database.
- If the user already has SnowConvert output, route to dbt-migration (the orchestrator).

## Orchestration & validation

- **dbt-migration** — end-to-end orchestrator: discovery, planning, conversion, testing, deployment
  → `snowflake-dbt-migration:dbt-migration`
- **dbt-quality** — static checks on one converted model file and project-wide audits with an HTML
  report → `dbt-quality:dbt-quality`. This is static analysis only. It does not run warehouse-backed
  equivalence tests.

## Source-platform converters

- **dbt-migration-snowflake** — convert Snowflake DDL to dbt models →
  `snowflake-dbt-migration:dbt-migration-snowflake`
- **dbt-migration-bigquery** — convert BigQuery SQL to dbt models →
  `snowflake-dbt-migration:dbt-migration-bigquery`
- **dbt-migration-db2** — convert IBM DB2 DDL to dbt models →
  `snowflake-dbt-migration:dbt-migration-db2`
- **dbt-migration-hive** — convert Hive/Spark/Databricks DDL to dbt models →
  `snowflake-dbt-migration:dbt-migration-hive`
- **dbt-migration-ms-sql-server** — convert SQL Server/Azure Synapse T-SQL to dbt models →
  `snowflake-dbt-migration:dbt-migration-ms-sql-server`
- **dbt-migration-oracle** — convert Oracle PL/SQL DDL to dbt models →
  `snowflake-dbt-migration:dbt-migration-oracle`
- **dbt-migration-postgres** — convert PostgreSQL/Greenplum/Netezza DDL to dbt models →
  `snowflake-dbt-migration:dbt-migration-postgres`
- **dbt-migration-redshift** — convert Amazon Redshift DDL to dbt models →
  `snowflake-dbt-migration:dbt-migration-redshift`
- **dbt-migration-sybase** — convert Sybase IQ DDL to dbt models →
  `snowflake-dbt-migration:dbt-migration-sybase`
- **dbt-migration-teradata** — convert Teradata DDL to dbt models →
  `snowflake-dbt-migration:dbt-migration-teradata`
- **dbt-migration-vertica** — convert Vertica DDL to dbt models →
  `snowflake-dbt-migration:dbt-migration-vertica`

## Patterns & architecture

- **dbt-modeling** — CTE patterns, SQL structure, layer-specific templates →
  `snowflake-dbt-migration:dbt-modeling`
- **dbt-architecture** — medallion architecture, folder structure, naming conventions →
  `snowflake-dbt-migration:dbt-architecture`

## Fallback

If no skill matches, say so explicitly, then help with your own knowledge. </skill-match>
