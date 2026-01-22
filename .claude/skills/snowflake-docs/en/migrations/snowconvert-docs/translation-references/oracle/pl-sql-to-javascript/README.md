---
auto_generated: true
description: This is a translation reference to convert PL/SQL statements to snowflake
  JavaScript
last_scraped: '2026-01-14T16:53:20.140368+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-javascript/README
title: SnowConvert AI - Oracle - PL/SQL to Javascript | Snowflake Documentation
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
            - [PL/SQL to Snowflake Scripting](../pl-sql-to-snowflake-scripting/README.md)
            - [PL/SQL to Javascript](README.md)

              * [Helpers](helpers.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Oracle](../README.md)PL/SQL to Javascript

# SnowConvert AI - Oracle - PL/SQL to Javascript[¶](#snowconvert-ai-oracle-pl-sql-to-javascript "Link to this heading")

This is a translation reference to convert PL/SQL statements to snowflake JavaScript

## Collections & Records[¶](#collections-records "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

### Records[¶](#records "Link to this heading")

Note

You might also be interested in [Records declaration.](#record-variable-declaration)

#### Oracle[¶](#oracle "Link to this heading")

```
CREATE OR REPLACE PROCEDURE RECORDS_PROC AS 
 TYPE DEPTRECTYP IS RECORD (
    DEPT_ID    NUMBER(4) NOT NULL := 10,
    DEPT_NAME  VARCHAR2(30) NOT NULL := 'ADMINISTRATION',
    MGR_ID     NUMBER(6) := 200,
    LOC_ID     NUMBER(4) := 1700
  );
  
  TYPE NAME_REC IS RECORD (
    FIRST  EMPLOYEES.FIRST_NAME%TYPE,
    LAST   EMPLOYEES.LAST_NAME%TYPE
  );
 
  TYPE CONTACT IS RECORD (
    NAME  NAME_REC,-- NESTED RECORD
    PHONE EMPLOYEES.PHONE_NUMBER%TYPE
  );
 
  DEPT1 DEPTRECTYP;
  DEPT_NAME DEPTRECTYP;
  C1 CONTACT;
BEGIN
  DEPT1.DEPT_NAME := 'PURCHASING';
  C1.NAME.FIRST := 'FALVARADO';
  C1.PHONE := '50687818481';
  SELECT * INTO DEPT1 FROM FTABLE46;
  INSERT INTO TABLA1 VALUES (DEPT1.DEPT_NAME);
  INSERT INTO TABLA1 VALUES (DEPT_NAME.DEPT_NAME);
  EXECUTE IMMEDIATE 'SELECT * FROM FTABLE46' INTO DEPT_NAME;
END;
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

Warning

Transformation for “SELECT INTO Record” is in progress.

```
CREATE OR REPLACE PROCEDURE RECORDS_PROC ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 DECLARE
  !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!
  TYPE DEPTRECTYP IS RECORD (
     DEPT_ID    NUMBER(4) NOT NULL := 10,
     DEPT_NAME  VARCHAR2(30) NOT NULL := 'ADMINISTRATION',
     MGR_ID     NUMBER(6) := 200,
     LOC_ID     NUMBER(4) := 1700
   );
  !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!

   TYPE NAME_REC IS RECORD (
     FIRST  EMPLOYEES.FIRST_NAME%TYPE,
     LAST   EMPLOYEES.LAST_NAME%TYPE
   );
  !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!

   TYPE CONTACT IS RECORD (
     NAME  NAME_REC,-- NESTED RECORD
     PHONE EMPLOYEES.PHONE_NUMBER%TYPE
   );

   DEPT1 OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - DEPTRECTYP DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
   DEPT_NAME OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - DEPTRECTYP DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
   C1 OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - CONTACT DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
 BEGIN
  DEPT1 := OBJECT_INSERT(DEPT1, 'DEPT_NAME', 'PURCHASING', true);
  C1 := OBJECT_INSERT(C1, 'FIRST', 'FALVARADO', true);
  C1 := OBJECT_INSERT(C1, 'PHONE', '50687818481', true);
  SELECT
   OBJECT_CONSTRUCT( *) INTO
   :DEPT1
  FROM
   FTABLE46;
  INSERT INTO TABLA1
  SELECT
   :DEPT1.DEPT_NAME:DEPT_ID,
   :DEPT1.DEPT_NAME:DEPT_NAME,
   :DEPT1.DEPT_NAME:MGR_ID,
   :DEPT1.DEPT_NAME:LOC_ID;
  INSERT INTO TABLA1
  SELECT
   :DEPT_NAME.DEPT_NAME:DEPT_ID,
   :DEPT_NAME.DEPT_NAME:DEPT_NAME,
   :DEPT_NAME.DEPT_NAME:MGR_ID,
   :DEPT_NAME.DEPT_NAME:LOC_ID;
  !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
  EXECUTE IMMEDIATE 'SELECT * FROM
   FTABLE46'
            !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'EXECUTE IMMEDIATE RETURNING CLAUSE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
            INTO DEPT_NAME;
 END;
$$;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

No issues were found.

### Related EWIS[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036): Data type converted to another data type.
2. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056): Create Type Not Supported.
3. [SSC-EWI-0058](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting.
4. [SSC-EWI-0030](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0030): The statement below has usages of dynamic SQL

## Conditional Compilation[¶](#conditional-compilation "Link to this heading")

### Description[¶](#description "Link to this heading")

> Provides conditional compilation based on the truth value of a condition.

For more information regarding Oracle Conditional Compilation IF, check [here](https://www.oracle.com/partners/campaign/plsql-conditional-compilation-133587.pdf).

```
$IF conditional_expression $THEN
     statement
     [ statement ]... 
[ $ELSIF conditional_expression $THEN
     statement
     [ statement ]... ]...
[ $ELSE   
     statement
     [ statement ]... ]
$END;
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### Possible IF variations[¶](#possible-if-variations "Link to this heading")

##### Oracle[¶](#id1 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROCEDURE_DEMO ()
   AS
   BEGIN
      SELECT 2 FROM DUAL;
      $IF $$debug_flag
      $THEN
         SELECT 1 FROM DUAL;
      $END
   END PROCEDURE_DEMO;
```

Copy

##### Snowflake Scripting[¶](#snowflake-scripting "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROCEDURE_DEMO ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      SELECT 2 FROM DUAL;
      !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'DOLLAR IF STATEMENT' NODE ***/!!!
      $IF $$debug_flag
      $THEN
         SELECT 1 FROM DUAL;
      $END
   END;
$$;
```

Copy

### Known issues[¶](#id2 "Link to this heading")

1. Transformation of Conditional Compilation is not currently supported.

### Related EWIs[¶](#id3 "Link to this heading")

* [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Control Statements[¶](#control-statements "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

### IF, ELSIF and ELSE Statement[¶](#if-elsif-and-else-statement "Link to this heading")

#### Oracle[¶](#id4 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1
IS
    sal_raise NUMBER;
BEGIN
  IF jobid = 'PU_CLERK' THEN sal_raise := .09;
  ELSIF jobid = 'SH_CLERK' THEN sal_raise := .08;
  ELSIF jobid = 'ST_CLERK' THEN sal_raise := .07;
  ELSE sal_raise := 0;
  END IF;
END;
```

Copy

#### Snowflake[¶](#id5 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  let SAL_RAISE;
  if (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT jobid MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
    JOBID == `PU_CLERK`) {
    SAL_RAISE = 0.09;
  } else if (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT jobid MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
    JOBID == `SH_CLERK`) {
    SAL_RAISE = 0.08;
  } else if (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT jobid MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
    JOBID == `ST_CLERK`) {
    SAL_RAISE = 0.07;
  } else {
    SAL_RAISE = 0;
  }
$$;
```

Copy

### Loop[¶](#loop "Link to this heading")

#### Oracle[¶](#id6 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 
IS
BEGIN
  LOOP
    i := i + 1;
    j := 0;
    LOOP
      j := j + 1;
      s := s + i * j; -- Sum several products
    END LOOP inner_loop;
  END LOOP outer_loop;
END;
```

Copy

#### Snowflake[¶](#id7 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  while ( true ) {
    I =
        !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT i MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
        I + 1;
    J = 0;
    while ( true ) {
      J =
          !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT j MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
          J + 1;
      S =
          !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT s MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
          S +
            !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT i MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
            I *
            !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT j MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
            J;
    }
  }
$$;
```

Copy

### While Statement[¶](#while-statement "Link to this heading")

#### Oracle[¶](#id8 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 
IS
I NUMBER := 1;
J NUMBER := 10;
BEGIN
  WHILE I <> J LOOP
    I := I+1;
  END LOOP;
END;
```

Copy

#### Snowflake[¶](#id9 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  let I = 1;
  let J = 10;
  while ( I != J ) {
    I = I + 1;
  }
$$;
```

Copy

### Related EWIs[¶](#id10 "Link to this heading")

1. [SSC-EWI-0053](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0053): Object may not work.

## Declarations[¶](#declarations "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

### Variable declaration and assignment[¶](#variable-declaration-and-assignment "Link to this heading")

#### Oracle[¶](#id11 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_VARIABLES 
IS
  localVar1 NUMBER;
  localVar2 VARCHAR(100);
  localVar3 VARCHAR2 := 'local variable 3';
  localVar4 VARCHAR2 DEFAULT 'local variable 4';
  localVar5 VARCHAR2 NOT NULL := 'local variable 5';
  localVar6 VARCHAR2 NOT NULL DEFAULT 'local variable 6';
  localVar7 NUMBER := NULL;
  localVar8 NUMBER := '';
BEGIN
    localVar1 := 123;
END;
```

Copy

#### Snowflake[¶](#id12 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_VARIABLES ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  let LOCALVAR1;
  let LOCALVAR2;
  let LOCALVAR3 = `local variable 3`;
  let LOCALVAR4 = `local variable 4`;
  let LOCALVAR5 = `local variable 5`;
  let LOCALVAR6 = `local variable 6`;
  let LOCALVAR7 = undefined;
  let LOCALVAR8 = undefined;
  LOCALVAR1 = 123;
$$;
```

Copy

### Record variable declaration[¶](#record-variable-declaration "Link to this heading")

Note

You might also be interested in [Records transformation section.](#collections-records)

#### Oracle[¶](#id13 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_RECORDS
IS
    TYPE DEPTRECTYP IS RECORD (
    DEPT_ID    NUMBER(4) NOT NULL := 10,
    DEPT_NAME  VARCHAR2(30) NOT NULL := 'ADMINISTRATION',
    MGR_ID     NUMBER(6) := 200,
    LOC_ID     NUMBER(4) := 1700
  );

  TYPE NAME_REC IS RECORD (
    FIRST  EMPLOYEES.FIRST_NAME%TYPE,
    LAST   EMPLOYEES.LAST_NAME%TYPE
  );
 
  TYPE CONTACT IS RECORD (
    NAME  NAME_REC,-- NESTED RECORD
    PHONE EMPLOYEES.PHONE_NUMBER%TYPE
  );
BEGIN
    null;
END;
```

Copy

#### Snowflake[¶](#id14 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_RECORDS ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  class DEPTRECTYP {
    DEPT_ID = 10
    DEPT_NAME = `ADMINISTRATION`
    MGR_ID = 200
    LOC_ID = 1700
    constructor() {
      [...arguments].map((element,Index) => this[(Object.keys(this))[Index]] = element)
    }
  }
  class NAME_REC {
    FIRST
    LAST
    constructor() {
      [...arguments].map((element,Index) => this[(Object.keys(this))[Index]] = element)
    }
  }
  class CONTACT {
    NAME = new NAME_REC()
    PHONE
    constructor() {
      [...arguments].map((element,Index) => this[(Object.keys(this))[Index]] = element)
    }
  }
  null;
$$;
```

Copy

### Rowtype Record variable declaration[¶](#rowtype-record-variable-declaration "Link to this heading")

#### Oracle[¶](#id15 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE ROWTYPE_PROC AS
  varname number := 1;
  CURSOR BOOK_CURSOR IS SELECT * FROM BOOK where 1 = varname;

  BOOK_REC BOOK%ROWTYPE;
  BOOK_CUR_REC BOOK_CURSOR%ROWTYPE;
BEGIN
  BOOK_REC.ID     := 10;
  BOOK_REC.TITLE  := 'A STUDY IN SCARLET';
  BOOK_REC.AUTHOR := 'SIR ARTHUR CONAN DOYLE';
 
  INSERT INTO BOOK VALUES(BOOK_REC.ID, BOOK_REC.TITLE, BOOK_REC.AUTHOR);
  OPEN BOOK_CURSOR;
  FETCH BOOK_CURSOR INTO BOOK_CUR_REC;
  CLOSE BOOK_CURSOR;
END;
```

Copy

#### Snowflake[¶](#id16 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE ROWTYPE_PROC ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  let VARNAME = 1;
  let BOOK_CURSOR = new CURSOR(`SELECT * FROM
      BOOK
   where 1 = ?`,() => [VARNAME]);
  let BOOK_REC = ROWTYPE(`BOOK`);
  let BOOK_CUR_REC = BOOK_CURSOR.ROWTYPE();
  BOOK_REC.ID = 10;
  BOOK_REC.TITLE = `A STUDY IN SCARLET`;
  BOOK_REC.AUTHOR = `SIR ARTHUR CONAN DOYLE`;
  EXEC(`INSERT INTO BOOK
  VALUES(
  !!!RESOLVE EWI!!! /*** SSC-EWI-0026 - THE  VARIABLE BOOK_REC.ID MAY REQUIRE A CAST TO DATE, TIME OR TIMESTAMP ***/!!!
  ?,
  !!!RESOLVE EWI!!! /*** SSC-EWI-0026 - THE  VARIABLE BOOK_REC.TITLE MAY REQUIRE A CAST TO DATE, TIME OR TIMESTAMP ***/!!!
  ?,
  !!!RESOLVE EWI!!! /*** SSC-EWI-0026 - THE  VARIABLE BOOK_REC.AUTHOR MAY REQUIRE A CAST TO DATE, TIME OR TIMESTAMP ***/!!!
  ?)`,[BOOK_REC.ID,BOOK_REC.TITLE,BOOK_REC.AUTHOR]);
  BOOK_CURSOR.OPEN();
  BOOK_CURSOR.FETCH(BOOK_CUR_REC) && ([BOOK_CUR_REC] = BOOK_CURSOR.INTO());
  BOOK_CURSOR.CLOSE();
