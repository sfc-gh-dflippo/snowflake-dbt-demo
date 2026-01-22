---
auto_generated: true
description: Translation references to convert Teradata BTEQ files to Python
last_scraped: '2026-01-14T16:53:45.072959+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-python/bteq-translation
title: SnowConvert AI - Teradata - BTEQ | Snowflake Documentation
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
          + [Teradata](../README.md)

            - [Data Migration Considerations](../data-migration-considerations.md)
            - [Session Modes in Teradata](../session-modes.md)
            - [Sql Translation Reference](../sql-translation-reference/README.md)
            - [SQL to JavaScript (Procedures)](../teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](../teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](README.md)

              * [BTEQ](bteq-translation.md)
              * [FLOAD](fastload-translation.md)
              * [MLOAD](multiload-translation.md)
              * [TPT](tpt-translation.md)
              * [Script helpers](snowconvert-script-helpers.md)
            - [Scripts to Snowflake SQL](../scripts-to-snowflake-sql-translation-reference/README.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](../etl-bi-repointing/power-bi-teradata-repointing.md)
          + [Oracle](../../oracle/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)Translation References[Teradata](../README.md)[Scripts To Python](README.md)BTEQ

# SnowConvert AI - Teradata - BTEQ[¶](#snowconvert-ai-teradata-bteq "Link to this heading")

Translation references to convert Teradata BTEQ files to Python

Basic Teradata Query (BTEQ) is a general-purpose, command-based program that enables users on a workstation to communicate with one or more Teradata Database systems, and to format reports for both print and screen output.

In order to simulate the BTEQ functionality for Teradata in Snowflake, BTEQ files and commands are transformed to Python code, similar to the transformations performed for MultiLoad and FastLoad scripts. The generated code uses the Snowflake Python project called [snowconvert.helpers](snowconvert-script-helpers) which contains the required functions to simulate the BTEQ statements in Snowflake.

## BTEQ Commands Translation[¶](#bteq-commands-translation "Link to this heading")

The following table presents the conversion for the BTEQ commands to Snowflake.

| Teradata | Snowflake | Notes |
| --- | --- | --- |
| ERRORCODE != 0 | snowconvert.helpers.error\_code != 0 |  |
| .EXPORT DATA FILE=fileName | Export.report(“fileName”, “,”) | The function has no functionality |
| .EXPORT INDICDATA FILE=fileName | Export.report(“fileName”, “,”) | The function has no functionality |
| .EXPORT REPORT FILE=fileName | Export.report(“fileName”, “,”) | The function has no functionality |
| .EXPORT DIF FILE=fileName | Export.report(“fileName”, “,”) | The function has no functionality |
| .EXPORT RESET | Export.reset() | The function has no functionality |
| .IF ERRORCODE != 0 THEN .QUIT ERRORCODE | If snowconvert.helpers.error\_code != 0: snowconvert.helpers.quit\_application (snowconvert.helpers.error\_code) |  |
| .IMPORT RESET | snowconvert.helpers.import\_reset() | The function has no functionality |
| .LABEL newLabel | def NEWLABEL(): snowconvert.helpers.quit\_application() |  |
| .LOGOFF | The statement is commented |  |
| .LOGON | The statement is commented |  |
| .LOGMECH | The statement is commented |  |
| .OS /fs/fs01/bin/filename.sh ‘load’ | snowconvert.helpers.os(“”/fs/fs01/bin/filename.sh ‘load’ “”) |  |
| .RUN FILE=newFile | for statement in snowconvert.helpers.readrun(“newFile”): eval(statement) |  |
| .SET DEFAULTS | Export.defaults() | The function has no functionality |
| .SET ERRORLEVEL 3807 SEVERITY 0 | snowconvert.helpers.set\_error\_level(3807, 0) |  |
| .SET RECORMODE OFF | Export.record\_mode(False) |  |
| .SET RECORMODE ON | Export.record\_mode(True) |  |
| .SET SEPARATOR ‘|’ | Export.separator\_string(‘|’) | The function has no functionality |
| .SET WIDTH 120 | Export.width(120) | The function has no functionality |
| .Remark “”Hello world!””” | snowconvert.helpers.remark(r””””””Hello world!””””””) |  |
| .QUIT ERRORCODE | snowconvert.helpers.quit\_application(  snowconvert.helpers.error\_code  ) |  |
| .QUIT | snowconvert.helpers.quit\_application() |  |
| SQL statements | exec(statement) |  |
| $(<$INPUT\_SQL\_FILE) | exec\_file(“$INPUT\_SQL\_FILE”) |  |
| = (Repeat previous command) | snowconvert.helpers.repeat\_previous\_sql\_statement(con) |  |

