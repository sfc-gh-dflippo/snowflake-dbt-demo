---
auto_generated: true
description: Amazon Redshift, which uses PL/pgSQL for procedural logic, does not have
  a native DECLARE CONTINUE HANDLER statement in the same way as systems like DB2
  or Teradata. In Redshift, exception handling is
last_scraped: '2026-01-14T16:53:37.764402+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-continue-handler
title: SnowConvert AI - Redshift - CONTINUE HANDLER | Snowflake Documentation
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
          + [SQL Server-Azure Synapse](../transact/README.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](README.md)

            - [Basic Elements](redshift-basic-elements.md)
            - [Expressions](redshift-expressions.md)
            - [Conditions](redshift-conditions.md)
            - [Data types](redshift-data-types.md)
            - [SQL Statements](redshift-sql-statements.md)

              * [CONTINUE HANDLER](redshift-continue-handler.md)
              * [EXIT HANDLER](redshift-exit-handler.md)
              * [CREATE TABLE](redshift-sql-statements-create-table.md)
              * [CREATE TABLE AS](redshift-sql-statements-create-table-as.md)
              * [CREATE PROCEDURE](rs-sql-statements-create-procedure.md)
              * [SELECT](rs-sql-statements-select.md)
              * [SELECT INTO](rs-sql-statements-select-into.md)
            - [Functions](redshift-functions.md)
            - [System Catalog Tables](redshift-system-catalog.md)
            - ETL And BI Repointing

              - [Power BI Redshift Repointing](etl-bi-repointing/power-bi-redshift-repointing.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)[SQL Statements](redshift-sql-statements.md)CONTINUE HANDLER

# SnowConvert AI - Redshift - CONTINUE HANDLER[¶](#snowconvert-ai-redshift-continue-handler "Link to this heading")

## Description[¶](#description "Link to this heading")

Amazon Redshift, which uses PL/pgSQL for procedural logic, does not have a native `DECLARE CONTINUE HANDLER` statement in the same way as systems like DB2 or Teradata. In Redshift, exception handling is managed through `EXCEPTION` blocks within procedures.

However, when migrating code from database systems that use CONTINUE HANDLERs (such as DB2, Teradata, or other systems), SnowConvert AI transforms these constructs into equivalent Snowflake Scripting exception handling mechanisms.

A CONTINUE HANDLER allows execution to continue after an error occurs, performing specific actions when certain conditions are met. In Snowflake, this behavior is emulated using EXCEPTION blocks with appropriate error handling logic.

For more information about Redshift exception handling, see [Exception Handling in PL/pgSQL](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors).

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

Redshift does not have native CONTINUE HANDLER syntax. However, when converting from other database systems, the source pattern typically looks like:

```
-- Pattern from source systems (e.g., DB2, Teradata)
DECLARE CONTINUE HANDLER FOR condition_value
  handler_action_statement;
```

Copy

In Redshift, exception handling uses:

```
BEGIN
  -- statements
EXCEPTION
  WHEN condition THEN
    -- handler statements
END;
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### CONTINUE HANDLER Conversion to Snowflake[¶](#continue-handler-conversion-to-snowflake "Link to this heading")

When migrating stored procedures from systems with CONTINUE HANDLER to Snowflake via Redshift, SnowConvert AI transforms them into Snowflake-compatible exception handling.

#### Input Code:[¶](#input-code "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#source-db2-teradata-pattern "Link to this heading")

```
-- Example pattern from source system
CREATE PROCEDURE example_handler_procedure()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLSTATE '02000'
    BEGIN
        -- Handler action: log the error
        INSERT INTO error_log VALUES (CURRENT_TIMESTAMP, 'No data found');
    END;
    
    -- Main procedure logic
    SELECT column1 INTO result_var FROM table1 WHERE id = 999;
    INSERT INTO results VALUES (result_var);
