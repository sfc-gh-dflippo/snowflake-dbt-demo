---
auto_generated: true
description: Translation reference to convert Teradata ABORT and ROLLBACK statements
  to Snowflake Scripting
last_scraped: '2026-01-14T16:53:54.656065+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/teradata-to-snowflake-scripting-translation-reference
title: SnowConvert AI - Teradata - SQL to Snowflake Scripting (Procedures) | Snowflake
  Documentation
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
          + [Teradata](README.md)

            - [Data Migration Considerations](data-migration-considerations.md)
            - [Session Modes in Teradata](session-modes.md)
            - [Sql Translation Reference](sql-translation-reference/README.md)
            - [SQL to JavaScript (Procedures)](teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](scripts-to-python/README.md)
            - [Scripts to Snowflake SQL](scripts-to-snowflake-sql-translation-reference/README.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](etl-bi-repointing/power-bi-teradata-repointing.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](../transact/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Teradata](README.md)SQL to Snowflake Scripting (Procedures)

# SnowConvert AI - Teradata - SQL to Snowflake Scripting (Procedures)[¶](#snowconvert-ai-teradata-sql-to-snowflake-scripting-procedures "Link to this heading")

## ABORT and ROLLBACK[¶](#abort-and-rollback "Link to this heading")

Translation reference to convert Teradata ABORT and ROLLBACK statements to Snowflake Scripting

### Description [¶](#description "Link to this heading")

Teradata’s `ABORT` and `ROLLBACK` statements are replaced by a `ROLLBACK` statement in Snowflake Scripting.

For more information on Teradata [ABORT](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/c6KYQ4ySu4QTCkKS4f5A2w) and for [ROLLBACK](https://docs.teradata.com/r/huc7AEHyHSROUkrYABqNIg/ZddbA8dTQ1LNcHwmCn8BVg).

```
 ABORT [abort_message] [FROM option] [WHERE abort_condition];

ROLLBACK [WORK] [abort_message] [FROM clause] [WHERE clause];
```

Copy

### Sample Source Patterns [¶](#sample-source-patterns "Link to this heading")

#### Basic ABORT and ROLLBACK[¶](#basic-abort-and-rollback "Link to this heading")

##### Teradata [¶](#teradata "Link to this heading")

##### Query[¶](#query "Link to this heading")

```
 REPLACE PROCEDURE procedureBasicAbort() 
BEGIN
    ABORT;	
    ROLLBACK;
END;
```

Copy

##### Snowflake Scripting [¶](#snowflake-scripting "Link to this heading")

##### Query[¶](#id1 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedureBasicAbort ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        ROLLBACK;
        ROLLBACK;
    END;
$$;
```

Copy

#### Conditional ABORT and ROLLBACK[¶](#conditional-abort-and-rollback "Link to this heading")

##### Teradata [¶](#id2 "Link to this heading")

##### Query[¶](#id3 "Link to this heading")

```
 REPLACE PROCEDURE procedureWhereAbort(AnotherValueProc INTEGER) 
BEGIN
    ABORT WHERE AValueProc > 2;
	
    ROLLBACK WHERE (AnotherValueProc > 2);
END;
```

Copy

##### Snowflake Scripting [¶](#id4 "Link to this heading")

##### Query[¶](#id5 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedureWhereAbort (ANOTHERVALUEPROC INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/23/2024" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        IF (AValueProc > 2) THEN
            ROLLBACK;
        END IF;
        IF (:AnotherValueProc > 2) THEN
            ROLLBACK;
        END IF;
    END;
$$;
```

Copy

#### ABORT and ROLLBACK with table references and FROM clause[¶](#abort-and-rollback-with-table-references-and-from-clause "Link to this heading")

##### Teradata [¶](#id6 "Link to this heading")

##### Query[¶](#id7 "Link to this heading")

```
 CREATE TABLE  ReferenceTable
    (ColumnValue INTEGER);
  
CREATE TABLE  ReferenceTable2
    (ColumnValue INTEGER);

REPLACE PROCEDURE procedureFromAbort() 
BEGIN
    ROLLBACK FROM ReferenceTable, ReferenceTable2
	WHERE ReferenceTable.ColumnValue = ReferenceTable2.ColumnValue;
    ABORT FROM ReferenceTable, ReferenceTable2
        WHERE ReferenceTable.ColumnValue = ReferenceTable2.ColumnValue;
END;
```

Copy

##### Snowflake Scripting [¶](#id8 "Link to this heading")

##### Query[¶](#id9 "Link to this heading")

```
 CREATE OR REPLACE TABLE ReferenceTable
(
	ColumnValue INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

CREATE TABLE ReferenceTable2
(
	ColumnValue INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

CREATE OR REPLACE PROCEDURE procedureFromAbort ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
	BEGIN
		LET _ROW_COUNT FLOAT;
		SELECT
			COUNT(*)
		INTO
			_ROW_COUNT
			FROM
			ReferenceTable,
			ReferenceTable2
				WHERE
			ReferenceTable.ColumnValue = ReferenceTable2.ColumnValue;
			IF (_ROW_COUNT > 0) THEN
			ROLLBACK;
			END IF;
			SELECT
			COUNT(*)
			INTO
			_ROW_COUNT
			FROM
			ReferenceTable,
			ReferenceTable2
			        WHERE
			ReferenceTable.ColumnValue = ReferenceTable2.ColumnValue;
			IF (_ROW_COUNT > 0) THEN
			ROLLBACK;
			END IF;
	END;
$$;
```

Copy

#### ABORT and ROLLBACK with table references without FROM clause[¶](#abort-and-rollback-with-table-references-without-from-clause "Link to this heading")

##### Teradata [¶](#id10 "Link to this heading")

##### Query[¶](#id11 "Link to this heading")

```
 CREATE TABLE  ReferenceTable
    (ColumnValue INTEGER);
    
REPLACE PROCEDURE procedureFromTableAbort() 
BEGIN
    ROLLBACK WHERE ReferenceTable.ColumnValue > 2;
    ABORT WHERE ReferenceTable.ColumnValue > 4;
END;
```

Copy

##### Snowflake Scripting [¶](#id12 "Link to this heading")

##### Abort and rollback[¶](#id13 "Link to this heading")

```
 CREATE OR REPLACE TABLE ReferenceTable
(
    ColumnValue INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

CREATE OR REPLACE PROCEDURE procedureFromTableAbort ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        LET _ROW_COUNT FLOAT;
        SELECT
            COUNT(*)
        INTO
            _ROW_COUNT
        FROM
            ReferenceTable
            WHERE
            ReferenceTable.ColumnValue > 2;
            IF (_ROW_COUNT > 0) THEN
            ROLLBACK;
            END IF;
            SELECT
            COUNT(*)
            INTO
            _ROW_COUNT
            FROM
            ReferenceTable
            WHERE
            ReferenceTable.ColumnValue > 4;
            IF (_ROW_COUNT > 0) THEN
            ROLLBACK;
            END IF;
    END;
$$;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

#### 1. Custom Error Message[¶](#custom-error-message "Link to this heading")

Even though the ROLLBACK AND ABORT are supported, using them with a custom error message is not supported.

##### Teradata [¶](#id14 "Link to this heading")

##### Error message[¶](#error-message "Link to this heading")

```
 ABORT 'Error message for abort';
ROLLBACK  'Error message for rollback';
```

Copy

##### Snowflake Scripting [¶](#id15 "Link to this heading")

##### Error message[¶](#id16 "Link to this heading")

```
 ABORT 'Error message for abort';
ROLLBACK  'Error message for rollback';
```

Copy

##### 2. Aggregate function[¶](#aggregate-function "Link to this heading")

The use of the aggregate function combined with ABORT/ROLLBACK is not supported

##### Teradata [¶](#id17 "Link to this heading")

##### Aggregate function[¶](#id18 "Link to this heading")

```
 ROLLBACK WHERE SUM(ATable.AValue) < 2;
ABORT WHERE SUM(ATable.AValue) < 2;
```

Copy

##### Snowflake Scripting [¶](#id19 "Link to this heading")

##### Aggregate function[¶](#id20 "Link to this heading")

```
 ROLLBACK WHERE SUM(ATable.AValue) < 2;
ABORT WHERE SUM(ATable.AValue) < 2;
```

Copy

### Related EWIS[¶](#related-ewis "Link to this heading")

No related EWIs.

## ACTIVITY\_COUNT[¶](#activity-count "Link to this heading")

Translation specification for the ACTIVITY\_COUNT status variable.

### Description[¶](#id21 "Link to this heading")

The `ACTIVITY_COUNT` status variable returns the number of rows affected by an SQL DML statement in an embedded SQL or stored procedure application. For more information check [here](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Stored-Procedures-and-Embedded-SQL/Result-Code-Variables/ACTIVITY_COUNT).

There is no direct equivalent in Snowflake. However, there is a workaround to emulate the `ACTIVITY_COUNT`’s behavior. One must simply use the following query:

```
 SELECT $1 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

Copy

This query retrieves and returns the first column of the result set from the last executed query in the current session. Furthermore, `$1` can be replaced by `"number of rows inserted"`, `"number of rows updated"` or `"number of rows deleted"` based on the query type.

As expected, this translation behaves like its Teradata counterpart only when no other queries besides the SQL DML statement are executed before calling `LAST_QUERY_ID`.

### Sample Source Patterns[¶](#id22 "Link to this heading")

#### Setup data[¶](#setup-data "Link to this heading")

##### Teradata[¶](#id23 "Link to this heading")

##### Query[¶](#id24 "Link to this heading")

```
 CREATE TABLE employees (
    employee_id INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department_id INT,
    salary DECIMAL(10,2),
    PRIMARY KEY (employee_id)
);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (1, 'John', 'Doe', 10, 60000.00);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (2, 'Johny', 'Doey', 10, 65000.00);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (3, 'Max', 'Smith', 10, 70000.00);

DROP TABLE activity_log;
CREATE TABLE activity_log (
    log_id INT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    operation VARCHAR(200),
    row_count INT,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id)
);
```

Copy

##### *Snowflake*[¶](#snowflake "Link to this heading")

##### Query[¶](#id25 "Link to this heading")

```
 CREATE OR REPLACE TABLE employees (
    employee_id INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department_id INT,
    salary DECIMAL(10,2),
    PRIMARY KEY (employee_id)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/11/2024" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (1, 'John', 'Doe', 10, 60000.00);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (2, 'Johny', 'Doey', 10, 65000.00);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary)
VALUES (3, 'Max', 'Smith', 10, 70000.00);

CREATE OR REPLACE TABLE activity_log (
    log_id INT DEFAULT activity_log_log_id.NEXTVAL NOT NULL,
    operation VARCHAR(200),
    row_count INT,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (log_id)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/11/2024" }}'
;
```

Copy

#### Supported usage[¶](#supported-usage "Link to this heading")

##### *Teradata*[¶](#id26 "Link to this heading")

##### Query[¶](#id27 "Link to this heading")

```
 REPLACE PROCEDURE UpdateEmployeeSalaryAndLog ()
BEGIN
    DECLARE row_count1 INT;

    UPDATE employees
    SET salary = 80000
    WHERE department_id = 10;

    -- Get the ACTIVITY_COUNT
    SET row_count1 = ACTIVITY_COUNT;

    -- Insert the ACTIVITY_COUNT into the activity_log table
    INSERT INTO activity_log (operation, row_count)
    VALUES ('UPDATE WHERE dept=10', row_count1);
END;

CALL UpdateEmployeeSalaryAndLog();

SELECT * FROM ACTIVITY_LOG;
```

Copy

##### Result[¶](#result "Link to this heading")

```
LOG_ID | OPERATION    	      | ROW_COUNT | LOG_TIMESTAMP              |
-------+----------------------+-----------+----------------------------+
1      | UPDATE WHERE dept=10 |	3         | 2024-07-10 15:58:46.490000 |
```

Copy

##### *Snowflake*[¶](#id28 "Link to this heading")

##### Query[¶](#id29 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE UpdateEmployeeSalaryAndLog ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/11/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        row_count1 INT;
    BEGIN
         
        UPDATE employees
    SET salary = 80000
    WHERE department_id = 10;

    -- Get the ACTIVITY_COUNT
        row_count1 := (
    SELECT
        $1
    FROM
        TABLE(RESULT_SCAN(LAST_QUERY_ID()))
        ) /*** SSC-FDM-TD0033 - 'ACTIVITY_COUNT' TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS ***/;

        -- Insert the ACTIVITY_COUNT into the activity_log table
        INSERT INTO activity_log (operation, row_count)
        VALUES ('UPDATE WHERE dept=10', :row_count1);
    END;
$$;

CALL UpdateEmployeeSalaryAndLog();

SELECT
    * FROM
    ACTIVITY_LOG;
```

Copy

##### Result[¶](#id30 "Link to this heading")

```
LOG_ID | OPERATION    	      | ROW_COUNT | LOG_TIMESTAMP            |
-------+----------------------+-----------+--------------------------+
102    | UPDATE WHERE dept=10 |	3         | 2024-07-11T12:42:35.280Z |
```

Copy

### Known Issues[¶](#id31 "Link to this heading")

1. If `ACTIVITY_COUNT` is called twice or more times before executing a DML statement, the transformation might not return the expected values. Check [here](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0033).
2. If `ACTIVITY_COUNT` is called after a non DML statement was executed, the transformation will not return the expected values. Check [here](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0033).
3. `ACTIVITY_COUNT` requires manual fixing when inside a `SELECT/SET INTO VARIABLE` statement and was not able to be identified as a column name. Check [here](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0003).

### Related EWIs[¶](#id32 "Link to this heading")

1. [SSC-FDM-TD0033](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0033): ‘ACTIVITY\_COUNT’ TRANSFORMATION MIGHT REQUIRE MANUAL ADJUSTMENTS.

## BEGIN END[¶](#begin-end "Link to this heading")

Translation reference to convert Teradata BEGIN END clause to Snowflake Scripting

### BEGIN END TRANSACTION[¶](#begin-end-transaction "Link to this heading")

#### Description[¶](#id33 "Link to this heading")

> Defines the beginning of an explicit logical transaction in Teradata session mode.

For more information regarding Teradata BEGIN END Transaction, check [here](https://docs.teradata.com/r/2_MC9vCtAJRlKle2Rpb0mA/EhQtM73NDooSYqTcaZEHzQ).

```
 [ BEGIN TRANSACTION | BT ]
     statement
     [ statement ]... ]
