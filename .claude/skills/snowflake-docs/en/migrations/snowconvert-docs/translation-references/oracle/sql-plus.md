---
auto_generated: true
description: This is a translation reference to convert SQL Plus statements to SnowSQL
  (CLI Client)
last_scraped: '2026-01-14T16:53:27.052125+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-plus
title: SnowConvert AI - Oracle - SQL*Plus | Snowflake Documentation
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
          + [Oracle](README.md)

            - [Sample Data](sample-data.md)
            - Basic Elements of Oracle SQL

              - [Literals](basic-elements-of-oracle-sql/literals.md)
              - [Data Types](basic-elements-of-oracle-sql/data-types/README.md)
            - [Pseudocolumns](pseudocolumns.md)
            - [Built-in Functions](functions/README.md)
            - [Built-in Packages](built-in-packages.md)
            - [SQL Queries and Subqueries](sql-queries-and-subqueries/selects.md)
            - [SQL Statements](sql-translation-reference/README.md)
            - [PL/SQL to Snowflake Scripting](pl-sql-to-snowflake-scripting/README.md)
            - [PL/SQL to Javascript](pl-sql-to-javascript/README.md)
            - [SQL Plus](sql-plus.md)
            - [Wrapped Objects](wrapped-objects.md)
            - ETL And BI Repointing

              - [Power BI Oracle Repointing](etl-bi-repointing/power-bi-oracle-repointing.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Oracle](README.md)SQL Plus

# SnowConvert AI - Oracle - SQL\*Plus[¶](#snowconvert-ai-oracle-sql-plus "Link to this heading")

This is a translation reference to convert SQL Plus statements to SnowSQL (CLI Client)

## Accept[¶](#accept "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#description "Link to this heading")

> Reads a line of input and stores it in a given substitution variable.. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/ACCEPT.html#GUID-5D07E526-202B-429B-9E0C-005D1E37BBAB))

#### Oracle Syntax[¶](#oracle-syntax "Link to this heading")

```
ACC[EPT] variable [NUM[BER] | CHAR | DATE | BINARY_FLOAT | BINARY_DOUBLE] [FOR[MAT] format] [DEF[AULT] default] [PROMPT text|NOPR[OMPT]] [HIDE]
```

Copy

Snowflake does not have a direct equivalent to this command. In order to emulate this functionality, the SnowCLI`!system` command will be used by taking advantage of the system resources for the input operations.

#### 1. Accept command[¶](#accept-command "Link to this heading")

##### Oracle[¶](#oracle "Link to this heading")

##### Command[¶](#command "Link to this heading")

```
ACCEPT variable_name CHAR PROMPT 'Enter the variable value >'
```

Copy

##### SnowSQL (CLI Client)[¶](#snowsql-cli-client "Link to this heading")

##### Command[¶](#id1 "Link to this heading")

```
!print Enter the value
!system read aux && echo '!define variable_name='"$aux" > sc_aux_file.sql 
!load sc_aux_file.sql
!system rm sc_aux_file.sql
```

Copy

Warning

Note that this approach only applies to MacOs and Linux. If you want to run these queries in Windows you may need a terminal that supports a Linux bash script language.

### Known Issues[¶](#known-issues "Link to this heading")

No Known Issues.

### Related EWIs[¶](#related-ewis "Link to this heading")

No related EWIs.

## Append[¶](#append "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id2 "Link to this heading")

> Adds specified text to the end of the current line in the SQL buffer. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/APPEND.html#GUID-43CA6E91-0BC9-4298-8823-BDB2512FC97F))

#### Oracle Syntax[¶](#id3 "Link to this heading")

```
A[PPEND] text
```

Copy

