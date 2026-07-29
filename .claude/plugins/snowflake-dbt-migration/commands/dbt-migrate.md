---
description: dbt-native migration — convert source SQL to dbt models on Snowflake
---

# dbt-migrate

Help me using the reference skills below.

$ARGUMENTS

<skill-match>
Match the user's request to the most relevant skill and load it.

**Routing rules:**

- If the user says "migrate" without "dbt", suggest `/migrate` first (SnowConvert-based conversion).
  This command is for dbt-native conversion.
- Match by source platform keyword. If ambiguous, ask which source database.
- If the user already has SnowConvert output, route to dbt-migration (the orchestrator).

## Orchestration & validation

- **dbt-migration** — end-to-end orchestrator: discovery, planning, conversion, testing, deployment
  → `./skills/dbt-migration`
- **dbt-migration-validation** — validate converted models: schema checks, anti-patterns, auto-fixes
  → `./skills/dbt-migration-validation`

## Source-platform converters

- **dbt-migration-snowflake** — convert Snowflake DDL to dbt models →
  `./skills/dbt-migration-snowflake`
- **dbt-migration-bigquery** — convert BigQuery SQL to dbt models →
  `./skills/dbt-migration-bigquery`
- **dbt-migration-db2** — convert IBM DB2 DDL to dbt models → `./skills/dbt-migration-db2`
- **dbt-migration-hive** — convert Hive/Spark/Databricks DDL to dbt models →
  `./skills/dbt-migration-hive`
- **dbt-migration-ms-sql-server** — convert SQL Server/Azure Synapse T-SQL to dbt models →
  `./skills/dbt-migration-ms-sql-server`
- **dbt-migration-oracle** — convert Oracle PL/SQL DDL to dbt models →
  `./skills/dbt-migration-oracle`
- **dbt-migration-postgres** — convert PostgreSQL/Greenplum/Netezza DDL to dbt models →
  `./skills/dbt-migration-postgres`
- **dbt-migration-redshift** — convert Amazon Redshift DDL to dbt models →
  `./skills/dbt-migration-redshift`
- **dbt-migration-sybase** — convert Sybase IQ DDL to dbt models → `./skills/dbt-migration-sybase`
- **dbt-migration-teradata** — convert Teradata DDL to dbt models →
  `./skills/dbt-migration-teradata`
- **dbt-migration-vertica** — convert Vertica DDL to dbt models → `./skills/dbt-migration-vertica`

## Patterns & architecture

- **dbt-modeling** — CTE patterns, SQL structure, layer-specific templates → `./skills/dbt-modeling`
- **dbt-architecture** — medallion architecture, folder structure, naming conventions →
  `./skills/dbt-architecture`

## Fallback

If no skill matches, say so explicitly, then help with your own knowledge. </skill-match>