[ END TRANSACTION | ET ];
```

Copy

#### Sample Source Pattern [¶](#sample-source-pattern "Link to this heading")

##### Teradata [¶](#id34 "Link to this heading")

##### Query[¶](#id35 "Link to this heading")

```
 REPLACE PROCEDURE BeginEndProcedure()
BEGIN
    DECLARE HELLOSTRING VARCHAR(60);
    BEGIN TRANSACTION
        SET HELLOSTRING = 'HELLO WORLD';
    END TRANSACTION;
END;
```

Copy

##### Snowflake Scripting [¶](#id36 "Link to this heading")

##### Query[¶](#id37 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE BeginEndProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        HELLOSTRING VARCHAR(60);
    BEGIN
         
        BEGIN TRANSACTION;
        HELLOSTRING := 'HELLO WORLD';
        COMMIT;
    END;
$$;
```

Copy

### BEGIN END REQUEST[¶](#begin-end-request "Link to this heading")

#### Description[¶](#id38 "Link to this heading")

> Delimits a SQL multistatement request

For more information regarding Teradata BEGIN END Request, check [here](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Data-Definition-Language-Syntax-and-Examples/March-2019/Procedure-Statements/CREATE-PROCEDURE-and-REPLACE-PROCEDURE-SQL-Form/Syntax-Elements/Statement-Options/BEGIN-REQUEST).

```
 BEGIN REQUEST
     statement
     [ statement ]... ]
END REQUEST;
```

Copy

#### Sample Source Pattern [¶](#id39 "Link to this heading")

##### Teradata [¶](#id40 "Link to this heading")

##### Query[¶](#id41 "Link to this heading")

```
 REPLACE PROCEDURE BeginEndProcedure()
BEGIN
    DECLARE HELLOSTRING VARCHAR(60);
    BEGIN REQUEST
        SET HELLOSTRING = 'HELLO WORLD';
    END REQUEST;
END;
```

Copy

##### Snowflake Scripting [¶](#id42 "Link to this heading")

##### Query[¶](#id43 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE BeginEndProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        HELLOSTRING VARCHAR(60);
    BEGIN
         
        BEGIN
            HELLOSTRING := 'HELLO WORLD';
            COMMIT;
        EXCEPTION
            WHEN OTHER THEN
                ROLLBACK;
        END;
    END;
$$;
```

Copy

### BEGIN END COMPOUND[¶](#begin-end-compound "Link to this heading")

#### Description[¶](#id44 "Link to this heading")

> Delimits a compound statement in a stored procedure.

For more information regarding Teradata BEGIN END Compound, check [here](https://docs.teradata.com/r/Teradata-Database-SQL-Stored-Procedures-and-Embedded-SQL/June-2017/SQL-Control-Statements/BEGIN-...-END).

```
 label_name: BEGIN
     statement
     [ statement ]... ]
END label_name;
```

Copy

#### Sample Source Pattern [¶](#id45 "Link to this heading")

##### Teradata [¶](#id46 "Link to this heading")

##### Query[¶](#id47 "Link to this heading")

```
 REPLACE PROCEDURE BeginEndProcedure()
BEGIN
    DECLARE HELLOSTRING VARCHAR(60);
    label_name: BEGIN
        SET HELLOSTRING = 'HELLO WORLD';
    END label_name;
END;
```

Copy

##### Snowflake Scripting [¶](#id48 "Link to this heading")

##### Query[¶](#id49 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE BeginEndProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        HELLOSTRING VARCHAR(60);
    BEGIN
         
        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'label_name LABEL' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
        label_name:
        BEGIN
            HELLOSTRING := 'HELLO WORLD';
        END;
    END;
$$;
```

Copy

### Known Issues[¶](#id50 "Link to this heading")

#### 1. Labels not supported in outer BEGIN END blocks[¶](#labels-not-supported-in-outer-begin-end-blocks "Link to this heading")

##### Teradata [¶](#id51 "Link to this heading")

##### Query[¶](#id52 "Link to this heading")

```
 REPLACE PROCEDURE procedureLabelSingle()
label_name: BEGIN
    DECLARE HELLOSTRING VARCHAR(60);
    SET HELLOSTRING = 'HELLO WORLD';
END label_name;
```

Copy

##### Snowflake Scripting [¶](#id53 "Link to this heading")

##### Query[¶](#id54 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE procedureLabelSingle ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'label_name LABEL' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
    label_name:
    DECLARE
        HELLOSTRING VARCHAR(60);
    BEGIN
         
        HELLOSTRING := 'HELLO WORLD';
    END;
$$;
```

Copy

### Related EWIs[¶](#id55 "Link to this heading")

1. [SSC-EWI-0058](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting.

## CASE[¶](#case "Link to this heading")

Translation reference to convert Teradata CASE statement to Snowflake Scripting

### Description [¶](#id56 "Link to this heading")

> Provides conditional execution of statements based on the evaluation of the specified conditional expression or equality of two operands.
>
> The CASE statement is different from the SQL CASE expression\_,\_ which returns the result of an expression.

For more information regarding Teradata CASE, check [here](https://docs.teradata.com/r/zzfV8dn~lAaKSORpulwFMg/3nWOY~VPjk9_5FJXaKQNFg).

```
 -- Simple CASE
CASE operant_1
[ WHEN operant_2 THEN
     statement
     [ statement ]... ]...
[ ELSE   
     statement
     [ statement ]... ]
END CASE;

-- Searched CASE
CASE
[ WHEN conditional_expression THEN
     statement
     [ statement ]... ]...
[ ELSE   
     statement
     [ statement ]... ]
END CASE;
```

Copy

### Sample Source Patterns [¶](#id57 "Link to this heading")

#### Sample auxiliar table[¶](#sample-auxiliar-table "Link to this heading")

##### Teradata[¶](#id58 "Link to this heading")

```
 CREATE TABLE case_table(col varchar(30));
```

Copy

##### Snowflake[¶](#id59 "Link to this heading")

```
 CREATE OR REPLACE TABLE case_table (
col varchar(30))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

Copy

#### Simple Case[¶](#simple-case "Link to this heading")

##### Teradata[¶](#id60 "Link to this heading")

##### Query[¶](#id61 "Link to this heading")

```
 CREATE  PROCEDURE caseExample1 ( grade NUMBER )
BEGIN
    CASE grade
        WHEN 10 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Excellent');
        WHEN 9 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Very Good');
        WHEN 8 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Good');
        WHEN 7 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Fair');
        WHEN 6 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Poor');
        ELSE INSERT INTO CASE_TABLE(COL) VALUES ('No such grade');
    END CASE;
END;

CALL caseExample1(6);
CALL caseExample1(4);
CALL caseExample1(10);
SELECT * FROM CASE_TABLE;
```

Copy

##### Result[¶](#id62 "Link to this heading")

```
|COL          |
|-------------|
|Poor         |
|No such grade|
|Excellent    |
```

Copy

##### Snowflake Scripting[¶](#id63 "Link to this heading")

##### Query[¶](#id64 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE caseExample1 (GRADE NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CASE (grade)
            WHEN 10 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Excellent');
            WHEN 9 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Very Good');
            WHEN 8 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Good');
            WHEN 7 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Fair');
            WHEN 6 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Poor');
            ELSE
                INSERT INTO CASE_TABLE (COL)
                VALUES ('No such grade');
        END CASE;
    END;
$$;

CALL caseExample1(6);
CALL caseExample1(4);
CALL caseExample1(10);
SELECT * FROM CASE_TABLE;
```

Copy

##### Result[¶](#id65 "Link to this heading")

```
|COL          |
|-------------|
|Poor         |
|No such grade|
|Excellent    |
```

Copy

#### Searched Case[¶](#searched-case "Link to this heading")

##### Teradata[¶](#id66 "Link to this heading")

##### Query[¶](#id67 "Link to this heading")

```
 CREATE PROCEDURE caseExample2 ( grade NUMBER )
BEGIN
    CASE
        WHEN grade = 10 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Excellent');
        WHEN grade = 9 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Very Good');
        WHEN grade = 8 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Good');
        WHEN grade = 7 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Fair');
        WHEN grade = 6 THEN INSERT INTO CASE_TABLE(COL) VALUES ('Poor');
        ELSE INSERT INTO CASE_TABLE(COL) VALUES ('No such grade');
    END CASE;
END;

CALL caseExample2(6);
CALL caseExample2(4);
CALL caseExample2(10);
SELECT * FROM CASE_TABLE;
```

Copy

##### Result[¶](#id68 "Link to this heading")

```
|COL          |
|-------------|
|Poor         |
|No such grade|
|Excellent    |
```

Copy

##### Snowflake Scripting[¶](#id69 "Link to this heading")

##### Query[¶](#id70 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE caseExample2 (GRADE NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CASE
            WHEN :grade = 10 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Excellent');
            WHEN :grade = 9 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Very Good');
            WHEN :grade = 8 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Good');
            WHEN :grade = 7 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Fair');
            WHEN :grade = 6 THEN
                INSERT INTO CASE_TABLE (COL)
                VALUES ('Poor');
                ELSE
                INSERT INTO CASE_TABLE (COL)
                VALUES ('No such grade');
        END CASE;
    END;
$$;

CALL caseExample2(6);

CALL caseExample2(4);

CALL caseExample2(10);

SELECT
    * FROM
    CASE_TABLE;
```

Copy

##### Result[¶](#id71 "Link to this heading")

```
|COL          |
|-------------|
|Poor         |
|No such grade|
|Excellent    |
```

Copy

### Known Issues[¶](#id72 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id73 "Link to this heading")

No related EWIs.

## CURSOR[¶](#cursor "Link to this heading")

Translation reference to convert Teradata CURSOR statement to Snowflake Scripting

### Description [¶](#id74 "Link to this heading")

A cursor is a data structure that is used by stored procedures at runtime to point to a resultset returned by an SQL query. For more information check [here](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/SQL-Cursor-Control-and-DML-Statements).

```
 DECLARE cursor_name [ SCROLL | NO SCROLL ] CURSOR
     [ 
          WITHOUT RETURN
          |
          WITH RETURN [ ONLY ] [ TO [ CALLER | CLIENT ] ]
     ]
     FOR
     cursor_specification [ FOR [ READ ONLY | UPDATE ] ]
     |
     statement_name
;
```

Copy

```
 FETCH [ [ NEXT | FIRST ] FROM ] cursor_name INTO
    [ variable_name | parameter_name ] [ ,...n ]
;
```

Copy

```
 OPEN cursor_name
    [ USING [ SQL_identifier | SQL_paramenter ] [ ,...n ] ]
;
```

Copy

```
 CLOSE cursor_name ;
```

Copy

### Sample Source Patterns [¶](#id75 "Link to this heading")

#### Setup Data[¶](#id76 "Link to this heading")

The following code is necessary to execute the sample patterns present in this section.

##### Teradata[¶](#id77 "Link to this heading")

```
 CREATE TABLE vEmployee(
    PersonID INT,
    LastName VARCHAR(255),
    FirstName VARCHAR(255)
);

CREATE TABLE ResTable(
    Column1 VARCHAR(255)
);

INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (1, 'Smith', 'Christian');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (2, 'Johnson', 'Jhon');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (3, 'Brown', 'William');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (4, 'Williams', 'Gracey');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (5, 'Garcia', 'Julia');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (6, 'Miller', 'Peter');
INSERT INTO vEmployee(PersonID, LastName, FirstName) VALUES (7, 'Davis', 'Jannys');

CREATE TABLE TEST_TABLE (
    ColumnA NUMBER, 
    ColumnB VARCHAR(8),
    ColumnC VARCHAR(8));


SELECT * FROM TEST_TABLE;
INSERT INTO TEST_TABLE VALUES (1, '1', '1');
INSERT INTO TEST_TABLE VALUES (2, '2', '2');
```

Copy

##### Snowflake[¶](#id78 "Link to this heading")

```
 CREATE OR REPLACE TABLE vEmployee (
    PersonID INT,
    LastName VARCHAR(255),
    FirstName VARCHAR(255)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

CREATE OR REPLACE TABLE ResTable (
    Column1 VARCHAR(255)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (1, 'Smith', 'Christian');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (2, 'Johnson', 'Jhon');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (3, 'Brown', 'William');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (4, 'Williams', 'Gracey');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (5, 'Garcia', 'Julia');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (6, 'Miller', 'Peter');

INSERT INTO vEmployee (PersonID, LastName, FirstName)
VALUES (7, 'Davis', 'Jannys');

CREATE OR REPLACE TABLE TEST_TABLE (
    ColumnA NUMBER(38, 18),
    ColumnB VARCHAR(8),
    ColumnC VARCHAR(8))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

SELECT
    * FROM
    TEST_TABLE;

    INSERT INTO TEST_TABLE
    VALUES (1, '1', '1');

    INSERT INTO TEST_TABLE
    VALUES (2, '2', '2');
```