For more complicated statements presented in the previous table, subsections with more elaborated examples are explained.

### .GOTO Conversion[¶](#goto-conversion "Link to this heading")

Since we are converting BTEQ scripts to Python, certain structures that are valid in BTEQ are not inherently supported in Python. This is the case for the `.GOTO` command using the `.Label` commands.

For this reason, an alternative has been developed so that the functionality of these commands can be emulated, turning the `.Label` commands into functions with subsequent call statements.

Check the following code:

```
 .LABEL FIRSTLABEL
SELECT * FROM MyTable1;
.LABEL SECONDLABEL
SELECT * FROM MyTable2;
SELECT * FROM MyTable3;
```

Copy

In the example above, there were five commands. Two of them were`.Label`commands. The command`FIRSTLABEL`was transformed into a function with the statement(s) that follow it below until another`.LABEL`command is found. When another label is called (in this case, `SECONDLABEL`), that call ends the first function and starts a new one.

If we were to migrate the previous example, the result would be:

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
 
import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  FIRSTLABEL()
  snowconvert.helpers.quit_application()
def FIRSTLABEL():
  exec("""
    SELECT
      *
    FROM
      MyTable1
    """)
  SECONDLABEL()
def SECONDLABEL():
  exec("""
    SELECT
      *
    FROM
      MyTable2
    """)
  exec("""
    SELECT
      *
    FROM
      MyTable3
    """)

if __name__ == "__main__":
  main()
```

Copy

*Notice there is a call to the function*`FIRSTLABEL`*, this function has only one statement, which would be the only non-label command that follows`FIRSTLABEL`in the original code. Before the`FIRSTLABEL`function ends, it calls* `SECONDLABEL`*, with the statements that followed it.*

> * *Notes:*
>
>   + Creating a connector variable `con = None`, and populating it in the `main()` function: `con = snowconvert.helpers.log_on()`.
>   + Setting up a log: `snowconvert.helpers.configure_log()`.

### Execute Query Statements[¶](#execute-query-statements "Link to this heading")

Every SQL statement found in a BTEQ file will be executed though to the`exec`function provided by the [snowconvert.helpers](snowconvert-script-helpers). Take for example the following code:

```
 CREATE TABLE aTable (aColumn BYTEINT);
```

Copy

This is converted to:

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
 
import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  exec("""
    CREATE OR REPLACE TABLE aTable (
      aColumn BYTEINT
    )
    """)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

Copy

### Execute Script Files[¶](#execute-script-files "Link to this heading")

Files that contain a user’s BTEQ commands and Teradata SQL statements are called scripts, run files, macros, or stored procedures. For example, create a file called SAMPFILE, and enter the following BTEQ script:

```
    .LOGON tdpid/userid,password 
   SELECT * FROM department;
   .LOGOFF
