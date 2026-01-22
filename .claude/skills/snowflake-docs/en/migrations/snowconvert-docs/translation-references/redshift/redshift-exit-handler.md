---
auto_generated: true
description: 'Amazon Redshift, which uses PL/pgSQL for procedural logic, supports
  EXIT handlers in stored procedures through EXCEPTION blocks. An EXIT handler terminates
  the current block when a specific condition '
last_scraped: '2026-01-14T16:53:38.528505+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-exit-handler
title: SnowConvert AI - Redshift - EXIT HANDLER | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)[SQL Statements](redshift-sql-statements.md)EXIT HANDLER

# SnowConvert AI - Redshift - EXIT HANDLER[¶](#snowconvert-ai-redshift-exit-handler "Link to this heading")

## Description[¶](#description "Link to this heading")

Amazon Redshift, which uses PL/pgSQL for procedural logic, supports EXIT handlers in stored procedures through EXCEPTION blocks. An EXIT handler terminates the current block when a specific condition is met and transfers control to the handler code.

When migrating code from database systems that use EXIT HANDLERs (such as DB2, Teradata, or other systems) to Snowflake, SnowConvert AI transforms these constructs into equivalent Snowflake Scripting exception handling mechanisms.

An EXIT HANDLER causes the procedure to exit the current block and return control to the caller after executing the handler code. In Snowflake, this behavior is emulated using EXCEPTION blocks with appropriate logic.

For more information about Redshift exception handling, see [Exception Handling in PL/pgSQL](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors).

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

Redshift does not have native `DECLARE EXIT HANDLER` syntax. However, when converting from other database systems, the source pattern typically looks like:

```
-- Pattern from source systems (e.g., DB2, Teradata)
DECLARE EXIT HANDLER FOR condition_value
  handler_action_statement;
```

Copy

In Redshift, exception handling uses:

```
BEGIN
  -- statements
EXCEPTION
  WHEN condition THEN
    -- handler statements that exit the block
END;
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### EXIT HANDLER Conversion to Snowflake[¶](#exit-handler-conversion-to-snowflake "Link to this heading")

When migrating stored procedures from systems with EXIT HANDLER to Snowflake via Redshift, SnowConvert AI transforms them into Snowflake-compatible exception handling.

#### Input Code:[¶](#input-code "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#source-db2-teradata-pattern "Link to this heading")

```
-- Example pattern from source system
CREATE PROCEDURE exit_handler_procedure()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        INSERT INTO error_log VALUES (CURRENT_TIMESTAMP, 'Error occurred, exiting');
        ROLLBACK;
    END;
    
    -- Main procedure logic
    INSERT INTO orders VALUES (1, 100.00);
    UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;
    
    -- This will NOT execute if an error occurred
    INSERT INTO audit_log VALUES ('Transaction completed');
