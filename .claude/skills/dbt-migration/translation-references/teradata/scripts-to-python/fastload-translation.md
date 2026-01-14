---
description: Translation references to convert Teradata FLOAD files to Python
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-python/fastload-translation
title: SnowConvert AI - Teradata - FLOAD | Snowflake Documentation
---

## FastLoad Commands Translation[¶](#fastload-commands-translation)

Most of the
[FastLoad commands](https://docs.teradata.com/r/vIWhrlrRPxEfMbR9H0qaTQ/GB0V~iGzwIASn~LiFWyAfA) are
considered not relevant in Snowflake, these commands are commented out. Below is the summary list of
FastLoad commands and their transformation status into Snowflake:

<!-- prettier-ignore -->
|Teradata FastLoad Command|Transformation Status|Note|
|---|---|---|
|AXSMOD|Commented|​|
|[BEGIN LOADING](#begin-loading)|**Transformed**|​The node is commented out since the transformation occurs in the related INSERT statement instead.|
|CLEAR|Commented|​|
|DATEFORM|Commented|​|
|[DEFINE](#define)|**Transformed**|​|
|[END LOADING](#end-loading)|**Transformed**|​Commented out since is not necessary for the transformation of the BEGIN LOADING.|
|ERRLIMIT|Commented|​|
|HELP|Commented|​|
|HELP TABLE|Commented|​|
|[INSERT](#insert)|**Transformed**|Transformed as part of the BEGIN LOADING.|
|LOGDATA|Commented|​|
|LOGMECH|Commented|​|
|LOGOFF|Commented|​|
|LOGON|Commented|​|
|NOTIFY|Commented|​|
|OS|Commented|​|
|QUIT|Commented|​|
|RECORD|Commented|​|
|RUN|Commented|​|
|SESSIONS|Commented|​|
|[SET RECORD](#set-record)|**Transformed**|​|
|SET SESSION CHARSET|Commented|​|
|SHOW|Commented|​|
|SHOW VERSIONS|Commented|​|
|SLEEP|Commented|​|
|TENACITY|Commented|​|

### Default Transformation[¶](#default-transformation)

The default behavior of the ConversionTool for these statements is to comment them out. For example:

**Teradata (FastLoad)**

```
 SESSIONS 4;
ERRLIMIT 25;
```

**Snowflake (Python)**

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
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
  #SESSIONS 4

  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
  #ERRLIMIT 25

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

Nonetheless, there are some exceptions that must be converted to specific Python statements in order
to work as intended in Snowflake.

### BEGIN LOADING (And related commands)[¶](#begin-loading-and-related-commands)

The transformation for the command `BEGIN LOADING` is a multi-part transformation that requires the
DEFINE, INSERT and (optionally) SET RECORD commands to simulate its behavior correctly.

This transformation is fully explained in this [section](#begin-loading).

#### SET RECORD[¶](#set-record)

As stated above, this command is not required for the transformation of the BEGIN LOADING. If not
found, the default delimiter will be set to ‘,’ (comma). Else, the defined delimiter will be used.

**Teradata (FastLoad)**

```
 BEGIN LOADING FastTable ERRORFILES Error1,Error2
   CHECKPOINT 10000;
```

**Snowflake (Python)**

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
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW **
  #BEGIN LOADING FastTable ERRORFILES Error1, Error2 CHECKPOINT 10000

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

In the example above, `FastTable` is the name of the table associated to the `BEGIN LOADING`
command. Note the use of the python variable`inputDataPlaceholder`, that must be defined by the user
in a previous step. The value represents the Snowflake stage that could be internal or external as
shown in the following table or as
[explained here](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html#examples).

<!-- prettier-ignore -->
|Stage|Input Data Place Holder|
|---|---|
|Stage|Input Data Place Holder|
|Internal stage|`@my_int_stage`|
|External stage|`@my_int_stage/path/file.csv`|
|Amazon S3 bucket|`s3://mybucket/data/files`|
|Google Cloud Storage|`gcs://mybucket/data/files`|
|Microsoft Azure|`azure://myaccount.blob.core.windows.net/mycontainer/data/files`|

### Embedded SQL[¶](#embedded-sql)

FastLoad scripts support Teradata statements inside the same file. The majority of these statements
are converted just as if they were inside a BTEQ file, with some exceptions.

Dropping an error table is commented out if inside a FastLoad file.

**Teradata (FastLoad)**

```
 DROP TABLE Error1;
DROP TABLE Error2;
```

**Snowflake (Python)**

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
    DROP TABLE Error1
    """)
  exec("""
    DROP TABLE Error2
    """)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

### Large Example[¶](#large-example)

Given the transformations shown above for a variety of commands, consider the following example.

**Teradata (FastLoad)**

```
 SESSIONS 4;
ERRLIMIT 25;
DROP TABLE FastTable;
DROP TABLE Error1;
DROP TABLE Error2;
CREATE TABLE FastTable, NO FALLBACK
   ( ID INTEGER, UFACTOR INTEGER, MISC CHAR(42))
   PRIMARY INDEX(ID);
DEFINE ID (INTEGER), UFACTOR (INTEGER), MISC (CHAR(42))
   FILE=FileName;
SHOW;
BEGIN LOADING FastTable ERRORFILES Error1,Error2
   CHECKPOINT 10000;
INSERT INTO FastTable (ID, UFACTOR, MISC) VALUES
   (:ID, :MISC);
END LOADING;
```

**Snowflake (Python)**

```
 #*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
#** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "Error1", "Error2" **

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
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
  #SESSIONS 4

  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
  #ERRLIMIT 25

  exec("""
    DROP TABLE FastTable
    """)
  exec("""
    CREATE OR REPLACE TABLE FastTable (
      ID INTEGER,
      UFACTOR INTEGER,
      MISC CHAR(42)
    )
    """)
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS ASSIGNMENT STATEMENTS **
  #DEFINE ID (INTEGER), UFACTOR (INTEGER), MISC (CHAR(42)) FILE = FileName

  ssc_define_columns = "ID (INTEGER), UFACTOR (INTEGER), MISC (CHAR(42))"
  #Set file name manually if empty
  ssc_define_file = f"""FileName"""
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
  #SHOW

  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW **
  #BEGIN LOADING FastTable ERRORFILES Error1, Error2 CHECKPOINT 10000

  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS PART OF THE BEGIN LOADING TRANSLATION **
  #INSERT INTO FastTable (ID, UFACTOR, MISC) VALUES (:ID, :MISC)

  ssc_begin_loading_columns = "(ID, UFACTOR, MISC)"
  ssc_begin_loading_values = [":ID", ":MISC"]
  BeginLoading.import_file_to_table(f"""FastTable""", ssc_define_columns, ssc_define_file, ssc_begin_loading_columns, ssc_begin_loading_values, ",")
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. END LOADING **
  #END LOADING

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

If you have any additional questions regarding this documentation, you can email us at
[snowconvert-support@snowflake.com](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-python/mailto:snowconvert-support%40snowflake.com).

## Known Issues[¶](#known-issues)

No issues were found.

## Related EWIs[¶](#related-ewis)

1. [SSC-FDM-0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007):
   Element with missing dependencies.
2. [SSC-FDM-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027):
   Removed next statement, not applicable in SnowFlake.

## BEGIN LOADING[¶](#begin-loading)

The transformation for the command `BEGIN LOADING` is a multi-part transformation that requires the
`DEFINE`, `INSERT` and (optionally) `SET RECORD` commands to simulate its behavior correctly.

This transformation is fully explained in the following subsections.

### SET RECORD[¶](#id1)

As stated above, this command is not required for the transformation of the BEGIN LOADING. If not
found, the default delimiter will be set to ‘,’ (comma). Else, the defined delimiter will be used.
This value is stored in the `ssc_set_record` variable.

As of now only `SET RECORD VARTEXT`, `SET RECORD FORMATTED` and `SET RECORD UNFORMATTED` are
supported. For the `BINARY` and `TEXT` keyword specification an error EWI is placed instead.

**Teradata (FastLoad)**

```
SET RECORD VARTEXT DELIMITER 'c' DISPLAY ERRORS 'efilename';
SET RECORD VARTEXT 'l' 'c' NOSTOP;
SET RECORD VARTEXT 'l' TRIM NONE LEADING 'p';
SET RECORD VARTEXT 'l' TRIM NONE TRAILING 'p';
SET RECORD VARTEXT 'l' TRIM NONE BOTH 'p';
SET RECORD FORMATTED TRIM NONE BOTH;
SET RECORD UNFORMATTED QUOTE NO OPTIONAL;
SET RECORD BINARY QUOTE NO YES 'q';
SET RECORD TEXT QUOTE OPTIONAL;
```

**Snowflake (Python)**

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
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS AN ASSIGNMENT STATEMENT **
  #SET RECORD VARTEXT DELIMITER 'c' DISPLAY ERRORS 'efilename'

  ssc_set_record = ""
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS AN ASSIGNMENT STATEMENT **
  #SET RECORD VARTEXT 'l' 'c' NOSTOP

  ssc_set_record = "'l'"
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS AN ASSIGNMENT STATEMENT **
  #SET RECORD VARTEXT 'l' TRIM NONE LEADING 'p'

  ssc_set_record = "'l'"
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS AN ASSIGNMENT STATEMENT **
  #SET RECORD VARTEXT 'l' TRIM NONE TRAILING 'p'

  ssc_set_record = "'l'"
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS AN ASSIGNMENT STATEMENT **
  #SET RECORD VARTEXT 'l' TRIM NONE BOTH 'p'

  ssc_set_record = "'l'"
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS AN ASSIGNMENT STATEMENT **
  #SET RECORD FORMATTED TRIM NONE BOTH

  ssc_set_record = ","
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS AN ASSIGNMENT STATEMENT **
  #SET RECORD UNFORMATTED QUOTE NO OPTIONAL

  ssc_set_record = "UNFORMATTED"
  #** SSC-EWI-0021 - 'BINARY' KEYWORD SPECIFICATION FOR SET RECORD NOT SUPPORTED IN SNOWFLAKE **
  #SET RECORD BINARY QUOTE NO YES 'q'

  #** SSC-EWI-0021 - 'TEXT' KEYWORD SPECIFICATION FOR SET RECORD NOT SUPPORTED IN SNOWFLAKE **
  #SET RECORD TEXT QUOTE OPTIONAL

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

### DEFINE[¶](#define)

The transformation for the `DEFINE` command sets the `ssc_define_columns` and `ssc_define_file`
variables with the value of the columns definition and the file path to be used in the
`BEGIN LOADING` transformation respectively.

**Teradata (FastLoad)**

```
DEFINE
    id (INTEGER),
    first_name (VARCHAR(50)),
    last_name (VARCHAR(50)),
    salary (FLOAT)
FILE=/tmp/inputData.txt;

DEFINE
    id (INTEGER),
    first_name (VARCHAR(50)),
    last_name (VARCHAR(50)),
    salary (FLOAT)

DEFINE
FILE=/tmp/inputData.txt;

DEFINE;
```

**Snowflake (Python)**

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
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS ASSIGNMENT STATEMENTS **
  #DEFINE id (INTEGER), first_name (VARCHAR(50)), last_name (VARCHAR(50)), salary (FLOAT) FILE = /tmp/inputData.txt

  ssc_define_columns = "id (INTEGER), first_name (VARCHAR(50)), last_name (VARCHAR(50)), salary (FLOAT)"
  #Set file name manually if empty
  ssc_define_file = f"""/tmp/inputData.txt"""
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS ASSIGNMENT STATEMENTS **
  #DEFINE id (INTEGER), first_name (VARCHAR(50)), last_name (VARCHAR(50)), salary (FLOAT)

  ssc_define_columns = "id (INTEGER), first_name (VARCHAR(50)), last_name (VARCHAR(50)), salary (FLOAT)"
  #Set file name manually if empty
  ssc_define_file = f""""""
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS ASSIGNMENT STATEMENTS **
  #DEFINE FILE = /tmp/inputData.txt

  ssc_define_columns = ""
  #Set file name manually if empty
  ssc_define_file = f"""/tmp/inputData.txt"""
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS ASSIGNMENT STATEMENTS **
  #DEFINE

  ssc_define_columns = ""
  #Set file name manually if empty
  ssc_define_file = f""""""
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

### BEGIN LOADING[¶](#id2)

The `BEGIN LOADING` command is commented out since the relevant information for the transformation
is found in the associated `INSERT` statement instead.

`ERRORFILES`, `NODROP`, `CHECKPOINT`, `INDICATORS` and `DATAENCRYPTION` specifications are not
necessary for the transformation and thus commented out.

**Teradata (FastLoad)**

```
BEGIN LOADING FastTable ERRORFILES Error1,Error2
   CHECKPOINT 10000;
```

**Snowflake (Python)**

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
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW **
  #BEGIN LOADING FastTable ERRORFILES Error1, Error2 CHECKPOINT 10000

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

### INSERT[¶](#insert)

The transformation for the associated `INSERT` statement sets the value for the
`ssc_begin_loading_columns` and `ssc_begin_loading_values` variables, used to determine the order in
which to insert the values to be loaded.

Finally, these variables and the ones described in the above sections are used to call the the
`BeginLoading.import_file_to_table` function part of the `SnowConvert.Helpers` module. This function
simulates the behavior of the whole FastLoad `BEGIN LOADING` process. To learn more about this
function check here.

**Teradata (FastLoad)**

```
SET RECORD VARTEXT """";
DEFINE
    _col1 (CHAR(10)),
    _col2 (CHAR(7)),
    _col3 (CHAR(2, NULLIF = 'V5'))
FILE=inputDataNoDel.txt;
BEGIN LOADING TESTS.EmpLoad4
ERRORFILES ${CPRDBName}.ET_${LOADTABLE},${CPRDBName}.UV_${LOADTABLE}
CHECKPOINT 1000;
INSERT INTO TESTS.EmpLoad4 (col2, col3, col1, col4)
VALUES
(
    :_col2,
    :_col3,
    :_col1,
    CURRENT_DATE
);
```

**Snowflake (Python)**

```
#*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
#** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TESTS.EmpLoad4" **

import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
#** SSC-FDM-TD0022 - SHELL VARIABLES FOUND, RUNNING THIS CODE IN A SHELL SCRIPT IS REQUIRED **
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS AN ASSIGNMENT STATEMENT **
  #SET RECORD VARTEXT "" ""

  ssc_set_record = ""
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS ASSIGNMENT STATEMENTS **
  #DEFINE _col1 (CHAR(10)), _col2 (CHAR(7)), _col3 (CHAR(2, NULLIF = 'V5')) FILE = inputDataNoDel.txt

  ssc_define_columns = "_col1 (CHAR(10)), _col2 (CHAR(7)), _col3 (CHAR(2, NULLIF = 'V5'))"
  #Set file name manually if empty
  ssc_define_file = f"""inputDataNoDel.txt"""
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW **
  #BEGIN LOADING TESTS.EmpLoad4 ERRORFILES ${CPRDBName}.ET_${LOADTABLE}, ${CPRDBName}.UV_${LOADTABLE} CHECKPOINT 1000

  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW AS PART OF THE BEGIN LOADING TRANSLATION **
  #INSERT INTO TESTS.EmpLoad4 (col2, col3, col1, col4) VALUES (:_col2, :_col3, :_col1, CURRENT_DATE)

  ssc_begin_loading_columns = "(col2, col3, col1, col4)"
  ssc_begin_loading_values = [":_col2", ":_col3", ":_col1", "CURRENT_DATE()"]
  BeginLoading.import_file_to_table(f"""TESTS.EmpLoad4""", ssc_define_columns, ssc_define_file, ssc_begin_loading_columns, ssc_begin_loading_values, ssc_set_record)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

Internally, the `import_file_to_table` function creates a temporary stage and puts the local file in
the stage to load into the specified table. However, the file might be already stored in one the
supported cloud provider by
[Snowflake](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table#required-parameters):

<!-- prettier-ignore -->
|Stage|Input Data Place Holder|
|---|---|
|**Stage**|**Input Data Place Holder**|
|Internal stage|`@my_int_stage`|
|External stage|`@my_int_stage/path/file.csv`|
|Amazon S3 bucket|`s3://mybucket/data/files`|
|Google Cloud Storage|`gcs://mybucket/data/files`|
|Microsoft Azure|`azure://myaccount.blob.core.windows.net/mycontainer/data/files`|

If this is the case, please manually add the additional parameter
`input_data_place_holder="<cloud_provider_path>"` in the `import_file_to_table` function. For
example:

```
BeginLoading.import_file_to_table(
  f"""TESTS.EmpLoad4""",
  ssc_define_columns,
  ssc_define_file,
  ssc_begin_loading_columns,
  ssc_begin_loading_values,
  ssc_set_record,
  input_data_place_holder="s3://mybucket/data/files")
```

### END LOADING[¶](#end-loading)

The `END LOADING` command is commented out since is not necessary for the transformation of the
`BEGIN LOADING`.

**Teradata (FastLoad)**

```
END LOADING;
```

**Snowflake (Python)**

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
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. END LOADING **
  #END LOADING

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

### Known Issues[¶](#id3)

**1. BINARY and TEXT keyword specification not supported**

The `BINARY` and `TEXT` keyword specification for the `SET RECORD` command are not yet supported.

**2. Only base specification for VARTEXT is supported**

Extra specifications for the `SET RECORD VARTEXT` such as `TRIM` or `QUOTE` are not yet supported.

### Related EWIs[¶](#id4)

1. [SSC-FDM-0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0007):
   Element with missing dependencies.
2. [SSC-FDM-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027):
   Removed next statement, not applicable in SnowFlake.
3. [SSC-EWI-0021](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0021):
   Not supported.
4. [SSC-FDM-TD0022](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0022):
   Shell variables found, running this code in a shell script is required.