Snowflake does not have a direct equivalent to this command. The Snowflake [`!edit`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#edit) command can be used to edit the last query using a predefined text editor. Whenever this approach does not cover all the `APPPEND` functionality but it is an alternative.

#### 1. Append command[¶](#append-command "Link to this heading")

##### Oracle[¶](#id4 "Link to this heading")

##### Command[¶](#id5 "Link to this heading")

```
APPEND SOME TEXT
```

Copy

##### SnowSQL (CLI Client)[¶](#id6 "Link to this heading")

##### Command[¶](#id7 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'APPEND STATEMENT' NODE ***/!!!
APPEND SOME TEXT;
```

Copy

### Known Issues[¶](#id8 "Link to this heading")

No Known Issues.

### Related EWIs[¶](#id9 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Archive Log[¶](#archive-log "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id10 "Link to this heading")

> The `ARCHIVE LOG` command displays information about redoing log files. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/WHENEVER-OSERROR.html#GUID-A52F926F-D6EC-434E-9C7E-CFDB76422E94))

#### Oracle Syntax[¶](#id11 "Link to this heading")

```
ARCHIVE LOG LIST
```

Copy

Snowflake does not have a direct equivalent to this command. The Snowflake [`!options`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#options-opts)command can be used to display the location path of some log files, however, it does not fully comply with the behavior expected by the `ARCHIVE LOG` command. At transformation time, an EWI will be added.

#### 1. Archive Log command[¶](#archive-log-command "Link to this heading")

##### Oracle[¶](#id12 "Link to this heading")

##### Command[¶](#id13 "Link to this heading")

```
ARCHIVE LOG LIST
```

Copy

##### SnowSQL (CLI Client)[¶](#id14 "Link to this heading")

##### Command[¶](#id15 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ARCHIVE LOG STATEMENT' NODE ***/!!!
ARCHIVE LOG LIST;
```

Copy

### Known Issues[¶](#id16 "Link to this heading")

No Known Issues.

### Related EWIs[¶](#id17 "Link to this heading")

* [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Attribute[¶](#attribute "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id18 "Link to this heading")

> The `ATTRIBUTE` command specifies display characteristics for a given attribute of an Object Type column. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/ATTRIBUTE.html#GUID-E37F3F55-23A9-42DD-BAA2-719BC5C5DD32))

#### Oracle Syntax[¶](#id19 "Link to this heading")

```
ATTR[IBUTE] [type_name.attribute_name [option ...]]
```

Copy

Snowflake does not have a direct equivalent to this command.

#### 1. Attribute command[¶](#attribute-command "Link to this heading")

##### Oracle[¶](#id20 "Link to this heading")

##### Command[¶](#id21 "Link to this heading")

```
ATTRIBUTE Address.street_address FORMAT A10
```

Copy

##### SnowSQL (CLI Client)[¶](#id22 "Link to this heading")

##### Command[¶](#id23 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ATTRIBUTE STATEMENT' NODE ***/!!!
ATTRIBUTE Address.street_address FORMAT A10;
```

Copy

Warning

The code for the EWI is not defined yet.

### Known Issues[¶](#id24 "Link to this heading")

**1. SnowSQL can set the format of a column**

Currently, SnowSQL does not support custom types nor does it have a command to format columns. However, you can use the following workaround to format columns in your query result:

```
SELECT SUBSTR(street_address, 1, 4) FROM person

SELECT TO_VARCHAR(1000.89, '$9,999.99')

SELECT to_varchar('03-Feb-2023'::DATE, 'yyyy.mm.dd');
```

Copy

This alternative solution must consider an additional strategy to disable when in Oracle the `ATTRIBUTE` command receives the OFF option.

### Related EWIs[¶](#id25 "Link to this heading")

No related EWIs.

## Break[¶](#break "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id26 "Link to this heading")

> Specifies where changes occur in a report and the formatting action to perform. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/BREAK.html))

#### Oracle Syntax[¶](#id27 "Link to this heading")

```
BRE[AK] [ON report_element [action [action]]] ...

report_element := {column|expr|ROW|REPORT}

action := [SKI[P] n|[SKI[P]] PAGE] [NODUP[LICATES]|DUP[LICATES]]
```

Copy

Snowflake does not support the use of this command and does not have any that might resemble its functionality. At the time of transformation, an EWI will be added.

#### 1. BREAK command[¶](#break-command "Link to this heading")

##### Oracle[¶](#id28 "Link to this heading")

##### Command[¶](#id29 "Link to this heading")

```
BREAK ON customer_age SKIP 5 DUPLICATES;
```

Copy

##### SnowSQL (CLI Client)[¶](#id30 "Link to this heading")

##### Command[¶](#id31 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BREAK STATEMENT' NODE ***/!!!
BREAK ON customer_age SKIP 5 DUPLICATES;
```

Copy

### Known Issues[¶](#id32 "Link to this heading")

No Known Issues.

### Related EWIs[¶](#id33 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Btitle[¶](#btitle "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id34 "Link to this heading")

> The `BTITLE` command places and formats a specified title at the bottom of each report page, or lists the current BTITLE definition. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/BTITLE.html#GUID-5046ABAA-1E2B-4A91-85BB-51EC2B6BD104))

#### Oracle Syntax[¶](#id35 "Link to this heading")

```
BTI[TLE] [printspec [text | variable] ...] | [ON | OFF]
```

Copy

Snowflake does not have a direct equivalent to this command.

#### 1. Btitle command[¶](#btitle-command "Link to this heading")

##### Oracle[¶](#id36 "Link to this heading")

##### Command[¶](#id37 "Link to this heading")

```
BTITLE BOLD 'This is the banner title'
```

Copy

##### SnowSQL (CLI Client)[¶](#id38 "Link to this heading")

##### Command[¶](#id39 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'BTITLE STATEMENT' NODE ***/!!!
BTITLE BOLD 'This is the banner title';
```

Copy

### Known Issues[¶](#id40 "Link to this heading")

**1. SnowSQL does not support the display of custom headers and footers in query**

Currently, SnowSQL does not support the display of custom headers and footers in query output. However, you can use the following workaround to display header and footer information in your query output:

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

Copy

This alternative solution must consider an additional strategy to disable when in Oracle the `BTITLE` command receives the OFF option.

### Related EWIs[¶](#id41 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Change[¶](#change "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id42 "Link to this heading")

> The `CHANGE` command Changes the first occurrence of the specified text on the current line in the buffer. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/CHANGE.html#GUID-9002CADF-74E2-427D-A404-F8019C7A2791))

#### Oracle Syntax[¶](#id43 "Link to this heading")

```
C[HANGE] sepchar old [sepchar [new [sepchar]]]
```

Copy

Snowflake does not have a direct equivalent to this command. The Snowflake [`!edit`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#edit) command can be used to edit the last query using a predefined text editor. Whenever this approach does not cover all the `CHANGE` functionality but it is an alternative.

#### 1. Change command[¶](#change-command "Link to this heading")

##### Oracle[¶](#id44 "Link to this heading")

##### Command[¶](#id45 "Link to this heading")

```
CHANGE /old/new/
```

Copy

##### SnowSQL (CLI Client)[¶](#id46 "Link to this heading")

##### Command[¶](#id47 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'CHANGE STATEMENT' NODE ***/!!!
CHANGE /old/new/;
```

Copy

### Known Issues[¶](#id48 "Link to this heading")

**1. Unsupported scenarios**

The CHANGE command can be presented in various ways, of which 2 of them are not currently supported by the translator, these are presented below:

```
3  WHERE col_id = 1
```

Copy

Entering a line number followed by a string will replace the line regardless of the text that follows the line number. This scenario is not supported as this does not follow the command grammar.

```
CHANGE/OLD/NEW/
```

Copy

Enter the text to replace followed by the command without using spaces. This scenario is not supported since it does not follow the logic of tokenization by spaces.

### Related EWIs[¶](#id49 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Column[¶](#column "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id50 "Link to this heading")

> The `COLUMN` command specifies display attributes for a given column. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/COLUMN.html#GUID-643B665F-B134-4A0B-88F7-10400D6D199E))

#### Oracle Syntax[¶](#id51 "Link to this heading")

```
COL[UMN] [{column | expr} [option ...]]
```

Copy

Snowflake does not support the use of this command and does not have any that might resemble its functionality. At the time of transformation, an EWI will be added.

#### 1. Column command[¶](#column-command "Link to this heading")

The `COLUMN` command with no clauses to list all current column display attributes.

##### Oracle[¶](#id52 "Link to this heading")

##### Command[¶](#id53 "Link to this heading")

```
COLUMN column_id ALIAS col_id NOPRINT
```

Copy

##### SnowSQL (CLI Client)[¶](#id54 "Link to this heading")

##### Command[¶](#id55 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'COLUMN STATEMENT' NODE ***/!!!
COLUMN column_id ALIAS col_id NOPRINT;
```

Copy

### Known Issues[¶](#id56 "Link to this heading")

No Known Issues.

### Related EWIs[¶](#id57 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Define[¶](#define "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id58 "Link to this heading")

> The `DEFINE` command specifies a user or predefined variable and assigns a CHAR value to it, or lists the value and variable type of a single variable or all variables. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/DEFINE.html#GUID-72D4998C-EC2C-4FA6-9F7F-A305C407D666))

#### Oracle Syntax[¶](#id59 "Link to this heading")

```
DEF[INE] [variable] | [variable = text]
```

Copy

##### SnowSQL (CLI Client) !define[¶](#snowsql-cli-client-define "Link to this heading")

```
!define [variable] | [variable=text]
```

Copy

Note

Snowflake recommends not adding whitespace in the variable value assignment statement.

#### 1. Define with simple variable assignment[¶](#define-with-simple-variable-assignment "Link to this heading")

Hint

This case is functionally equivalent.

The `DEFINE` command is replaced by the [`!define`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#define) command.

##### Oracle[¶](#id60 "Link to this heading")

##### Command[¶](#id61 "Link to this heading")

```
DEFINE column_id = test

DEFINE column_id = &column_reference
```

Copy

##### SnowSQL (CLI Client)[¶](#id62 "Link to this heading")

##### Command[¶](#id63 "Link to this heading")

```
!define column_id = test

!define column_id = &column_reference
```

Copy

For referring to a previously defined variable, & is preceded by the name of the variable, if the variable does not exist, Oracle allows its execution time assignment, however, Snowflake would throw an error indicating the non-existence of said variable

#### 2. Define without variable assignments[¶](#define-without-variable-assignments "Link to this heading")

Warning

This case is not functionally equivalent.

##### Oracle[¶](#id64 "Link to this heading")

##### Command[¶](#id65 "Link to this heading")

```
DEFINE column_id
```

Copy

##### SnowSQL (CLI Client)[¶](#id66 "Link to this heading")

##### Command[¶](#id67 "Link to this heading")

```
!define column_id
```

Copy

The DEFINE command used without the assignment statement is used in Oracle to show the definition of the variable, on the other hand in Snowflake this way of using the DEFINE command would reset the assignment of the variable, so a way to simulate the behavior presented in Oracle it is by using the SELECT command.

This solution would be something like this:

##### Command[¶](#id68 "Link to this heading")

```
select '&column_id';
```

Copy

### Known Issues[¶](#id69 "Link to this heading")

**1. Enabling variable substitution**

To enable SnowSQL CLI to substitute values for the variables, you must set the variable\_substitution configuration option to true. This process can be done at installation, when starting a database instance, or by running the following command:

#### Command[¶](#id70 "Link to this heading")

```
!set variable_substitution=true
```

Copy

**2. Predefined variables**

There are nine predefined variables during SQL\*Plus installation. These variables can be used later by the user. The SnowSQL CLI client only has two predefined variables `__ROWCOUNT` and `__SFQID`.

## Host[¶](#host "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id71 "Link to this heading")

> The `HOST` command executes an operating system command without leaving SQL\*Plus. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/HOST.html#GUID-E6391C3D-E87E-4BCA-B903-A4402D7E399B))

#### Oracle Syntax[¶](#id72 "Link to this heading")

```
HO[ST] [command]
```

Copy

##### SnowSQL (CLI Client) !system[¶](#snowsql-cli-client-system "Link to this heading")

```
!system <command>
```

Copy

#### 1. Set with simple variable assignment[¶](#set-with-simple-variable-assignment "Link to this heading")

Hint

This case is functionally equivalent.

The `HOST` command is replaced by the [`!system`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#system) command.

##### Oracle[¶](#id73 "Link to this heading")

##### Command[¶](#id74 "Link to this heading")

```
HOST dir *.sql
```

Copy

##### SnowSQL (CLI Client)[¶](#id75 "Link to this heading")

##### Command[¶](#id76 "Link to this heading")

```
!system dir *.sql
```

Copy

### Known Issues[¶](#id77 "Link to this heading")

No Known Issues.

### Related EWIs[¶](#id78 "Link to this heading")

No related EWIs.

## Prompt[¶](#prompt "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id79 "Link to this heading")

> The `PROMPT` command sends the specified message or a blank line to the user’s screen. If you omit a text, `PROMPT` displays a blank line on the user’s screen. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/PROMPT.html#GUID-2B2DE976-FBA5-4565-8B21-058289A16234))

#### Oracle Syntax[¶](#id80 "Link to this heading")

```
PRO[MPT] [text]
```

Copy

##### SnowSQL (CLI Client) !print[¶](#snowsql-cli-client-print "Link to this heading")

```
!print [text]
```

Copy

#### 1. Simple print[¶](#simple-print "Link to this heading")

The `PROMPT` command is replaced by the [`!print`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#print) command.

Hint

This case is functionally equivalent.

##### Oracle[¶](#id81 "Link to this heading")

##### Command[¶](#id82 "Link to this heading")

```
PROMPT

PROMPT text

PROMPT db_link_name = "&1"
```

Copy

##### SnowSQL (CLI Client)[¶](#id83 "Link to this heading")

##### Command[¶](#id84 "Link to this heading")

```
!print

!print text

!print db_link_name = "&1"
```

Copy

### Known Issues[¶](#id85 "Link to this heading")

No Known Issues

### Related EWIs[¶](#id86 "Link to this heading")

No related EWIs.

## Remark[¶](#remark "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id87 "Link to this heading")

> The `REMARK` command begins a comment in a script. SQL\*Plus does not interpret the comment as a command.. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/REMARK.html#GUID-F4BF8426-AFE4-49C9-B073-57CB91B440F8))

#### Oracle Syntax[¶](#id88 "Link to this heading")

```
REM[ARK] comment
```

Copy

Snowflake does not have a direct equivalent for this command. However, some of its functionalities can be emulated.

#### 1. Remark after the first line[¶](#remark-after-the-first-line "Link to this heading")

Hint

This case is functionally equivalent.

When the `REMARK` command is not at the beginning of a script you can use the standard SQL comment markers and double hyphens.

##### Oracle[¶](#id89 "Link to this heading")

##### Command[¶](#id90 "Link to this heading")

```
SELECT 'hello world' FROM dual;
REMARK and now exit the session
EXIT;
```

Copy

##### SnowSQL (CLI Client)[¶](#id91 "Link to this heading")

##### Command[¶](#id92 "Link to this heading")

```
select 'hello world';
-- and now exit the session
!exit
```

Copy

#### 2. Remark on the first line[¶](#remark-on-the-first-line "Link to this heading")

Warning

This case is not functionally equivalent.

When the `REMARK` command is at the beginning of a script, scenarios could appear such as:

Case 1: The next line is a query, in which case the conversion to Snowflake of the `REMARK` command succeeds.

Case 2: The next line is another SQL\*Plus command, in which case the conversion cannot be performed since Snowflake is not capable of executing either of the two statements (This also applies to the scenario where there is only one statement in the script statement that corresponds to the `REMARK` command).

Below are some examples, where the first two could not be translated correctly.

##### Oracle[¶](#id93 "Link to this heading")

##### Command[¶](#id94 "Link to this heading")

```
REMARK single line

REMARK first line
HOST dir *.sql

REMARK first line
SELECT 'hello world' FROM dual;
```

Copy

##### SnowSQL (CLI Client)[¶](#id95 "Link to this heading")

##### Command[¶](#id96 "Link to this heading")

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

Copy

### Known Issues[¶](#id97 "Link to this heading")

No Known Issues.

### Related EWIs[¶](#id98 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Set[¶](#set "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id99 "Link to this heading")

> The `SET` command sets a system variable to alter the SQL\*Plus environment settings for your current session. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/SET.html#GUID-9095C4FF-F4EB-4218-84AA-83061186625F))

#### Oracle Syntax[¶](#id100 "Link to this heading")

```
SET system_variable value
```

Copy

##### SnowSQL (CLI Client) !set[¶](#snowsql-cli-client-set "Link to this heading")

```
!set <option>=<value>
```

Copy

Note

Snowflake recommends not adding whitespace in the variable value assignment statement.

#### 1. Set with simple variable assignment[¶](#id101 "Link to this heading")

Hint

This case is functionally equivalent.

The `SET` command is replaced by the [`!set`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#set) command.

##### Oracle[¶](#id102 "Link to this heading")

##### Command[¶](#id103 "Link to this heading")

```
SET wrap on
```

Copy

##### SnowSQL (CLI Client)[¶](#id104 "Link to this heading")

##### Command[¶](#id105 "Link to this heading")

```
!set wrap=true
```

Copy

#### 2. Define without variable assignments[¶](#id106 "Link to this heading")

Warning

This case is not functionally equivalent.

Oracle allows bypassing the key-value rule for assigning values to system variables with a numeric domain, assigning the value of 0 by default in such cases. In Snowflake this is not allowed, so an alternative is to set the value of 0 to a said variable explicitly.

##### Oracle[¶](#id107 "Link to this heading")

##### Command[¶](#id108 "Link to this heading")

```
SET pagesize
```

Copy

##### SnowSQL (CLI Client)[¶](#id109 "Link to this heading")

##### Command[¶](#id110 "Link to this heading")

```
!set rowset_size=0
```

Copy

### Known Issues[¶](#id111 "Link to this heading")

**1. Predefined variables**

The SET command only works for system variables, which may differ in quantity, name, or domain between the two languages, so a review should be done on the variable being used within the command to find its correct Snowflake equivalence. To see the list of system variables in Oracle you can use the command `SHOW ALL` whereas in Snowflake you can use [`!options`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#options-opts).

### Related EWIs[¶](#id112 "Link to this heading")

No related EWIs.

## Show[¶](#show "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id113 "Link to this heading")

> Shows the value of a SQLPlus system variable or the current SQLPlus environment. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/SHOW.html#GUID-6BB1499D-E537-43D1-A209-401F5DB95E16))

#### Oracle Syntax[¶](#id114 "Link to this heading")

```
SHO[W] system_variable  ALL BTI[TLE]  CON_ID  CON_NAME EDITION  ERR[ORS] [ {ANALYTIC VIEW | ATTRIBUTE DIMENSION | HIERARCHY | FUNCTION | PROCEDURE | PACKAGE | PACKAGE BODY | TRIGGER | VIEW | TYPE | TYPE BODY | DIMENSION | JAVA CLASS } [schema.]name]HISTORY  LNO  LOBPREF[ETCH]  PARAMETER[S] [parameter_name]  PDBS PNO  RECYC[LEBIN] [original_name]  REL[EASE]  REPF[OOTER]  REPH[EADER]  ROWPREF[ETCH] SGA SPOO[L]  SPPARAMETER[S] [parameter_name]  SQLCODE STATEMENTC[ACHE] TTI[TLE] USER XQUERY
```

Copy

Snowflake does not have a direct equivalent for this command. However, some of its functionalities can be emulated.

#### 1. Show ERRORS[¶](#show-errors "Link to this heading")

> Shows the compilation errors of a stored procedure (includes stored functions, procedures, and packages). After you use the CREATE command to create a stored procedure, a message is displayed if the stored procedure has any compilation errors.

In Snowflake, performing an extra statement to display all the compilation errors is unnecessary. The compilation errors are displayed immediately when executing the CREATE statement.

##### Oracle[¶](#id115 "Link to this heading")

##### Command[¶](#id116 "Link to this heading")

```
CREATE OR REPLACE PROCEDURE RANCOM_PROC
AS
BEGIN
  INSERT INTO NE_TABLE SELECT 1 FROM DUAL;
END;

SHOW ERRORS
```

Copy

##### Result[¶](#result "Link to this heading")

```
LINE/COL ERROR
-------- -----------------------------------------------------------------
4/3      PL/SQL: SQL Statement ignored
4/10     PL/SQL: ORA-00925: missing INTO keyword
```

Copy

Note

Note that the INTO keyword is misspelled in order to cause a compilation error.

##### SnowSQL (CLI Client)[¶](#id117 "Link to this heading")

##### Command[¶](#id118 "Link to this heading")

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

Copy

##### Result[¶](#id119 "Link to this heading")

```
001003 (42000): SQL compilation error:
syntax error line 3 at position 7 unexpected 'INT'.
syntax error line 3 at position 11 unexpected 'PUBLIC'.
```

Copy

#### Show ALL[¶](#show-all "Link to this heading")

> Lists the settings of all SHOW options, except ERRORS and SGA, in alphabetical order.

In order to display all the possible options in SnowCLI you can run the [`!options`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#options-opts) command.

##### Oracle[¶](#id120 "Link to this heading")

##### Command[¶](#id121 "Link to this heading")

```
show all;
```

Copy

##### Result[¶](#id122 "Link to this heading")

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

Copy

##### SnowSQL (CLI Client)[¶](#id123 "Link to this heading")

##### Command[¶](#id124 "Link to this heading")

```
!options
```

Copy

##### Result[¶](#id125 "Link to this heading")

| Name | Value | Help |
| --- | --- | --- |
| auto\_completion | True | Displays auto-completion suggestions for commands and Snowflake objects |
| client\_session\_keep\_alive | False | Keeps the session active indefinitely, even if there is no activity from the user. |
| client\_store\_temporary\_credential | False | Enable Linux users to use temporary file to store ID\_TOKEN. |
| connection\_options | {} | Set arbitrary connection parameters in underlying Python connector connections. |
| echo | False | Outputs the SQL command to the terminal when it is executed |
| editor | vim | Changes the editor to use for the !edit command |
| empty\_for\_null\_in\_tsv | False | Outputs an empty string for NULL values in TSV format |
| environment\_variables | [] | Specifies the environment variables to be set in the SnowSQL variables. |
|  |  | The variable names should be comma separated. |
| execution\_only | False | Executes queries only. No data will be fetched |
| exit\_on\_error | False | Quits when SnowSQL encounters an error |
| fix\_parameter\_precedence | True | Fix the connection parameter precedence in the order of 1) Environment variables, 2) Connection parameters, 3) Default connection parameters. |
| force\_put\_overwrite | False | Forces OVERWRITE=true for PUT. This is to mitigate S3’s eventually consistent issue. |
| friendly | True | Shows the splash text and goodbye messages |
| header | True | Outputs the header in query results |
| insecure\_mode | False | Turns off OSCP certificate checks |
| key\_bindings | emacs | Changes keybindings for navigating the prompt to emacs or vi |
| log\_bootstrap\_file | ../snowsql\_rt.log\_bo.. | SnowSQL bootstrap log file location |
| log\_file | ../snowsql\_rt.log | SnowSQL main log file location |
| log\_level | DEBUG | Changes the log level (critical, debug, info, error, warning) |
| login\_timeout | 120 | Login timeout in seconds. |
| noup | False | Turns off auto upgrading Snowsql |
| ocsp\_fail\_open | True | Sets the fail open mode for OCSP Failures. For help please refer the documentation. |
| output\_file | None | Writes output to the specified file in addition to the terminal |
| output\_format | psql | Sets the output format for query results. |
| paging | False | Enables paging to pause output per screen height. |
| progress\_bar | True | Shows progress bar while transferring data. |
| prompt\_format | [user]#[warehouse]@[.. | Sets the prompt format. For help, see the documentation |
| quiet | False | Hides all output |
| remove\_comments | False | Removes comments before sending query to Snowflake |
| remove\_trailing\_semicolons | False | Removes trailing semicolons from SQL text before sending queries to Snowflake |
| results | True | If set to off, queries will be sent asynchronously, but no results will be fetched. |
|  |  | Use !queries to check the status. |
| rowset\_size | 1000 | Sets the size of rowsets to fetch from the server. |
|  |  | Set the option low for smooth output, high for fast output. |
| sfqid | False | Turns on/off Snowflake query id in the summary. |
| sfqid\_in\_error | False | Turns on/off Snowflake query id in the error message |
| sql\_delimiter | ; | Defines what reserved keyword splits SQL statements from each other. |
| sql\_split | snowflake.connector… | Choose SQL spliter implementation. Currently snowflake.connector.util\_text, or snowflake.cli.sqlsplit. |
| stop\_on\_error | False | Stops all queries yet to run when SnowSQL encounters an error |
| syntax\_style | default | Sets the colors for the text of SnowSQL. |
| timing | True | Turns on/off timing for each query |
| timing\_in\_output\_file | False | Includes timing in the output file. |
| variable\_substitution | False | Substitutes variables (starting with ‘&’) with values |
| version | 1.2.24 | SnowSQL version |
| wrap | True | Truncates lines at the width of the terminal screen |
| ———————————– | ———————— | ———————————————————————————————————————————————– |

### Known Issues[¶](#id126 "Link to this heading")

**1. It’s not possible in SnowCLI to display de value of a single option.**

SnowCLI does not provide a way to display the value of a specific option. You may use `!options` to watch the value of the option.

**2. Research is pending to match each SQLPLUS option to a SnowflakeCLI equivalent.**

It is pending to define an equivalent for each SQLPLUS option.

### Related EWIs[¶](#id127 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Spool[¶](#spool "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id128 "Link to this heading")

> The `SPOOL` command stores query results in a file, or optionally sends the file to a printer. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/SPOOL.html#GUID-61492052-ECCB-45C8-AF94-AB9794C60BEA))

#### Oracle Syntax[¶](#id129 "Link to this heading")

```
SPO[OL] [file_name[.ext] [CRE[ATE] | REP[LACE] | APP[END]] | OFF | OUT]
```

Copy

##### SnowSQL (CLI Client) !spool[¶](#snowsql-cli-client-spool "Link to this heading")

```
!spool [<file_name>] | [off]
```

Copy

#### 1. Spool without options[¶](#spool-without-options "Link to this heading")

Hint

This case is functionally equivalent.

When the `SPOOL` command is not accompanied by any option, by default it creates a new file with the specified name and extension. The `SPOOL` command is replaced by the [`!spool`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#spool) command.

##### Oracle[¶](#id130 "Link to this heading")

##### Command[¶](#id131 "Link to this heading")

```
SPOOL temp
SPOOL temp.txt
```

Copy

##### SnowSQL (CLI Client)[¶](#id132 "Link to this heading")

##### Command[¶](#id133 "Link to this heading")

```
!spool temp
!spool temp.txt
```

Copy

#### 2. Spool with write options[¶](#spool-with-write-options "Link to this heading")

Warning

This case is not functionally equivalent.

Oracle allows 3 types of options when writing to a file through the `SPOOL` command, the CREATE and APPEND options create a file for writing from scratch and concatenate text to the end of an existing file (or create a new one if it doesn’t exist) respectively. Snowflake does not support these options, however, its default behavior is to create a file and if it exists, concatenate the text in it. The REPLACE option, on the other hand, writes to the specific file replacing the existing content. To simulate this behavior in Snowflake it is recommended to delete the file where you want to write and start writing again, as shown in the following code

##### Oracle[¶](#id134 "Link to this heading")

##### Command[¶](#id135 "Link to this heading")

```
SPOOL temp.txt CREATE
SPOOL temp.txt APPEND
SPOOL temp.txt REPLACE
```

Copy

##### SnowSQL (CLI Client)[¶](#id136 "Link to this heading")

##### Command[¶](#id137 "Link to this heading")

```
!spool temp.txt
!spool temp.txt

!system del temp.txt
!spool temp.txt
```

Copy

#### 3. Spool turn off[¶](#spool-turn-off "Link to this heading")

Hint

This case is functionally equivalent.

Oracle has two options to turn off results spooling, OFF and OUT. both are meant to stop rolling, with the difference that the second also sends the file to the computer’s standard (default) printer. This option is not available on some operating systems. Snowflake only has the option to turn off results spooling

##### Oracle[¶](#id138 "Link to this heading")

##### Command[¶](#id139 "Link to this heading")

```
SPOOL OFF
SPOOL OUT
```

Copy

##### SnowSQL (CLI Client)[¶](#id140 "Link to this heading")

##### Command[¶](#id141 "Link to this heading")

```
!spool off
!spool off
```

Copy

### Known Issues[¶](#id142 "Link to this heading")

No Known Issues.

### Related EWIs[¶](#id143 "Link to this heading")

No related EWIs.

## Start[¶](#start "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id144 "Link to this heading")

> The `START` command runs the SQL\*Plus statements in the specified script. The script can be called from the local file system or from a web server. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/START.html#GUID-A8D3613E-A141-42FB-8288-654427BAB28F))

#### Oracle Syntax[¶](#id145 "Link to this heading")

```
STA[RT] {url | file_name[.ext] } [arg...]
```

Copy

##### SnowSQL (CLI Client) !load[¶](#snowsql-cli-client-load "Link to this heading")

```
!(load | source) {url | file_name[.ext] }
```

Copy

The Snowflake [`!source`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#source-load) and [`!load`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#source-load) commands are equivalent.

#### 1. Simple start[¶](#simple-start "Link to this heading")

The `START` command is replaced by the [`!load`](https://docs.snowflake.com/en/user-guide/snowsql-use.html#source-load) command.

Hint

This case is functionally equivalent.

##### Oracle[¶](#id146 "Link to this heading")

##### Command[¶](#id147 "Link to this heading")

```
START C:\Users\My_User\Desktop\My\Path\insert_script.sql
```

Copy

##### SnowSQL (CLI Client)[¶](#id148 "Link to this heading")

##### Command[¶](#id149 "Link to this heading")

```
!load C:\Users\My_User\Desktop\My\Path\insert_script.sql
```

Copy

#### 2. Start with arguments[¶](#start-with-arguments "Link to this heading")

##### Oracle[¶](#id150 "Link to this heading")

##### Command[¶](#id151 "Link to this heading")

```
START C:\Users\My_User\Desktop\My\Path\insert_script.sql 123 456 789
```

Copy

##### SnowSQL (CLI Client)[¶](#id152 "Link to this heading")

##### Command[¶](#id153 "Link to this heading")

```
!load C:\Users\My_User\Desktop\My\Path\insert_script.sql
```

Copy

Warning

Script arguments are currently not supported for SnowSQL (CLI Client).

### Known Issues[¶](#id154 "Link to this heading")

**1. Arguments are not supported in the SnowSQL CLI Client**

Oracle can pass down multiple arguments to a script and can be accessed with &1, &2, and so on, but this cannot be done in the SnowSQL CLI Client. You can simulate arguments by declaring variables with the `!define` command. Keep in mind that these values are defined globally for all the scripts so the behavior may not be equivalent.

This workaround would look something like this:

```
!set variable_substitution=true
!define 1=123
!define 2=456
!define 3=789
!load C:\Users\My_User\Desktop\My\Path\insert_script.sql
```

Copy

### Related EWIs[¶](#id155 "Link to this heading")

No related EWIs.

## Whenever oserror[¶](#whenever-oserror "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id156 "Link to this heading")

> The `WHENEVER OSERROR` command Performs the specified action (exits SQL\*Plus by default) if an operating system error occurs. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/WHENEVER-OSERROR.html#GUID-A52F926F-D6EC-434E-9C7E-CFDB76422E94))

#### Oracle Syntax[¶](#id157 "Link to this heading")

```
WHENEVER OSERROR {EXIT [SUCCESS | FAILURE | n | variable | :BindVariable]  [COMMIT | ROLLBACK] | CONTINUE [COMMIT | ROLLBACK | NONE]}
```

Copy

Snowflake does not support the use of this command and does not have any that might resemble its functionality. At the time of transformation, an EWI will be added.

#### 1. Whenever oserror command[¶](#whenever-oserror-command "Link to this heading")

##### Oracle[¶](#id158 "Link to this heading")

##### Command[¶](#id159 "Link to this heading")

```
WHENEVER OSERROR EXIT
```

Copy

##### SnowSQL (CLI Client)[¶](#id160 "Link to this heading")

##### Command[¶](#id161 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'WHENEVER ERROR STATEMENT' NODE ***/!!!
WHENEVER OSERROR EXIT;
```

Copy

### Known Issues[¶](#id162 "Link to this heading")

No Known Issues.

### Related EWIs[¶](#id163 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

## Whenever sqlerror[¶](#whenever-sqlerror "Link to this heading")

Warning

Transformation for this command is pending

### Description[¶](#id164 "Link to this heading")

> The `WHENEVER SQLERROR` command Performs the specified action (exits SQL\*Plus by default) if a SQL command or PL/SQL block generates an error. ([Oracle SQL Plus User’s Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/WHENEVER-SQLERROR.html#GUID-66C1C12C-5E95-4440-A37B-7CCE7E33491C))

#### Oracle Syntax[¶](#id165 "Link to this heading")

```
WHENEVER SQLERROR {EXIT [SUCCESS | FAILURE | WARNING | n | variable  | :BindVariable] [COMMIT | ROLLBACK] | CONTINUE [COMMIT | ROLLBACK | NONE]}
```

Copy

Snowflake does not support the use of this command and does not have any that might resemble its functionality. At the time of transformation, an EWI will be added.

#### 1. Whenever sqlerror command[¶](#whenever-sqlerror-command "Link to this heading")

##### Oracle[¶](#id166 "Link to this heading")

##### Command[¶](#id167 "Link to this heading")

```
WHENEVER SQLERROR EXIT
```

Copy

##### SnowSQL (CLI Client)[¶](#id168 "Link to this heading")

##### Command[¶](#id169 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'WHENEVER ERROR STATEMENT' NODE ***/!!!
WHENEVER SQLERROR EXIT;
```

Copy

### Known Issues[¶](#id170 "Link to this heading")

No Known Issues.

### Related EWIs[¶](#id171 "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

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

1. [Accept](#accept)
2. [Append](#append)
3. [Archive Log](#archive-log)
4. [Attribute](#attribute)
5. [Break](#break)
6. [Btitle](#btitle)
7. [Change](#change)
8. [Column](#column)
9. [Define](#define)
10. [Host](#host)
11. [Prompt](#prompt)
12. [Remark](#remark)
13. [Set](#set)
14. [Show](#show)
15. [Spool](#spool)
16. [Start](#start)
17. [Whenever oserror](#whenever-oserror)
18. [Whenever sqlerror](#whenever-sqlerror)