END;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake Scripting[¶](#snowflake-scripting "Link to this heading")

```
CREATE OR REPLACE PROCEDURE exit_handler_procedure()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    BEGIN
        -- Main procedure logic
        INSERT INTO orders VALUES (1, 100.00);
        UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;
        
        -- This will NOT execute if an error occurred
        INSERT INTO audit_log VALUES ('Transaction completed');
        
        EXCEPTION
            WHEN OTHER THEN
                BEGIN
                    INSERT INTO error_log 
                    VALUES (CURRENT_TIMESTAMP(), 'Error occurred, exiting');
                    ROLLBACK;
                END;
    END;
$$;
```

Copy

### EXIT HANDLER with Specific SQLSTATE[¶](#exit-handler-with-specific-sqlstate "Link to this heading")

#### Input Code:[¶](#id1 "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#id2 "Link to this heading")

```
CREATE PROCEDURE specific_error_exit()
BEGIN
    DECLARE EXIT HANDLER FOR SQLSTATE '23505'
    BEGIN
        INSERT INTO error_log VALUES ('Duplicate key error');
    END;
    
    INSERT INTO users VALUES (1, 'John');
    INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key
    
    -- This will NOT execute
    INSERT INTO success_log VALUES ('Completed');
END;
```

Copy

#### Output Code:[¶](#id3 "Link to this heading")

##### Snowflake Scripting[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE specific_error_exit()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    BEGIN
        INSERT INTO users VALUES (1, 'John');
        INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key
        
        -- This will NOT execute
        INSERT INTO success_log VALUES ('Completed');
        
        EXCEPTION
            WHEN OTHER EXIT THEN
                CASE
                    WHEN (SQLSTATE = '23505') THEN
                        INSERT INTO error_log VALUES ('Duplicate key error')
                END;
    END;
$$;
```

Copy

### EXIT HANDLER for NOT FOUND[¶](#exit-handler-for-not-found "Link to this heading")

#### Input Code:[¶](#id5 "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#id6 "Link to this heading")

```
CREATE PROCEDURE not_found_exit()
BEGIN
    DECLARE v_name VARCHAR(100);
    
    DECLARE EXIT HANDLER FOR NOT FOUND
        INSERT INTO log_table VALUES ('No data found, exiting');
    
    SELECT name INTO v_name FROM employees WHERE id = 9999;
    
    -- This will NOT execute if no data found
    INSERT INTO results VALUES (v_name);
END;
```

Copy

#### Output Code:[¶](#id7 "Link to this heading")

##### Snowflake Scripting[¶](#id8 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE not_found_exit()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        v_name VARCHAR(100);
    BEGIN
        SELECT name INTO v_name FROM employees WHERE id = 9999;
        
        -- This will NOT execute if no data found
        INSERT INTO results VALUES (v_name);
        
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                INSERT INTO log_table VALUES ('No data found, exiting');
    END;
$$;
```

Copy

### EXIT HANDLER with Cursor[¶](#exit-handler-with-cursor "Link to this heading")

#### Input Code:[¶](#id9 "Link to this heading")

##### Source (DB2/Teradata Pattern)[¶](#id10 "Link to this heading")

```
CREATE PROCEDURE cursor_exit_handler()
BEGIN
    DECLARE v_id INT;
    DECLARE v_name VARCHAR(100);
    DECLARE v_count INT := 0;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        INSERT INTO error_log VALUES ('Error in cursor processing');
        RETURN -1;
    END;
    
    DECLARE cur CURSOR FOR SELECT id, name FROM employees;
    
    OPEN cur;
    LOOP
        FETCH cur INTO v_id, v_name;
        EXIT WHEN NOT FOUND;
        
        -- Process each row
        INSERT INTO processed_employees VALUES (v_id, v_name);
        v_count := v_count + 1;
    END LOOP;
    CLOSE cur;
    
    RETURN v_count;
END;
```

Copy

#### Output Code:[¶](#id11 "Link to this heading")

##### Snowflake Scripting[¶](#id12 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE cursor_exit_handler()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        v_id INT;
        v_name VARCHAR(100);
        v_count INT := 0;
        cur CURSOR FOR SELECT id, name FROM employees;
    BEGIN
        OPEN cur;
        LOOP
            FETCH cur INTO v_id, v_name;
            IF (SQLCODE != 0) THEN
                BREAK;
            END IF;
            
            -- Process each row
            INSERT INTO processed_employees VALUES (v_id, v_name);
            v_count := v_count + 1;
        END LOOP;
        CLOSE cur;
        
        RETURN v_count;
        
        EXCEPTION
            WHEN OTHER THEN
                BEGIN
                    INSERT INTO error_log VALUES ('Error in cursor processing');
                    RETURN -1;
                END;
    END;
$$;
```

Copy

## Known Issues[¶](#known-issues "Link to this heading")

### EXIT HANDLER Behavior[¶](#exit-handler-behavior "Link to this heading")

The conversion from EXIT HANDLER to Snowflake exception handling provides equivalent termination behavior:

1. **Block Termination**: Both EXIT HANDLER and Snowflake EXCEPTION blocks terminate the current BEGIN…END block.
2. **Return Control**: After executing the handler code, control returns to the caller.
3. **Execution Flow**: Statements after the error point are not executed.

### Multiple EXIT Handlers[¶](#multiple-exit-handlers "Link to this heading")

When multiple EXIT HANDLERs are defined with different conditions, they must be merged into conditional logic:

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
    WHEN OTHER EXIT THEN
        CASE
            WHEN (SQLSTATE = '23505') THEN
                INSERT INTO log VALUES ('Duplicate key')
            ELSE
                INSERT INTO log VALUES ('General error')
        END;
```

Copy

### Mixed CONTINUE and EXIT Handlers[¶](#mixed-continue-and-exit-handlers "Link to this heading")

Source systems that allow mixing CONTINUE and EXIT handlers in the same block present special challenges. Snowflake does not support this pattern in a single EXCEPTION block.

#### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0114](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0114): MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING

### SQLSTATE Mapping[¶](#sqlstate-mapping "Link to this heading")

Not all SQLSTATE codes from source systems map directly to Snowflake exception types. SnowConvert AI performs best-effort mapping:

| Source SQLSTATE | Condition | Snowflake Equivalent |
| --- | --- | --- |
| 02000 | NO DATA | NO\_DATA\_FOUND |
| 23xxx | Integrity Constraint | STATEMENT\_ERROR |
| 42xxx | Syntax Error | STATEMENT\_ERROR |
| Other | General | OTHER |

## Best Practices[¶](#best-practices "Link to this heading")

When working with converted EXIT HANDLER code in Snowflake:

1. **Understand Exit Semantics**: EXIT handlers terminate the current block. Verify this matches your requirements.
2. **Test Error Conditions**: Thoroughly test all error scenarios to ensure proper exit behavior.
3. **Use Return Values**: Consider using RETURN statements in exception handlers to communicate status.
4. **Implement Logging**: Add comprehensive logging to track when and why procedures exit.
5. **Transaction Management**: Use Snowflake’s transaction support to maintain data consistency.
6. **Nested Blocks**: Remember that EXIT only affects the current block, not outer blocks or the entire procedure.
7. **Error Information**: Capture error details (SQLCODE, SQLERRM, SQLSTATE) in exception handlers for debugging.

## Related Documentation[¶](#related-documentation "Link to this heading")

* [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
* [Redshift Exception Handling](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors)
* [CREATE PROCEDURE](rs-sql-statements-create-procedure)

## See Also[¶](#see-also "Link to this heading")

* [CONTINUE HANDLER](redshift-continue-handler)
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