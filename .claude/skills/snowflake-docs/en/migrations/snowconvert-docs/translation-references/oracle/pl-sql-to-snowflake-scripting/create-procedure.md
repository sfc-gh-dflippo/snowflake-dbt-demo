---
auto_generated: true
description: Oracle Create Procedure to Snowflake Snow Scripting
last_scraped: '2026-01-14T16:53:24.538155+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/create-procedure
title: SnowConvert AI - Oracle - CREATE PROCEDURE | Snowflake Documentation
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../overview.md)

        + General

          + [About](../../../general/about.md)
          + [Getting Started](../../../general/getting-started/README.md)
          + [Terms And Conditions](../../../general/terms-and-conditions/README.md)
          + [Release Notes](../../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../../general/user-guide/project-creation.md)
            + [Extraction](../../../general/user-guide/extraction.md)
            + [Deployment](../../../general/user-guide/deployment.md)
            + [Data Migration](../../../general/user-guide/data-migration.md)
            + [Data Validation](../../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../general/technical-documentation/README.md)
          + [Contact Us](../../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../general/README.md)
          + [Teradata](../../teradata/README.md)
          + [Oracle](../README.md)

            - [Sample Data](../sample-data.md)
            - Basic Elements of Oracle SQL

              - [Literals](../basic-elements-of-oracle-sql/literals.md)
              - [Data Types](../basic-elements-of-oracle-sql/data-types/README.md)
            - [Pseudocolumns](../pseudocolumns.md)
            - [Built-in Functions](../functions/README.md)
            - [Built-in Packages](../built-in-packages.md)
            - [SQL Queries and Subqueries](../sql-queries-and-subqueries/selects.md)
            - [SQL Statements](../sql-translation-reference/README.md)
            - [PL/SQL to Snowflake Scripting](README.md)

              * [CREATE PROCEDURE](create-procedure.md)
              * [CREATE FUNCTION](create-function.md)
              * [COLLECTIONS AND RECORDS](collections-and-records.md)
              * [CURSOR](cursor.md)
              * [DML STATEMENTS](dml-statements.md)
              * [HELPERS](helpers.md)
              * [PACKAGES](packages.md)
            - [PL/SQL to Javascript](../pl-sql-to-javascript/README.md)
            - [SQL Plus](../sql-plus.md)
            - [Wrapped Objects](../wrapped-objects.md)
            - ETL And BI Repointing

              - [Power BI Oracle Repointing](../etl-bi-repointing/power-bi-oracle-repointing.md)
          + [SQL Server-Azure Synapse](../../transact/README.md)
          + [Sybase IQ](../../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../hive/README.md)
          + [Redshift](../../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../postgres/README.md)
          + [BigQuery](../../bigquery/README.md)
          + [Vertica](../../vertica/README.md)
          + [IBM DB2](../../db2/README.md)
          + [SSIS](../../ssis/README.md)
        + [Migration Assistant](../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../data-validation-cli/index.md)
        + [AI Verification](../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../guides/teradata.md)
      * [Databricks](../../../../guides/databricks.md)
      * [SQL Server](../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../guides/redshift.md)
      * [Oracle](../../../../guides/oracle.md)
      * [Azure Synapse](../../../../guides/azuresynapse.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Oracle](../README.md)[PL/SQL to Snowflake Scripting](README.md)CREATE PROCEDURE

# SnowConvert AI - Oracle - CREATE PROCEDURE[¶](#snowconvert-ai-oracle-create-procedure "Link to this heading")

Oracle Create Procedure to Snowflake Snow Scripting

## Description[¶](#description "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

