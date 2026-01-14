---
description: SQL Server
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-built-in-functions
title: SnowConvert AI - SQL Server-Azure Synapse - Built-in functions | Snowflake
---

## Aggregate[¶](#aggregate)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|TransactSQL|Snowflake|Notes|
|APPROX_COUNT_DISTINCT|APPROX_COUNT_DISTINCT||
|AVG​|AVG||
|CHECKSUM_AGG|_\*to be defined_||
|COUNT|COUNT||
|COUNT_BIG|_\*to be defined_||
|GROUPING|GROUPING||
|GROUPING_ID|GROUPING_ID||
|MAX|MAX||
|MIN|MIN||
|STDEV|STDDEV, STDEV_SAMP||
|STDEVP|STDDEV_POP||
|SUM|SUM||
|VAR|VAR_SAMP||
|VARP|VAR_POP​||

## Analytic[¶](#analytic)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|CUME_DIST|CUME_DIST||
|FIRST_VALUE|FIRST_VALUE||
|LAG|LAG||
|LAST_VALUE|LAST_VALUE||
|LEAD|LEAD||
|PERCENTILE_CONT|PERCENTILE_CONT||
|PERCENTILE_DISC|PERCENTILE_DISC||
|PERCENT_RANK|PERCENT_RANK||

## Collation[¶](#collation)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|COLLATIONPROPERTY|_\*to be defined_||
|TERTIARY_WEIGHTS|_\*to be defined_||