Copy

#### Basic Cursor[¶](#basic-cursor "Link to this heading")

##### Teradata[¶](#id79 "Link to this heading")

##### Cursor Code[¶](#cursor-code "Link to this heading")

```
 REPLACE PROCEDURE CursorsTest()
BEGIN
    DECLARE val1 VARCHAR(255);
    DECLARE empcursor CURSOR FOR
        SELECT LastName
        FROM vEmployee
        ORDER BY PersonID;
    
    OPEN empcursor;
    FETCH NEXT FROM empcursor INTO val1;
    FETCH NEXT FROM empcursor INTO val1;
    INSERT INTO ResTable(Column1) VALUES (val1);
    CLOSE empcursor;
END;

CALL CursorsTest();
SELECT * FROM ResTable;
```

Copy

##### Result[¶](#id80 "Link to this heading")

```
Johnson
```

Copy

##### Snowflake Scripting[¶](#id81 "Link to this heading")

##### Cursor Code[¶](#id82 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE CursorsTest ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        val1 VARCHAR(255);
    BEGIN
         
        LET empcursor CURSOR
        FOR
            SELECT
                LastName
                   FROM
                vEmployee
                   ORDER BY PersonID;
        OPEN empcursor;
        FETCH NEXT FROM empcursor INTO val1;
            FETCH NEXT FROM empcursor INTO val1;
        INSERT INTO ResTable (Column1)
        VALUES (:val1);
            CLOSE empcursor;
    END;
$$;

CALL CursorsTest();

SELECT
    * FROM
    ResTable;
```

Copy

##### Result[¶](#id83 "Link to this heading")

```
Johnson
```

Copy

#### Single Returnable Cursor[¶](#single-returnable-cursor "Link to this heading")

The following procedure is intended to return one result set since it has the `DYNAMIC RESULT SETS 1` property in the header, the cursor has the `WITH RETURN` property and is being opened in the body.

##### Teradata[¶](#id84 "Link to this heading")

##### Cursor Code[¶](#id85 "Link to this heading")

```
 REPLACE PROCEDURE spSimple ()
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE result_set CURSOR WITH RETURN ONLY FOR
    SELECT *
    FROM vEmployee;
        
    OPEN result_set;
END;

CALL spSimple();
```

Copy

##### Result[¶](#id86 "Link to this heading")

```
PersonID|LastName|FirstName|
--------+--------+---------+
       7|Davis   |Jannys   |
       5|Garcia  |Julia    |
       3|Brown   |William  |
       1|Smith   |Christian|
       6|Miller  |Peter    |
       4|Williams|Gracey   |
       2|Johnson |Jhon     |
```

Copy

##### Snowflake Scripting[¶](#id87 "Link to this heading")

##### Cursor Code[¶](#id88 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE spSimple ()
RETURNS TABLE (
)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        LET result_set CURSOR FOR
            SELECT * FROM vEmployee;
        OPEN result_set;
        RETURN TABLE(resultset_from_cursor(result_set));
    END;
$$;

CALL spSimple();
```

Copy

##### Result[¶](#id89 "Link to this heading")

```
PERSONID|LASTNAME|FIRSTNAME|
--------+--------+---------+
       1|Smith   |Christian|
       2|Johnson |Jhon     |
       3|Brown   |William  |
       4|Williams|Gracey   |
       5|Garcia  |Julia    |
       6|Miller  |Peter    |
       7|Davis   |Jannys   |
```

Copy

#### Multiple Returnable Cursors[¶](#multiple-returnable-cursors "Link to this heading")

The following procedure is intended to return multiple results when `DYNAMIC RESULT SETS` property in the header is greater than 1, the procedure has multiple cursors with the `WITH RETURN` property and these same cursors are being opened in the body.

##### Teradata[¶](#id90 "Link to this heading")

##### Cursor Code[¶](#id91 "Link to this heading")

```
 REPLACE PROCEDURE spTwoOrMore()
DYNAMIC RESULT SETS 2
BEGIN
    DECLARE result_set CURSOR WITH RETURN ONLY FOR
        SELECT * FROM SampleTable2;

    DECLARE result_set2 CURSOR WITH RETURN ONLY FOR
	SELECT Column11 FROM SampleTable1;
    OPEN result_set2;
    OPEN result_set;
END;

CALL spTwoOrMore();
```

Copy

##### Result[¶](#id92 "Link to this heading")

```
ColumnA|ColumnB|ColumnC|
-------+-------+-------+
      2|2      |2      |
      1|1      |1      |

PersonID|LastName|FirstName|
--------+--------+---------+
       7|Davis   |Jannys   |
       5|Garcia  |Julia    |
       3|Brown   |William  |
       1|Smith   |Christian|
       6|Miller  |Peter    |
       4|Williams|Gracey   |
       2|Johnson |Jhon     |
```

Copy

##### Snowflake Scripting[¶](#id93 "Link to this heading")

##### Cursor Code[¶](#id94 "Link to this heading")

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "SampleTable2", "SampleTable1" **
CREATE OR REPLACE PROCEDURE spTwoOrMore ()
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		tbl_result_set VARCHAR;
		tbl_result_set2 VARCHAR;
		return_arr ARRAY := array_construct();
	BEGIN
		tbl_result_set := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_result_set) AS
			SELECT
				* FROM
				SampleTable2;
		LET result_set CURSOR
		FOR
			SELECT
				*
			FROM
				IDENTIFIER(?);
		tbl_result_set2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
		CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:tbl_result_set2) AS
			SELECT
				Column11 FROM
				SampleTable1;
		LET result_set2 CURSOR
		FOR
			SELECT
				*
			FROM
				IDENTIFIER(?);
		OPEN result_set2 USING (tbl_result_set2);
		return_arr := array_append(return_arr, :tbl_result_set2);
		OPEN result_set USING (tbl_result_set);
		return_arr := array_append(return_arr, :tbl_result_set);
		--** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
		RETURN return_arr;
	END;
$$;

CALL spTwoOrMore();
```

Copy

##### Results[¶](#results "Link to this heading")

```
[
  "RESULTSET_B5B0005D_1602_48B7_9EE4_62E1A28B000C",
  "RESULTSET_1371794D_7B77_4DA9_B42E_7981F35CEA9C"
]

ColumnA|ColumnB|ColumnC|
-------+-------+-------+
      2|2      |2      |
      1|1      |1      |

PersonID|LastName|FirstName|
--------+--------+---------+
       7|Davis   |Jannys   |
       5|Garcia  |Julia    |
       3|Brown   |William  |
       1|Smith   |Christian|
       6|Miller  |Peter    |
       4|Williams|Gracey   |
       2|Johnson |Jhon     |
```

Copy

#### Cursors With Binding Variables[¶](#cursors-with-binding-variables "Link to this heading")

The following cursor uses binding variables as the were condition to perform the query.

##### Teradata[¶](#id95 "Link to this heading")

##### Cursor Code[¶](#id96 "Link to this heading")

```
 REPLACE PROCEDURE TestProcedure (IN param1 NUMBER, param2 VARCHAR(8), param3 VARCHAR(8))
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE cursorExample CURSOR WITH RETURN ONLY FOR
        SELECT * FROM  TEST_TABLE
   	WHERE ColumnA = param1 AND ColumnB LIKE param2 and ColumnC LIKE param3;
    
    OPEN cursorExample;	  
END;
```

Copy

##### Result[¶](#id97 "Link to this heading")

```
|ColumnA|ColumnB|ColumnC|
+-------+-------+-------+
|      2|2      |2      |
```

Copy

##### Snowflake Scripting[¶](#id98 "Link to this heading")

##### Cursor Code[¶](#id99 "Link to this heading")

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TEST_TABLE" **
CREATE OR REPLACE PROCEDURE TestProcedure (PARAM1 NUMBER(38, 18), PARAM2 VARCHAR(8), PARAM3 VARCHAR(8))
RETURNS TABLE (
)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      LET cursorExample CURSOR
      FOR
         SELECT
            * FROM
            TEST_TABLE
           	WHERE ColumnA = ?
            AND ColumnB ILIKE ?
            and ColumnC ILIKE ?;
      OPEN cursorExample USING (param1, param2, param3);
      RETURN TABLE(resultset_from_cursor(cursorExample));
   END;
$$;
```

Copy

##### Result[¶](#id100 "Link to this heading")

```
|ColumnA|ColumnB|ColumnC|
+-------+-------+-------+
|      2|2      |2      |
```

Copy

#### Cursor For Loop[¶](#cursor-for-loop "Link to this heading")

It is a type of loop that uses a cursor to fetch rows from a SELECT statement and then performs some processing on each row.

##### Teradata[¶](#id101 "Link to this heading")

##### Cursor Code[¶](#id102 "Link to this heading")

```
 REPLACE PROCEDURE TestProcedure ()
DYNAMIC RESULT SETS 1
BEGIN
    FOR fUsgClass AS cUsgClass CURSOR FOR
        SELECT columnA FROM  TEST_TABLE
    DO
        INSERT INTO ResTable(Column1) VALUES (fUsgClass.columnA);
    END FOR;
END;

CALL TestProcedure();
SELECT * FROM ResTable;
```

Copy

##### Result[¶](#id103 "Link to this heading")

```
|Column1|
+-------+
|      1|
|      2|
```

Copy

##### Snowflake Scripting[¶](#id104 "Link to this heading")

##### Cursor Code[¶](#id105 "Link to this heading")

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "TEST_TABLE", "ResTable" **
CREATE OR REPLACE PROCEDURE TestProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        !!!RESOLVE EWI!!! /*** SSC-EWI-0110 - TRANSFORMATION NOT PERFORMED DUE TO MISSING DEPENDENCIES ***/!!!
        temp_fUsgClass_columnA;
    BEGIN
        LET cUsgClass CURSOR
        FOR
            SELECT
                columnA FROM
                TEST_TABLE;
        --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
        FOR fUsgClass IN cUsgClass DO
            temp_fUsgClass_columnA := fUsgClass.columnA;
            INSERT INTO ResTable (Column1)
            VALUES (:temp_fUsgClass_columnA);
        END FOR;
    END;
$$;

CALL TestProcedure();

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "ResTable" **
SELECT
    * FROM
    ResTable;
```

Copy

##### Result[¶](#id106 "Link to this heading")

```
|Column1|
+-------+
|      1|
|      2|
```

Copy

#### Cursor Fetch inside a Loop[¶](#cursor-fetch-inside-a-loop "Link to this heading")

It allows one to retrieve rows from a result set one at a time and perform some processing on each row.

##### Teradata[¶](#id107 "Link to this heading")

##### Cursor Code[¶](#id108 "Link to this heading")

```
 REPLACE PROCEDURE teradata_fetch_inside_loop() 
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE col_name VARCHAR(255);
    DECLARE col_int INTEGER DEFAULT 1;
    DECLARE cursor_var CURSOR FOR SELECT columnA FROM TEST_TABLE;
    WHILE (col_int <> 0) DO		
        FETCH cursor_var INTO col_name;
        INSERT INTO ResTable(Column1) VALUES (cursor_var.columnA);
        SET col_int = 0;
    END WHILE;
END;

CALL teradata_fetch_inside_loop();
SELECT * FROM ResTable;
```

Copy

##### Result[¶](#id109 "Link to this heading")

```
|Column1|
+-------+
|      2|
```

Copy

##### Snowflake Scripting[¶](#id110 "Link to this heading")

##### Cursor Code[¶](#id111 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE teradata_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        col_name VARCHAR(255);
        col_int INTEGER DEFAULT 1;
    BEGIN
         
         
        LET cursor_var CURSOR
        FOR
            SELECT
                columnA FROM
                TEST_TABLE;
                WHILE (:col_int <> 0) LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
                    FETCH cursor_var INTO col_name;
            INSERT INTO ResTable (Column1)
            VALUES (cursor_var.columnA);
            col_int := 0;
                END LOOP;
    END;
$$;

CALL teradata_fetch_inside_loop();

SELECT
    * FROM
    ResTable;
```

Copy

##### Result[¶](#id112 "Link to this heading")

```
|Column1|
+-------+
|      2|
```

Copy

### Known Issues[¶](#id113 "Link to this heading")

The following parameters are not applicable in Snowflake Scripting.

#### 1. Declare[¶](#declare "Link to this heading")

[ SCROLL/NO SCROLL ] Snowflake Scripting only supports FETCH NEXT.

[ READ-ONLY ] This is the default in Snowflake Scripting.

[ UPDATE ].

##### 2. Fetch[¶](#fetch "Link to this heading")

[ NEXT ] This is the default behavior in Snowflake Scripting.

[ FIRST ].

### Related EWIs[¶](#id114 "Link to this heading")

