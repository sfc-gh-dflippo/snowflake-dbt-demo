---
description: Translation references to convert Teradata MLOAD files to Python
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-python/multiload-translation
title: SnowConvert AI - Teradata - MLOAD | Snowflake Documentation
---

## MultiLoad Commands Translation[¶](#multiload-commands-translation)

Most of the
[MultiLoad Commands](https://docs.teradata.com/reader/u5g65Je3hpMChJXfDyt1hg/KRpA6tp8QD64m48~ng0PFw)
are considered not relevant in Snowflake, these commands are commented out. Below is the summary
list of MultiLoad commands and their transformation status into Snowflake:

<!-- prettier-ignore -->
|Commands|Transformation Status|Note|
|---|---|---|
|ACCEPT|Commented|​|
|[BEGIN MLOAD](begin-mload.md)|**Transformed**|​​The node is commented out since the transformation occurs in other related statements instead.|
|BEGIN DELETE MLOAD|Commented|​|
|DATEFORM|Commented|​|
|DELETE|**Partially transformed**|Check [known issues](begin-mload.md#known-issues).​|
|DISPLAY|Commented|​|
|[DML LABEL](begin-mload.md#.dml-label)|**Transformed**|​|
|END MLOAD|**Transformed**|​​Commented out since is not necessary for the transformation of the BEGIN MLOAD.|
|EOC|Commented|​|
|[FIELD](begin-mload.md#.layout-.field-and-.filler)|**Transformed**|​|
|[FILLER](begin-mload.md#.layout-.field-and-.filler)|**Transformed**|This command needs to be with a FIELD and LAYOUT command to be converted.|
|IF, ELSE, and ENDIF|Commented|​|
|[IMPORT](begin-mload.md#.import)|**Transformed**|​|
|INSERT|**Transformed**|This is taken as a Teradata Statement, so it doesn't appear in this chapter.|
|[LAYOUT](begin-mload.md#.layout-.field-and-.filler)|**Transformed**|This command needs to be with a FIELD and FILLER command to be converted.|
|LOGDATA|Commented|​|
|LOGMECH|Commented|​|
|LOGOFF|Commented|​|
|LOGON|Commented|​|
|LOGTABLE|Commented|​|
|PAUSE ACQUISITION|Commented|​|
|RELEASE MLOAD|Commented|​|
|ROUTE MESSAGES|Commented|​|
|RUN FILE|Commented|​|
|SET|Commented|​|
|SYSTEM|Commented|​|
|TABLE|Commented|​|
|UPDATE|**Transformed**|This is taken as a Teradata Statement, so it doesn't appear in this chapter.|
|VERSION|Commented|​|

However, there are some exceptional commands that must be converted into Python-specific code for
them to work as intended in Snowflake. See this [section](#begin-mload).

If you have any additional questions regarding this documentation, you can email us at
[snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com).

## BEGIN MLOAD[¶](#begin-mload)

The transformation for the command `.BEGIN MLOAD` is a multi-part transformation that requires the
`.LAYOUT`, `.FIELD`, `.FILLER`,`.DML LABEL`, and `.IMPORT` commands to simulate its behavior
correctly.

This transformation is fully explained in the following subsections.

### .LAYOUT, .FIELD and .FILLER[¶](#layout-field-and-filler)

The transformation for the commands `.LAYOUT`, `.FIELD`, and `.FILLER` will create variable
definitions to be used in a future function call of the IMPORT of this layout.

**Teradata (MultiLoad)**

```
.LAYOUT INFILE_LAYOUT;
.FIELD TABLE_ID        * INTEGER;
.FIELD TABLE_DESCR     * CHAR(8);
.FILLER COL1           * CHAR(1);
.FIELD TABLE_NBR       * SMALLINT;
.FIELD TABLE_SOMEFIELD * SMALLINT;
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
  INFILE_LAYOUT_TableName = "INFILE_LAYOUT_TEMP_TABLE"
  INFILE_LAYOUT_Columns = """TABLE_ID INTEGER,
TABLE_DESCR CHAR(8),
COL1 CHAR(1),
TABLE_NBR SMALLINT,
TABLE_SOMEFIELD SMALLINT"""
  INFILE_LAYOUT_Conditions = """TABLE_ID AS TABLE_ID, TABLE_DESCR AS TABLE_DESCR, COL1 AS COL1, TABLE_NBR AS TABLE_NBR, TABLE_SOMEFIELD AS TABLE_SOMEFIELD"""
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

### .DML LABEL[¶](#dml-label)

The transformation for the `.DML LABEL`command will create a function containing the statements
after the label definition. Note that after the `.DML LABEL` command there is usually an `Insert`,
`Update` or `Delete`.

**Teradata (MultiLoad)**

```
-- Example of .DML LABEL with INSERT:
.DML LABEL INSERT_TABLE;
INSERT INTO mydb.mytable( TABLE_ID,TABLE_DESCR,TABLE_NBR ) VALUES( :TABLE_ID,:TABLE_DESCR,:TABLE_NBR );

-- Example of .DML LABEL with DELETE:
.DML LABEL DELETE_TABLE;
DELETE FROM Employee WHERE EmpNo  = :EmpNo;

-- Example of .DML LABEL with an UPDATE, followed by an INSERT:
.DML LABEL UPSERT_TABLE DO INSERT FOR MISSING UPDATE ROWS;
UPDATE   mydb.mytable SET TABLE_ID = :TABLE_ID WHERE TABLE_DESCR = :somedescription
INSERT INTO mydb.mytable(TABLE_ID, TABLE_DESCR, TABLE_NBR) VALUES(:TABLE_ID, :TABLE_DESCR, :TABLE_NBR );
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
  def INSERT_TABLE(tempTableName, queryConditions = ""):
    exec(f"""INSERT INTO mydb.mytable (TABLE_ID, TABLE_DESCR, TABLE_NBR)
SELECT
   :TABLE_ID,
   :TABLE_DESCR,
   :TABLE_NBR
FROM {tempTableName} SRC {queryConditions}""")
  exec("""
    DELETE FROM
      Employee
    WHERE
      EmpNo = :EmpNo
    """)
  def UPSERT_TABLE(tempTableName, queryConditions = ""):
    exec(f"""MERGE INTO mydb.mytable TGT USING (SELECT * FROM {tempTableName} {queryConditions}) SRC ON TABLE_DESCR = :somedescription
WHEN MATCHED THEN UPDATE SET
   TABLE_ID = :TABLE_ID
WHEN NOT MATCHED THEN INSERT (TABLE_ID, TABLE_DESCR, TABLE_NBR)
VALUES (:TABLE_ID, :TABLE_DESCR, :TABLE_NBR)""")
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

### .IMPORT[¶](#import)

The transformation of the `.IMPORT` command will create a call to
the`import_file_to_temptable`helper to load the data from the file to a temporary table. Then, the
calls to all the`APPLY`labels used in the original import will be created. Finally, the calls for
an`INSERT`label will be transformed to a query parameter and optionally can have a query condition.

**Teradata (MultiLoad)**

```
.IMPORT INFILE INFILE_FILENAME
    LAYOUT INFILE_LAYOUT
    APPLY INSERT_TABLE
    APPLY UPSERT_TABLE
    Apply DELETE_TABLE;
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
  #.IMPORT INFILE INFILE_FILENAME LAYOUT INFILE_LAYOUT APPLY INSERT_TABLE APPLY UPSERT_TABLE Apply DELETE_TABLE

  snowconvert.helpers.import_file_to_temptable(fr"INFILE_FILENAME", INFILE_LAYOUT_TableName, INFILE_LAYOUT_Columns, INFILE_LAYOUT_Conditions, ',')
  INSERT_TABLE(INFILE_LAYOUT_TableName)
  UPSERT_TABLE(INFILE_LAYOUT_TableName)
  DELETE_TABLE(INFILE_LAYOUT_TableName)
  exec(f"""DROP TABLE {INFILE_LAYOUT_TableName}""")
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

### Large Example[¶](#large-example)

Given the transformations shown above for a variety of commands, consider the following example.

With this input data:

```
id,name,age
1,John,25
2,Maria,29
3,Carlos,31
4,Mike,40
5,Laura,27
```

**Teradata (MultiLoad)**

**Query**

```
.begin import mload
        tables
	mySampleTable1
sessions 20
ampcheck none;

.layout myLayOut;
 .field ID * VARCHAR(2) NULLIF ID = '1';
 .field NAME * VARCHAR(25);
 .field AGE * VARCHAR(10);
.dml label insert_data;

INSERT INTO mySampleTable1
 (
    ID,
    NAME,
    AGE
 )
VALUES
 (
    :ID,
    SUBSTRING(:NAME FROM 2),
    :AGE
 );

.import infile sampleData.txt
layout myLayOut
apply insert_data

.end mload;
.logoff;
```

**Result**

<!-- prettier-ignore -->
|ROW|ID|NAME|AGE|
|---|---|---|---|
|1|NULL|ohn|25|
|2|2|aria|29|
|3|3|arlos|31|
|4|4|ike|40|
|5|5|aura|27|

**Snowflake (Python)**

**Query**

```
#*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***
#** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "mySampleTable1" **

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
  #.begin import mload tables mySampleTable1 sessions 20 ampcheck none

  myLayOut_TableName = "myLayOut_TEMP_TABLE"
  myLayOut_Columns = """ID VARCHAR(2),
NAME VARCHAR(25),
AGE VARCHAR(10)"""
  myLayOut_Conditions = """CASE
   WHEN UPPER(RTRIM(ID)) = UPPER(RTRIM('1'))
      THEN NULL
   ELSE ID
END AS ID, NAME AS NAME, AGE AS AGE"""
  def insert_data(tempTableName, queryConditions = ""):
    exec(f"""INSERT INTO mySampleTable1 (ID, NAME, AGE)
SELECT
   SRC.ID,
   SUBSTRING(SRC.NAME, 2),
   SRC.AGE
FROM {tempTableName} SRC {queryConditions}""")
  #** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. TRANSLATED BELOW **
  #.import infile sampleData.txt layout myLayOut apply insert_data

  snowconvert.helpers.import_file_to_temptable(fr"sampleData.txt", myLayOut_TableName, myLayOut_Columns, myLayOut_Conditions, ',')
  insert_data(myLayOut_TableName)
  exec(f"""DROP TABLE {myLayOut_TableName}""")

  if con is not None:
    con.close()
    con = None
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

**Result**

<!-- prettier-ignore -->
|ROW|ID|NAME|AGE|
|---|---|---|---|
|1|NULL|ohn|25|
|2|2|aria|29|
|3|3|arlos|31|
|4|4|ike|40|
|5|5|aura|27|

### Known Issues[¶](#known-issues)

**1. Delete statement is partially supported**

The `DELETE` statement is partially supported since the where conditions, when found, are not being
converted correctly if pointing to a `LAYOUT` defined column.

In the example below, `:EmpNo` is pointing to a `LAYOUT` defined column. However, the transformation
does not take this into account and thus the code will be referencing a column that does not exists.

```
  exec("""
    DELETE FROM
      Employee
    WHERE
      EmpNo = :EmpNo
    """)
```

If you have any additional questions regarding this documentation, you can email us at
[snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com).

### Related EWIs [¶](#related-ewis)

1. [SSC-FDM-0027](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0027):
   Removed next statement, not applicable in SnowFlake.