```

Copy

To execute the run file, enter either form of the BTEQ RUN command:

```
.RUN FILE=sampfile
```

Copy

If you convert the second code, the result is the following:

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
 
import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()

  for statement in snowconvert.helpers.readrun(fr"sampfile"):
    eval(statement)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

Copy

The `snowconvert.helpers.readrun("sampfile")` will return each line from the SAMPFILE and in the`FOR`statement, each one of the lines will be passed to the `eval` function, a method that parses the expression passed to it and runs python expression (the SAMPFILE should be converted to work) within the program.

### Execute SQL Files[¶](#execute-sql-files "Link to this heading")

In some instances during the execution of a BTEQ file a SQL file can be found, take for example the SQL file called NEWSQL:

```
 CREATE TABLE aTable (aColumn BYTEINT);
```

Copy

This can be executed during a script with the following line:

```
 $(<$NEWSQL)
```

Copy

And after the conversion of the script the result is:

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
 
import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  exec("""
    CREATE OR REPLACE TABLE aTable (
      aColumn BYTEINT
    )
    """)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

Copy

The `exec_file` helper function will read each line from the NEWSQL file and then use the exec function as explained in the section [Execute query statement](#execute-query-statements).

## Known Issues [¶](#known-issues "Link to this heading")

No issues were found.

## Related EWIs [¶](#related-ewis "Link to this heading")

No issues were found.

## REPEAT[¶](#repeat "Link to this heading")

Translation specification for the REPEAT statement.

Note

Some parts in the output code are omitted for clarity reasons.

As per Teradata’s [documentation](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018/BTEQ-Commands/BTEQ-Command-Descriptions/REPEAT), the REPEAT statement enables users to specify the maximum number of times the next SQL request is to be submitted. Note that a SQL request can be a single or multi-statement request. This is defined by the position of the semicolons for each statement following the REPEAT statement.

### Syntax[¶](#syntax "Link to this heading")

```
REPEAT [ n [ PACK p [ REQBUFLEN b ] ] | * | RECS r]
<sql_request>
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

With this input data:

#### inputData.dat[¶](#inputdata-dat "Link to this heading")

```
A B C
D E F
G H I
```

Copy

##### inputData2.dat[¶](#inputdata2-dat "Link to this heading")

```
* [
] *
```

Copy

#### Teradata:[¶](#teradata "Link to this heading")

##### Query[¶](#query "Link to this heading")

```
 .IMPORT DATA FILE = inputData.dat;
.REPEAT *
USING var_1 (CHARACTER), var_2 (CHARACTER), var_3 (CHARACTER)
INSERT INTO testtabu (c1) VALUES (:var_1)
;INSERT INTO testtabu (c1) VALUES (:var_2) 
;INSERT INTO testtabu (c1) VALUES (:var_3) 
;UPDATE testtabu 
   SET c2 = 'X'
   WHERE c1 = :var_1 
;UPDATE testtabu 
   SET c2 = 'Y' 
   WHERE c1 = :var_2 
;UPDATE testtabu 
   SET c2 = 'Z'
   WHERE c1 = :var_3
;INSERT INTO TESTTABU (c1, c2) VALUES ('?','_');

.REPEAT 10
INSERT INTO TESTTABU2 VALUES ('John Doe', 23);

.REPEAT RECS 5
INSERT INTO TESTTABU2 VALUES ('Bob Alice', 21);

.IMPORT DATA FILE = inputData2.dat;
USING (var_1 CHARACTER, var_2 CHARACTER)
INSERT INTO testtabu (c1) VALUES (:var_1) 
;INSERT INTO testtabu (c1) VALUES (:var_2);
```

Copy

##### TESTTABU Result[¶](#testtabu-result "Link to this heading")