1. [SSC-FDM-0020](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0020): Multiple result sets are returned in temporary tables.
2. [SSC-PRF-0003](../../general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html#ssc-prf-0003): Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance.
3. [SSC-PRF-0004](../../general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html#ssc-prf-0004): This statement has usages of cursor for loop.

## DECLARE CONTINUE HANDLER[¶](#declare-continue-handler "Link to this heading")

Translation reference to convert Teradata DECLARE CONTINUE handler to Snowflake Scripting

### Description [¶](#id115 "Link to this heading")

> Handle completion conditions and exception conditions not severe enough to affect the flow of control.

For more information regarding the Teradata DECLARE CONTINUE handler, check [here](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Stored-Procedures-and-Embedded-SQL/Condition-Handling/DECLARE-HANDLER-CONTINUE-Type).

```
 DECLARE CONTINUE HANDLER FOR
  { 
    { sqlstate_state_spec | condition_name } [,...] |

    { SQLEXCEPTION | SQLWARNING | NOT FOUND } [,...]

  } handler_action_statement ;
```

Copy

### Sample Source Patterns [¶](#id116 "Link to this heading")

#### DECLARE CONTINUE HANDLER[¶](#id117 "Link to this heading")

##### Teradata [¶](#id118 "Link to this heading")

##### Query[¶](#id119 "Link to this heading")

```
 REPLACE PROCEDURE PURGING_ADD_TABLE
( 
 IN inDatabaseName     	VARCHAR(30), 
 IN inTableName    		VARCHAR(30)
)
BEGIN
 DECLARE vCHAR_SQLSTATE CHAR(5);
 DECLARE vSUCCESS       CHAR(5);

  DECLARE CONTINUE HANDLER FOR SQLSTATE 'T5628'
  BEGIN
     SET vCHAR_SQLSTATE = SQLCODE;
     SET vSUCCESS    = SQLCODE;
  END;

  SELECT 1;
 
END;
```

Copy

##### Snowflake Scripting [¶](#id120 "Link to this heading")

##### Query[¶](#id121 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE PURGING_ADD_TABLE
(INDATABASENAME VARCHAR(30), INTABLENAME VARCHAR(30)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  vCHAR_SQLSTATE CHAR(5);
  vSUCCESS       CHAR(5);
 BEGIN
   
   
  BEGIN
   SELECT
    1;
  EXCEPTION
   WHEN statement_error THEN
    LET errcode := :sqlcode
    LET sqlerrmsg := :sqlerrm
    IF (errcode = '904'
    AND contains(sqlerrmsg, 'invalid value')) THEN
     BEGIN
      vCHAR_SQLSTATE := SQLCODE;
      vSUCCESS := SQLCODE;
     END;
    ELSE
     RAISE
    END IF
  END
 END;
$$;
```

Copy

### Known Issues[¶](#id122 "Link to this heading")

#### DECLARE CONTINUE HANDLER FOR SQLSTATE[¶](#declare-continue-handler-for-sqlstate "Link to this heading")

The support of declaring continue handlers for some SQLSTATE values is not currently supported by Snowflake Scripting.

##### Teradata [¶](#id123 "Link to this heading")

##### Query[¶](#id124 "Link to this heading")

```
 CREATE PROCEDURE declareConditionExample2 ( )
BEGIN
   DECLARE CONTINUE HANDLER FOR SQLSTATE 'UNSUPPORTED'
     BEGIN
       SET vCHAR_SQLSTATE = SQLCODE;
       SET vSUCCESS    = SQLCODE;
    END;
END;
```

Copy

##### Snowflake Scripting [¶](#id125 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE declareConditionExample2 ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      !!!RESOLVE EWI!!! /*** SSC-EWI-TD0004 - NOT SUPPORTED SQL EXCEPTION ON CONTINUE HANDLER ***/!!!
      DECLARE CONTINUE HANDLER FOR SQLSTATE 'UNSUPPORTED'
      BEGIN
         vCHAR_SQLSTATE := SQLCODE;
         vSUCCESS := SQLCODE;
      END;
   END;
$$;
```

Copy

### Related EWIS[¶](#id126 "Link to this heading")

1. [SSC-EWI-TD0004](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0004): Not supported SQL Exception on continue handler.

## DECLARE CONDITION HANDLER[¶](#declare-condition-handler "Link to this heading")

Translation reference to convert Teradata DECLARE CONDITION handler to Snowflake Scripting

### Description [¶](#id127 "Link to this heading")

> Assign a name to an SQLSTATE code, or declare a user-defined condition.

For more information regarding the Teradata DECLARE CONDITION handler, check [here](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/Condition-Handling/DECLARE-CONDITION).

```
 DECLARE condition_name CONDITION
    [ FOR SQLSTATE [ VALUE ] sqlstate_code ] ;
```

Copy

### Sample Source Patterns [¶](#id128 "Link to this heading")

#### DECLARE CONDITION[¶](#declare-condition "Link to this heading")

##### Teradata [¶](#id129 "Link to this heading")

##### Query[¶](#id130 "Link to this heading")

```
 CREATE PROCEDURE declareConditionExample ( )
BEGIN
    DECLARE DB_ERROR CONDITION;
    ...
END;
```

Copy

##### Snowflake Scripting [¶](#id131 "Link to this heading")

##### Query[¶](#id132 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE declareConditionExample ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        DB_ERROR EXCEPTION;
    BEGIN
    END;
$$;
```

Copy

### Known Issues[¶](#id133 "Link to this heading")

#### DECLARE CONDITION FOR SQLSTATE[¶](#declare-condition-for-sqlstate "Link to this heading")

The support of declaring conditions for SQLSTATE values is not currently supported by Snowflake Scripting.

##### Teradata [¶](#id134 "Link to this heading")

##### Query[¶](#id135 "Link to this heading")

```
 CREATE PROCEDURE declareConditionExample2 ( )
BEGIN
    DECLARE ERROR_EXISTS CONDITION FOR SQLSTATE VALUE '42000';
END;
```

Copy

##### Snowflake Scripting [¶](#id136 "Link to this heading")

##### Query[¶](#id137 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE declareConditionExample2 ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        ERROR_EXISTS EXCEPTION;
    BEGIN
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'SET EXCEPTION DETAILS' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
-- ERROR_EXISTS CONDITION FOR SQLSTATE VALUE '42000';
    END;
$$;
```

Copy

### Related EWIS[¶](#id138 "Link to this heading")

1. [SSC-EWI-0058:](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0058) Functionality is not currently supported by Snowflake Scripting.

## DECLARE[¶](#id139 "Link to this heading")

Translation reference to convert Teradata DECLARE statement to Snowflake Scripting

### Description [¶](#id140 "Link to this heading")

> Declares one or more local variables.

For more information regarding Teradata DECLARE, check [here](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/SQL-Control-Statements/DECLARE).

```
 DECLARE variable_name [, variable_name ]... DATA_TYPE [ DEFAULT default_value]
```

Copy

### Sample Source Patterns [¶](#id141 "Link to this heading")

#### Teradata [¶](#id142 "Link to this heading")

##### Query[¶](#id143 "Link to this heading")

```
 CREATE PROCEDURE declareExample ( )
BEGIN
    DECLARE COL_NAME, COL_TYPE VARCHAR(200) DEFAULT '' ;
    DECLARE COL_COUNT, COL_LEN INTEGER;
END;
```

Copy

##### Snowflake Scripting [¶](#id144 "Link to this heading")

##### Query[¶](#id145 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE declareExample ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        COL_NAME VARCHAR(200) DEFAULT '';
        COL_TYPE VARCHAR(200) DEFAULT '';
        COL_COUNT INTEGER;
        COL_LEN INTEGER;
    BEGIN
         
         
        RETURN 1;
    END;
$$;
```

Copy

### Known Issues[¶](#id146 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id147 "Link to this heading")

No related EWIs.

## DML and DDL Objects[¶](#dml-and-ddl-objects "Link to this heading")

### Description [¶](#id148 "Link to this heading")

DML and DDL objects are translated in the same way regardless of whether they are inside stored procedures or not. For further information check the following links.

### Translation References[¶](#translation-references "Link to this heading")

* [data-types.md](sql-translation-reference/data-types): Compare Teradata data types and their equivalents in Snowflake.
* [ddl](sql-translation-reference/ddl-teradata): Explore the translation of the Data Definition Language.
* [dml](sql-translation-reference/dml-teradata): Explore the translation of the Data Manipulation Language.
* [built-in-functions](sql-translation-reference/teradata-built-in-functions): Compare functions included in the runtime of both languages.

## EXCEPTION HANDLERS[¶](#exception-handlers "Link to this heading")

Translation reference to convert Teradata EXCEPTION HANDLERS clause to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id149 "Link to this heading")

Teradata’s single and multiple Exception Handlers are replaced by its equivalent handlers in Snowflake Scripting.

For more information regarding Teradata EXCEPTION HANDLERS, check [here](https://docs.teradata.com/r/zzfV8dn~lAaKSORpulwFMg/gH3xxgeVDpIqVBjEQfppyQ).

```
 DECLARE < handler_type > HANDLER
  FOR  < condition_value_list > < handler_action > ;
```

Copy

### Sample Source Patterns [¶](#id150 "Link to this heading")

#### SQLEXCEPTION HANDLER[¶](#sqlexception-handler "Link to this heading")

##### Teradata [¶](#id151 "Link to this heading")

##### Single handler[¶](#single-handler "Link to this heading")

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        INSERT INTO Proc_Error_Table ('procSample', 'Failed SqlException');
    SELECT * FROM Proc_Error_Table;
END;
```

Copy

##### Multiple handlers[¶](#multiple-handlers "Link to this heading")

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE ConditionByUser1 CONDITION;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        INSERT INTO Proc_Error_Table ('procSample', 'Failed SqlException');
    DECLARE EXIT HANDLER FOR ConditionByUser1
        INSERT INTO Proc_Error_Table ('procSample', 'Failed ConditionByUser1');
    SELECT * FROM Proc_Error_Table;
END;
```

Copy

##### Snowflake Scripting [¶](#id152 "Link to this heading")

##### Single handler[¶](#id153 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
         
        SELECT
            * FROM
            Proc_Error_Table;
    EXCEPTION
            WHEN other THEN
            INSERT INTO Proc_Error_Table
            VALUES ('procSample', 'Failed SqlException');
    END;
$$;
```

Copy

##### Multiple handlers[¶](#id154 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        ConditionByUser1 EXCEPTION;
    BEGIN
         
         
        SELECT
            * FROM
            Proc_Error_Table;
    EXCEPTION
            WHEN ConditionByUser1 THEN
            INSERT INTO Proc_Error_Table
            VALUES ('procSample', 'Failed ConditionByUser1');
            WHEN other THEN
            INSERT INTO Proc_Error_Table
            VALUES ('procSample', 'Failed SqlException');
    END;
$$;
```

Copy

#### User-Defined Handlers[¶](#user-defined-handlers "Link to this heading")

##### Teradata [¶](#id155 "Link to this heading")

##### Query[¶](#id156 "Link to this heading")

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE EXIT HANDLER FOR Custom1, Custom2, Custom3
      BEGIN
        SET Message1 = 'custom1 and custom2 and custom3';
      END;
    SELECT * FROM Proc_Error_Table;
END;
```

Copy

##### Snowflake Scripting [¶](#id157 "Link to this heading")

##### Query[¶](#id158 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
         
        SELECT
            * FROM
            Proc_Error_Table;
    EXCEPTION
            WHEN Custom1 OR Custom2 OR Custom3 THEN
            BEGIN
                    Message1 := 'custom1 and custom2 and custom3';
            END;
    END;
$$;
```

Copy

### Known Issues[¶](#id159 "Link to this heading")

#### CONTINUE Handler[¶](#continue-handler "Link to this heading")

Danger

A ‘CONTINUE’ handler in Teradata allows the execution to be resumed after executing a statement with errors. This is not supported by the exception blocks in Snowflake Scripting. [Condition Handler Teradata reference documentation.](https://docs.teradata.com/r/CeAGk~BNtx~axcR0ed~5kw/EN6T2zEDlgBRvSKjw7shUg)

##### Teradata [¶](#id160 "Link to this heading")

##### Query[¶](#id161 "Link to this heading")

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO Proc_Error_Table ('spSample4', 'Failed SqlException');
    SELECT * FROM Proc_Error_Table;
END;
```

Copy

##### Snowflake Scripting [¶](#id162 "Link to this heading")

##### Query[¶](#id163 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        !!!RESOLVE EWI!!! /*** SSC-EWI-TD0004 - NOT SUPPORTED SQL EXCEPTION ON CONTINUE HANDLER ***/!!!
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        INSERT INTO Proc_Error_Table
        VALUES ('spSample4', 'Failed SqlException');
        SELECT
            * FROM
            Proc_Error_Table;
    END;
$$;
```

Copy

#### Other not supported handlers[¶](#other-not-supported-handlers "Link to this heading")

Danger

Handlers for SQLSTATE, SQLWARNING, and NOT FOUND are not supported

##### Teradata [¶](#id164 "Link to this heading")

##### Query[¶](#id165 "Link to this heading")

```
 CREATE PROCEDURE handlerSample ()
BEGIN
    DECLARE EXIT HANDLER FOR SQLSTATE '42002', SQLWARNING, NOT FOUND
        INSERT INTO Proc_Error_Table ('procSample', 'Failed SqlState or SqlWarning or Not Found');
    SELECT * FROM Proc_Error_Table;
END;
```

Copy

##### Snowflake Scripting [¶](#id166 "Link to this heading")

##### Query[¶](#id167 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE handlerSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/04/2024" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'SQLSTATE, SQLWARNING, NOT-FOUND TYPES HANDLER' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--        DECLARE EXIT HANDLER FOR SQLSTATE '42002', SQLWARNING, NOT FOUND
--            INSERT INTO Proc_Error_Table ('procSample', 'Failed SqlState or SqlWarning or Not Found');
        SELECT
            * FROM
            Proc_Error_Table;
    END;
$$;
```

Copy

### Related EWIS[¶](#id168 "Link to this heading")

1. [SSC-EWI-0058](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting.
2. [SSC-EWI-TD0004](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI.html#ssc-ewi-td0004): Not supported SQL Exception on continue handler.

## EXECUTE/EXEC[¶](#execute-exec "Link to this heading")

Translation reference to convert Teradata EXECUTE or EXEC statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id169 "Link to this heading")

The Teradata `EXECUTE`statement allows the execution prepared dynamic SQL or macros, on the other hand exec only allows macros.

For more information regarding Teradata EXECUTE/EXEC, check [Macro Form](https://docs.teradata.com/r/Teradata-Database-SQL-Data-Manipulation-Language/June-2017/Statement-Syntax/EXECUTE-Macro-Form) and [Dynamic SQL Form](https://docs.teradata.com/r/Teradata-Database-SQL-Stored-Procedures-and-Embedded-SQL/June-2017/Dynamic-Embedded-SQL-Statements/Dynamic-SQL-Statement-Syntax/EXECUTE-Dynamic-SQL-Form)

```
 -- EXECUTE macro syntax
{EXECUTE | EXEC } macro_identifier [ (<parameter_definition>[, ...n] ) ] [;]  

<parameter_definition>:= {parameter_name = constant_expression | constant_expresion}


-- EXECUTE prepared dynamic SQL syntax
EXECUTE prepare_indentifier [<using>|<usingDescriptor>]

<using>:= USING < host_variable >[, ...n]
<host_variable>:= [:] host_variable_name [[INDICATOR] :host_indicator_name]
<usingDescriptor>:= USING DESCRIPTOR [:] descript_area
```

Copy

### Sample Source Patterns [¶](#id170 "Link to this heading")

#### Setup data[¶](#id171 "Link to this heading")

The following code is necessary to execute the sample patterns present in this section.

##### Teradata[¶](#id172 "Link to this heading")

```
 -- Additional Params: -t JavaScript
CREATE TABLE inventory (
    product_name VARCHAR(50),
    price INTEGER
);

CREATE MACRO dummyMacro AS(
  SELECT * FROM INVENTORY;
);
```

Copy

##### Snowflake[¶](#id173 "Link to this heading")

```
 CREATE OR REPLACE TABLE inventory (
  product_name VARCHAR(50),
  price INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

CREATE OR REPLACE PROCEDURE dummyMacro ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.
  
  INSERT_TEMP(`SELECT
   *
  FROM
   INVENTORY`,[]);
  return tablelist;
$$;
```

Copy

#### Execute prepared statement[¶](#execute-prepared-statement "Link to this heading")

##### Teradata[¶](#id174 "Link to this heading")

##### Execute[¶](#execute "Link to this heading")

```
 CREATE PROCEDURE InsertProductInInventory(IN productName VARCHAR(50), IN price INTEGER)
BEGIN
    DECLARE dynamicSql CHAR(200);
    SET dynamicSql = 'INSERT INTO INVENTORY VALUES( ?, ?)';
    PREPARE preparedSql FROM dynamicSql;
    EXECUTE preparedSql USING productName, price;
    
END;

CALL InsertProductInInventory('''Chocolate''', 75);
CALL InsertProductInInventory('''Sugar''', 65);
CALL InsertProductInInventory('''Rice''', 100);
```

Copy

##### Snowflake Scripting [¶](#id175 "Link to this heading")

##### Execute[¶](#id176 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE InsertProductInInventory (PRODUCTNAME VARCHAR(50), PRICE INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        dynamicSql CHAR(200);
    BEGIN
         
        dynamicSql := 'INSERT INTO INVENTORY
VALUES (?, ?)';
        !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PREPARE STATEMENT' NODE ***/!!!
            PREPARE preparedSql FROM dynamicSql;
        !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
        EXECUTE IMMEDIATE dynamicSql;
    END;
$$;

CALL InsertProductInInventory('''Chocolate''', 75);

CALL InsertProductInInventory('''Sugar''', 65);

CALL InsertProductInInventory('''Rice''', 100);
```

Copy

#### Execute macro statement[¶](#execute-macro-statement "Link to this heading")

##### Teradata[¶](#id177 "Link to this heading")

##### Execute[¶](#id178 "Link to this heading")

```
 EXECUTE dummyMacro;
```

Copy

##### Result[¶](#id179 "Link to this heading")

```
+---------------+-------+
| product_name  | price |
+---------------+-------+
| 'Chocolate'   | 75    |
+---------------+-------+
| 'Sugar'       | 65    |
+---------------+-------+
| 'Rice'        | 100   |
+---------------+-------+
```

Copy

##### Snowflake Scripting [¶](#id180 "Link to this heading")

##### Execute[¶](#id181 "Link to this heading")

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
EXECUTE IMMEDIATE dummyMacro;
```

Copy

### Related EWIs[¶](#id182 "Link to this heading")

1. [SSC-EWI-0030:](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0030) The statement below has usages of dynamic SQL.
2. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## EXECUTE IMMEDIATE[¶](#execute-immediate "Link to this heading")

Translation reference to convert Teradata EXECUTE IMMENDIATE statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id183 "Link to this heading")

The Teradata `EXECUTE IMMEDIATE` statement allows the execution of dynamic SQL contained on variables or string literals.

For more information about `EXECUTE IMMEDIATE` click [here](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/Dynamic-Embedded-SQL-Statements/Dynamic-SQL-Statement-Syntax/EXECUTE-IMMEDIATE).

```
 -- EXECUTE IMMEDIATE syntax
EXECUTE IMMEDIATE <dynamic_statement>

<dynamic_statement> := {string_literal | string_variable}
```

Copy

### Sample Source Patterns [¶](#id184 "Link to this heading")

#### Setup data[¶](#id185 "Link to this heading")

The following code is necessary to execute the sample patterns present in this section.

##### Teradata[¶](#id186 "Link to this heading")

```
 CREATE TABLE inventory (
    product_name VARCHAR(50),
    price INTEGER
);
```

Copy

##### Snowflake[¶](#id187 "Link to this heading")

```
 CREATE OR REPLACE TABLE inventory (
    product_name VARCHAR(50),
    price INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

Copy

#### Execute Example [¶](#execute-example "Link to this heading")

##### Teradata [¶](#id188 "Link to this heading")

##### Query[¶](#id189 "Link to this heading")

```
 REPLACE PROCEDURE InsertProductInInventory(IN productName VARCHAR(50), IN price INTEGER)
BEGIN
	DECLARE insertStatement VARCHAR(100);
	SET insertStatement = 'INSERT INTO INVENTORY VALUES(' || productName || ', ' || price || ')';
    EXECUTE IMMEDIATE insertStatement;
END;

CALL InsertProductInInventory('''Chocolate''', 75);
CALL InsertProductInInventory('''Sugar''', 65);
CALL InsertProductInInventory('''Rice''', 100);

SELECT product_name, price FROM inventory;
```

Copy

##### Result[¶](#id190 "Link to this heading")

```
+--------------+-------+
| product_name | price |
+--------------+-------+
| Chocolate    | 75    |
+--------------+-------+
| Sugar        | 65    |
+--------------+-------+
| Rice         | 100   |
+--------------+-------+
```

Copy

##### Snowflake Scripting [¶](#id191 "Link to this heading")

##### Query[¶](#id192 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE InsertProductInInventory (PRODUCTNAME VARCHAR(50), PRICE INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		insertStatement VARCHAR(100);
	BEGIN
		 
		insertStatement := 'INSERT INTO INVENTORY
VALUES (' || productName || ', ' || price || ')';
		!!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
		EXECUTE IMMEDIATE insertStatement;
	END;
$$;

CALL InsertProductInInventory('''Chocolate''', 75);

CALL InsertProductInInventory('''Sugar''', 65);

CALL InsertProductInInventory('''Rice''', 100);

SELECT
	product_name,
	price FROM
	inventory;
```

Copy

##### Result[¶](#id193 "Link to this heading")

```
+--------------+-------+
| PRODUCT_NAME | PRICE |
+--------------+-------+
| Chocolate    | 75    |
+--------------+-------+
| Sugar        | 65    |
+--------------+-------+
| Rice         | 100   |
+--------------+-------+
```

Copy

##### Result[¶](#id194 "Link to this heading")

```
column1|column2                  |column3|
-------+-------------------------+-------+
      3|Mundo3                   |    3.3|
```

Copy

### Related EWIS[¶](#id195 "Link to this heading")

1. [SSC-EWI-0030](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0030): The statement below has usages of dynamic SQL.

## FUNCTION OPTIONS OR DATA ACCESS[¶](#function-options-or-data-access "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

Note

Non-relevant statement.

Warning

**Notice that this statement is****removed from the migration****because it is a non-relevant syntax. It means that it is not required in Snowflake.**

### Description[¶](#id196 "Link to this heading")

Functions options or data access options are statements used in functions on the declaration part to specify certain characteristics. These can be:

* `CONTAINS SQL`
* `SQL SECURITY DEFINER`
* `COLLATION INVOKER`
* `SPECIFIC FUNCTION_NAME`

### Sample Source Patterns[¶](#id197 "Link to this heading")

#### Function Options[¶](#function-options "Link to this heading")

Notice that in this example the function options have been removed because they are not required in Snowflake.

##### Teradata[¶](#id198 "Link to this heading")

```
 CREATE FUNCTION sumValues(A INTEGER, B INTEGER)
   RETURNS INTEGER
   LANGUAGE SQL
   CONTAINS SQL
   SQL SECURITY DEFINER
   SPECIFIC sumTwoValues
   COLLATION INVOKER
   INLINE TYPE 1
   RETURN A + B;
```

Copy

##### Snowflake[¶](#id199 "Link to this heading")

```
 CREATE OR REPLACE FUNCTION sumValues (A INTEGER, B INTEGER)
   RETURNS INTEGER
   LANGUAGE SQL
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
   AS
   $$
      A + B
   $$;
```

Copy

### Known Issues [¶](#id200 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id201 "Link to this heading")

No related EWIs.

## GET DIAGNOSTICS EXCEPTION[¶](#get-diagnostics-exception "Link to this heading")

Translation reference to convert Teradata GET DIAGNOSTICS EXCEPTION statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id202 "Link to this heading")

> GET DIAGNOSTICS retrieves information about successful, exception, or completion conditions from the Diagnostics Area.

For more information regarding Teradata GET DIAGNOSTICS, check [here](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/Condition-Handling/GET-DIAGNOSTICS).

```
 GET DIAGNOSTICS
{
  [ EXCEPTION < condition_number >
    [ < parameter_name | variable_name > = < information_item > ]...
  ] 
  |
  [ < parameter_name | variable_name > = < information_item > ]...
}
```

Copy

### Sample Source Patterns [¶](#id203 "Link to this heading")

#### Teradata [¶](#id204 "Link to this heading")

##### Query[¶](#id205 "Link to this heading")

```
 CREATE PROCEDURE getDiagnosticsSample ()
BEGIN
    DECLARE V_MESSAGE, V_CODE VARCHAR(200);
    DECLARE V_Result INTEGER;
    
    SELECT c1 INTO V_Result FROM tab1;
    GET DIAGNOSTICS EXCEPTION 1
        V_MESSAGE = Message_Text,
        V_CODE = RETURNED_SQLSTATE;
END;
```

Copy

##### Snowflake Scripting [¶](#id206 "Link to this heading")

##### Query[¶](#id207 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE getDiagnosticsSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        V_MESSAGE VARCHAR(200);
        V_CODE VARCHAR(200);
        V_Result INTEGER;
    BEGIN
         
         
        SELECT
            c1 INTO
            :V_Result
        FROM
            tab1;
            V_MESSAGE := SQLERRM;
            V_CODE := SQLSTATE;
    END;
$$;
```

Copy

### Known Issues[¶](#id208 "Link to this heading")

#### CLASS\_ORIGIN, CONDITION\_NUMBER[¶](#class-origin-condition-number "Link to this heading")

Danger

The use of GET DIAGNOSTICS for CLASS\_ORIGIN, CONDITION\_NUMBER is not supported

##### Teradata [¶](#id209 "Link to this heading")

##### Query[¶](#id210 "Link to this heading")

```
 CREATE PROCEDURE getDiagnosticsSample ()
BEGIN
    DECLARE V_MESSAGE, V_CODE VARCHAR(200);
    DECLARE V_Result INTEGER;
    
    SELECT c1 INTO V_Result FROM tab1;
    GET DIAGNOSTICS EXCEPTION 5
        V_CLASS = CLASS_ORIGIN,
        V_COND = CONDITION_NUMBER;
END;
```

Copy

##### Snowflake Scripting [¶](#id211 "Link to this heading")

##### Query[¶](#id212 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE getDiagnosticsSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "06/18/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        V_MESSAGE VARCHAR(200);
        V_CODE VARCHAR(200);
        V_Result INTEGER;
    BEGIN
         
         
        SELECT
            c1 INTO
            :V_Result
        FROM
            tab1;
--            V_CLASS = CLASS_ORIGIN
                                  !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'GET DIAGNOSTICS DETAIL FOR CLASS_ORIGIN' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
             
--            V_COND = CONDITION_NUMBER
                                     !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'GET DIAGNOSTICS DETAIL FOR CONDITION_NUMBER' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
             
    END;
$$;
```

Copy

### Related EWIS[¶](#id213 "Link to this heading")

1. [SSC-EWI-0058](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting.

## IF[¶](#if "Link to this heading")

Translation reference to convert Teradata IF statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id214 "Link to this heading")

> Provides conditional execution based on the truth value of a condition.

For more information regarding Teradata IF, check [here](https://docs.teradata.com/r/zzfV8dn~lAaKSORpulwFMg/BER5lYjGTnRKex5a8eznnA).

```
 IF conditional_expression THEN
     statement
     [ statement ]... 
[ ELSEIF conditional_expression THEN
     statement
     [ statement ]... ]...
[ ELSE   
     statement
     [ statement ]... ]
END IF;
```

Copy

### Sample Source Patterns [¶](#id215 "Link to this heading")

#### Sample auxiliar table[¶](#id216 "Link to this heading")

##### Teradata[¶](#id217 "Link to this heading")

```
 CREATE TABLE if_table(col1 varchar(30));
```

Copy

##### Snowflake[¶](#id218 "Link to this heading")

```
 CREATE OR REPLACE TABLE if_table (
col1 varchar(30))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

Copy

#### Possible IF variations[¶](#possible-if-variations "Link to this heading")

##### Teradata [¶](#id219 "Link to this heading")

##### Code 1[¶](#code-1 "Link to this heading")

```
 CREATE PROCEDURE ifExample1 ( flag NUMBER )
BEGIN
   IF flag = 1 THEN
      INSERT INTO if_table(col1) VALUES ('one');
   END IF;
END;

CALL ifExample1(1);
SELECT * FROM if_table;
```

Copy

##### Code 2[¶](#code-2 "Link to this heading")

```
 CREATE PROCEDURE ifExample2 ( flag NUMBER )
BEGIN
   IF flag = 1 THEN
      INSERT INTO if_table(col1) VALUES ('one');
   ELSE
      INSERT INTO if_table(col1) VALUES ('Unexpected input.');
   END IF;
END;

CALL ifExample2(2);
SELECT * FROM if_table;
```

Copy

##### Code 3[¶](#code-3 "Link to this heading")

```
 CREATE PROCEDURE ifExample3 ( flag NUMBER )
BEGIN
   IF flag = 1 THEN
      INSERT INTO if_table(col1) VALUES ('one');
   ELSEIF flag = 2 THEN
      INSERT INTO if_table(col1) VALUES ('two');
   ELSEIF flag = 3 THEN
      INSERT INTO if_table(col1) VALUES ('three');
   END IF;
END;

CALL ifExample3(3);
SELECT * FROM if_table;
```

Copy

##### Code 4[¶](#code-4 "Link to this heading")

```
 CREATE PROCEDURE ifExample4 ( flag NUMBER )
BEGIN
   IF flag = 1 THEN
      INSERT INTO if_table(col1) VALUES ('one');
   ELSEIF flag = 2 THEN
      INSERT INTO if_table(col1) VALUES ('two');
   ELSEIF flag = 3 THEN
      INSERT INTO if_table(col1) VALUES ('three');
   ELSE
      INSERT INTO if_table(col1) VALUES ('Unexpected input.');  
   END IF;
END;

CALL ifExample4(4);
SELECT * FROM if_table;
```

Copy

##### Result 1[¶](#result-1 "Link to this heading")

```
|COL1|
|----|
|one |
```

Copy

##### Result 2[¶](#result-2 "Link to this heading")

```
|COL1             |
|-----------------|
|Unexpected input.|
```

Copy

##### Result 3[¶](#result-3 "Link to this heading")

```
|COL1 |
|-----|
|three|
```

Copy

##### Result 4[¶](#result-4 "Link to this heading")

```
|COL1             |
|-----------------|
|Unexpected input.|
```

Copy

##### Snowflake Scripting[¶](#id220 "Link to this heading")

##### Query 1[¶](#query-1 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE ifExample1 (FLAG NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      IF (:flag = 1) THEN
         INSERT INTO if_table (col1)
         VALUES ('one');
      END IF;
   END;
$$;

CALL ifExample1(1);

SELECT
   * FROM
   if_table;
```

Copy

##### Query 2[¶](#query-2 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE ifExample2 (FLAG NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      IF (:flag = 1) THEN
         INSERT INTO if_table (col1)
         VALUES ('one');
      ELSE
         INSERT INTO if_table (col1)
         VALUES ('Unexpected input.');
      END IF;
   END;
$$;

CALL ifExample2(2);

SELECT
   * FROM
   if_table;
```

Copy

##### Query 3[¶](#query-3 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE ifExample3 (FLAG NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      IF (:flag = 1) THEN
         INSERT INTO if_table (col1)
         VALUES ('one');
      ELSEIF (:flag = 2) THEN
         INSERT INTO if_table (col1)
         VALUES ('two');
      ELSEIF (:flag = 3) THEN
         INSERT INTO if_table (col1)
         VALUES ('three');
      END IF;
   END;
$$;

CALL ifExample3(3);

SELECT
   * FROM
   if_table;
```

Copy

##### Query 4[¶](#query-4 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE ifExample4 (FLAG NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      IF (:flag = 1) THEN
         INSERT INTO if_table (col1)
         VALUES ('one');
      ELSEIF (:flag = 2) THEN
         INSERT INTO if_table (col1)
         VALUES ('two');
      ELSEIF (:flag = 3) THEN
         INSERT INTO if_table (col1)
         VALUES ('three');
      ELSE
         INSERT INTO if_table (col1)
         VALUES ('Unexpected input.');
      END IF;
   END;
$$;

CALL ifExample4(4);

SELECT
   * FROM
   if_table;
```

Copy

##### Result 1[¶](#id221 "Link to this heading")

```
|COL1|
|----|
|one |
```

Copy

##### Result 2[¶](#id222 "Link to this heading")

```
|COL1             |
|-----------------|
|Unexpected input.|
```

Copy

##### Result 3[¶](#id223 "Link to this heading")

```
|COL1 |
|-----|
|three|
```

Copy

##### Result 4[¶](#id224 "Link to this heading")

```
|COL1             |
|-----------------|
|Unexpected input.|
```

Copy

### Known Issues [¶](#id225 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id226 "Link to this heading")

No related EWIs.

## LOCKING FOR ACCESS[¶](#locking-for-access "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

Note

Non-relevant statement.

Warning

**Notice that this statement is****removed from the migration****because it is a non-relevant syntax. It means that it is not required in Snowflake.**

### Description[¶](#id227 "Link to this heading")

The functionality of locking a row in Teradata is related to the access and the privileges. Revire the following [documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/Statement-Syntax/LOCKING-Request-Modifier/Usage-Notes/Using-LOCKING-ROW) to know more.

### Sample Source Patterns[¶](#id228 "Link to this heading")

#### Locking row[¶](#locking-row "Link to this heading")

Notice that in this example the `LOCKING ROW FOR ACCESS` has been deleted. This is because Snowflake handles accesses with roles and privileges. The statement is not required.

##### Teradata[¶](#id229 "Link to this heading")

```
 REPLACE VIEW SCHEMA2.VIEW1
AS 
LOCKING ROW FOR ACCESS
SELECT * FROM SCHEMA1.TABLE1;
```

Copy

##### Snowflake[¶](#id230 "Link to this heading")

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "SCHEMA1.TABLE1" **
CREATE OR REPLACE VIEW SCHEMA2.VIEW1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT
* FROM
SCHEMA1.TABLE1;
```

Copy

### Known Issues [¶](#id231 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id232 "Link to this heading")

1. [SSC-FDM-0001](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0001): Views selecting all columns from a single table are not required in Snowflake.
2. [SSC-FDM-0007](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0007): Element with missing dependencies.

## LOOP[¶](#loop "Link to this heading")

Translation reference to convert Teradata LOOP statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id233 "Link to this heading")

Teradata’s `LOOP` statement is translated to Snowflake Scripting `LOOP` syntax.

For more information on Teradata Loop, check [here](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/SQL-Control-Statements/LOOP).

```
 [label_name:] LOOP
    { sql_statement }
END LOOP [label_name];
```

Copy

### Sample Source Patterns [¶](#id234 "Link to this heading")

#### Teradata [¶](#id235 "Link to this heading")

##### Loop[¶](#id236 "Link to this heading")

```
 CREATE PROCEDURE loopProcedure(OUT resultCounter INTEGER)
BEGIN
    DECLARE counter INTEGER DEFAULT 0;
   
    customeLabel: LOOP 
    	SET counter = counter + 1;
	IF counter = 10 THEN
	    LEAVE customeLabel;
	END IF;
    END LOOP customeLabel;
   
    SET resultCounter = counter;
END;

CALL loopProcedure(:?);
```

Copy

##### Result[¶](#id237 "Link to this heading")

```
 |resultCounter|
|-------------|
|10           |
```

Copy

##### Snowflake Scripting [¶](#id238 "Link to this heading")

##### Loop[¶](#id239 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE loopProcedure (RESULTCOUNTER OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		counter INTEGER DEFAULT 0;
	BEGIN
		 
		LOOP
			counter := counter + 1;
			IF (:counter = 10) THEN
				BREAK CUSTOMELABEL;
			END IF;
		END LOOP CUSTOMELABEL;
		resultCounter := counter;
	END;
$$;

CALL loopProcedure(:?);
```

Copy

##### Result[¶](#id240 "Link to this heading")

```
 |LOOPPROCEDURE|
|-------------|
|10           |
```

Copy

### Known Issues [¶](#id241 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id242 "Link to this heading")

No related EWIs.

## OUTPUT PARAMETERS[¶](#output-parameters "Link to this heading")

This article is about the current transformation of the output parameters and how their functionality is being emulated.

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id243 "Link to this heading")

An **output parameter** is a parameter whose value is passed out of the stored procedure, back to the calling statement. Snowflake has direct support for output parameters.

### Sample Source Patterns[¶](#id244 "Link to this heading")

#### Single out parameter[¶](#single-out-parameter "Link to this heading")

##### Teradata[¶](#id245 "Link to this heading")

```
CREATE PROCEDURE demo.proc_with_single_output_parameters(OUT param1 NUMBER)
BEGIN
 SET param1 = 100;
END;

REPLACE PROCEDURE demo.proc_calling_proc_with_single_output_parameters ()
BEGIN
  DECLARE mytestvar NUMBER;
  CALL demo.proc_with_single_output_parameters(mytestvar);
  INSERT INTO demo.TABLE20 VALUES(mytestvar,432);
END;
```

Copy

##### Snowflake[¶](#id246 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE demo.proc_with_single_output_parameters (PARAM1 OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
 BEGIN
  param1 := 100;
 END;
$$;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "demo.TABLE20" **
CREATE OR REPLACE PROCEDURE demo.proc_calling_proc_with_single_output_parameters ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  mytestvar NUMBER(38, 18);
 BEGIN
   
  CALL demo.proc_with_single_output_parameters(:mytestvar);
  INSERT INTO demo.TABLE20
  VALUES (:mytestvar,432);
 END;
$$;
```

Copy

#### Multiple out parameter[¶](#multiple-out-parameter "Link to this heading")

##### Teradata[¶](#id247 "Link to this heading")

```
 CREATE PROCEDURE demo.proc_with_multiple_output_parameters(OUT param1 NUMBER, INOUT param2 NUMBER)
BEGIN
  SET param1 = param2;
  SET param2 = 32;
END;

CREATE PROCEDURE demo.proc_calling_proc_with_multiple_output_parameters ()
BEGIN
    DECLARE var1  NUMBER;
    DECLARE var2  NUMBER;
    SET var2 = 34;
    CALL demo.proc_with_multiple_output_parameters(var1, var2);
    INSERT INTO demo.TABLE20 VALUES(var1,var2);
END;
```

Copy

##### Snowflake[¶](#id248 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE demo.proc_with_multiple_output_parameters (PARAM1 OUT NUMBER(38, 18), PARAM2 OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    param1 := param2;
    param2 := 32;
  END;
$$;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "demo.TABLE20" **
CREATE OR REPLACE PROCEDURE demo.proc_calling_proc_with_multiple_output_parameters ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    var1 NUMBER(38, 18);
    var2 NUMBER(38, 18);
  BEGIN
     
     
    var2 := 34;
    CALL demo.proc_with_multiple_output_parameters(:var1, :var2);
    INSERT INTO demo.TABLE20
    VALUES (:var1, :var2);
  END;
$$;
```

Copy

### Related EWIs [¶](#id249 "Link to this heading")

No related EWIs.

## PREPARE[¶](#prepare "Link to this heading")

Translation specification to convert Teradata PREPARE statement to Snowflake Scripting. This section review the PREPARE pattern related to a cursor logic.

### Description [¶](#id250 "Link to this heading")

> Prepares the dynamic DECLARE CURSOR statement to allow the creation of different result sets. Allows dynamic parameter markers.

For more information, please review the following [documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Stored-Procedures-and-Embedded-SQL/SQL-Cursor-Control-and-DML-Statements/PREPARE).

**Tedarata syntax**:

```
 PREPARE statement_name FROM { 'statement_string' | statement_string_variable } ;
```

Copy

Where:

* **statement\_name** is the same identifier as `statement_name` in a **DECLARE CURSOR** statement.
* **statement\_string** is the SQL text that is to be executed dynamically.
* **statement\_string\_variable** is the name of an SQL local variable, or an SQL parameter or string variable, that contains the SQL text string to be executed dynamically.

Note

**Important information**

**For this transformation, the cursors are renamed since they cannot be dynamically updated.**

### Sample Source Patterns [¶](#id251 "Link to this heading")

#### Data setting for examples[¶](#data-setting-for-examples "Link to this heading")

For this example, please use the following complementary queries in the case that you want to run each case.

##### Teradata[¶](#id252 "Link to this heading")

```
 CREATE TABLE MyTemporaryTable(
    Col1  INTEGER
);

INSERT INTO MyTemporaryTable(col1) VALUES (1);
SELECT * FROM databaseTest.MyTemporaryTable;


CREATE TABLE MyStatusTable (
    Col1  VARCHAR(2)
);
SELECT * FROM MyStatusTable;
```

Copy

##### Snowflake[¶](#id253 "Link to this heading")

```
 CREATE TABLE MyTemporaryTable (
    Col1 INTEGER
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

INSERT INTO MyTemporaryTable (col1) VALUES (1);

SELECT * FROM MyTemporaryTable;

    CREATE TABLE MyStatusTable (
    Col1 VARCHAR(2)
   )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

SELECT * FROM MyStatusTable;
```

Copy

#### Simple scenario[¶](#simple-scenario "Link to this heading")

This example reviews the functionality for the cases where a single cursor is being used one single time.

##### Teradata [¶](#id254 "Link to this heading")

##### Query[¶](#id255 "Link to this heading")

```
 REPLACE PROCEDURE simple_scenario()
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT * FROM MyTemporaryTable';
    DECLARE procedure_result INTEGER DEFAULT 0;

    -- Actual Cursor usage
    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO procedure_result;
    INSERT INTO databaseTest.MyStatusTable(Col1) VALUES (procedure_result);
    CLOSE C1;
END;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#output "Link to this heading")

| Col1 |
| --- |
| 1 |

##### Snowflake Scripting [¶](#id256 "Link to this heading")

Note

Usages for cursors must be renamed and declared again.

##### Query[¶](#id257 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE simple_scenario ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   * FROM
   MyTemporaryTable';
    procedure_result INTEGER DEFAULT 0;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN
     
    -- Actual Cursor usage
     
    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      procedure_result;
    INSERT INTO databaseTest.MyStatusTable (Col1)
    VALUES (procedure_result);
    CLOSE CURSOR_S1_INSTANCE_V0;
  END;
$$;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id258 "Link to this heading")

| Col1 |
| --- |
| 1 |

#### Simple scenario with RETURN ONLY[¶](#simple-scenario-with-return-only "Link to this heading")

##### Teradata [¶](#id259 "Link to this heading")

##### Query[¶](#id260 "Link to this heading")

```
 REPLACE PROCEDURE simple_scenario()
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT * FROM MyTemporaryTable';
    DECLARE procedure_result VARCHAR(100);
    DECLARE C1 CURSOR WITH RETURN ONLY FOR S1;

    SET procedure_result = '';
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
END;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id261 "Link to this heading")

| Col1 |
| --- |
| 1 |

##### Snowflake Scripting [¶](#id262 "Link to this heading")

Note

Usages for cursors must be renamed and declared again.

##### Query[¶](#id263 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE simple_scenario ()
RETURNS TABLE (
)
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   * FROM
   MyTemporaryTable';
    procedure_result VARCHAR(100);
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN
     
     
    procedure_result := '';
    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    RETURN TABLE(resultset_from_cursor(CURSOR_S1_INSTANCE_V0));
  END;
$$;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id264 "Link to this heading")

| Col1 |
| --- |
| 1 |

#### Reused cursor case[¶](#reused-cursor-case "Link to this heading")

##### Teradata [¶](#id265 "Link to this heading")

##### Query[¶](#id266 "Link to this heading")

```
 CREATE PROCEDURE fetch_simple_reused_cursor(OUT procedure_result INTEGER)
BEGIN
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 1';

    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO procedure_result;
    CLOSE C1;

    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO procedure_result;
    CLOSE C1;
END;
```

Copy

##### Output[¶](#id267 "Link to this heading")

```
No returning information.
```

Copy

##### Snowflake Scripting [¶](#id268 "Link to this heading")

Note

Usages for cursors must be renamed and declared again.

##### Query[¶](#id269 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE fetch_simple_reused_cursor (
--                                                        OUT
                                                            PROCEDURE_RESULT INTEGER)
RETURNS VARIANT
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/24/2024" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 1';
        S1 RESULTSET;
        prepareQuery_aux_sql VARCHAR;
    BEGIN
         
        prepareQuery_aux_sql := SQL_string_sel;
        S1 := (
            EXECUTE IMMEDIATE prepareQuery_aux_sql
        );
        LET CURSOR_S1_INSTANCE_V0 CURSOR
        FOR
            S1;
        OPEN CURSOR_S1_INSTANCE_V0;
            FETCH
            CURSOR_S1_INSTANCE_V0
        INTO procedure_result;
            CLOSE CURSOR_S1_INSTANCE_V0;
        prepareQuery_aux_sql := SQL_string_sel;
        S1 := (
            EXECUTE IMMEDIATE prepareQuery_aux_sql
        );
        LET CURSOR_S1_INSTANCE_V1 CURSOR
        FOR
            S1;
        OPEN CURSOR_S1_INSTANCE_V1;
            FETCH
            CURSOR_S1_INSTANCE_V1
        INTO procedure_result;
            CLOSE CURSOR_S1_INSTANCE_V1;
        RETURN procedure_result;
    END;
$$;
```

Copy

##### Output[¶](#id270 "Link to this heading")

```
No returning information.
```

Copy

#### Modified query before usage[¶](#modified-query-before-usage "Link to this heading")

##### Teradata [¶](#id271 "Link to this heading")

##### Query[¶](#id272 "Link to this heading")

```
 REPLACE PROCEDURE fetch_modified_query_cursor()
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 1';
    DECLARE procedure_result INTEGER DEFAULT 0;
    -- Actual Cursor usages
    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;

    -- This modification does not take effect since S1 is already staged for the Cursor
    SET SQL_string_sel = 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 0';
    OPEN C1;
    FETCH C1 INTO procedure_result;
    INSERT INTO databaseTest.MyStatusTable(Col1) VALUES (procedure_result);
    CLOSE C1;
END;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id273 "Link to this heading")

| Col1 |
| --- |
| 1 |

##### Snowflake Scripting [¶](#id274 "Link to this heading")

Note

Usages for cursors must be renamed and declared again.

##### Query[¶](#id275 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE fetch_modified_query_cursor ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 1';
    procedure_result INTEGER DEFAULT 0;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN
     
    -- Actual Cursor usages
     
    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    -- This modification does not take effect since S1 is already staged for the Cursor
    SQL_string_sel := 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 0';
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      procedure_result;
    INSERT INTO databaseTest.MyStatusTable (Col1)
    VALUES (procedure_result);
    CLOSE CURSOR_S1_INSTANCE_V0;
  END;
$$;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id276 "Link to this heading")

| Col1 |
| --- |
| 1 |

#### Simple cursor combined with no PREPARE pattern[¶](#simple-cursor-combined-with-no-prepare-pattern "Link to this heading")

##### Teradata [¶](#id277 "Link to this heading")

##### Query[¶](#id278 "Link to this heading")

```
 REPLACE PROCEDURE fetch_cursor_ignored_query_cursor()
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT * FROM MyTemporaryTable WHERE col1 = 1';
    DECLARE intermediate_result INTEGER;
    DECLARE procedure_result INTEGER DEFAULT 0;
    DECLARE C2 CURSOR FOR SELECT col1 FROM MyTemporaryTable WHERE col1 = 1;

    -- Actual Cursor usage
    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO intermediate_result;
    CLOSE C1;
    SET procedure_result = intermediate_result;
    INSERT INTO databaseTest.MyStatusTable(Col1) VALUES (procedure_result);

    OPEN C2;
    FETCH C2 INTO intermediate_result;
    CLOSE C2;
    SET procedure_result = procedure_result + intermediate_result;
END;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id279 "Link to this heading")

| Col1 |
| --- |
| 1 |

##### Snowflake Scripting [¶](#id280 "Link to this heading")

Note

Usages for cursors must be renamed and declared again.

##### Query[¶](#id281 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE fetch_cursor_ignored_query_cursor ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   * FROM
   MyTemporaryTable
WHERE col1 = 1';
    intermediate_result INTEGER;
    procedure_result INTEGER DEFAULT 0;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN
     
    -- Actual Cursor usage
    LET C2 CURSOR
    FOR
      SELECT
        col1
      FROM
        MyTemporaryTable
      WHERE
        col1 = 1;
    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      intermediate_result;
    CLOSE CURSOR_S1_INSTANCE_V0;
    procedure_result := intermediate_result;
    INSERT INTO databaseTest.MyStatusTable (Col1)
    VALUES (procedure_result);
    OPEN C2;
    FETCH
      C2
    INTO
      intermediate_result;
    CLOSE C2;
    procedure_result := procedure_result + intermediate_result;
  END;
$$;

CALL databaseTest.simple_scenario();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id282 "Link to this heading")

| Col1 |
| --- |
| 1 |

#### Prepare combined with nested cursors[¶](#prepare-combined-with-nested-cursors "Link to this heading")

##### Teradata [¶](#id283 "Link to this heading")

##### Query[¶](#id284 "Link to this heading")

```
 REPLACE PROCEDURE fetch_nested_cursor()
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 1';
    DECLARE intermediate_result INTEGER;
    DECLARE C2 CURSOR FOR SELECT col1 FROM MyTemporaryTable WHERE col1 = 1;

    -- Actual Cursor usage
    DECLARE C1 CURSOR FOR S1;
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    OPEN C2;
    FETCH C2 INTO intermediate_result;

    CLOSE C2;
    FETCH C1 INTO intermediate_result;
    CLOSE C1;
END;
```

Copy

##### Output[¶](#id285 "Link to this heading")

```
No returning information.
```

Copy

##### Snowflake Scripting [¶](#id286 "Link to this heading")

Note

Usages for cursors must be renamed and declared again.

##### Query[¶](#id287 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE fetch_nested_cursor ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ ""origin"": ""sf_sc"", ""name"": ""snowconvert"", ""version"": {  ""major"": 0,  ""minor"": 0,  ""patch"": ""0"" }, ""attributes"": {  ""component"": ""none"",  ""convertedOn"": ""01/01/0001"" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 1';
    intermediate_result INTEGER;
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
  BEGIN
     
     
    -- Actual Cursor usage
    LET C2 CURSOR
    FOR
      SELECT
        col1
      FROM
        MyTemporaryTable
      WHERE
        col1 = 1;
    prepareQuery_aux_sql := SQL_string_sel;
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    OPEN C2;
    FETCH
      C2
    INTO
      intermediate_result;
    CLOSE C2;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      intermediate_result;
    CLOSE CURSOR_S1_INSTANCE_V0;
  END;
$$;
```

Copy

##### Output[¶](#id288 "Link to this heading")

```
No returning information.
```

Copy

#### Variable markers without variable reordering[¶](#variable-markers-without-variable-reordering "Link to this heading")

Warning

**This case is not supported yet.**

##### Teradata [¶](#id289 "Link to this heading")

##### Query[¶](#id290 "Link to this heading")

```
 CREATE PROCEDURE PREPARE_ST_TEST()
BEGIN
    DECLARE ctry_list VARCHAR(100);
    DECLARE SQL_string_sel VARCHAR(255);
    DECLARE col_value NUMBER;

    DECLARE C1 CURSOR FOR S1;

    SET ctry_list = '';
    SET col_value = 1;
    SET SQL_string_sel = 'SELECT * FROM databaseTest.MyTemporaryTable where Col1 = ?';
    PREPARE S1 FROM SQL_string_sel;
    OPEN C1 USING col_value;
    FETCH C1 INTO ctry_list;
    IF (ctry_list <> '') THEN
        INSERT INTO databaseTest.MyStatusTable(col1) VALUES ('ok');
    END IF;
    CLOSE C1;
END;

CALL PREPARE_ST_TEST();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id291 "Link to this heading")

