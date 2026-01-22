---
description: Translation references to convert Teradata BTEQ files to Python
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-python/bteq-translation
title: SnowConvert AI - Teradata - BTEQ | Snowflake Documentation
---

## BTEQ Commands Translation

The following table presents the conversion for the BTEQ commands to Snowflake.

<!-- prettier-ignore -->
|Teradata|Snowflake|Notes|
|---|---|---|---|---|
|ERRORCODE != 0|snowconvert.helpers.error_code != 0||
|.EXPORT DATA FILE=fileName|Export.report(“fileName”, “,”)|The function has no functionality|
|.EXPORT INDICDATA FILE=fileName|Export.report(“fileName”, “,”)|The function has no functionality|
|.EXPORT REPORT FILE=fileName|Export.report(“fileName”, “,”)|The function has no functionality|
|.EXPORT DIF FILE=fileName|Export.report(“fileName”, “,”)|The function has no functionality|
|.EXPORT RESET|Export.reset()|The function has no functionality|
|.IF ERRORCODE != 0 THEN .QUIT ERRORCODE|If snowconvert.helpers.error_code != 0: snowconvert.helpers.quit_application (snowconvert.helpers.error_code)||
|.IMPORT RESET|snowconvert.helpers.import_reset()|The function has no functionality|
|.LABEL newLabel|def NEWLABEL(): snowconvert.helpers.quit_application()||
|.LOGOFF|The statement is commented||
|.LOGON|The statement is commented||
|.LOGMECH|The statement is commented||
|.OS /fs/fs01/bin/filename.sh ‘load’|snowconvert.helpers.os(“”/fs/fs01/bin/filename.sh ‘load’ “”)||
|.RUN FILE=newFile|for statement in snowconvert.helpers.readrun(“newFile”): eval(statement)||
|.SET DEFAULTS|Export.defaults()|The function has no functionality|
|.SET ERRORLEVEL 3807 SEVERITY 0|snowconvert.helpers.set_error_level(3807, 0)||
|.SET RECORMODE OFF|Export.record_mode(False)||
|.SET RECORMODE ON|Export.record_mode(True)||
|.SET SEPARATOR ‘|’|Export.separator_string(‘|’)|The function has no functionality|
|.SET WIDTH 120|Export.width(120)|The function has no functionality|
|.Remark “”Hello world!”””|snowconvert.helpers.remark(r””””””Hello world!””””””)||
|.QUIT ERRORCODE|snowconvert.helpers.quit_application( snowconvert.helpers.error_code )||
|.QUIT|snowconvert.helpers.quit_application()||
|SQL statements|exec(statement)||
|$(<$INPUT_SQL_FILE)|exec_file(“$INPUT_SQL_FILE”)||
|= (Repeat previous command)|snowconvert.helpers.repeat_previous_sql_statement(con)||

For more complicated statements presented in the previous table, subsections with more elaborated
examples are explained.

### .GOTO Conversion

Since we are converting BTEQ scripts to Python, certain structures that are valid in BTEQ are not
inherently supported in Python. This is the case for the `.GOTO` command using the `.Label`
commands.

For this reason, an alternative has been developed so that the functionality of these commands can
be emulated, turning the `.Label` commands into functions with subsequent call statements.

Check the following code:

```sql
 .LABEL FIRSTLABEL
SELECT * FROM MyTable1;
.LABEL SECONDLABEL
SELECT * FROM MyTable2;
SELECT * FROM MyTable3;
```

In the example above, there were five commands. Two of them were`.Label`commands. The
command`FIRSTLABEL`was transformed into a function with the statement(s) that follow it below until
another`.LABEL`command is found. When another label is called (in this case, `SECONDLABEL`), that
call ends the first function and starts a new one.

If we were to migrate the previous example, the result would be:

```sql
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

_Notice there is a call to the function_`FIRSTLABEL`_, this function has only one statement, which
would be the only non-label command that follows`FIRSTLABEL`in the original code. Before
the`FIRSTLABEL`function ends, it calls_ `SECONDLABEL`_, with the statements that followed it._

> - _Notes:_
>   - Creating a connector variable `con = None`, and populating it in the `main()` function:
>     `con = snowconvert.helpers.log_on()`.
>   - Setting up a log: `snowconvert.helpers.configure_log()`.

### Execute Query Statements

Every SQL statement found in a BTEQ file will be executed though to the`exec`function provided by
the [snowconvert.helpers](snowconvert-script-helpers). Take for example the following code:

```sql
 CREATE TABLE aTable (aColumn BYTEINT);
```

This is converted to:

```sql
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

### Execute Script Files

Files that contain a user’s BTEQ commands and Teradata SQL statements are called scripts, run files,
macros, or stored procedures. For example, create a file called SAMPFILE, and enter the following
BTEQ script:

```sql
    .LOGON tdpid/userid,password
   SELECT * FROM department;
   .LOGOFF
```

To execute the run file, enter either form of the BTEQ RUN command:

```sql
.RUN FILE=sampfile
```

If you convert the second code, the result is the following:

