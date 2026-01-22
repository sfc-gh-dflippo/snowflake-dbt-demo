---
auto_generated: true
description: 'In SQL Server and Azure Synapse Analytics, exception handling is primarily
  managed through TRY...CATCH blocks. Unlike some other database systems (such as
  Teradata or DB2), SQL Server does not have a '
last_scraped: '2026-01-14T16:54:02.261423+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-continue-handler
title: SnowConvert AI - SQL Server-Azure Synapse - CONTINUE HANDLER | Snowflake Documentation
---

1. [Overview](../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../guides/overview-db.md)
8. [Data types](../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../README.md)

    * Tools

      * [SnowConvert AI](../../overview.md)

        + General

          + [About](../../general/about.md)
          + [Getting Started](../../general/getting-started/README.md)
          + [Terms And Conditions](../../general/terms-and-conditions/README.md)
          + [Release Notes](../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../general/user-guide/project-creation.md)
            + [Extraction](../../general/user-guide/extraction.md)
            + [Deployment](../../general/user-guide/deployment.md)
            + [Data Migration](../../general/user-guide/data-migration.md)
            + [Data Validation](../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../general/technical-documentation/README.md)
          + [Contact Us](../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../general/README.md)
          + [Teradata](../teradata/README.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](README.md)

            - [ANSI NULLS](transact-ansi-nulls.md)
            - [QUOTED\_IDENTIFIER](transact-quoted-identifier.md)
            - [Built-in Functions](transact-built-in-functions.md)
            - [Built-in Procedures](transact-built-in-procedures.md)
            - Data Definition Language

              - [ALTER TABLE](transact-alter-statement.md)
              - [CONTINUE HANDLER](transact-continue-handler.md)
              - [EXIT HANDLER](transact-exit-handler.md)
              - [CREATE FUNCTION](transact-create-function.md)
              - [CREATE INDEX](transact-create-index.md)
              - [CREATE MATERIALIZED VIEW](transact-create-materialized-view.md)
              - [CREATE PROCEDURE (JavaScript)](transact-create-procedure.md)")
              - [CREATE PROCEDURE (Snowflake Scripting)](transact-create-procedure-snow-script.md)")
              - [CREATE TABLE](transact-create-table.md)
              - [CREATE VIEW](transact-create-view.md)
            - [Data Types](transact-data-types.md)
            - [Data Manipulation Language](transact-dmls.md)
            - [General Statements](transact-general-statements.md)
            - [SELECT](transact-select.md)
            - [SYSTEM TABLES](transact-system-tables.md)
            - ETL And BI Repointing

              - [Power BI Transact and Synapse Repointing](etl-bi-repointing/power-bi-transact-repointing.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](../db2/README.md)
          + [SSIS](../ssis/README.md)
        + [Migration Assistant](../../migration-assistant/README.md)
        + [Data Validation CLI](../../data-validation-cli/index.md)
        + [AI Verification](../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../guides/teradata.md)
      * [Databricks](../../../guides/databricks.md)
      * [SQL Server](../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../guides/redshift.md)
      * [Oracle](../../../guides/oracle.md)
      * [Azure Synapse](../../../guides/azuresynapse.md)
15. [Queries](../../../../guides/overview-queries.md)
16. [Listings](../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../guides/overview-alerts.md)
25. [Security](../../../../guides/overview-secure.md)
26. [Data Governance](../../../../guides/overview-govern.md)
27. [Privacy](../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../guides/overview-cost.md)

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)Data Definition LanguageCONTINUE HANDLER

# SnowConvert AI - SQL Server-Azure Synapse - CONTINUE HANDLER[¶](#snowconvert-ai-sql-server-azure-synapse-continue-handler "Link to this heading")

## Description[¶](#description "Link to this heading")

In SQL Server and Azure Synapse Analytics, exception handling is primarily managed through `TRY...CATCH` blocks. Unlike some other database systems (such as Teradata or DB2), SQL Server does not have a native `DECLARE CONTINUE HANDLER` statement.

However, when migrating code from other database systems that use CONTINUE HANDLERs, SnowConvert AI transforms these constructs into equivalent Snowflake Scripting exception handling mechanisms.

A CONTINUE HANDLER in the source system allows execution to continue after an error occurs, performing specific actions when certain conditions are met. In Snowflake, this is achieved using EXCEPTION blocks with conditional logic.

For more information about SQL Server error handling, see [TRY…CATCH (Transact-SQL)](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql).

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

SQL Server does not have native CONTINUE HANDLER syntax. However, when converting from other database systems, the source pattern typically looks like:

```
-- Pattern from source systems (e.g., DB2, Teradata)
DECLARE CONTINUE HANDLER FOR condition_value
  handler_action_statement;
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### CONTINUE HANDLER Conversion from DB2/Teradata[¶](#continue-handler-conversion-from-db2-teradata "Link to this heading")

When migrating stored procedures from DB2 or Teradata that contain CONTINUE HANDLER declarations, SnowConvert AI transforms them into Snowflake-compatible exception handling.

#### Input Code:[¶](#input-code "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#source-db2-teradata-pattern "Link to this heading")

```
-- Example pattern from source system
CREATE PROCEDURE example_procedure()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLSTATE '02000'
    BEGIN
        -- Handler action
        SET error_count = error_count + 1;
    END;
    
    -- Main procedure logic
    SELECT * FROM non_existent_table;