| Col1 |
| --- |
| ok |

##### Snowflake Scripting [¶](#id292 "Link to this heading")

Note

Usages for cursors must be renamed and declared again.

##### Query[¶](#id293 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE PREPARE_ST_TEST_MARKERS ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE 
        p1 RESULTSET;
        p1_sql VARCHAR DEFAULT '';
        
    BEGIN
        LET ctry_list VARCHAR(100);
        LET SQL_string_sel VARCHAR(255);
        LET col_value NUMBER(38, 18);
        LET S1 RESULTSET;
        
        ctry_list := '';
        
        col_value := 1;
        
        SQL_string_sel := 'SELECT * FROM MyTemporaryTable WHERE Col1 = ?';
        
        p1_sql := SQL_string_sel;
        S1 := (
            EXECUTE IMMEDIATE p1_sql USING (col_value)
        );
        LET C1 CURSOR FOR S1;
        
        OPEN C1;
            FETCH C1 INTO ctry_list;
        IF (RTRIM(ctry_list) <> '') THEN
            INSERT INTO MyStatusTable (col1)
            VALUES ('ok');
        END IF;
            CLOSE C1;
    END;
$$;
```

Copy

##### Output[¶](#id294 "Link to this heading")

| Col1 |
| --- |
| ok |

#### Variable markers with variable reordering[¶](#variable-markers-with-variable-reordering "Link to this heading")

Warning

**This case is not supported yet.**

Note

When there are variables setting the value into different ones between the `PREPARE` statement and `OPEN` cursor in Teradata, It is necessary to move this variable before the `EXECUTE IMMEDIATE` in Snowflake. So, the dynamic variable information is updated at the moment of running the dynamic query.

##### Teradata [¶](#id295 "Link to this heading")

##### Query[¶](#id296 "Link to this heading")

```
 CREATE PROCEDURE PREPARE_ST_TEST()
