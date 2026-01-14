---
description:
  Translation references to convert Teradata script statements that are in common among all scripts
  syntaxes to Snowflake SQL
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-snowflake-sql-translation-reference/common-statements
title: SnowConvert AI - Teradata - COMMON STATEMENTS | Snowflake Documentation
---

## ERROR HANDLING[¶](#error-handling)

> The BTEQ error handling capabilities are based on the Teradata Database error codes. These are the
> standard error codes and messages produced in response to user-specified Teradata SQL statements.
> A BTEQ user cannot change, modify or delete these messages.

For more information regarding BTEQ Error Handling, check
[here](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018/Using-BTEQ/Error-Handling).

### Sample Source Patterns[¶](#sample-source-patterns)

#### Basic BTEQ Error Handling Example[¶](#basic-bteq-error-handling-example)

The error conditions content is relocated in different statements in case ERRORCODE is different to
zero, otherwise it can be located as the original code. First, the query above the if statement is
relocated within a BEGIN - END block, where in case of an exception it will be caught in the
EXCEPTION block. Second of all, the ERRORCODE variable will be changed to the variable declared
indicating their SQLCODE with an EWI indicating that the exact number of the SQLCODE is not the same
as the ERRORCODE in BTEQ.

##### Teradata BTEQ[¶](#teradata-bteq)

```
-- Additional Params: -q SnowScript
SELECT * FROM table1;

.IF ERRORCODE<>0 THEN .EXIT 1

.QUIT 0
```

Copy

##### Snowflake SQL[¶](#snowflake-sql)

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    BEGIN
      -- Additional Params: -q SnowScript
      SELECT
        *
      FROM
        table1;
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    IF (STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/ != 0) THEN
      RETURN 1;
    END IF;
    RETURN 0;
  END
$$
```

Copy

### Known Issues[¶](#known-issues)

No issues were found.

### Related EWIs[¶](#related-ewis)

1. [SSC-FDM-TD0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0013):
   The Snowflake error code mismatch the original Teradata error code.

## EXIT or QUIT[¶](#exit-or-quit)

Logs off all database sessions and then exits BTEQ.

The highest severity value encountered during BTEQ’s execution will by default be used as BTEQ’s
return code value unless an argument is explicitly supplied.
([Teradata Basic Query Reference EXIT or QUIT Command](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018/BTEQ-Commands/BTEQ-Command-Descriptions/ERROROUT))

```
.<ExitCommand> [<Result>];
<ExitCommand> := EXIT | QUIT
<Result> := <Status_variable> | Number
<Status_variable> := ACTIVITY_COUNT | ERRORCODE | ERRORLEVEL
```

Copy

### Sample Source Patterns[¶](#id1)

#### Basic IF example[¶](#basic-if-example)

##### Teradata BTEQ[¶](#id2)

```
-- Additional Params: -q SnowScript
.QUIT ERRORCODE;
```

Copy

##### Snowflake SQL[¶](#id3)

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    RETURN STATUS_OBJECT['SQLCODE'] /*** SSC-FDM-TD0013 - THE SNOWFLAKE ERROR CODE MISMATCH THE ORIGINAL TERADATA ERROR CODE ***/;
  END
$$
```

Copy

### Known Issues[¶](#id4)

When the EXIT or QUIT command doesn’t have an input, it returns the ERRORLEVEL as default. However,
SnowConvert AI transforms it to return 0.

### Related EWIS[¶](#id5)

1. [SSC-FDM-TD0013](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0013):
   The Snowflake error code mismatch the original Teradata error code.

## GOTO[¶](#goto)

### Description[¶](#description)