$$;
```

Copy

### Constant Declaration[¶](#constant-declaration "Link to this heading")

#### Oracle[¶](#id17 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_CONSTANTS
IS
    MY_VAR1 NUMBER;
    MY_CONST_VAR1 CONSTANT INTEGER(4) := 40;
    MY_CONST_VAR2 CONSTANT INTEGER(4) NOT NULL := MY_CONST_VAR1;
    MY_CONST_VAR3 CONSTANT VARCHAR(20) DEFAULT 'const variable';
    MY_CONST_VAR4 CONSTANT REAL NOT NULL DEFAULT 3.14159;
BEGIN
    MY_VAR1 := MY_CONST_VAR1 + MY_CONST_VAR2 + 1;
END;
```

Copy

#### Snowflake[¶](#id18 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC_CONSTANTS ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    let MY_VAR1;
    const MY_CONST_VAR1 = 40;
    const MY_CONST_VAR2 = MY_CONST_VAR1;
    const MY_CONST_VAR3 = `const variable`;
    const MY_CONST_VAR4 = 3.14159;
    const MY_CONST_VAR1 = 40;
    const MY_CONST_VAR2 = MY_CONST_VAR1;
    MY_VAR1 = MY_CONST_VAR1 + MY_CONST_VAR2 + 1;
$$;
```

Copy

### Cursor declarations and definition[¶](#cursor-declarations-and-definition "Link to this heading")

#### Oracle[¶](#id19 "Link to this heading")

Note

You might also be interested in [Cursor helper](helpers.html#cursor-helper)

```
CREATE OR REPLACE PROCEDURE PROC_CURSORS
IS
    CURSOR C1 RETURN Table1%ROWTYPE;
    CURSOR C2 RETURN UserDefinedRecordType;
    CURSOR C3 RETURN Table1%ROWTYPE IS 
        SELECT * FROM Table1 WHERE ID = 110;
    CURSOR C4 IS 
        SELECT * FROM Table1 WHERE ID = 123;
    CURSOR C5 (cursorParam NUMBER ) RETURN Table1%ROWTYPE IS 
        SELECT * FROM Table1 WHERE ID = cursorParam;
BEGIN
    null;
END;
```

Copy

#### Snowflake[¶](#id20 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC_CURSORS ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    let C1 = new CURSOR();
    let C2 = new CURSOR();
    let C3 = new CURSOR(`SELECT * FROM
           Table1
        WHERE ID = 110`,() => []);
    let C4 = new CURSOR(`SELECT * FROM
           Table1
        WHERE ID = 123`,() => []);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    let C5 = new CURSOR(`SELECT * FROM
           Table1
        WHERE ID = ?`,(CURSORPARAM) => [CURSORPARAM]);
    null;
$$;
```

Copy

### Known Issues[¶](#id21 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id22 "Link to this heading")

No related EWIs.

1. [SSC-EWI-0022](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0022): One or more identifiers in this statement were considered parameters by default.
2. [SSC-EWI-0026](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0026): The variable may requiere a cast to date, time or timestamp.

## Expressions and operators[¶](#expressions-and-operators "Link to this heading")

### Expressions[¶](#expressions "Link to this heading")

#### Concatenation Operator[¶](#concatenation-operator "Link to this heading")

Note

