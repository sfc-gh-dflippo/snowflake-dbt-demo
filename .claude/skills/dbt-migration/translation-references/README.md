# Database Translation References

This directory contains translation references for converting SQL from various source databases to Snowflake-compatible SQL and dbt models.

## Supported Source Databases

<!-- prettier-ignore -->
|Database|Description|
|---|---|
|[Teradata](teradata/README.md)|Teradata SQL, BTEQ, FastLoad, MultiLoad|
|[Oracle](oracle/README.md)|Oracle SQL, PL/SQL, SQL\*Plus|
|[SQL Server / Azure Synapse](transact/README.md)|T-SQL, stored procedures|
|[BigQuery](bigquery/README.md)|Google BigQuery|
|[Redshift](redshift/README.md)|Amazon Redshift|
|[PostgreSQL / Greenplum / Netezza](postgres/README.md)|PostgreSQL family|
|[Hive / Spark / Databricks](hive/README.md)|Apache Hive, Spark SQL, Databricks|
|[DB2](db2/README.md)|IBM DB2|
|[Vertica](vertica/README.md)|HP Vertica|
|[Sybase](sybase/README.md)|Sybase IQ|
|[SSIS](ssis/README.md)|SQL Server Integration Services|
|[General](general/README.md)|Cross-platform references|

## Key Translation Topics

Each database folder typically contains:

- **Data Types** - Mapping tables from source to Snowflake types
- **DDL Statements** - CREATE TABLE, VIEW, PROCEDURE translations
- **DML Statements** - INSERT, UPDATE, DELETE, MERGE patterns
- **Functions** - Built-in function equivalents
- **Query Syntax** - SELECT statement differences
- **Procedural Code** - Stored procedure to Snowflake Scripting/JavaScript

## Usage in dbt Migrations

When converting source database objects to dbt models:

1. Use data type mappings to ensure compatible column definitions
2. Translate proprietary functions to Snowflake equivalents
3. Convert procedural logic to declarative dbt SQL where possible
4. Break complex procedures into multiple dbt models
5. Implement appropriate incremental strategies

See the main [dbt-migration skill](../SKILL.md) for complete conversion guidelines.