BEGIN
    DECLARE ctry_list VARCHAR(100);
    DECLARE SQL_string_sel VARCHAR(255);
    DECLARE col_name NUMBER;

    DECLARE C1 CURSOR FOR S1;

    SET ctry_list = '';
    SET col_name = 1;
    SET SQL_string_sel = 'SELECT * FROM databaseTest.MyTemporaryTable where Col1 = ?';
    PREPARE S1 FROM SQL_string_sel;
    SET col_name = 2; // change value before open cursor
    OPEN C1 USING col_name;
    FETCH C1 INTO ctry_list;
    IF (ctry_list <> '') THEN
        INSERT INTO databaseTest.MyStatusTable(col1) VALUES ('ok');
    END IF;
    CLOSE C1;
END;

CALL PREPARE_ST_TEST();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id297 "Link to this heading")

```
"MyStatusTable" should be empty.
```

Copy

##### Snowflake Scripting [¶](#id298 "Link to this heading")

Note

Usages for cursors must be renamed and declared again.

##### Query[¶](#id299 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE PREPARE_ST_TEST_MARKERS ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE 
        p1 RESULTSET;
        p1_sql VARCHAR DEFAULT '';
        
    BEGIN
        LET ctry_list VARCHAR(100);
        LET SQL_string_sel VARCHAR(255);
        LET col_value NUMBER(38, 18);
        LET S1 RESULTSET;
        
        ctry_list := '';
        
        col_value := 1;
        
        SQL_string_sel := 'SELECT * FROM MyTemporaryTable WHERE Col1 = ?';
        
        p1_sql := SQL_string_sel;

        col_value:= 2; // Move variable setting before the EXECUTE IMMEDIATE
        
        S1 := (
            EXECUTE IMMEDIATE p1_sql USING (col_value)
        );
                
        LET C1 CURSOR FOR S1;
        
        OPEN C1;
            FETCH C1 INTO ctry_list;
        IF (RTRIM(ctry_list) <> '') THEN
            INSERT INTO MyStatusTable (col1)
            VALUES ('ok');
        END IF;
            CLOSE C1;
    END;
