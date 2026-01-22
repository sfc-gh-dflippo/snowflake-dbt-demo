---
auto_generated: true
description: This statement has usages of cursor fetch bulk operations
last_scraped: '2026-01-14T16:55:34.444304+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html
title: SnowConvert AI - General Performance Review Messages | Snowflake Documentation
---

1. [Overview](../../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../../guides/overview-db.md)
8. [Data types](../../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../overview.md)

        + General

          + [About](../../../about.md)
          + [Getting Started](../../../getting-started/README.md)
          + [Terms And Conditions](../../../terms-and-conditions/README.md)
          + [Release Notes](../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../user-guide/snowconvert/README.md)
            + [Project Creation](../../../user-guide/project-creation.md)
            + [Extraction](../../../user-guide/extraction.md)
            + [Deployment](../../../user-guide/deployment.md)
            + [Data Migration](../../../user-guide/data-migration.md)
            + [Data Validation](../../../user-guide/data-validation.md)
            + [Power BI Repointing](../../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../README.md)

            - [Considerations](../../considerations/README.md)
            - [Issues And Troubleshooting](../README.md)

              * [Conversion Issues](../conversion-issues/README.md)
              * [Functional Difference](../functional-difference/README.md)
              * [Out Of Scope](../out-of-scope/README.md)
              * [Performance Review](README.md)

                + [General](generalPRF.md)
                + [SQL Server-Azure Synapse](sqlServerPRF.md)
            - Function References

              - [SnowConvert AI Udfs](../../function-references/snowconvert-udfs.md)
              - [Teradata](../../function-references/teradata/README.md)
              - [Oracle](../../function-references/oracle/README.md)
              - [Shared](../../function-references/shared/README.md)
              - [SQL Server](../../function-references/sql-server/README.md)
          + [Contact Us](../../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../../translation-references/general/README.md)
          + [Teradata](../../../../translation-references/teradata/README.md)
          + [Oracle](../../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../../translation-references/hive/README.md)
          + [Redshift](../../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../../translation-references/postgres/README.md)
          + [BigQuery](../../../../translation-references/bigquery/README.md)
          + [Vertica](../../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../../translation-references/db2/README.md)
          + [SSIS](../../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../../data-validation-cli/index.md)
        + [AI Verification](../../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../../guides/teradata.md)
      * [Databricks](../../../../../guides/databricks.md)
      * [SQL Server](../../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../../guides/redshift.md)
      * [Oracle](../../../../../guides/oracle.md)
      * [Azure Synapse](../../../../../guides/azuresynapse.md)
15. [Queries](../../../../../../guides/overview-queries.md)
16. [Listings](../../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../../guides/overview-alerts.md)
25. [Security](../../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../../guides/overview-cost.md)

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Technical Documentation](../../README.md)[Issues And Troubleshooting](../README.md)[Performance Review](README.md)General

# SnowConvert AI - General Performance Review Messages[¶](#snowconvert-ai-general-performance-review-messages "Link to this heading")

## SSC-PRF-0001[¶](#ssc-prf-0001 "Link to this heading")

This statement has usages of cursor fetch bulk operations

### Description[¶](#description "Link to this heading")

This warning indicates that the statement uses cursor fetch bulk operations. These operations allow you to retrieve multiple rows of data from a cursor at once, instead of one row at a time. Using bulk operations improves performance by reducing the number of communications needed between the client and server.

This pattern can become complex if not implemented correctly. For example, retrieving too many rows in a single fetch operation can consume excessive memory. It’s crucial to maintain a balance between the number of rows fetched and the available memory resources.

### Code Example[¶](#code-example "Link to this heading")

#### Oracle[¶](#oracle "Link to this heading")

##### Input[¶](#input "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE oracle_cursor_fetch_bulk AS
--cursor and variable declarations
BEGIN
    OPEN c1;
    FETCH c1 BULK COLLECT INTO col1;
    CLOSE c1;
END;
```

Copy

##### Output[¶](#output "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE oracle_cursor_fetch_bulk ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
--cursor and variable declarations
$$
    BEGIN
        OPEN c1;
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        c1 := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:c1)
        );
        col1 := :c1:RESULT;
        CLOSE c1;
    END;
$$;
```

Copy

