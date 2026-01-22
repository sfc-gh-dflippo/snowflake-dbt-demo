---
auto_generated: true
description: 'In SQL Server and Azure Synapse Analytics, exception handling is primarily
  managed through TRY...CATCH blocks. Unlike some other database systems (such as
  Teradata or DB2), SQL Server does not have a '
last_scraped: '2026-01-14T16:54:07.868310+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-exit-handler
title: SnowConvert AI - SQL Server-Azure Synapse - EXIT HANDLER | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)Data Definition LanguageEXIT HANDLER

# SnowConvert AI - SQL Server-Azure Synapse - EXIT HANDLER[¶](#snowconvert-ai-sql-server-azure-synapse-exit-handler "Link to this heading")

## Description[¶](#description "Link to this heading")

In SQL Server and Azure Synapse Analytics, exception handling is primarily managed through `TRY...CATCH` blocks. Unlike some other database systems (such as Teradata or DB2), SQL Server does not have a native `DECLARE EXIT HANDLER` statement.

However, when migrating code from other database systems that use EXIT HANDLERs, SnowConvert AI transforms these constructs into equivalent Snowflake Scripting exception handling mechanisms.

An EXIT HANDLER in source systems terminates the current block when a specific condition is met and transfers control to the handler code before returning to the caller. In Snowflake, this is achieved using EXCEPTION blocks with appropriate exit behavior.

For more information about SQL Server error handling, see [TRY…CATCH (Transact-SQL)](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql).

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

SQL Server does not have native EXIT HANDLER syntax. However, when converting from other database systems, the source pattern typically looks like:

```
-- Pattern from source systems (e.g., DB2, Teradata)
DECLARE EXIT HANDLER FOR condition_value
  handler_action_statement;
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### EXIT HANDLER Conversion from DB2/Teradata[¶](#exit-handler-conversion-from-db2-teradata "Link to this heading")

When migrating stored procedures from DB2 or Teradata that contain EXIT HANDLER declarations, SnowConvert AI transforms them into Snowflake-compatible exception handling.

#### Input Code:[¶](#input-code "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#source-db2-teradata-pattern "Link to this heading")

```
-- Example pattern from source system
CREATE PROCEDURE exit_handler_example()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        INSERT INTO error_log VALUES (SQLCODE, SQLERRM, CURRENT_TIMESTAMP);
        ROLLBACK;
    END;
    
    -- Main procedure logic
    INSERT INTO orders VALUES (1, 100.00);
    UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;
    
    -- This will NOT execute if an error occurred
    INSERT INTO audit_log VALUES ('Transaction completed successfully');
