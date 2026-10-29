---
name: dbt-migrate
description:
  Entry point for dbt-native migration. Routes a request to convert source SQL (Oracle, SQL Server,
  Teradata, Snowflake, BigQuery, DB2, Hive, PostgreSQL, Redshift, Sybase, Vertica) into dbt models
  on Snowflake. Use when the user says dbt migrate, convert to dbt, migrate to dbt, or migrate this
  warehouse to dbt models.
---

# dbt-migrate

Help me using the reference skills below.

<skill-match>
Match the user's request to the most relevant skill and load it.

**Routing rules:**

- If the user says "migrate" without "dbt", suggest `/migrate` first (SnowConvert-based conversion).
  This skill is for dbt-native conversion.
- Match by source platform keyword. If ambiguous, ask which source database.
- If the user already has SnowConvert output, route to dbt-migration (the orchestrator).

## Orchestration & validation

- **snowflake-dbt-migration:dbt-migration** — end-to-end orchestrator: discovery, planning,
  conversion, testing, deployment → `../dbt-migration`
- **dbt-quality:dbt-quality** — static quality checks (no dbt run, no warehouse): validate one
  converted model file, or audit the whole project with an HTML report. It does not test data
  equivalence against the source. Use the data validation steps in
  `snowflake-dbt-migration:dbt-migration` for that.

## Source-platform converters

- **snowflake-dbt-migration:dbt-migration-snowflake** — convert Snowflake DDL to dbt models →
  `../dbt-migration-snowflake`
- **snowflake-dbt-migration:dbt-migration-bigquery** — convert BigQuery SQL to dbt models →
  `../dbt-migration-bigquery`
- **snowflake-dbt-migration:dbt-migration-db2** — convert IBM DB2 DDL to dbt models →
  `../dbt-migration-db2`
- **snowflake-dbt-migration:dbt-migration-hive** — convert Hive/Spark/Databricks DDL to dbt models →
  `../dbt-migration-hive`
- **snowflake-dbt-migration:dbt-migration-ms-sql-server** — convert SQL Server/Azure Synapse T-SQL
  to dbt models → `../dbt-migration-ms-sql-server`
- **snowflake-dbt-migration:dbt-migration-oracle** — convert Oracle PL/SQL DDL to dbt models →
  `../dbt-migration-oracle`
- **snowflake-dbt-migration:dbt-migration-postgres** — convert PostgreSQL/Greenplum/Netezza DDL to
  dbt models → `../dbt-migration-postgres`
- **snowflake-dbt-migration:dbt-migration-redshift** — convert Amazon Redshift DDL to dbt models →
  `../dbt-migration-redshift`
- **snowflake-dbt-migration:dbt-migration-sybase** — convert Sybase IQ DDL to dbt models →
  `../dbt-migration-sybase`
- **snowflake-dbt-migration:dbt-migration-teradata** — convert Teradata DDL to dbt models →
  `../dbt-migration-teradata`
- **snowflake-dbt-migration:dbt-migration-vertica** — convert Vertica DDL to dbt models →
  `../dbt-migration-vertica`

## Patterns & architecture

- **snowflake-dbt-migration:dbt-modeling** — CTE patterns, SQL structure, layer-specific templates →
  `../dbt-modeling`
- **snowflake-dbt-migration:dbt-architecture** — medallion architecture, folder structure, naming
  conventions → `../dbt-architecture`

## Fallback

If no skill matches, say so explicitly, then help with your own knowledge. </skill-match>
