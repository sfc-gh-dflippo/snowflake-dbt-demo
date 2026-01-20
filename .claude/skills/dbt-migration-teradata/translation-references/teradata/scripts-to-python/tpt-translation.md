---
description: This section illustrates TPT translation from Teradata to Snowflake.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/scripts-to-python/tpt-translation
title: SnowConvert AI - Teradata - TPT | Snowflake Documentation
---

## TPT statements transformation[¶](#tpt-statements-transformation)

All TPT statements, like other Teradata scripting languages, are being converted to python code.
Here are some examples of transformations already supported.

### Define Job header transformation[¶](#define-job-header-transformation)

The job statement is translated to a python class with all the statements like operators, schema
definitions, and steps inside of it.

Source code

```
 /* Some comments on the job  */
DEFINE JOB LOADJOB
DESCRIPTION 'LOAD AC_SCHEMA TABLE FROM A FILE'
JobBody
```

Translated code

```
 # Some comments on the job
class LOADJOB:
    # DESCRIPTION 'LOAD AC_SCHEMA TABLE FROM A FILE'
    JobBody
```

### Define Schema transformation[¶](#define-schema-transformation)

The schema statement is translated to an attribute in the class created for the job statement.

Source code

```
 DEFINE SCHEMA DCS_SCHEMA
DESCRIPTION 'DCS DATA'
(
PNRHEADER_ID   PERIOD(DATE),
PNRLOCPERIOD   PERIOD(TIMESTAMP(0)),
CRTDATE        CLOB,
REQTYP         JSON(100000),
seqno          INTEGER,
resdata        INTEGER
);
```

Translated code

```
 class JOBNAME:
    DCS_SCHEMA = """(
    PNRHEADER_ID VARCHAR(24),
    PNRLOCPERIOD VARCHAR(58),
    CRTDATE VARCHAR /*** MSC-WARNING - SSC-FDM-TD0002 - COLUMN CONVERTED FROM CLOB DATA TYPE ***/,
    REQTYP VARIANT,
    seqno INTEGER,
    resdata INTEGER,
    );"""
```

### Define Operator transformation[¶](#define-operator-transformation)

The operators are translated to python functions inside the class generated for the job. The
examples provided are the operators that SnowConvert AI currently supports

#### DDL Operator[¶](#ddl-operator)

Source code for DDL operator

```
 DEFINE OPERATOR DDL_OPERATOR()
DESCRIPTION 'TERADATA PARALLEL TRANSPORTER DDL OPERATOR'
TYPE DDL
ATTRIBUTES
(
  VARCHAR PrivateLogName ,
  VARCHAR TdpId          = @MyTdpId,
  VARCHAR UserName       = @MyUserName,
  VARCHAR UserPassword   = 'SomePassWord',
  VARCHAR AccountID,
  VARCHAR ErrorList      = ['3807','2580']
);
```

Translated code

```
 class JobName:
    def DDL_OPERATOR(self):
        #'TERADATA PARALLEL TRANSPORTER DDL OPERATOR'
        global args
        self.con = log_on(user = args.MyUserName, password = 'SomePassWord')
```

#### UPDATE Operator[¶](#update-operator)

Source code for UPDATE operator

```
 DEFINE OPERATOR LOAD_OPERATOR()
DESCRIPTION 'TERADATA PARALLEL TRANSPORTER LOAD OPERATOR'
TYPE UPDATE
SCHEMA AC_MASTER_SCHEMA
ATTRIBUTES
(
    VARCHAR PrivateLogName ,
    INTEGER MaxSessions       =  32,
    INTEGER MinSessions       =  1,
    VARCHAR TargetTable       = '&TARGET_TABLE',
    VARCHAR TdpId             = @MyTdpId,
    VARCHAR UserName          = @MyUserName,
    VARCHAR UserPassword      = @MyPassword,
    VARCHAR AccountId,
    VARCHAR ErrorTable1       = '&LOG_DB_NAME.ERR1',
    VARCHAR ErrorTable2       = '&LOG_DB_NAME.ERR2',
    VARCHAR LogTable          = '&LOG_DB_NAME.LOG_TABLE'
);
```

Translated code