| C1 | C2 |
| --- | --- |
| A | X |
| D | X |
| G | X |
| B | Y |
| E | Y |
| H | Y |
| C | Z |
| F | Z |
| I | Z |
| ? | \_ |
| ? | \_ |
| ? | \_ |
| \* | null |
| [ | null |

##### TESTTABU2 Result[¶](#testtabu2-result "Link to this heading")

| MY\_NAME | MY\_AGE |
| --- | --- |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| Bob Alice | 21 |
| Bob Alice | 21 |
| Bob Alice | 21 |
| Bob Alice | 21 |
| Bob Alice | 21 |

#### Snowflake:[¶](#snowflake "Link to this heading")

##### Query[¶](#id1 "Link to this heading")

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
 
import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  snowconvert.helpers.import_file(fr"inputData.dat")
  ssc_repeat_value = '*'
  ssc_max_iterations = 1

  for ssc_repeat_position in range(0, ssc_max_iterations):

    if ssc_repeat_position == 0:
      using = snowconvert.helpers.using("var_1", "CHARACTER", "var_2", "CHARACTER", "var_3", "CHARACTER", rows_to_read = ssc_repeat_value)
      exec("""
        INSERT INTO testtabu (c1)
        VALUES (:var_1)
        """, using = using)
      exec("""
        INSERT INTO testtabu (c1)
        VALUES (:var_2)
        """, using = using)
      exec("""
        INSERT INTO testtabu (c1)
        VALUES (:var_3)
        """, using = using)
      exec("""
        UPDATE testtabu
          SET
            c2 = 'X'
          WHERE
            c1 = :var_1
        """, using = using)
      exec("""
        UPDATE testtabu
          SET
            c2 = 'Y'
          WHERE
            c1 = :var_2
        """, using = using)
      exec("""
        UPDATE testtabu
          SET
            c2 = 'Z'
          WHERE
            c1 = :var_3
        """, using = using)
      exec("""
        INSERT INTO TESTTABU (c1, c2)
        VALUES ('?', '_')
        """, using = using)

  ssc_repeat_value = 10
  ssc_max_iterations = 10

  for ssc_repeat_position in range(0, ssc_max_iterations):
    exec("""
      INSERT INTO TESTTABU2
      VALUES ('John Doe', 23)
      """)
  ssc_repeat_value = 5
  ssc_max_iterations = 5

  for ssc_repeat_position in range(0, ssc_max_iterations):
    exec("""
      INSERT INTO TESTTABU2
      VALUES ('Bob Alice', 21)
      """)
  snowconvert.helpers.import_file(fr"inputData2.dat")
  using = snowconvert.helpers.using("var_1", "CHARACTER", "var_2", "CHARACTER", rows_to_read = 1)
  exec("""
    INSERT INTO testtabu (c1)
    VALUES (:var_1)
    """, using = using)
  exec("""
    INSERT INTO testtabu (c1)
    VALUES (:var_2)
    """, using = using)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

Copy

##### TESTTABU Result[¶](#id2 "Link to this heading")

| C1 | C2 |
| --- | --- |
| A | X |
| D | X |
| G | X |
| B | Y |
| E | Y |
| H | Y |
| C | Z |
| F | Z |
| I | Z |
| ? | \_ |
| ? | \_ |
| ? | \_ |
| \* | null |
| [ | null |

##### TESTTABU2 Result[¶](#id3 "Link to this heading")

| MY\_NAME | MY\_AGE |
| --- | --- |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| John Doe | 23 |
| Bob Alice | 21 |
| Bob Alice | 21 |
| Bob Alice | 21 |
| Bob Alice | 21 |
| Bob Alice | 21 |

### Known Issues [¶](#id4 "Link to this heading")

No issues were found.

### Related EWIs [¶](#id5 "Link to this heading")

No related EWIs.

## USING REQUEST MODIFIER[¶](#using-request-modifier "Link to this heading")

Translation specification for the USING REQUEST MODIFIER query.

Note

Some parts in the output code are omitted for clarity reasons.

As per Teradata’s [documentation](https://docs.teradata.com/r/SQL-Data-Manipulation-Language/September-2020/Statement-Syntax/USING-Request-Modifier/USING-Request-Modifier-Syntax), the USING REQUEST MODIFIER defines one or more variable parameter names to be used in the subsequent `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statements to import or export data.

The syntax for this statement is as follows:

```
 USING ( <using_spec> [,...] ) SQL_request

<using_spec> ::= using_variable_name data_type [ data_type_attribute [...] ]
  [ AS { DEFERRED [BY NAME] | LOCATOR } ]
```

Copy

As stated in Teradata’s documentation, the USING REQUEST MODIFIER needs to be preceded by an .IMPORT statement for it to load the data into the defined parameters.

Thus, the transformation for this statement follows these steps:

1. Call the `import_file()` function from the SnowConvert AI Helpers. This loads the data into a temporary file.
2. Call the `using()` function from the SnowConvert AI Helpers to create a dictionary with the loaded data.
3. For each query, run the `exec()` function from the SnowConvert AI Helpers and pass the previously defined dictionary. This will use Snowflake Python Connector data binding capabilities.

With this input data:

```
 A,B,C
```

Copy

**Teradata (MultiLoad)**

### Query[¶](#id6 "Link to this heading")

```
 .IMPORT DATA FILE = inputData.dat;
USING var_1 (CHARACTER), var_2 (CHARACTER), var_3 (CHARACTER)
INSERT INTO testtabu (c1) VALUES (:var_1)
;INSERT INTO testtabu (c1) VALUES (:var_2) 
;INSERT INTO testtabu (c1) VALUES (:var_3) 
;UPDATE testtabu 
   SET c2 = 'X'
   WHERE c1 = :var_1 
;UPDATE testtabu 
   SET c2 = 'Y' 
   WHERE c1 = :var_2 
;UPDATE testtabu 
   SET c2 = 'Z'
   WHERE c1 = :var_3;
```

Copy

#### Result[¶](#result "Link to this heading")

| ROW | C1 | C2 |
| --- | --- | --- |
| 1 | A | X |
| 2 | B | Y |
| 3 | C | Z |

**Snowflake (Python)**

##### Query[¶](#id7 "Link to this heading")

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
 
import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  snowconvert.helpers.import_file(fr"inputData.dat")
  using = snowconvert.helpers.using("var_1", "CHARACTER", "var_2", "CHARACTER", "var_3", "CHARACTER", rows_to_read = 1)
  exec("""
    INSERT INTO testtabu (c1)
    VALUES (:var_1)
    """, using = using)
  exec("""
    INSERT INTO testtabu (c1)
    VALUES (:var_2)
    """, using = using)
  exec("""
    INSERT INTO testtabu (c1)
    VALUES (:var_3)
    """, using = using)
  exec("""
    UPDATE testtabu
      SET
        c2 = 'X'
      WHERE
        c1 = :var_1
    """, using = using)
  exec("""
    UPDATE testtabu
      SET
        c2 = 'Y'
      WHERE
        c1 = :var_2
    """, using = using)
  exec("""
    UPDATE testtabu
      SET
        c2 = 'Z'
      WHERE
        c1 = :var_3
    """, using = using)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

Copy

##### Result[¶](#id8 "Link to this heading")

| ROW | C1 | C2 |
| --- | --- | --- |
| 1 | A | X |
| 2 | B | Y |
| 3 | C | Z |

### Known Issues[¶](#id9 "Link to this heading")

**1. .REPEAT command is not yet supported**

The `.REPEAT` command is not yet supported. This means that the USING REQUEST MODIFIER will only use the data loaded from the first row of the input file. Thus, the queries will only run once.

This issue should be fixed when the .REPEAT command receives proper transformation support.

If you have any additional questions regarding this documentation, you can email us at [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com).

### Related EWIs [¶](#id10 "Link to this heading")

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

1. [BTEQ Commands Translation](#bteq-commands-translation)
2. [Known Issues](#known-issues)
3. [Related EWIs](#related-ewis)
4. [REPEAT](#repeat)
5. [USING REQUEST MODIFIER](#using-request-modifier)