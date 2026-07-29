# Power BI Repointing

SnowConvert AI's Power BI Repointing feature redirects Power BI reports from source databases to
migrated Snowflake databases.

## Supported Source Databases

- SQL Server
- Oracle
- Teradata
- Amazon Redshift
- Azure Synapse
- PostgreSQL

## What Gets Converted

- Table and view connections
- Embedded SQL queries within Power BI connectors
- Column references (renamed based on DDLs or Power BI references)

## Output Structure

```text
Output/
├── repointing_output/           # Repointed Power BI reports
│   ├── report1.pbit
│   └── report2.pbit
└── power_bi_sql_queries/        # Extracted SQL for review
    ├── query1.sql
    └── query2.sql
```

## Prerequisites

- SnowConvert AI installed
- Power BI reports saved as `.pbit` format (not `.pbix`)
- Database objects deployed in Snowflake before opening repointed reports

## How to Save Reports as .pbit

1. Open your .pbix file in Power BI Desktop
2. File > Save as > Browse this device
3. Select .pbit extension
4. Save (optionally add description)

## Migration Steps

1. Locate all .pbit files in a folder
2. In SnowConvert AI, add path in "Where is your SSIS/Power BI project(s)?" section
3. Continue migration steps
4. Review ETLAndBiRepointing report for transformation details
5. Run migrated DDLs in Snowflake
6. Open repointed Power BI report
7. Fill parameters: SF_SERVER_LINK, SF_DB_NAME, SF_WAREHOUSE_NAME
8. Provide Snowflake credentials
9. Verify visualizations load correctly

## Power BI Parameters

Repointed reports include parameters for Snowflake connection:

- `SF_SERVER_LINK` - Snowflake account URL
- `SF_DB_NAME` - Database name
- `SF_WAREHOUSE_NAME` - Warehouse name

## Capabilities

- Repointing tables, views, and embedded SQL
- Maintaining M Language logic after connection steps
- Converting queries saved as expressions
- Column renaming based on DDLs or Power BI references
- Multi-database and multi-schema support

## Limitations

- Dynamic SQL in connectors not supported
- Column renaming may require manual adjustment if DDLs not provided
- Functions and procedures only supported for SQL Server and Azure Synapse connectors

## Documentation

- [Power BI Repointing Guide](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/power-bi-repointing-general)
- [SQL Server Repointing](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/etl-bi-repointing/power-bi-transact-repointing)
- [Oracle Repointing](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/etl-bi-repointing/power-bi-oracle-repointing)
- [Teradata Repointing](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/etl-bi-repointing/power-bi-teradata-repointing)
- [Redshift Repointing](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/etl-bi-repointing/power-bi-redshift-repointing)
- [PostgreSQL Repointing](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/etl-bi-repointing/power-bi-postgres-repointing)