```sql
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

The `snowconvert.helpers.readrun("sampfile")` will return each line from the SAMPFILE and in
the`FOR`statement, each one of the lines will be passed to the `eval` function, a method that parses
the expression passed to it and runs python expression (the SAMPFILE should be converted to work)
within the program.

### Execute SQL Files

In some instances during the execution of a BTEQ file a SQL file can be found, take for example the
SQL file called NEWSQL:

```sql
 CREATE TABLE aTable (aColumn BYTEINT);
```

This can be executed during a script with the following line:

```sql
 $(<$NEWSQL)
```

And after the conversion of the script the result is:

```sql
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

The `exec_file` helper function will read each line from the NEWSQL file and then use the exec
function as explained in the section [Execute query statement](#execute-query-statements).

## Known Issues

No issues were found.

## Related EWIs

No issues were found.

## REPEAT

Translation specification for the REPEAT statement.

### Note

Some parts in the output code are omitted for clarity reasons.

As per Teradata’s
[documentation](https://docs.teradata.com/r/Basic-Teradata-Query-Reference/October-2018/BTEQ-Commands/BTEQ-Command-Descriptions/REPEAT),
the REPEAT statement enables users to specify the maximum number of times the next SQL request is to
be submitted. Note that a SQL request can be a single or multi-statement request. This is defined by
the position of the semicolons for each statement following the REPEAT statement.

### Syntax

```sql
REPEAT [ n [ PACK p [ REQBUFLEN b ] ] | * | RECS r]
`<sql_request>`
```

### Sample Source Patterns

With this input data:

#### inputData.dat

```sql
A B C
D E F
G H I
```

##### inputData2.dat

```sql
* [
] *
```

#### Teradata

##### Query

```sql
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

##### TESTTABU Result

<!-- prettier-ignore -->
|C1|C2|
|---|---|
|A|X|
|D|X|
|G|X|
|B|Y|
|E|Y|
|H|Y|
|C|Z|
|F|Z|
|I|Z|
|?|\_|
|?|\_|
|?|\_|
|\*|null|
|[|null|

##### TESTTABU2 Result

<!-- prettier-ignore -->
|MY_NAME|MY_AGE|
|---|---|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|Bob Alice|21|
|Bob Alice|21|
|Bob Alice|21|
|Bob Alice|21|
|Bob Alice|21|

#### Snowflake

##### Query 2

```sql
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

##### TESTTABU Result 2

<!-- prettier-ignore -->
|C1|C2|
|---|---|
|A|X|
|D|X|
|G|X|
|B|Y|
|E|Y|
|H|Y|
|C|Z|
|F|Z|
|I|Z|
|?|\_|
|?|\_|
|?|\_|
|\*|null|
|[|null|

##### TESTTABU2 Result 2

<!-- prettier-ignore -->
|MY_NAME|MY_AGE|
|---|---|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|John Doe|23|
|Bob Alice|21|
|Bob Alice|21|
|Bob Alice|21|
|Bob Alice|21|
|Bob Alice|21|

### Known Issues 2

No issues were found.

### Related EWIs 2

No related EWIs.

## USING REQUEST MODIFIER

Translation specification for the USING REQUEST MODIFIER query.

### Note 2

Some parts in the output code are omitted for clarity reasons.

As per Teradata’s
[documentation](https://docs.teradata.com/r/SQL-Data-Manipulation-Language/September-2020/Statement-Syntax/USING-Request-Modifier/USING-Request-Modifier-Syntax),
the USING REQUEST MODIFIER defines one or more variable parameter names to be used in the subsequent
`SELECT`, `INSERT`, `UPDATE`, or `DELETE` statements to import or export data.

The syntax for this statement is as follows:

```sql
 USING ( `<using_spec>` [,...] ) SQL_request

`<using_spec>` ::= using_variable_name data_type [ data_type_attribute [...] ]
  [ AS { DEFERRED [BY NAME] | LOCATOR } ]
```

As stated in Teradata’s documentation, the USING REQUEST MODIFIER needs to be preceded by an .IMPORT
statement for it to load the data into the defined parameters.

Thus, the transformation for this statement follows these steps:

1. Call the `import_file()` function from the SnowConvert AI Helpers. This loads the data into a
   temporary file.
2. Call the `using()` function from the SnowConvert AI Helpers to create a dictionary with the
   loaded data.
3. For each query, run the `exec()` function from the SnowConvert AI Helpers and pass the previously
   defined dictionary. This will use Snowflake Python Connector data binding capabilities.

With this input data:

```sql
 A,B,C
```

### Teradata (MultiLoad)

### Query 3

```sql
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

#### Result

<!-- prettier-ignore -->
|ROW|C1|C2|
|---|---|---|
|1|A|X|
|2|B|Y|
|3|C|Z|

##### Snowflake (Python)

##### Query 4

```sql
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

##### Result 2

<!-- prettier-ignore -->
|ROW|C1|C2|
|---|---|---|
|1|A|X|
|2|B|Y|
|3|C|Z|

### Known Issues 3

#### 1. .REPEAT command is not yet supported

The `.REPEAT` command is not yet supported. This means that the USING REQUEST MODIFIER will only use
the data loaded from the first row of the input file. Thus, the queries will only run once.

This issue should be fixed when the .REPEAT command receives proper transformation support.

If you have any additional questions regarding this documentation, you can email us at
[snowconvert-support@snowflake.com](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-python/mailto:snowconvert-support%40snowflake.com).

### Related EWIs 3

No related EWIs.