> A procedure is a group of PL/SQL statements that you can call by name. A call specification (sometimes called call spec) declares a Java method or a third-generation language (3GL) routine so that it can be called from SQL and PL/SQL. The call spec tells Oracle Database which Java method to invoke when a call is made. It also tells the database what type conversions to make for the arguments and return value. [Oracle SQL Language Reference Create Procedure](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/CREATE-PROCEDURE.html#GUID-771879D8-BBFD-4D87-8A6C-290102142DA3).

For more information regarding Oracle Create Procedure, check [here](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/CREATE-PROCEDURE-statement.html#GUID-5F84DB47-B5BE-4292-848F-756BF365EC54).

### Oracle Create Procedure Syntax[¶](#oracle-create-procedure-syntax "Link to this heading")

```
CREATE [ OR REPLACE ] [ EDITIONABLE | NONEDITIONABLE ]
PROCEDURE
[ schema. ] procedure_name
[ ( parameter_declaration [, parameter_declaration ]... ) ] [ sharing_clause ]
[ ( default_collation_option | invoker_rights_clause | accessible_by_clause)... ] 
{ IS | AS } { [ declare_section ] 
    BEGIN statement ...
    [ EXCEPTION exception_handler [ exception_handler ]... ]
    END [ name ] ;
      |
    { java_declaration | c_declaration } } ;
```

Copy

For more information regarding Snowflake Create Procedure, check [here](https://docs.snowflake.com/en/sql-reference/sql/create-procedure.html#create-procedure).

#### Snowflake Create Procedure Syntax[¶](#snowflake-create-procedure-syntax "Link to this heading")

```
CREATE [ OR REPLACE ] PROCEDURE <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS <result_data_type> [ NOT NULL ]
  LANGUAGE SQL
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { CALLER | OWNER } ]
  AS '<procedure_definition>'
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### 1. Basic Procedure[¶](#basic-procedure "Link to this heading")

#### Oracle[¶](#oracle "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1
IS
BEGIN
null;
END;
```

Copy

##### Snow Scripting[¶](#snow-scripting "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
BEGIN
null;
END;
$$;
```

Copy

### 2. Procedure with Different Parameters[¶](#procedure-with-different-parameters "Link to this heading")

#### Oracle[¶](#id1 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE proc2
(
    p1 OUT INTEGER,
    p2 OUT INTEGER,
    p3 INTEGER := 1,
    p4 INTEGER DEFAULT 1
)
AS
BEGIN
	p1 := 17;
	p2 := 93;
END;
```

Copy

##### Snow Scripting[¶](#id2 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE proc2
(p1 OUT INTEGER, p2 OUT INTEGER,
    p3 INTEGER DEFAULT 1,
    p4 INTEGER DEFAULT 1
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	BEGIN
		p1 := 17;
		p2 := 93;
	END;
$$;
```

Copy

#### Output parameters[¶](#output-parameters "Link to this heading")

Snowflake does not allow output parameters in procedures, a way to simulate this behavior could be to declare a variable and return its value at the end of the procedure.

#### Parameters with default values[¶](#parameters-with-default-values "Link to this heading")

Snowflake does not allow setting default values for parameters in procedures, a way to simulate this behavior could be to declare a variable with the default value or overload the procedure.

### 3. Procedure with Additional Settings[¶](#procedure-with-additional-settings "Link to this heading")

#### Oracle[¶](#id3 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE proc3
DEFAULT COLLATION USING_NLS_COMP
AUTHID CURRENT_USER
AS
BEGIN
NULL;
END;
```

Copy

##### Snow Scripting[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE proc3 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/14/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
BEGIN
NULL;
END;
$$;
```

Copy

### 4. Procedure with Basic Statements[¶](#procedure-with-basic-statements "Link to this heading")

#### Oracle[¶](#id5 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE proc4
(
  param1 NUMBER
)
IS
  localVar1 NUMBER;
  countRows NUMBER;
  tempSql VARCHAR(100);
  tempResult NUMBER;
  CURSOR MyCursor IS SELECT COL1 FROM Table1;

BEGIN
    localVar1 := param1;
    countRows := 0;
    tempSql := 'SELECT COUNT(*) FROM Table1 WHERE COL1 =' || localVar1;

    FOR myCursorItem IN MyCursor
        LOOP
            localVar1 := myCursorItem.Col1;
            countRows := countRows + 1; 
        END LOOP;
    INSERT INTO Table2 VALUES(countRows, 'ForCursor: Total Row count is: ' || countRows);
    countRows := 0;

    OPEN MyCursor;
    LOOP
        FETCH MyCursor INTO tempResult;
        EXIT WHEN MyCursor%NOTFOUND;
        countRows := countRows + 1;
    END LOOP;
    CLOSE MyCursor;
    INSERT INTO Table2 VALUES(countRows, 'LOOP: Total Row count is: ' || countRows);

    EXECUTE IMMEDIATE tempSql INTO tempResult;
    IF tempResult > 0 THEN 
        INSERT INTO Table2 (COL1, COL2) VALUES(tempResult, 'Hi, found value:' || localVar1 || ' in Table1 -- There are ' || tempResult || ' rows');
        COMMIT;
    END IF;
END proc3;
```

Copy

##### Snow Scripting[¶](#id6 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE proc4
(param1 NUMBER(38, 18)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    localVar1 NUMBER(38, 18);
    countRows NUMBER(38, 18);
    tempSql VARCHAR(100);
    tempResult NUMBER(38, 18);
    --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
    MyCursor CURSOR
    FOR
      SELECT COL1 FROM
        Table1;
  BEGIN
    localVar1 := :param1;
    countRows := 0;
    tempSql := 'SELECT COUNT(*) FROM
   Table1
WHERE COL1 =' || NVL(:localVar1 :: STRING, '');
    OPEN MyCursor;
    --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
    FOR myCursorItem IN MyCursor DO
      localVar1 := myCursorItem.Col1;
      countRows := :countRows + 1;
    END FOR;
    CLOSE MyCursor;
    INSERT INTO Table2
    VALUES(:countRows, 'ForCursor: Total Row count is: ' || NVL(:countRows :: STRING, ''));
    countRows := 0;
    OPEN MyCursor;
    --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
      --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        FETCH MyCursor INTO
        :tempResult;
      IF (tempResult IS NULL) THEN
        EXIT;
      END IF;
      countRows := :countRows + 1;
    END LOOP;
    CLOSE MyCursor;
    INSERT INTO Table2
    SELECT
      :countRows,
      'LOOP: Total Row count is: ' || NVL(:countRows :: STRING, '');
    !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!

    EXECUTE IMMEDIATE :tempSql
                               !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'EXECUTE IMMEDIATE RETURNING CLAUSE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
                               INTO tempResult;
    IF (:tempResult > 0) THEN
      INSERT INTO Table2(COL1, COL2)
      SELECT
        :tempResult,
        'Hi, found value:' || NVL(:localVar1 :: STRING, '') || ' in Table1 -- There are ' || NVL(:tempResult :: STRING, '') || ' rows';
      --** SSC-FDM-OR0012 - COMMIT REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
      COMMIT;
    END IF;
  END;
$$;
```

Copy

### 5. Procedure with empty `RETURN` statements[¶](#procedure-with-empty-return-statements "Link to this heading")

In Oracle procedures you can have empty `RETURN` statements to finish the execution of a procedure. In Snowflake Scripting procedures can have `RETURN` statements but they must have a value. By default all empty `RETURN` statements are converted with a `NULL` value.

#### Oracle[¶](#id7 "Link to this heading")

```
-- Procedure with empty return
CREATE OR REPLACE PROCEDURE MY_PROC
IS
BEGIN
   NULL;
   RETURN;
END;
```

Copy

##### Snowflake Scripting[¶](#snowflake-scripting "Link to this heading")

```
-- Procedure with empty return
CREATE OR REPLACE PROCEDURE MY_PROC ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      NULL;
      RETURN NULL;
   END;
$$;
```

Copy

#### `RETURN` statements in procedures with output parameters[¶](#return-statements-in-procedures-with-output-parameters "Link to this heading")

In procedures with output parameters, instead of a `NULL` value an `OBJECT_CONSTRUCT` will be used in the empty `RETURN` statements to simulate the output parameters in Snowflake Scripting.

##### Oracle[¶](#id8 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_WITH_OUTPUT_PARAMETERS (
    param1 OUT NUMBER,
    param2 OUT NUMBER,
    param3 NUMBER
)
IS
BEGIN 
    IF param3 > 0 THEN
        param1 := 2;
        param2 := 1000;
        RETURN;
    END IF;
    param1 := 5;
    param2 := 3000;
END;
```

Copy

##### Snowflake Scripting[¶](#id9 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_WITH_OUTPUT_PARAMETERS (param1 OUT NUMBER(38, 18), param2 OUT NUMBER(38, 18), param3 NUMBER(38, 18)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        IF (:param3 > 0) THEN
            param1 := 2;
            param2 := 1000;
            RETURN NULL;
        END IF;
        param1 := 5;
        param2 := 3000;
    END;
$$;
```

Copy

### 6. Procedure with DEFAULT parameters[¶](#procedure-with-default-parameters "Link to this heading")

DEFAULT parameters allow named parameters to be initialized with default values if no value is passed.

#### Oracle[¶](#id10 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE TEST(
    X IN VARCHAR DEFAULT 'P',
    Y IN VARCHAR DEFAULT 'Q'
)
AS 
    varX VARCHAR(32767) := NVL(X, 'P');
    varY NUMBER := NVL(Y, 1);
BEGIN
    NULL;
END TEST;

BEGIN
    TEST(Y => 'Y');
END;
```

Copy

##### Snowflake Scripting[¶](#id11 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE TEST (
    X VARCHAR DEFAULT 'P',
    Y VARCHAR DEFAULT 'Q'
)
    RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
    EXECUTE AS CALLER
    AS
    $$
        DECLARE
            varX VARCHAR(32767) := NVL(:X, 'P');
            varY NUMBER(38, 18) := NVL(:Y, 1);
        BEGIN
            NULL;
        END;
    $$;

    DECLARE
        call_results VARIANT;

        BEGIN
        CALL
        TEST(Y => 'Y');
        RETURN call_results;
        END;
```

Copy

## Known Issues[¶](#known-issues "Link to this heading")

### 1. Unsupported OUT parameters[¶](#unsupported-out-parameters "Link to this heading")

Snowflake procedures do not have a native option for output parameters.

#### 2. Unsupported Oracle additional settings[¶](#unsupported-oracle-additional-settings "Link to this heading")

The following Oracle settings and clauses are not supported by Snowflake procedures:

* `sharing_clause`
* `default_collation_option`
* `invoker_rights_clause`
* `accessible_by_clause`
* `java_declaration`
* `c_declaration`

## Related EWIS[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0058](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting
2. [SSC-EWI-OR0097](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0097): Procedures properties are not supported in Snowflake procedures.
3. [SSC-FDM-OR0012:](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0012) COMMIT and ROLLBACK statements require adequate setup to perform as intended.
4. [SSC-PRF-0003](../../../general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html#ssc-prf-0003): Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance.
5. [SSC-PRF-0004](../../../general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html#ssc-prf-0004): This statement has usages of cursor for loop.
6. [SSC-EWI-0030](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0030): The statement below has usages of dynamic SQL

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
2. [Sample Source Patterns](#sample-source-patterns)
3. [Known Issues](#known-issues)
4. [Related EWIS](#related-ewis)