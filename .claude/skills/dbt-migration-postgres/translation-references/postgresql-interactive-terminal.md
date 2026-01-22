---
description: PSQL commands
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/postgresql-interactive-terminal
title: SnowConvert AI - PostgreSQL - PostgreSQL interactive terminal | Snowflake Documentation
---

## Applies to

- PostgreSQL
- Netezza

## Description

> PSQL is a terminal-based front-end to PostgreSQL. It enables you to type in queries interactively,
> issue them to PostgreSQL, and see the query results. Alternatively, input can be from a file. In
> addition, it provides a number of meta-commands and various shell-like features to facilitate
> writing scripts and automating a wide variety of tasks.
> ([PSQL documentation](https://www.postgresql.org/docs/9.2/app-psql.html)).

In Snowflake, **PSQL commands are not applicable.** While no longer needed for execution,
SnowConvert AI retains the original PSQL command as a comment

## Sample Source Patterns

### Input Code

#### Greenplum

```sql
\set ON_ERROR_STOP TRUE
```

### Output Code

#### Snowflake

```sql
----** SSC-FDM-PG0015 - PSQL COMMAND IS NOT APPLICABLE IN SNOWFLAKE. **
--\set ON_ERROR_STOP TRUE
```

## Related EWIs

1. [SSC-FDM-PG0015](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0015)
   : PSQL command is not applicable in Snowflake.