```
 class JobName:
    def LOAD_OPERATOR(self, query):
        #'TERADATA PARALLEL TRANSPORTER LOAD OPERATOR'
        #USES SCHEMA AC_MASTER_SCHEMA
        operator_name = "LOAD_OPERATOR"
        return query
```

#### DATA CONNECTOR PRODUCER Operator[¶](#data-connector-producer-operator)

Source code for Data Connector Producer operator

```
 DEFINE OPERATOR FILE_READER()
DESCRIPTION 'TERADATA PARALLEL TRANSPORTER DATA CONNECTOR OPERATOR'
TYPE DATACONNECTOR PRODUCER
SCHEMA AC_MASTER_SCHEMA
ATTRIBUTES
(
  VARCHAR PrivateLogName ,
  VARCHAR DirectoryPath   = '&INPUTFILEPATH' ,
  VARCHAR FileName        = '&INPUTTEXTFILE' ,
  VARCHAR Format          = 'delimited',
  VARCHAR OpenMode        = 'Read',
  VARCHAR TextDelimiter     = '~',
  VARCHAR IndicatorMode   = 'N'
);
```

Translated code

```
 class JobName:
    def FILE_READER(self):
        #'TERADATA PARALLEL TRANSPORTER DATA CONNECTOR OPERATOR'
        #USES SCHEMA AC_MASTER_SCHEMA
        operator_name = "FILE_READER"
        stage_name = f"{self.jobname}_{operator_name}"
        format_name = f"{self.jobname}_{operator_name}_FILEFORMAT"
        exec(f"""CREATE OR REPLACE FILE FORMAT {format_name} TYPE = 'CSV' FIELD_DELIMITER = '~' TRIM_SPACE = TRUE SKIP_HEADER = 0""")
        exec(f"""CREATE STAGE IF NOT EXISTS {self.jobname}_STAGE""")
        exec(f"""PUT file://{INPUTFILEPATH}/{INPUTTEXTFILE} @{stage_name} OVERWRITE = TRUE AUTO_COMPRESS = FALSE;""")
        temp_table_name = f"{self.jobname}_{operator_name}_TEMP"
        exec(f"""DROP TABLE IF EXISTS {temp_table_name}""")
        exec(f"""CREATE TEMPORARY TABLE {temp_table_name} {self.AC_MASTER_SCHEMA}""")
        exec(f"""COPY INTO {temp_table_name} FROM @{stage_name} FILE_FORMAT = (format_name = '{format_name}')""")
        return temp_table_name
```

### Define step transformation[¶](#define-step-transformation)

Steps are too translated to python functions inside the class generated for the job, they will be
called in the main function of the translated code.

Step source code

```
 STEP setup_tables
(
  APPLY
  ('DELETE FROM  &STAGE_DB_NAME.EMS_AC_MASTER_STG;')
   TO OPERATOR (DDL_OPERATOR() );
);

STEP stLOAD_FILE_NAME
(
  APPLY
  ('INSERT INTO CRASHDUMPS.EMP_NAME
  (EMP_NAME, EMP_YEARS, EMP_TEAM)
  VALUES
  (:EMP_NAME, :EMP_YEARS, :EMP_TEAM);')
  TO OPERATOR (ol_EMP_NAME() [1])
  SELECT * FROM OPERATOR(op_EMP_NAME);
);
```

Translated code

```
 def setup_tables(self):
    self.DDL_OPERATOR()
    exec(f"""DELETE FROM DATABASE1.{STAGE_DB_NAME}.EMS_AC_MASTER_STG""")

def stLOAD_FILE_NAME(self):
    exec(f"""INSERT INTO DATABASE1.CRASHDUMPS.EMP_NAME (EMP_NAME, EMP_YEARS, EMP_TEAM)
SELECT EMP_NAME, EMP_YEARS, EMP_TEAM
FROM (
{self.ol_EMP_NAME('SELECT * FROM ' + self.op_EMP_NAME() )})""")
```

### Main function[¶](#main-function)

The main function is always generated for any scripting language, for TPT the main function contains
an instance of the job class and calls to the steps in the job

Main function sample code

```
 def main():
  _LOADJOB = LOADJOB()
  _LOADJOB.setup_tables()
  _LOADJOB.stLOAD_FILE_NAME()
  snowconvert.helpers.quit_application()
```