## Configuration[¶](#configuration)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|​@@DBTS|_\*to be defined_||
|@@LANGID|_\*to be defined_||
|@@LANGUAGE|_\*to be defined_||
|@@LOCK_TIMEOUT|_\*to be defined_||
|@@MAX_CONNECTIONS|_\*to be defined_||
|@@MAX_PRECISION|_\*to be defined_||
|@@NESTLEVEL|_\*to be defined_||
|@@OPTIONS|_\*to be defined_||
|@@REMSERVER|_\*to be defined_||
|@@SERVERNAME|CONCAT(’[app.snowflake.com](http://app.snowflake.com/)’, CURRENT_ACCOUNT( ))||
|@@SERVICENAME|_\*to be defined_||
|@@SPID|_\*to be defined_||
|@@TEXTSIZE|_\*to be defined_||
|@@VERSION|_\*to be defined_|Can be mimicked by using CURRENT_VERSION|

## Conversion[¶](#conversion)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|CAST|CAST|Returns NULL if the value isn’t a number, otherwise returns the numeric value as its. When using operators such as <, >, =, <> then must be follow by a NULL|
|CONVERT|Check [CONVERT](#convert)|Same behavior as CAST|
|PARSE|_\*to be defined_||
|TRY_CAST|TRY_CAST|Returns NULL if the value isn’t a number, otherwise returns the numeric value as its. When using operators such as <, >, =, <> then must be follow by a NULL|
|[TRY_CONVERT](#try-convert)|_\*to be defined_|Same behavior as TRY_CAST|
|TRY_PARSE|TRY_CAST|Behavior may be different when parsing an integer as date or timestamp.|

## Cryptographic[¶](#cryptographic)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|ASYMKEY_ID|_\*to be defined_||
|ASYMKEYPROPERTY|_\*to be defined_||
|CERTENCODED|_\*to be defined_||
|CERTPRIVATEKEY|_\*to be defined_||
|DECRYPTBYASYMKEY|_\*to be defined_||
|DECRYPTBYCERT|_\*to be defined_||
|DECRYPTBYKEY|_\*to be defined_||
|DECRYPTBYKEYAUTOASYMKEY|_\*to be defined_||
|DECRYPTBYKEYAUTOCERT|_\*to be defined_||
|DECRYPTBYPASSPHRASE|\_\*to be defined_​|Can be mimicked by using DENCRYPT_RAW|
|ENCRYPTBYASYMKEY|_\*to be defined_||
|ENCRYPTBYCERT|_\*to be defined_||
|ENCRYPTBYKEY|_\*to be defined_||
|ENCRYPTBYPASSPHRASE|_\*to be defined_|Can be mimicked by using ENCRYPT_RAW|
|HASHBYTES|**MD5, SHA1, SHA2**|Currently only supported separated hash. Use proper one according to the required algorithm **MD5**, is a 32-character hex-encoded **SHA1**, has a 40-character hex-encoded string containing the 160-bit **SHA2**, a hex-encoded string containing the N-bit SHA-2 message digest. Sizes are: 224 = SHA-224 256 = SHA-256 (Default) 384 = SHA-384 512 = SHA-512|
|IS_OBJECTSIGNED|_\*to be defined_||
|KEY_GUID|_\*to be defined_||
|KEY_ID|_\*to be defined_||
|KEY_NAME|_\*to be defined_||
|SIGNBYASYMKEY|_\*to be defined_||
|SIGNBYCERT|_\*to be defined_||
|SYMKEYPROPERTY|_\*to be defined_||
|VERIGYSIGNEDBYCERT|_\*to be defined_||

## Cursor[¶](#cursor)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|@@CURSOR_ROWS|_\*to be defined_|​|
|@@FETCH_STATUS|_\*to be defined_||
|CURSOR_STATUS|_\*to be defined_||

## Data type[¶](#data-type)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|DATALENGTH|OCTET_LENGTH|​Snowflake doesn’t use fractional bytes so length is always calculated as 8 \* OCTET_LENGTH|
|IDENT_SEED|_\*to be defined_||
|IDENT_CURRENT|_\*to be defined_||
|IDENTITY|_\*to be defined_||
|IDENT_INCR|_\*to be defined_||
|SQL_VARIANT_PROPERTY|_\*to be defined_||

## Date & Time[¶](#date-time)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|@@DATEFIRST|_\*to be defined_||
|@@LANGUAGE|_\*to be defined_||
|CURRENT_TIMESTAMP|CURRENT_TIMESTAMP||
|CURRENT_TIMEZONE|_\*to be defined_||
|DATEADD|DATEADD||
|DATEDIFF|DATEDIFF||
|DATEDIFF_BIG|_\*to be defined_||
|DATEFROMPARTS|DATE_FROM_PARTS||
|DATENAME|_\*to be defined_|This function receives two arguments: a datepart and date. It returns a string. Here are the supported dateparts from TSQL to Snowflake **year, yyyy, yy** -> DATE_PART(YEAR, “$date”) **quarter, qq, q** -> DATE\_PART(QUARTER, “$date”) **month, mm, m** -> **MONTHNAME**( “$date”), thou only providing a three-letter english month name **dayofyear, dy, y** -> DATE\_PART(DAYOFYEAR, “$date”) **day, dd, d** -> DATE_PART(DAY, “$date”) **week, wk, ww** -> DATE\_PART(WEEK, “$date”) **weekday, dw** -> **DAYNAME**(“$date”), thou only providing an three-letter english day name **hour, hh** -> DATE\_PART(HOUR, “$date”) **minute, n** -> DATE_PART(MINUTE, “$date”) **second, ss, s** -> DATE\_PART(SECOND, “$date”) **millisecond, ms** -> DATE_PART(MS, “$date”) **microsecond, mcs** -> DATE\_PART(US, “$date”) **nanosecond, ns** -> DATE_PART(NS, “$date”) **TZoffset, tz** -> needs a special implementation to get the time offset|
|DATEPART|DATE_PART||
|DATETIME2FROMPARTS|_\*to be defined_||
|DATETIMEFROMPARTS|_\*to be defined_|​Can be mimicked by using a combination of **DATE_FROM_PARTS and TIME_FROM_PARTS**|
|DATETIMEOFFSETFROMPARTS|_\*to be defined_||
|DAY|DAY||
|EOMONTH|_\*to be defined_|Can be mimicked by using **LAST_DAY**|
|GETDATE|GETDATE||
|GETUTCDATE|_\*to be defined_|Can be mimicked by using **CONVERT_TIMEZONE**|
|ISDATE|_\*to be defined_|Can be mimicked by using **TRY_TO_DATE** Returns NULL if the value isn’t a **date**, otherwise returns the date value as its. When using operators such as <, >, =, <> then must be follow by a NULL|
|MONTH|MONTH||
|SMALLDATETIMEFROMPARTS|_\*to be defined_|​​Can be mimicked by using a combination of **DATE_FROM_PARTS and TIME_FROM_PARTS**|
|SWITCHOFFSET|_\*to be defined_|​Can be mimicked by using **CONVERT_TIMEZONE**|
|SYSDATETIME|LOCALTIME||
|SYSDATETIMEOFFSET|_\*to be defined_|​Can be mimicked by using **CONVERT_TIMEZONE and LOCALTIME**|
|SYSUTCDATETIME|_\*to be defined_|​​Can be mimicked by using **CONVERT_TIMEZONE and LOCALTIME**|
|TIMEFROMPARTS|TIME_FROM_PARTS|​|
|TODATETIMEOFFSET|_\*to be defined_|​Can be mimicked by using **CONVERT_TIMEZONE**|
|YEAR|YEAR||

## JSON[¶](#json)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|ISJSON|CHECK_JSON|​This is a ‘preview feature’ in Snowflake|
|JSON_VALUE|_\*to be defined_|Can be mimic by using TO_VARCHAR(GET_PATH(PARSE_JSON(JSON), PATH))|
|JSON_QUERY|_\*to be defined_||
|JSON_MODIFY|_\*to be defined_||

## Mathematical[¶](#mathematical)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|ABS|ABS||
|ACOS|ACOS||
|ASIN|ASIN||
|ATAN|ATAN||
|ATN2|ATAN2||
|CEILING|CEIL||
|COS|COS||
|COT|COT||
|DEGREES|DEGREES||
|EXP|EXP||
|FLOOR|FLOOR||
|LOG|LN||
|LOG10|LOG||
|PI|PI||
|POWER|POWER||
|RADIANS|RADIANS||
|RAND|RANDOM||
|ROUND|ROUND||
|SIGN|SIGN||
|SIN|SIN||
|SQRT|SQRT||
|SQUARE|SQUARE||

## Logical[¶](#logical)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|CHOOSE|_\*to be defined_|Can be mimic by using DECODE|
|GREATEST|GREATEST||
|IIF|IIF||
|LEAST|LEAST||
|NULLIF|NULLIF||

## Metadata[¶](#metadata)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|---|---|
|TransactSQL|Snowflake|Notes|
|@@PROCID|_\*to be defined_||
|APP_NAME|_\*to be defined_||
|APPLOCK_MODE|_\*to be defined_||
|APPLOCK_TEST|_\*to be defined_||
|ASSEMBLYPROPERTY|_\*to be defined_||
|COL_LENGTH|A UDF named COL_LENGTH_UDF is provided to retrieve this information. This UDF works only with VARCHAR types, as specified in the Transact-SQL documentation. For other data types, it returns NULL.||
|COL_NAME|_\*to be defined_||
|COLUMNPROPERTY|_\*to be defined_||
|DATABASE_PRINCIPAL_ID|_\*to be defined_|Maps to CURRENT_USER when no args|
|DATABASEPROPERTYEX|_\*to be defined_||
|DB_ID|_\*to be defined_|We recommend changing to CURRENT_DATABASE(). If there is a need to emulate this functionality. SELECT DATE_PART(EPOCH,CREATED) FROM INFORMATION_SCHEMA.DATABASES WHERE DATABASE_NAME = ‘DB’ ; Can achieve something similar|
|DB_NAME|_\*to be defined_|Mostly used in the procedurename mentioned above|
|FILE_ID|_\*to be defined_||
|FILE_IDEX|_\*to be defined_||
|FILE_NAME|_\*to be defined_||
|FILEGROUP_ID|_\*to be defined_||
|FILEGROUP_NAME|_\*to be defined_||
|FILEGROUPPROPERTY|_\*to be defined_||
|FILEPROPERTY|_\*to be defined_||
|FULLTEXTCATALOGPROPERTY|_\*to be defined_||
|FULLTEXTSERVICEPROPERTY|_\*to be defined_||
|INDEX_COL|_\*to be defined_||
|INDEXKEY_PROPERTY|_\*to be defined_||
|INDEXPROPERTY|_\*to be defined_||
|NEXT VALUE FOR|_\*to be defined_||
|OBJECT_DEFINITION|_\*to be defined_||
|OBJECT_ID|_\*to be defined_|In most cases can be replaced. Most cases are like: IF OBJECT_ID(‘dbo.TABLE’) IS NOT NULL DROP TABLE dbo.Table which can be replaced by a DROP TABLE IF EXISTS (this syntax is also supported in SQL SERVER). If the object_id needs to be replicated, a UDF is added depending on the second parameter of the function call.|
|OBJECT_NAME|_\*to be defined_|Can be replaced by: CREATE OR REPLACE PROCEDURE FOO() RETURNS STRING LANGUAGE JAVASCRIPT AS ‘ var rs = snowflake.execute({sqlText:`SELECT CURRENT_DATABASE()|'.'|?`, binds:[arguments.callee.name]}); rs.next(); var procname = rs.getColumnValue(1); return procname; ‘;|
|OBJECT_NAME(@@PROCID)|‘ObjectName’|This transformation only occurs when it is inside a DeclareStatement. ObjectName is the name of the TopLevelObject that contains the Function.|
|OBJECT_SCHEMA_NAME|_\*to be defined_||
|OBJECT_SCHEMA_NAME(@@PROCID)|:OBJECT_SCHEMA_NAME|This transformation only occurs when it is inside a DeclareStatement.|
|OBJECTPROPERTY|_\*to be defined_||
|OBJECTPROPERTYEX|_\*to be defined_||
|ORIGINAL_DB_NAME|_\*to be defined_||
|PARSENAME|PARSENAME_UDF|It creates a UDF to emulate the same behavior of Parsename function.|
|_\*to be defined_|||
|SCHEMA_NAME|_\*to be defined_||
|SCOPE_IDENTITY|_\*to be defined_|It this is needed I would recommend to use sequences, and capture the value before insert|
|SERVERPROPERTY|_\*to be defined_||
|STATS_DATE|_\*to be defined_||
|TYPE_ID|_\*to be defined_||
|TYPE_NAME|_\*to be defined_||
|TYPEPROPERTY|_\*to be defined_||
|VERSION|_\*to be defined_||

## Ranking[¶](#ranking)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|DENSE_RANK|DENSE_RANK||
|NTILE|NTILE||
|RANK|RANK||
|ROW_NUMBER|ROW_NUMBER||

## Replication[¶](#replication)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|PUBLISHINGSERVERNAME|_\*to be defined_||

## Rowset[¶](#rowset)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|OPENDATASOURCE|_\*to be defined_||
|OPENJSON|_\*to be defined_||
|QPENQUERY|_\*to be defined_||
|OPENROWSET|_\*to be defined_||
|OPENXML|OPENXML_UDF|User-defined function used as a equivalent behavior in Snowflake.|
|STRING_SPLIT|SPLIT_TO_TABLE|The enable_ordinal flag in Transact-SQL’s STRING_SPLIT is not directly supported by Snowflake’s SPLIT_TO_TABLE function. If the ordinal column is required, a user-defined function (UDF) named STRING_SPLIT_UDF will be generated to replicate this behavior. Without the ordinal column, note that STRING_SPLIT returns a single column named value, while SPLIT_TO_TABLE returns three columns: value, index (equivalent to ordinal), and seq. For additional details, see the [SPLIT_TO_TABLE documentation](https://docs.snowflake.com/en/sql-reference/functions/split_to_table).|

## Security[¶](#security)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|CERTENCODED|_\*to be defined_||
|CERTPRIVATEKEY|_\*to be defined_||
|CURRENT_USER|CURRENT_USER||
|DATABASE_PRINCIPAL_ID|_\*to be defined_||
|HAS_PERMS_BY_NAME|_\*to be defined_||
|IS_MEMBER|_\*to be defined_|Change to query INFORMATION_SCHEMA although the client might require defining new roles|
|IS_ROLEMEMBER|_\*to be defined_|Snowflake’s a similar function **IS_ROLE_IN_SESSION**|
|IS_SRVROLEMEMBER|_\*to be defined_||
|LOGINPROPERTY|_\*to be defined_||
|ORIGINAL_LOGIN|_\*to be defined_||
|PERMISSIONS|_\*to be defined_||
|PWDCOMPARE|_\*to be defined_||
|PWDENCRYPT|_\*to be defined_||
|SCHEMA_ID|_\*to be defined_||
|SCHEMA_NAME|_\*to be defined_||
|SESSION_USER|_\*to be defined_||
|SUSER_ID|_\*to be defined_||
|SUSER_NAME|_\*to be defined_||
|SUSER_SID|_\*to be defined_||
|SUSER_SNAME|_\*to be defined_||
|sys.fn_builtin_permissions|_\*to be defined_||
|sys.fn_get_audit_file|_\*to be defined_||
|sys.fn_my_permissions|_\*to be defined_||
|SYSTEM_USER|_\*to be defined_||
|USER_ID|_\*to be defined_||
|USER_NAME|_\*to be defined_|Maps to CURRENT_USER|

## String[¶](#string)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|ASCII|ASCII||
|CHAR|CHR, CHAR||
|CHARINDEX|CHARINDEX||
|CONCAT|CONCAT||
|CONCAT_WS|CONCAT_WS||
|COALESCE|COALESCE||
|DIFFERENCE|_\*to be defined_||
|FORMAT|TO_CHAR|The SSC-EWI-0006 or SSC-FDM-0036 could be generated when the format (numeric or date time) is not fully supported.|
|LEFT|LEFT||
|LEN|LEN||
|LOWER|LOWER||
|LTRIM|LTRIM||
|NCHAR|_\*to be defined_||
|PATINDEX|_\*to be defined_|Map to REGEXP_INSTR|
|QUOTENAME|QUOTENAME_UDF|It creates a UDF to emulate the same behavior of Quotename function|
|REPLACE|REPLACE||
|REPLICATE|REPEAT||
|REVERSE|REVERSE||
|RIGHT|RIGHT||
|RTRIM|RTRIM||
|SOUNDEX|SOUNDEX||
|SPACE|_\*to be defined_||
|STR|_\*to be defined_||
|STRING_AGG|_\*to be defined_||
|STRING_ESCAPE|_\*to be defined_||
|STRING_SPLIT|SPLIT_TO_TABLE||
|STUFF|_\*to be defined_|CREATE OR REPLACE FUNCTION STUFF(S string, STARTPOS int, LENGTH int, NEWSTRING string) RETURNS string LANGUAGE SQL AS ‘ left(S, STARTPOS)|
|SUBSTRING|SUBSTRING||
|TRANSLATE|TRANSLATE||
|TRIM|TRIM||
|UNICODE|UNICODE||
|UPPER|UPPER||

## System[¶](#system)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|$PARTITION|_\*to be defined_||
|@@ERROR|_\*to be defined_||
|@@IDENTITY|_\*to be defined_|It this is needed I would recommend to use sequences, and capture the value before insert|
|@@PACK_RECEIVED|_\*to be defined_||
|@@ROWCOUNT|_\*to be defined_||
|@@TRANCOUNT|_\*to be defined_||
|BINARY_CHECKSUM|_\*to be defined_||
|CHECKSUM|_\*to be defined_||
|COMPRESS|COMPRESS|​Snowflake’s version has a method argument to indicate the compression method. These are the valid values: **SNAPPY, ZLIB, ZSTD, BZ2** The compression level is specified in parentheses and must be a non-negative integer|
|CONNECTIONPROPERTY|_\*to be defined_||
|CONTEXT_INFO|_\*to be defined_||
|CURRENT_REQUEST_ID|_\*to be defined_||
|CURRENT_TRANSACTION_ID|_\*to be defined_||
|DECOMPRESS|_\*to be defined_|Snowflake has two functions for these: **DECOMPRESS_BINARY** and **DECOMPRESS_STRING**​|
|ERROR_LINE|_\*to be defined_|SnowScript: Not supported in Snowflake with **[SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI)**. JavaScript: Will map to **ERROR_LINE** helper. EXEC helper will capture the Exception line property from the stack trace.|
|ERROR_MESSAGE|SQLERRM|Added **SSC-FDM-TS0023** returned error message could be different in Snowflake.|
|ERROR_NUMBER|_\*to be defined_|SnowScript: Not supported in Snowflake with **[SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI)**. JavaScript: Will map to **ERROR_NUMBER** helper. EXEC helper will capture the Exception code property.|
|ERROR_PROCEDURE|_Mapped_|SnowScript: Use current procedure name, added **SSC-FDM-TS0023** result value is based on the stored procedure where the function is called instead of where the exception occurs. JavaScript: Will map to **ERROR_PROCEDURE** helper, taken from the `arguments.callee.name` procedure property|
|ERROR_SEVERITY|_\*to be defined_|SnowScript: Not supported in Snowflake with **[SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI)**.|
|ERROR_STATE|SQLSTATE|SnowScript: Converted to **SQLSTATE** snowflake property, added **SSC-FDM-TS0023** returned value could be different in Snowflake. JavaScript: Helper will capture Exception state property|
|FORMATMESSAGE|FORMATEMESSAGE_UDF|It creates a UDF to emulate the same behavior of FORMATMESSAGE function but with some limitations.|
|GET_FILESTREAM_TRANSACTION_CONTEXT|_\*to be defined_||
|GETANSINULL|_\*to be defined_||
|HOST_ID|_\*to be defined_||
|HOST_NAME|_\*to be defined_||
|ISNULL|NVL||
|ISNUMERIC|_\*to be defined_|No direct equivalent but can be mapped to a custom UDF, returning the same values as in TSQL.|
|MIN_ACTIVE_ROWVERSION|_\*to be defined_|​|
|NEWID|_\*to be defined_|​Maps to UUID_STRING|
|NEWSEQUENTIALID|_\*to be defined_|​|
|ROWCOUNT_BIG|_\*to be defined_|​|
|SESSION_CONTEXT|_\*to be defined_|​|
|SESSION_ID|_\*to be defined_|​|
|XACT_STATE|_\*to be defined_|​|

## System Statistical[¶](#system-statistical)

<!-- prettier-ignore -->
|TransactSql|Snowflake|Notes|
|---|---|---|
|@@CONNECTIONS|_\*to be defined_|​Snowflake’s a similar function: **LOGIN_HISTORY.** Returns login events within a specified time range|
|@@PACK_RECEIVED|_\*to be defined_||
|@@CPU_BUSY|_\*to be defined_||
|@@PACK_SENT|_\*to be defined_||
|@@TIMETICKS|_\*to be defined_||
|@@IDLE|_\*to be defined_||
|@@TOTAL_ERRORS|_\*to be defined_||
|@@IO_BUSY|_\*to be defined_||
|@@TOTAL_READ|_\*to be defined_||
|@@PACKET_ERRORS|_\*to be defined_||
|@@TOTAL_WRITE|_\*to be defined_||

## Text & Image[¶](#text-image)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|TEXTPTR|_\*to be defined_||
|TEXTVALID|_\*to be defined_||

## Trigger[¶](#trigger)

<!-- prettier-ignore -->
|TransactSQL|Snowflake|Notes|
|---|---|---|
|COLUMNS_UPDATED|_\*to be defined_||
|EVENTDATA|_\*to be defined_||
|TRIGGER_NESTLEVEL|_\*to be defined_||
|UPDATE|_\*to be defined_||

# System functions[¶](#system-functions)

This section describes the functional equivalents of system functions in Transact-SQL to Snowflake
SQL and JavaScript code, oriented to the creation of UDFs in Snowflake.

## ISNULL[¶](#isnull)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#description)

Replaces NULL with the specified replacement value.
([ISNULL in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/isnull-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#sample-source-pattern)

#### Syntax[¶](#syntax)

##### SQL Server[¶](#sql-server)

```
ISNULL ( check_expression , replacement_value )
```

##### Snowflake SQL[¶](#snowflake-sql)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/nvl.html)

```
NVL( <expr1> , <expr2> )
```

### Examples[¶](#examples)

#### SQL Server[¶](#id1)

```
SELECT ISNULL(NULL, 'SNOWFLAKE') AS COMPANYNAME;
```

**Result:**

<!-- prettier-ignore -->
|COMPANYNAME|
|---|
|SNOWFLAKE|

##### Snowflake SQL[¶](#id2)

```
SELECT
NVL(NULL, 'SNOWFLAKE') AS COMPANYNAME;
```

**Result:**

<!-- prettier-ignore -->
|COMPANYNAME|
|---|
|SNOWFLAKE|

## NEWID[¶](#newid)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id3)

Creates a unique value of type uniqueidentifier.
([NEWID in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/newid-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id4)

#### Syntax[¶](#id5)

##### SQL Server[¶](#id6)

```
NEWID ( )
```

##### Snowflake SQL[¶](#id7)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/nvl.html)

```
UUID_STRING()
```

### Examples[¶](#id8)

Warning

Outputs may differ because it generates a unique ID in runtime

#### SQL Server[¶](#id9)

```
SELECT NEWID ( ) AS ID;
```

**Result:**

<!-- prettier-ignore -->
|ID|
|---|
|47549DDF-837D-41D2-A59C-A6BC63DF7910|

##### Snowflake SQL[¶](#id10)

```
SELECT
UUID_STRING( ) AS ID;
```

**Result:**

<!-- prettier-ignore -->
|ID|
|---|
|6fd4312a-7925-4ad9-85d8-e039efd82089|

## NULLIF[¶](#nullif)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id11)

Returns a null value if the two specified expressions are equal.

### Sample Source Pattern[¶](#id12)

#### Syntax[¶](#id13)

##### SQL Server[¶](#id14)

```
NULLIF ( check_expression , replacement_value )
```

##### Snowflake SQL[¶](#id15)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/nullif.html)

```
NULLIF( <expr1> , <expr2> )
```

### Examples[¶](#id16)

#### SQL Server[¶](#id17)

```
SELECT NULLIF(6,9) AS RESULT1, NULLIF(5,5) AS RESULT2;
```

**Result:**

<!-- prettier-ignore -->
|RESULT1|RESULT2|
|---|---|
|6|null|

##### Snowflake SQL[¶](#id18)

```
SELECT
NULLIF(6,9) AS RESULT1,
NULLIF(5,5) AS RESULT2;
```

**Result:**

<!-- prettier-ignore -->
|RESULT1|RESULT2|
|---|---|
|6|null|

## @@ROWCOUNT[¶](#rowcount)

Applies to

- SQL Server

### Description[¶](#id19)

Returns the number of rows affected by the last statement.
([@@ROWCOUNT in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/rowcount-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern[¶](#id20)

#### Syntax[¶](#id21)

##### SQL Server[¶](#id22)

```
@@ROWCOUNT
```

##### Snowflake SQL[¶](#id23)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/dml-status)

```
SQLROWCOUNT
```

### Examples[¶](#id24)

#### SQL Server[¶](#id25)

```
CREATE TABLE table1
(
    column1 INT
);

CREATE PROCEDURE procedure1
AS
BEGIN
    declare @addCount int = 0;

    INSERT INTO table1 (column1) VALUES (1),(2),(3);
    set @addCount = @addCount + @@ROWCOUNT

   select @addCount
END
;
GO

EXEC procedure1;
```

**Result:**

<!-- prettier-ignore -->
|     |
|---|
|3|

##### Snowflake SQL[¶](#id26)

```
CREATE OR REPLACE TABLE table1
(
    column1 INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "11/13/2024",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        ADDCOUNT INT := 0;
        ProcedureResultSet RESULTSET;
    BEGIN


        INSERT INTO table1 (column1) VALUES (1),(2),(3);
        ADDCOUNT := :ADDCOUNT + SQLROWCOUNT;
        ProcedureResultSet := (

       select
            :ADDCOUNT);
        RETURN TABLE(ProcedureResultSet);
    END;
$$;

CALL procedure1();
```

**Result:**

<!-- prettier-ignore -->
|:ADDCOUNT|
|---|
|3|

## FORMATMESSAGE[¶](#formatmessage)

Applies to

- SQL Server

### Description[¶](#id27)

Constructs a message from an existing message in sys.messages or from a provided string.
([FORMATMESSAGE in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/formatmessage-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern[¶](#id28)

Since Snowflake does not support `FORMATMESSAGE` function, the
[FORMATMESSAGE_UDF](#formatmessage-udf) is added to simulate its behavior.

### Syntax[¶](#id29)

#### SQL Server[¶](#id30)

```
FORMATMESSAGE ( { msg_number  | ' msg_string ' | @msg_variable} , [ param_value [ ,...n ] ] )
```

### Examples[¶](#id31)

#### SQL Server[¶](#id32)

```
SELECT FORMATMESSAGE('This is the %s and this is the %s.', 'first variable', 'second variable') AS RESULT;
```

**Result:**

<!-- prettier-ignore -->
|RESULT|
|---|
|This is the first variable and this is the second variable.|

#### Snowflake[¶](#snowflake)

```
SELECT
--** SSC-FDM-TS0008 - FORMATMESSAGE WAS CONVERTED TO CUSTOM UDF FORMATMESSAGE_UDF AND IT MIGHT HAVE A DIFFERENT BEHAVIOR. **
FORMATMESSAGE_UDF('This is the %s and this is the %s.', ARRAY_CONSTRUCT('first variable', 'second variable')) AS RESULT;
```

**Result:**

<!-- prettier-ignore -->
|RESULT|
|---|
|This is the first variable and this is the second variable.|

### Related EWIs[¶](#related-ewis)

1. [SSC-FDM-TS0008](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0008):
   FORMATMESSAGE function was converted to UDF.

## FORMATMESSAGE_UDF[¶](#formatmessage-udf)

Snowflake does not have a function with the functionality of `FORMATMESSAGE`. SnowConvert AI
generates the following Python UDF to emulate the behavior of `FORMATMESSAGE`.

```
CREATE OR REPLACE FUNCTION FORMATMESSAGE_UDF(MESSAGE STRING, ARGS ARRAY)
RETURNS STRING
LANGUAGE python
IMMUTABLE
RUNTIME_VERSION = '3.8'
HANDLER = 'format_py'
as
$$
def format_py(message,args):
  return message % (*args,)
$$;
```

This UDF may not work correctly on some cases:

- Using the `%I64d` placeholder will throw an error.
- If the number of substitution arguments is different than the number of place holders, it will
  throw an error.
- Some unsigned placeholders like `%u` or `%X` will not behave properly when formatting the value.
- It cannot handle message_ids.

## String functions[¶](#string-functions)

This section describes the functional equivalents of string functions in Transact-SQL to Snowflake
SQL and JavaScript code, oriented to the creation of UDFs in Snowflake.

## CHAR[¶](#char)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id33)

Returns a single-byte character with the integer sent as a parameter on the ASCII table
([CHAR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/char-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id34)

#### Syntax[¶](#id35)

##### SQL Server[¶](#id36)

```
CHAR( expression )
```

##### Snowflake SQL[¶](#id37)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/chr.html)

```
{CHR | CHAR} ( <input> )
```

##### JavaScript[¶](#javascript)

[JavaScript complete documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCharCode)

```
String.fromCharCode( expression1, ... , expressionN )
```

### Examples[¶](#id38)

#### SQL Server[¶](#id39)

```
SELECT CHAR(170) AS SMALLEST_A
```

**Output:**

<!-- prettier-ignore -->
|SMALLEST_A|
|---|
|ª|

##### Snowflake SQL[¶](#id40)

```
SELECT
CHAR(170) AS SMALLEST_A;
```

**Result:**

<!-- prettier-ignore -->
|SMALLEST_A|
|---|
|ª|

##### JavaScript[¶](#id41)

```
CREATE OR REPLACE FUNCTION get_char(expression float)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
  return String.fromCharCode( EXPRESSION );
$$;

SELECT GET_CHAR(170) SMALLEST_A;
```

**Result:**

<!-- prettier-ignore -->
|SMALLEST_A|
|---|
|ª|

## CHARINDEX[¶](#charindex)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id42)

Returns the index of the first occurrence of the specified value sent as a parameter when it matches
([CHARINDEX in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/charindex-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id43)

#### Syntax[¶](#id44)

##### SQL Server[¶](#id45)

```
CHARINDEX( expression_to_find, expression_to_search [, start] )
```

##### Snowflake SQL[¶](#id46)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/charindex.html)

```
CHARINDEX( <expr1>, <expr2> [ , <start_pos> ] )
```

##### JavaScript[¶](#id47)

[JavaScript complete documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/indexOf)

```
String.indexOf( search_value [, index] )
```

### Examples[¶](#id48)

#### SQL Server[¶](#id49)

```
SELECT CHARINDEX('t', 'Customer') AS MatchPosition;
```

**Result:**

<!-- prettier-ignore -->
|INDEX|
|---|
|33|

##### Snowflake SQL[¶](#id50)

```
SELECT
CHARINDEX('t', 'Customer') AS MatchPosition;
```

**Result:**

<!-- prettier-ignore -->
|INDEX|
|---|
|33|

##### JavaScript[¶](#id51)

**Note:**

Indexes in Transact start at 1, instead of JavaScript which start at 0.

```
CREATE OR REPLACE FUNCTION get_index
(
  expression_to_find varchar,
  expression_to_search varchar,
  start_index  float
)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  return EXPRESSION_TO_SEARCH.indexOf(EXPRESSION_TO_FIND, START_INDEX)+1;
$$;

SELECT GET_INDEX('and', 'Give your heart and soul to me, and life will always be la vie en rose', 20) AS INDEX;
```

**Result:**

<!-- prettier-ignore -->
|INDEX|
|---|
|33|

## COALESCE[¶](#coalesce)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id52)

Evaluates the arguments in order and returns the current value of the first expression that
initially doesn’t evaluate to NULL. For example,SELECT COALESCE(NULL, NULL, ‘third_value’,
‘fourth_value’); returns the third value because the third value is the first value that isn’t null.
([COALESCE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/coalesce-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id53)

#### Syntax[¶](#id54)

##### SQL Server[¶](#id55)

```
COALESCE ( expression [ ,...n ] )
```

##### Snowflake SQL[¶](#id56)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/coalesce.html)

```
COALESCE( <expr1> , <expr2> [ , ... , <exprN> ] )
```

### Examples[¶](#id57)

#### SQL Server[¶](#id58)

```
SELECT TOP 10 StartDate,
COALESCE(EndDate,'2000-01-01') AS FIRST_NOT_NULL
FROM HumanResources.EmployeeDepartmentHistory
```

**Result:**

<!-- prettier-ignore -->
|StartDate|FIRST_NOT_NULL|
|---|---|
|2009-01-14|2000-01-01|
|2008-01-31|2000-01-01|
|2007-11-11|2000-01-01|
|2007-12-05|2010-05-30|
|2010-05-31|2000-01-01|
|2008-01-06|2000-01-01|
|2008-01-24|2000-01-01|
|2009-02-08|2000-01-01|
|2008-12-29|2000-01-01|
|2009-01-16|2000-01-01|

##### Snowflake SQL[¶](#id59)

```
SELECT TOP 10
StartDate,
COALESCE(EndDate,'2000-01-01') AS FIRST_NOT_NULL
FROM
HumanResources.EmployeeDepartmentHistory;
```

**Result:**

<!-- prettier-ignore -->
|StartDate|FIRST_NOT_NULL|
|---|---|
|2009-01-14|2000-01-01|
|2008-01-31|2000-01-01|
|2007-11-11|2000-01-01|
|2007-12-05|2010-05-30|
|2010-05-31|2000-01-01|
|2008-01-06|2000-01-01|
|2008-01-24|2000-01-01|
|2009-02-08|2000-01-01|
|2008-12-29|2000-01-01|
|2009-01-16|2000-01-01|

## CONCAT[¶](#concat)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id60)

Makes a concatenation of string values with others.
([CONCAT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/concat-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id61)

#### Syntax[¶](#id62)

##### SQL Server[¶](#id63)

```
CONCAT ( string_value1, string_value2 [, string_valueN ] )
```

##### Snowflake SQL[¶](#id64)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/concat.html)

```
CONCAT( <expr1> [ , <exprN> ... ] )

<expr1> || <expr2> [ || <exprN> ... ]
```

##### JavaScript[¶](#id65)

[JavaScript complete documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/concat)

```
 String.concat( expression1, ..., expressionN )
```

### Examples[¶](#id66)

#### SQL Server[¶](#id67)

```
SELECT CONCAT('Ray',' ','of',' ','Light') AS TITLE;
```

**Output:**

<!-- prettier-ignore -->
|TITLE|
|---|
|Ray of Light|

##### Snowflake SQL[¶](#id68)

```
SELECT
CONCAT('Ray',' ','of',' ','Light') AS TITLE;
```

**Output:**

<!-- prettier-ignore -->
|TITLE|
|---|
|Ray of Light|

##### JavaScript[¶](#id69)

```
CREATE OR REPLACE FUNCTION concatenate_strs(strings array)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
  var result = ""
  STRINGS.forEach(element => result = result.concat(element));
  return result;
$$;
SELECT concatenate_strs(array_construct('Ray',' ','of',' ','Light')) TITLE;
```

**Output:**

```
   TITLE|
```

————| Ray of Light|

## LEFT[¶](#left)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id70)

Returns the right part of a character string with the specified number of characters.
([RIGHT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/right-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id71)

#### Syntax[¶](#id72)

##### SQL Server[¶](#id73)

```
LEFT ( character_expression , integer_expression )
```

##### Snowflake SQL[¶](#id74)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/left.html)

```
LEFT ( <expr> , <length_expr> )
```

##### JavaScript[¶](#id75)

Function used to emulate the behavior

```
function LEFT(string, index){
    if(index < 0){
        throw new RangeError('Invalid INDEX on LEFT function');
    }
    return string.slice( 0, index);
  }
return LEFT(STR, INDEX);
```

### Examples[¶](#id76)

#### SQL Server[¶](#id77)

```
SELECT LEFT('John Smith', 5) AS FIRST_NAME;
```

**Output:**

<!-- prettier-ignore -->
|FIRST_NAME|
|---|
|John|

##### Snowflake SQL[¶](#id78)

```
SELECT LEFT('John Smith', 5) AS FIRST_NAME;
```

**Output:**

<!-- prettier-ignore -->
|FIRST_NAME|
|---|
|John|

##### JavaScript[¶](#id79)

```
CREATE OR REPLACE FUNCTION left_str(str varchar, index float)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
    function LEFT(string, index){
      if(index < 0){
          throw new RangeError('Invalid INDEX on LEFT function');
      }
      return string.slice( 0, index);
    }
  return LEFT(STR, INDEX);
$$;
SELECT LEFT_STR('John Smith', 5) AS FIRST_NAME;
```

**Output:**

<!-- prettier-ignore -->
|FIRST_NAME|
|---|
|John|

## LEN[¶](#len)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id80)

Returns the length of a string
([LEN in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/len-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id81)

#### Syntax[¶](#id82)

##### SQL Server[¶](#id83)

```
LEN( string_expression )
```

##### Snowflake SQL[¶](#id84)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/length.html)

```
LENGTH( <expression> )
LEN( <expression> )
```

##### JavaScript[¶](#id85)

[JavaScript SQL complete documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/length)

```
 string.length
```

### Examples[¶](#id86)

#### SQL Server[¶](#id87)

```
SELECT LEN('Sample text') AS [LEN];
```

**Output:**

<!-- prettier-ignore -->
|LEN|
|---|
|11|

##### Snowflake SQL[¶](#id88)

```
SELECT LEN('Sample text') AS LEN;
```

**Output:**

<!-- prettier-ignore -->
|LEN|
|---|
|11|

##### JavaScript[¶](#id89)

```
CREATE OR REPLACE FUNCTION get_len(str varchar)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return STR.length;
$$;
SELECT GET_LEN('Sample text') LEN;
```

**Output:**

<!-- prettier-ignore -->
|LEN|
|---|
|11|

## LOWER[¶](#lower)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id90)

Converts a string to lowercase
([LOWER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/lower-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id91)

#### Syntax[¶](#id92)

##### SQL Server[¶](#id93)

```
LOWER ( character_expression )
```

##### Snowflake SQL[¶](#id94)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/lower.html)

```
LOWER( <expr> )
```

##### JavaScript[¶](#id95)

[JavaScript SQL complete documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/toLowerCase)

```
 String.toLowerCase( )
```

### Examples[¶](#id96)

#### SQL Server[¶](#id97)

```
SELECT LOWER('YOU ARE A PREDICTION OF THE GOOD ONES') AS LOWERCASE;
```

**Output:**

<!-- prettier-ignore -->
|LOWERCASE|
|---|
|you are a prediction of the good ones|

##### Snowflake SQL[¶](#id98)

```
SELECT LOWER('YOU ARE A PREDICTION OF THE GOOD ONES') AS LOWERCASE;
```

**Output:**

<!-- prettier-ignore -->
|LOWERCASE|
|---|
|you are a prediction of the good ones|

##### JavaScript[¶](#id99)

```
CREATE OR REPLACE FUNCTION to_lower(str varchar)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
  return STR.toLowerCase();
$$;

SELECT TO_LOWER('YOU ARE A PREDICTION OF THE GOOD ONES') LOWERCASE;
```

**Output:**

<!-- prettier-ignore -->
|LOWERCASE|
|---|
|you are a prediction of the good ones|

## NCHAR[¶](#nchar)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id100)

Returns the UNICODE character of an integer sent as a parameter
([NCHAR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/nchar-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id101)

#### Syntax[¶](#id102)

```
NCHAR( expression )
```

##### Arguments[¶](#arguments)

`expression`: Integer expression.

##### Return Type[¶](#return-type)

String value, it depends on the input received.

### Examples[¶](#id103)

#### Query[¶](#query)

```
SELECT NCHAR(170);
```

##### Result[¶](#result)

<!-- prettier-ignore -->
|     |
|---|
|ª|

**Note:**

The equivalence for this function in JavaScript is documented in [CHAR](#char).

## REPLACE[¶](#replace)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id104)

Replaces all occurrences of a specified string value with another string value.
([REPLACE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/replace-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id105)

#### Syntax[¶](#id106)

##### SQL Server[¶](#id107)

```
REPLACE ( string_expression , string_pattern , string_replacement )
```

##### Snowflake SQL[¶](#id108)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/replace.html)

```
REPLACE( <subject> , <pattern> [ , <replacement> ] )
```

##### JavaScript[¶](#id109)

```
 String.replace( pattern, new_expression)
```

### Examples[¶](#id110)

#### SQL Server[¶](#id111)

```
SELECT REPLACE('Real computer software', 'software','science') AS COLUMNNAME;
```

**Output:**

```
COLUMNNAME           |
---------------------|
Real computer science|
```

##### Snowflake SQL[¶](#id112)

```
SELECT REPLACE('Real computer software', 'software','science') AS COLUMNNAME;
```

**Output:**

```
COLUMNNAME           |
---------------------|
Real computer science|
```

##### JavaScript[¶](#id113)

```
 CREATE OR REPLACE FUNCTION REPLACER (str varchar, pattern varchar, new_expression varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
   return STR.replace( PATTERN, NEW_EXPRESSION );
$$;

SELECT REPLACER('Real computer software', 'software', 'science') AS COLUMNNAME;
```

**Output:**

```
COLUMNNAME             |
---------------------|
Real computer science|
```

## REPLICATE[¶](#replicate)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id114)

Replicates a string value a specified number of times
([REPLICATE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/replicate-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id115)

#### Syntax[¶](#id116)

##### SQL Server[¶](#id117)

```
REPLICATE( string_expression, number_expression )
```

##### Snowflake SQL[¶](#id118)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/repeat.html)

```
REPEAT(<input>, <n>)
```

##### JavaScript[¶](#id119)

[JavaScript Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/repeat)

```
String.repeat( number_expression )
```

### Examples[¶](#id120)

#### SQL Server[¶](#id121)

```
SELECT REPLICATE('Staying alive',5) AS RESULT
```

**Result:**

```
RESULT                                                           |
-----------------------------------------------------------------|
Staying aliveStaying aliveStaying aliveStaying aliveStaying alive|
```

##### Snowflake SQL[¶](#id122)

```
SELECT REPEAT('Staying alive',5) AS RESULT;
```

**Result:**

```
RESULT                                                           |
-----------------------------------------------------------------|
Staying aliveStaying aliveStaying aliveStaying aliveStaying alive|
```

##### JavaScript[¶](#id123)

```
 CREATE OR REPLACE FUNCTION REPEAT_STR (str varchar, occurrences float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$

   return STR.repeat( OCCURRENCES );
$$;

SELECT REPEAT_STR('Staying alive ', 5) AS RESULT;
```

**Result:**

```
RESULT                                                           |
-----------------------------------------------------------------|
Staying aliveStaying aliveStaying aliveStaying aliveStaying alive|
```

## RIGHT[¶](#right)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id124)

Returns the right part of a character string with the specified number of characters.
([RIGHT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/right-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id125)

#### Syntax[¶](#id126)

##### SQL Server[¶](#id127)

```
RIGHT ( character_expression , integer_expression )
```

##### Snowflake SQL[¶](#id128)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/right.html)

```
RIGHT( <expr> , <length_expr> )
```

##### JavaScript[¶](#id129)

UDF used to emulate the behavior

```
 function RIGHT(string, index){
      if(index< 0){
          throw new RangeError('Invalid INDEX on RIGHT function');
      }
      return string.slice( string.length - index, string.length );
    }
```

### Examples[¶](#id130)

#### SQL Server[¶](#id131)

```
SELECT RIGHT('John Smith', 5) AS LAST_NAME;
```

**Output:**

```
   LAST_NAME|
------------|
       Smith|
```

##### Snowflake SQL[¶](#id132)

```
SELECT RIGHT('John Smith', 5) AS LAST_NAME;
```

**Output:**

```
   LAST_NAME|
------------|
       Smith|
```

##### JavaScript[¶](#id133)

```
 CREATE OR REPLACE FUNCTION right_str(str varchar, index float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    function RIGHT(string, index){
      if(index< 0){
          throw new RangeError('Invalid INDEX on RIGHT function');
      }
      return string.slice( string.length - index, string.length );
    }
  return RIGHT(STR, INDEX);
$$;

SELECT RIGHT_STR('John Smith', 5) AS LAST_NAME;
```

**Output:**

```
   LAST_NAME|
------------|
       Smith|
```

## RTRIM[¶](#rtrim)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id134)

Returns a character expression after it removes leading blanks
([RTRIM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/rtrim-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id135)

#### Syntax[¶](#id136)

##### SQL Server[¶](#id137)

```
RTRIM( string_expression )
```

##### Snowflake SQL[¶](#id138)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/rtrim.html)

```
RTRIM(<expr> [, <characters> ])
```

##### JavaScript[¶](#id139)

Custom function used to emulate the behavior

```
 function RTRIM(string){
    return string.replace(/s+$/,"");
}
```

### Examples[¶](#id140)

#### SQL Server[¶](#id141)

**Input:**

```
SELECT RTRIM('LAST TWO BLANK SPACES  ') AS [RTRIM]
```

**Output:**

```
RTRIM                |
---------------------|
LAST TWO BLANK SPACES|
```

##### Snowflake SQL[¶](#id142)

```
SELECT RTRIM('LAST TWO BLANK SPACES  ') AS RTRIM;
```

**Result:**

```
RTRIM                |
---------------------|
LAST TWO BLANK SPACES|
```

##### JavaScript[¶](#id143)

```
 CREATE OR REPLACE FUNCTION rtrim(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  function RTRIM(string){
    return string.replace(/s+$/,"");
    }
   return RTRIM( STR );
$$;

SELECT RTRIM('LAST TWO BLANK SPACES  ') AS RTRIM;
```

**Result:**

```
RTRIM                |
---------------------|
LAST TWO BLANK SPACES|
```

## SPACE[¶](#space)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id144)

Returns a number of occurrences of blank spaces
([SPACE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/space-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id145)

#### Syntax[¶](#id146)

##### SQL Server[¶](#id147)

```
SPACE ( integer_expression )
```

##### Snowflake SQL[¶](#id148)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/space.html)

```
SPACE(<n>)
```

##### JavaScript[¶](#id149)

Custom function used to emulate the behavior

```
 function SPACE( occurrences ){
    return ' '.repeat( occurrences );
}
```

### Examples[¶](#id150)

#### SQL Server[¶](#id151)

**Input:**

```
SELECT CONCAT('SOME', SPACE(5), 'TEXT') AS RESULT;
```

**Output:**

```
RESULT       |
-------------|
SOME     TEXT|
```

##### Snowflake SQL[¶](#id152)

**Input:**

```
SELECT CONCAT('SOME', SPACE(5), 'TEXT') AS RESULT;
```

**Output:**

```
RESULT       |
-------------|
SOME     TEXT|
```

##### JavaScript[¶](#id153)

**Input:**

```
 CREATE OR REPLACE FUNCTION SPACE(occurrences float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    function SPACE( occurrences ){
    return ' '.repeat( occurrences );
    }
    return SPACE( OCCURRENCES );
$$;

SELECT CONCAT('SOME', SPACE(5), 'TEXT') RESULT;
```

**Output:**

```
RESULT       |
-------------|
SOME     TEXT|
```

## SUBSTRING[¶](#substring)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id154)

Returns a character expression after it removes leading blanks
([RTRIM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/rtrim-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id155)

#### Syntax[¶](#id156)

##### SQL Server[¶](#id157)

```
SUBSTRING( string_expression, start, length )
```

##### Snowflake SQL[¶](#id158)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/substr.html)

```
SUBSTR( <base_expr>, <start_expr> [ , <length_expr> ] )

SUBSTRING( <base_expr>, <start_expr> [ , <length_expr> ] )
```

##### JavaScript[¶](#id159)

Custom function used to emulate the behavior

```
 string.substring( indexA [, indexB])
```

### Examples[¶](#id160)

#### SQL Server[¶](#id161)

**Input:**

```
SELECT SUBSTRING('abcdef', 2, 3) AS SOMETEXT;
```

**Output:**

```
SOMETEXT|
--------|
bcd     |
```

##### Snowflake SQL[¶](#id162)

```
SELECT SUBSTRING('abcdef', 2, 3) AS SOMETEXT;
```

**Result:**

```
SOMETEXT|
--------|
bcd     |
```

##### JavaScript[¶](#id163)

```
 CREATE OR REPLACE FUNCTION REPLACER_LENGTH(str varchar, index float, length float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    var start = INDEX - 1;
    var end = STR.length - (LENGTH - 1);
    return STR.substring(start, end);
$$;

SELECT REPLACER_LENGTH('abcdef', 2, 3) AS SOMETEXT;
```

**Result:**

```
SOMETEXT|
--------|
bcd     |
```

## UPPER[¶](#upper)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id164)

Converts a string to uppercase
([UPPER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/upper-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id165)

#### Syntax[¶](#id166)

##### SQL Server[¶](#id167)

```
UPPER( string_expression )
```

##### Snowflake SQL[¶](#id168)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/upper.html)

```
UPPER( <expr> )
```

##### JavaScript[¶](#id169)

[JavaScript SQL complete documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/toUpperCase)

```
 String.toUpperCase( )
```

### Examples[¶](#id170)

#### SQL Server[¶](#id171)

```
SELECT UPPER('you are a prediction of the good ones') AS [UPPER]
```

**Output:**

```
+-------------------------------------|
<!-- prettier-ignore -->
|UPPER|
+-------------------------------------|
<!-- prettier-ignore -->
|YOU ARE A PREDICTION OF THE GOOD ONES|
+-------------------------------------|
```

##### Snowflake SQL[¶](#id172)

```
SELECT
UPPER('you are a prediction of the good ones') AS UPPER;
```

**Output:**

```
+-------------------------------------|
<!-- prettier-ignore -->
|UPPER|
+-------------------------------------|
<!-- prettier-ignore -->
|YOU ARE A PREDICTION OF THE GOOD ONES|
+-------------------------------------|
```

##### JavaScript[¶](#id173)

```
 CREATE OR REPLACE FUNCTION to_upper(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return STR.toUpperCase();
$$;

SELECT TO_UPPER('you are a prediction of the good ones') UPPER;
```

**Output:**

```
UPPER                                |
-------------------------------------|
YOU ARE A PREDICTION OF THE GOOD ONES|
```

## ASCII[¶](#ascii)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id174)

Returns the number code of a character on the ASCII table
([ASCII in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/ascii-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id175)

### Syntax[¶](#id176)

```
ASCII( expression )
```

#### Arguments[¶](#id177)

`expression`: `VARCVHAR` or `CHAR` expression.

#### Return Type[¶](#id178)

`INT`.

### Examples[¶](#id179)

### Query[¶](#id180)

```
SELECT ASCII('A') AS A , ASCII('a') AS a;
```

#### Result[¶](#id181)

```
          A|          a|
-----------| ----------|
         65|         97|
```

## ASCII in JS[¶](#ascii-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id182)

This function returns the number code of a character on the ASCII table
([JavaScript charCodeAt function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/charCodeAt)).

### Sample Source Pattern[¶](#id183)

#### Syntax[¶](#id184)

```
 string.charCodeAt( [index] )
```

##### Arguments[¶](#id185)

`index`(Optional): Index of string to get character and return its code number on the ASCII table.
If this parameter is not specified, it takes 0 as default. \

##### Return Type[¶](#id186)

`Int`.

### Examples[¶](#id187)

#### Query[¶](#id188)

```
 CREATE OR REPLACE FUNCTION get_ascii(c char)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return C.charCodeAt();
$$;

SELECT GET_ASCII('A') A, GET_ASCII('a') a;
```

##### Result[¶](#id189)

```
          A|          a|
-----------| ----------|
         65|         97|
```

## QUOTENAME[¶](#quotename)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id190)

Returns a string delimited using quotes
([QUOTENAME in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/quotename-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id191)

### Syntax[¶](#id192)

```
QUOTENAME( string_expression [, quote_character])
```

#### Arguments[¶](#id193)

`string_expression`: String to delimit.

`quote_character`: one-character to delimit the string.

#### Return Type[¶](#id194)

`NVARCHAR(258)`. Null if the quote is different of (‘), ([]), (“), ( () ), ( >< ), ({}) or (`).

### Examples[¶](#id195)

### Query[¶](#id196)

```
SELECT QUOTENAME('Hello', '`') AS HELLO;
```

#### Result[¶](#id197)

```
    HELLO|
---------|
  `Hello`|
```

## QUOTENAME in JS[¶](#quotename-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id198)

Unfortunately, this function is not available in JavaScript, but it can be implemented using
predefined functions.

### Sample Source Pattern[¶](#id199)

#### Implementation Example[¶](#implementation-example)

```
 function QUOTENAME(string, quote){
    return quote.concat(string, quote);
}
```

##### Arguments[¶](#id200)

`string`: String expression to delimit.

`quote`: Quote to be used as a delimiter.

##### Return Type[¶](#id201)

String.

### Examples[¶](#id202)

#### Query[¶](#id203)

```
CREATE OR REPLACE FUNCTION QUOTENAME(str varchar, quote char)
RETURNS string
LANGUAGE JAVASCRIPT
AS
$$
  function QUOTENAME(string, quote){
    const allowed_quotes = /[\']|[\"]|[(]|[)]|[\[]|[\]]|[\{]|[\}]|[\`]/;

    if(!allowed_quotes.test(quote)) throw new TypeError('Invalid Quote');

    return quote.concat(string, quote);
  }
   return QUOTENAME(STR, QUOTE);
$$;

SELECT QUOTENAME('Hola', '`') HELLO;
```

##### Result[¶](#id204)

```
    HELLO|
---------|
  `Hello`|
```

## CONCAT_WS[¶](#concat-ws)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id205)

Makes a concatenation of string values with others using a separator between them
([CONCAT_WS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/concat-ws-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id206)

### Syntax[¶](#id207)

```
CONCAT_WS( separator, expression1, ... ,expressionN )
```

#### Arguments[¶](#id208)

`separator`: Separator to join.

`expression1, ... ,expressionN:` Expression to be found into a string.

#### Return Type[¶](#id209)

String value, depends on the input received.

### Examples[¶](#id210)

### Query[¶](#id211)

```
SELECT CONCAT_WS(' ', 'Mariah','Carey') AS NAME;
```

#### Result[¶](#id212)

```
        NAME|
------------|
Mariah Carey|
```

## Join in JS[¶](#join-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id213)

Concatenates the string arguments to the calling string using a separator
([JavaScript Join function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array/join)).

### Sample Source Pattern[¶](#id214)

#### Syntax[¶](#id215)

```
 Array.join( separator )
```

##### Arguments[¶](#id216)

`separator`: Character to join.

##### Return Type[¶](#id217)

`String`.

### Examples[¶](#id218)

#### Query[¶](#id219)

```
 CREATE OR REPLACE FUNCTION join_strs(separator varchar, strings array)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return STRINGS.join(SEPARATOR);
$$;
SELECT join_strs(' ',array_construct('Mariah','Carey')) NAME;
```

##### Result[¶](#id220)

```
        NAME|
------------|
Mariah Carey|
```

## SOUNDEX[¶](#soundex)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id221)

Returns a four-character code to evaluate the similarity of two strings
([SOUNDEX in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/soundex-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id222)

### Syntax[¶](#id223)

```
SOUNDEX( string_expression )
```

#### Arguments[¶](#id224)

`string_expression`: String expression to reverse.

#### Return Type[¶](#id225)

The same data type of the string expression sent as a parameter.

### Examples[¶](#id226)

### Query[¶](#id227)

```
SELECT SOUNDEX('two') AS TWO , SOUNDEX('too') AS TOO;
```

#### Result[¶](#id228)

```
      TWO|      TOO|
---------|---------|
     T000|     T000|
```

## SOUNDEX in JS[¶](#soundex-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id229)

Unfortunately, JavaScript does not provide a method that executes the SOUNDEX algorithm, but it can
be implemented manually.

### Sample Source Pattern[¶](#id230)

#### Implementation Example[¶](#id231)

```
 const dic = {A:0, B:1, C:2, D:3, E:0, F:1, G:2, H:0, I:0, J:2, K:2, L:4, M:5, N:5, O:0, P:1, Q:2, R:6, S:2, T:3, U:0, V:1, W:0, X:2, Y:0, Z:2};

  function getCode(letter){
      return dic[letter.toUpperCase()];
  }

  function SOUNDEX(word){
    var initialCharacter = word[0].toUpperCase();
    var initialCode = getCode(initialCharacter);
    for(let i = 1; i < word.length; ++i) {
        const letterCode = getCode(word[i]);
        if (letterCode && letterCode != initialCode) {
             initialCharacter += letterCode;
             if(initialCharacter.length == 4) break;
        }
        initialCode = letterCode;
    }

      return initialCharacter.concat( '0'.repeat( 4 - initialCharacter.length));

  }
```

##### Arguments[¶](#id232)

`word`: String expression to get its SOUNDEX equivalence.

##### Return Type[¶](#id233)

String.

### Examples[¶](#id234)

#### Query[¶](#id235)

```
 CREATE OR REPLACE FUNCTION get_soundex(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  const dic = {A:0, B:1, C:2, D:3, E:0, F:1, G:2, H:0, I:0, J:2, K:2, L:4, M:5, N:5, O:0, P:1, Q:2, R:6, S:2, T:3, U:0, V:1, W:0, X:2, Y:0, Z:2};

  function getCode(letter){
      return dic[letter.toUpperCase()];
  }

  function SOUNDEX(word){
    var initialCharacter = word[0].toUpperCase();
    var initialCode = getCode(initialCharacter);
    for(let i = 1; i < word.length; ++i) {
        const letterCode = getCode(word[i]);
        if (letterCode && letterCode != initialCode) {
             initialCharacter += letterCode;
             if(initialCharacter.length == 4) break;
        }
        initialCode = letterCode;
    }

    return initialCharacter.concat( '0'.repeat( 4 - initialCharacter.length));
  }

  return SOUNDEX( STR );
$$;

SELECT GET_SOUNDEX('two') AS TWO , GET_SOUNDEX('too') AS TOO;
```

##### Result[¶](#id236)

```
      TWO|      TOO|
---------|---------|
     T000|     T000|
```

## REVERSE[¶](#reverse)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id237)

Reverses a string
([REVERSE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/reverse-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id238)

### Syntax[¶](#id239)

```
REVERSE( string_expression )
```

#### Arguments[¶](#id240)

`string_expression`: String expression to reverse.

#### Return Type[¶](#id241)

The same data type of the string expression sent as a parameter.

### Examples[¶](#id242)

### Query[¶](#id243)

```
SELECT REVERSE('rotator') AS PALINDROME;
```

#### Result[¶](#id244)

```
      PALINDROME|
----------------|
         rotator|
```

## reverse in JS[¶](#reverse-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id245)

Unfortunately, this function is not available in JavaScript, but it can be implemented using
predefined functions.

### Sample Source Pattern[¶](#id246)

#### Implementation Example[¶](#id247)

```
 function REVERSE(string){
    return string.split("").reverse().join("");
}
```

##### Arguments[¶](#id248)

`string`: String expression to reverse.

##### Return Type[¶](#id249)

String.

### Examples[¶](#id250)

#### Query[¶](#id251)

```
 CREATE OR REPLACE FUNCTION REVERSE(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
   return STR.split("").reverse().join("");
$$;

SELECT REVERSE('rotator') PALINDROME;
```

##### Result[¶](#id252)

```
      PALINDROME|
----------------|
         rotator|
```

## STRING_ESCAPE[¶](#string-escape)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id253)

Escapes special characters in texts and returns text with escaped characters.
([STRING_ESCAPE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/string-escape-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id254)

### Syntax[¶](#id255)

```
STRING_ESCAPE( text, type )
```

#### Arguments[¶](#id256)

`text`: Text to escape characters.

`type`: Format type to escape characters. Currently, JSON is the only format supported.

#### Return Type[¶](#id257)

`VARCHAR`.

### Examples[¶](#id258)

### Query[¶](#id259)

```
SELECT STRING_ESCAPE('\   /  \\    "     ', 'json') AS [ESCAPE];
```

#### Result[¶](#id260)

```
ESCAPE|
--------------------------|
  \\   \/  \\\\    \"     |
```

## stringify in JS[¶](#stringify-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id261)

Converts an object to a JSON string format
([JavaScript stringify function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)).

### Sample Source Pattern[¶](#id262)

#### Syntax[¶](#id263)

```
 JSON.stringify( value )
```

##### Arguments[¶](#id264)

`value`: Object expression to convert.

##### Return Type[¶](#id265)

String.

### Examples[¶](#id266)

#### Query[¶](#id267)

```
 CREATE OR REPLACE FUNCTION string_escape (str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
   return JSON.stringify( STR );
$$;

SELECT STRING_ESCAPE('\   /  \\    "     ') ESCAPE;
```

##### Result[¶](#id268)

```
                    ESCAPE|
--------------------------|
  \\   \/  \\\\    \"     |
```

## TRIM[¶](#trim)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id269)

Returns a character expression without blank spaces
([TRIM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/trim-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id270)

### Syntax[¶](#id271)

```
TRIM( string_expression )
```

#### Arguments[¶](#id272)

`string_expression:` String expressions to convert.

#### Return Type[¶](#id273)

`VARCHAR` or `NVARCHAR`

### Examples[¶](#id274)

### SQL Server[¶](#id275)

```
SELECT TRIM('  FIRST AND LAST TWO BLANK SPACES  ') AS [TRIM];
```

**Output:**

```
+-------------------------------|
<!-- prettier-ignore -->
|TRIM|
+-------------------------------|
<!-- prettier-ignore -->
|FIRST AND LAST TWO BLANK SPACES|
+-------------------------------|
```

#### Snowflake SQL[¶](#id276)

```
SELECT TRIM('  FIRST AND LAST TWO BLANK SPACES  ') AS TRIM;
```

**Output:**

```
+-------------------------------|
<!-- prettier-ignore -->
|TRIM|
+-------------------------------|
<!-- prettier-ignore -->
|FIRST AND LAST TWO BLANK SPACES|
+-------------------------------|
```

## trim in JS[¶](#trim-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id277)

Replaces the occurrences of a pattern using a new one sent as a parameter
([JavaScript Replace function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace)).

### Sample Source Pattern[¶](#id278)

#### Syntax[¶](#id279)

```
 String.trim( )
```

##### Arguments[¶](#id280)

This function does not receive any parameters.

##### Return Type[¶](#id281)

String.

### Examples[¶](#id282)

#### Query[¶](#id283)

```
 CREATE OR REPLACE FUNCTION TRIM_STR(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
   return STR.trim( );
$$;

SELECT TRIM_STR('  FIRST AND LAST TWO BLANK SPACES  ')TRIM
```

##### Result[¶](#id284)

```
                           TRIM|
-------------------------------|
FIRST AND LAST TWO BLANK SPACES|
```

## DIFFERENCE[¶](#difference)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id285)

Returns an integer measuring the difference between two strings using the SOUNDEX algorithm
([DIFFERENCE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/difference-transact-sql?view=sql-server-ver15)).
It counts the common characters of the strings resulting by executing the SOUNDEX algorithm.

### Sample Source Pattern[¶](#id286)

### Syntax[¶](#id287)

```
DIFFERENCE( expression1, expression1 )
```

#### Arguments[¶](#id288)

`expression1, expression2:` String expressions to be compared.

#### Return Type[¶](#id289)

`Int`.

### Examples[¶](#id290)

### Query[¶](#id291)

```
SELECT DIFFERENCE('Like', 'Mike');
```

#### Result[¶](#id292)

```
    Output |
-----------|
         3 |
```

## DIFFERENCE in JS[¶](#difference-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id293)

Unfortunately, this functionality is not available in JS, but this can be implemented easily.

**Note:**

This functions requires the [SOUNDEX algorithm implementation](#soundex-in-js).

### Sample Source Pattern[¶](#id294)

#### Implementation Example[¶](#id295)

```
 function DIFFERENCE(strA, strB) {
    var count = 0;
    for (var i = 0; i < strA.length; i++){
       if ( strA[i] == strB[i] ) count++;
    }

    return count;
}
```

##### Arguments[¶](#id296)

`strA, strB`: String expressions resulting by executing the SOUNDEX algorithm.

##### Return Type[¶](#id297)

`String`.

### Examples[¶](#id298)

#### Query[¶](#id299)

```
 CREATE OR REPLACE FUNCTION SOUNDEX_DIFFERENCE(str_1 varchar, str_2 varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    function DIFFERENCE(strA, strB) {
      var count = 0;
      for (var i = 0; i < strA.length; i++){
         if ( strA[i] == strB[i] ) count++;
      }

    return count;
    }

    return DIFFERENCE(STR_1, STR_2);
$$;

SELECT SOUNDEX_DIFFERENCE(GET_SOUNDEX('two'), GET_SOUNDEX('too')) DIFFERENCE;
```

##### Result[¶](#id300)

```
   DIFFERENCE|
-------------|
            4|
```

## FORMAT[¶](#format)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id301)

Returns a value formatted with the specified format and optional culture
([FORMAT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/format-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id302)

### Syntax[¶](#id303)

```
FORMAT( value, format [, culture])
```

#### Arguments[¶](#id304)

`value:` String expressions to give format.

format: Desired format.

culture (Optional): NVarchar argument specifying culture. If it is not specified, takes the
languages of the current session.

#### Return Type[¶](#id305)

NULL if the culture parameter is invalid, otherwise, it follows the next data types:

<!-- prettier-ignore -->
|Category||.NET type|
|---|---|---|
|Numeric|bigint|Int64|
|Numeric|int|Int32|
|Numeric|smallint|Int16|
|Numeric|tinyint|Byte|
|Numeric|decimal|SqlDecimal|
|Numeric|numeric|SqlDecimal|
|Numeric|float|Double|
|Numeric|real|Single|
|Numeric|smallmoney|Decimal|
|Numeric|money|Decimal|
|Date and Time|date|DateTime|
|Date and Time|time|TimeSpan|
|Date and Time|datetime|DateTime|
|Date and Time|smalldatetime|DateTime|
|Date and Time|datetime2|DateTime|
|Date and Time|datetimeoffset|DateTimeOffset|

### Examples[¶](#id306)

### Query[¶](#id307)

```
SELECT FORMAT(CAST('2022-01-24' AS DATE), 'd', 'en-gb')  AS 'Great Britain';
```

#### Result[¶](#id308)

```
  GREAT BRITAIN|
---------------|
     24/01/2022|
```

##### Query[¶](#id309)

```
SELECT FORMAT(244900.25, 'C', 'cr-CR')  AS 'CURRENCY';
```

##### Result[¶](#id310)

<!-- prettier-ignore -->
|CURRENCY|
|---|
|₡244,900.25|

## FORMAT in JS[¶](#format-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id311)

There are different functions to format date and integer values in JavaScript. Unfortunately, these
functionalities are not integrated into one method.

### DateTime values[¶](#datetime-values)

#### Syntax[¶](#id312)

```
 Intl.DateTimeFormat( format ).format( value )
```

##### Arguments[¶](#id313)

`locales` (Optional): String expression of the format to apply.

`options` (Optional): Object with different supported properties for formats of numeric expressions
([JavaScript NumberFormat function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)).

`value`: Numeric expression to format.

##### Return Type[¶](#id314)

`String`.

### Numeric values[¶](#numeric-values)

#### Syntax[¶](#id315)

```
 Intl.NumberFormat( [locales [, options]] ).format( value )
```

##### Arguments[¶](#id316)

`locales` (Optional): String expression of the format to apply.

`options` (Optional): Object with different supported properties for formats of numeric expressions
([JavaScript NumberFormat function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)).

`value`: Numeric expression to format.

##### Return Type[¶](#id317)

`String`.

### Examples[¶](#id318)

#### DateTime[¶](#datetime)

##### Query[¶](#id319)

```
 CREATE OR REPLACE FUNCTION format_date(date timestamp, format varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return new Intl.DateTimeFormat( FORMAT ).format( DATE );
$$;
SELECT FORMAT_DATE(TO_DATE('2022-01-24'), 'en-gb') GREAT_BRITAIN;
```

##### Result[¶](#id320)

```
  GREAT_BRITAIN|
---------------|
     24/01/2022|
```

#### Numeric[¶](#numeric)

##### Query[¶](#id321)

```
 CREATE OR REPLACE FUNCTION format_numeric(number float, locales varchar, options variant)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  return new Intl.NumberFormat( LOCALES , OPTIONS ).format( NUMBER );
$$;
SELECT FORMAT_NUMERIC(244900.25, 'de-DE', PARSE_JSON('{ style: "currency", currency: "CRC" }')) CURRENCY;
```

##### Result[¶](#id322)

```
       CURRENCY|
---------------|
 244.900,25 CRC|
```

## PATINDEX[¶](#patindex)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id323)

Returns the starting position of the first occurrence of a pattern in a specified expression
([PATINDEX in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/patindex-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id324)

### Syntax[¶](#id325)

```
PATINDEX( pattern, expression )
```

#### Arguments[¶](#id326)

`pattern`: Pattern to find.

`expression`: Expression to search.

#### Return Type[¶](#id327)

Integer. Returns 0 if the pattern is not found.

### Examples[¶](#id328)

### Query[¶](#id329)

```
SELECT PATINDEX( '%on%', 'No, no, non esistono più') AS [PATINDEX]
```

#### Result[¶](#id330)

```
    PATINDEX|
------------|
          10|
```

## search in JS[¶](#search-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id331)

Finds the index of a pattern using REGEX
([JavaScript search function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/String/search)).

### Sample Source Pattern[¶](#id332)

#### Syntax[¶](#id333)

```
 String.search( regex )
```

##### Arguments[¶](#id334)

`regex`: Regular expression which matches with the desired pattern.

##### Return Type[¶](#id335)

Integer. If the pattern does not match with any part of the string, returns -1.

### Examples[¶](#id336)

#### Query[¶](#id337)

```
 CREATE OR REPLACE FUNCTION get_index_pattern(pattern varchar, str varchar)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  function GET_PATTERN(pattern, string){
    return string.search(new RegExp( pattern ));
    }
   return GET_PATTERN(PATTERN, STR) + 1;
$$;

SELECT GET_INDEX_PATTERN('on+', 'No, no, non esistono più') PATINDEX;
```

##### Result[¶](#id338)

```
    PATINDEX|
------------|
          10|
```

## STR[¶](#str)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id339)

Returns character data converted from numeric data. The character data is right-justified, with a
specified length and decimal precision.
([STR in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/str-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern[¶](#id340)

### Syntax[¶](#id341)

#### SQL Server[¶](#id342)

```
STR ( float_expression [ , length [ , decimal ] ] )
```

##### Snowflake SQL[¶](#id343)

```
STR_UDF( numeric_expression, number_format )
```

#### Arguments[¶](#id344)

`numeric_expression`: Float expression with a decimal point.

`length` (Optional): Length that the returning expression will have, including point notation,
decimal, and float parts.

`decimal`(Optional): Is the number of places to the right of the decimal point.

#### Return Type[¶](#id345)

`VARCHAR`.

### Examples[¶](#id346)

### SQL Server[¶](#id347)

**Input:**

```
/* 1 */
SELECT STR(123.5);

/* 2 */
SELECT STR(123.5, 2);

/* 3 */
SELECT STR(123.45, 6);

/* 4 */
SELECT STR(123.45, 6, 1);
```

**Output:**

```
1) 124
2) **
3) 123
4) 123.5
```

#### Snowflake SQL[¶](#id348)

**Input:**

```
/* 1 */
SELECT
PUBLIC.STR_UDF(123.5, '99999');

/* 2 */
SELECT
PUBLIC.STR_UDF(123.5, '99');

/* 3 */
SELECT
PUBLIC.STR_UDF(123.45, '999999');

/* 4 */
SELECT
PUBLIC.STR_UDF(123.45, '9999.9');
```

**Output:**

```
1) 124

2) ##

3) 123
4) 123.5
```

## STR in JS[¶](#str-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id349)

Unfortunately, this functionality is not available in JS, but it can be implemented easily using the
predefined functions for strings.

### Sample Source Pattern[¶](#id350)

#### Implementation Example[¶](#id351)

```
 function validLength(number, max_length, float_precision) {
  var float_point = number.match(/[\.][0-9]+/);
  /*if the number does not have point float, checks if the float precision
   * and current number are greater than max_length
   */
   if(!float_point) return number.length + float_precision + 1 < max_length;
    //removes the '.' and checks if there is overflow with the float_precision
    return number.length - float_point[0].trim('.').length + float_precision  < max_length;
}
 function STR(number, max_length, float_precision) {
  var number_str = number.toString();
   //if the expression exceeds the max_length, returns '**'
   if(number_str.length > max_length || float_precision > max_length) return '**';
   if(validLength(number_str, max_length, float_precision)) {
      return number.toFixed(float_precision);
    }
    return number.toFixed(max_length - float_precision);
}
```

##### Arguments[¶](#id352)

`number`: Float expression with a decimal point.

`max_length`: Length that the returning expression will have, including point notation, decimal, and
float parts.

`float_precision`: Is the number of places to the right of the decimal point.

##### Return Type[¶](#id353)

String.

### Examples[¶](#id354)

#### Query[¶](#id355)

```
 CREATE OR REPLACE FUNCTION STR(number float, max_length float, float_precision float)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
    function validLength(number, max_length, float_precision) {
        var float_point = number.match(/[\.][0-9]+/);
        if(!float_point) return number.length + float_precision + 1 < max_length;
        return number.length - float_point[0].trim('.').length + float_precision  < max_length;
    }
    function STR(number, max_length, float_precision) {
      var number_str = number.toString();
      if(number_str.length > max_length || float_precision > max_length) return '**';
      if(validLength(number_str, max_length, float_precision)) {
        return number.toFixed(float_precision);
      }
      return number.toFixed(max_length - float_precision);
    }
    return STR( NUMBER, MAX_LENGTH, FLOAT_PRECISION );
$$;

SELECT STR(12345.674, 12, 6);
```

##### Result[¶](#id356)

```
           STR|
--------------|
  12345.674000|
```

## LTRIM[¶](#ltrim)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id357)

Returns a character expression after it removes leading blanks
([LTRIM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/ltrim-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id358)

### Syntax[¶](#id359)

```
LTRIM( string_expression )
```

#### Arguments[¶](#id360)

`string_expression:` String expressions to convert.

#### Return Type[¶](#id361)

`VARCHAR` or `NVARCHAR`

### Examples[¶](#id362)

### Query[¶](#id363)

```
SELECT LTRIM('  FIRST TWO BLANK SPACES') AS [LTRIM]
```

#### Result[¶](#id364)

```
                 LTRIM|
----------------------|
FIRST TWO BLANK SPACES|
```

## LTRIM in JS[¶](#ltrim-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id365)

Unfortunately, this function is not available in JavaScript, but it can be implemented using regular
expressions.

### Sample Source Pattern[¶](#id366)

#### Implementation Example[¶](#id367)

```
 function LTRIM(string){
    return string.replace(/^s+/,"");
}
```

##### Arguments[¶](#id368)

`string`: String expression to remove blank spaces.

##### Return Type[¶](#id369)

String.

### Examples[¶](#id370)

#### Query[¶](#id371)

```
 CREATE OR REPLACE FUNCTION ltrim(str varchar)
  RETURNS string
  LANGUAGE JAVASCRIPT
AS
$$
  function LTRIM(string){
    return string.replace(/^s+/,"");
    }
   return LTRIM(S TR );
$$;

SELECT LTRIM('  FIRST TWO BLANK SPACES') AS LTRIM;
```

##### Result[¶](#id372)

```
                 LTRIM|
----------------------|
FIRST TWO BLANK SPACES|
```

## Ranking functions[¶](#ranking-functions)

This section describes the functional equivalents of ranking functions in Transact-SQL to Snowflake
SQL and JavaScript code, oriented to their usage in stored procedures in SnowFlake.

## DENSE_RANK[¶](#dense-rank)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id373)

This function returns the rank of each row within a result set partition, with no gaps in the
ranking values. The rank of a specific row is one plus the number of distinct rank values that come
before that specific row.
([DENSE_RANK in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/dense-rank-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id374)

#### Syntax[¶](#id375)

##### SQL Server[¶](#id376)

```
 DENSE_RANK ( ) OVER ( [ <partition_by_clause> ] < order_by_clause > )
```

##### Snowflake SQL[¶](#id377)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/dense_rank.html)

```
 DENSE_RANK( )
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '1' COLUMN '15' OF THE SOURCE CODE STARTING AT 'OVER'. EXPECTED 'BATCH' GRAMMAR. CODE '80'. **
--              OVER ( [ <partition_by_clause> ] < order_by_clause > )
```

### Examples[¶](#id378)

#### SQL Server[¶](#id379)

```
SELECT TOP 10 BUSINESSENTITYID, NATIONALIDNUMBER, RANK() OVER (ORDER BY NATIONALIDNUMBER) AS RANK FROM HUMANRESOURCES.EMPLOYEE AS TOTAL
```

**Result:**

```
BUSINESSENTITYID|NATIONALIDNUMBER|DENSE_RANK|
----------------|----------------|----------|
              57|10708100        |         1|
              54|109272464       |         2|
             273|112432117       |         3|
               4|112457891       |         4|
             139|113393530       |         5|
             109|113695504       |         6|
             249|121491555       |         7|
             132|1300049         |         8|
             214|131471224       |         9|
              51|132674823       |        10|
```

##### Snowflake SQL[¶](#id380)

```
SELECT TOP 10
BUSINESSENTITYID,
NATIONALIDNUMBER,
RANK() OVER (ORDER BY NATIONALIDNUMBER) AS RANK
FROM
HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

```
BUSINESSENTITYID|NATIONALIDNUMBER|DENSE_RANK|
----------------|----------------|----------|
              57|10708100        |         1|
              54|109272464       |         2|
             273|112432117       |         3|
               4|112457891       |         4|
             139|113393530       |         5|
             109|113695504       |         6|
             249|121491555       |         7|
             132|1300049         |         8|
             214|131471224       |         9|
              51|132674823       |        10|
```

#### Related EWIs[¶](#id381)

- [SSC-EWI-0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0001):
  Unrecognized token on the line of the source code.

## RANK[¶](#rank)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id382)

Returns the rank of each row within the partition of a result set. The rank of a row is one plus the
number of ranks that come before the row in question.
([RANK in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/rank-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id383)

#### Syntax[¶](#id384)

##### SQL Server[¶](#id385)

```
 RANK ( ) OVER ( [ partition_by_clause ] order_by_clause )
```

##### Snowflake SQL[¶](#id386)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/rank.html)

```
 RANK( )
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '1' COLUMN '9' OF THE SOURCE CODE STARTING AT 'OVER'. EXPECTED 'BATCH' GRAMMAR. CODE '80'. **
--        OVER ( [ partition_by_clause ] order_by_clause )
```

### Examples[¶](#id387)

#### SQL Server[¶](#id388)

```
SELECT TOP 10 BUSINESSENTITYID, NATIONALIDNUMBER, RANK() OVER (ORDER BY NATIONALIDNUMBER) AS RANK FROM HUMANRESOURCES.EMPLOYEE AS TOTAL
```

**Result:**

```
BUSINESSENTITYID|NATIONALIDNUMBER|RANK|
----------------|----------------|----|
              57|10708100        |   1|
              54|109272464       |   2|
             273|112432117       |   3|
               4|112457891       |   4|
             139|113393530       |   5|
             109|113695504       |   6|
             249|121491555       |   7|
             132|1300049         |   8|
             214|131471224       |   9|
              51|132674823       |  10|
```

##### Snowflake SQL[¶](#id389)

```
SELECT TOP 10
BUSINESSENTITYID,
NATIONALIDNUMBER,
RANK() OVER (ORDER BY NATIONALIDNUMBER) AS RANK
FROM
HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

```
BUSINESSENTITYID|NATIONALIDNUMBER|RANK|
----------------|----------------|----|
              57|10708100        |   1|
              54|109272464       |   2|
             273|112432117       |   3|
               4|112457891       |   4|
             139|113393530       |   5|
             109|113695504       |   6|
             249|121491555       |   7|
             132|1300049         |   8|
             214|131471224       |   9|
              51|132674823       |  10|
```

#### Related EWIs[¶](#id390)

- [SSC-EWI-0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0001):
  Unrecognized token on the line of the source code.

## ROW_NUMBER[¶](#row-number)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id391)

Numbers the output of a result set. More specifically, returns the sequential number of a row within
a partition of a result set, starting at 1 for the first row in each partition.
([ROW_NUMBER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/row-number-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id392)

#### Syntax[¶](#id393)

##### SQL Server[¶](#id394)

```
 ROW_NUMBER ( )
    OVER ( [ PARTITION BY value_expression , ... [ n ] ] order_by_clause )
```

##### Snowflake SQL[¶](#id395)

[Snowflake SQL complete documentation](https://docs.snowflake.com/en/sql-reference/functions/row_number.html)

```
 ROW_NUMBER( )
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '2' COLUMN '5' OF THE SOURCE CODE STARTING AT 'OVER'. EXPECTED 'BATCH' GRAMMAR. CODE '80'. **
--    OVER ( [ PARTITION BY value_expression , ... [ n ] ] order_by_clause )
```

### Examples[¶](#id396)

#### SQL Server[¶](#id397)

```
SELECT
ROW_NUMBER() OVER(ORDER BY NAME  ASC) AS RowNumber,
NAME
FROM HUMANRESOURCES.DEPARTMENT
```

**Output:**

```
RowNumber|NAME                      |
---------|--------------------------|
        1|Document Control          |
        2|Engineering               |
        3|Executive                 |
        4|Facilities and Maintenance|
        5|Finance                   |
        6|Human Resources           |
        7|Information Services      |
        8|Marketing                 |
        9|Production                |
       10|Production Control        |
       11|Purchasing                |
       12|Quality Assurance         |
       13|Research and Development  |
       14|Sales                     |
       15|Shipping and Receiving    |
       16|Tool Design               |
```

##### Snowflake SQL[¶](#id398)

```
SELECT
ROW_NUMBER() OVER(ORDER BY NAME ASC) AS RowNumber,
NAME
FROM
HUMANRESOURCES.DEPARTMENT;
```

**Output:**

```
RowNumber|NAME                      |
---------|--------------------------|
        1|Document Control          |
        2|Engineering               |
        3|Executive                 |
        4|Facilities and Maintenance|
        5|Finance                   |
        6|Human Resources           |
        7|Information Services      |
        8|Marketing                 |
        9|Production                |
       10|Production Control        |
       11|Purchasing                |
       12|Quality Assurance         |
       13|Research and Development  |
       14|Sales                     |
       15|Shipping and Receiving    |
       16|Tool Design               |
```

#### Related EWIs[¶](#id399)

- [SSC-EWI-0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0001):
  Unrecognized token on the line of the source code.

## Logical functions[¶](#logical-functions)

This section describes the functional equivalents of logical functions in Transact-SQL to Snowflake
SQL and JavaScript code, oriented to their usage in stored procedures in SnowFlake.

## IIF[¶](#iif)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id400)

Returns one of two values, depending on whether the Boolean expression evaluates to true or false.
([IIF in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/logical-functions-iif-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id401)

#### Syntax[¶](#id402)

##### SQL Server[¶](#id403)

```
IIF( boolean_expression, true_value, false_value )
```

##### Snowflake SQL[¶](#id404)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/iff.html)

```
IFF( <condition> , <expr1> , <expr2> )
```

### Examples[¶](#id405)

#### SQL Server[¶](#id406)

```
SELECT IIF( 2 > 3, 'TRUE', 'FALSE' ) AS RESULT
```

**Result:**

```
RESULT|
------|
 FALSE|
```

##### Snowflake SQL[¶](#id407)

```
SELECT
IFF( 2 > 3, 'TRUE', 'FALSE' ) AS RESULT;
```

**Result:**

```
RESULT|
------|
 FALSE|
```

## XML Functions[¶](#xml-functions)

This section describes the translation of XML functions in Transact-SQL to Snowflake SQL.

## Query[¶](#id408)

Applies to

- SQL Server

Warning

This transformation will be delivered in the future

### Description[¶](#id409)

Specifies an XQuery against an instance of the **xml** data type. The result is of **xml** type. The
method returns an instance of untyped XML.
([`Query() in Transact-SQL`](https://learn.microsoft.com/en-us/sql/t-sql/xml/query-method-xml-data-type?view=sql-server-ver16))

### Sample Source Patterns [¶](#sample-source-patterns)

The following example details the transformation for .query( )

#### SQL Server [¶](#id410)

##### Input[¶](#input)

```
 CREATE TABLE xml_demo(object_col XML);

INSERT INTO xml_demo (object_col)
   SELECT
        '<Root>
<ProductDescription ProductID="1" ProductName="Road Bike">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

INSERT INTO xml_demo (object_col)
   SELECT
        '<Root>
<ProductDescription ProductID="2" ProductName="Skate">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

SELECT
    xml_demo.object_col.query('/Root/ProductDescription/Features/Warranty') as Warranty,
    xml_demo.object_col.query('/Root/ProductDescription/Features/Maintenance') as Maintenance
from xml_demo;
```

##### Output[¶](#output)

```
 Warranty                                     | Maintenance                                                                          |
----------------------------------------------|--------------------------------------------------------------------------------------|
<Warranty>1 year parts and labor</Warranty>   | <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>  |
<Warranty>1 year parts and labor</Warranty>   | <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>  |
```

##### Snowflake SQL [¶](#id411)

##### Input[¶](#id412)

```
 CREATE OR REPLACE TABLE xml_demo (
    object_col VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - XML DATA TYPE CONVERTED TO VARIANT ***/!!!
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO xml_demo (object_col)
SELECT
        '<Root>
<ProductDescription ProductID="1" ProductName="Road Bike">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

INSERT INTO xml_demo (object_col)
SELECT
        '<Root>
<ProductDescription ProductID="2" ProductName="Skate">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

SELECT
    XMLGET(XMLGET(XMLGET(object_col, 'ProductDescription'), 'Features'), 'Warranty') as Warranty,
    XMLGET(XMLGET(XMLGET(object_col, 'ProductDescription'), 'Features'), 'Maintenance') as Maintenance
from
    xml_demo;
```

##### Output[¶](#id413)

```
 Warranty                                     | Maintenance                                                                          |
----------------------------------------------|--------------------------------------------------------------------------------------|
<Warranty>1 year parts and labor</Warranty>   | <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>  |
<Warranty>1 year parts and labor</Warranty>   | <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>  |
```

### Known Issues[¶](#known-issues)

No issues were found.

### Related EWIs[¶](#id414)

1. [SSC-EWI-0036](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036):
   Data type converted to another data type.

## Value[¶](#value)

Applies to

- SQL Server

Warning

This transformation will be delivered in the future

### Description[¶](#id415)

Performs an XQuery against the XML and returns a value of SQL type. This method returns a scalar
value.
([`value() in Transact-SQL`](https://learn.microsoft.com/en-us/sql/t-sql/xml/value-method-xml-data-type?view=sql-server-ver16)).

### Sample Source Patterns [¶](#id416)

The following example details the transformation for .value( )

#### SQL Server [¶](#id417)

##### Input[¶](#id418)

```
 CREATE TABLE xml_demo(object_col XML);

INSERT INTO xml_demo (object_col)
   SELECT
        '<Root>
<ProductDescription ProductID="1" ProductName="Road Bike">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

INSERT INTO xml_demo (object_col)
   SELECT
        '<Root>
<ProductDescription ProductID="2" ProductName="Skate">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

SELECT
    xml_demo.object_col.value('(/Root/ProductDescription/@ProductID)[1]', 'int' ) as ID,
    xml_demo.object_col.value('(/Root/ProductDescription/@ProductName)[1]', 'varchar(max)' ) as ProductName,
    xml_demo.object_col.value('(/Root/ProductDescription/Features/Warranty)[1]', 'varchar(max)' ) as Warranty
from xml_demo;
```

##### Output[¶](#id419)

```
 ID | ProductName | Warranty               |
----|-------------|------------------------|
1   | Road Bike   | 1 year parts and labor |
2   | Skate       | 1 year parts and labor |
```

##### Snowflake SQL [¶](#id420)

##### Input[¶](#id421)

```
 CREATE OR REPLACE TABLE xml_demo (
    object_col VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - XML DATA TYPE CONVERTED TO VARIANT ***/!!!
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO xml_demo (object_col)
SELECT
        '<Root>
<ProductDescription ProductID="1" ProductName="Road Bike">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

INSERT INTO xml_demo (object_col)
SELECT
        '<Root>
<ProductDescription ProductID="2" ProductName="Skate">
<Features>
  <Warranty>1 year parts and labor</Warranty>
  <Maintenance>3 year parts and labor extended maintenance is available</Maintenance>
</Features>
</ProductDescription>
</Root>';

SELECT
    GET(XMLGET(object_col, 'ProductDescription'), '@ProductID') :: INT as ID,
    GET(XMLGET(object_col, 'ProductDescription'), '@ProductName') :: VARCHAR as ProductName,
    GET(XMLGET(XMLGET(XMLGET(object_col, 'ProductDescription'), 'Features'), 'Warranty', 0), '$') :: VARCHAR as Warranty
from
    xml_demo;
```

##### Output[¶](#id422)

```
 ID | PRODUCTNAME | WARRANRTY              |
----|-------------|------------------------|
1   | Road Bike   | 1 year parts and labor |
2   | Skate       | 1 year parts and labor |
```

### Known Issues[¶](#id423)

No issues were found.

### Related EWIs[¶](#id424)

1. [SSC-EWI-0036](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036):
   Data type converted to another data type.

## Aggregate functions[¶](#aggregate-functions)

This section describes the functional equivalents of aggregate functions in Transact-SQL to
Snowflake SQL and JavaScript code, oriented to the creation of UDFs in Snowflake.

## COUNT[¶](#count)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id425)

This function returns the number of items found in a group. COUNT operates like the COUNT_BIG
function. These functions differ only in the data types of their return values. COUNT always returns
an int data type value. COUNT_BIG always returns a bigint data type value.
([COUNT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id426)

#### Syntax[¶](#id427)

##### SQL Server[¶](#id428)

```
COUNT ( { [ [ ALL | DISTINCT ] expression ] | * } )
```

##### Snowflake SQL[¶](#id429)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/count.html)

```
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] )
```

### Examples[¶](#id430)

#### SQL Server[¶](#id431)

```
SELECT COUNT(NATIONALIDNUMBER) FROM HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

<!-- prettier-ignore -->
|TOTAL|
|---|
|290|

##### Snowflake SQL[¶](#id432)

```
SELECT
COUNT(NATIONALIDNUMBER) FROM
HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

<!-- prettier-ignore -->
|TOTAL|
|---|
|290|

## COUNT_BIG[¶](#count-big)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id433)

This function returns the number of items found in a group. COUNT_BIG operates like the COUNT
function. These functions differ only in the data types of their return values. COUNT_BIG always
returns a bigint data type value. COUNT always returns an int data type value.
([COUNT_BIG in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/count-big-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id434)

#### Syntax[¶](#id435)

##### SQL Server[¶](#id436)

```
COUNT_BIG ( { [ [ ALL | DISTINCT ] expression ] | * } )
```

##### Snowflake SQL[¶](#id437)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/count.html)

```
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] )
```

### Examples[¶](#id438)

#### SQL Server[¶](#id439)

```
SELECT COUNT_BIG(NATIONALIDNUMBER) FROM HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

<!-- prettier-ignore -->
|TOTAL|
|---|
|290|

##### Snowflake SQL[¶](#id440)

```
SELECT
COUNT(NATIONALIDNUMBER) FROM
HUMANRESOURCES.EMPLOYEE AS TOTAL;
```

**Result:**

<!-- prettier-ignore -->
|TOTAL|
|---|
|290|

## SUM[¶](#sum)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id441)

Returns the sum of all the values, or only the DISTINCT values, in the expression. SUM can be used
with numeric columns only. Null values are ignored.
([SUM in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/sum-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id442)

#### Syntax[¶](#id443)

##### SQL Server[¶](#id444)

```
SUM ( [ ALL | DISTINCT ] expression )
```

##### Snowflake SQL[¶](#id445)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/sum.html)

```
SUM( [ DISTINCT ] <expr1> )
```

### Examples[¶](#id446)

#### SQL Server[¶](#id447)

```
SELECT SUM(VACATIONHOURS) FROM HUMANRESOURCES.EMPLOYEE AS TOTALVACATIONHOURS;
```

**Result:**

<!-- prettier-ignore -->
|TOTALVACATIONHOURS|
|---|
|14678|

##### Snowflake SQL[¶](#id448)

```
SELECT
SUM(VACATIONHOURS) FROM
HUMANRESOURCES.EMPLOYEE AS TOTALVACATIONHOURS;
```

**Result:**

<!-- prettier-ignore -->
|TOTALVACATIONHOURS|
|---|
|14678|

## SnowConvert AI custom UDFs[¶](#snowconvert-ai-custom-udfs)

### Description[¶](#id449)

Some Transact-SQL functions or behaviors may not be available or may behave differently in
Snowflake. To minimize these differences, some functions are replaced with SnowConvert AI Custom
UDFs.

These UDFs are automatically created during migration, in the `UDF Helper` folder, inside the
`Output` folder. There is one file per custom UDF.

## OPENXML UDF[¶](#openxml-udf)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id450)

This custom UDF is added to process a rowset view over an XML document. This would be used for
declarations in because it works as a rowset provider.

[Optional parameters](https://learn.microsoft.com/en-us/sql/t-sql/functions/openxml-transact-sql?view=sql-server-ver16#remarks)
and different node types are not supported in this version of the UDF. The element node is processed
by default.

### Custom UDF overloads[¶](#custom-udf-overloads)

**Parameters**

1. **XML**: A `VARCHAR` that represents the readable content of the XML.
2. **PATH**: A varchar that contains the pattern of the nodes to be processed as rows.

#### UDF[¶](#udf)

```
CREATE OR REPLACE FUNCTION OPENXML_UDF(XML VARCHAR, PATH VARCHAR)
RETURNS TABLE(VALUE VARIANT)
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
SELECT VALUE from TABLE(FLATTEN(input=>XML_JSON_SIMPLE(PARSE_XML(XML)), path=>PATH))
$$;


CREATE OR REPLACE FUNCTION XML_JSON_SIMPLE(XML VARIANT)
RETURNS OBJECT
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
function toNormalJSON(xmlJSON) {
    var finalres = {};
    var name=xmlJSON['@'];
    var res = {};
    finalres[name] = res;
    for(var key in xmlJSON)
    {
        if (key == "@")
        {
            res["$name"] = xmlJSON["@"];
        }
        else if (key == "$") {
            continue;
        }
        else if (key.startsWith("@"))
        {
            // This is an attribute
            res[key]=xmlJSON[key];
        }
        else
        {
            var elements = xmlJSON['$']
            var value = xmlJSON[key];
            res[key] = [];
            if (Array.isArray(value))
            {
                for(var elementKey in value)
                {
                    var currentElement = elements[elementKey];
                    var fixedElement = toNormalJSON(currentElement);
                    res[key].push(fixedElement);
                }
            }
            else if (value === 0)
            {
                var fixedElement = toNormalJSON(elements);
                res[key].push(fixedElement);
            }
        }
    }
    return finalres;
}
return toNormalJSON(XML);
$$;
```

##### Transact-SQL[¶](#transact-sql)

##### Query[¶](#id451)

```
DECLARE @idoc INT, @doc VARCHAR(1000);
SET @doc ='
<ROOT>
<Customer CustomerID="VINET" ContactName="Paul Henriot">
   <Order CustomerID="VINET" EmployeeID="5" OrderDate="1996-07-04T00:00:00">
      <OrderDetail OrderID="10248" ProductID="11" Quantity="12"/>
      <OrderDetail OrderID="10248" ProductID="42" Quantity="10"/>
   </Order>
</Customer>
<Customer CustomerID="LILAS" ContactName="Carlos Gonzlez">
   <Order CustomerID="LILAS" EmployeeID="3" OrderDate="1996-08-16T00:00:00">
      <OrderDetail OrderID="10283" ProductID="72" Quantity="3"/>
   </Order>
</Customer>
</ROOT>';

EXEC sp_xml_preparedocument @idoc OUTPUT, @doc;

SELECT *  FROM OPENXML (@idoc, '/ROOT/Customer',1)
WITH (CustomerID  VARCHAR(10), ContactName VARCHAR(20));
```

##### Result[¶](#id452)

```
CustomerID  | ContactName
----------------------------|
VINET     | Paul Henriot
LILAS     | Carlos Gonzlez
```

##### Snowflake[¶](#id453)

**Note:**

The following example is isolated into a stored procedure because environment variables only support
256 bytes of storage, and the XML demo code uses more than that limit.

##### Query[¶](#id454)

```
DECLARE
IDOC INT;
DOC VARCHAR(1000);
BlockResultSet RESULTSET;
BEGIN
DOC := '
<ROOT>
<Customer CustomerID="VINET" ContactName="Paul Henriot">
   <Order CustomerID="VINET" EmployeeID="5" OrderDate="1996-07-04T00:00:00">
      <OrderDetail OrderID="10248" ProductID="11" Quantity="12"/>
      <OrderDetail OrderID="10248" ProductID="42" Quantity="10"/>
   </Order>
</Customer>
<Customer CustomerID="LILAS" ContactName="Carlos Gonzlez">
   <Order CustomerID="LILAS" EmployeeID="3" OrderDate="1996-08-16T00:00:00">
      <OrderDetail OrderID="10283" ProductID="72" Quantity="3"/>
   </Order>
</Customer>
</ROOT>';
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0075 - TRANSLATION FOR BUILT-IN PROCEDURE 'sp_xml_preparedocument' IS NOT CURRENTLY SUPPORTED. ***/!!!

EXEC sp_xml_preparedocument :IDOC OUTPUT, :DOC;
BlockResultSet := (

SELECT
Left(value:Customer['@CustomerID'], '10') AS 'CustomerID',
Left(value:Customer['@ContactName'], '20') AS 'ContactName'
FROM
OPENXML_UDF(:IDOC, ':ROOT:Customer'));
RETURN TABLE(BlockResultSet);
END;
```

##### Result[¶](#id455)

<!-- prettier-ignore -->
|CustomerID|ContactName|
|---|---|
|VINET|Paul Henriot|
|LILAS|Carlos Gonzlez|

##### Query[¶](#id456)

```
SET code = '<ROOT>
<Customer CustomerID="VINET" ContactName="Paul Henriot">
   <Order CustomerID="VINET" EmployeeID="5" OrderDate="1996-07-04T00:00:00">
      <OrderDetail OrderID="10248" ProductID="11" Quantity="12"/>
   </Order>
</Customer>
</ROOT>';
SELECT
Left(value:Customer['@CustomerID'],10) as "CustomerID",
Left(value:Customer['@ContactName'],20) as "ContactName"
FROM TABLE(OPENXML_UDF($code,'ROOT:Customer'));
```

##### Result[¶](#id457)

<!-- prettier-ignore -->
|CustomerID|ContactName|
|---|---|
|VINET|Paul Henriot|

### Known Issues[¶](#id458)

No issues were found.

### Related EWIs[¶](#id459)

1. [SSC-EWI-TS0075](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sqlServerEWI.html#ssc-ewi-ts0075):
   Built In Procedure Not Supported.

## STR UDF[¶](#str-udf)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id460)

This custom UDF converts numeric data to character data.

### Custom UDF overloads[¶](#id461)

#### Parameters[¶](#parameters)

1. **FLOAT_EXPR**: A numeric expression to be converted to varchar.
2. **FORMAT**: A varchar expression with the length and number of decimals of the resulting varchar.
   This format is automatically generated in SnowConvert.

##### UDF[¶](#id462)

```
 CREATE OR REPLACE FUNCTION PUBLIC.STR_UDF(FLOAT_EXPR FLOAT, FORMAT VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    TRIM(TRIM(SELECT TO_CHAR(FLOAT_EXPR, FORMAT)), '.')
$$;

CREATE OR REPLACE FUNCTION PUBLIC.STR_UDF(FLOAT_EXPR FLOAT)
RETURNS VARCHAR
LANGUAGE SQL
IMMUTABLE
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
    STR_UDF(FLOAT_EXPR, '999999999999999999')
$$;
```

##### Transact-SQL[¶](#id463)

##### Query[¶](#id464)

```
SELECT
    STR(123.5) as A,
    STR(123.5, 2) as B,
    STR(123.45, 6) as C,
    STR(123.45, 6, 1) as D;
```

##### Result[¶](#id465)

<!-- prettier-ignore -->
|A|B|C|D|
|---|---|---|---|
|124|\*\*|123|123.5|

##### Snowflake[¶](#id466)

##### Query[¶](#id467)

```
SELECT
    PUBLIC.STR_UDF(123.5, '99999') as A,
    PUBLIC.STR_UDF(123.5, '99') as B,
    PUBLIC.STR_UDF(123.45, '999999') as C,
    PUBLIC.STR_UDF(123.45, '9999.9') as D;
```

## SWITCHOFFSET_UDF[¶](#switchoffset-udf)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id468)

This custom UDF is added to return a datetimeoffset value that is changed from the stored time zone
offset to a specified new time zone offset.

### Custom UDF overloads[¶](#id469)

**Parameters**

1. **source_timestamp**: A TIMESTAMP_TZ that can be resolved to a datetimeoffset(n) value.
2. **target_tz**: A varchar that represents the time zone offset

#### UDF[¶](#id470)

```
CREATE OR REPLACE FUNCTION PUBLIC.SWITCHOFFSET_UDF(source_timestamp TIMESTAMP_TZ, target_tz varchar)
RETURNS TIMESTAMP_TZ
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
WITH tz_values AS (
SELECT
    RIGHT(source_timestamp::varchar, 5) as source_tz,

    REPLACE(source_tz::varchar, ':', '') as source_tz_clean,
    REPLACE(target_tz::varchar, ':', '') as target_tz_clean,

    target_tz_clean::integer - source_tz_clean::integer as offset,

    RIGHT(offset::varchar, 2) as tz_min,
    PUBLIC.OFFSET_FORMATTER(RTRIM(offset::varchar, tz_min)) as tz_hrs,


    TIMEADD( hours, tz_hrs::integer, source_timestamp ) as adj_hours,
    TIMEADD( minutes, (LEFT(tz_hrs, 1) || tz_min)::integer, adj_hours::timestamp_tz ) as new_timestamp

FROM DUAL)
SELECT
    (LEFT(new_timestamp, 24) || ' ' || target_tz)::timestamp_tz
FROM tz_values
$$;

-- ==========================================================================
-- Description: The function OFFSET_FORMATTER(offset_hrs varchar) serves as
-- an auxiliar function to format the offter hours and its prefix operator.
-- ==========================================================================
CREATE OR REPLACE FUNCTION PUBLIC.OFFSET_FORMATTER(offset_hrs varchar)
RETURNS varchar
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"udf"}}'
AS
$$
CASE
   WHEN LEN(offset_hrs) = 0 THEN '+' || '0' || '0'
   WHEN LEN(offset_hrs) = 1 THEN '+' || '0' || offset_hrs
   WHEN LEN(offset_hrs) = 2 THEN
        CASE
            WHEN LEFT(offset_hrs, 1) = '-' THEN '-' || '0' || RIGHT(offset_hrs, 1)
            ELSE '+' || offset_hrs
        END
    ELSE offset_hrs
END
$$;
```

##### Transact-SQL[¶](#id471)

##### Query[¶](#id472)

```
SELECT
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  SWITCHOFFSET('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

##### Result[¶](#id473)

```
SELECT
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  SWITCHOFFSET('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

##### Snowflake[¶](#id474)

##### Query[¶](#id475)

```
SELECT
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  PUBLIC.SWITCHOFFSET_UDF('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

##### Result[¶](#id476)

<!-- prettier-ignore -->
|fr_time|cr_time|
|---|---|
|1998-09-20 7:45:50.71345 +02:00|1998-09-19 23:45:50.7134500 -06:00|

## Metadata functions[¶](#metadata-functions)

This section describes the functional equivalents of metadata functions in Transact-SQL to Snowflake
SQL and JavaScript code, oriented to their usage in stored procedures in SnowFlake.

## DB_NAME[¶](#db-name)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id477)

This function returns the name of a specified
database.([DB_NAME in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/db-name-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern[¶](#id478)

#### Syntax[¶](#id479)

##### SQL Server[¶](#id480)

```
 DB_NAME ( [ database_id ] )
```

##### Snowflake SQL[¶](#id481)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/current_database.html)

```
 CURRENT_DATABASE() /*** SSC-FDM-TS0010 - CURRENT_DATABASE function has different behavior in certain cases ***/
```

### Examples[¶](#id482)

#### SQL Server[¶](#id483)

```
SELECT DB_NAME();
```

**Result:**

<!-- prettier-ignore -->
|RESULT|
|---|
|ADVENTUREWORKS2019|

##### Snowflake SQL[¶](#id484)

```
SELECT
CURRENT_DATABASE() /*** SSC-FDM-TS0010 - CURRENT_DATABASE function has different behavior in certain cases ***/;
```

**Result:**

<!-- prettier-ignore -->
|RESULT|
|---|
|ADVENTUREWORKS2019|

### Known issues[¶](#id485)

**1. CURRENT_DATABASE function has different behavior in certain cases**

DB_NAME function can be invoked with the **database_id** parameter, which returns the name of the
specified database. Without parameters, the function returns the current database name. However,
SnowFlake does not support this parameter and the CURRENT_DATABASE function will always return the
current database name.

### Related EWIs[¶](#id486)

1. [SSC-FDM-TS0010](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0010):
   CURRENT_DATABASE function has different behavior in certain cases.

## OBJECT_ID[¶](#object-id)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id487)

This function returns the database object identification number of a schema-scoped
object.[(OBJECT_ID in Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/functions/object-id-transact-sql?view=sql-server-ver16).

#### SQL Server syntax[¶](#sql-server-syntax)

```
 OBJECT_ID ( '[ database_name . [ schema_name ] . | schema_name . ]
  object_name' [ ,'object_type' ] )
```

### Sample Source Patterns[¶](#id488)

#### 1. Default transformation[¶](#default-transformation)

##### SQL Server[¶](#id489)

```
 IF OBJECT_ID_UDF('DATABASE2.DBO.TABLE1') is not null) THEN
            DROP TABLE IF EXISTS TABLE1;
        END IF;
```

##### Snowflake SQL[¶](#id490)

```
 BEGIN
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '1' COLUMN '0' OF THE SOURCE CODE STARTING AT 'IF'. EXPECTED 'If Statement' GRAMMAR. LAST MATCHING TOKEN WAS 'null' ON LINE '1' COLUMN '48'. FAILED TOKEN WAS ')' ON LINE '1' COLUMN '52'. CODE '70'. **
--IF OBJECT_ID_UDF('DATABASE2.DBO.TABLE1') is not null) THEN
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
DROP TABLE IF EXISTS TABLE1;
END;
```

#### 2. Unknown database[¶](#unknown-database)

##### SQL Server[¶](#id491)

```
 IF OBJECT_ID_UDF('DATABASE1.DBO.TABLE1') is not null) THEN
            DROP TABLE IF EXISTS TABLE1;
        END IF;
```

##### Snowflake SQL[¶](#id492)

```
  IF (
 OBJECT_ID_UDF('DATABASE1.DBO.TABLE1') is not null) THEN
     DROP TABLE IF EXISTS TABLE1;
 END IF;
```

#### 3. Different object names[¶](#different-object-names)

##### SQL Server[¶](#id493)

```
 IF OBJECT_ID_UDF('DATABASE1.DBO.TABLE2') is not null) THEN
            DROP TABLE IF EXISTS TABLE1;
        END IF;
```

##### Snowflake SQL[¶](#id494)

```
  IF (
 OBJECT_ID_UDF('DATABASE1.DBO.TABLE2') is not null) THEN
     DROP TABLE IF EXISTS TABLE1;
 END IF;
```

### Known issues[¶](#id495)

**1. OBJECT_ID_UDF function has different behavior in certain cases**

OBJECT_ID returns the object identification number but the OBJECT_ID_UDF returns a boolean value, so
that they are equivalent only when OBJECT_ID is used with not null condition.

### Related EWIs[¶](#id496)

- [SSC-EWI-0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0001):
  Unrecognized token on the line of the source code.
- [SSC-FDM-0007](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0007):
  Element with missing dependencies

## Analytic Functions[¶](#analytic-functions)

This section describes the functional equivalents of analytic functions in Transact-SQL to Snowflake
SQL and JavaScript code, oriented to the creation of UDFs in Snowflake.

## LAG[¶](#lag)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id497)

Accesses data from a previous row in the same result set without the use of a self-join starting
with SQL Server 2012 (11.x). LAG provides access to a row at a given physical offset that comes
before the current row. Use this analytic function in a SELECT statement to compare values in the
current row with values in a previous row. ([COUNT in Transact-SQL](#lag)).

### Sample Source Pattern[¶](#id498)

#### Syntax[¶](#id499)

##### SQL Server[¶](#id500)

```
LAG (scalar_expression [,offset] [,default])
    OVER ( [ partition_by_clause ] order_by_clause )
```

##### Snowflake SQL[¶](#id501)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/count.html)

```
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] )
```

### Examples[¶](#id502)

#### SQL Server[¶](#id503)

```
SELECT TOP 10
LAG(E.VacationHours,1) OVER(ORDER BY E.NationalIdNumber) as PREVIOUS,
E.VacationHours AS ACTUAL
FROM HumanResources.Employee E
```

**Result:**

<!-- prettier-ignore -->
|PREVIOUS|ACTUAL|
|---|---|
|NULL|10|
|10|89|
|89|10|
|10|48|
|48|0|
|0|95|
|95|55|
|55|67|
|67|84|
|84|85|

##### Snowflake SQL[¶](#id504)

```
SELECT TOP 10
LAG(E.VacationHours,1) OVER(ORDER BY E.NationalIdNumber) as PREVIOUS,
E.VacationHours AS ACTUAL
FROM
HumanResources.Employee E;
```

**Result:**

<!-- prettier-ignore -->
|PREVIOUS|ACTUAL|
|---|---|
|NULL|10|
|10|89|
|89|10|
|10|48|
|48|0|
|0|95|
|95|55|
|55|67|
|67|84|
|84|85|

## Data Type functions[¶](#data-type-functions)

This section describes the functional equivalents of data type functions in Transact-SQL to
Snowflake SQL and JavaScript code.

## DATALENGTH[¶](#datalength)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id505)

This function returns the number of bytes used to represent any expression.
([DATALENGTH in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/datalength-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id506)

#### Syntax[¶](#id507)

##### SQL Server[¶](#id508)

```
DATALENGTH ( expression )
```

##### Snowflake SQL[¶](#id509)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/cast.html)

```
OCTET_LENGTH(<string_or_binary>)
```

### Examples[¶](#id510)

#### SQL Server[¶](#id511)

```
SELECT DATALENGTH('SomeString') AS SIZE;
```

**Result:**

<!-- prettier-ignore -->
|SIZE|
|---|
|10|

##### Snowflake SQL[¶](#id512)

```
SELECT OCTET_LENGTH('SomeString') AS SIZE;
```

**Result:**

<!-- prettier-ignore -->
|SIZE|
|---|
|10|

## Mathematical functions[¶](#mathematical-functions)

This section describes the functional equivalents of mathematical functions in Transact-SQL to
Snowflake SQL and JavaScript code, oriented to their usage in stored procedures in SnowFlake.

## ABS[¶](#abs)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id513)

A mathematical function that returns the absolute (positive) value of the specified numeric
expression. (`ABS` changes negative values to positive values. `ABS` has no effect on zero or
positive values.)
([ABS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/abs-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id514)

#### Syntax[¶](#id515)

##### SQL Server[¶](#id516)

```
ABS( expression )
```

##### Snowflake SQL[¶](#id517)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/abs.html)

```
ABS( <num_expr> )
```

##### JavaScript[¶](#id518)

[JavaScript complete documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/abs)

```
Math.abs( expression )
```

### Examples[¶](#id519)

#### SQL Server[¶](#id520)

```
SELECT ABS(-5);
```

**Result:**

<!-- prettier-ignore -->
|ABS(-5)|
|---|
|5|

##### Snowflake SQL[¶](#id521)

```
SELECT ABS(-5);
```

**Result:**

<!-- prettier-ignore -->
|ABS(-5)|
|---|
|5|

##### JavaScript[¶](#id522)

```
CREATE OR REPLACE FUNCTION compute_abs(a float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return Math.abs(A);
$$
;
SELECT COMPUTE_ABS(-5);
```

**Result:**

<!-- prettier-ignore -->
|COMPUTE_ABS(-5)|
|---|
|5|

### Related Documentation[¶](#related-documentation)

- [Transact-SQL supported numeric types](https://docs.microsoft.com/en-us/sql/t-sql/data-types/numeric-types?view=sql-server-ver15)

## AVG[¶](#avg)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id523)

**Note:**

SnowConvert AI Helpers Code section is omitted.

This function returns the average of the values in a group. It ignores null values.
([AVG in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/avg-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id524)

#### Syntax[¶](#id525)

##### SQL Server[¶](#id526)

```
AVG ( [ ALL | DISTINCT ] expression )
   [ OVER ( [ partition_by_clause ] order_by_clause ) ]
```

##### Snowflake SQL[¶](#id527)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/avg.html)

```
AVG( [ DISTINCT ] <expr1> )

AVG( [ DISTINCT ] <expr1> ) OVER (
                                 [ PARTITION BY <expr2> ]
                                 [ ORDER BY <expr3> [ ASC | DESC ] [ <window_frame> ] ]
                                 )
```

### Examples[¶](#id528)

#### SQL Server[¶](#id529)

```
SELECT AVG(VACATIONHOURS) AS AVG_VACATIONS FROM HUMANRESOURCES.EMPLOYEE;
```

**Result:**

<!-- prettier-ignore -->
|AVG_VACATIONS|
|---|
|50|

##### Snowflake SQL[¶](#id530)

```
SELECT AVG(VACATIONHOURS) AS AVG_VACATIONS FROM HUMANRESOURCES.EMPLOYEE;
```

**Result:**

<!-- prettier-ignore -->
|AVG_VACATIONS|
|---|
|50|

## CEILING[¶](#ceiling)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id531)

A mathematical function that returns the smallest greater integer greater/equal to the number sent
as a parameter
([CEILING in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/ceiling-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id532)

#### Syntax[¶](#id533)

##### SQL Server[¶](#id534)

```
CEILING( expression )
```

##### Snowflake SQL[¶](#id535)

```
CEIL( <input_expr> [, <scale_expr> ] )
```

##### JavaScript[¶](#id536)

```
 Math.ceil( expression )
```

### Examples[¶](#id537)

#### SQL Server[¶](#id538)

```
SELECT CEILING(642.20);
```

**Result:**

<!-- prettier-ignore -->
|CEILING(642.20)|
|---|
|643|

##### Snowflake SQL[¶](#id539)

```
SELECT CEIL(642.20);
```

**Result:**

<!-- prettier-ignore -->
|CEIL(642.20)|
|---|
|643|

##### JavaScript[¶](#id540)

```
CREATE OR REPLACE FUNCTION compute_ceil(a double)
RETURNS double
LANGUAGE JAVASCRIPT
AS
$$
  return Math.ceil(A);
$$
;
SELECT COMPUTE_CEIL(642.20);
```

**Result:**

```
COMPUTE_CEIL(642.20)|
--------------------|
                 643|
```

## FLOOR[¶](#floor)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id541)

Returns the largest integer less than or equal to the specified numeric expression.
([FLOOR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/floor-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id542)

#### Syntax[¶](#id543)

##### SQL Server[¶](#id544)

```
FLOOR ( numeric_expression )
```

##### Snowflake SQL[¶](#id545)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/floor.html)

```
FLOOR( <input_expr> [, <scale_expr> ] )
```

### Examples[¶](#id546)

#### SQL Server[¶](#id547)

```
SELECT FLOOR (124.87) AS FLOOR;
```

**Result:**

```
FLOOR|
-----|
  124|
```

##### Snowflake SQL[¶](#id548)

```
SELECT FLOOR (124.87) AS FLOOR;
```

**Result:**

```
FLOOR|
-----|
  124|
```

## POWER[¶](#power)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id549)

Returns the value of the specified expression to the specified power.
([POWER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/power-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id550)

#### Syntax[¶](#id551)

##### SQL Server[¶](#id552)

```
POWER ( float_expression , y )
```

##### Snowflake SQL[¶](#id553)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/pow.html)

```
POW(x, y)

POWER (x, y)
```

### Examples[¶](#id554)

#### SQL Server[¶](#id555)

```
SELECT POWER(2, 10.0) AS IntegerResult
```

**Result:**

```
IntegerResult |
--------------|
          1024|
```

##### Snowflake SQL[¶](#id556)

```
SELECT POWER(2, 10.0) AS IntegerResult;
```

**Result:**

```
IntegerResult |
--------------|
          1024|
```

### Related Documentation[¶](#id557)

- [SQL Server supported numeric types](https://docs.microsoft.com/en-us/sql/t-sql/data-types/numeric-types?view=sql-server-ver15)

## ROUND[¶](#round)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id558)

Returns a numeric value, rounded to the specified length or precision.
([ROUND in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/round-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id559)

#### Syntax[¶](#id560)

##### SQL Server[¶](#id561)

```
ROUND ( numeric_expression , length [ ,function ] )
```

##### Snowflake SQL[¶](#id562)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/round.html)

```
ROUND( <input_expr> [, <scale_expr> ] )
```

### Examples[¶](#id563)

#### SQL Server[¶](#id564)

```
SELECT ROUND(123.9994, 3) AS COL1, ROUND(123.9995, 3) AS COL2;
```

**Result:**

```
COL1    |COL2    |
--------|--------|
123.9990|124.0000|
```

##### Snowflake SQL[¶](#id565)

```
SELECT ROUND(123.9994, 3) AS COL1,
ROUND(123.9995, 3) AS COL2;
```

**Result:**

```
COL1   | COL2  |
--------|------|
123.999|124.000|
```

### Related Documentation[¶](#id566)

- [SQL Server supported numeric types](https://docs.microsoft.com/en-us/sql/t-sql/data-types/numeric-types?view=sql-server-ver15)

## SQRT[¶](#sqrt)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id567)

Returns the square root of the specified float value.
([SQRT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/sqrt-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id568)

#### Syntax[¶](#id569)

##### SQL Server[¶](#id570)

```
SQRT ( float_expression )
```

##### Snowflake SQL[¶](#id571)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/sqrt.html)

```
SQRT(expr)
```

### Examples[¶](#id572)

#### SQL Server[¶](#id573)

```
SELECT SQRT(25) AS RESULT;
```

**Result:**

```
RESULT|
------|
   5.0|
```

##### Snowflake SQL[¶](#id574)

```
SELECT SQRT(25) AS RESULT;
```

**Result:**

```
RESULT|
------|
   5.0|
```

## SQUARE[¶](#square)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id575)

Returns the square of the specified float value.
([SQUARE in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/square-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id576)

#### Syntax[¶](#id577)

##### SQL Server[¶](#id578)

```
SQUARE ( float_expression )  ****
```

##### Snowflake SQL[¶](#id579)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/square.html)

```
SQUARE(expr)
```

### Examples[¶](#id580)

#### SQL Server[¶](#id581)

```
SELECT SQUARE (5) AS SQUARE;
```

**Result:**

```
SQUARE|
------|
  25.0|
```

##### Snowflake SQL[¶](#id582)

```
SELECT SQUARE (5) AS SQUARE;
```

**Result:**

```
SQUARE|
------|
    25|
```

## STDEV[¶](#stdev)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id583)

Returns the statistical standard deviation of all values in the specified expression.
([STDEV in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/degrees-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id584)

#### Syntax[¶](#id585)

##### SQL Server[¶](#id586)

```
 STDEV ( [ ALL | DISTINCT ] expression )
```

##### Snowflake SQL[¶](#id587)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/stddev.html)

```
 STDDEV( [ DISTINCT ] <expression_1> )
```

### Examples[¶](#id588)

#### SQL Server[¶](#id589)

```
SELECT
    STDEV(VACATIONHOURS)
FROM
    HUMANRESOURCES.EMPLOYEE AS STDEV;
```

**Result:**

```
           STDEV|
----------------|
28.7862150320948|
```

##### Snowflake SQL[¶](#id590)

```
SELECT
    STDDEV(VACATIONHOURS)
FROM
    HUMANRESOURCES.EMPLOYEE AS STDEV;
```

**Result:**

```
       STDEV|
------------|
28.786215034|
```

## STDEVP[¶](#stdevp)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id591)

Returns the statistical standard deviation for the population for all values in the specified
expression.
([STDVEP in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/degrees-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id592)

#### Syntax[¶](#id593)

##### SQL Server[¶](#id594)

```
STDEVP ( [ ALL | DISTINCT ] expression )
```

##### Snowflake SQL[¶](#id595)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/stddev_pop.html)

```
STDDEV_POP( [ DISTINCT ] expression_1)
```

### Examples[¶](#id596)

#### SQL Server[¶](#id597)

```
SELECT
    STDEVP(VACATIONHOURS) AS STDEVP_VACATIONHOURS
FROM
    HumanResources.Employee;
```

**Result:**

```
STDEVP_VACATIONHOURS|
--------------------|
  28.736540767245085|
```

##### Snowflake SQL[¶](#id598)

```
SELECT
    STDDEV_POP(VACATIONHOURS) AS STDEVP_VACATIONHOURS
FROM
    HumanResources.Employee;
```

**Result:**

```
STDEVP_VACATIONHOURS|
--------------------|
        28.736540763|
```

## VAR[¶](#var)

Applies to

- SQL Server
- Azure Synapse Analytics

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id599)

Returns the statistical variance of all values in the specified expression.
([VAR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/var-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id600)

#### Syntax[¶](#id601)

##### SQL Server[¶](#id602)

```
VAR ( [ ALL | DISTINCT ] expression )
```

##### Snowflake SQL[¶](#id603)

```
VAR_SAMP( [DISTINCT] <expr1> )
```

### Examples[¶](#id604)

#### SQL Server[¶](#id605)

```
SELECT
    VAR(VACATIONHOURS)
FROM
    HUMANRESOURCES.EMPLOYEE AS VAR;
```

**Result:**

```
             VAR|
----------------|
28.7862150320948|
```

##### Snowflake SQL[¶](#id606)

```
SELECT
    VAR_SAMP(VACATIONHOURS)
FROM
    HUMANRESOURCES.EMPLOYEE AS VAR;
```

**Result:**

```
       VAR|
----------|
828.646176|
```

## POWER[¶](#id607)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id608)

Returns the value of the specified expression for a specific power.
([POWER in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/power-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id609)

### Syntax[¶](#id610)

```
POWER( base, exp )
```

#### Arguments[¶](#id611)

`base`: Base of number, it must be a float expression. `exp`: Power to which raise the base.

#### Return Type[¶](#id612)

The return type depends on the input expression:

<!-- prettier-ignore -->
|Input Type|Return Type|
|---|---|
|float, real|float|
|decimal(p, s)|decimal(38, s)|
|int, smallint, tinyint|int|
|bigint|bigint|
|money, smallmoney|money|
|bit, char, nchar, varchar, nvarchar|float|

### Examples[¶](#id613)

### Query[¶](#id614)

```
SELECT POWER(2, 3)
```

#### Result[¶](#id615)

```
POWER(2, 3)|
-----------|
        8.0|
```

## POW in JS[¶](#pow-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id616)

Returns the base of the exponent power.
([JavaScript POW function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/pow)).

### Sample Source Pattern[¶](#id617)

#### Syntax[¶](#id618)

```
 Math.pow( base, exp )
```

##### Arguments[¶](#id619)

`base`: Base of number, it must be a float expression. `exp`: Power to which raise the base.

##### Return Type[¶](#id620)

Same data type sent through parameter as a numeric expression.

### Examples[¶](#id621)

#### Query[¶](#id622)

```
 CREATE OR REPLACE FUNCTION compute_pow(base float, exp float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
    return Math.pow(BASE, EXP);
$$
;
SELECT COMPUTE_POW(2, 3);
```

##### Result[¶](#id623)

```
COMPUTE_POW(2, 3)|
-----------------|
                8|
```

## ACOS[¶](#acos)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id624)

Function that returns the arccosine in radians of the number sent as a parameter
([ACOS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/acos-transact-sql?view=sql-server-ver15)).

Mathematically, the arccosine is the inverse function of the cosine, resulting in the following
definition: $$y = cos^{-1} \Leftrightarrow x = cos(y)$$

For $$y = cos^{-1}(x)$$:

- Range: $$0\leqslant y \leqslant \pi$$ or $$0^{\circ}\leqslant y \leqslant 180^{\circ}$$
- Domain: $$-1\leqslant x \leqslant 1$$

### Sample Source Pattern[¶](#id625)

### Syntax[¶](#id626)

```
ACOS ( expression )
```

#### Arguments[¶](#id627)

`expression`: Numeric **float** expression, where expression is in$$[-1,1]$$.

#### Return Type[¶](#id628)

Numeric float expression between 0 and π. If the numeric expression sent by parameter is out of the
domain $$[-1, 1]$$, the database engine throws an error.

### Examples[¶](#id629)

### Query[¶](#id630)

```
SELECT ACOS(-1.0);
```

#### Result[¶](#id631)

```
ACOS(-1.0)       |
-----------------|
3.141592653589793|
```

## ACOS in JS[¶](#acos-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id632)

Function that returns the arccosine of a specified number
([JavaScript ACOS function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/acos)).

### Sample Source Pattern[¶](#id633)

#### Syntax[¶](#id634)

```
 Math.acos( expression )
```

##### Arguments[¶](#id635)

`expression`: Numeric expression, where expression is in$$[-1,1]$$.

##### Return Type[¶](#id636)

Numeric expression between 0 and π. If the numeric expression sent by parameter is out of the range
of the arccosine in radians $$[-1, 1]$$, the function returns NaN.

### Examples[¶](#id637)

#### Query[¶](#id638)

```
 CREATE OR REPLACE FUNCTION compute_acos(a double)
  RETURNS double
  LANGUAGE JAVASCRIPT
AS
$$
  return Math.acos(A);
$$
;
SELECT COMPUTE_ACOS(-1);
```

##### Result[¶](#id639)

```
COMPUTE_ACOS(-1)|
---------------|
    3.141592654|
```

## ASIN[¶](#asin)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id640)

Function that returns the arcsine in radians of the number sent as parameter
([ASIN in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/asin-transact-sql?view=sql-server-ver15)).

The arcsine is the inverse function of the sine , summarized in the next definition:
$$y = sin^{-1} \Leftrightarrow x = sin(x)$$

For $$y = sin^{-1}(x)$$:

- Range: $$-\frac{\pi}{2}\leqslant y \leqslant \frac{\pi}{2}$$ or
  $$-90^{\circ}\leqslant y \leqslant 90^{\circ}$$
- Domain: $$-1\leqslant x \leqslant 1$$

### Sample Source Pattern[¶](#id641)

### Syntax[¶](#id642)

```
ASIN( expression )
```

#### Arguments[¶](#id643)

`expression`: Numeric **float** expression, where expression is in$$[-1,1]$$.

#### Return Type[¶](#id644)

Numeric float expression between $$-\frac{\pi}{2}$$ and $$\frac{\pi}{2}$$. If the numeric expression
sent by parameter is not in $$[-1, 1]$$, the database engine throws an error.

### Examples[¶](#id645)

### Query[¶](#id646)

```
SELECT ASIN(0.5);
```

#### Result[¶](#id647)

```
ASIN(0.5)         |
------------------|
0.5235987755982989|
```

## ASIN in JS[¶](#asin-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id648)

Function that returns the arcsine of a specified number
([JavaScript ASIN function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/asin)).

### Sample Source Pattern[¶](#id649)

#### Syntax[¶](#id650)

```
 Math.asin( expression )
```

##### Arguments[¶](#id651)

`expression`: Numeric expression, where expression is in$$[-1,1]$$.

##### Return Type[¶](#id652)

Numeric expression between $$-\frac{\pi}{2}$$ and $$\frac{\pi}{2}$$. If the numeric expression sent
by parameter is out of the domain of the arccosine $$[-1, 1]$$, the function returns NaN.

### Examples[¶](#id653)

#### Query[¶](#id654)

```
 CREATE OR REPLACE FUNCTION compute_asin(a float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  return Math.asin(A);
$$
;
SELECT COMPUTE_ASIN(0.5);
```

##### Result[¶](#id655)

```
COMPUTE_ASIN(1)   |
------------------|
      0.5235987756|
```

## COS[¶](#cos)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id656)

Function that returns the cosine of the angle sent through parameters (must be measured in radians)
([COS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/cos-transact-sql?view=sql-server-ver15)).

The cosine is defined as: $$y = cos(x)$$ Where:

- Range: $$-1\leqslant y \leqslant 1$$
- Domain: $$\mathbb{R}$$

### Sample Source Pattern[¶](#id657)

### Syntax[¶](#id658)

```
COS( expression )
```

#### Arguments[¶](#id659)

`expression`: Numeric **float** expression, where expression is in $$\mathbb{R}$$.

#### Return Type[¶](#id660)

Numeric float expression in $$[-1, 1]$$.

### Examples[¶](#id661)

### Query[¶](#id662)

```
SELECT COS(PI())
```

#### Result[¶](#id663)

```
COS(PI())|
---------|
     -1.0|
```

## COS in JS[¶](#cos-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id664)

Static function that returns the cosine of an angle in radians
([JavaScript COS function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/cos)).

### Sample Source Pattern[¶](#id665)

#### Syntax[¶](#id666)

```
 Math.cos( expression )
```

##### Arguments[¶](#id667)

`expression:` Numeric expressions.

##### Return Type[¶](#id668)

Same data type sent through parameter as a numeric expression.

### Examples[¶](#id669)

#### Query[¶](#id670)

```
CREATE OR REPLACE FUNCTION compute_cos(angle float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return Math.cos(ANGLE);
$$
;
SELECT COMPUTE_COS(PI());
```

##### Result[¶](#id671)

```
COMPUTE_COS(PI())|
-----------------|
               -1|
```

## COT[¶](#cot)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id672)

Returns the cotangent of the angle in radians sent through parameters
([COT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/cot-transact-sql?view=sql-server-ver15)).

The cosine is defined as: $$cot(x) = \frac{cos(x)}{sin(x)}$$ or $$cot(x) = \frac{1}{tan(x)}$$ To
calculate the cosine, the parameter must comply with the constraints of sine and [cosine](#cos)
functions.

### Sample Source Pattern[¶](#id673)

### Syntax[¶](#id674)

```
COT( expression )
```

#### Arguments[¶](#id675)

`expression`: Numeric **float** expression, where expression is in
$$\mathbb{R}-{sin(expression)=0 \wedge tan(expression) =0}$$.

#### Return Type[¶](#id676)

Numeric float expression in $$\mathbb{R}$$.

### Examples[¶](#id677)

### Query[¶](#id678)

```
SELECT COT(1)
```

#### Result[¶](#id679)

```
COT(1)            |
------------------|
0.6420926159343306|
```

## COT in JS[¶](#cot-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id680)

Unfortunately, the object `Math`in JavaScript does not provide a method to calculate the cotangent
of a given angle. This could be calculated using the equation: $$cot(x) = \frac{cos(x)}{sin(x)}$$

### Sample Source Pattern[¶](#id681)

#### Implementation example[¶](#id682)

```
 function cot(angle){
    return Math.cos(angle)/Math.sin(angle);
}
```

##### Arguments[¶](#id683)

`angle:` Numeric expression in radians.

##### Return Type[¶](#id684)

Same data type sent through parameter as a numeric expression.

### Examples[¶](#id685)

#### Query[¶](#id686)

```
CREATE OR REPLACE FUNCTION compute_cot(angle float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  function cot(angle){
    return Math.cos(angle)/Math.sin(angle);
  }
  return cot(ANGLE);

$$
;
SELECT COMPUTE_COT(1);
```

##### Result[¶](#id687)

```
COMPUTE_COT(1);   |
------------------|
0.6420926159343308|
```

## RADIANS[¶](#radians)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id688)

Converts degrees to radians.
([RADIANS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/radians-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id689)

### Syntax[¶](#id690)

```
RADIANS( expression )
```

#### Arguments[¶](#id691)

`expression`: Numeric expression in degrees.

#### Return Type[¶](#id692)

Same data type sent through parameter as a numeric expression in radians.

### Examples[¶](#id693)

### Query[¶](#id694)

```
SELECT RADIANS(180.0)
```

#### Result[¶](#id695)

<!-- prettier-ignore -->
|RADIANS(180)|
|---|
|3.141592653589793116|

**Note:**

Cast the parameter of this function to float, otherwise, the above statement will return 3 instead
of PI value.

## RADIANS in JS[¶](#radians-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id696)

JavaScript does not provide a method to convert degrees to radians of a given angle. This could be
calculated using the equation: $$Radians = \frac{\pi}{180^{\circ}} \cdot angle$$

### Sample Source Pattern[¶](#id697)

#### Implementation example[¶](#id698)

```
 function radians(angle){
    return (Math.PI/180) * angle;
}
```

##### Arguments[¶](#id699)

`angle`: Float expression in degrees.

##### Return Type[¶](#id700)

Same data type sent through parameter as a numeric expression in radians.

### Examples[¶](#id701)

#### Query[¶](#id702)

```
CREATE OR REPLACE FUNCTION RADIANS(angle float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
    function radians(angle){
      return (Math.PI/180) * angle;
    }
    return radians(ANGLE);
$$
;
SELECT RADIANS(180);
```

##### Result[¶](#id703)

<!-- prettier-ignore -->
|RADIANS(180)|
|---|
|3.141592654|

## PI[¶](#pi)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id704)

Returns the constant value of PI
([PI in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/pi-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id705)

### Syntax[¶](#id706)

```
PI( )
```

#### Arguments[¶](#id707)

This method does not receive any parameters.

#### Return Type[¶](#id708)

Float.

### Examples[¶](#id709)

### Query[¶](#id710)

```
CREATE PROCEDURE CIRCUMFERENCE @radius float
AS
    SELECT 2 * PI() * @radius;
GO:

EXEC CIRCUMFERENCE @radius = 2;
```

#### Result[¶](#id711)

```
CIRCUMFERENCE @radius = 2 |
--------------------------|
          12.5663706143592|
```

## PI in JS[¶](#pi-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id712)

Constant which represents the PI number (approximately 3.141592…)
([JavaScript PI Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/PI)).

### Sample Source Pattern[¶](#id713)

#### Syntax[¶](#id714)

```
 Math.PI
```

### Examples[¶](#id715)

#### Query[¶](#id716)

```
CREATE OR REPLACE FUNCTION circumference(radius float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  function circumference(r){
    return 2 * Math.PI * r;
  }
  return circumference(RADIUS);
$$
;
SELECT CIRCUMFERENCE(2);
```

##### Result[¶](#id717)

```
  CIRCUMFERENCE(2)|
------------------|
12.566370614359172|
```

## DEGREES[¶](#degrees)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id718)

Converts the angle in radians sent through parameters to degrees
([DEGREES in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/degrees-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id719)

### Syntax[¶](#id720)

```
DEGREES( expression )
```

#### Arguments[¶](#id721)

`expression`: Numeric **float** expression in radians.

#### Return Type[¶](#id722)

Same data type sent through parameter as a numeric expression.

### Examples[¶](#id723)

### Query[¶](#id724)

```
SELECT DEGREES(PI())
```

#### Result[¶](#id725)

```
DEGREES(PI())|
-------------|
        180.0|
```

## DEGREES in JS[¶](#degrees-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id726)

JavaScript does not provide a method to convert radians to degrees of a given angle. This could be
calculated using the equation: $$Degrees = \frac{180^{\circ}}{\pi} \cdot angle$$

### Sample Source Pattern[¶](#id727)

#### Implementation example[¶](#id728)

```
 function degress(angle){
    return (180/Math.PI) * angle;
}
```

##### Arguments[¶](#id729)

`angle`: Numeric expression in radians.

##### Return Type[¶](#id730)

Same data type sent through parameter as a numeric expression.

### Examples[¶](#id731)

#### Query[¶](#id732)

```
CREATE OR REPLACE FUNCTION compute_degrees(angle float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  function degrees(angle){
    return (180/Math.PI) * angle;
  }
  return degrees(ANGLE);

$$
;
SELECT COMPUTE_DEGREES(PI());
```

##### Result[¶](#id733)

```
COMPUTE_DEGREES(PI())|
---------------------|
                180.0|
```

## LOG[¶](#log)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id734)

Returns the natural logarithm of a number
([LOG in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/log-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id735)

### Syntax[¶](#id736)

```
LOG( expression [, base ] )
```

#### Arguments[¶](#id737)

`expression`: Numeric expression.

`base` (optional): Base to calculate the logarithm of a number, it is Euler by default.

#### Return Type[¶](#id738)

Float.

### Examples[¶](#id739)

### Query[¶](#id740)

```
SELECT LOG(8, 2)
```

#### Result[¶](#id741)

```
LOG(8, 2)  |
-----------|
          3|
```

## LOG in JS[¶](#log-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id742)

Returns the logarithm using the Euler’s number as a base.
([JavaScript LOG function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/log)).

Warning

Unfortunately, JavaScript does not provide a method that receives a logarithm base through its
parameters, but this can be solved by dividing the base by the argument.

### Sample Source Pattern[¶](#id743)

#### Syntax[¶](#id744)

```
 Math.log( expression )
```

##### Arguments[¶](#id745)

`expression`: Numeric expression. It must be positive, otherwise returns NaN.\

##### Return Type[¶](#id746)

Same data type sent through parameter as a numeric expression.

### Examples[¶](#id747)

#### Query[¶](#id748)

```
 CREATE OR REPLACE FUNCTION base_log(base float, exp float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  function getBaseLog(x, y){
    return Math.log(y)/Math.log(x);
  }
  return getBaseLog(EXP, BASE)
$$
;
SELECT BASE_LOG(2, 8);
```

##### Result[¶](#id749)

```
BASE_LOG(2, 8)|
--------------|
             3|
```

## ATAN[¶](#atan)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id750)

Function that returns the arctangent in radians of the number sent as a parameter
([ATAN in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/atan-transact-sql?view=sql-server-ver15)).

The arctangent is the inverse function of the tangent, summarized in the next definition:
$$y = arctan^{-1} \Leftrightarrow x = tan(x)$$

For $$y = tan^{-1}(x)$$:

- Range: $$-\frac{\pi}{2}\leqslant y \leqslant \frac{\pi}{2}$$ or
  $$-90^{\circ}\leqslant y \leqslant 90^{\circ}$$
- Domain: $$\mathbb{R}$$

### Sample Source Pattern[¶](#id751)

### Syntax[¶](#id752)

```
ATAN( expression )
```

#### Arguments[¶](#id753)

`expression`: Numeric **float** expression, or a numeric type which could be converted to float.

#### Return Type[¶](#id754)

Numeric float expression between $$-\frac{\pi}{2}$$ and $$\frac{\pi}{2}$$.

### Examples[¶](#id755)

### Query[¶](#id756)

```
SELECT ATAN(-30);
```

#### Result[¶](#id757)

```
ATAN(-30)          |
-------------------|
-1.5374753309166493|
```

## ATAN in JS[¶](#atan-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id758)

Function that returns the arctangent of a specified number
([JavaScript ATAN function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/atan)).

### Sample Source Pattern[¶](#id759)

#### Syntax[¶](#id760)

```
 Math.atan( expression )
```

##### Arguments[¶](#id761)

`expression`: Numeric expression.

##### Return Type[¶](#id762)

Numeric expression between $$-\frac{\pi}{2}$$ and $$\frac{\pi}{2}$$.

### Examples[¶](#id763)

#### Query[¶](#id764)

```
 CREATE OR REPLACE FUNCTION compute_atan(a float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
  return Math.atan(A);
$$
;
SELECT COMPUTE_ATAN(-30);
```

##### Result[¶](#id765)

```
COMPUTE_ATAN(-30)|
-----------------|
     -1.537475331|
```

## ATN2[¶](#atn2)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id766)

Function that returns the arctangent in radians of two coordinates sent as a parameter
([ATN2 in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/atn2-transact-sql?view=sql-server-ver15)).

For $$z = tan^{-1}(x, y)$$:

- Range: $$-\pi\leqslant z \leqslant \pi$$ or $$-180^{\circ}\leqslant z \leqslant 180^{\circ}$$
- Domain: $$\mathbb{R}$$

### Sample Source Pattern[¶](#id767)

### Syntax[¶](#id768)

```
ATN2( expression_1, expression_2 )
```

#### Arguments[¶](#id769)

`expression1`and `expression2`: Numeric expressions.

#### Return Type[¶](#id770)

Numeric expression between $$-\pi$$ and $$\pi$$.

### Examples[¶](#id771)

### Query[¶](#id772)

```
SELECT ATN2(7.5, 2);
```

#### Result[¶](#id773)

```
ATN2(7.5, 2)      |
------------------|
1.3101939350475555|
```

## ATAN2 in JS[¶](#atan2-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id774)

Function that returns the arctangent of two parameters
([JavaScript ATAN2 function Documentation](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Math/atan2)).

### Sample Source Pattern[¶](#id775)

#### Syntax[¶](#id776)

```
 Math.atan2( expression_1, expression_2 )
```

##### Arguments[¶](#id777)

`expression_1`and `expression_2`: Numeric expressions.

##### Return Type[¶](#id778)

Numeric expression between $$-\pi$$ and $$\pi$$.

### Examples[¶](#id779)

#### Query[¶](#id780)

```
CREATE OR REPLACE FUNCTION compute_atan2(x float, y float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return Math.atan2(X, Y);
$$
;
SELECT COMPUTE_ATAN2(7.5, 2);
```

##### Result[¶](#id781)

```
ATAN2(7.5, 3)     |
------------------|
       1.310193935|
```

## LOG10[¶](#log10)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id782)

Returns the base 10 logarithm of a number
([LOG10 in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/log10-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id783)

### Syntax[¶](#id784)

```
LOG10( expression )
```

#### Arguments[¶](#id785)

`expression`: Numeric expression, must be positive.

#### Return Type[¶](#id786)

Float.

### Examples[¶](#id787)

### Query[¶](#id788)

```
SELECT LOG10(5)
```

#### Result[¶](#id789)

```
LOG10(5)         |
-----------------|
0.698970004336019|
```

## LOG10 in JS[¶](#log10-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id790)

Returns the base 10 logarithm of a number
([JavaScript LOG10 function Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/log10)).

### Sample Source Pattern[¶](#id791)

#### Syntax[¶](#id792)

```
 Math.log10( expression )
```

##### Arguments[¶](#id793)

`expression`: Numeric expression. It must be positive, otherwise returns NaN.\

##### Return Type[¶](#id794)

Same data type sent through parameter as a numeric expression.

### Examples[¶](#id795)

#### Query[¶](#id796)

```
 CREATE OR REPLACE FUNCTION compute_log10(argument float)
  RETURNS float
  LANGUAGE JAVASCRIPT
AS
$$
    return Math.log10(ARGUMENT);
$$
;
SELECT COMPUTE_LOG10(7.5);
```

##### Result[¶](#id797)

```
COMPUTE_LOG10(5)|
----------------|
    0.6989700043|
```

## EXP[¶](#exp)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id798)

Returns the exponential value of Euler
([EXP in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/exp-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id799)

### Syntax[¶](#id800)

```
EXP( expression )
```

#### Arguments[¶](#id801)

`expression`: Numeric expression.

#### Return Type[¶](#id802)

Same data type sent through parameter as a numeric expression.

### Examples[¶](#id803)

### Query[¶](#id804)

```
SELECT EXP(LOG(20)), LOG(EXP(20))
GO
```

#### Result[¶](#id805)

```
EXP(LOG(20))   |LOG(EXP(20))    |
---------------|----------------|
           20.0|            20.0|
```

## EXP in JS[¶](#exp-in-js)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id806)

Constant which represents Euler’s number (approximately 2.718…)
([JavaScript Euler’s Number Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/E)).
JavaScript allows make different operations using this constant, instead of Transact-SQL which only
supports the exponential of Euler.

### Sample Source Pattern[¶](#id807)

#### Syntax[¶](#id808)

```
 Math.E
```

### Examples[¶](#id809)

#### Query[¶](#id810)

```
CREATE OR REPLACE FUNCTION compute_exp(x float)
RETURNS float
LANGUAGE JAVASCRIPT
AS
$$
  return Math.E**X;
$$
;
SELECT COMPUTE_EXP(LN(20)), LN(COMPUTE_EXP(20));
```

##### Result[¶](#id811)

```
COMPUTE_EXP(LOG(20))|LOG(COMPUTE_EXP(20))|
--------------------|--------------------|
                20.0|                20.0|
```

## Conversion functions[¶](#conversion-functions)

This section describes the functional equivalents of date & time functions in Transact-SQL to
Snowflake SQL code.

## CONVERT[¶](#convert)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id812)

Convert an expression of one data type to another.
([CONVERT in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id813)

#### Syntax[¶](#id814)

##### SQL Server[¶](#id815)

```
CONVERT ( data_type [ ( length ) ] , expression [ , style ] )
```

##### Snowflake SQL[¶](#id816)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/cast.html)

```
CAST( <source_expr> AS <target_data_type> )
```

### Examples[¶](#id817)

#### SQL Server[¶](#id818)

```
SELECT CONVERT(INT, '1998') as MyDate
```

##### Result[¶](#id819)

<!-- prettier-ignore -->
|MyDate|
|---|
|1998|

##### Snowflake SQL[¶](#id820)

```
SELECT
CAST('1998' AS INT) as MyDate;
```

##### Result[¶](#id821)

<!-- prettier-ignore -->
|MYDATE|
|---|
|1998|

##### Casting date type to varchar[¶](#casting-date-type-to-varchar)

##### SQL Server[¶](#id822)

```
SELECT CONVERT(varchar, getdate(), 1) AS RESULT;
```

##### Result[¶](#id823)

<!-- prettier-ignore -->
|RESULT|
|---|
|12/08/22|

##### Swowflake SQL[¶](#swowflake-sql)

```
SELECT
TO_VARCHAR(CURRENT_TIMESTAMP() :: TIMESTAMP, 'mm/dd/yy') AS RESULT;
```

##### Result[¶](#id824)

<!-- prettier-ignore -->
|RESULT|
|---|
|12/08/22|

##### Casting date type to varchar with size[¶](#casting-date-type-to-varchar-with-size)

##### SQL Server[¶](#id825)

```
SELECT CONVERT(varchar(2), getdate(), 1) AS RESULT;
```

##### Result[¶](#id826)

<!-- prettier-ignore -->
|RESULT|
|---|
|07|

##### Snowflake SQL[¶](#id827)

```
SELECT
LEFT(TO_VARCHAR(CURRENT_TIMESTAMP() :: TIMESTAMP, 'mm/dd/yy'), 2) AS RESULT;
```

##### Result[¶](#id828)

<!-- prettier-ignore -->
|RESULT|
|---|
|07|

The supported formats for dates casts are:

**Date formats**

<!-- prettier-ignore -->
|Code|Format|
|---|---|
|1|mm/dd/yy|
|2|yy.mm.dd|
|3|dd/mm/yy|
|4|dd.mm.yy|
|5|dd-mm-yy|
|6|dd-Mon-yy|
|7|Mon dd, yy|
|10|mm-dd-yy|
|11|yy/mm/dd|
|12|yymmdd|
|23|yyyy-mm-dd|
|101|mm/dd/yyyy|
|102|yyyy.mm.dd|
|103|dd/mm/yyyy|
|104|dd.mm.yyyy|
|105|dd-mm-yyyy|
|106|dd Mon yyyy|
|107|Mon dd, yyyy|
|110|mm-dd-yyyy|
|111|yyyy/mm/dd|
|112|yyyymmdd|

**Time formats**

<!-- prettier-ignore -->
|Code|Format|
|---|---|
|8|hh:mm:ss|
|14|hh:mm:ss:ff3|
|24|hh:mm:ss|
|108|hh:mm:ss|
|114|hh:mm:ss:ff3|

**Date and time formats**

<!-- prettier-ignore -->
|     |                                |
|---|---|
|0|Mon dd yyyy hh:mm AM/PM|
|9|Mon dd yyyy hh:mm:ss:ff3 AM/PM|
|13|dd Mon yyyy hh:mm:ss:ff3 AM/PM|
|20|yyyy-mm-dd hh:mm:ss|
|21|yyyy-mm-dd hh:mm:ss:ff3|
|22|mm/dd/yy hh:mm:ss AM/PM|
|25|yyyy-mm-dd hh:mm:ss:ff3|
|100|Mon dd yyyy hh:mm AM/PM|
|109|Mon dd yyyy hh:mm:ss:ff3 AM/PM|
|113|dd Mon yyyy hh:mm:ss:ff3|
|120|yyyy-mm-dd hh:mm:ss|
|121|yyyy-mm-dd hh:mm:ss:ff3|
|126|yyyy-mm-dd T hh:mm:ss:ff3|
|127|yyyy-mm-dd T hh:mm:ss:ff3|

**Islamic calendar dates**

<!-- prettier-ignore -->
|Code|Format|
|---|---|
|130|dd mmm yyyy hh:mi:ss:ff3 AM/PM|
|131|dd mmm yyyy hh:mi:ss:ff3 AM/PM|

If there is no pattern matching with the current code, it will be formatted to `yyyy-mm-dd hh:mm:ss`

## TRY_CONVERT[¶](#try-convert)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id829)

Returns a value cast to the specified data type if the cast succeeds; otherwise, returns null.

([SQL Server Language Reference TRY_CONVERT](https://docs.microsoft.com/en-us/sql/t-sql/functions/try-convert-transact-sql?view=sql-server-ver15))

#### Syntax[¶](#id830)

```
TRY_CONVERT ( data_type [ ( length ) ], expression [, style ] )
```

### Source Patterns[¶](#source-patterns)

#### Basic Transformation[¶](#basic-transformation)

In order to transform this function, we have to check the parameters of the TRY_CONVERT first.

```
TRY_CONVERT( INT, 'test')
```

If the expression that needs to be casted is a string, it will be transfomed to TRY_CAST, which is a
function of Snowflake.

```
TRY_CAST( 'test' AS INT)
```

#### TRY_CAST[¶](#try-cast)

The TRY_CAST shares the same transformation with TRY_CONVERT.

##### Example[¶](#example)

##### Sql Server[¶](#id831)

```
SELECT TRY_CAST('12345' AS NUMERIC) NUMERIC_RESULT,
 TRY_CAST('123.45' AS DECIMAL(20,2)) DECIMAL_RESULT,
 TRY_CAST('123' AS INT) INT_RESULT,
 TRY_CAST('123.02' AS FLOAT) FLOAT_RESULT,
 TRY_CAST('123.02' AS DOUBLE PRECISION) DOUBLE_PRECISION_RESULT,

 TRY_CAST('2017-01-01 12:00:00' AS DATE) DATE_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS DATETIME) DATETIME_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS SMALLDATETIME) SMALLDATETIME_RESULT,
 TRY_CAST('12:00:00' AS TIME) TIME_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS TIMESTAMP) TIMESTAMP_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS DATETIMEOFFSET) DATETIMEOFFSET_RESULT,

 TRY_CAST(1234 AS VARCHAR) VARCHAR_RESULT,
 TRY_CAST(1 AS CHAR) CHAR_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS SQL_VARIANT) SQL_VARIANT_RESULT,
 TRY_CAST('LINESTRING(-122.360 47.656, -122.343 47.656 )' AS GEOGRAPHY) GEOGRAPHY_RESULT;
```

The result will be the same with the example of TRY_CONVERT.

##### Snowflake[¶](#id832)

```
SELECT
 TRY_CAST('12345' AS NUMERIC(38, 18)) NUMERIC_RESULT,
 TRY_CAST('123.45' AS DECIMAL(20,2)) DECIMAL_RESULT,
 TRY_CAST('123' AS INT) INT_RESULT,
 TRY_CAST('123.02' AS FLOAT) FLOAT_RESULT,
 TRY_CAST('123.02' AS DOUBLE PRECISION) DOUBLE_PRECISION_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS DATE) DATE_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS TIMESTAMP_NTZ(3)) DATETIME_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS TIMESTAMP_NTZ(0)) SMALLDATETIME_RESULT,
 TRY_CAST('12:00:00' AS TIME(7)) TIME_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS BINARY(8)) TIMESTAMP_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS TIMESTAMP_TZ(7)) DATETIMEOFFSET_RESULT,
 TO_VARCHAR(1234) VARCHAR_RESULT,
 TO_CHAR(1) CHAR_RESULT,
 TRY_CAST('2017-01-01 12:00:00' AS VARIANT) SQL_VARIANT_RESULT,
 TRY_CAST('LINESTRING(-122.360 47.656, -122.343 47.656 )' AS GEOGRAPHY) GEOGRAPHY_RESULT;
```

### Known Issues[¶](#id833)

If the data type is Varchar or Char, then it will be transformed differently.

```
TRY_CONVERT(VARCHAR, 1234);
TRY_CONVERT(CHAR, 1);
```

If TRY_CAST is used with VARCHAR or CHAR in Snowflake, it will cause an error, so it will be
transformed to

```
TO_VARCHAR(1234);
TO_CHAR(1);
```

The same happens with the data types of SQL_VARIANT and GEOGRAPHY.

```
TRY_CONVERT(SQL_VARIANT, '2017-01-01 12:00:00');
TRY_CONVERT(GEOGRAPHY, 'LINESTRING(-122.360 47.656, -122.343 47.656 )');
```

Are transformed to

```
TO_VARIANT('2017-01-01 12:00:00');
TO_GEOGRAPHY('LINESTRING(-122.360 47.656, -122.343 47.656 )');
```

If the expression is not a string, there is a very high chance that it will fail, since the TRY_CAST
of snowflake works only with string expressions.

In this case, another transformation will be done

```
TRY_CAST(14.85 AS INT)
```

Will be transformed to

```
CAST(14.85 AS INT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/
```

Now, with these transformation, there could be problems depending on what is being done with the
functions. The TRY_CONVERT of SqlServer returns nulls if the convertion was not possible.

This can be used to do logic like this

```
SELECT
    CASE
        WHEN TRY_CONVERT( INT, 'Expression') IS NULL
        THEN 'FAILED'
        ELSE 'SUCCEDDED'
    END;
```

That type of conditions with the TRY_CONVERT can be used with the TRY_CAST, but what happens if it
is transformed to TO_VARCHAR, TOCHAR or to the CAST? If the convertion in those functions fails, it
will cause an error instead of just returning null.

#### Examples[¶](#id834)

In this sample we have several TRY_CONVERT with different data types

##### SQL Server[¶](#id835)

```
SELECT TRY_CONVERT(NUMERIC, '12345') NUMERIC_RESULT,
 TRY_CONVERT(DECIMAL(20,2), '123.45') DECIMAL_RESULT,
 TRY_CONVERT(INT, '123') INT_RESULT,
 TRY_CONVERT(FLOAT, '123.02') FLOAT_RESULT,
 TRY_CONVERT(DOUBLE PRECISION, '123.02') DOUBLE_PRECISION_RESULT,

 TRY_CONVERT(DATE, '2017-01-01 12:00:00') DATE_RESULT,
 TRY_CONVERT(DATETIME, '2017-01-01 12:00:00') DATETIME_RESULT,
 TRY_CONVERT(SMALLDATETIME, '2017-01-01 12:00:00') SMALLDATETIME_RESULT,
 TRY_CONVERT(TIME, '12:00:00') TIME_RESULT,
 TRY_CONVERT(TIMESTAMP, '2017-01-01 12:00:00') TIMESTAMP_RESULT,
 TRY_CONVERT(DATETIMEOFFSET, '2017-01-01 12:00:00') DATETIMEOFFSET_RESULT,

 TRY_CONVERT(VARCHAR, 1234) VARCHAR_RESULT,
 TRY_CONVERT(CHAR, 1) CHAR_RESULT,
 TRY_CONVERT(SQL_VARIANT, '2017-01-01 12:00:00') SQL_VARIANT_RESULT,
 TRY_CONVERT(GEOGRAPHY, 'LINESTRING(-122.360 47.656, -122.343 47.656 )') GEOGRAPHY_RESULT;
```

If we migrate that select, we will get the following result

##### Snowflake[¶](#id836)

```
SELECT
 CAST('12345' AS NUMERIC(38, 18)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ NUMERIC_RESULT,
 CAST('123.45' AS DECIMAL(20,2)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DECIMAL_RESULT,
 CAST('123' AS INT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ INT_RESULT,
 CAST('123.02' AS FLOAT) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ FLOAT_RESULT,
 CAST('123.02' AS DOUBLE PRECISION) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DOUBLE_PRECISION_RESULT,
 CAST('2017-01-01 12:00:00' AS DATE) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DATE_RESULT,
 CAST('2017-01-01 12:00:00' AS TIMESTAMP_NTZ(3)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DATETIME_RESULT,
 CAST('2017-01-01 12:00:00' AS TIMESTAMP_NTZ(0)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ SMALLDATETIME_RESULT,
 CAST('12:00:00' AS TIME(7)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ TIME_RESULT,
 CAST('2017-01-01 12:00:00' AS BINARY(8)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ TIMESTAMP_RESULT,
 CAST('2017-01-01 12:00:00' AS TIMESTAMP_TZ(7)) /*** SSC-FDM-TS0005 - TRY_CONVERT/TRY_CAST COULD NOT BE CONVERTED TO TRY_CAST ***/ DATETIMEOFFSET_RESULT,
 TO_VARCHAR(1234) VARCHAR_RESULT,
 TO_CHAR(1) CHAR_RESULT,
 TO_VARIANT('2017-01-01 12:00:00') SQL_VARIANT_RESULT,
 TO_GEOGRAPHY('LINESTRING(-122.360 47.656, -122.343 47.656 )') GEOGRAPHY_RESULT;
```

Let’s execute each one and compare the result.

<!-- prettier-ignore -->
|Alias|SqlServer Result|Snowflake Result|
|---|---|---|
|NUMERIC_RESULT|12345|12345|
|DECIMAL_RESULT|123.45|123.45|
|INT_RESULT|123|123|
|FLOAT_RESULT|123.02|123.02|
|DOUBLE_PRECISION_RESULT|123.02|123.02|
|DATE_RESULT|2017-01-01|2017-01-01|
|DATETIME_RESULT|2017-01-01 12:00:00.000|2017-01-01 12:00:00.000|
|SMALLDATETIME_RESULT|2017-01-01 12:00:00|2017-01-01 12:00:00.000|
|TIME_RESULT|12:00:00.0000000|12:00:00|
|TIMESTAMP_RESULT|0x323031372D30312D|2017-01-01 12:00:00.000|
|DATETIMEOFFSET_RESULT|2017-01-01 12:00:00.0000000 +00:00|2017-01-01 12:00:00.000 -0800|
|VARCHAR_RESULT|1234|1234|
|CHAR_RESULT|1|1|
|SQL_VARIANT_RESULT|2017-01-01 12:00:00|“2017-01-01 12:00:00”|
|GEOGRAPHY_RESULT|0xE610000001148716D9CEF7D34740D7A3703D0A975EC08716D9CEF7D34740CBA145B6F3955EC0|{ “coordinates”: [ [ -122.36, 47.656 ], [ -122.343, 47.656 ] ], “type”: “LineString” }|

### Related EWIs[¶](#id837)

1. [SSC-FDM-TS0005](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0005):
   TRY_CONVERT/TRY_CAST could not be converted to TRY_CAST.

## Date & Time functions[¶](#date-time-functions)

This section describes the functional equivalents of date & time functions in Transact-SQL to
Snowflake SQL and JavaScript code.

## AT TIME ZONE[¶](#at-time-zone)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id838)

Converts an _inputdate_ to the corresponding _datetimeoffset_ value in the target time zone.
([AT TIME ZONE in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern[¶](#id839)

#### Syntax[¶](#id840)

##### SQL Server[¶](#id841)

```
inputdate AT TIME ZONE timezone
```

##### Snowflake SQL[¶](#id842)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone.html)

```
CONVERT_TIMEZONE( <source_tz> , <target_tz> , <source_timestamp_ntz> )

CONVERT_TIMEZONE( <target_tz> , <source_timestamp> )
```

### Examples[¶](#id843)

#### SQL Server[¶](#id844)

```
SELECT CAST('2022-11-24 11:00:45.2000000 +00:00' as datetimeoffset) at time zone 'Alaskan Standard Time';
```

**Result:**

```
                          DATE|
------------------------------|
2022-11-24 02:00:45.200 -09:00|
```

##### Snowflake SQL[¶](#id845)

```
SELECT
CONVERT_TIMEZONE('America/Anchorage', CAST('2022-11-24 11:00:45.2000000 +00:00' as TIMESTAMP_TZ(7)));
```

**Result:**

```
                          DATE|
------------------------------|
2022-11-24 02:00:45.200 -09:00|
```

##### SQL Server[¶](#id846)

```
SELECT current_timestamp at time zone 'Central America Standard Time';
```

**Result:**

```
                          DATE|
------------------------------|
2022-10-10 10:55:50.090 -06:00|
```

##### Snowflake SQL[¶](#id847)

```
SELECT
CONVERT_TIMEZONE('America/Costa_Rica', CURRENT_TIMESTAMP() /*** SSC-FDM-TS0024 - CURRENT_TIMESTAMP in At Time Zone statement may have a different behavior in certain cases ***/);
```

**Result:**

```
                          DATE|
------------------------------|
2022-10-10 10:55:50.090 -06:00|
```

### Known Issues[¶](#id848)

1. Snowflake does not support all the time zones that SQL Server does. You can check the supported
   time zones at this
   [link](https://docs.snowflake.com/en/sql-reference/functions/convert_timezone.html).

#### SQL Server[¶](#id849)

```
SELECT current_timestamp at time zone 'Turks And Caicos Standard Time';
```

**Result:**

```
                          DATE|
------------------------------|
2022-12-14 20:04:18.317 -05:00|
```

##### Snowflake SQL[¶](#id850)

```
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0063 - TIME ZONE NOT SUPPORTED IN SNOWFLAKE ***/!!!
CURRENT_TIMESTAMP() at time zone 'Turks And Caicos Standard Time';
```

### Related EWIs[¶](#id851)

1. [SSC-FDM-TS0024](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0024):
   CURRENT_TIMESTAMP in At Time Zone statement may have a different behavior in certain cases.
2. [SSC-EWI-TS0063](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sqlServerEWI.html#ssc-ewi-ts0063):
   Time zone not supported in Snowflake.

## DATEADD[¶](#dateadd)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id852)

This function returns an integer representing the specified datepart of the specified date.
([DATEPART in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/abs-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id853)

#### Syntax[¶](#id854)

##### SQL Server[¶](#id855)

```
DATEADD (datepart , number , date )
```

##### Snowflake SQL[¶](#id856)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/dateadd.html)

```
DATEADD( <date_or_time_part>, <value>, <date_or_time_expr> )
```

### Examples[¶](#id857)

#### SQL Server[¶](#id858)

```
SELECT DATEADD(year,123, '20060731') as ADDDATE;
```

**Result:**

```
                 ADDDATE|
------------------------|
 2129-07-31 00:00:00.000|
```

##### Snowflake SQL[¶](#id859)

```
SELECT
DATEADD(year, 123, '20060731') as ADDDATE;
```

**Result:**

```
                 ADDDATE|
------------------------|
 2129-07-31 00:00:00.000|
```

## DATEDIFF[¶](#datediff)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id860)

This function returns the count (as a signed integer value) of the specified datepart boundaries
crossed between the specified startdate and enddate.
([DATEDIFF in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/datediff-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id861)

#### Syntax[¶](#id862)

##### SQL Server[¶](#id863)

```
DATEDIFF ( datepart , startdate , enddate )
```

##### Snowflake SQL[¶](#id864)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/datediff.html)

```
DATEDIFF( <date_or_time_part>, <date_or_time_expr1>, <date_or_time_expr2> )
```

### Examples[¶](#id865)

#### SQL Server[¶](#id866)

```
SELECT DATEDIFF(year,'2005-12-31 23:59:59.9999999', '2006-01-01 00:00:00.0000000');
```

**Result:**

<!-- prettier-ignore -->
|DIFF|
|---|
|1|

##### Snowflake SQL[¶](#id867)

```
SELECT DATEDIFF(year,'2005-12-31 23:59:59.9999999', '2006-01-01 00:00:00.0000000');
```

**Result:**

<!-- prettier-ignore -->
|DIFF|
|---|
|1|

## DATEFROMPARTS[¶](#datefromparts)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id868)

This function returns a **date** value that maps to the specified year, month, and day
values.([DATEFROMPARTS in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/datefromparts-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id869)

#### Syntax[¶](#id870)

##### SQL Server[¶](#id871)

```
DATEFROMPARTS ( year, month, day )
```

##### Snowflake SQL[¶](#id872)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/date_from_parts.html)

```
DATE_FROM_PARTS( <year>, <month>, <day> )
```

### Examples[¶](#id873)

#### SQL Server[¶](#id874)

```
SELECT DATEFROMPARTS ( 2010, 12, 31 ) AS RESULT;
```

**Result:**

<!-- prettier-ignore -->
|RESULT|
|---|
|2022-12-12|

##### Snowflake SQL[¶](#id875)

```
SELECT DATE_FROM_PARTS ( 2010, 12, 31 ) AS RESULT;
```

**Result:**

<!-- prettier-ignore -->
|RESULT|
|---|
|2022-12-12|

## DATENAME[¶](#datename)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id876)

This function returns a character string representing the specified datepart of the specified date.
([DATENAME in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/datename-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id877)

#### Syntax[¶](#id878)

##### SQL Server[¶](#id879)

```
DATENAME ( datepart , date )
```

##### Snowflake SQL[¶](#id880)

**Note:**

This transformation uses several functions depending on the inputs

```
DATE_PART( <date_or_time_part> , <date_or_time_expr> )
MONTHNAME( <date_or_timestamp_expr> )
DAYNAME( <date_or_timestamp_expr> )
```

### Examples[¶](#id881)

#### SQL Server[¶](#id882)

```
SELECT DATENAME(month, getdate()) AS DATE1,
DATENAME(day, getdate()) AS DATE2,
DATENAME(dw, GETDATE()) AS DATE3;
```

**Result:**

<!-- prettier-ignore -->
|DATE1|DATE2|DATE3|
|---|---|---|
|May|3|Tuesday|

##### Snowflake SQL[¶](#id883)

```
SELECT
MONTHNAME_UDF(CURRENT_TIMESTAMP() :: TIMESTAMP) AS DATE1,
DAYNAME_UDF(CURRENT_TIMESTAMP() :: TIMESTAMP) AS DATE2,
DAYNAME(CURRENT_TIMESTAMP() :: TIMESTAMP) AS DATE3;
```

**Result:**

<!-- prettier-ignore -->
|DATE1|DATE2|DATE3|
|---|---|---|
|May|Tue|Tue|

## DATEPART[¶](#datepart)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id884)

This function returns an integer representing the specified datepart of the specified date.
([DATEPART in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/abs-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id885)

#### Syntax[¶](#id886)

##### SQL Server[¶](#id887)

```
DATEPART ( datepart , date )
```

##### Snowflake SQL[¶](#id888)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/date_part.html)

```
DATE_PART( <date_or_time_part> , <date_or_time_expr> )
```

### Examples[¶](#id889)

#### SQL Server[¶](#id890)

```
SELECT DATEPART(YEAR, '10-10-2022') as YEAR
```

**Result:**

<!-- prettier-ignore -->
|YEAR|
|---|
|2022|

##### Snowflake SQL[¶](#id891)

```
SELECT
DATE_PART(YEAR, '10-10-2022' :: TIMESTAMP) as YEAR;
```

**Result:**

<!-- prettier-ignore -->
|YEAR|
|---|
|2022|

## DAY[¶](#day)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id892)

This function returns an integer that represents the day (day of the month) of the specified date.
([DAY in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/day-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id893)

#### Syntax[¶](#id894)

##### SQL Server[¶](#id895)

```
DAY ( date )
```

##### Snowflake SQL[¶](#id896)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/year.html)

```
DAY( <date_or_timestamp_expr> )
```

### Examples[¶](#id897)

#### SQL Server[¶](#id898)

```
SELECT DAY('10-10-2022') AS DAY
```

**Result:**

<!-- prettier-ignore -->
|DAY|
|---|
|10|

##### Snowflake SQL[¶](#id899)

```
SELECT DAY('10-10-2022' :: TIMESTAMP) AS DAY;
```

**Result:**

<!-- prettier-ignore -->
|DAY|
|---|
|10|

## EOMONTH[¶](#eomonth)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id900)

This function returns the last day of the month containing a specified date, with an optional
offset.
([EOMONTH in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/eomonth-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id901)

#### Syntax[¶](#id902)

##### SQL Server[¶](#id903)

```
EOMONTH ( start_date [, month_to_add ] )
```

##### Snowflake SQL[¶](#id904)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/last_day.html)

```
LAST_DAY( <date_or_time_expr> [ , <date_part> ] )
```

### Examples[¶](#id905)

#### SQL Server[¶](#id906)

```
SELECT EOMONTH (GETDATE()) AS Result;
```

**Result:**

<!-- prettier-ignore -->
|RESULT|
|---|
|2022-05-31|

##### Snowflake SQL[¶](#id907)

```
SELECT
LAST_DAY(DATEADD('month', 0, CURRENT_TIMESTAMP() :: TIMESTAMP)) AS Result;
```

**Result:**

<!-- prettier-ignore -->
|RESULT|
|---|
|2022-05-31|

## GETDATE[¶](#getdate)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id908)

Returns the current database system timestamp as a **datetime** value without the database time zone
offset.
([GETDATE in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/getdate-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id909)

#### Syntax[¶](#id910)

##### SQL Server[¶](#id911)

```
GETDATE()
```

##### Snowflake SQL[¶](#id912)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp.html)

```
CURRENT_TIMESTAMP( [ <fract_sec_precision> ] )
```

### Examples[¶](#id913)

#### SQL Server[¶](#id914)

```
SELECT GETDATE() AS DATE;
```

**Result:**

<!-- prettier-ignore -->
|DATE|
|---|
|2022-05-06 09:54:42.757|

##### Snowflake SQL[¶](#id915)

```
SELECT CURRENT_TIMESTAMP() :: TIMESTAMP AS DATE;
```

**Result:**

<!-- prettier-ignore -->
|DATE|
|---|
|2022-05-06 08:55:05.422|

## MONTH[¶](#month)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id916)

Returns an integer that represents the month of the specified _date_.
([MONTH in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/month-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id917)

#### Syntax[¶](#id918)

##### SQL Server[¶](#id919)

```
MONTH( date )
```

##### Snowflake SQL[¶](#id920)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/year.html)

```
MONTH ( <date_or_timestamp_expr> )
```

### Examples[¶](#id921)

#### SQL Server[¶](#id922)

```
SELECT MONTH('10-10-2022') AS MONTH
```

**Result:**

<!-- prettier-ignore -->
|MONTH|
|---|
|10|

##### Snowflake SQL[¶](#id923)

```
SELECT MONTH('10-10-2022' :: TIMESTAMP) AS MONTH;
```

**Result:**

<!-- prettier-ignore -->
|MONTH|
|---|
|10|

## SWITCHOFFSET[¶](#switchoffset)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id924)

The SWITCHOFFSET adjusts a given timestamp value to a specific timezone offset. This is done through
numerical values. More information can be found at
[SWITCHOFFSET (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/functions/switchoffset-transact-sql?view=sql-server-ver16).

### Sample Source Pattern[¶](#id925)

#### Syntax[¶](#id926)

[A UDF Helper](#switchoffset-udf) accomplish functional equivalence, also it shares the same syntax
as the SQLServer’s SWITCHOFFSET function.

##### SQLServer[¶](#sqlserver)

```
 SWITCHOFFSET ( datetimeoffset_expression, timezoneoffset_expression )
```

##### Snowflake SQL[¶](#id927)

```
 SWITCHOFFSET_UDF ( timestamp_tz_expression, timezoneoffset_expression )
```

#### Example[¶](#id928)

##### SQLServer[¶](#id929)

```
SELECT
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  SWITCHOFFSET('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

**Result:**

<!-- prettier-ignore -->
|fr_time|cr_time|
|---|---|
|1998-09-20 7:45:50.71345 +02:00|1998-09-19 23:45:50.7134500 -06:00|

##### Snowflake SQL[¶](#id930)

```
SELECT
  '1998-09-20 7:45:50.71345 +02:00' as fr_time,
  PUBLIC.SWITCHOFFSET_UDF('1998-09-20 7:45:50.71345 +02:00', '-06:00') as cr_time;
```

**Result:**

<!-- prettier-ignore -->
|fr_time|cr_time|
|---|---|
|1998-09-20 7:45:50.71345 +02:00|1998-09-19 23:45:50.7134500 -06:00|

## SYSDATETIME[¶](#sysdatetime)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id931)

Returns a datetime2(7) value that contains the date and time of the computer on which the instance
of SQL Server is running.
([SYSDATETIME in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/sysdatetime-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id932)

#### Syntax[¶](#id933)

##### SQL Server[¶](#id934)

```
SYSDATETIME ( )
```

##### Snowflake SQL[¶](#id935)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/localtime.html)

```
LOCALTIME()
```

### Examples[¶](#id936)

#### SQL Server[¶](#id937)

```
SELECT SYSDATETIME ( ) AS SYSTEM_DATETIME;
```

**Result:**

<!-- prettier-ignore -->
|SYSTEM_DATETIME|
|---|
|2022-05-06 12:08:05.501|

##### Snowflake SQL[¶](#id938)

```
SELECT LOCALTIME ( ) AS SYSTEM_DATETIME;
```

**Result:**

<!-- prettier-ignore -->
|SYSTEM_DATETIME|
|---|
|211:09:14|

## SYSUTCDATETIME[¶](#sysutcdatetime)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id939)

Returns a datetime2(7) value that contains the date and time of the computer on which the instance
of SQL Server is running.
([SYSUTCDATETIME in Transact-SQL](https://learn.microsoft.com/en-us/sql/t-sql/functions/sysutcdatetime-transact-sql?view=sql-server-ver16)).

### Sample Source Pattern[¶](#id940)

#### Syntax[¶](#id941)

##### SQL Server[¶](#id942)

```
SYSUTCDATETIME ( )
```

##### Snowflake SQL[¶](#id943)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/localtime.html)

```
SYSDATE()
```

### Examples[¶](#id944)

#### SQL Server[¶](#id945)

```
SELECT SYSUTCDATETIME() as SYS_UTC_DATETIME;
```

**Result:**

<!-- prettier-ignore -->
|SYSTEM_UTC_DATETIME|
|---|
|2023-02-02 20:59:28.0926502|

##### Snowflake SQL[¶](#id946)

```
SELECT
SYSDATE() as SYS_UTC_DATETIME;
```

**Result:**

<!-- prettier-ignore -->
|SYSTEM_UTC_DATETIME|
|---|
|2023-02-02 21:02:05.557|

## YEAR[¶](#year)

Applies to

- SQL Server
- Azure Synapse Analytics

### Description[¶](#id947)

Returns an integer that represents the year of the specified _date_.
([YEAR in Transact-SQL](https://docs.microsoft.com/en-us/sql/t-sql/functions/year-transact-sql?view=sql-server-ver15)).

### Sample Source Pattern[¶](#id948)

#### Syntax[¶](#id949)

##### SQL Server[¶](#id950)

```
YEAR( date )
```

##### Snowflake SQL[¶](#id951)

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/year.html)

```
YEAR ( <date_or_timestamp_expr> )
```

### Examples[¶](#id952)

#### SQL Server[¶](#id953)

```
SELECT YEAR('10-10-2022') AS YEAR
```

**Result:**

<!-- prettier-ignore -->
|YEAR|
|---|
|2022|

##### Snowflake SQL[¶](#id954)

```
SELECT YEAR('10-10-2022' :: TIMESTAMP) AS YEAR;
```

**Result:**

<!-- prettier-ignore -->
|YEAR|
|---|
|2022|