END;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake Scripting[¶](#snowflake-scripting "Link to this heading")

```
CREATE OR REPLACE PROCEDURE example_handler_procedure()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        result_var VARCHAR;
    BEGIN
        BEGIN
            -- Main procedure logic
            SELECT column1 INTO result_var FROM table1 WHERE id = 999;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                -- Handler action: log the error
                INSERT INTO error_log 
                VALUES (CURRENT_TIMESTAMP(), 'No data found');
                -- Continue execution by not re-raising
        END;
        
        INSERT INTO results VALUES (result_var);
    END;
$$;
```

Copy

### CONTINUE HANDLER with SQLEXCEPTION[¶](#continue-handler-with-sqlexception "Link to this heading")

#### Input Code:[¶](#id1 "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#id2 "Link to this heading")

```
CREATE PROCEDURE multi_statement_handler()
BEGIN
    DECLARE error_count INT DEFAULT 0;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        SET error_count = error_count + 1;
    END;
    
    -- Multiple statements that might fail
    UPDATE table1 SET status = 'processed' WHERE id = -1;
    DELETE FROM table2 WHERE amount = 0/0;
    INSERT INTO table3 VALUES (1, 'Success');
END;
```

Copy

#### Output Code:[¶](#id3 "Link to this heading")

##### Snowflake Scripting[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE multi_statement_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        error_count INT := 0;
    BEGIN
        -- Multiple statements with individual exception handling
        BEGIN
            UPDATE table1 SET status = 'processed' WHERE id = -1;
        EXCEPTION
            WHEN OTHER THEN
                error_count := error_count + 1;
        END;
        
        BEGIN
            DELETE FROM table2 WHERE amount = 0/0;
        EXCEPTION
            WHEN OTHER THEN
                error_count := error_count + 1;
        END;
        
        INSERT INTO table3 VALUES (1, 'Success');
    END;
$$;
```

Copy

### CONTINUE HANDLER for NOT FOUND[¶](#continue-handler-for-not-found "Link to this heading")

#### Input Code:[¶](#id5 "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#id6 "Link to this heading")

```
CREATE PROCEDURE cursor_with_handler()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE val INT;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET done = 1;
    
    DECLARE cur CURSOR FOR SELECT id FROM table1;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO val;
        IF done = 1 THEN
            LEAVE read_loop;
        END IF;
        -- Process val
        INSERT INTO results VALUES (val);
    END LOOP;
    
    CLOSE cur;
END;
```

Copy

#### Output Code:[¶](#id7 "Link to this heading")

##### Snowflake Scripting[¶](#id8 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE cursor_with_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        done INT := 0;
        val INT;
        cur CURSOR FOR SELECT id FROM table1;
    BEGIN
        OPEN cur;
        
        LOOP
            BEGIN
                FETCH cur INTO val;
            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    done := 1;
            END;
            
            IF (done = 1) THEN
                BREAK;
            END IF;
            
            -- Process val
            INSERT INTO results VALUES (val);
        END LOOP;
        
        CLOSE cur;
    END;
$$;
```

Copy

## Known Issues[¶](#known-issues "Link to this heading")

### Limited CONTINUE HANDLER Emulation[¶](#limited-continue-handler-emulation "Link to this heading")

The conversion from CONTINUE HANDLER to Snowflake exception handling has some limitations:

1. **Execution Flow**: True CONTINUE HANDLER behavior (continuing from the exact point of error) cannot be fully replicated in Snowflake.
2. **Performance**: Wrapping individual statements in exception blocks can impact performance.
3. **Granularity**: Statement-level exception handling may be required to properly emulate CONTINUE HANDLER behavior.

### SQLSTATE Mapping[¶](#sqlstate-mapping "Link to this heading")

Not all SQLSTATE codes from source systems map directly to Snowflake exception types. SnowConvert AI performs best-effort mapping:

* `SQLSTATE '02000'` (NO DATA) → `NO_DATA_FOUND`
* `SQLSTATE '23xxx'` (Integrity Constraint Violation) → `STATEMENT_ERROR`
* Generic SQLEXCEPTION → `OTHER`

#### Known Issues[¶](#id9 "Link to this heading")

When migrating CONTINUE HANDLER patterns from other systems to Redshift and then to Snowflake, be aware that exception handling behavior may differ between systems. Thorough testing is recommended to ensure the converted code maintains the intended behavior.

### SQLWARNING Handling[¶](#sqlwarning-handling "Link to this heading")

Source systems that use CONTINUE HANDLER for SQLWARNING conditions present special challenges:

* Snowflake does not distinguish between warnings and errors in the same way
* Warnings in source systems may be errors in Snowflake
* Manual review of warning handling logic is recommended

#### Example[¶](#example "Link to this heading")

##### Source Pattern[¶](#source-pattern "Link to this heading")

```
DECLARE CONTINUE HANDLER FOR SQLWARNING
BEGIN
    INSERT INTO warning_log VALUES (SQLCODE, 'Warning occurred');
END;
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
-- Warning handling may need to be implemented through validation logic
BEGIN
    -- Perform validation before operation
    IF EXISTS (SELECT 1 FROM table1 WHERE condition) THEN
        INSERT INTO warning_log VALUES (0, 'Warning occurred');
    END IF;
EXCEPTION
    WHEN OTHER THEN
        -- Handle actual errors
        INSERT INTO error_log VALUES (:SQLCODE, :SQLERRM);
END;
```

Copy

## Best Practices[¶](#best-practices "Link to this heading")

When working with converted CONTINUE HANDLER code in Snowflake:

1. **Test Thoroughly**: Verify that error handling behavior matches the original system’s behavior.
2. **Review Performance**: Multiple exception blocks can impact performance; consider refactoring where appropriate.
3. **Validate Error Conditions**: Ensure that all error conditions from the source system are properly handled.
4. **Use Transactions**: Leverage Snowflake’s transaction support for data consistency.
5. **Monitor Execution**: Use Snowflake’s logging capabilities to track exception handling.

## Related Documentation[¶](#related-documentation "Link to this heading")

* [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
* [Redshift Exception Handling](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors)
* [CREATE PROCEDURE](rs-sql-statements-create-procedure)

## See Also[¶](#see-also "Link to this heading")

* [EXCEPTION](rs-sql-statements-create-procedure.html#exception)
* [RAISE](rs-sql-statements-create-procedure.html#raise)
* [DECLARE](rs-sql-statements-create-procedure.html#declare)

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