You might also be interested in [Concat helper.](helpers.html#concat-value-helper)

Oracle concatenation is achieved in JavaScript using [Template literal](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals). Also it uses the *Concat Helper* to properly handle concatenations with nulls.

##### Oracle[¶](#id23 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE CONCAT_TEST
IS
NUM1 INTEGER := 123;
NUM2 INTEGER := 321;
VAR1 VARCHAR(10) := 'value';
concat_var VARCHAR(100);
sql_stmt VARCHAR(100);
BEGIN
    concat_var := NUM1 || NUM2 || VAR1 || 'literal';   
    sql_stmt := 'INSERT INTO t1 VALUES (''' || concat_var || ''')';    
    EXECUTE IMMEDIATE sql_stmt;
END;
```

Copy

##### Snowflake[¶](#id24 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE CONCAT_TEST ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    let NUM1 = 123;
    let NUM2 = 321;
    let VAR1 = `value`;
    let CONCAT_VAR;
    let SQL_STMT;
    CONCAT_VAR = `${concatValue(NUM1)}${concatValue(NUM2)}${concatValue(VAR1)}literal`;
    SQL_STMT = `INSERT INTO t1
VALUES ('${concatValue(CONCAT_VAR)}')`;
    EXEC(SQL_STMT);
$$;
```

Copy

#### Logical Operators[¶](#logical-operators "Link to this heading")

##### Oracle[¶](#id25 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE BOOLEAN_PROC (b_name VARCHAR2, b_value  BOOLEAN)
IS
BOOL1 BOOLEAN := FALSE;
x NUMBER := 5;
y NUMBER := NULL;
BEGIN

  IF b_value IS NULL THEN
    null;
  ELSIF b_value = TRUE THEN
    null;
  ELSIF b_value = TRUE AND b_value = BOOL1  OR b_value = BOOL1 THEN
    null;
  ELSIF x > y THEN
    null;
  ELSIF x != y AND x <> y THEN
    null;
  ELSE
    null;
  END IF;
END;
```

Copy

##### Snowflake[¶](#id26 "Link to this heading")

Note

You might also be interested in [IS NULL helper](helpers.html#is-null-helper)[.](helpers.html#is-null-helper)

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE BOOLEAN_PROC (b_name STRING, b_value BOOLEAN)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  
  // SnowConvert AI Helpers Code section is omitted.
  
  let BOOL1 = false;
  let X = 5;
  let Y = undefined;
  if (IS_NULL(B_VALUE)) {
    null;
  } else if (B_VALUE == true) {
    null;
  } else if (B_VALUE == true && B_VALUE == BOOL1 || B_VALUE == BOOL1) {
    null;
  } else if (X > Y) {
    null;
  } else if (X != Y && X != Y) {
    null;
  } else {
    null;
  }
$$;
```

Copy

#### Comparison Operator[¶](#comparison-operator "Link to this heading")

Documentation in progress.

##### IS [NOT] NULL[¶](#is-not-null "Link to this heading")

Note

You might also be interested in [IS NULL helper](helpers.html#is-null-helper).

##### Oracle[¶](#id27 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE NULL_TEST
IS
NUM1 INTEGER := 789;
BEGIN
    IF NUM1 IS NOT NULL THEN
        NULL;
    END IF;
    
    NUM1 := NULL;
    
    IF NUM1 IS NULL THEN
        NULL;
    END IF;
END;
```

Copy

##### Snowflake[¶](#id28 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE NULL_TEST ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$

    // SnowConvert AI Helpers Code section is omitted.

    let NUM1 = 789;
    if (!IS_NULL(NUM1)) {
        null;
    }
    NUM1 = undefined;
    if (IS_NULL(NUM1)) {
        null;
    }
$$;
```

Copy

##### Like Operator[¶](#like-operator "Link to this heading")

Note

You might also be interested in [Like operator helper.](helpers.html#like-operator-helper)

When there is a LIKE operation, the helper function will be called instead.

###### Oracle[¶](#id29 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROCEDURE_WITH_LIKE AS
BEGIN
	IF 'ABC' LIKE '%A%' THEN
		 null;
	END IF;
  IF 'ABC' LIKE 'A%' THEN
     null;
  END IF;
  IF 'ABC' NOT LIKE 'D_%' THEN
     null;
  END IF;
  IF 'ABC' NOT LIKE 'D/%%' ESCAPE '/' THEN
     null;
  END IF;
END;
```

Copy

###### Snowflake[¶](#id30 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROCEDURE_WITH_LIKE ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	if (LIKE(`ABC`,`%A%`)) {
		null;
	}
	if (LIKE(`ABC`,`A%`)) {
		null;
	}
	if (!LIKE(`ABC`,`D_%`)) {
		null;
	}
	if (!LIKE(`ABC`,`D/%%`,`/`)) {
		null;
	}
$$;
```

Copy

##### Between Operator[¶](#between-operator "Link to this heading")

Note

You may also be interested in [Between operator helper.](helpers.html#between-operator-helper)

###### Oracle[¶](#id31 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE BETWEEN_TEST
IS
NUM1 INTEGER := 789;
US INTEGER := 1000;
BEGIN
    IF 800 BETWEEN US AND NUM1 THEN
        NULL;
    END IF;
    IF 'BA' BETWEEN 'B' AND 'CA' THEN
        NULL;
    END IF;
    
    -- Assign null to the variable num1
    NUM1 := NULL;
    
    IF (0 BETWEEN NULL AND NUM1) IS NULL THEN
        NULL;
    END IF;
END;
```

Copy

###### Snowflake[¶](#id32 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE BETWEEN_TEST ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.
    
    let NUM1 = 789;
    let US = 1000;
    if (BetweenFunc(800,US,NUM1)) {
        null;
    }
    if (BetweenFunc(`BA`,`B`,`CA`)) {
        null;
    }

    // Assign null to the variable num1
    NUM1 = undefined;
    if (IS_NULL(BetweenFunc(0,undefined,NUM1))) {
        null;
    }
$$;
```

Copy

##### IN Operator[¶](#in-operator "Link to this heading")

###### Oracle[¶](#id33 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE IN_PROC
IS
letter VARCHAR2(1) := 'm';
BEGIN
  IF letter IN ('a', 'b', 'c') THEN
    null;  
  ELSE
    null;
  END IF;
END;
```

Copy

###### Snowflake[¶](#id34 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE IN_PROC ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.
  
  let LETTER = `m`;
  if ([`a`,`b`,`c`].includes(LETTER)) {
    null;
  } else {
    null;
  }
$$;
```

Copy

#### Boolean Expressions[¶](#boolean-expressions "Link to this heading")

##### Oracle[¶](#id35 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE BOOLEAN_TEST
IS
done BOOLEAN;
BEGIN
  -- These WHILE loops are equivalent  
  done := FALSE;
  WHILE done = FALSE
    LOOP
      done := TRUE;
    END LOOP;    
 
  done := FALSE;
  WHILE NOT (done = TRUE)
    LOOP
      done := TRUE;
    END LOOP; 

  done := FALSE;
  WHILE NOT done
    LOOP
      done := TRUE;
    END LOOP;
END;
```

Copy

##### Snowflake[¶](#id36 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE BOOLEAN_TEST ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.
  
  let DONE;
  // These WHILE loops are equivalent  
  DONE = false;
  while ( DONE == false ) {
    DONE = true;
  }
  DONE = false;
  while ( !(DONE == true) ) {
    DONE = true;
  }
  DONE = false;
  while ( !DONE ) {
    DONE = true;
  }
$$;
```

Copy

#### Function Expressions[¶](#function-expressions "Link to this heading")

For Function Expressions inside procedures, they are being converted to the corresponding function or expression in Snowflake. These function calls are passed to an EXEC with a CALL or a SELECT depending on the converted value.

##### Oracle[¶](#id37 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE FUNCTIONS_TEST(DATEPARAM DATE)
IS
	STRING_VALUE VARCHAR(20) := 'HELLO';
BEGIN
	STRING_VALUE := TO_CHAR(123);
	STRING_VALUE := TO_CHAR(DATEPARAM, 'dd-mm-yyyy', 'NLS_DATE_LANGUAGE = language');
END;
```

Copy

##### Snowflake[¶](#id38 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE FUNCTIONS_TEST (DATEPARAM TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	let STRING_VALUE = `HELLO`;
	STRING_VALUE = (EXEC(`SELECT
   TO_CHAR(123)`))[0];
	STRING_VALUE = (EXEC(`SELECT
   !!!RESOLVE EWI!!! /*** SSC-EWI-OR0013 - NLS PARAMETER 'NLS_DATE_LANGUAGE = language' NOT SUPPORTED ***/!!!
   TO_CHAR(PUBLIC.CAST_DATE_UDF(?), 'dd-mm-yyyy')`,[DATEPARAM]))[0];
$$;
```

Copy

For more information on the function’s transformations check [here](../functions/README).

### Known Issues[¶](#id39 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id40 "Link to this heading")

No related EWIs.

1. [SSC-EWI-OR0013](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0013): NLS parameter is not supported.
2. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior.

## User defined functions[¶](#user-defined-functions "Link to this heading")

### General Description[¶](#general-description "Link to this heading")

Most Oracle UDFs and UDFs inside packages, are being transformed to Snowflake Stored Procedures, to maintain functional equivalence, due to Snowflake UDFs having some limitations executing DML (Data Manipulation Language) statements.

### Translation[¶](#translation "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

#### Create Function[¶](#create-function "Link to this heading")

##### Oracle[¶](#id41 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1(PAR1 VARCHAR)
RETURN VARCHAR
IS
    VAR1 VARCHAR(20);
    VAR2 VARCHAR(20);
BEGIN
    SELECT COL1 INTO VAR1 FROM TABLE1 where col1 = 1;
    VAR2 := PAR1 || VAR1;
    RETURN VAR2 ;
END;
```

Copy

##### Snowflake[¶](#id42 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1 (PAR1 VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/13/2024",  "domain": "test" }}'
AS
$$
    WITH declaration_variables_cte1 AS
    (
        SELECT
            (
            SELECT COL1
            FROM
                TABLE1
            where col1 = 1) AS VAR1,
            NVL(PAR1 :: STRING, '') || NVL(VAR1 :: STRING, '') AS
            VAR2
    )
    SELECT
        VAR2
    FROM
        declaration_variables_cte1
$$;
```

Copy

#### Function inside Package[¶](#function-inside-package "Link to this heading")

##### Oracle[¶](#id43 "Link to this heading")

```
CREATE OR REPLACE PACKAGE BODY pkg1 AS
FUNCTION f1(PAR1 VARCHAR) RETURN VARCHAR IS
    VAR1 VARCHAR(20);
    VAR2 VARCHAR(20);
  BEGIN
    SELECT COL1 INTO VAR1 FROM TABLE1 where col1 = 1;
    VAR2 := PAR1 || VAR1;
    RETURN VAR2 ;
  END f1;
END pkg1;
```

Copy

##### Snowflake[¶](#id44 "Link to this heading")

```
CREATE OR REPLACE FUNCTION pkg1.f1(PAR1 VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/13/2024",  "domain": "test" }}'
AS
$$
  WITH declaration_variables_cte1 AS
  (
    SELECT
      (
      SELECT COL1
      FROM
        TABLE1
      where col1 = 1) AS VAR1,
      NVL(PAR1 :: STRING, '') || NVL(VAR1 :: STRING, '') AS
      VAR2
  )
  SELECT
    VAR2
  FROM
    declaration_variables_cte1
$$;
```

Copy

### Return data type mapping[¶](#return-data-type-mapping "Link to this heading")

| Oracle PL SQL type | Snowflake equivalent |
| --- | --- |
| NUMBER | FLOAT |
| LONG | VARCHAR |
| VARCHAR2 | STRING |
| BLOB | BINARY |
| BFILE | BINARY |

### Call[¶](#call "Link to this heading")

#### Inside queries[¶](#inside-queries "Link to this heading")

Calls of functions that were transformed to procedures inside queries are converted into a an empty Snowflake JavaScript UDF. This Snowflake UDF is generated in the **STUB\_UDF.sql** file inside the **UDF Helpers** directory.

##### Oracle[¶](#id45 "Link to this heading")

```
CREATE VIEW VIEW1 AS SELECT FUN1(COL2) FROM TABLE1;
CREATE VIEW VIEW2 AS SELECT PKG1.F1(COL1) FROM TABLE1;
```

Copy

##### Snowflake[¶](#id46 "Link to this heading")

```
CREATE OR REPLACE VIEW VIEW1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
SELECT FUN1(COL2) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FUN1' NODE ***/!!! FROM
TABLE1;

CREATE OR REPLACE VIEW VIEW2
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
SELECT PKG1.F1(COL1) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PKG1.F1' NODE ***/!!! FROM
TABLE1;
```

Copy

#### Inside other functions or stored procedures[¶](#inside-other-functions-or-stored-procedures "Link to this heading")

The functions that are converted to procedures are called using the [EXEC Snowflake helper](helpers.html#exec-helper).

##### Oracle[¶](#id47 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1(x NUMBER) RETURN NUMBER IS
  VAR1 NUMBER;
  BEGIN
    -- FUN2 is another UDF
    VAR1 := FUN2(pkg1.f1(X, FUN2(10)));
    RETURN VAR1;
  END f1;
```

Copy

##### Snowflake[¶](#id48 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1 (x NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/13/2024",  "domain": "test" }}'
AS
$$
  WITH declaration_variables_cte1 AS
  (
    SELECT
      FUN2(pkg1.f1(X, FUN2(10) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FUN2' NODE ***/!!!) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'pkg1.f1' NODE ***/!!!) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FUN2' NODE ***/!!! AS
      -- FUN2 is another UDF
      VAR1
  )
  SELECT
    VAR1
  FROM
    declaration_variables_cte1
$$;
```

Copy

##### Oracle[¶](#id49 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1(x NUMBER) RETURN NUMBER IS
  VAR1 NUMBER;
  BEGIN
    -- FUN2 is another UDF
    VAR1 := FUN2(X);
    RETURN VAR1;
  END f1;
```

Copy

##### Snowflake[¶](#id50 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1 (x NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/13/2024",  "domain": "test" }}'
AS
$$
  WITH declaration_variables_cte1 AS
  (
    SELECT
      FUN2(X) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FUN2' NODE ***/!!! AS
      -- FUN2 is another UDF
      VAR1
  )
  SELECT
    VAR1
  FROM
    declaration_variables_cte1
$$;
```

Copy

### Different cases and limitations[¶](#different-cases-and-limitations "Link to this heading")

#### Functions with DMLs[¶](#functions-with-dmls "Link to this heading")

These functions cannot be executed in queries in Oracle, so their usage wont be limited when transforming them to Snowflake Procedures.

##### Oracle[¶](#id51 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1(x NUMBER)
RETURN NUMBER IS
VAR1 NUMBER;
BEGIN
    VAR1 := VAR1 + 1;
    INSERT INTO TABLE1(col1, col2) VALUES(X, VAR1);
    UPDATE TABLE2 SET COL1 = VAR1 WHERE ID = X;
    RETURN VAR1;
END FUN1;
```

Copy

##### Snowflake[¶](#id52 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE FUN1 (x FLOAT)
RETURNS FLOAT
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    let VAR1;
    VAR1 = VAR1 + 1;
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`INSERT INTO TABLE1(col1, col2) VALUES(?, ?)`,[X,VAR1]);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`UPDATE TABLE2
       SET COL1 = ?
       WHERE ID = ?`,[VAR1,X]);
    return VAR1;
$$;
```

Copy

#### Functions with only one SELECT INTO[¶](#functions-with-only-one-select-into "Link to this heading")

These functions are transformed to Snowflake SQL functions by removing the INTO part of the select.

##### Oracle[¶](#id53 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1(PAR1 VARCHAR)
RETURN VARCHAR
IS
    VAR1 VARCHAR(20);
BEGIN
    SELECT COL1 INTO VAR1 FROM TABLE1 where col1 = PAR1;
    RETURN VAR1;
END;
```

Copy

##### Snowflake[¶](#id54 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1 (PAR1 VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/13/2024",  "domain": "test" }}'
AS
$$
    WITH declaration_variables_cte1 AS
    (
        SELECT
            (
            SELECT COL1
            FROM
                TABLE1
            where col1 = PAR1) AS VAR1
    )
    SELECT
        VAR1
    FROM
        declaration_variables_cte1
$$;
```

Copy

#### Functions with only logic[¶](#functions-with-only-logic "Link to this heading")

UDFs that do not use any SQL statement are converted into Snowflake JavaScript UDFs.

Note

When SQL built-in functions are included in the logic the user defined function is converted to a Snowflake procedure. Translation for built in functions to a JavaScript equivalent is planned to be delivered in the future.

Examples for built-in functions: UPPER(), TRIM(), ABS().

##### Oracle[¶](#id55 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1(x NUMBER)
RETURN NUMBER IS
VAR1 NUMBER;
BEGIN
    IF x < 5 THEN
        VAR1 := 1;   
    ELSE
        VAR1 := 0;
    END IF;
    RETURN VAR1;
END FUNC01;
```

Copy

##### Snowflake[¶](#id56 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1 (x NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/13/2024",  "domain": "test" }}'
AS
$$
    WITH declaration_variables_cte1 AS
    (
        SELECT
            CASE
                WHEN x < 5
                    THEN 1
                ELSE 0
            END AS VAR1
    )
    SELECT
        VAR1
    FROM
        declaration_variables_cte1
$$;
```

Copy

#### Functions with more than one SQL statement[¶](#functions-with-more-than-one-sql-statement "Link to this heading")

Warning

UDFs transformed into procedures cannot be called from a query.

##### Oracle[¶](#id57 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1(x NUMBER)
RETURN NUMBER IS
VAR1 NUMBER;
BEGIN
    SELECT COL1 INTO VAR1 FROM TABLE1 WHERE ID = X;
    IF VAR1 < 5 THEN
        VAR1 := 1;   
    ELSE
        VAR1 := 0;
    END IF;
    UPDATE TABLE1 SET COL1 = VAR1 WHERE ID = X;
    RETURN VAR1;
END FUN1;
```

Copy

##### Snowflake[¶](#id58 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0068 - USER DEFINED FUNCTION WAS TRANSFORMED TO SNOWFLAKE PROCEDURE ***/!!!
CREATE OR REPLACE PROCEDURE FUN1 (x FLOAT)
RETURNS FLOAT
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/14/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    let VAR1;
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    [VAR1] = EXEC(`SELECT
   COL1
FROM
   TABLE1
WHERE ID = ?`,[X]);
    if (VAR1 < 5) {
        VAR1 = 1;
    } else {
        VAR1 = 0;
    }
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`UPDATE TABLE1
       SET COL1 = ?
       WHERE ID = ?`,[VAR1,X]);
    return VAR1;
$$;
```

Copy

#### Functions with only logic and built-in SQL functions[¶](#functions-with-only-logic-and-built-in-sql-functions "Link to this heading")

Note

This transformation is planned to be delivery in the future, currently all functions are being transformed to stored procedures.

##### Oracle[¶](#id59 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1(x FLOAT)
RETURN NUMBER IS
VAR1 NUMBER;
BEGIN
    IF TRUNC(X) < 5 THEN
        VAR1 := 1;   
    ELSE
        VAR1 := 0;
    END IF;
    RETURN VAR1;
END FUNC01;
```

Copy

###### Snowflake[¶](#id60 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1 (x FLOAT)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/13/2024",  "domain": "test" }}'
AS
$$
    WITH declaration_variables_cte1 AS
    (
        SELECT
            CASE
                WHEN TRUNC(X) < 5
                    THEN 1
                ELSE 0
            END AS VAR1
    )
    SELECT
        VAR1
    FROM
        declaration_variables_cte1
$$;
```

Copy

#### RETURN CASE[¶](#return-case "Link to this heading")

The transformation is the same transformation when the CASE is use to assign a variable.

##### Oracle[¶](#id61 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1 (flag FLOAT)
RETURN NUMBER IS
BEGIN
  return CASE flag
	WHEN 1 THEN 'one'
	WHEN 2 THEN 'two'
	WHEN 3 THEN 'three'
	WHEN 4 THEN 'four'
	ELSE 'unknown' END;
END FUN1;
```

Copy

##### Snowflake[¶](#id62 "Link to this heading")

```
CREATE OR REPLACE FUNCTION FUN1 (flag FLOAT)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/13/2024",  "domain": "test" }}'
AS
$$
	SELECT
		CASE flag
			WHEN 1 THEN 'one'
			WHEN 2 THEN 'two'
			WHEN 3 THEN 'three'
			WHEN 4 THEN 'four'
			ELSE 'unknown' END
$$;
```

Copy

### Known Issues[¶](#id63 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id64 "Link to this heading")

1. [SSC-EWI-0022](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0022): One or more identifiers in this statement were considered parameters by default.
2. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.
3. [SSC-FDM-0029](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0029): User defined function was transformed to a Snowflake procedure.

## Packages[¶](#packages "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

### Package Declaration[¶](#package-declaration "Link to this heading")

This section shows the equivalence between Oracle Package Declaration members and Snowflake statements.

#### Package Translation options[¶](#package-translation-options "Link to this heading")

There are two options to migrate packages, each option will affect directly the naming of the objects inside the package. Check [here](../../../general/getting-started/running-snowconvert/conversion/oracle-conversion-settings) how you can change this mode in the UI.

Let’s suppose that we have the next scenario in Oracle:

* A package named `MY_PACKAGE.`
* A procedure inside the package named `MY_PROCEDURE.`

##### Option 1 (Using new schema)[¶](#option-1-using-new-schema "Link to this heading")

With this option, packages are transformed into new schemas. Package elements like functions and procedures are created inside the new schema. If the package is already inside a schema, the name of the package will be joined with the name of the schema with an underscore.

This is the **default** option for translating packages.

Result:

* An schema will be created with the name `MY_PACKAGE`.
* Qualified name of the procedure will be updated to `MY_PACKAGE.MY_PROCEDURE`.
* It the package is inside an schema then the procedure will be updated to `MY_SCHEMA_MY_PACKAGE.MY_PROCEDURE`.

##### Option 2[¶](#option-2 "Link to this heading")

With this option, the name of the package elements will be joined with the package name with an underscore. New schemas will not be created.

Result:

* Name of the procedure will be updated to `MY_PACKAGE_MY_PROCEDURE`.
* It the package is inside an schema then the procedure will be updated to `MY_SCHEMA.MY_PACKAGE_MY_PROCEDURE`.

#### Create Package[¶](#create-package "Link to this heading")

The CREATE PACKAGE statement will be converted to a CREATE SCHEMA statement. Any member inside the package will be converted outside of the package.

##### Oracle[¶](#id65 "Link to this heading")

```
CREATE OR REPLACE PACKAGE MY_PACKAGE AS
-- Other elements...  
END MY_PACKAGE ;
```

Copy

##### Transformation with option 1 (Using new schema)[¶](#transformation-with-option-1-using-new-schema "Link to this heading")

```
CREATE IF NOT EXISTS SCHEMA MY_PACKAGE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
-- Other elements...
```

Copy

##### Transformation with option 2[¶](#transformation-with-option-2 "Link to this heading")

With this option, the Schema won’t be generated and only the inner elements will be kept but with their names renamed.

```
-- Other elements...
```

Copy

#### Procedure and function declaration[¶](#procedure-and-function-declaration "Link to this heading")

Procedure and function declarations are not necessary for the transformation to Snowflake. Existing procedure or function declarations will be commented out.

##### Oracle[¶](#id66 "Link to this heading")

```
CREATE OR REPLACE PACKAGE MY_PACKAGE AS
  PROCEDURE MY_PROCEDURE(PARAM1 VARCHAR2);
  FUNCTION MY_FUNCTION(PARAM1 VARCHAR2) RETURN NUMBER ;
END MY_PACKAGE;
```

Copy

##### Transformation with option 1 (Using new schema)[¶](#id67 "Link to this heading")

```
CREATE SCHEMA IF NOT EXISTS MY_PACKAGE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

Copy

Note

Note that that for option 1, the `PROCEDURE` definition in the package is removed since it is not required by Snowflake.

#### Variables declaration[¶](#variables-declaration "Link to this heading")

Note

You might also be interested in [variables helper.](helpers.html#package-variables-helper)

Oracle package variables are transformed into Snowflake Session Variables. A prefix is added to the values to know what type it is inside stored procedures. If the value should be null, a “~” is added. Because of this, variables that depend on other variables will require a SUBSTR and a CAST.

##### Data type and Code mappings[¶](#data-type-and-code-mappings "Link to this heading")

| Data type or value | Code |
| --- | --- |
| Numeric types | # |
| Datetime types | & |
| String types | $ |
| NULL values | ~ |

The transformation of the variables will be always the same regardless of the transformation option.

###### Oracle[¶](#id68 "Link to this heading")

```
CREATE OR REPLACE PACKAGE PACKAGE_VARIABLES AS 
    VAR1 integer := 333;
    VAR2 INTEGER := VAR1 + 456;
	  VAR3 DATE := CURRENT_DATE;
	  VAR4 VARCHAR(20) := 'HELLO WORLD';
	  VAR5 INTEGER;
END;
```

Copy

###### Snowflake[¶](#id69 "Link to this heading")

```
CREATE SCHEMA IF NOT EXISTS PACKAGE_VARIABLES
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PACKAGE_VARIABLES.VAR1" = '' || (333);

SET "PACKAGE_VARIABLES.VAR2" = (SELECT
	'' || (GETVARIABLE('PACKAGE_VARIABLES.VAR1') :: INTEGER + 456));

SET "PACKAGE_VARIABLES.VAR3" = (SELECT
	'' || (CURRENT_DATE()));

SET "PACKAGE_VARIABLES.VAR4" = '' || ('HELLO WORLD');

SET "PACKAGE_VARIABLES.VAR5" = '~';
```

Copy

#### Constants declaration[¶](#constants-declaration "Link to this heading")

Constants declaration will be declared inside the procedure or functions that use them. Existing package constants declaration will be commented out and a warning will be added.

##### Oracle[¶](#id70 "Link to this heading")

```
CREATE OR REPLACE PACKAGE PACKAGE_CONSTANTS
IS
const_name CONSTANT VARCHAR(10) := 'Snow';
PROCEDURE PROCEDURE1;
END PACKAGE_CONSTANTS;

CREATE OR REPLACE PACKAGE BODY PACKAGE_CONSTANTS
IS
PROCEDURE MY_PROCEDURE IS 
   BEGIN 
      INSERT INTO DBUSER ("USER_NAME") 
      VALUES (const_name);
   END;

END PACKAGE_CONSTANTS;
```

Copy

**Transformation with option 1**

```
CREATE SCHEMA IF NOT EXISTS PACKAGE_CONSTANTS
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE PACKAGE_CONSTANTS.MY_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   DECLARE
      CONST_NAME VARCHAR(10) := 'Snow';
   BEGIN
      INSERT INTO DBUSER("USER_NAME")
      VALUES (:CONST_NAME);
   END;
$$;
```

Copy

Note

Note that the `PROCEDURE` definition in the package is removed since it is not required by Snowflake.

#### Other Package members[¶](#other-package-members "Link to this heading")

The transformation for other package members like cursors, exceptions and user defined types, is still a work in progress.

##### Oracle[¶](#id71 "Link to this heading")

```
CREATE OR REPLACE PACKAGE MY_PACKAGE_EX AS
    an_exception EXCEPTION;
END MY_PACKAGE_EX;
```

Copy

##### Transformation with option 1[¶](#transformation-with-option-1 "Link to this heading")

```
CREATE SCHEMA IF NOT EXISTS MY_PACKAGE_EX
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

!!!RESOLVE EWI!!! /*** SSC-EWI-OR0049 - PACKAGE EXCEPTIONS in stateful package MY_PACKAGE_EX are not supported yet ***/!!!
an_exception EXCEPTION;
```

Copy

### Package Body Definition[¶](#package-body-definition "Link to this heading")

This section shows the equivalence between Oracle Package Body Definition members and Snowflake statements.

#### Create Package Body[¶](#create-package-body "Link to this heading")

Elements inside a Package Body are going to be extracted from the package. The package body will disappear so the Create Package Body statement is removed in the converted code.

#### Procedure Definition[¶](#procedure-definition "Link to this heading")

Stored Procedures inside packages use the same transformations defined in the [PL/SQL Translation Reference](#packages).

##### Oracle[¶](#id72 "Link to this heading")

```
CREATE OR REPLACE PACKAGE BODY PACKAGE_PROCEDURE
IS
PROCEDURE MY_PROCEDURE (MY_PARAM VARCHAR) IS 
   BEGIN 
      null;
   END;

END PACKAGE_PROCEDURE;
```

Copy

##### Transformation with option 1[¶](#id73 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PACKAGE_PROCEDURE.MY_PROCEDURE (MY_PARAM STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   // SnowConvert AI Helpers Code section is omitted.

   null;
$$;
```

Copy

##### Transformation with option 2[¶](#id74 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PACKAGE_PROCEDURE_MY_PROCEDURE (MY_PARAM STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   // REGION SnowConvert AI Helpers Code
   null;
$$;
```

Copy

#### Function Definition[¶](#function-definition "Link to this heading")

Functions inside package bodies are converted into Snowflake stored procedures.

##### Oracle[¶](#id75 "Link to this heading")

```
CREATE OR REPLACE PACKAGE BODY PACKAGE_FUNCTION
IS
FUNCTION MY_FUNCTION (MY_PARAM VARCHAR) RETURN NUMBER 
AS
   BEGIN 
      null;
   END;
END PACKAGE_FUNCTION;
```

Copy

##### Transformation with option 1[¶](#id76 "Link to this heading")

```
CREATE OR REPLACE FUNCTION PACKAGE_FUNCTION.MY_FUNCTION (MY_PARAM STRING)
RETURNS FLOAT
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
$$
   // SnowConvert AI Helpers Code section is omitted.
   null;
$$;
```

Copy

##### Transformation with option 2[¶](#id77 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE FUNCTION PACKAGE_FUNCTION_MY_FUNCTION (MY_PARAM STRING)
RETURNS NUMBER
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
$$
   // REGION SnowConvert AI Helpers Code
   null;
$$;
```

Copy

#### Other package body members[¶](#other-package-body-members "Link to this heading")

Please refer to the “other package members” section in [Package declaration.](#package-declaration)

### Using package members[¶](#using-package-members "Link to this heading")

#### Call of procedures inside packages[¶](#call-of-procedures-inside-packages "Link to this heading")

If the procedure is inside a package and the package is inside a schema, the call will be renamed.

##### Oracle[¶](#id78 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROCEDURE02(param1 NUMBER, param2 VARCHAR)
IS
BEGIN
    SCHEMA1.PACKAGE1.PROCEDURE01(param1, param2);
END;

CALL SCHEMA1.PACKAGE1.PROCEDURE01(param1, param2);
```

Copy

##### Transformation with option 1[¶](#id79 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROCEDURE02 (param1 FLOAT, param2 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    EXEC(`CALL
SCHEMA1.PACKAGE1.PROCEDURE01(?, ?)`,[PARAM1,PARAM2]);
$$;

CALL SCHEMA1.PACKAGE1.PROCEDURE01(param1, param2);
```

Copy

##### Transformation with option 2[¶](#id80 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

With this option, the call of the procedures will be renamed accordingly to the rename of the procedure declaration. The schema name will be separated from the procedure name with a dot.

###### Snowflake[¶](#id81 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PUBLIC.PROCEDURE02 (param1 FLOAT, param2 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   // REGION SnowConvert AI Helpers Code
   EXEC(`CALL SCHEMA1.PACKAGE1_PROCEDURE01(?, ?)`,[PARAM1,PARAM2]);
$$;

CALL SCHEMA1.PACKAGE1_PROCEDURE01(param1, param2);
```

Copy

#### Package variables inside procedures[¶](#package-variables-inside-procedures "Link to this heading")

Note

Packages variables are transformed to session variables. Those variables are usable through the “[Package variables helper](helpers.html#package-variables-helper)”.

Note

This sample is using variables declared in packages [Variables declaration](#variables-declaration) section.

##### Oracle[¶](#id82 "Link to this heading")

```
CREATE OR REPLACE PACKAGE BODY PACKAGE_VARIABLES AS
  PROCEDURE P1 AS
    BEGIN         
			VAR1 := VAR1 + 888;         
			INSERT INTO TABLE1 values (VAR1);
         INSERT INTO TABLE2 values (VAR4);
    END;
END;
```

Copy

##### Snowflake[¶](#id83 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PACKAGE_VARIABLES.P1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.
	
	VAR1 =
			!!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT VAR1 MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
			VAR1 + 888;
	EXEC(`INSERT INTO TABLE1
			values (VAR1)`);
	EXEC(`INSERT INTO TABLE2
         values (VAR4)`);
$$;
```

Copy

### Known Issues[¶](#id84 "Link to this heading")

No issues were found.

#### Related EWIs[¶](#id85 "Link to this heading")

1. [SSC-EWI-0053](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0053): Object may not work.
2. [SSC-EWI-OR0049](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0049): Package constants in stateful package are not supported yet.

## Procedures[¶](#procedures "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

**Example 1:** Basic Procedure Conversion

### Oracle[¶](#id86 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1
IS
BEGIN
null;
END;
```

Copy

### Snowflake[¶](#id87 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    null;
$$;
```

Copy

**Example 2:** Procedure Conversion with basic statements: Declaration, Assignment, Cursor Declaration, FOR Cursor, Open, LOOP, CLOSE, IF,

### Oracle[¶](#id88 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1
(
  param1 NUMBER
)
IS
  localVar1 NUMBER;
  countRows NUMBER;
  tempSql VARCHAR(100);
  tempResult NUMBER;
  CURSOR MyCursor
    IS
       SELECT COL1 FROM Table1;

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
END PROC1;
```

Copy

### Snowflake[¶](#id89 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1
(param1 FLOAT
)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // REGION SnowConvert AI Helpers Code
  var formatDate = (arg) => (new Date(arg - (arg.getTimezoneOffset() * 60000))).toISOString().slice(0,-1);
  var fixBind = function (arg) {
    arg = arg instanceof Date ? formatDate(arg) : IS_NULL(arg) ? null : arg;
    return arg;
  };
  var SQL = {
    FOUND : false,
    NOTFOUND : false,
    ROWCOUNT : 0,
    ISOPEN : false
  };
  var _RS, _ROWS, SQLERRM = "normal, successful completion", SQLCODE = 0;
  var getObj = (_rs) => Object.assign(new Object(),_rs);
  var getRow = (_rs) => (values = Object.values(_rs)) && (values = values.splice(-1 * _rs.getColumnCount())) && values;
  var fetch = (_RS,_ROWS,fmode) => _RS.getRowCount() && _ROWS.next() && (fmode ? getObj : getRow)(_ROWS) || (fmode ? new Object() : []);
  var EXEC = function (stmt,binds,opts) {
    try {
      binds = !(arguments[1] instanceof Array) && ((opts = arguments[1]) && []) || (binds || []);
      opts = opts || new Object();
      binds = binds ? binds.map(fixBind) : binds;
      _RS = snowflake.createStatement({
          sqlText : stmt,
          binds : binds
        });
      _ROWS = _RS.execute();
      if (opts.sql !== 0) {
        var isSelect = stmt.toUpperCase().trimStart().startsWith("SELECT");
        var affectedRows = isSelect ? _RS.getRowCount() : _RS.getNumRowsAffected();
        SQL.FOUND = affectedRows != 0;
        SQL.NOTFOUND = affectedRows == 0;
        SQL.ROWCOUNT = affectedRows;
      }
      if (opts.row === 2) {
        return _ROWS;
      }
      var INTO = function (opts) {
        if (opts.vars == 1 && _RS.getColumnCount() == 1 && _ROWS.next()) {
          return _ROWS.getColumnValue(1);
        }
        if (opts.rec instanceof Object && _ROWS.next()) {
          var recordKeys = Object.keys(opts.rec);
          Object.assign(opts.rec,Object.fromEntries(new Map(getRow(_ROWS).map((element,Index) => [recordKeys[Index],element]))))
          return opts.rec;
        }
        return fetch(_RS,_ROWS,opts.row);
      };
      var BULK_INTO_COLLECTION = function (into) {
        for(let i = 0;i < _RS.getRowCount();i++) {
          FETCH_INTO_COLLECTIONS(into,fetch(_RS,_ROWS,opts.row));
        }
        return into;
      };
      if (_ROWS.getRowCount() > 0) {
        return _ROWS.getRowCount() == 1 ? INTO(opts) : BULK_INTO_COLLECTION(opts);
      }
    } catch(error) {
      RAISE(error.code,error.name,error.message)
    }
  };
  var RAISE = function (code,name,message) {
    message === undefined && ([name,message] = [message,name])
    var error = new Error(message);
    error.name = name
    SQLERRM = `${(SQLCODE = (error.code = code))}: ${message}`
    throw error;
  };
  var FETCH_INTO_COLLECTIONS = function (collections,fetchValues) {
    for(let i = 0;i < collections.length;i++) {
      collections[i].push(fetchValues[i]);
    }
  };
  var IS_NULL = (arg) => !(arg || arg === 0);
  var CURSOR = function (stmt,binds,isRefCursor,isOut) {
    var statementObj, result_set, total_rows, ISOPEN = false, result_set_table = '', self = this, row_count, found;
    this.CURRENT = new Object;
    this.INTO = function () {
        return self.res;
      };
    this.OPEN = function (openParameters) {
        if (ISOPEN && !isRefCursor) RAISE(-6511,"CURSOR_ALREADY_OPEN","cursor already open");
        var finalStmt = openParameters && openParameters.query || stmt;
        var parameters = openParameters && openParameters.binds || [];
        var finalBinds = binds instanceof Function ? binds(...parameters) : binds;
        finalBinds = finalBinds || parameters;
        try {
          if (isOut) {
            if (!temptable_prefix) {
              temptable_prefix = `${procname}_TEMP_${(EXEC(`select current_session() || '_' || to_varchar(current_timestamp, 'yyyymmddhh24missss')`,{
                  sql : 0
                }))[0]}_`;
            }
            if (!result_set_table) {
              result_set_table = temptable_prefix + outCursorResultNumber++;
              EXEC(`CREATE OR REPLACE TEMPORARY TABLE ${result_set_table} AS ${finalStmt}`,{
                sql : 0
              });
            }
            finalStmt = "SELECT * FROM " + result_set_table
          }
          [result_set,statementObj,total_rows] = [EXEC(finalStmt,finalBinds,{
              sql : 0,
              row : 2
            }),_RS,_RS.getColumnCount()]
          ISOPEN = true;
          row_count = 0;
        } catch(error) {
          RAISE(error.code,"error",error.message);
        }
        return this;
      };
    this.NEXT = function () {
        if (total_rows && result_set.next()) {
          this.CURRENT = new Object;
          for(let i = 1;i <= statementObj.getColumnCount();i++) {
            (this.CURRENT)[statementObj.getColumnName(i)] = result_set.getColumnValue(i);
          }
          return true;
        } else return false;
      };
    this.FETCH = function (record) {
        var recordKeys = record ? Object.keys(record) : undefined;
        self.res = [];
        if (!ISOPEN) RAISE(-1001,"INVALID_CURSOR","invalid cursor");
        if (recordKeys && recordKeys.length != statementObj.getColumnCount()) RAISE(-6504,"ROWTYPE_MISMATCH","Return types of Result Set variables or query do not match");
        self.res = fetch(statementObj,result_set);
        if (self.res && self.res.length > 0) {
          found = true;
          row_count++;
          if (recordKeys) {
            for(let i = 0;i < self.res.length;i++) {
              record[recordKeys[i]] = (self.res)[i];
            }
            return false;
          }
          return true;
        } else found = false;
        return false;
      };
    this.CLOSE = function () {
        if (!ISOPEN) RAISE(-1001,"INVALID_CURSOR","invalid cursor");
        found = row_count = result_set_table = total_rows = result_set = statementObj = undefined;
        ISOPEN = false;
      };
    this.FETCH_BULK_COLLECT_INTO = function (variables,limit) {
        if (variables.length != statementObj.getColumnCount()) RAISE(-6504,"ROWTYPE_MISMATCH","Return types of Result Set variables or query do not match");
        if (limit) {
          for(let i = 0;i < limit && this.FETCH();i++)FETCH_INTO_COLLECTIONS(variables,self.res);
        } else {
          while ( this.FETCH() )
            FETCH_INTO_COLLECTIONS(variables,self.res);
        }
      };
    this.FOUND = () => ISOPEN ? typeof(found) == "boolean" ? found : null : RAISE(-1001,"INVALID_CURSOR","invalid cursor");
    this.NOTFOUND = () => ISOPEN ? typeof(found) == "boolean" ? !found : null : RAISE(-1001,"INVALID_CURSOR","invalid cursor");
    this.ROWCOUNT = () => ISOPEN ? row_count : RAISE(-1001,"INVALID_CURSOR","invalid cursor");
    this.ISOPEN = () => ISOPEN;
    this.SAVE_STATE = function () {
        return {
          tempTable : result_set_table,
          position : row_count
        };
      };
    this.RESTORE_STATE = function (tempTable,position) {
        result_set_table = tempTable
        if (result_set_table) {
          isOut = true
          this.OPEN();
          for(let i = 0;i < position;i++)this.FETCH();
        }
      };
    this.ROWTYPE = () => ROWTYPE(stmt,binds());
  };
  var outCursorResultNumber = 0;
  var concatValue = (arg) => IS_NULL(arg) ? "" : arg;
  // END REGION

  let LOCALVAR1;
  let COUNTROWS;
  let TEMPSQL;
  let TEMPRESULT;
  let MYCURSOR = new CURSOR(`SELECT COL1 FROM
          Table1`,() => []);
  LOCALVAR1 = PARAM1;
  COUNTROWS = 0;
  TEMPSQL = `SELECT COUNT(*) FROM
   Table1
WHERE COL1 =${concatValue(LOCALVAR1)}`;
  MYCURSOR.OPEN();
  while ( MYCURSOR.NEXT() ) {
    let MYCURSORITEM = MYCURSOR.CURRENT;
    LOCALVAR1 = MYCURSORITEM.COL1;
    COUNTROWS = COUNTROWS + 1;
  }
  MYCURSOR.CLOSE();
  EXEC(`INSERT INTO Table2
    VALUES(?, 'ForCursor: Total Row count is: ' || NVL(? :: STRING, ''))`,[COUNTROWS,COUNTROWS]);
  COUNTROWS = 0;
  MYCURSOR.OPEN();
  while ( true ) {
    MYCURSOR.FETCH(TEMPRESULT) && ([TEMPRESULT] = MYCURSOR.INTO());
    if (MYCURSOR.NOTFOUND()) {
      break;
    }
    COUNTROWS = COUNTROWS + 1;
  }
  MYCURSOR.CLOSE();
  EXEC(`INSERT INTO Table2
    VALUES(?, 'LOOP: Total Row count is: ' || NVL(? :: STRING, ''))`,[COUNTROWS,COUNTROWS]);
  [TEMPRESULT] = EXEC(TEMPSQL);
  if (TEMPRESULT > 0) {
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`INSERT INTO Table2(COL1, COL2) VALUES(?, 'Hi, found value:' || NVL(? :: STRING, '') || ' in Table1 -- There are ' || NVL(? :: STRING, '') || ' rows')`,[TEMPRESULT,LOCALVAR1,TEMPRESULT]);
    EXEC(`--** SSC-FDM-OR0012 - COMMIT REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
COMMIT;`);
  }
$$;
```

Copy

#### Call of procedures inside other procedure[¶](#call-of-procedures-inside-other-procedure "Link to this heading")

##### Oracle[¶](#id90 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROCEDURE01(param1 NUMBER, param2 VARCHAR)
IS
BEGIN
INSERT INTO TABLE1 VALUES(param1, param2);
END;

CREATE OR REPLACE PROCEDURE PROCEDURE02(param1 NUMBER, param2 VARCHAR)
IS
BEGIN
PROCEDURE01(param1, param2);
END;
```

Copy

##### Snowflake[¶](#id91 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROCEDURE01 (param1 FLOAT, param2 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	EXEC(`INSERT INTO TABLE1
	VALUES(?, ?)`,[PARAM1,PARAM2]);
$$;

CREATE OR REPLACE PROCEDURE PROCEDURE02 (param1 FLOAT, param2 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.

	EXEC(`CALL
	PROCEDURE01(?, ?)`,[PARAM1,PARAM2]);
$$;
```

Copy

### Known Issues[¶](#id92 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id93 "Link to this heading")

1. [SSC-EWI-0022](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0022): One or more identifiers in this statement were considered parameters by default.
2. [SSC-FDM-OR0012](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0012): COMMIT and ROLLBACK statements require adequate setup to perform as intended.

## SQL Language Elements[¶](#sql-language-elements "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

### Cursor FOR LOOP[¶](#cursor-for-loop "Link to this heading")

Note

You might also be interested in [Cursor helper](helpers.html#cursor-helper) and [Cursor declaration.](#cursor-declarations-and-definition)

#### Oracle[¶](#id94 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1
IS
    MyVariable1 NUMBER;
    MyOtherVariable2 NUMBER := 1;
    CURSOR C1 IS 
        SELECT * FROM Table1 WHERE ID = 123;
    CURSOR C2 (paramCursor1 NUMBER) IS
        SELECT COL1 AS C_1 FROM TABLE1 WHERE ID = paramCursor1;
BEGIN
    FOR myCursorRecord IN C1
        LOOP
            MyVariable1 := myCursorRecord.Col1;
        END LOOP;

    FOR myCursorRecord IN (SELECT * FROM Table1 WHERE ID = MyVariable1)
        LOOP
            MyVariable1 := myCursorRecord.Col1;
        END LOOP;

    <<Block1>>
    FOR myCursorRecord IN C2 (MyOtherVariable2)
        LOOP
            MyVariable1 := myCursorRecord.Col1;
        END LOOP Block1;
END;
```

Copy

#### Snowflake[¶](#id95 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    let MYVARIABLE1;
    let MYOTHERVARIABLE2 = 1;
    let C1 = new CURSOR(`SELECT * FROM
           Table1
        WHERE ID = 123`,() => []);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    let C2 = new CURSOR(`SELECT COL1 AS C_1 FROM
           TABLE1
        WHERE ID = ?`,(PARAMCURSOR1) => [PARAMCURSOR1]);
    C1.OPEN();
    while ( C1.NEXT() ) {
        let MYCURSORRECORD = C1.CURRENT;
        MYVARIABLE1 = MYCURSORRECORD.COL1;
    }
    C1.CLOSE();
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    for(var MYCURSORRECORD_CURSOR = new CURSOR(`(SELECT * FROM
      Table1
   WHERE ID = ?
)`,[MYVARIABLE1]).OPEN();MYCURSORRECORD_CURSOR.NEXT();) {
        let MYCURSORRECORD = MYCURSORRECORD_CURSOR.CURRENT;
        MYVARIABLE1 = MYCURSORRECORD.COL1;
    }
    MYCURSORRECORD_CURSOR.CLOSE();
    C2.OPEN({
        binds : [MYOTHERVARIABLE2]
    });
    while ( C2.NEXT() ) {
        let BLOCK1 = C2.CURRENT;
        MYVARIABLE1 = MYCURSORRECORD.COL1;
    }
    C2.CLOSE();
$$;
```

Copy

### OPEN, FETCH and CLOSE Statement[¶](#open-fetch-and-close-statement "Link to this heading")

Note

You might also be interested in [Cursor helper](helpers.html#cursor-helper) and [Cursor declaration.](#cursor-declarations-and-definition)

#### Oracle[¶](#id96 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC2
IS
    col1Value   table1.COL1%TYPE;
    col2Value   table1.COL2%TYPE;
    entireRow   table1%ROWTYPE;
    TYPE MyRowType IS RECORD ( COLUMN1 NUMBER, COLUMN2 NUMBER);
    entireRow_1 MyRowType;
    CURSOR C1 IS  SELECT * FROM table1;
    C2 SYS_REFCURSOR;
    TYPE COLLECTION_TYPE IS TABLE OF TABLE1.COL1%TYPE;
    MY_COLLECTION MY_COLLECTION_TYPE := MY_COLLECTION_TYPE();
    SOME_SELECT VARCHAR(200);
BEGIN
    OPEN C1;
    FETCH C1 INTO col1Value, col2Value;
    CLOSE C1;
    
    OPEN C1;
    FETCH C1 INTO entireRow;
    CLOSE C1;
    
    OPEN C1;
    FETCH C1 INTO entireRow_1;
    CLOSE C1;
    
    OPEN C2 FOR 'SELECT COL1 FROM TABLE1 WHERE COL1 <> :v' USING 123;
    FETCH C2 BULK COLLECT INTO MY_COLLECTION LIMIT 2;
    CLOSE C2;
    
    OPEN C2 FOR SELECT * FROM TABLE1 WHERE COL1 = NUM1;
    CLOSE C2;
END;
```

Copy

#### Snowflake[¶](#id97 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC2 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "12/16/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    let COL1VALUE;
    let COL2VALUE;
    let ENTIREROW = ROWTYPE(`table1`);
    class MYROWTYPE {
        COLUMN1
        COLUMN2
        constructor() {
            [...arguments].map((element,Index) => this[(Object.keys(this))[Index]] = element)
        }
    }
    let ENTIREROW_1 = new MYROWTYPE();
    let C1 = new CURSOR(`SELECT * FROM
   table1`,() => []);
    let C2 = new CURSOR(undefined,undefined,true);
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0072 - PROCEDURAL MEMBER TYPE DEFINITION NOT SUPPORTED. ***/!!!
    /*     TYPE COLLECTION_TYPE IS TABLE OF TABLE1.COL1%TYPE */
    ;
    let MY_COLLECTION = new MY_COLLECTION_TYPE();
    let SOME_SELECT;
    C1.OPEN();
    C1.FETCH(COL1VALUE,COL2VALUE) && ([COL1VALUE,COL2VALUE] = C1.INTO());
    C1.CLOSE();
    C1.OPEN();
    C1.FETCH(ENTIREROW) && ([ENTIREROW] = C1.INTO());
    C1.CLOSE();
    C1.OPEN();
    C1.FETCH(ENTIREROW_1) && ([ENTIREROW_1] = C1.INTO());
    C1.CLOSE();
    C2.OPEN({
        query : `SELECT COL1 FROM
   TABLE1
WHERE COL1 <> ?`,
        binds : [123]
    });
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0104 - UNUSABLE VARIABLE, ITS TYPE WAS NOT TRANSFORMED ***/!!!
    /*     FETCH C2 BULK COLLECT INTO MY_COLLECTION LIMIT 2 */
    ;
    C2.CLOSE();
    C2.OPEN({
        query : `SELECT * FROM
   TABLE1
WHERE COL1 = NUM1`
    });
    C2.CLOSE();
$$;
```

Copy

Warning

Transformation for the following lines correspond to custom types which are work in progress:

```
entireRow   table1%ROWTYPE; // ROW TYPES
TYPE COLLECTION_TYPE IS TABLE OF TABLE1.COL1%TYPE; // COLLECTIONS
```

Copy

Currently the next statement is being emitted but the class is not being created yet. A warning will be applied in the future to all the uses of the unsupported custom types.

```
let MY_COLLECTION = new MY_COLLECTION_TYPE();
```

Copy

### SQL Implicit Cursor[¶](#sql-implicit-cursor "Link to this heading")

#### Oracle[¶](#id98 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE SP_IMPLICIT_CURSOR_SAMPLE AUTHID DEFINER IS
  VAR_AUX  NUMBER(3);
  STMT_STAT1  NUMBER(3):= 0;
  STMT_STAT2  NUMBER(3):= 0;
  STMT_STAT3  NUMBER(3):= 0;
BEGIN
  EXECUTE IMMEDIATE 'CREATE TABLE FTABLE35(COL1 NUMBER(3))';
  IF SQL%FOUND THEN
    STMT_STAT1 := 1;
  END IF;
  IF SQL%NOTFOUND THEN
   STMT_STAT2 := 1;
  END IF;
  IF SQL%ISOPEN THEN
   STMT_STAT3 := 1;
  END IF;
  EXECUTE IMMEDIATE 'INSERT INTO FTABLE33 VALUES(:D1,:D2,:D3,:D4)' USING SQL%ROWCOUNT, STMT_STAT1, STMT_STAT2, STMT_STAT3;
END;
```

Copy

#### Snowflake[¶](#id99 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE SP_IMPLICIT_CURSOR_SAMPLE ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "12/16/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
  !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PlInvokerRightsClause' NODE ***/!!!
  //AUTHID DEFINER
  null
  // SnowConvert AI Helpers Code section is omitted.

  let VAR_AUX;
  let STMT_STAT1 = 0;
  let STMT_STAT2 = 0;
  let STMT_STAT3 = 0;
  EXEC(`CREATE OR REPLACE TABLE FTABLE35 (COL1 NUMBER(3)
)`);
  if (SQL.FOUND) {
    STMT_STAT1 = 1;
  }
  if (SQL.NOTFOUND) {
    STMT_STAT2 = 1;
  }
  if (SQL.ISOPEN) {
    STMT_STAT3 = 1;
  }
  EXEC(`INSERT INTO FTABLE33
VALUES(?, ?, ?, ?)`,[SQL.ROWCOUNT /*** SSC-FDM-OR0009 - SQL IMPLICIT CURSOR VALUES MAY DIFFER ***/,STMT_STAT1,STMT_STAT2,STMT_STAT3]);
$$;
```

Copy

### EXIT[¶](#exit "Link to this heading")

Note

You might also be interested in [Loop](#loop)  and [while](#while-statement) statements.

Warning

Transformation for labels is a work in progress.

#### Oracle[¶](#id100 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROCEDURE1
IS
  i NUMBER := 0;
  j NUMBER := 0;
  k NUMBER := 0;
BEGIN
  <<loop_a>>
  LOOP
    i := i + 1;

    <<loop_b>>
    LOOP
      j := j + 1;

      <<loop_c>>
      LOOP
        k := k + j + i;
        EXIT;
      END LOOP loop_c;

      EXIT loop_b WHEN (j > 3);
    END LOOP loop_b;

    EXIT loop_a WHEN (i > 3);
  END LOOP loop_a;
  
END;
```

Copy

#### Snowflake[¶](#id101 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROCEDURE1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "12/16/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  let I = 0;
  let J = 0;
  let K = 0;
  while ( true ) {
    I = I + 1;
    while ( true ) {
      J = J + 1;
      while ( true ) {
        K = K + J + I;
        break;
      }
      !!!RESOLVE EWI!!! /*** SSC-EWI-OR0075 - LABELS IN STATEMENTS ARE NOT SUPPORTED. ***/!!!
      /* 
            EXIT loop_b WHEN (j > 3) */
      ;
    }
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0075 - LABELS IN STATEMENTS ARE NOT SUPPORTED. ***/!!!
    /* 
        EXIT loop_a WHEN (i > 3) */
    ;
  }
$$;
```

Copy

### Execute Immediate[¶](#execute-immediate "Link to this heading")

Note

You might also be interested in [EXEC helper](helpers.html#exec-helper)

#### Oracle[¶](#id102 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE sp_sample5 AS
   sql_stmt    VARCHAR2(200);
   plsql_block VARCHAR2(500);
   emp_id      NUMBER(4) := 7566;
   dept_id     NUMBER(2) := 20;
   dept_id2     NUMBER(2) := 12;
   dept_id_upd VARCHAR(14);
   dept_name   VARCHAR2(14) := 'PERSONNEL';
   location    VARCHAR2(13) := 'DALLAS';
   dept_rec     deptt%ROWTYPE;
   TYPE NumList IS TABLE OF NUMBER;
   sals   NumList;
BEGIN
   EXECUTE IMMEDIATE 'CREATE TABLE dept (id NUMBER, name varchar(14), location varchar2(13))';
   sql_stmt := 'INSERT INTO dept VALUES (:1, :2, :3)';
   EXECUTE IMMEDIATE sql_stmt USING dept_id, dept_name, location;
   sql_stmt := 'SELECT * FROM dept WHERE id = :idd';
   EXECUTE IMMEDIATE sql_stmt INTO dept_rec USING dept_id;
   sql_stmt := 'UPDATE dept SET id = 200 WHERE id = :1 RETURNING name INTO :2';
   EXECUTE IMMEDIATE sql_stmt USING dept_id RETURNING INTO dept_id_upd;
   sql_stmt := 'delete from dept where id = :1 RETURNING name INTO :2';
   EXECUTE IMMEDIATE sql_stmt USING dept_id RETURNING INTO dept_id_upd;
   EXECUTE IMMEDIATE 'INSERT INTO dept VALUES (12, ''NAME1'', ''TEXAS'')';
   EXECUTE IMMEDIATE 'INSERT INTO DEPT VALUES(13, ''' || dept_name || ''', ''LA'')';
   EXECUTE IMMEDIATE 'DELETE FROM dept WHERE id = :num' USING dept_id2;
   EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT = ''DD-MM-YYYY''';
   EXECUTE IMMEDIATE 'SELECT id FROM dept' BULK COLLECT INTO sals;
END;
```

Copy

#### Snowflake[¶](#id103 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE sp_sample5 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "12/16/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
   // SnowConvert AI Helpers Code section is omitted.

   let SQL_STMT;
   let PLSQL_BLOCK;
   let EMP_ID = 7566;
   let DEPT_ID = 20;
   let DEPT_ID2 = 12;
   let DEPT_ID_UPD;
   let DEPT_NAME = `PERSONNEL`;
   let LOCATION = `DALLAS`;
   let DEPT_REC = ROWTYPE(`deptt`);
   !!!RESOLVE EWI!!! /*** SSC-EWI-OR0072 - PROCEDURAL MEMBER TYPE DEFINITION NOT SUPPORTED. ***/!!!
   /*    TYPE NumList IS TABLE OF NUMBER */
   ;
   !!!RESOLVE EWI!!! /*** SSC-EWI-OR0104 - UNUSABLE VARIABLE, ITS TYPE WAS NOT TRANSFORMED ***/!!!
   /*    sals   NumList */
   ;
   EXEC(`CREATE OR REPLACE TABLE dept (id NUMBER(38, 18),
   name varchar(14),
   location VARCHAR(13))`);
   SQL_STMT = `INSERT INTO dept
VALUES (?, ?, ?)`;
   EXEC(SQL_STMT,[DEPT_ID,DEPT_NAME,LOCATION]);
   SQL_STMT = `SELECT * FROM
   dept
WHERE id = ?`;
   EXEC(SQL_STMT,[DEPT_ID],{
      rec : dept_rec
   });
   SQL_STMT = `UPDATE dept
   SET id = 200 WHERE id = ?
   RETURNING name INTO :2`;
   !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'THIS EXECUTE IMMEDIATE CASE' NODE ***/!!!
   /*    EXECUTE IMMEDIATE sql_stmt USING dept_id RETURNING INTO dept_id_upd */
   ;
   SQL_STMT = `delete FROM
   dept
where id = ?
RETURNING name INTO :2`;
   !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'THIS EXECUTE IMMEDIATE CASE' NODE ***/!!!
   /*    EXECUTE IMMEDIATE sql_stmt USING dept_id RETURNING INTO dept_id_upd */
   ;
   EXEC(`INSERT INTO dept
VALUES (12, 'NAME1', 'TEXAS')`);
   EXEC(`INSERT INTO DEPT
VALUES(13, '${concatValue(DEPT_NAME)}', 'LA')`);
   EXEC(`DELETE FROM
   dept
WHERE id = ?`,[DEPT_ID2]);
   EXEC(`ALTER SESSION SET DATE_INPUT_FORMAT = 'DD-MM-YYYY' DATE_OUTPUT_FORMAT = 'DD-MM-YYYY'`);
   !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'THIS EXECUTE IMMEDIATE CASE' NODE ***/!!!
   /*    EXECUTE IMMEDIATE 'SELECT id FROM dept' BULK COLLECT INTO sals */
   ;
$$;
```

Copy

Warning

Since the “RETURNING INTO” clause requires special analysis of the statement executed, its translation is planned to be delivered in the future.

Warning

Transformation for the following line correspond to collection types which is work in progress:

```
TYPE NumList IS TABLE OF NUMBER;
```

Copy

Currently the next statement is being emitted but the class is not being created yet. A warning will be applied in the future to all the uses of the unsupported custom types.

```
let SALS = new NUMLIST();
```

Copy

Also the following `EXECUTE IMMEDIATE` related with the `BULK COLLECT` into the `sals` variable, is also work in progress.

```
EXECUTE IMMEDIATE 'SELECT id FROM dept' BULK COLLECT INTO sals;
```

Copy

### Errors and Exception Handling[¶](#errors-and-exception-handling "Link to this heading")

Note

You might also be interested in [Raise helper](helpers.html#raise-helper)

#### Raise Helper Usage[¶](#raise-helper-usage "Link to this heading")

##### Oracle[¶](#id104 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE HANDLERS_WITH_OTHERS_COMMENTS AUTHID DEFINER IS
  deadlock_detected EXCEPTION;
  deadlock_dex EXCEPTION;
  PRAGMA EXCEPTION_INIT(deadlock_detected, -60);
  PRAGMA EXCEPTION_INIT(deadlock_dex, -63);
BEGIN

  IF true THEN
    RAISE NO_DATA_FOUND;
  END IF;
  IF TRUE THEN
    RAISE_APPLICATION_ERROR(-20010, SQLERRM);
  END IF;
  IF TRUE THEN
    RAISE_APPLICATION_ERROR(-20000, SQLERRM, PARM);
  END IF;
  IF TRUE THEN
    RAISE_APPLICATION_ERROR(-20000, SQLERRM, TRUE);
  END IF;
  IF TRUE THEN
    RAISE_APPLICATION_ERROR(-20000, SQLERRM, FALSE);
  END IF;
  IF TRUE THEN
    RAISE_APPLICATION_ERROR(-20000, 'CUSTOM ERROR MESSAGE', TRUE);
  END IF;
  IF TRUE THEN
    RAISE_APPLICATION_ERROR(-20010, 'SECOND CUSTOM ERROR MESSAGE', TRUE);
  END IF;
  IF TRUE THEN
    RAISE_APPLICATION_ERROR(-20010, 'OTHER CUSTOM ERROR MESSAGE', FALSE);
  END IF;

EXCEPTION
    WHEN EXC_NAME THEN
        --Handle Exc_name  found exception
        null;
    WHEN NO_DATA_FOUND THEN
        --Handle No data found exception
        null;
    WHEN OTHERS THEN
        --Handler for others exception
        null;
END;
```

Copy

##### Snowflake[¶](#id105 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE HANDLERS_WITH_OTHERS_COMMENTS ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "12/16/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
  !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PlInvokerRightsClause' NODE ***/!!!
  //AUTHID DEFINER
  null
  // SnowConvert AI Helpers Code section is omitted.

  try {
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0052 - EXCEPTION DECLARATION IS HANDLED BY RAISE FUNCTION ***/!!!
    /*   deadlock_detected EXCEPTION */
    ;
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0052 - EXCEPTION DECLARATION IS HANDLED BY RAISE FUNCTION ***/!!!
    /*   deadlock_dex EXCEPTION */
    ;
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0051 - PRAGMA EXCEPTION_INIT IS NOT SUPPORTED ***/!!!
    /*   PRAGMA EXCEPTION_INIT(deadlock_detected, -60) */
    ;
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0051 - PRAGMA EXCEPTION_INIT IS NOT SUPPORTED ***/!!!
    /*   PRAGMA EXCEPTION_INIT(deadlock_dex, -63) */
    ;
    if (true) {
      RAISE(100,`NO_DATA_FOUND`,`Single row SELECT returned no rows or your program referenced a deleted element in a nested table or an uninitialized element in an associative array (index-by table).`);
    }
    if (true) {
      RAISE(-20010,SQLERRM);
    }
    if (true) {
      // ** SSC-FDM-OR0011 - ADD TO STACK OF ERRORS IS NOT SUPPORTED, BOOLEAN ARGUMENT PARM WAS REMOVED. **
      RAISE(-20000,SQLERRM);
    }
    if (true) {
      // ** SSC-FDM-OR0011 - ADD TO STACK OF ERRORS IS NOT SUPPORTED, BOOLEAN ARGUMENT TRUE WAS REMOVED. **
      RAISE(-20000,SQLERRM);
    }
    if (true) {
      RAISE(-20000,SQLERRM);
    }
    if (true) {
      // ** SSC-FDM-OR0011 - ADD TO STACK OF ERRORS IS NOT SUPPORTED, BOOLEAN ARGUMENT TRUE WAS REMOVED. **
      RAISE(-20000,`CUSTOM ERROR MESSAGE`);
    }
    if (true) {
      // ** SSC-FDM-OR0011 - ADD TO STACK OF ERRORS IS NOT SUPPORTED, BOOLEAN ARGUMENT TRUE WAS REMOVED. **
      RAISE(-20010,`SECOND CUSTOM ERROR MESSAGE`);
    }
    if (true) {
      RAISE(-20010,`OTHER CUSTOM ERROR MESSAGE`);
    }
  } catch(error) {
    switch(error.name) {
      case `EXC_NAME`: {
        //Handle Exc_name  found exception
        null;
        break;
      }
      case `NO_DATA_FOUND`: {
        //Handle No data found exception
        null;
        break;
      }
      default: {
        //Handler for others exception
        null;
        break;
      }
    }
  }
$$;
```

Copy

When there is not OTHERS handler, SnowConvert AI uses the “default” case in the switch that throws the original Error Object.

#### Commit[¶](#commit "Link to this heading")

Note

You might also be interested in [EXEC helper](helpers.html#exec-helper)

##### Oracle[¶](#id106 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 (param1 NUMBER, param2 NUMBER)
IS
BEGIN
    INSERT INTO TABLE1 VALUES(param1, param2);
    COMMIT;
END;
```

Copy

##### Snowflake[¶](#id107 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC1 (param1 FLOAT, param2 FLOAT)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.
    
    EXEC(`INSERT INTO TABLE1
    VALUES(?, ?)`,[PARAM1,PARAM2]);
    EXEC(`--** SSC-FDM-OR0012 - COMMIT REQUIRES THE APPROPRIATE SETUP TO WORK AS INTENDED **
COMMIT;`);
$$;
```

Copy

#### CASE[¶](#case "Link to this heading")

##### Oracle[¶](#id108 "Link to this heading")

```
CREATE OR REPLACE EDITIONABLE PROCEDURE PROCEDURE2 ()
IS
  localVar1 NUMBER;
  localVar2 VARCHAR(100);
BEGIN
CASE (localVar1)
WHEN 1 THEN
    localVar2 := 'one';
WHEN 2 THEN 
    localVar := 'two'; 
WHEN 3 THEN 
    lovalVar := 'three';
ELSE
    localVar := 'error';
END CASE;

CASE
WHEN localVar = 1 THEN
    localVar2 := 'one';
WHEN localVar = 2 THEN 
    localVar := 'two'; 
WHEN localVar = 3 THEN 
    lovalVar := 'three';
ELSE
    localVar := 'error';
END CASE;
END;
```

Copy

##### Snowflake[¶](#id109 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
--** SSC-FDM-OR0007 - SNOWFLAKE DOESN'T SUPPORT VERSIONING OF OBJECTS. DEVELOPERS SHOULD CONSIDER ALTERNATE APPROACHES FOR CODE VERSIONING. **
CREATE OR REPLACE PROCEDURE PROCEDURE2 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.
  
  let LOCALVAR1;
  let LOCALVAR2;
  switch(LOCALVAR1) {
    case 1:LOCALVAR2 = `one`;
    break;
    case 2:LOCALVAR = `two`;
    break;
    case 3:LOVALVAR = `three`;
    break;
    default:LOCALVAR = `error`;
    break;
  }
  if (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT localVar MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
    LOCALVAR == 1) {
    LOCALVAR2 = `one`;
  } else if (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT localVar MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
    LOCALVAR == 2) {
    LOCALVAR = `two`;
  } else if (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT localVar MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
    LOCALVAR == 3) {
    LOVALVAR = `three`;
  } else {
    LOCALVAR = `error`;
  }
$$;
```

Copy

#### CASE in a variable assignment[¶](#case-in-a-variable-assignment "Link to this heading")

##### Oracle[¶](#id110 "Link to this heading")

```
CREATE OR REPLACE EDITIONABLE PROCEDURE PROCEDURE2 ()
IS
  localVar1 NUMBER;
BEGIN
	var1 := CASE flag
	WHEN 1 THEN 'one'
	WHEN 2 THEN 'two'
	WHEN 3 THEN 'three'
	WHEN 4 THEN 'four'
	ELSE 'unknown' END;

END;
```

Copy

##### Snowflake[¶](#id111 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
--** SSC-FDM-OR0007 - SNOWFLAKE DOESN'T SUPPORT VERSIONING OF OBJECTS. DEVELOPERS SHOULD CONSIDER ALTERNATE APPROACHES FOR CODE VERSIONING. **
CREATE OR REPLACE PROCEDURE PROCEDURE2 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.
	
	let LOCALVAR1;
	VAR1 =
					!!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT flag MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
					FLAG == 1 && `one` || (
						!!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT flag MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
						FLAG == 2 && `two` || (
							!!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT flag MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
							FLAG == 3 && `three` || (
								!!!RESOLVE EWI!!! /*** SSC-EWI-0053 - OBJECT flag MAY NOT WORK PROPERLY, ITS DATATYPE WAS NOT RECOGNIZED ***/!!!
								FLAG == 4 && `four` || `unknown`)));
$$;
```

Copy

#### Call to external C or Java programs[¶](#call-to-external-c-or-java-programs "Link to this heading")

##### Oracle[¶](#id112 "Link to this heading")

```
CREATE OR REPLACE EDITIONABLE PROCEDURE "OWB_REP_OWNER"."WB_RT_DP_CREATE_FKPARTITION" (prfID IN NUMBER,datatype IN VARCHAR2) AUTHID CURRENT_USER AS LANGUAGE JAVA NAME 'oracle.wh.service.impl.dataProfile.analysis.storedprocs.ForeignKey.createFKPartition(int,java.lang.String)';
```

Copy

##### Snowflake[¶](#id113 "Link to this heading")

```
----** SSC-OOS - OUT OF SCOPE CODE UNIT. CREATE PROCEDURE IS OUT OF TRANSLATION SCOPE. **
--CREATE OR REPLACE EDITIONABLE PROCEDURE "OWB_REP_OWNER"."WB_RT_DP_CREATE_FKPARTITION" (prfID IN NUMBER,datatype IN VARCHAR2) AUTHID CURRENT_USER AS LANGUAGE JAVA NAME 'oracle.wh.service.impl.dataProfile.analysis.storedprocs.ForeignKey.createFKPartition(int,java.lang.String)'
                                                                                                                                                                                                                                                                                   ;
```

Copy

### Known Issues[¶](#id114 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id115 "Link to this heading")

1. [SSC-EWI-0022](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0022): One or more identifiers in a specific statement are considered parameters by default.
2. [SSC-EWI-0053](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0053): Object may not work.
3. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.
4. [SSC-EWI-OR0052](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0052): Exception declaration is handled by the raise function.
5. [SSC-EWI-OR0072](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0072): Procedural Member not supported.
6. [SSC-EWI-OR0075](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0075): Current of clause is not supported in Snowflake.
7. [SSC-EWI-OR0104](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0104): Unusable collection variable.
8. [SSC-FDM-OR0007](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0007): Snowflake does not support the versioning of objects. Developers should consider alternate approaches for code versioning.
9. [SSC-FDM-OR0009](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0009): SQL IMPLICIT CURSOR VALUES MAY DIFFER.
10. [SSC-FDM-OR0011](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0011): The Boolean argument was removed because the “add to stack” options is not supported.
11. [SSC-FDM-OR0012:](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0012) COMMIT and ROLLBACK statements require adequate setup to perform as intended.

## DDL - DML Statements[¶](#ddl-dml-statements "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

Note

All statements use the [EXEC helper.](helpers.html#exec-helper)

### SELECT[¶](#select "Link to this heading")

#### Oracle[¶](#id116 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 (param1 VARCHAR)
IS
    VAR1 NUMBER := 789;
BEGIN
    SELECT * FROM TABLE01;
    SELECT DISTINCT COL1 FROM TABLE01;
    SELECT * FROM TABLE01 WHERE COL1 = VAR1;
    SELECT * FROM TABLE01 WHERE COL1 = PARAM1;
    SELECT * FROM TABLE01 WHERE COL1 = PARAM1 AND COL2 = VAR1;
END;
```

Copy

#### Snowflake[¶](#id117 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC1 (param1 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.
    
    let VAR1 = 789;
    EXEC(`SELECT * FROM
       TABLE01`);
    EXEC(`SELECT DISTINCT COL1 FROM
       TABLE01`);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`SELECT * FROM
       TABLE01
    WHERE COL1 = ?`,[VAR1]);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`SELECT * FROM
       TABLE01
    WHERE COL1 = ?`,[PARAM1]);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`SELECT * FROM
       TABLE01
    WHERE COL1 = ?
       AND COL2 = ?`,[PARAM1,VAR1]);
$$;
```

Copy

### SELECT INTO[¶](#select-into "Link to this heading")

#### Oracle[¶](#id118 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 (param1 VARCHAR, param2 VARCHAR)
IS
    VAR1 NUMBER;
    VAR2 NUMBER;
BEGIN
    SELECT COL1 INTO VAR1 FROM TABLE01;
    SELECT COL1 INTO VAR1 FROM TABLE01 WHERE COL2 = PARAM1;
    SELECT COL1 INTO VAR1, VAR2 FROM TABLE01;
    SELECT COL1 INTO VAR1, VAR2 FROM TABLE01
        WHERE COL2 = param1 AND COL3 = param1;
END
```

Copy

#### Snowflake[¶](#id119 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC1 (param1 STRING, param2 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.
    
    let VAR1;
    let VAR2;
    [VAR1] = EXEC(`SELECT
   COL1
FROM
   TABLE01`);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    [VAR1] = EXEC(`SELECT
   COL1
FROM
   TABLE01
WHERE COL2 = ?`,[PARAM1]);
    [VAR1,VAR2] = EXEC(`SELECT
   COL1
FROM
   TABLE01`);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    [VAR1,VAR2] = EXEC(`SELECT
   COL1
FROM
   TABLE01
       WHERE COL2 = ?
   AND COL3 = ?`,[PARAM1,PARAM1]);
$$;
```

Copy

### INSERT and INSERT INTO SELECT[¶](#insert-and-insert-into-select "Link to this heading")

#### Oracle[¶](#id120 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 (param1 VARCHAR)
IS
    var1 NUMBER := 789;
BEGIN
    INSERT INTO TABLE01 VALUES('name', 123);
    INSERT INTO TABLE01 VALUES(param1, 456);
    INSERT INTO TABLE01 VALUES(param1, var1);
    INSERT INTO TABLE01 (col1, col2)
    SELECT col1, col2 FROM TABLE02 tb2
    WHERE tb2.col1 = 'myName';
END;
```

Copy

#### Snowflake[¶](#id121 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC1 (param1 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.
    
    let VAR1 = 789;
    EXEC(`INSERT INTO TABLE01
    VALUES('name', 123)`);
    EXEC(`INSERT INTO TABLE01
    VALUES(?, 456)`,[PARAM1]);
    EXEC(`INSERT INTO TABLE01
    VALUES(?, ?)`,[PARAM1,VAR1]);
    EXEC(`INSERT INTO TABLE01(col1, col2)
    SELECT col1, col2 FROM
       TABLE02 tb2
    WHERE tb2.col1 = 'myName'`);
$$;
```

Copy

### DELETE[¶](#delete "Link to this heading")

#### Oracle[¶](#id122 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1 (PARAM1 VARCHAR)
IS
    VAR1 NUMBER := 0;
BEGIN
    DELETE FROM TABLE1 WHERE COL2 = 1;
    DELETE FROM TABLE1 WHERE COL2 = VAR1;
    DELETE FROM TABLE1 WHERE COL1 = PARAM1;
END;
```

Copy

#### Snowflake[¶](#id123 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC1 (PARAM1 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   // SnowConvert AI Helpers Code section is omitted.
   
    let VAR1 = 0;
    EXEC(`DELETE FROM
       TABLE1
    WHERE COL2 = 1`);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`DELETE FROM
       TABLE1
    WHERE COL2 = ?`,[VAR1]);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`DELETE FROM
       TABLE1
    WHERE COL1 = ?`,[PARAM1]);
$$;
```

Copy

### UPDATE[¶](#update "Link to this heading")

#### Oracle[¶](#id124 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1(PARAM1 VARCHAR)
IS
    VAR1 NUMBER := 3;
BEGIN
    UPDATE TABLE1 SET COL2 = 1 where COL2 = 0;
    UPDATE TABLE1 SET COL1 = VAR1 where COL1 = 0;
    UPDATE TABLE1 SET COL1 = 'name' where COL1 = PARAM11;
    UPDATE TABLE1 SET COL2 = VAR1 where COL1 = PARAM1;
END;
```

Copy

#### Snowflake[¶](#id125 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC1 (PARAM1 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   // SnowConvert AI Helpers Code section is omitted.

    let VAR1 = 3;
    EXEC(`UPDATE TABLE1
       SET COL2 = 1 where COL2 = 0`);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`UPDATE TABLE1
       SET COL1 = ?
       where COL1 = 0`,[VAR1]);
    EXEC(`UPDATE TABLE1
       SET COL1 = 'name' where COL1 = PARAM11`);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`UPDATE TABLE1
       SET COL2 = ?
       where COL1 = ?`,[VAR1,PARAM1]);
$$;
```

Copy

### MERGE[¶](#merge "Link to this heading")

#### Oracle[¶](#id126 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE PROC1
IS
BEGIN
	MERGE INTO TABLE01 t01
	USING TABLE02 t02
		ON (t01.col2 = t02.col2)
	WHEN MATCHED THEN 
		UPDATE SET t01.col1 = t02.col2;
END;
```

Copy

#### Snowflake[¶](#id127 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
	// SnowConvert AI Helpers Code section is omitted.
	
	EXEC(`MERGE INTO TABLE01 t01
	USING TABLE02 t02
		ON (t01.col2 = t02.col2)
		WHEN MATCHED THEN
		   UPDATE SET t01.col1 = t02.col2`);
$$;
```

Copy

### Known Issues[¶](#id128 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id129 "Link to this heading")

1. [SSC-EWI-0022](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0022): One or more identifiers in a specific statement are considered parameters by default.

## Synonyms[¶](#synonyms "Link to this heading")

Synonyms used inside PL/SQL blocks are changed to the referenced object and the Schema will be added if necessary.

### Implicit Schema added[¶](#implicit-schema-added "Link to this heading")

When the procedure or function is inside a schema and the synonym is inside that schema, but it is being used without the schema, the converted code will add the schema.

#### Oracle[¶](#id130 "Link to this heading")

```
CREATE TABLE schema_one.TABLE_TEST1(
    COL1 INTEGER,
    COL2 DATE DEFAULT SYSDATE
    );

CREATE OR REPLACE SYNONYM schema_one.MY_SYNONYM1 FOR schema_one.TABLE_TEST1;

create or replace procedure schema_one.procedure1  as
returnval integer;
begin
    select col1 into returnval from my_synonym1;
end;
```

Copy

#### Snowflake[¶](#id131 "Link to this heading")

```
CREATE OR REPLACE TABLE schema_one.TABLE_TEST1 (
        COL1 INTEGER,
        COL2 TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/ DEFAULT CURRENT_TIMESTAMP()
        )
        COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
        ;

--        --** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **

--        CREATE OR REPLACE SYNONYM schema_one.MY_SYNONYM1 FOR schema_one.TABLE_TEST1
                                                                                   ;

        CREATE OR REPLACE PROCEDURE schema_one.procedure1 ()
        RETURNS VARCHAR
        LANGUAGE SQL
        COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
        EXECUTE AS CALLER
        AS
        $$
        DECLARE
                returnval integer;
        BEGIN
                select col1 into
                    :returnval
                from
                    schema_one.TABLE_TEST1;
        END;
        $$;
```

Copy

### Schema of referenced object added[¶](#schema-of-referenced-object-added "Link to this heading")

When the synonym references an object that is in a specific schema, the schema name will be added to the referenced object.

#### Oracle[¶](#id132 "Link to this heading")

```
CREATE OR REPLACE SYNONYM MY_SYNONYM2 FOR schema_one.TABLE_TEST1;

create or replace procedure procedure2  as
returnval integer;
begin
    select col1 into returnval from my_synonym2;
end;
```

Copy

#### Snowflake[¶](#id133 "Link to this heading")

```
----** SSC-FDM-OR0005 - SYNONYMS NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS SYNONYM WERE CHANGED BY THE ORIGINAL OBJECT NAME. **
--CREATE OR REPLACE SYNONYM MY_SYNONYM2 FOR schema_one.TABLE_TEST1
                                                                ;

CREATE OR REPLACE PROCEDURE procedure2 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.
    
    let RETURNVAL;
    [RETURNVAL] = EXEC(`SELECT
   col1
from
   schema_one.TABLE_TEST1`);
$$;
```

Copy

### Related EWIs[¶](#id134 "Link to this heading")

1. [SSC-FDM-OR0005](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0005): Synonyms are not supported in Snowflake but references to this synonym were changed by the original object name.
2. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042): Date Type Transformed To Timestamp Has A Different Behavior.

## Triggers[¶](#triggers "Link to this heading")

Warning

Triggers are not supported by Snowflake, and then they will not be migrated automatically.

Snowflake at this moment does not provide a direct mechanism for triggers, but some Snowflake features can be used to achieve similar results.

We recommend that you perform an analysis of your triggers, and classify them by purpose:

* **Audit Triggers:** the intention of these triggers is to capture information and record the changes done on some tables into other tables.
* **Initialization Triggers:** the intention of these triggers is to add some default values to the new records. They are usually before or after insert triggers
* **Business Rule Barrier Triggers**: these usually apply for BEFORE/AFTER DELETE or UPDATE. These triggers are meant to create a *barrier* to avoid data entry or deletion that will break some business rules.
* **Instead of Triggers**: used for example to allow inserts on views are not supported. The recommendation will be to turn that logic into a stored procedure and introduce calls whenever they were used for insert/delete/update operations.
* **Database Triggers:** cannot be replicated, it is also recommended to encapsulate this logic into a stored procedure. But this logic will need to be manually invoked.
* **Generic After Triggers**: for some **after** triggers, streams, and tasks can be leveraged see section below.

### Audit Trigger[¶](#audit-trigger "Link to this heading")

```
CREATE OR REPLACE TRIGGER SCHEMA.TRIGGER_NAME
BEFORE UPDATE OR INSERT ON SCHEMA.TRIGGER_NAME FOR EACH ROW  
BEGIN 
:NEW.LAST_UPDATE := SYSDATE; 
END;
```

Copy

Before UPDATE triggers for audit cases like this cannot be handled directly. For the INSERT case you can use the default value case explained for the initialization trigger. However for the update case the only option will be to use a task as it is explained later for AFTER triggers. However the LAST\_*UPDATE will not be accurate, there will be an offset because the recorded modification will be at the time of task execution (for example if the tasks executes each 5min then the LAST\_UPDATE will be recorded 5min later)*.

For UPDATE cases trying to capture the CURRENT\_USER is not possible.

Other cases of AUDIT triggers are when they register changes of a table into an update table. Using the AFTER trigger technique describe later can be used but again USER information cannot be tracked and TIME information will not be accurate.

### Initialization Trigger[¶](#initialization-trigger "Link to this heading")

```
CREATE OR REPLACE TRIGGER SCHEMA.TRIGGER_NAME
BEFORE INSERT ON SCHEMA.TABLE1 FOR EACH ROW
BEGIN
   SELECT SCHEMA.TABLE.NEXTVAL INTO :NEW.COLUMN_SEQ FROM DUAL;
   SELECT USER INTO :NEW.UPDATED_BY FROM DUAL;
   SELECT SYSTIMESTAMP INTO :NEW.UPDATED_TM FROM DUAL;
END
```

Copy

For these triggers, you might use [Snowflake Default column values](https://docs.snowflake.com/en/sql-reference/sql/create-table.html#optional-parameters) for example for sequence values.

You can also use `CURRENT_`*`USER`() and `CURRENT_TIMESTAMP` instead of `USER` or `SYS_TIMESTAMP`*

This only applies for BEFORE INSERT or AFTER INSERT cases.

### Business Rule Barrier[¶](#business-rule-barrier "Link to this heading")

```
CREATE OR REPLACE EDITIONABLE TRIGGER SCHEMA.TRIGGER_NAME
BEFORE DELETE ON SCHEMA.TABLE FOR EACH ROW
BEGIN
   IF (:OLD.termination_date is NULL OR 
   :OLD.termination_date >= TRUNC(SYSDATE)+1 ) THEN
     RAISE_APPLICATION_ERROR(-30001,'An employee must be terminated before deleteing the row');
 END IF;
```

Copy

For these cases you will need to in-line the trigger actions after/before the DELETE or UPDATE is performed.

A task is not recommended here because tasks are run on an schedule, and then the row will already be modified.

Warning

This section shows a known workaround for partially implementing *AFTER* Triggers.

### **GENERIC AFTER TRIGGER**[¶](#generic-after-trigger "Link to this heading")

#### Example 1: Basic Trigger conversion[¶](#example-1-basic-trigger-conversion "Link to this heading")

##### Oracle[¶](#id135 "Link to this heading")

```
CREATE TRIGGER example_trigger
AFTER INSERT ON table1
SELECT * FROM DUAL;
```

Copy

##### Snowflake[¶](#id136 "Link to this heading")

Note

SnowConvert AI helpers Code removed from the example. You can find them [here.](helpers)

```
----** SSC-OOS - OUT OF SCOPE CODE UNIT. CREATE TRIGGER IS OUT OF TRANSLATION SCOPE. **
--CREATE TRIGGER example_trigger
--AFTER INSERT ON table1
--SELECT * FROM DUAL
```

Copy

### In-depth explanation for the snowflake code[¶](#in-depth-explanation-for-the-snowflake-code "Link to this heading")

#### Streams[¶](#streams "Link to this heading")

These take care of storing the changes made to the table. Please note:

* These will store the delta between the current table state, and the last offset stored by the stream itself. Please take this into account for billing purposes.
* Notice that these do **not** store the information of updates, but rather store them as an insertion.
* In the same manner, they cannot be configured to track only deletions or only updates, and thus they should have to be filtered in the procedure and the task itself (see below).

#### Procedures[¶](#id137 "Link to this heading")

These take care of running the trigger’s SQL statement(s). Please note:

* There is a need to flush the stream, hence the new stream creation at the end of the procedure.
* Any actions that need to be filtered (like AFTER-INSERTs-only triggers) will need to be filtered in the stored procedure itself.

#### Tasks[¶](#tasks "Link to this heading")

These take care of regularly verifying for stream changes and accordingly execute the trigger’s SQL statement(s). Please note:

* The Tasks work on a schedule, an action does not trigger them. This means that there will be trigger scheduled checks with no data changes performed in the table.
* Tasks cannot be configured to run more than once every sixty (60) seconds, as the minimum time is one (1) minute.
* Once the stream has detected changes there will be, in the worst-case scenario, sixty (60) seconds of delay between the change detection and the trigger execution.
* While adding the WHEN avoids Task execution, snowflake still adds Charge every time it is evaluated; and said Charge will be added to the bill when the trigger actually executes.
* The Task needs a Warehouse to be executed in and will need to be manually set by the client.

### Known Issues[¶](#id138 "Link to this heading")

No issues were found.

### Related EWIs[¶](#id139 "Link to this heading")

No related EWIs.

## TYPE attribute[¶](#type-attribute "Link to this heading")

### Description[¶](#id140 "Link to this heading")

This chapter is related to transforming the [TYPE attribute](https://docs.oracle.com/en/database/oracle/oracle-database/18/lnpls/TYPE-attribute.html#GUID-EAB44F7E-B2AB-4AC6-B83D-B586193D75FC) when it references a column, variable, record, collection, or cursor. The transformation involves getting the referenced item data type and replacing the referencing item TYPE attribute for the data type obtained.

### Sample Source Patterns[¶](#id141 "Link to this heading")

#### TYPE attribute for columns[¶](#type-attribute-for-columns "Link to this heading")

In this case, the referenced item is a column from a table created previously.

##### Oracle[¶](#id142 "Link to this heading")

```
CREATE TABLE table1(
col1 NUMBER
);

CREATE OR REPLACE PROCEDURE procedure1
IS
var1 table1.col1%TYPE;
BEGIN
NULL;
END;
```

Copy

##### Snowflake[¶](#id143 "Link to this heading")

```
CREATE OR REPLACE TABLE table1 (
col1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
DECLARE
var1 NUMBER(38, 18);
BEGIN
NULL;
END;
$$;
```

Copy

#### TYPE attribute for variables[¶](#type-attribute-for-variables "Link to this heading")

In this case, the referenced item is a variable declared previously.

##### Oracle[¶](#id144 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE procedure1
IS
var0 FLOAT;
var1 var0%TYPE;
var2 var1%TYPE;
var3 var2%TYPE;
BEGIN
NULL;
END;
```

Copy

##### Snowflake[¶](#id145 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
DECLARE
var0 FLOAT;
var1 FLOAT;
var2 FLOAT;
var3 FLOAT;
BEGIN
NULL;
END;
$$;
```

Copy

Note

Further information about FLOAT datatype can be found in [FLOAT Data Type](../basic-elements-of-oracle-sql/data-types/oracle-built-in-data-types.html#float-data-type) section

#### TYPE attribute for records[¶](#type-attribute-for-records "Link to this heading")

In this case, the referenced item is a record declared previously.

##### Oracle[¶](#id146 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE procedure1
IS
TYPE record_typ_def IS RECORD(field1 NUMBER);
record_var record_typ_def;
var1 record_var%TYPE;
var2 record_var.field1%TYPE;
BEGIN
NULL;
END;
```

Copy

##### Snowflake[¶](#id147 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
DECLARE
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!
TYPE record_typ_def IS RECORD(field1 NUMBER);
record_var OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - record_typ_def DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
var1 OBJECT := OBJECT_CONSTRUCT();
var2 NUMBER(38, 18);
BEGIN
NULL;
END;
$$;
```

Copy

In the example before, the variable which is referencing the record variable is changed to `OBJECT` as same as the record variable, and the variable which is referencing the record field is changed to the record field data type (`NUMBER (38, 18)`).

Warning

These changes don’t work for embedded records.

Note

Further information about records can be found in [Collection & Records](#collections-records) section.

#### TYPE attribute for collections[¶](#type-attribute-for-collections "Link to this heading")

In this case, the referenced item is a collection variable, but since collections are not supported, the referencing item TYPE attribute is changed to VARIANT data type.

##### Oracle[¶](#id148 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE procedure1
IS
TYPE collection_type IS TABLE OF NUMBER;
collection_var collection_type;
var1 collection_var%TYPE;
BEGIN
NULL;
END;
```

Copy

##### Snowflake[¶](#id149 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
DECLARE
--!!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--TYPE collection_type IS TABLE OF NUMBER;
collection_var VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'collection_type' USAGE CHANGED TO VARIANT ***/!!!;
var1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'collection_var%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
BEGIN
NULL;
END;
$$;
```

Copy

#### TYPE attribute for cursors[¶](#type-attribute-for-cursors "Link to this heading")

In this case, the referenced item is a cursor variable, but since REF cursors are not supported, the referencing item TYPE attribute is changed to VARIANT data type.

##### Oracle[¶](#id150 "Link to this heading")

```
CREATE TABLE table1 (col1 NUMBER);

CREATE OR REPLACE PROCEDURE procedure1
IS
TYPE cursor_type IS REF CURSOR RETURN table1%ROWTYPE;
cursor_var cursor_type;
var1 cursor_var%TYPE;
BEGIN
NULL;
END;
```

Copy

##### Snowflake[¶](#id151 "Link to this heading")

```
CREATE OR REPLACE TABLE table1 (col1 NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
DECLARE
--!!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL REF CURSOR TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--TYPE cursor_type IS REF CURSOR RETURN table1%ROWTYPE;
cursor_var_res RESULTSET;
var1_res RESULTSET;
BEGIN
NULL;
END;
$$;
```

Copy

Note

For those cases when the data type of the referenced item cannot be obtained, the referencing item TYPE attribute is changed to `VARIANT`.

### Knows Issues[¶](#knows-issues "Link to this heading")

#### 1. Cursors and collections declarations are not supported.[¶](#cursors-and-collections-declarations-are-not-supported "Link to this heading")

Collection and cursor variable declarations are not supported yet so the referencing item TYPE attribute is changed to VARIANT and a warning is added in these cases.

##### 2. Original data type could not be obtained.[¶](#original-data-type-could-not-be-obtained "Link to this heading")

When the referenced item data type could not be obtained the referencing item TYPE attribute is changed to VARIANT and a warning is added.

### Related EWIS[¶](#id152 "Link to this heading")

1. [SSC-EWI-0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036): Data type converted to another data type.
2. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056): Create Type Not Supported.
3. [SSC-EWI-0058](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0058): Functionality is not currently supported by Snowflake Scripting.
4. [SSC-EWI-0062](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0062): Custom type usage changed to variant.
5. [SSC-EWI-OR0129](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0129): The statement below has usages of nested cursors.
6. [SSC-FDM-0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006): Number type column may not behave similarly in Snowflake.

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

1. [Collections & Records](#collections-records)
2. [Conditional Compilation](#conditional-compilation)
3. [Control Statements](#control-statements)
4. [Declarations](#declarations)
5. [Expressions and operators](#expressions-and-operators)
6. [User defined functions](#user-defined-functions)
7. [Packages](#packages)
8. [Procedures](#procedures)
9. [SQL Language Elements](#sql-language-elements)
10. [DDL - DML Statements](#ddl-dml-statements)
11. [Synonyms](#synonyms)
12. [Triggers](#triggers)
13. [TYPE attribute](#type-attribute)