---
description: This is a translation reference to convert SQL Plus statements to SnowSQL (CLI Client)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-plus
title: SnowConvert AI - Oracle - SQL*Plus | Snowflake Documentation
---

## Accept[¶](#accept)

Warning

Transformation for this command is pending

### Description[¶](#description)

> Reads a line of input and stores it in a given substitution variable..
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/ACCEPT.html#GUID-5D07E526-202B-429B-9E0C-005D1E37BBAB))

#### Oracle Syntax[¶](#oracle-syntax)

```
ACC[EPT] variable [NUM[BER] | CHAR | DATE | BINARY_FLOAT | BINARY_DOUBLE] [FOR[MAT] format] [DEF[AULT] default] [PROMPT text|NOPR[OMPT]] [HIDE]
```

Snowflake does not have a direct equivalent to this command. In order to emulate this functionality,
the SnowCLI`!system` command will be used by taking advantage of the system resources for the input
operations.

#### 1. Accept command[¶](#accept-command)

##### Oracle[¶](#oracle)

##### Command[¶](#command)

```
ACCEPT variable_name CHAR PROMPT 'Enter the variable value >'
```

##### SnowSQL (CLI Client)[¶](#snowsql-cli-client)

##### Command[¶](#id1)

```
!print Enter the value
!system read aux && echo '!define variable_name='"$aux" > sc_aux_file.sql
!load sc_aux_file.sql
!system rm sc_aux_file.sql
```

Warning

Note that this approach only applies to MacOs and Linux. If you want to run these queries in Windows
you may need a terminal that supports a Linux bash script language.

### Known Issues[¶](#known-issues)

No Known Issues.

### Related EWIs[¶](#related-ewis)

No related EWIs.

## Append[¶](#append)

Warning

Transformation for this command is pending

### Description[¶](#id2)

> Adds specified text to the end of the current line in the SQL buffer.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/APPEND.html#GUID-43CA6E91-0BC9-4298-8823-BDB2512FC97F))

#### Oracle Syntax[¶](#id3)

```
A[PPEND] text
```