### Best Practices[¶](#best-practices "Link to this heading")

* For additional support, please contact us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

## SSC-PRF-0002[¶](#ssc-prf-0002 "Link to this heading")

Case insensitive columns can decrease performance of queries

### Description[¶](#id1 "Link to this heading")

Using collation in Snowflake can impact query performance, particularly in WHERE clauses. To learn more about how collation affects performance, please refer to the [Performance Implications of Using Collation](https://docs.snowflake.com/en/sql-reference/collation#performance-implications-of-using-collation).

A warning has been generated to indicate that a column was created with case-insensitive collation. Using this column in queries may cause slower performance.

### Code examples[¶](#code-examples "Link to this heading")

#### Output[¶](#id2 "Link to this heading")

```
 CREATE TABLE exampleTable
(
    col1 CHAR(10),
    col2 CHAR(20) COLLATE 'en-ci' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

Copy

#### Oracle[¶](#id3 "Link to this heading")

##### Input[¶](#id4 "Link to this heading")

```
 CREATE TABLE exampleTable (
    col1 VARCHAR(50) COLLATE BINARY_CI,
    col2 VARCHAR(50) COLLATE BINARY_CS
);
```

Copy

##### Output[¶](#id5 "Link to this heading")

```
 CREATE OR REPLACE TABLE exampleTable (
       col1 VARCHAR(50) COLLATE BINARY_CI /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/,
       col2 VARCHAR(50) COLLATE BINARY_CS
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
   ;
```

Copy

#### Microsoft SQL Server[¶](#microsoft-sql-server "Link to this heading")

##### Input[¶](#id6 "Link to this heading")

```
 CREATE TABLE exampleTable (
    col1 VARCHAR(50) COLLATE Latin1_General_CI_AS,
    col2 VARCHAR(50) COLLATE Latin1_General_CS_AS
);
```

Copy

##### Output[¶](#id7 "Link to this heading")

```
 CREATE OR REPLACE TABLE exampleTable (
    col1 VARCHAR(50) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/,
    col2 VARCHAR(50) COLLATE 'EN-CS-AS'
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

Copy

### Best Practices[¶](#id8 "Link to this heading")

* If your application’s performance is significantly affected by case-insensitive collation, consider rewriting your code to avoid using it. However, if the performance impact is acceptable, you can ignore this warning.
* For additional assistance, contact us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

## SSC-PRF-0003[¶](#ssc-prf-0003 "Link to this heading")

Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance

### Severity[¶](#severity "Link to this heading")

Low

### Description[¶](#id9 "Link to this heading")

This warning appears when a `FETCH` statement is detected within a loop. The `FETCH` statement retrieves and processes individual rows from a result set one at a time.

Processing large datasets using cursors within loops can become complex, especially when:

* Multiple table joins are involved
* Complex calculations are required
* Large numbers of rows need to be processed

This pattern may lead to performance issues and can be difficult to maintain as the data volume grows.

#### Code Example[¶](#id10 "Link to this heading")

#### Teradata[¶](#teradata "Link to this heading")

##### Input[¶](#id11 "Link to this heading")

```
 REPLACE PROCEDURE teradata_fetch_inside_loop()
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE col_name VARCHAR(200);
    DECLARE col_int INTEGER DEFAULT 0;
    DECLARE cursor_var CURSOR FOR SELECT some_column FROM tabla1;
    WHILE (col_int <> 0) DO		
        FETCH cursor_var INTO col_name;
        SET col_int = col_int + 1;
    END WHILE;
END;
```

Copy

##### Output[¶](#id12 "Link to this heading")

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "tabla1" **
CREATE OR REPLACE PROCEDURE teradata_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        col_name VARCHAR(200);
        col_int INTEGER DEFAULT 0;
    BEGIN
         
         
        LET cursor_var CURSOR
        FOR
            SELECT
                some_column FROM
                tabla1;
                WHILE (:col_int <> 0) LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
                    FETCH cursor_var INTO col_name;
            col_int := col_int + 1;
                END LOOP;
    END;
$$;
```

Copy

#### Oracle[¶](#id13 "Link to this heading")

##### Input[¶](#id14 "Link to this heading")

```
 CREATE PROCEDURE oracle_fetch_inside_loop
IS
  var1 table1.column1%TYPE;
  CURSOR cursor1 IS SELECT COLUMN_NAME FROM table1; 
BEGIN
  WHILE true LOOP
    FETCH cursor1 INTO var1;
    EXIT WHEN cursor1%NOTFOUND;
  END LOOP;  
END;
```

Copy

##### Output[¶](#id15 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE oracle_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    var1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'table1.column1%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
    --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
    cursor1 CURSOR
    FOR
      SELECT COLUMN_NAME FROM
        table1;
  BEGIN
    WHILE (true)
                 --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                 LOOP
      --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
         FETCH cursor1 INTO
        :var1;
         IF (var1 IS NULL) THEN
        EXIT;
         END IF;
       END LOOP;
  END;
$$;
```

Copy

#### SQL Server[¶](#sql-server "Link to this heading")

##### Input[¶](#id16 "Link to this heading")

```
 CREATE OR ALTER PROCEDURE transact_fetch_inside_loop
AS
BEGIN
    DECLARE cursor1 CURSOR
        FOR SELECT col1 FROM my_table;
    WHILE 1=0
    BEGIN
       FETCH NEXT FROM @cursor1 INTO @variable1;
    END
END;
```

Copy

##### Output[¶](#id17 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE transact_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
        cursor1 CURSOR
        FOR
            SELECT
                col1
            FROM
                my_table;
    BEGIN
         
        WHILE (1=0) LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
            FETCH
                CURSOR1
                INTO
                :VARIABLE1;
        END LOOP;
    END;
$$;
```

Copy

### Best Practices[¶](#id18 "Link to this heading")

* To improve performance and avoid complex patterns, use set-based operations instead of loops. Replace row-by-row processing with SQL statements (SELECT, UPDATE, DELETE) that operate on multiple rows simultaneously using WHERE clauses. This approach is more efficient and easier to maintain.

#### Oracle[¶](#id19 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_fetch_inside_loop 
AS
  record_employee employees%rowtype;
  CURSOR emp_cursor IS SELECT * FROM employees;
BEGIN
  OPEN emp_cursor;
  LOOP
    FETCH emp_cursor INTO record_employee;
    EXIT WHEN emp_cursor%notfound;
    INSERT INTO new_employees VALUES (record_employee.first_name, record_employee.last_name);
  END LOOP;
  CLOSE emp_cursor;
END;
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE cursor_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    record_employee OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWTYPE DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
    --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
    emp_cursor CURSOR
    FOR
      SELECT
        OBJECT_CONSTRUCT( *) sc_cursor_record FROM
        employees;
  BEGIN
    OPEN emp_cursor;
    --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
      --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
      FETCH emp_cursor INTO
        :record_employee;
      IF (record_employee IS NULL) THEN
        EXIT;
      END IF;
      INSERT INTO new_employees
      SELECT
        :record_employee:FIRST_NAME,
        :record_employee:LAST_NAME;
    END LOOP;
  CLOSE emp_cursor;
  END;
$$;
```

Copy

Set-based operations can be used to process data more efficiently.

```
 CREATE OR REPLACE PROCEDURE cursor_fetch_inside_loop AS
BEGIN
  INSERT INTO new_employees (first_name, last_name)
  SELECT first_name, last_name FROM employees;
END;
```

Copy

Set-based operations can be used to process data more efficiently.

```
 CREATE OR REPLACE PROCEDURE cursor_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    INSERT INTO new_employees(first_name, last_name)
    SELECT first_name, last_name FROM
      employees;
  END;
$$;
```

Copy

### Best Practices[¶](#id20 "Link to this heading")

* For additional support, please contact us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

## SSC-PRF-0004[¶](#ssc-prf-0004 "Link to this heading")

This statement has usages of cursor for loop

### Severity[¶](#id21 "Link to this heading")

None

### Description[¶](#id22 "Link to this heading")

This warning indicates that the statement contains cursor for loops. A cursor for loop is a programming structure that processes query results one row at a time, allowing you to work with individual records from a result set.

This warning helps identify potential performance issues in cursor FOR loops. Performance problems may arise when:

* The SELECT statement within the cursor returns a large dataset
* The loop contains complex operations
* The loop contains nested loops

While SnowConvert AI can detect these patterns, you should review and optimize the code to ensure efficient execution.

#### Code Example[¶](#id23 "Link to this heading")

#### Teradata[¶](#id24 "Link to this heading")

##### Input[¶](#id25 "Link to this heading")

```
 REPLACE PROCEDURE teradata_cursor_for_loop()    
BEGIN
    FOR fUsgClass AS cUsgClass CURSOR FOR
        (SELECT col1
        FROM sample_table)
    DO
        SET var1 = fUsgClass.col1;
    END FOR;
END;
```

Copy

##### Output[¶](#id26 "Link to this heading")

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "sample_table" **
CREATE OR REPLACE PROCEDURE teradata_cursor_for_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        !!!RESOLVE EWI!!! /*** SSC-EWI-0110 - TRANSFORMATION NOT PERFORMED DUE TO MISSING DEPENDENCIES ***/!!!
        temp_fUsgClass_col1;
    BEGIN
        LET cUsgClass CURSOR
        FOR
            SELECT
                col1
                   FROM
                sample_table;
        --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
        FOR fUsgClass IN cUsgClass DO
            temp_fUsgClass_col1 := fUsgClass.col1;
            var1 := :temp_fUsgClass_col1;
        END FOR;
    END;
$$;
```

Copy

#### Oracle[¶](#id27 "Link to this heading")

##### Input[¶](#id28 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE oracle_cursor_for_loop AS
BEGIN
    FOR r1 IN (SELECT col1 FROM sample_table) LOOP
        NULL;
    END LOOP;
END;
```

Copy

##### Output[¶](#id29 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE oracle_cursor_for_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        LET temporary_for_cursor_0 CURSOR
        FOR
            (SELECT col1 FROM
                    sample_table
            );
        --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
        FOR r1 IN temporary_for_cursor_0 DO
            NULL;
        END FOR;
    END;
$$;
```

Copy

### Best Practices[¶](#id30 "Link to this heading")

* For additional support, please contact us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

## SSC-PRF-0005[¶](#ssc-prf-0005 "Link to this heading")

The statement below has usages of nested cursors

Note

For better readability, we have simplified some sections of the code in this example.

### Severity[¶](#id31 "Link to this heading")

None

### Description[¶](#id32 "Link to this heading")

This warning indicates that the statement contains nested cursors. A cursor is a database feature that lets you process rows from a query result one at a time. Nested cursors occur when you use one cursor inside another cursor’s loop, which can impact performance and should be used with caution.

Nested cursors can significantly slow down your code’s performance, particularly when working with large amounts of data. This is because each time a cursor operates, it needs to communicate with the database server, creating additional processing overhead and delays.

### Code examples[¶](#id33 "Link to this heading")

#### SQL Server[¶](#id34 "Link to this heading")

##### Input[¶](#id35 "Link to this heading")

```
 CREATE OR ALTER PROCEDURE procedureSample
AS
BEGIN
  DECLARE
    @outer_category_id INT,
    @outer_category_name NVARCHAR(50),
    @inner_product_name NVARCHAR(50);

  -- Define the outer cursor
  DECLARE outer_cursor CURSOR FOR 
    SELECT category_id, category_name FROM categories;

  -- Open the outer cursor
  OPEN @outer_cursor;

  -- Fetch the first row from the outer cursor
  FETCH NEXT FROM outer_cursor INTO @outer_category_id, @outer_category_name;

  -- Start the outer loop
  WHILE @@FETCH_STATUS = 0
  BEGIN

    PRINT 'Category: ' + @outer_category_name;
	
    -- Define the inner cursor
    DECLARE inner_cursor CURSOR FOR
      SELECT product_name FROM products WHERE category_id = @outer_category_id;
    
    -- Open the inner cursor
    OPEN inner_cursor;
	FETCH NEXT FROM inner_cursor INTO @inner_product_name;

    WHILE @@FETCH_STATUS = 0
    BEGIN
      PRINT 'Product: ' + @inner_product_name + ' Category: ' + CAST(@outer_category_id AS NVARCHAR(10));

      -- Fetch the next row from the inner cursor
      FETCH NEXT FROM inner_cursor INTO @inner_product_name;
    END;

    -- Close the inner cursor
    CLOSE inner_cursor;
    DEALLOCATE inner_cursor;

    -- Fetch the next row from the outer cursor
    FETCH NEXT FROM outer_cursor INTO @outer_category_id, @outer_category_name;
  END;

  -- Close the outer cursor
  CLOSE outer_cursor;
  DEALLOCATE outer_cursor;
  
END;
```

Copy

##### Output[¶](#id36 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedureSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		OUTER_CATEGORY_ID INT;
		OUTER_CATEGORY_NAME VARCHAR(50);
		INNER_PRODUCT_NAME VARCHAR(50);

		-- Define the outer cursor
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		outer_cursor CURSOR
		FOR
			SELECT
				category_id,
				category_name
			FROM
				categories;

		-- Define the inner cursor
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		inner_cursor CURSOR
		FOR
			SELECT
				product_name
			FROM
				products
			WHERE
				category_id = :OUTER_CATEGORY_ID;
	BEGIN
		 
		 

		-- Open the outer cursor
		--** SSC-PRF-0005 - THE STATEMENT BELOW HAS USAGES OF NESTED CURSORS. **
		OPEN OUTER_CURSOR;
  -- Fetch the first row from the outer cursor
		FETCH
			outer_cursor
			INTO
			:OUTER_CATEGORY_ID,
			:OUTER_CATEGORY_NAME;

			-- Start the outer loop

			  -- Define the inner cursor
			WHILE (:FETCH_STATUS = 0) LOOP
			!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PRINT' NODE ***/!!!

			  PRINT 'Category: ' + @outer_category_name;
			 

			-- Open the inner cursor
			OPEN inner_cursor;
			--** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
			FETCH
				inner_cursor
			INTO
				:INNER_PRODUCT_NAME;
			WHILE (:FETCH_STATUS = 0) LOOP
				!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PRINT' NODE ***/!!!
				PRINT 'Product: ' + @inner_product_name + ' Category: ' + CAST(@outer_category_id AS NVARCHAR(10));
				-- Fetch the next row from the inner cursor
				--** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
				FETCH
					inner_cursor
				INTO
					:INNER_PRODUCT_NAME;
			END LOOP;
			-- Close the inner cursor
			CLOSE inner_cursor;
			!!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'DEALLOCATE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
			  DEALLOCATE inner_cursor;
			-- Fetch the next row from the outer cursor
			--** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
			FETCH
				outer_cursor
			INTO
				:OUTER_CATEGORY_ID,
				:OUTER_CATEGORY_NAME;
			END LOOP;
  -- Close the outer cursor
			CLOSE outer_cursor;
			!!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'DEALLOCATE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
			DEALLOCATE outer_cursor;
	END;
$$;
```

Copy

#### Oracle[¶](#id37 "Link to this heading")

#### Explicit cursor[¶](#explicit-cursor "Link to this heading")

##### Input[¶](#id38 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedureSample AS
BEGIN
DECLARE
  CURSOR outer_cursor IS
    SELECT category_id, category_name FROM categories;

  CURSOR inner_cursor (p_category_id NUMBER) IS
    SELECT product_name FROM products WHERE category_id = p_category_id;

  outer_category_id categories.category_id%TYPE;
  outer_category_name categories.category_name%TYPE;
  inner_product_name products.product_name%TYPE;
BEGIN

  OPEN outer_cursor;
  FETCH outer_cursor INTO outer_category_id, outer_category_name;

  LOOP
    EXIT WHEN outer_cursor%NOTFOUND;
    DBMS_OUTPUT.PUT_LINE('Category: ' || outer_category_name);

    OPEN inner_cursor(outer_category_id);
    LOOP
        FETCH inner_cursor INTO inner_product_name;
        EXIT WHEN inner_cursor%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE('Product: ' || inner_product_name || ' Category: ' || outer_category_id);
    END LOOP;
    CLOSE inner_cursor;

    FETCH outer_cursor INTO outer_category_id, outer_category_name;
  END LOOP;

  CLOSE outer_cursor;
END;
END;
```

Copy

##### Output[¶](#id39 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedureSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    DECLARE
      --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
      outer_cursor CURSOR
      FOR
        SELECT category_id, category_name FROM
          categories;
      --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
      inner_cursor CURSOR
      FOR
        SELECT product_name FROM
          products
        WHERE category_id = ?;
      outer_category_id VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'categories.category_id%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
      outer_category_name VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'categories.category_name%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
      inner_product_name VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'products.PRODUCT_NAME%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
      call_results VARIANT;
    BEGIN
      --** SSC-PRF-0005 - THE STATEMENT BELOW HAS USAGES OF NESTED CURSORS. **
      OPEN outer_cursor USING ('DEFAULT VALUE NOT FOUND');
      FETCH outer_cursor INTO
        :outer_category_id,
        :outer_category_name;
      --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
      LOOP
        IF (outer_category_id IS NULL) THEN
          EXIT;
        END IF;
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        call_results := (
          CALL DBMS_OUTPUT.PUT_LINE_UDF('Category: ' || NVL(:outer_category_name :: STRING, ''))
        );
        OPEN inner_cursor USING (:outer_category_id);
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        LOOP
          --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
            FETCH inner_cursor INTO
            :inner_product_name;
          IF (inner_product_name IS NULL) THEN
            EXIT;
          END IF;
          --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
          call_results := (
            CALL DBMS_OUTPUT.PUT_LINE_UDF('Product: ' || NVL(:inner_product_name :: STRING, '') || ' Category: ' || NVL(:outer_category_id :: STRING, ''))
          );
        END LOOP;
        CLOSE inner_cursor;
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        FETCH outer_cursor INTO
          :outer_category_id,
          :outer_category_name;
      END LOOP;
      CLOSE outer_cursor;
      RETURN call_results;
    END;
  END;
$$;
```

Copy

#### Implicit Cursor[¶](#implicit-cursor "Link to this heading")

##### Input[¶](#id40 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedureSample AS
BEGIN
DECLARE
   inner_category_id categories.category_name%TYPE;
   inner_product_name products.product_name%TYPE;
   inner_cursor SYS_REFCURSOR;
BEGIN
   FOR outer_cursor IN (SELECT category_id, category_name FROM categories)
   LOOP
      OPEN inner_cursor
       FOR SELECT product_name, category_id FROM products WHERE category_id = outer_cursor.category_id;
      LOOP
         FETCH inner_cursor INTO inner_product_name, inner_category_id;
         EXIT WHEN inner_cursor%NOTFOUND;
         dbms_output.put_line( 'Category id: '|| outer_cursor.category_id);
         dbms_output.put_line('Product name: ' || inner_product_name);
      END LOOP;
      CLOSE inner_cursor;
   END LOOP;
END;
END;
```

Copy

##### Output[¶](#id41 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedureSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      DECLARE
         inner_category_id VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'categories.category_name%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
         inner_product_name VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'products.product_name%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
         inner_cursor_res RESULTSET;
         call_results VARIANT;
      BEGIN
         LET temporary_for_cursor_0 CURSOR
         FOR
            (SELECT category_id, category_name FROM
                  categories
            );
         --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
         --** SSC-PRF-0005 - THE STATEMENT BELOW HAS USAGES OF NESTED CURSORS. **
         FOR outer_cursor IN temporary_for_cursor_0 DO
            LET inner_cursor CURSOR
            FOR
               SELECT product_name, category_id FROM
                  products
               WHERE category_id = outer_cursor.category_id;
            OPEN inner_cursor;
            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                 LOOP
               --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
                    FETCH inner_cursor INTO
                  :inner_product_name,
                  :inner_category_id;
               IF (inner_product_name IS NULL) THEN
                  EXIT;
               END IF;
               --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
               call_results := (
                  CALL dbms_output.put_line( 'Category id: ' || NVL(outer_cursor.category_id :: STRING, ''))
               );
               --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
               call_results := (
                  CALL dbms_output.put_line('Product name: ' || NVL(:inner_product_name :: STRING, ''))
               );
                 END LOOP;
                 CLOSE inner_cursor;
         END FOR;
         RETURN call_results;
      END;
   END;
$$;
```

Copy

### Best Practices[¶](#id42 "Link to this heading")

* Nested cursors should be avoided as they can negatively impact performance and make code more complex.
* Instead of nested cursors, use SQL features such as:

  + SQL functions
  + Joins
  + Subqueries
  + Window functions
  + Common Table Expressions (CTEs)
  + Recursive queries
    These alternatives process data in bulk and are more efficient.
* For additional assistance, contact us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

## SSC-PRF-0006[¶](#ssc-prf-0006 "Link to this heading")

Nested cursor inside query is not supported in Snowflake

### Severity[¶](#id43 "Link to this heading")

None

### Description[¶](#id44 "Link to this heading")

This message appears when a query contains a cursor definition. When a cursor expression is evaluated, it returns and automatically opens a nested cursor. For more details, see [Oracle Cursor Expression](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CURSOR-Expressions.html#GUID-B28362BE-8831-4687-89CF-9F77DB3698D2).

### Code examples[¶](#id45 "Link to this heading")

#### Input[¶](#id46 "Link to this heading")

```
 SELECT
  category_id,
  category_name,
  CURSOR (
    SELECT
      product_id,
      product_name || ', ' || category_id
    FROM
      products e
    WHERE
      e.category_id = d.category_id
  ) EMP_CUR
FROM
  categories d;
```

Copy

#### Output[¶](#id47 "Link to this heading")

```
 SELECT
  category_id,
  category_name,
  --** SSC-PRF-0006 - NESTED CURSOR INSIDE QUERY IS NOT SUPPORTED IN SNOWFLAKE. **
  CURSOR
    !!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!! (
    SELECT
      product_id,
      NVL(
      product_name :: STRING, '') || ', ' || NVL(category_id :: STRING, '')
    FROM
      products e
    WHERE
      e.category_id = d.category_id
  ) EMP_CUR
FROM
  categories d;
```

Copy

### Best Practices[¶](#id48 "Link to this heading")

* We recommend avoiding cursors as they can negatively affect performance and make code more complex.
* Instead of using nested cursors, consider these alternatives:

  + SQL functions
  + Joins
  + Subqueries
  + Window functions
  + Common Table Expressions (CTEs)
  + Recursive queries
    These options are better for processing large amounts of data efficiently.
* For additional assistance, contact us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

## SSC-PRF-0007[¶](#ssc-prf-0007 "Link to this heading")

PERFORMANCE REVIEW - CLUSTER BY

### Description[¶](#id49 "Link to this heading")

Marks where the usage of CLUSTER BY may cause performance issues.

#### Example Code[¶](#example-code "Link to this heading")

##### Teradata:[¶](#id50 "Link to this heading")

```
 CREATE MULTISET TABLE T_2008,
NO FALLBACK,
NO BEFORE JOURNAL,
NO AFTER JOURNAL,
CHECKSUM = DEFAULT,
DEFAULT MERGEBLOCKRATIO
(
      COL1 NUMBER(20,0) NOT NULL,
      COL2 INTEGER,
      COL3 VARCHAR(4) CHARACTER SET LATIN NOT CASESPECIFIC,
      COL4 DATE FORMAT 'YYYY-MM-DD'
)
PRIMARY INDEX 
( 
      COL1, COL2
)
PARTITION BY ( RANGE_N(COL4 BETWEEN DATE '2010-01-01' AND DATE '2025-12-31' EACH INTERVAL '1' YEAR ),
CASE_N(
COL3  = 'T',
COL3 = 'M',
COL3 = 'L') ); -- PARTITION BY transformed to CLUSTER BY
```

Copy

##### Snowflake:[¶](#id51 "Link to this heading")

```
CREATE OR REPLACE TABLE T_2008
(
      COL1 NUMBER(20,0) NOT NULL,
      COL2 INTEGER,
      COL3 VARCHAR(4),
      COL4 DATE
)
--** SSC-PRF-0007 - PERFORMANCE REVIEW - CLUSTER BY **
CLUSTER BY (
             !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - RANGE_N FUNCTION NOT SUPPORTED ***/!!!
             RANGE_N(COL4 BETWEEN DATE '2010-01-01' AND DATE '2025-12-31' EACH INTERVAL '1' YEAR ),
!!!RESOLVE EWI!!! /*** SSC-EWI-0031 - CASE_N FUNCTION NOT SUPPORTED ***/!!!
CASE_N(
COL3  = 'T',
COL3 = 'M',
COL3 = 'L'))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
; -- PARTITION BY transformed to CLUSTER BY
```

Copy

##### Transact:[¶](#transact "Link to this heading")

```
 CREATE TABLE my_table (
    enterprise_cif INT,
    name NVARCHAR(100),
    address NVARCHAR(255),
    created_at DATETIME
) 
WITH (
    DISTRIBUTION = HASH(enterprise_cif),
    CLUSTERED INDEX (enterprise_cif)
);
```

Copy

##### Snowflake:[¶](#id52 "Link to this heading")

```
 CREATE OR REPLACE TABLE my_table (
  enterprise_cif INT,
  name VARCHAR(100),
  address VARCHAR(255),
  created_at TIMESTAMP_NTZ(3)
)
--** SSC-PRF-0007 - PERFORMANCE REVIEW - CLUSTER BY **
CLUSTER BY (enterprise_cif)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/09/2024" }}'
;
```

Copy

#### Best Practices[¶](#id53 "Link to this heading")

* Review the code in order to identify possible performance issues. More information about this topic can be read [here](https://docs.snowflake.com/en/user-guide/tables-clustering-keys.html).
* If you need more support, you can email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

## SSC-PRF-0010[¶](#ssc-prf-0010 "Link to this heading")

Partition by removed, at least one of the specified expressions have no iceberg partition transform equivalent

### Severity[¶](#id54 "Link to this heading")

None

### Description[¶](#id55 "Link to this heading")

Snowflake supports the PARTITION BY clause in Iceberg tables, however, only [Iceberg partition transforms](https://iceberg.apache.org/spec/#partition-transforms) are supported. When transforming paritioning into Iceberg tables, SnowConvert AI will generate the equivalent partition transforms for supported cases. When no partition transform equivalent can be generated for the partition expressions, the PARTITION BY will be removed from the table by commenting it out with this PRF.

This PRF is only generated when SnowConvert AI migrates tables into Iceberg tables using the [Tables translation](../../../getting-started/running-snowconvert/conversion/teradata-conversion-settings.html#table-translation) conversion setting.

### Code examples[¶](#id56 "Link to this heading")

#### Input[¶](#id57 "Link to this heading")

```
 -- Additional Params: --TablesTransformationTarget SnowflakeIceberg
CREATE TABLE FINANCE.FINANCE_TABLE
(
  customerName VARCHAR(30),
  accountBalance VARCHAR(20)
)
PARTITION BY CASE_N(
accountBalance <  0 ,
accountBalance >=  0);
```

Copy

#### Output[¶](#id58 "Link to this heading")

```
 -- Additional Params: --TablesTransformationTarget SnowflakeIceberg
CREATE OR REPLACE ICEBERG TABLE FINANCE.FINANCE_TABLE
  (
 customerName VARCHAR,
 accountBalance VARCHAR
  )
  CATALOG = 'SNOWFLAKE'
--  --** SSC-PRF-0010 - PARTITION BY REMOVED, AT LEAST ONE OF THE SPECIFIED EXPRESSIONS HAVE NO ICEBERG PARTITION TRANSFORM EQUIVALENT **
--  PARTITION BY CASE_N(
--  accountBalance <  0 ,
--  accountBalance >=  0)
  COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 1,  "minor": 0,  "patch": "0.0" }, "attributes": {  "component": "teradata",  "convertedOn": "12/16/2025",  "domain": "no-domain-provided",  "migrationid": "9CebAVkM33qsfTnTrMh3Dw==" }}'
;
```

Copy

### Best Practices[¶](#id59 "Link to this heading")

* Analyze the impact of partitioning in the performance of queries over the generated Iceberg tables, if the difference is neglible then this PRF can be safely ignored.
* For additional assistance, contact us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

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

1. [SSC-PRF-0001](#ssc-prf-0001)
2. [SSC-PRF-0002](#ssc-prf-0002)
3. [SSC-PRF-0003](#ssc-prf-0003)
4. [SSC-PRF-0004](#ssc-prf-0004)
5. [SSC-PRF-0005](#ssc-prf-0005)
6. [SSC-PRF-0006](#ssc-prf-0006)
7. [SSC-PRF-0007](#ssc-prf-0007)
8. [SSC-PRF-0010](#ssc-prf-0010)