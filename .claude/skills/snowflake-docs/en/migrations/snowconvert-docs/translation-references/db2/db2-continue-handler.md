---
auto_generated: true
description: A CONTINUE handler allows the execution to continue after a condition
  is encountered. When a condition occurs and a continue handler is invoked, control
  is passed to the handler. When the handler comp
last_scraped: '2026-01-14T16:53:05.675440+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-continue-handler
title: SnowConvert AI - IBM DB2 - CONTINUE HANDLER | Snowflake Documentation
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
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](README.md)

            - [CONTINUE HANDLER](db2-continue-handler.md)
            - [EXIT HANDLER](db2-exit-handler.md)
            - [CREATE TABLE](db2-create-table.md)
            - [CREATE VIEW](db2-create-view.md)
            - [CREATE PROCEDURE](db2-create-procedure.md)
            - [CREATE FUNCTION](db2-create-function.md)
            - [Data Types](db2-data-types.md)
            - [SELECT](db2-select-statement.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[IBM DB2](README.md)CONTINUE HANDLER

# SnowConvert AI - IBM DB2 - CONTINUE HANDLER[¶](#snowconvert-ai-ibm-db2-continue-handler "Link to this heading")

## Description[¶](#description "Link to this heading")

> A CONTINUE handler allows the execution to continue after a condition is encountered. When a condition occurs and a continue handler is invoked, control is passed to the handler. When the handler completes, control returns to the statement following the statement that raised the condition.

In IBM DB2, the `DECLARE CONTINUE HANDLER` statement is used to define actions that should be taken when specific SQL conditions or errors occur during procedure execution, while allowing the procedure to continue running.

When migrating from DB2 to Snowflake, SnowConvert AI transforms CONTINUE HANDLER declarations into equivalent Snowflake Scripting exception handling using EXCEPTION blocks with appropriate logic to continue execution.

For more information about DB2 condition handlers, see [IBM DB2 DECLARE HANDLER](https://www.ibm.com/docs/en/db2/11.5?topic=statements-declare-handler).

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
DECLARE CONTINUE HANDLER FOR condition_value [, ...]
  handler_action_statement;

-- Where condition_value can be:
-- SQLSTATE [VALUE] sqlstate_value
-- condition_name
-- SQLWARNING
-- SQLEXCEPTION
-- NOT FOUND
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### DECLARE CONTINUE HANDLER FOR SQLEXCEPTION[¶](#declare-continue-handler-for-sqlexception "Link to this heading")

The most common use case is handling SQL exceptions while allowing the procedure to continue.

#### Input Code:[¶](#input-code "Link to this heading")

##### IBM DB2[¶](#ibm-db2 "Link to this heading")

```
CREATE PROCEDURE error_handler_example()
LANGUAGE SQL
BEGIN
    DECLARE error_count INT DEFAULT 0;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        SET error_count = error_count + 1;
    END;
    
    -- These statements may cause errors
    INSERT INTO table1 VALUES (1/0);
    UPDATE table2 SET status = 'completed' WHERE id = -1;
    DELETE FROM table3 WHERE invalid_column = 'test';
    
    -- This will execute even if errors occurred above
    INSERT INTO error_summary VALUES (error_count);
END;
```

Copy

#### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE PROCEDURE error_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        error_count INT := 0;
    BEGIN
        -- Statements in procedure body
        INSERT INTO table1 VALUES (1/0);
        UPDATE table2 SET status = 'completed' WHERE id = -1;
        DELETE FROM table3 WHERE invalid_column = 'test';
        
        -- This will execute even if errors occurred above
        INSERT INTO error_summary VALUES (error_count);
        
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                error_count := error_count + 1;
    END;
$$;
```

Copy

### DECLARE CONTINUE HANDLER FOR SQLSTATE[¶](#declare-continue-handler-for-sqlstate "Link to this heading")

Handling specific SQLSTATE codes allows more granular control over error handling.

#### Input Code:[¶](#id1 "Link to this heading")

##### IBM DB2[¶](#id2 "Link to this heading")

```
CREATE PROCEDURE sqlstate_handler_example()
LANGUAGE SQL
BEGIN
    DECLARE duplicate_key_count INT DEFAULT 0;
    
    -- Handle duplicate key errors (SQLSTATE 23505)
    DECLARE CONTINUE HANDLER FOR SQLSTATE '23505'
    BEGIN
        SET duplicate_key_count = duplicate_key_count + 1;
    END;
    
    -- Attempt to insert multiple records
    INSERT INTO users VALUES (1, 'John');
    INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key
    INSERT INTO users VALUES (2, 'Bob');
    
    -- Log the results
    INSERT INTO process_log VALUES ('Duplicates found: ' || duplicate_key_count);
END;
```

Copy

#### Output Code:[¶](#id3 "Link to this heading")

##### Snowflake[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE sqlstate_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        duplicate_key_count INT := 0;
    BEGIN
        -- Attempt to insert multiple records
        INSERT INTO users VALUES (1, 'John');
        INSERT INTO users VALUES (1, 'Jane');  -- Duplicate key
        INSERT INTO users VALUES (2, 'Bob');
        
        -- Log the results
        INSERT INTO process_log VALUES ('Duplicates found: ' || duplicate_key_count);
        
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                CASE
                    WHEN (SQLSTATE = '23505') THEN
                        duplicate_key_count := duplicate_key_count + 1;
                END;
    END;
$$;
```

Copy

### DECLARE CONTINUE HANDLER FOR NOT FOUND[¶](#declare-continue-handler-for-not-found "Link to this heading")

The NOT FOUND condition is commonly used with cursors and SELECT INTO statements.

#### Input Code:[¶](#id5 "Link to this heading")

##### IBM DB2[¶](#id6 "Link to this heading")

```
CREATE PROCEDURE cursor_handler_example()
LANGUAGE SQL
BEGIN
    DECLARE v_id INT;
    DECLARE v_name VARCHAR(100);
    DECLARE v_done INT DEFAULT 0;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET v_done = 1;
    
    DECLARE cur1 CURSOR FOR
        SELECT id, name FROM employees WHERE department = 'Sales';
    
    OPEN cur1;
    
    fetch_loop:
    LOOP
        FETCH cur1 INTO v_id, v_name;
        
        IF v_done = 1 THEN
            LEAVE fetch_loop;
        END IF;
        
        INSERT INTO sales_employees VALUES (v_id, v_name);
    END LOOP fetch_loop;
    
    CLOSE cur1;
END;
```

Copy

#### Output Code:[¶](#id7 "Link to this heading")

##### Snowflake[¶](#id8 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE cursor_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        v_id INT;
        v_name VARCHAR(100);
        v_done INT := 0;
        cur1 CURSOR FOR
            SELECT id, name FROM employees WHERE department = 'Sales';
    BEGIN
        OPEN cur1;
        
        LOOP
            BEGIN
                FETCH cur1 INTO v_id, v_name;
            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    v_done := 1;
            END;
            
            IF (v_done = 1) THEN
                BREAK;
            END IF;
            
            INSERT INTO sales_employees VALUES (v_id, v_name);
        END LOOP;
        
        CLOSE cur1;
    END;
$$;
```

Copy

### DECLARE CONTINUE HANDLER FOR SQLWARNING[¶](#declare-continue-handler-for-sqlwarning "Link to this heading")

Handling warnings while allowing execution to continue.

#### Input Code:[¶](#id9 "Link to this heading")

##### IBM DB2[¶](#id10 "Link to this heading")

```
CREATE PROCEDURE warning_handler_example()
LANGUAGE SQL
BEGIN
    DECLARE warning_count INT DEFAULT 0;
    
    DECLARE CONTINUE HANDLER FOR SQLWARNING
    BEGIN
        SET warning_count = warning_count + 1;
        INSERT INTO warning_log VALUES (CURRENT_TIMESTAMP, SQLSTATE, SQLCODE);
    END;
    
    -- Operations that might generate warnings
    UPDATE products SET price = price * 1.1 WHERE category = 'Electronics';
    DELETE FROM old_records WHERE record_date < CURRENT_DATE - 365 DAYS;
    
    INSERT INTO process_summary VALUES (warning_count);
END;
```

Copy

#### Output Code:[¶](#id11 "Link to this heading")

##### Snowflake[¶](#id12 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE warning_handler_example()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        warning_count INT := 0;
    BEGIN
        -- Note: Snowflake doesn't distinguish warnings from errors in the same way
        -- Warning handling may need to be implemented through validation logic
        
        BEGIN
            UPDATE products SET price = price * 1.1 WHERE category = 'Electronics';
        EXCEPTION
            WHEN OTHER THEN
                warning_count := warning_count + 1;
                INSERT INTO warning_log 
                VALUES (CURRENT_TIMESTAMP(), :SQLSTATE, :SQLCODE);
        END;
        
        BEGIN
            DELETE FROM old_records WHERE record_date < CURRENT_DATE - 365;
        EXCEPTION
            WHEN OTHER THEN
                warning_count := warning_count + 1;
                INSERT INTO warning_log 
                VALUES (CURRENT_TIMESTAMP(), :SQLSTATE, :SQLCODE);
        END;
        
        INSERT INTO process_summary VALUES (warning_count);
    END;
$$;
```

Copy

## Known Issues[¶](#known-issues "Link to this heading")

### CONTINUE HANDLER Behavior Differences[¶](#continue-handler-behavior-differences "Link to this heading")

Applies to

* IBM DB2

#### Description[¶](#id13 "Link to this heading")

The exact behavior of DB2’s CONTINUE HANDLER cannot be fully replicated in Snowflake due to architectural differences:

1. **Execution Continuation**: In DB2, a CONTINUE HANDLER allows execution to continue from the statement immediately following the one that raised the condition. In Snowflake, each statement must be wrapped in its own exception block to achieve similar behavior.
2. **Performance Impact**: Wrapping multiple statements in individual exception blocks can impact performance compared to a single handler declaration.
3. **Scope**: DB2 CONTINUE HANDLERs apply to all statements in their scope. In Snowflake, exception handling must be more explicit.

#### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0114](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0114): MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING
2. [SSC-FDM-0027](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0027): REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE (applies to FROM clause RETURN DATA UNTIL statements)

### SQLSTATE Mapping[¶](#sqlstate-mapping "Link to this heading")

Not all DB2 SQLSTATE codes have direct equivalents in Snowflake. SnowConvert AI performs best-effort mapping:

| DB2 SQLSTATE | Condition | Snowflake Equivalent |
| --- | --- | --- |
| 02000 | NOT FOUND | NO\_DATA\_FOUND |
| 23xxx | Integrity Constraint Violation | STATEMENT\_ERROR |
| 42xxx | Syntax Error | STATEMENT\_ERROR |
| 01xxx | Warning | OTHER (requires validation) |

#### Input Code:[¶](#id14 "Link to this heading")

##### IBM DB2[¶](#id15 "Link to this heading")

```
DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02'
BEGIN
    -- Table doesn't exist
    CREATE TABLE missing_table (id INT, name VARCHAR(100));
END;
```

Copy

#### Output Code:[¶](#id16 "Link to this heading")

##### Snowflake[¶](#id17 "Link to this heading")

```
BEGIN
    -- Operation that might fail
    SELECT * FROM missing_table;
EXCEPTION
    WHEN STATEMENT_ERROR THEN
        LET errcode := :SQLCODE;
        LET sqlerrmsg := :SQLERRM;
        IF (CONTAINS(sqlerrmsg, 'does not exist') OR CONTAINS(sqlerrmsg, 'Table')) THEN
            -- Table doesn't exist
            CREATE TABLE missing_table (id INT, name VARCHAR(100));
        ELSE
            RAISE;
        END IF;
END;
```

Copy

### Multiple CONTINUE Handlers[¶](#multiple-continue-handlers "Link to this heading")

DB2 allows multiple CONTINUE HANDLERs with different priorities. In Snowflake, handler precedence must be managed through explicit conditional logic using CASE statements.

#### Input Code:[¶](#id18 "Link to this heading")

##### IBM DB2[¶](#id19 "Link to this heading")

```
CREATE PROCEDURE multiple_handlers()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLSTATE '23505'
        INSERT INTO log VALUES ('Duplicate key error');
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO log VALUES ('General SQL exception');
    
    INSERT INTO table1 VALUES (1, 'test');
END;
```

Copy

#### Output Code:[¶](#id20 "Link to this heading")

##### Snowflake[¶](#id21 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE multiple_handlers()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    BEGIN
        INSERT INTO table1 VALUES (1, 'test');
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                CASE
                    WHEN (SQLSTATE = '23505') THEN
                        INSERT INTO log VALUES ('Duplicate key error')
                    ELSE
                        INSERT INTO log VALUES ('General SQL exception')
                END;
    END;
$$;
```

Copy

### Mixed CONTINUE and EXIT Handlers[¶](#mixed-continue-and-exit-handlers "Link to this heading")

Applies to

* IBM DB2

#### Description[¶](#id22 "Link to this heading")

DB2 allows declaring both CONTINUE and EXIT handlers in the same procedure block. However, Snowflake Scripting does not support mixing CONTINUE and EXIT handlers in the same EXCEPTION block. When this pattern is encountered, SnowConvert AI generates separate EXCEPTION blocks with an EWI warning.

#### Input Code:[¶](#id23 "Link to this heading")

##### IBM DB2[¶](#id24 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE with_continueAndExit()
BEGIN
    DECLARE test_1 INTEGER DEFAULT 10;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION 
        INSERT INTO error_test VALUES ('EXCEPTION');
    DECLARE EXIT HANDLER FOR SQLSTATE '20000' 
        INSERT INTO error_test VALUES ('ERROR 2000');
    
    SET test_1 = 1 / 0;
    INSERT INTO error_test VALUES ('EXIT');
END;
```

Copy

#### Output Code:[¶](#id25 "Link to this heading")

##### Snowflake[¶](#id26 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE with_continueAndExit()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "01/15/2025" }}'
AS
$$
    DECLARE
        test_1 INTEGER DEFAULT 10;
    BEGIN
        test_1 := 1 / 0;
        INSERT INTO error_test VALUES ('EXIT');
        EXCEPTION
            WHEN OTHER CONTINUE THEN
                INSERT INTO error_test VALUES ('EXCEPTION')
        !!!RESOLVE EWI!!! /*** SSC-EWI-0114 - MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        EXCEPTION
            WHEN OTHER EXIT THEN
                CASE
                    WHEN (SQLSTATE = '20000') THEN
                        INSERT INTO error_test VALUES ('ERROR 2000')
                END
    END;
$$;
```

Copy

#### Related EWIs[¶](#id27 "Link to this heading")

1. [SSC-EWI-0114](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0114): MIXED CONTINUE AND EXIT EXCEPTION HANDLERS IN THE SAME BLOCK ARE NOT SUPPORTED BY SNOWFLAKE SCRIPTING

## Best Practices[¶](#best-practices "Link to this heading")

When working with converted CONTINUE HANDLER code:

1. **Validate Error Handling**: Thoroughly test all error scenarios to ensure the converted code behaves as expected.
2. **Review Performance**: Multiple exception blocks can impact performance. Consider refactoring when appropriate.
3. **Use Appropriate Exception Types**: Map DB2 conditions to the most specific Snowflake exception types available.
4. **Implement Logging**: Add comprehensive logging to track errors and ensure visibility into exception handling.
5. **Consider Transactions**: Use Snowflake’s transaction support to maintain data consistency when errors occur.
6. **Document Behavior Changes**: Document any differences in behavior between DB2 CONTINUE HANDLER and the Snowflake implementation.

## Related Documentation[¶](#related-documentation "Link to this heading")

* [IBM DB2 DECLARE HANDLER](https://www.ibm.com/docs/en/db2/11.5?topic=statements-declare-handler)
* [Snowflake Exception Handling](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions)
* [Snowflake Stored Procedures](https://docs.snowflake.com/en/sql-reference/stored-procedures-overview)

## See Also[¶](#see-also "Link to this heading")

* [DB2 CREATE PROCEDURE](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-procedure-sql)
* [DB2 FROM Clause](db2-from-clause)
* [DB2 SELECT Statement](db2-select-statement)
* [DB2 Data Types](db2-data-types)

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