END;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake Scripting[¶](#snowflake-scripting "Link to this heading")

```
CREATE OR REPLACE PROCEDURE example_procedure()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        error_count INTEGER := 0;
    BEGIN
        BEGIN
            -- Main procedure logic
            SELECT * FROM non_existent_table;
        EXCEPTION
            WHEN OTHER THEN
                -- Handler action
                error_count := error_count + 1;
                -- Continue execution
        END;
    END;
$$;
```

Copy

### CONTINUE HANDLER with SQLEXCEPTION[¶](#continue-handler-with-sqlexception "Link to this heading")

#### Input Code:[¶](#id1 "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#id2 "Link to this heading")

```
CREATE PROCEDURE handler_example()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO error_log VALUES (SQLCODE, SQLERRM);
    
    -- Procedure body with multiple statements
    DELETE FROM table1 WHERE id = 0/0;
    INSERT INTO table2 VALUES (1, 'Success');
END;
```

Copy

#### Output Code:[¶](#id3 "Link to this heading")

##### Snowflake Scripting[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        BEGIN
            -- Procedure body with multiple statements
            DELETE FROM table1 WHERE id = 0/0;
        EXCEPTION
            WHEN OTHER THEN
                INSERT INTO error_log 
                SELECT :SQLCODE, :SQLERRM;
                -- Continue execution
        END;
        
        INSERT INTO table2 VALUES (1, 'Success');
    END;
$$;
```

Copy

## Known Issues[¶](#known-issues "Link to this heading")

### Limited CONTINUE HANDLER Support[¶](#limited-continue-handler-support "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

SQL Server’s native `TRY...CATCH` mechanism does not have an exact equivalent to CONTINUE HANDLER. When an error occurs in a TRY block, control immediately passes to the CATCH block, and execution does not continue from the point of error.

SnowConvert AI attempts to emulate CONTINUE HANDLER behavior in Snowflake, but there are limitations:

1. **Execution Flow**: True CONTINUE HANDLER behavior (continuing from the exact point of error) cannot be fully replicated.
2. **Statement-level Wrapping**: Individual statements may need to be wrapped in separate exception blocks.
3. **Performance**: Multiple nested exception blocks can impact performance.

#### Known Issues[¶](#id5 "Link to this heading")

When migrating CONTINUE HANDLER patterns from other database systems through SQL Server to Snowflake, be aware that exception handling behavior may differ. The TRY…CATCH pattern in SQL Server is converted to Snowflake’s EXCEPTION blocks, but semantic differences may exist. Thorough testing is recommended to ensure the converted code maintains the intended behavior.

### SQLWARNING and NOT FOUND Conditions[¶](#sqlwarning-and-not-found-conditions "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

CONTINUE HANDLERs for SQLWARNING and NOT FOUND conditions require special handling in Snowflake:

* **SQLWARNING**: Snowflake does not distinguish between warnings and errors in the same way as source systems.
* **NOT FOUND**: Typically used for cursor operations or SELECT INTO statements that return no rows.

#### Example[¶](#example "Link to this heading")

##### Source Pattern[¶](#source-pattern "Link to this heading")

```
DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET done = TRUE;
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
-- Handled through conditional logic rather than exception handling
IF (SELECT COUNT(*) FROM table1) = 0 THEN
    done := TRUE;
END IF;
```

Copy

## Best Practices[¶](#best-practices "Link to this heading")

When working with converted CONTINUE HANDLER code:

1. **Review Exception Handling**: Verify that the converted exception handling logic matches the intended behavior.
2. **Test Error Scenarios**: Thoroughly test error conditions to ensure the application behavior is correct.
3. **Consider Refactoring**: In some cases, refactoring the error handling logic may provide better performance and maintainability.
4. **Use Transactions**: Leverage Snowflake’s transaction support to ensure data consistency.

## Related Documentation[¶](#related-documentation "Link to this heading")

* [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
* [SQL Server TRY…CATCH](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql)
* [TRY CATCH Translation Reference](transact-create-procedure-snow-script.html#try-catch)

## See Also[¶](#see-also "Link to this heading")

* [CREATE PROCEDURE](transact-create-procedure)
* [CREATE PROCEDURE - Snowflake Scripting](transact-create-procedure-snow-script)
* [General Statements](transact-general-statements)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Terms of Use

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [Description](#description)
2. [Grammar Syntax](#grammar-syntax)
3. [Sample Source Patterns](#sample-source-patterns)
4. [Known Issues](#known-issues)
5. [Best Practices](#best-practices)
6. [Related Documentation](#related-documentation)
7. [See Also](#see-also)