> The BTEQ Goto command skips over all intervening BTEQ commands and SQL statements until a
> specified label is encountered, then resumes processing as usual.
> ([Teradata Basic Query Reference Goto Command](https://docs.teradata.com/r/1fdhoBglKXYl~W_OyMEtGQ/KzhGjSojGrSjKxfWnYYrMw))

```
.GOTO LabelName;
```

Copy

### Sample Source Patterns[¶](#id6)

#### Basic GOTO example[¶](#basic-goto-example)

Snowflake scripting doesn’t have an equivalent statement for Teradata BTEQ Goto command, but
fortunately it can be removed from the input code and get an equivalent code, due to the sequence of
Goto and Labels commands in reverse topological order always. In other words, the definitions come
after their uses. Thus, SnowConvert AI just needs to copy bottom-up all Label section code to its
corresponding Goto statements.

##### Teradata BTEQ[¶](#id7)

```
-- Additional Params: -q SnowScript
.LOGON 0/dbc,dbc;
   DATABASE tduser;
.LOGON 127.0.0.1/dbc,dbc;

INSERT INTO TABLEB VALUES (1);
.IF activitycount = 0 then .GOTO SECTIONA
.IF activitycount >= 1 then .GOTO SECTIONB

.label SECTIONA
.REMARK 'Zero Hours on Account'
.GOTO SECTIONC

.label SECTIONB
.REMARK 'Total Hours on Account'

.label SECTIONC
.logoff
.exit
```

Copy

##### Snowflake[¶](#snowflake)

```
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
    --.LOGON
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTLogOn' NODE ***/!!!
    null;
    /*** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '4' COLUMN '8' OF THE SOURCE CODE STARTING AT '127.0'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'LOGON' ON LINE '4' COLUMN '2'. FAILED TOKEN WAS '127.0' ON LINE '4' COLUMN '8'. CODE '81'. ***/
    /*--127.0.0.1/dbc,dbc*/

    BEGIN
      INSERT INTO TABLEB
      VALUES (1);
      STATUS_OBJECT := OBJECT_CONSTRUCT('SQLROWCOUNT', SQLROWCOUNT);
    EXCEPTION
      WHEN OTHER THEN
        STATUS_OBJECT := OBJECT_CONSTRUCT('SQLCODE', SQLCODE, 'SQLERRM', SQLERRM, 'SQLSTATE', SQLSTATE);
    END;
    IF (NOT (STATUS_OBJECT['SQLROWCOUNT'] = 0)) THEN
      --** SSC-FDM-TD0026 - GOTO SECTIONA WAS REMOVED DUE TO IF STATEMENT INVERSION **

      IF (STATUS_OBJECT['SQLROWCOUNT'] >= 1) THEN

        /*.label SECTIONB*/

        --.REMARK 'Total Hours on Account'
        null;
        /*.label SECTIONC*/

        --.logoff
        null;
        RETURN 0;
      END IF;
    END IF;
    /*.label SECTIONA*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    --.REMARK 'Zero Hours on Account'
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Remark' NODE ***/!!!
    null;

    /*.label SECTIONC*/

    --.logoff
    null;
    RETURN 0;
    /*.label SECTIONB*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    --.REMARK 'Total Hours on Account'
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Remark' NODE ***/!!!
    null;
    /*.label SECTIONC*/
    --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **

    --.logoff
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'LogOff' NODE ***/!!!
    null;
    RETURN 0;
  END
$$
```

Copy

### Known Issues [¶](#id8)

No issues were found.

### Related EWIS[¶](#id9)

1. [SSC-EWI-0001](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0001):
   Unrecognized token on the line of the source code.
2. [SSC-FDM-0027](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0027):
   Removed next statement, not applicable in SnowFlake.
3. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review
4. [SSC-FDM-TD0026](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM.html#ssc-fdm-td0026):
   GOTO statement was removed due to if statement inversion.

## IF… THEN…[¶](#if-then)

### Description[¶](#id10)

> The IF statement validates a condition and executes an action when the action is true.
> ([Teradata SQL Language reference IF…THEN…](https://docs.teradata.com/r/1fdhoBglKXYl~W_OyMEtGQ/92K64CKQxrkuO4Hm7P8IEA))

```
.IF <Condition> THEN <Action>;

<Condition> := <Status_variable> <Operator> Number
<Status_variable> := ACTIVITY_COUNT | ERRORCODE | ERRORLEVEL
<Operator> := ^= | != | ~= | <> | = | < | > | <= | >=
<Action> := BTEQ_command | SQL_request
```

Copy

### Sample Source Patterns[¶](#id11)

#### Basic IF example[¶](#id12)

##### Teradata BTEQ[¶](#id13)

```
-- Additional Params: -q SnowScript
.IF ACTIVITYCOUNT <> 0 THEN .GOTO InsertEmployee;
```

Copy

##### Snowflake SQL[¶](#id14)

```
EXECUTE IMMEDIATE
$$
  DECLARE
    STATUS_OBJECT OBJECT := OBJECT_CONSTRUCT('SQLCODE', 0);
  BEGIN
    IF (STATUS_OBJECT['SQLROWCOUNT'] != 0) THEN

      RETURN 1;
    END IF;
  END
$$
```

Copy

### Related EWIS[¶](#id15)

No related EWIs.