$$;

CALL PREPARE_ST_TEST();
SELECT * FROM MyStatusTable;
```

Copy

##### Output[¶](#id300 "Link to this heading")

```
"MyStatusTable" should be empty.
```

Copy

#### Anonymous blocks - Declaration outside the block[¶](#anonymous-blocks-declaration-outside-the-block "Link to this heading")

Warning

**This case is not supported yet.**

##### Teradata [¶](#id301 "Link to this heading")

##### Query[¶](#id302 "Link to this heading")

```
 REPLACE PROCEDURE anonymous_blocks_case(OUT procedure_result INTEGER)
BEGIN
    --Variables for the example's procedure_results
    DECLARE SQL_string_sel VARCHAR(200) DEFAULT 'SELECT col1 FROM MyTemporaryTable WHERE col1 = 1';

    -- Actual Cursor usage
    DECLARE C1 CURSOR FOR S1;
    DECLARE C2 CURSOR FOR S2;

    PREPARE S1 FROM SQL_string_sel;
    OPEN C1;
    FETCH C1 INTO procedure_result;
    CLOSE C1;

    BEGIN
        PREPARE S2 FROM SQL_string_sel;
        OPEN C2;
        FETCH C2 INTO procedure_result;
        CLOSE C2;
    END;

    OPEN C1;
    CLOSE C1;