Snowflake does not have a direct equivalent to this command. The Snowflake
[`!edit`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#edit) command can be used to
edit the last query using a predefined text editor. Whenever this approach does not cover all the
`APPPEND` functionality but it is an alternative.

#### 1. Append command[¶](#append-command)

##### Oracle[¶](#id4)

##### Command[¶](#id5)

```
APPEND SOME TEXT
```

##### SnowSQL (CLI Client)[¶](#id6)

##### Command[¶](#id7)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'APPEND STATEMENT' NODE ***/!!!
APPEND SOME TEXT;
```

### Known Issues[¶](#id8)

No Known Issues.

### Related EWIs[¶](#id9)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Archive Log[¶](#archive-log)

Warning

Transformation for this command is pending

### Description[¶](#id10)

> The `ARCHIVE LOG` command displays information about redoing log files.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/WHENEVER-OSERROR.html#GUID-A52F926F-D6EC-434E-9C7E-CFDB76422E94))

#### Oracle Syntax[¶](#id11)

```
ARCHIVE LOG LIST
```

Snowflake does not have a direct equivalent to this command. The Snowflake
[`!options`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#options-opts)command can be
used to display the location path of some log files, however, it does not fully comply with the
behavior expected by the `ARCHIVE LOG` command. At transformation time, an EWI will be added.

#### 1. Archive Log command[¶](#archive-log-command)

##### Oracle[¶](#id12)

##### Command[¶](#id13)

```
ARCHIVE LOG LIST
```

##### SnowSQL (CLI Client)[¶](#id14)

##### Command[¶](#id15)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ARCHIVE LOG STATEMENT' NODE ***/!!!
ARCHIVE LOG LIST;
```

### Known Issues[¶](#id16)

No Known Issues.

### Related EWIs[¶](#id17)

- [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
  Pending Functional Equivalence Review.

## Attribute[¶](#attribute)

Warning

Transformation for this command is pending

### Description[¶](#id18)

> The `ATTRIBUTE` command specifies display characteristics for a given attribute of an Object Type
> column.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/ATTRIBUTE.html#GUID-E37F3F55-23A9-42DD-BAA2-719BC5C5DD32))

#### Oracle Syntax[¶](#id19)

```
ATTR[IBUTE] [type_name.attribute_name [option ...]]
```

Snowflake does not have a direct equivalent to this command.

#### 1. Attribute command[¶](#attribute-command)

##### Oracle[¶](#id20)

##### Command[¶](#id21)

```
ATTRIBUTE Address.street_address FORMAT A10
```

##### SnowSQL (CLI Client)[¶](#id22)

##### Command[¶](#id23)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ATTRIBUTE STATEMENT' NODE ***/!!!
ATTRIBUTE Address.street_address FORMAT A10;
```

Warning

The code for the EWI is not defined yet.

### Known Issues[¶](#id24)

**1. SnowSQL can set the format of a column**

Currently, SnowSQL does not support custom types nor does it have a command to format columns.
However, you can use the following workaround to format columns in your query result:

```
SELECT SUBSTR(street_address, 1, 4) FROM person

SELECT TO_VARCHAR(1000.89, '$9,999.99')

SELECT to_varchar('03-Feb-2023'::DATE, 'yyyy.mm.dd');
```

This alternative solution must consider an additional strategy to disable when in Oracle the
`ATTRIBUTE` command receives the OFF option.

### Related EWIs[¶](#id25)

No related EWIs.

## Break[¶](#break)

Warning

Transformation for this command is pending

### Description[¶](#id26)

> Specifies where changes occur in a report and the formatting action to perform.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/BREAK.html))

#### Oracle Syntax[¶](#id27)

```
BRE[AK] [ON report_element [action [action]]] ...

report_element := {column|expr|ROW|REPORT}

action := [SKI[P] n|[SKI[P]] PAGE] [NODUP[LICATES]|DUP[LICATES]]
```

Snowflake does not support the use of this command and does not have any that might resemble its
functionality. At the time of transformation, an EWI will be added.

#### 1. BREAK command[¶](#break-command)

##### Oracle[¶](#id28)

##### Command[¶](#id29)

```
BREAK ON customer_age SKIP 5 DUPLICATES;
```

##### SnowSQL (CLI Client)[¶](#id30)

##### Command[¶](#id31)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BREAK STATEMENT' NODE ***/!!!
BREAK ON customer_age SKIP 5 DUPLICATES;
```

### Known Issues[¶](#id32)

No Known Issues.

### Related EWIs[¶](#id33)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Btitle[¶](#btitle)

Warning

Transformation for this command is pending

### Description[¶](#id34)

> The `BTITLE` command places and formats a specified title at the bottom of each report page, or
> lists the current BTITLE definition.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/BTITLE.html#GUID-5046ABAA-1E2B-4A91-85BB-51EC2B6BD104))

#### Oracle Syntax[¶](#id35)

```
BTI[TLE] [printspec [text | variable] ...] | [ON | OFF]
```

Snowflake does not have a direct equivalent to this command.

#### 1. Btitle command[¶](#btitle-command)

##### Oracle[¶](#id36)

##### Command[¶](#id37)

```
BTITLE BOLD 'This is the banner title'
```

##### SnowSQL (CLI Client)[¶](#id38)

##### Command[¶](#id39)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTITLE STATEMENT' NODE ***/!!!
BTITLE BOLD 'This is the banner title';
```

### Known Issues[¶](#id40)

**1. SnowSQL does not support the display of custom headers and footers in query**

Currently, SnowSQL does not support the display of custom headers and footers in query output.
However, you can use the following workaround to display header and footer information in your query
output:

```
SELECT column1,
       column2
FROM my_table;

SELECT 'This is the banner title' AS BTITLE;

--Another alternative
!print 'This is the banner title'

--To emulate BTITLE COL 5 'This is the banner title'
SELECT CONCAT(SPACE(5), 'This is the banner title');
```

This alternative solution must consider an additional strategy to disable when in Oracle the
`BTITLE` command receives the OFF option.

### Related EWIs[¶](#id41)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Change[¶](#change)

Warning

Transformation for this command is pending

### Description[¶](#id42)

> The `CHANGE` command Changes the first occurrence of the specified text on the current line in the
> buffer.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/CHANGE.html#GUID-9002CADF-74E2-427D-A404-F8019C7A2791))

#### Oracle Syntax[¶](#id43)

```
C[HANGE] sepchar old [sepchar [new [sepchar]]]
```

Snowflake does not have a direct equivalent to this command. The Snowflake
[`!edit`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#edit) command can be used to
edit the last query using a predefined text editor. Whenever this approach does not cover all the
`CHANGE` functionality but it is an alternative.

#### 1. Change command[¶](#change-command)

##### Oracle[¶](#id44)

##### Command[¶](#id45)

```
CHANGE /old/new/
```

##### SnowSQL (CLI Client)[¶](#id46)

##### Command[¶](#id47)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'CHANGE STATEMENT' NODE ***/!!!
CHANGE /old/new/;
```

### Known Issues[¶](#id48)

**1. Unsupported scenarios**

The CHANGE command can be presented in various ways, of which 2 of them are not currently supported
by the translator, these are presented below:

```
3  WHERE col_id = 1
```

Entering a line number followed by a string will replace the line regardless of the text that
follows the line number. This scenario is not supported as this does not follow the command grammar.

```
CHANGE/OLD/NEW/
```

Enter the text to replace followed by the command without using spaces. This scenario is not
supported since it does not follow the logic of tokenization by spaces.

### Related EWIs[¶](#id49)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Column[¶](#column)

Warning

Transformation for this command is pending

### Description[¶](#id50)

> The `COLUMN` command specifies display attributes for a given column.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/COLUMN.html#GUID-643B665F-B134-4A0B-88F7-10400D6D199E))

#### Oracle Syntax[¶](#id51)

```
COL[UMN] [{column | expr} [option ...]]
```

Snowflake does not support the use of this command and does not have any that might resemble its
functionality. At the time of transformation, an EWI will be added.

#### 1. Column command[¶](#column-command)

The `COLUMN` command with no clauses to list all current column display attributes.

##### Oracle[¶](#id52)

##### Command[¶](#id53)

```
COLUMN column_id ALIAS col_id NOPRINT
```

##### SnowSQL (CLI Client)[¶](#id54)

##### Command[¶](#id55)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'COLUMN STATEMENT' NODE ***/!!!
COLUMN column_id ALIAS col_id NOPRINT;
```

### Known Issues[¶](#id56)

No Known Issues.

### Related EWIs[¶](#id57)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Define[¶](#define)

Warning

Transformation for this command is pending

### Description[¶](#id58)

> The `DEFINE` command specifies a user or predefined variable and assigns a CHAR value to it, or
> lists the value and variable type of a single variable or all variables.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/DEFINE.html#GUID-72D4998C-EC2C-4FA6-9F7F-A305C407D666))

#### Oracle Syntax[¶](#id59)

```
DEF[INE] [variable] | [variable = text]
```

##### SnowSQL (CLI Client) !define[¶](#snowsql-cli-client-define)

```
!define [variable] | [variable=text]
```

**Note:**

Snowflake recommends not adding whitespace in the variable value assignment statement.

#### 1. Define with simple variable assignment[¶](#define-with-simple-variable-assignment)

Hint

This case is functionally equivalent.

The `DEFINE` command is replaced by the
[`!define`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#define) command.

##### Oracle[¶](#id60)

##### Command[¶](#id61)

```
DEFINE column_id = test

DEFINE column_id = &column_reference
```

##### SnowSQL (CLI Client)[¶](#id62)

##### Command[¶](#id63)

```
!define column_id = test

!define column_id = &column_reference
```

For referring to a previously defined variable, & is preceded by the name of the variable, if the
variable does not exist, Oracle allows its execution time assignment, however, Snowflake would throw
an error indicating the non-existence of said variable

#### 2. Define without variable assignments[¶](#define-without-variable-assignments)

Warning

This case is not functionally equivalent.

##### Oracle[¶](#id64)

##### Command[¶](#id65)

```
DEFINE column_id
```

##### SnowSQL (CLI Client)[¶](#id66)

##### Command[¶](#id67)

```
!define column_id
```

The DEFINE command used without the assignment statement is used in Oracle to show the definition of
the variable, on the other hand in Snowflake this way of using the DEFINE command would reset the
assignment of the variable, so a way to simulate the behavior presented in Oracle it is by using the
SELECT command.

This solution would be something like this:

##### Command[¶](#id68)

```
select '&column_id';
```

### Known Issues[¶](#id69)

**1. Enabling variable substitution**

To enable SnowSQL CLI to substitute values for the variables, you must set the variable_substitution
configuration option to true. This process can be done at installation, when starting a database
instance, or by running the following command:

#### Command[¶](#id70)

```
!set variable_substitution=true
```

**2. Predefined variables**

There are nine predefined variables during SQL\*Plus installation. These variables can be used later
by the user. The SnowSQL CLI client only has two predefined variables `__ROWCOUNT` and `__SFQID`.

## Host[¶](#host)

Warning

Transformation for this command is pending

### Description[¶](#id71)

> The `HOST` command executes an operating system command without leaving SQL\*Plus.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/HOST.html#GUID-E6391C3D-E87E-4BCA-B903-A4402D7E399B))

#### Oracle Syntax[¶](#id72)

```
HO[ST] [command]
```

##### SnowSQL (CLI Client) !system[¶](#snowsql-cli-client-system)

```
!system <command>
```

#### 1. Set with simple variable assignment[¶](#set-with-simple-variable-assignment)

Hint

This case is functionally equivalent.

The `HOST` command is replaced by the
[`!system`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#system) command.

##### Oracle[¶](#id73)

##### Command[¶](#id74)

```
HOST dir *.sql
```

##### SnowSQL (CLI Client)[¶](#id75)

##### Command[¶](#id76)

```
!system dir *.sql
```

### Known Issues[¶](#id77)

No Known Issues.

### Related EWIs[¶](#id78)

No related EWIs.

## Prompt[¶](#prompt)

Warning

Transformation for this command is pending

### Description[¶](#id79)

> The `PROMPT` command sends the specified message or a blank line to the user’s screen. If you omit
> a text, `PROMPT` displays a blank line on the user’s screen.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/PROMPT.html#GUID-2B2DE976-FBA5-4565-8B21-058289A16234))

#### Oracle Syntax[¶](#id80)

```
PRO[MPT] [text]
```

##### SnowSQL (CLI Client) !print[¶](#snowsql-cli-client-print)

```
!print [text]
```

#### 1. Simple print[¶](#simple-print)

The `PROMPT` command is replaced by the
[`!print`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#print) command.

Hint

This case is functionally equivalent.

##### Oracle[¶](#id81)

##### Command[¶](#id82)

```
PROMPT

PROMPT text

PROMPT db_link_name = "&1"
```

##### SnowSQL (CLI Client)[¶](#id83)

##### Command[¶](#id84)

```
!print

!print text

!print db_link_name = "&1"
```

### Known Issues[¶](#id85)

No Known Issues

### Related EWIs[¶](#id86)

No related EWIs.

## Remark[¶](#remark)

Warning

Transformation for this command is pending

### Description[¶](#id87)

> The `REMARK` command begins a comment in a script. SQL\*Plus does not interpret the comment as a
> command..
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/REMARK.html#GUID-F4BF8426-AFE4-49C9-B073-57CB91B440F8))

#### Oracle Syntax[¶](#id88)

```
REM[ARK] comment
```

Snowflake does not have a direct equivalent for this command. However, some of its functionalities
can be emulated.

#### 1. Remark after the first line[¶](#remark-after-the-first-line)

Hint

This case is functionally equivalent.

When the `REMARK` command is not at the beginning of a script you can use the standard SQL comment
markers and double hyphens.

##### Oracle[¶](#id89)

##### Command[¶](#id90)

```
SELECT 'hello world' FROM dual;
REMARK and now exit the session
EXIT;
```

##### SnowSQL (CLI Client)[¶](#id91)

##### Command[¶](#id92)

```
select 'hello world';
-- and now exit the session
!exit
```

#### 2. Remark on the first line[¶](#remark-on-the-first-line)

Warning

This case is not functionally equivalent.

When the `REMARK` command is at the beginning of a script, scenarios could appear such as:

Case 1: The next line is a query, in which case the conversion to Snowflake of the `REMARK` command
succeeds.

Case 2: The next line is another SQL\*Plus command, in which case the conversion cannot be performed
since Snowflake is not capable of executing either of the two statements (This also applies to the
scenario where there is only one statement in the script statement that corresponds to the `REMARK`
command).

Below are some examples, where the first two could not be translated correctly.

##### Oracle[¶](#id93)

##### Command[¶](#id94)

```
REMARK single line

REMARK first line
HOST dir *.sql

REMARK first line
SELECT 'hello world' FROM dual;
```

##### SnowSQL (CLI Client)[¶](#id95)

##### Command[¶](#id96)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'REMARK STATEMENT' NODE ***/!!!
REMARK single line;

!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'REMARK STATEMENT' NODE ***/!!!
REMARK first line;

!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'HOST STATEMENT' NODE ***/!!!
HOST dir *.sql;

!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'REMARK STATEMENT' NODE ***/!!!
REMARK first line;
SELECT 'hello world' FROM dual;
```

### Known Issues[¶](#id97)

No Known Issues.

### Related EWIs[¶](#id98)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Set[¶](#set)

Warning

Transformation for this command is pending

### Description[¶](#id99)

> The `SET` command sets a system variable to alter the SQL\*Plus environment settings for your
> current session.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/SET.html#GUID-9095C4FF-F4EB-4218-84AA-83061186625F))

#### Oracle Syntax[¶](#id100)

```
SET system_variable value
```

##### SnowSQL (CLI Client) !set[¶](#snowsql-cli-client-set)

```
!set <option>=<value>
```

**Note:**

Snowflake recommends not adding whitespace in the variable value assignment statement.

#### 1. Set with simple variable assignment[¶](#id101)

Hint

This case is functionally equivalent.

The `SET` command is replaced by the
[`!set`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#set) command.

##### Oracle[¶](#id102)

##### Command[¶](#id103)

```
SET wrap on
```

##### SnowSQL (CLI Client)[¶](#id104)

##### Command[¶](#id105)

```
!set wrap=true
```

#### 2. Define without variable assignments[¶](#id106)

Warning

This case is not functionally equivalent.

Oracle allows bypassing the key-value rule for assigning values to system variables with a numeric
domain, assigning the value of 0 by default in such cases. In Snowflake this is not allowed, so an
alternative is to set the value of 0 to a said variable explicitly.

##### Oracle[¶](#id107)

##### Command[¶](#id108)

```
SET pagesize
```

##### SnowSQL (CLI Client)[¶](#id109)

##### Command[¶](#id110)

```
!set rowset_size=0
```

### Known Issues[¶](#id111)

**1. Predefined variables**

The SET command only works for system variables, which may differ in quantity, name, or domain
between the two languages, so a review should be done on the variable being used within the command
to find its correct Snowflake equivalence. To see the list of system variables in Oracle you can use
the command `SHOW ALL` whereas in Snowflake you can use
[`!options`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#options-opts).

### Related EWIs[¶](#id112)

No related EWIs.

## Show[¶](#show)

Warning

Transformation for this command is pending

### Description[¶](#id113)

> Shows the value of a SQLPlus system variable or the current SQLPlus environment.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/SHOW.html#GUID-6BB1499D-E537-43D1-A209-401F5DB95E16))

#### Oracle Syntax[¶](#id114)

```
SHO[W] system_variable  ALL BTI[TLE]  CON_ID  CON_NAME EDITION  ERR[ORS] [ {ANALYTIC VIEW | ATTRIBUTE DIMENSION | HIERARCHY | FUNCTION | PROCEDURE | PACKAGE | PACKAGE BODY | TRIGGER | VIEW | TYPE | TYPE BODY | DIMENSION | JAVA CLASS } [schema.]name]HISTORY  LNO  LOBPREF[ETCH]  PARAMETER[S] [parameter_name]  PDBS PNO  RECYC[LEBIN] [original_name]  REL[EASE]  REPF[OOTER]  REPH[EADER]  ROWPREF[ETCH] SGA SPOO[L]  SPPARAMETER[S] [parameter_name]  SQLCODE STATEMENTC[ACHE] TTI[TLE] USER XQUERY
```

Snowflake does not have a direct equivalent for this command. However, some of its functionalities
can be emulated.

#### 1. Show ERRORS[¶](#show-errors)

> Shows the compilation errors of a stored procedure (includes stored functions, procedures, and
> packages). After you use the CREATE command to create a stored procedure, a message is displayed
> if the stored procedure has any compilation errors.

In Snowflake, performing an extra statement to display all the compilation errors is unnecessary.
The compilation errors are displayed immediately when executing the CREATE statement.

##### Oracle[¶](#id115)

##### Command[¶](#id116)

```
CREATE OR REPLACE PROCEDURE RANCOM_PROC
AS
BEGIN
  INSERT INTO NE_TABLE SELECT 1 FROM DUAL;
END;

SHOW ERRORS
```

##### Result[¶](#result)

```
LINE/COL ERROR
-------- -----------------------------------------------------------------
4/3      PL/SQL: SQL Statement ignored
4/10     PL/SQL: ORA-00925: missing INTO keyword
```

**Note:**

Note that the INTO keyword is misspelled in order to cause a compilation error.

##### SnowSQL (CLI Client)[¶](#id117)

##### Command[¶](#id118)

```
CREATE OR REPLACE PROCEDURE RANCOM_PROC ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    INSERT INTO NE_TABLE
    SELECT 1 FROM DUAL;
  END;
$$;

!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SHOW STATEMENT' NODE ***/!!!

SHOW ERRORS;
```

##### Result[¶](#id119)

```
001003 (42000): SQL compilation error:
syntax error line 3 at position 7 unexpected 'INT'.
syntax error line 3 at position 11 unexpected 'PUBLIC'.
```

#### Show ALL[¶](#show-all)

> Lists the settings of all SHOW options, except ERRORS and SGA, in alphabetical order.

In order to display all the possible options in SnowCLI you can run the
[`!options`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#options-opts) command.

##### Oracle[¶](#id120)

##### Command[¶](#id121)

```
show all;
```

##### Result[¶](#id122)

```
appinfo is OFF and set to "SQL*Plus"
arraysize 15
autocommit OFF
autoprint OFF
autorecovery OFF
autotrace OFF
blockterminator "." (hex 2e)
btitle OFF and is the first few characters of the next SELECT statement
cmdsep OFF
colinvisible OFF
coljson OFF
colsep " "
compatibility version NATIVE
concat "." (hex 2e)
copycommit 0
COPYTYPECHECK is ON
define "&" (hex 26)
describe DEPTH 1 LINENUM OFF INDENT ON
echo OFF
editfile "afiedt.buf"
embedded OFF
errorlogging is OFF
escape OFF
escchar OFF
exitcommit ON
FEEDBACK ON for 6 or more rows SQL_ID OFF
flagger OFF
flush ON
fullcolname OFF
heading ON
headsep "|" (hex 7c)
history is OFF
instance "local"
jsonprint NORMAL
linesize 80
lno 5
loboffset 1
lobprefetch 0
logsource ""
long 80
longchunksize 80
markup HTML OFF HEAD "<style type='text/css'> body {font:10pt Arial,Helvetica,sans-serif; color:black; background:White;} p {font:10pt Arial,Helvetica,sans-serif; color:black; background:White;} table,tr,td {font:10pt Arial,Helvetica,sans-serif; color:Black; background:#f7f7e7; padding:0px 0px 0px 0px; margin:0px 0px 0px 0px;} th {font:bold 10pt Arial,Helvetica,sans-serif; color:#336699; background:#cccc99; padding:0px 0px 0px 0px;} h1 {font:16pt Arial,Helvetica,Geneva,sans-serif; color:#336699; background-color:White; border-bottom:1px solid #cccc99; margin-top:0pt; margin-bottom:0pt; padding:0px 0px 0px 0px;-
} h2 {font:bold 10pt Arial,Helvetica,Geneva,sans-serif; color:#336699; background-color:White; margin-top:4pt; margin-bottom:0pt;} a {font:9pt Arial,Helvetica,sans-serif; color:#663300; background:#ffffff; margin-top:0pt; margin-bottom:0pt; vertical-align:top;}</style><title>SQL*Plus Report</title>" BODY "" TABLE "border='1' width='90%' align='center' summary='Script output'" SPOOL OFF ENTMAP ON PREFORMAT OFF
markup CSV OFF DELIMITER , QUOTE ON
newpage 1
null ""
numformat ""
numwidth 10
pagesize 14
PAUSE is OFF
pno 1
recsep WRAP
recsepchar " " (hex 20)
release 2103000000
repfooter OFF and is NULL
repheader OFF and is NULL
rowlimit OFF
rowprefetch 1
securedcol is OFF
serveroutput OFF
shiftinout INVISIBLE
showmode OFF
spool OFF
sqlblanklines OFF
sqlcase MIXED
sqlcode 0
sqlcontinue "> "
sqlnumber ON
sqlpluscompatibility 21.0.0
sqlprefix "#" (hex 23)
sqlprompt "SQL> "
sqlterminator ";" (hex 3b)
statementcache is 0
suffix "sql"
tab ON
termout ON
timing OFF
trimout ON
trimspool OFF
ttitle OFF and is the first few characters of the next SELECT statement
underline "-" (hex 2d)
USER is "SYSTEM"
verify ON
wrap : lines will be wrapped
xmloptimizationcheck OFF
```

##### SnowSQL (CLI Client)[¶](#id123)

##### Command[¶](#id124)

```
!options
```

##### Result[¶](#id125)

<!-- prettier-ignore -->
|Name|Value|Help|
|---|---|---|
|auto_completion|True|Displays auto-completion suggestions for commands and Snowflake objects|
|client_session_keep_alive|False|Keeps the session active indefinitely, even if there is no activity from the user.|
|client_store_temporary_credential|False|Enable Linux users to use temporary file to store ID_TOKEN.|
|connection_options|{}|Set arbitrary connection parameters in underlying Python connector connections.|
|echo|False|Outputs the SQL command to the terminal when it is executed|
|editor|vim|Changes the editor to use for the !edit command|
|empty_for_null_in_tsv|False|Outputs an empty string for NULL values in TSV format|
|environment_variables|[]|Specifies the environment variables to be set in the SnowSQL variables.|
|||The variable names should be comma separated.|
|execution_only|False|Executes queries only. No data will be fetched|
|exit_on_error|False|Quits when SnowSQL encounters an error|
|fix_parameter_precedence|True|Fix the connection parameter precedence in the order of 1) Environment variables, 2) Connection parameters, 3) Default connection parameters.|
|force_put_overwrite|False|Forces OVERWRITE=true for PUT. This is to mitigate S3’s eventually consistent issue.|
|friendly|True|Shows the splash text and goodbye messages|
|header|True|Outputs the header in query results|
|insecure_mode|False|Turns off OSCP certificate checks|
|key_bindings|emacs|Changes keybindings for navigating the prompt to emacs or vi|
|log_bootstrap_file|../snowsql_rt.log_bo..|SnowSQL bootstrap log file location|
|log_file|../snowsql_rt.log|SnowSQL main log file location|
|log_level|DEBUG|Changes the log level (critical, debug, info, error, warning)|
|login_timeout|120|Login timeout in seconds.|
|noup|False|Turns off auto upgrading Snowsql|
|ocsp_fail_open|True|Sets the fail open mode for OCSP Failures. For help please refer the documentation.|
|output_file|None|Writes output to the specified file in addition to the terminal|
|output_format|psql|Sets the output format for query results.|
|paging|False|Enables paging to pause output per screen height.|
|progress_bar|True|Shows progress bar while transferring data.|
|prompt_format|[user]#[warehouse]@[..|Sets the prompt format. For help, see the documentation|
|quiet|False|Hides all output|
|remove_comments|False|Removes comments before sending query to Snowflake|
|remove_trailing_semicolons|False|Removes trailing semicolons from SQL text before sending queries to Snowflake|
|results|True|If set to off, queries will be sent asynchronously, but no results will be fetched.|
|||Use !queries to check the status.|
|rowset_size|1000|Sets the size of rowsets to fetch from the server.|
|||Set the option low for smooth output, high for fast output.|
|sfqid|False|Turns on/off Snowflake query id in the summary.|
|sfqid_in_error|False|Turns on/off Snowflake query id in the error message|
|sql_delimiter|;|Defines what reserved keyword splits SQL statements from each other.|
|sql_split|snowflake.connector…|Choose SQL spliter implementation. Currently snowflake.connector.util_text, or snowflake.cli.sqlsplit.|
|stop_on_error|False|Stops all queries yet to run when SnowSQL encounters an error|
|syntax_style|default|Sets the colors for the text of SnowSQL.|
|timing|True|Turns on/off timing for each query|
|timing_in_output_file|False|Includes timing in the output file.|
|variable_substitution|False|Substitutes variables (starting with ‘&’) with values|
|version|1.2.24|SnowSQL version|
|wrap|True|Truncates lines at the width of the terminal screen|
|———————————–|————————|———————————————————————————————————————————————–|

### Known Issues[¶](#id126)

**1. It’s not possible in SnowCLI to display de value of a single option.**

SnowCLI does not provide a way to display the value of a specific option. You may use `!options` to
watch the value of the option.

**2. Research is pending to match each SQLPLUS option to a SnowflakeCLI equivalent.**

It is pending to define an equivalent for each SQLPLUS option.

### Related EWIs[¶](#id127)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Spool[¶](#spool)

Warning

Transformation for this command is pending

### Description[¶](#id128)

> The `SPOOL` command stores query results in a file, or optionally sends the file to a printer.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/SPOOL.html#GUID-61492052-ECCB-45C8-AF94-AB9794C60BEA))

#### Oracle Syntax[¶](#id129)

```
SPO[OL] [file_name[.ext] [CRE[ATE] | REP[LACE] | APP[END]] | OFF | OUT]
```

##### SnowSQL (CLI Client) !spool[¶](#snowsql-cli-client-spool)

```
!spool [<file_name>] | [off]
```

#### 1. Spool without options[¶](#spool-without-options)

Hint

This case is functionally equivalent.

When the `SPOOL` command is not accompanied by any option, by default it creates a new file with the
specified name and extension. The `SPOOL` command is replaced by the
[`!spool`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#spool) command.

##### Oracle[¶](#id130)

##### Command[¶](#id131)

```
SPOOL temp
SPOOL temp.txt
```

##### SnowSQL (CLI Client)[¶](#id132)

##### Command[¶](#id133)

```
!spool temp
!spool temp.txt
```

#### 2. Spool with write options[¶](#spool-with-write-options)

Warning

This case is not functionally equivalent.

Oracle allows 3 types of options when writing to a file through the `SPOOL` command, the CREATE and
APPEND options create a file for writing from scratch and concatenate text to the end of an existing
file (or create a new one if it doesn’t exist) respectively. Snowflake does not support these
options, however, its default behavior is to create a file and if it exists, concatenate the text in
it. The REPLACE option, on the other hand, writes to the specific file replacing the existing
content. To simulate this behavior in Snowflake it is recommended to delete the file where you want
to write and start writing again, as shown in the following code

##### Oracle[¶](#id134)

##### Command[¶](#id135)

```
SPOOL temp.txt CREATE
SPOOL temp.txt APPEND
SPOOL temp.txt REPLACE
```

##### SnowSQL (CLI Client)[¶](#id136)

##### Command[¶](#id137)

```
!spool temp.txt
!spool temp.txt

!system del temp.txt
!spool temp.txt
```

#### 3. Spool turn off[¶](#spool-turn-off)

Hint

This case is functionally equivalent.

Oracle has two options to turn off results spooling, OFF and OUT. both are meant to stop rolling,
with the difference that the second also sends the file to the computer’s standard (default)
printer. This option is not available on some operating systems. Snowflake only has the option to
turn off results spooling

##### Oracle[¶](#id138)

##### Command[¶](#id139)

```
SPOOL OFF
SPOOL OUT
```

##### SnowSQL (CLI Client)[¶](#id140)

##### Command[¶](#id141)

```
!spool off
!spool off
```

### Known Issues[¶](#id142)

No Known Issues.

### Related EWIs[¶](#id143)

No related EWIs.

## Start[¶](#start)

Warning

Transformation for this command is pending

### Description[¶](#id144)

> The `START` command runs the SQL\*Plus statements in the specified script. The script can be
> called from the local file system or from a web server.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/START.html#GUID-A8D3613E-A141-42FB-8288-654427BAB28F))

#### Oracle Syntax[¶](#id145)

```
STA[RT] {url | file_name[.ext] } [arg...]
```

##### SnowSQL (CLI Client) !load[¶](#snowsql-cli-client-load)

```
!(load | source) {url | file_name[.ext] }
```

The Snowflake [`!source`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#source-load) and
[`!load`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#source-load) commands are
equivalent.

#### 1. Simple start[¶](#simple-start)

The `START` command is replaced by the
[`!load`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#source-load) command.

Hint

This case is functionally equivalent.

##### Oracle[¶](#id146)

##### Command[¶](#id147)

```
START C:\Users\My_User\Desktop\My\Path\insert_script.sql
```

##### SnowSQL (CLI Client)[¶](#id148)

##### Command[¶](#id149)

```
!load C:\Users\My_User\Desktop\My\Path\insert_script.sql
```

#### 2. Start with arguments[¶](#start-with-arguments)

##### Oracle[¶](#id150)

##### Command[¶](#id151)

```
START C:\Users\My_User\Desktop\My\Path\insert_script.sql 123 456 789
```

##### SnowSQL (CLI Client)[¶](#id152)

##### Command[¶](#id153)

```
!load C:\Users\My_User\Desktop\My\Path\insert_script.sql
```

Warning

Script arguments are currently not supported for SnowSQL (CLI Client).

### Known Issues[¶](#id154)

**1. Arguments are not supported in the SnowSQL CLI Client**

Oracle can pass down multiple arguments to a script and can be accessed with &1, &2, and so on, but
this cannot be done in the SnowSQL CLI Client. You can simulate arguments by declaring variables
with the `!define` command. Keep in mind that these values are defined globally for all the scripts
so the behavior may not be equivalent.

This workaround would look something like this:

```
!set variable_substitution=true
!define 1=123
!define 2=456
!define 3=789
!load C:\Users\My_User\Desktop\My\Path\insert_script.sql
```

### Related EWIs[¶](#id155)

No related EWIs.

## Whenever oserror[¶](#whenever-oserror)

Warning

Transformation for this command is pending

### Description[¶](#id156)

> The `WHENEVER OSERROR` command Performs the specified action (exits SQL\*Plus by default) if an
> operating system error occurs.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/WHENEVER-OSERROR.html#GUID-A52F926F-D6EC-434E-9C7E-CFDB76422E94))

#### Oracle Syntax[¶](#id157)

```
WHENEVER OSERROR {EXIT [SUCCESS | FAILURE | n | variable | :BindVariable]  [COMMIT | ROLLBACK] | CONTINUE [COMMIT | ROLLBACK | NONE]}
```

Snowflake does not support the use of this command and does not have any that might resemble its
functionality. At the time of transformation, an EWI will be added.

#### 1. Whenever oserror command[¶](#whenever-oserror-command)

##### Oracle[¶](#id158)

##### Command[¶](#id159)

```
WHENEVER OSERROR EXIT
```

##### SnowSQL (CLI Client)[¶](#id160)

##### Command[¶](#id161)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'WHENEVER ERROR STATEMENT' NODE ***/!!!
WHENEVER OSERROR EXIT;
```

### Known Issues[¶](#id162)

No Known Issues.

### Related EWIs[¶](#id163)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Whenever sqlerror[¶](#whenever-sqlerror)

Warning

Transformation for this command is pending

### Description[¶](#id164)

> The `WHENEVER SQLERROR` command Performs the specified action (exits SQL\*Plus by default) if a
> SQL command or PL/SQL block generates an error.
> ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/WHENEVER-SQLERROR.html#GUID-66C1C12C-5E95-4440-A37B-7CCE7E33491C))

#### Oracle Syntax[¶](#id165)

```
WHENEVER SQLERROR {EXIT [SUCCESS | FAILURE | WARNING | n | variable  | :BindVariable] [COMMIT | ROLLBACK] | CONTINUE [COMMIT | ROLLBACK | NONE]}
```

Snowflake does not support the use of this command and does not have any that might resemble its
functionality. At the time of transformation, an EWI will be added.

#### 1. Whenever sqlerror command[¶](#whenever-sqlerror-command)

##### Oracle[¶](#id166)

##### Command[¶](#id167)

```
WHENEVER SQLERROR EXIT
```

##### SnowSQL (CLI Client)[¶](#id168)

##### Command[¶](#id169)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'WHENEVER ERROR STATEMENT' NODE ***/!!!
WHENEVER SQLERROR EXIT;
```

### Known Issues[¶](#id170)

No Known Issues.

### Related EWIs[¶](#id171)

1. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