END;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake Scripting[¶](#snowflake-scripting "Link to this heading")

```
CREATE OR REPLACE PROCEDURE exit_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        -- Main procedure logic
        INSERT INTO orders VALUES (1, 100.00);
        UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;
        
        -- This will NOT execute if an error occurred
        INSERT INTO audit_log VALUES ('Transaction completed successfully');
        
        EXCEPTION
            WHEN OTHER THEN
                BEGIN
                    INSERT INTO error_log 
                    VALUES (:SQLCODE, :SQLERRM, CURRENT_TIMESTAMP());
                    ROLLBACK;
                END;
    END;
$$;
```

Copy

### EXIT HANDLER with Specific Error Codes[¶](#exit-handler-with-specific-error-codes "Link to this heading")

#### Input Code:[¶](#id1 "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#id2 "Link to this heading")

```
CREATE PROCEDURE specific_error_handler()
BEGIN
    DECLARE EXIT HANDLER FOR SQLSTATE '23505'
    BEGIN
        INSERT INTO error_log VALUES ('Duplicate key error');
        RETURN -1;
    END;
    
    INSERT INTO users VALUES (1, 'John Doe');
    INSERT INTO users VALUES (1, 'Jane Doe');  -- Will trigger handler
    
    -- This will NOT execute
    INSERT INTO success_log VALUES ('All inserts completed');
END;
```

Copy

#### Output Code:[¶](#id3 "Link to this heading")

##### Snowflake Scripting[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE specific_error_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        INSERT INTO users VALUES (1, 'John Doe');
        INSERT INTO users VALUES (1, 'Jane Doe');  -- Will trigger handler
        
        -- This will NOT execute
        INSERT INTO success_log VALUES ('All inserts completed');
        
        EXCEPTION
            WHEN OTHER THEN
                LET errcode := :SQLCODE;
                LET sqlerrmsg := :SQLERRM;
                IF (errcode = '100183' OR CONTAINS(sqlerrmsg, 'duplicate key')) THEN
                    INSERT INTO error_log VALUES ('Duplicate key error');
                    RETURN -1;
                ELSE
                    RAISE;
                END IF;
    END;
$$;
```

Copy

### EXIT HANDLER with NOT FOUND[¶](#exit-handler-with-not-found "Link to this heading")

#### Input Code:[¶](#id5 "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#id6 "Link to this heading")

```
CREATE PROCEDURE not_found_handler()
BEGIN
    DECLARE v_name VARCHAR(100);
    
    DECLARE EXIT HANDLER FOR NOT FOUND
    BEGIN
        INSERT INTO log_table VALUES ('Record not found');
        RETURN 0;
    END;
    
    SELECT name INTO v_name FROM employees WHERE id = 9999;
    
    -- This will NOT execute if no record found
    INSERT INTO results VALUES (v_name);
END;
```

Copy

#### Output Code:[¶](#id7 "Link to this heading")

##### Snowflake Scripting[¶](#id8 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE not_found_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        v_name VARCHAR(100);
    BEGIN
        SELECT name INTO v_name FROM employees WHERE id = 9999;
        
        -- This will NOT execute if no record found
        INSERT INTO results VALUES (v_name);
        
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                BEGIN
                    INSERT INTO log_table VALUES ('Record not found');
                    RETURN 0;
                END;
    END;
$$;
```

Copy

## Known Issues[¶](#known-issues "Link to this heading")

### EXIT HANDLER Behavior[¶](#exit-handler-behavior "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

SQL Server’s native `TRY...CATCH` mechanism provides similar functionality to EXIT HANDLER. When an error occurs in a TRY block, control passes to the CATCH block, and execution does not continue after the CATCH block in the current scope.

SnowConvert AI transforms EXIT HANDLER patterns to Snowflake EXCEPTION blocks, which provide equivalent exit behavior:

1. **Execution Termination**: The current block is terminated when an exception occurs.
2. **Control Flow**: Control passes to the exception handler, executes the handler code, then exits the block.
3. **Return Behavior**: The procedure can return a value or status from within the exception handler.

### Multiple EXIT Handlers[¶](#multiple-exit-handlers "Link to this heading")

When multiple EXIT HANDLERs are defined in the source system, they must be merged into a single EXCEPTION block with conditional logic:

#### Source Pattern[¶](#source-pattern "Link to this heading")

```
DECLARE EXIT HANDLER FOR SQLSTATE '23505'
    INSERT INTO log VALUES ('Duplicate key');
    
DECLARE EXIT HANDLER FOR SQLEXCEPTION
    INSERT INTO log VALUES ('General error');
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
EXCEPTION
    WHEN OTHER THEN
        LET errcode := :SQLCODE;
        LET sqlerrmsg := :SQLERRM;
        IF (errcode = '100183' OR CONTAINS(sqlerrmsg, 'duplicate key')) THEN
            INSERT INTO log VALUES ('Duplicate key');
        ELSE
            INSERT INTO log VALUES ('General error');
        END IF;
```

Copy

### Mixed CONTINUE and EXIT Handlers[¶](#mixed-continue-and-exit-handlers "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

Source systems may allow mixing CONTINUE and EXIT handlers in the same block. This pattern cannot be directly replicated in Snowflake, as EXCEPTION blocks handle errors uniformly.

When this pattern is encountered:

* Separate EXCEPTION blocks may be generated
* An EWI warning (`SSC-EWI-0114`) is added
* Manual review is recommended

#### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0114](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0114): MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING

## Best Practices[¶](#best-practices "Link to this heading")

When working with converted EXIT HANDLER code:

1. **Understand Exit Semantics**: EXIT handlers terminate the current block. Verify this matches your application’s requirements.
2. **Test Error Scenarios**: Thoroughly test all error conditions to ensure proper exit behavior.
3. **Use Transactions**: Leverage Snowflake’s transaction support for data consistency.
4. **Return Values**: Use RETURN statements in exception handlers to communicate exit status to callers.
5. **Logging**: Implement comprehensive error logging to track when and why procedures exit.
6. **Nested Blocks**: Remember that EXIT behavior only affects the current block, not outer blocks.

## Related Documentation[¶](#related-documentation "Link to this heading")

* [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
* [SQL Server TRY…CATCH](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql)
* [TRY CATCH Translation Reference](transact-create-procedure-snow-script.html#try-catch)

## See Also[¶](#see-also "Link to this heading")

* [CONTINUE HANDLER](transact-continue-handler)
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