END;
```

Copy

##### Output[¶](#id303 "Link to this heading")

```
No returning information.
```

Copy

##### Query[¶](#id304 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE anonymous_blocks_case (
--                                                   OUT
                                                       PROCEDURE_RESULT INTEGER)
RETURNS VARIANT
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "none",  "convertedOn": "01/01/0001" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --Variables for the example's procedure_results
    SQL_string_sel VARCHAR(200) DEFAULT 'SELECT
   col1 FROM
   MyTemporaryTable
WHERE col1 = 1';
    S1 RESULTSET;
    prepareQuery_aux_sql VARCHAR;
    S2 RESULTSET;
  BEGIN
    -- Actual Cursor usage
     
    prepareQuery_aux_sql := SQL_string_sel
    S1 := (
      EXECUTE IMMEDIATE prepareQuery_aux_sql
    );
    LET CURSOR_S1_INSTANCE_V0 CURSOR
    FOR
      S1;
    OPEN CURSOR_S1_INSTANCE_V0;
    FETCH
      CURSOR_S1_INSTANCE_V0
    INTO
      procedure_result;
    CLOSE CURSOR_S1_INSTANCE_V0;
 
    BEGIN
      prepareQuery_aux_sql := SQL_string_sel
      S2 := (
        EXECUTE IMMEDIATE prepareQuery_aux_sql
      );
      LET CURSOR_S2_INSTANCE_V# CURSOR
      FOR
        S1;
      OPEN CURSOR_S2_INSTANCE_V#;
      FETCH
        CURSOR_S2_INSTANCE_V#
      INTO
        procedure_result;
      CLOSE CURSOR_S2_INSTANCE_V#;
    END;
    
    OPEN CURSOR_S1_INSTANCE_V0; -- NAME REMAINS AS NEEDED IN LOGIC
    CLOSE CURSOR_S1_INSTANCE_V0;
    RETURN null;
  END;
$$;
```

Copy

##### Output[¶](#id305 "Link to this heading")

```
No returning information.
```

Copy

### Known Issues[¶](#id306 "Link to this heading")

* Review carefully nested cursors and conditionals, if that is the case.

### Related EWIs [¶](#id307 "Link to this heading")

No related EWIs.

## REPEAT[¶](#repeat "Link to this heading")

Translation reference to convert Teradata REPEAT statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id308 "Link to this heading")

Teradata’s `REPEAT` statement is translated to Snowflake Scripting `REPEAT` syntax.

For more information on Teradata Repeat, check [here](https://docs.teradata.com/r/Teradata-Database-SQL-Stored-Procedures-and-Embedded-SQL/June-2017/SQL-Control-Statements/REPEAT).

```
 [label_name:] REPEAT 
    { sql_statement }
    UNTIL conditional_expression
END REPEAT [label_name];
```

Copy

### Sample Source Patterns [¶](#id309 "Link to this heading")

#### Teradata [¶](#id310 "Link to this heading")

##### Repeat[¶](#id311 "Link to this heading")

```
 CREATE PROCEDURE repeatProcedure(OUT resultCounter INTEGER)
BEGIN
    DECLARE counter INTEGER DEFAULT 0;
   
    customeLabel: REPEAT 
    	SET counter = counter + 1;
	UNTIL 10 < counter    
    END REPEAT customeLabel;
   
    SET resultCounter = counter;
END;

CALL repeatProcedure(:?);
```

Copy

##### Result[¶](#id312 "Link to this heading")

```
|resultCounter|
|-------------|
|11           |
```

Copy

##### Snowflake Scripting [¶](#id313 "Link to this heading")

##### Repeat[¶](#id314 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE repeatProcedure (RESULTCOUNTER OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		counter INTEGER DEFAULT 0;
	BEGIN
		 
		REPEAT
			counter := counter + 1;
		UNTIL (10 < :counter)
		END REPEAT CUSTOMELABEL;
		resultCounter := counter;
	END;
$$;

CALL repeatProcedure(:?);
```

Copy

##### Result[¶](#id315 "Link to this heading")

```
|REPEATPROCEDURE|
|---------------|
|1             |
```

Copy

### Known Issues [¶](#id316 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id317 "Link to this heading")

No related EWIs.

## SET[¶](#set "Link to this heading")

Translation reference to convert Teradata SET statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id318 "Link to this heading")

> Assigns a value to a local variable or parameter in a stored procedure.

For more information regarding Teradata SET, check [here](https://docs.teradata.com/r/zzfV8dn~lAaKSORpulwFMg/7wwpafjC_5JfF~I2zpTsQQ).

```
 SET assigment_target = assigment_source ;
```

Copy

### Sample Source Patterns [¶](#id319 "Link to this heading")

#### Teradata [¶](#id320 "Link to this heading")

##### Query[¶](#id321 "Link to this heading")

```
 CREATE PROCEDURE setExample ( OUT PARAM1 INTEGER )
BEGIN
    DECLARE COL_COUNT INTEGER;
    SET COL_COUNT = 3;
    SET PARAM1 = COL_COUNT + 1;
END;
```

Copy

##### Result[¶](#id322 "Link to this heading")

```
|PARAM1 |
|-------|
|4      |
```

Copy

##### Snowflake Scripting[¶](#id323 "Link to this heading")

##### Query[¶](#id324 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE setExample (PARAM1 OUT INTEGER )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        COL_COUNT INTEGER;
    BEGIN
         
        COL_COUNT := 3;
        PARAM1 := COL_COUNT + 1;
    END;
$$;
```

Copy

##### Result[¶](#id325 "Link to this heading")

```
|PARAM1 |
|-------|
|4      |
```

Copy

### Known Issues [¶](#id326 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id327 "Link to this heading")

No related EWIs.

## SYSTEM\_DEFINED[¶](#system-defined "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

Note

Non-relevant statement.

Warning

**Notice that this statement is****removed from the migration****because it is a non-relevant syntax. It means that it is not required in Snowflake.**

### Description[¶](#id328 "Link to this heading")

Property in Teradata that can be after a `CREATE` statement in cases such as `JOIN INDEX`.

### Sample Source Patterns[¶](#id329 "Link to this heading")

Notice that SYSTEM\_DEFINED has been removed from the source code because it is a non-relevant syntax in Snowflake.

#### Teradata[¶](#id330 "Link to this heading")

```
 CREATE SYSTEM_DEFINED JOIN INDEX MY_TESTS.MYPARTS_TJI004 ,FALLBACK ,CHECKSUM = DEFAULT, MAP = TD_MAP1 AS
CURRENT TRANSACTIONTIME 
SELECT
    MY_TESTS.myParts.ROWID,
    MY_TESTS.myParts.part_id,
    MY_TESTS.part_duration
FROM MY_TESTS.myParts
UNIQUE PRIMARY INDEX (part_id);
```

Copy

##### Snowflake[¶](#id331 "Link to this heading")

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "MY_TESTS.myParts" **
CREATE OR REPLACE DYNAMIC TABLE MY_TESTS.MYPARTS_TJI004
--** SSC-FDM-0031 - DYNAMIC TABLE REQUIRED PARAMETERS SET BY DEFAULT **
TARGET_LAG='1 day'
WAREHOUSE=UPDATE_DUMMY_WAREHOUSE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/01/2024" }}'
AS
--    --** SSC-FDM-TD0025 - TEMPORAL FORMS ARE NOT SUPPORTED IN SNOWFLAKE **
--    CURRENT TRANSACTIONTIME
                            SELECT
        MY_TESTS.myParts.ROWID,
        MY_TESTS.myParts.part_id,
        MY_TESTS.part_duration
    FROM
        MY_TESTS.myParts;
```

Copy

### Known Issues [¶](#id332 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id333 "Link to this heading")

1. [SSC-FDM-0007](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0007): Element with missing dependencies.
2. [SSC-FDM-TD0025](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0025): Teradata Database Temporal Table is not supported in Snowflake.
3. [SSC-FDM-0031](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0031): Dynamic Table required parameters set by default

## WHILE[¶](#while "Link to this heading")

Translation reference to convert Teradata WHILE statement to Snowflake Scripting

Note

Some parts in the output code are omitted for clarity reasons.

### Description [¶](#id334 "Link to this heading")

Teradata’s `WHILE` statement is translated to Snowflake Scripting`WHILE` syntax.

For more information on Teradata While, check [here](https://docs.teradata.com/r/Teradata-Database-SQL-Stored-Procedures-and-Embedded-SQL/June-2017/SQL-Control-Statements/WHILE).

```
 [label_name:] WHILE conditional_expression DO
    { sql_statement }
END WHILE [label_name];
```

Copy

### Sample Source Patterns[¶](#id335 "Link to this heading")

#### Teradata[¶](#id336 "Link to this heading")

##### While[¶](#id337 "Link to this heading")

```
 REPLACE PROCEDURE whileProcedure(OUT resultCounter INTEGER)
BEGIN
    DECLARE counter INTEGER DEFAULT 0;
    customeLabel: WHILE counter < 10 DO
        SET counter = counter + 1;
    END WHILE customeLabel;
    SET resultCounter = counter;
END;

CALL whileProcedure(:?);
```

Copy

##### Result[¶](#id338 "Link to this heading")

```
 |resultCounter|
|-------------|
|10           |
```

Copy

##### Snowflake Scripting [¶](#id339 "Link to this heading")

##### While[¶](#id340 "Link to this heading")

```
 CREATE OR REPLACE PROCEDURE whileProcedure (RESULTCOUNTER OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        counter INTEGER DEFAULT 0;
    BEGIN
         
        WHILE (:counter < 10) LOOP
            counter := counter + 1;
        END LOOP CUSTOMELABEL;
        resultCounter := counter;
    END;
$$;

CALL whileProcedure(:?);
```

Copy

##### Result[¶](#id341 "Link to this heading")

```
 |WHILEPROCEDURE|
|--------------|
|10            |
```

Copy

### Known Issues [¶](#id342 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id343 "Link to this heading")

No related EWIs.

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

1. [ABORT and ROLLBACK](#abort-and-rollback)
2. [ACTIVITY\_COUNT](#activity-count)
3. [BEGIN END](#begin-end)
4. [CASE](#case)
5. [CURSOR](#cursor)
6. [DECLARE CONTINUE HANDLER](#declare-continue-handler)
7. [DECLARE CONDITION HANDLER](#declare-condition-handler)
8. [DECLARE](#id139)
9. [DML and DDL Objects](#dml-and-ddl-objects)
10. [EXCEPTION HANDLERS](#exception-handlers)
11. [EXECUTE/EXEC](#execute-exec)
12. [EXECUTE IMMEDIATE](#execute-immediate)
13. [FUNCTION OPTIONS OR DATA ACCESS](#function-options-or-data-access)
14. [GET DIAGNOSTICS EXCEPTION](#get-diagnostics-exception)
15. [IF](#if)
16. [LOCKING FOR ACCESS](#locking-for-access)
17. [LOOP](#loop)
18. [OUTPUT PARAMETERS](#output-parameters)
19. [PREPARE](#prepare)
20. [REPEAT](#repeat)
21. [SET](#set)
22. [SYSTEM\_DEFINED](#system-defined)
23. [WHILE](#while)