---
description: Translation references to convert Teradata BTEQ files to Snowflake SQL
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-snowflake-sql-translation-reference/bteq
title: SnowConvert AI - Teradata - BTEQ | Snowflake Documentation
---

## Description

### Note

Some parts in the output code are omitted for clarity reasons.

> Basic Teradata Query (BTEQ) is a general-purpose, command-based program that enables users on a
> workstation to communicate with one or more Teradata Database systems and to format reports for
> both print and screen output.

For more information regarding BTEQ, check
[here](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018).

### Sample Source Patterns

#### 1. Basic BTEQ Example

The BTEQ content is relocated within an `EXECUTE IMMEDIATE` block of to transfer the BTEQ script
functionality to Snowflake SQL executable code.

All the DML and DDL statements inside BTEQ scripts are supported by SnowConvert AI and successfully
translated to Snowflake SQL. The commands that do not have support yet, or do not have support at
all, are being marked with a warning message and commented out.

##### Teradata BTEQ

```sql
 -- Additional Params: -q SnowScript
.LOGON 0/dbc,dbc;
   DATABASE tduser;

   CREATE TABLE employee_bkup (
      EmployeeNo INTEGER,
      FirstName CHAR(30),
      LastName CHAR(30),
      DepartmentNo SMALLINT,
      NetPay INTEGER
   )
   Unique Primary Index(EmployeeNo);

   DROP TABLE employee_bkup;

   .IF ERRORCODE <> 0 THEN .EXIT ERRORCODE;
.LOGOFF;
```

##### Snowflake SQL

```sql
 EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    --.LOGON 0/dbc,dbc
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    BEGIN
      USE DATABASE tduser;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      CREATE OR REPLACE TABLE employee_bkup (
        EmployeeNo INTEGER,
        FirstName CHAR(30),
        LastName CHAR(30),
        DepartmentNo SMALLINT,
        NetPay INTEGER,
        UNIQUE (EmployeeNo)
      );
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      DROP TABLE employee_bkup;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    IF (STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/ != 0) THEN
      RETURN STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
    END IF;
    --.LOGOFF
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'LogOff' NODE ***/!!!
    null;
  END
$$
```

#### 2. Bash Variable Placeholders Example

SnowConvert AI supports the migration of BTEQ code with Bash Variable Placeholders used for shell
scripts, these placeholders will be migrated to its SnowSQL equivalent and
[SSC-FDM-TD0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0003)
will be added to the code. Please consider the following when migrating code with these
placeholders:

- SnowConvert AI does **not** support the migration of shell scripts, to migrate the BTEQ code
  please isolate it in a BTEQ file and supply it as input for the tool.
- SnowSQL with variable substitution enabled is required to execute the migrated code, for more
  information on how to use SnowSQL please check
  [SSC-FDM-TD0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0003)
  and the
  [official documentation for SnowSQ](https://docs.snowflake.com/en/user-guide/snowsql-use.html#using-snowsql)L.

##### Teradata BTEQ 2

```sql
 -- Additional Params: -q SnowScript
.LOGON dbc, dbc;

DATABASE testing;

SELECT $columnVar FROM $tableVar WHERE col2 = $nameExprVar;
INSERT INTO $tableName values ('$myString', $numValue);
UPDATE $dbName.$tableName SET col1 = $myValue;
DELETE FROM $tableName;

.LOGOFF;
```

##### Snowflake SQL 2

```sql
 EXECUTE IMMEDIATE
$$
  --** SSC-FDM-TD0003 - BASH VARIABLES FOUND, USING SNOWSQL WITH VARIABLE SUBSTITUTION ENABLED IS REQUIRED TO RUN THIS SCRIPT **
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    -- Additional Params: -q SnowScript
    --.LOGON dbc, dbc
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    BEGIN
      USE DATABASE testing;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      SELECT
        &columnVar
      FROM
        &tableVar
      WHERE
        col2 = &nameExprVar;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      INSERT INTO &tableName
      VALUES ('&myString', &numValue);
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      UPDATE &dbName.&tableName
        SET
          col1 = &myValue
        ;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    BEGIN
      DELETE FROM
        &tableName;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    --.LOGOFF
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'LogOff' NODE ***/!!!
    null;
  END
$$
```

### Known Issues

1. **There may be BTEQ commands that do not have an equivalent in Snowflake SQL**

Since BTEQ is a command-based program, there may be some commands in your input code that do not
have a hundred percent functional equivalence in Snowflake SQL. Those particular cases are
identified, marked with warnings in the output code, and documented in the further pages.

### Related EWIs

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
2. [SSC-FDM-TD0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0003):
   Bash variables found, using Snow SQL with variable substitution enabled is required to run this
   script.
3. [SSC-FDM-TD0013](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0013):
   The Snowflake error code mismatch the original Teradata error code.
