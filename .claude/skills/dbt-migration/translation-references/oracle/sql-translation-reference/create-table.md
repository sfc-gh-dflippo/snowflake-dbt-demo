---
description:
  In this section you could find information about TABLES, their syntax and current convertions.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-translation-reference/create-table
title: SnowConvert AI - Oracle - Create Table | Snowflake Documentation
---

## Description[¶](#description)

In Oracle, the CREATE TABLE statement is used to create one of the following types of tables: a
relational table which is the basic structure to hold user data, or an object table which is a table
that uses an object type for a column definition.
([Oracle documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-TABLE.html#GUID-F9CE0CC3-13AE-4744-A43C-EAC7A71AAAB6))

**Oracle syntax**

```
CREATE [ { GLOBAL | PRIVATE } TEMPORARY | SHARDED | DUPLICATED | [ IMMUTABLE ] BLOCKCHAIN
  | IMMUTABLE  ]
   TABLE
  [ schema. ] table
  [ SHARING = { METADATA | DATA | EXTENDED DATA | NONE } ]
  { relational_table | object_table | XMLType_table }
  [ MEMOPTIMIZE FOR READ ]
  [ MEMOPTIMIZE FOR WRITE ]
  [ PARENT [ schema. ] table ] ;
```

Copy

**Snowflake Syntax**

```
CREATE [ OR REPLACE ]
    [ { [ { LOCAL | GLOBAL } ] TEMP | TEMPORARY | VOLATILE | TRANSIENT } ]
  TABLE [ IF NOT EXISTS ] <table_name> (
    -- Column definition
    <col_name> <col_type>
      [ inlineConstraint ]
      [ NOT NULL ]
      [ COLLATE '<collation_specification>' ]
      [
        {
          DEFAULT <expr>
          | { AUTOINCREMENT | IDENTITY }
            [
              {
                ( <start_num> , <step_num> )
                | START <num> INCREMENT <num>
              }
            ]
            [ { ORDER | NOORDER } ]
        }
      ]
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
      [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
      [ COMMENT '<string_literal>' ]

    -- Additional column definitions
    [ , <col_name> <col_type> [ ... ] ]

    -- Out-of-line constraints
    [ , outoflineConstraint [ ... ] ]
  )
  [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
  [ ENABLE_SCHEMA_EVOLUTION = { TRUE | FALSE } ]
  [ STAGE_FILE_FORMAT = (
     { FORMAT_NAME = '<file_format_name>'
       | TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } [ formatTypeOptions ]
     } ) ]
  [ STAGE_COPY_OPTIONS = ( copyOptions ) ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ CHANGE_TRACKING = { TRUE | FALSE } ]
  [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
```

Copy

Note

For more Snowflake information review the following
[documentation](https://docs.snowflake.com/en/sql-reference/sql/create-table).

## Sample Source Patterns[¶](#sample-source-patterns)

### 2.1. Physical and Table Properties[¶](#physical-and-table-properties)

#### Oracle[¶](#oracle)

```
CREATE TABLE "MySchema"."BaseTable"
(
    BaseId NUMBER DEFAULT 10 NOT NULL ENABLE
) SEGMENT CREATION IMMEDIATE
  PCTFREE 0 PCTUSED 40 INITRANS 1 MAXTRANS 255
  COLUMN STORE COMPRESS FOR QUERY HIGH NO ROW LEVEL LOCKING LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "MyTableSpace"
  PARTITION BY LIST ("BaseId")
 (
    PARTITION "P20211231"  VALUES (20211231) SEGMENT CREATION DEFERRED
    PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255
    ROW STORE COMPRESS ADVANCED LOGGING
    STORAGE(
    BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
    TABLESPACE "MyTableSpace"
  )
  PARALLEL;
```

Copy

#### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE TABLE "MySchema"."BaseTable"
 (
     BaseId NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ DEFAULT 10 NOT NULL
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;
```

Copy

Note

Table properties are removed because they are not required after the migration in Snowflake.

### 2.2. Constraints and Constraint States[¶](#constraints-and-constraint-states)

The following constraints will be commented out:

- `CHECK` Constraint

Note

The `USING INDEX` constraint will be entirely removed from the output code during the conversion.

#### Oracle[¶](#id1)

```
CREATE TABLE "MySchema"."BaseTable"
(
    BaseId NUMBER DEFAULT 10 NOT NULL ENABLE NOVALIDATE,
    "COL1" NUMBER CHECK( "COL1" IS NOT NULL ),
	  CHECK( "COL1" IS NOT NULL ),
    CONSTRAINT "Constraint1BaseTable" PRIMARY KEY (BaseId)
        USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS
        STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
        PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1) ENABLE
);
```

Copy

#### Snowflake[¶](#id2)

```
CREATE OR REPLACE TABLE "MySchema"."BaseTable"
	(
	    BaseId NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ DEFAULT 10 NOT NULL,
	    "COL1" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ NOT NULL
 	                                                                                                                     !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
 	                                                                                                                     CHECK( "COL1" IS NOT NULL ),
	!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
		  CHECK( "COL1" IS NOT NULL ),
	    CONSTRAINT "Constraint1BaseTable" PRIMARY KEY (BaseId)
	)
	COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
	;
```

Copy

On the other hand, but in the same way, in case you have any constraint state after a NOT NULL
constraint as follows:

- `RELY`
- `NO RELY`
- `RELY ENABLE`
- `RELY DISABLE`
- `VALIDATE`
- `NOVALIDATE`

These will also be commented out.

Note

The ENABLE constraint state will be completely removed from the output code during the conversion
process. In the case of the DISABLE state, it will also be removed concurrently with the NOT NULL
constraint.

#### Oracle[¶](#id3)

```
CREATE TABLE Table1(
  col1 INT NOT NULL ENABLE,
  col2 INT NOT NULL DISABLE,
  col3 INT NOT NULL RELY
);
```

Copy

#### Snowflake[¶](#id4)

```
CREATE OR REPLACE TABLE Table1 (
    col1 INT NOT NULL,
    col2 INT ,
    col3 INT NOT NULL /*** SSC-FDM-OR0006 - CONSTRAINT STATE RELY REMOVED FROM NOT NULL INLINE CONSTRAINT ***/
  )
  COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
  ;
```

Copy

### 2.3. Foreign Key[¶](#foreign-key)

If there is a table with a NUMBER column with no precision nor scale, and another table with a
NUMBER(\*,0) column that references to the previously mentioned NUMBER column, we will comment out
this foreign key.

#### Oracle[¶](#id5)

```
CREATE TABLE "MySchema"."MyTable"
(
    "COL1" NUMBER,
    CONSTRAINT "PK" PRIMARY KEY ("COL1")
);
```

Copy

#### Snowflake[¶](#id6)

```
CREATE OR REPLACE TABLE "MySchema"."MyTable"
    (
        "COL1" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
        CONSTRAINT "PK" PRIMARY KEY ("COL1")
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

Copy

### 2.4. Virtual Column[¶](#virtual-column)

#### Oracle[¶](#id7)

```
CREATE TABLE "MySchema"."MyTable"
(
    "COL1" NUMBER GENERATED ALWAYS AS (COL1 * COL2) VIRTUAL
);
```

Copy

#### Snowflake[¶](#id8)

```
CREATE OR REPLACE TABLE "MySchema"."MyTable"
    (
        "COL1" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ AS (COL1 * COL2)
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

Copy

### 2.5. Identity Column[¶](#identity-column)

For identity columns, a sequence is created and assigned to the column.

#### Oracle[¶](#id9)

```
CREATE TABLE "MySchema"."BaseTable"
(
	"COL0" NUMBER GENERATED BY DEFAULT ON NULL
		AS IDENTITY MINVALUE 1 MAXVALUE 9999999999999999999999999999
		INCREMENT BY 1
		START WITH 621
		CACHE 20
		NOORDER  NOCYCLE  NOT NULL ENABLE
);
```

Copy

#### Snowflake[¶](#id10)

```
CREATE OR REPLACE TABLE "MySchema"."BaseTable"
	(
		"COL0" NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ IDENTITY(621, 1) ORDER NOT NULL
	)
	COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
	;
```

Copy

### 2.6. CLOB and BLOB column declaration[¶](#clob-and-blob-column-declaration)

Columns declared as CLOB or BLOB will be changed to VARCHAR.

#### Oracle[¶](#id11)

```
CREATE TABLE T
(
 Col1 BLOB DEFAULT EMPTY_BLOB(),
Col5 CLOB DEFAULT EMPTY_CLOB()
);
```

Copy

#### Snowflake[¶](#id12)

```
CREATE OR REPLACE TABLE T
 (
  Col1 BINARY,
 Col5 VARCHAR
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;
```

Copy

### 2.7. Constraint Name[¶](#constraint-name)

Warning

The constraint name is removed from the code because it is not applicable in Snowflake.

#### Oracle[¶](#id13)

```
CREATE TABLE "CustomSchema"."BaseTable"(
 "PROPERTY" VARCHAR2(64) CONSTRAINT "MICROSOFT_NN_PROPERTY" NOT NULL ENABLE
  );
```

Copy

#### Snowflake[¶](#id14)

```
CREATE OR REPLACE TABLE "CustomSchema"."BaseTable" (
  "PROPERTY" VARCHAR(64) NOT NULL /*** SSC-FDM-0012 - CONSTRAINT NAME '"MICROSOFT_NN_PROPERTY"' IN NULL OR NOT NULL CONSTRAINT IS NOT SUPPORTED IN SNOWFLAKE ***/
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
   ;
```

Copy

### 2.8. Default columns with times[¶](#default-columns-with-times)

The columns declared as Date types will be cast to match with the specific date type.

#### Oracle[¶](#id15)

```
CREATE TABLE TABLE1
(
"COL1" VARCHAR(50) DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TABLE1
(
 COL0 TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
 COL1 TIMESTAMP(6) DEFAULT CURRENT_TIME,
 COL2 TIMESTAMP(6) WITH LOCAL TIME ZONE DEFAULT '1900-01-01 12:00:00',
 COL3 TIMESTAMP(6) WITH TIME ZONE DEFAULT '1900-01-01 12:00:00',
 COL4 TIMESTAMP(6) WITHOUT TIME ZONE DEFAULT '1900-01-01 12:00:00',
 COL5 TIMESTAMP(6) DEFAULT TO_TIMESTAMP('01/01/1900 12:00:00.000000 AM', 'MM/DD/YYYY HH:MI:SS.FF6 AM')
 );
```

Copy

#### Snowflake[¶](#id16)

```
CREATE OR REPLACE TABLE TABLE1
 (
 "COL1" VARCHAR(50) DEFAULT TO_VARCHAR(CURRENT_TIMESTAMP(), 'YYYY-MM-DD HH:MI:SS')
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;

 --** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR TABLE1. CHECK IF THE NAME IS INVALID OR DUPLICATED. **
 CREATE OR REPLACE TABLE TABLE1
 (
  COL0 TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP() :: TIMESTAMP(6),
  COL1 TIMESTAMP(6) DEFAULT CURRENT_TIME() :: TIMESTAMP(6),
  COL2 TIMESTAMP_LTZ(6) DEFAULT '1900-01-01 12:00:00' :: TIMESTAMP_LTZ(6),
  COL3 TIMESTAMP_TZ(6) DEFAULT '1900-01-01 12:00:00' :: TIMESTAMP_TZ(6),
  COL4 TIMESTAMP(6) WITHOUT TIME ZONE DEFAULT '1900-01-01 12:00:00' :: TIMESTAMP(6) WITHOUT TIME ZONE,
  COL5 TIMESTAMP(6) DEFAULT TO_TIMESTAMP('01/01/1900 12:00:00.000000 AM', 'MM/DD/YYYY HH:MI:SS.FF6 AM') :: TIMESTAMP(6)
  )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
 ;
```

Copy

### 2.9 Sharing and Memoptimize options[¶](#sharing-and-memoptimize-options)

Some options in Oracle are not required in Snowflake. That is the case for the `sharing` and
`memoptimize` options, they will be removed in the output code.

#### Oracle[¶](#id17)

```
CREATE TABLE table1
    SHARING = METADATA (
     id NUMBER,
     name VARCHAR2(50),
     date DATE,
     CONSTRAINT pk_table PRIMARY KEY (id)
 ) MEMOPTIMIZE FOR READ;
```

Copy

#### Snowflake[¶](#id18)

```
CREATE OR REPLACE TABLE table1 (
     id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
     name VARCHAR(50),
     date TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
     CONSTRAINT pk_table PRIMARY KEY (id)
 )
 COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
 ;
```

Copy

### 2.10 AS SubQuery[¶](#as-subquery)

The following properties and clauses are unsupported when creating a table through `AS SubQuery` in
Snowflake.

```
[ immutable_table_clauses ]
[ blockchain_table_clauses ]
[ DEFAULT COLLATION collation_name ]
[ ON COMMIT { DROP | PRESERVE } DEFINITION ]
[ ON COMMIT { DELETE | PRESERVE } ROWS ]
[ physical_properties ]
```

Copy

#### Oracle[¶](#id19)

```
create table table1
-- NO DROP NO DELETE HASHING USING sha2_512 VERSION v1 -- blockchain_clause not yet supported
DEFAULT COLLATION somename
ON COMMIT DROP DEFINITION
ON COMMIT DELETE ROWS
COMPRESS
NOLOGGING
AS
   select
      *
   from
      table1;
```

Copy

#### Snowflake[¶](#id20)

```
CREATE OR REPLACE TABLE table1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
-- NO DROP NO DELETE HASHING USING sha2_512 VERSION v1 -- blockchain_clause not yet supported
AS
   select
      *
   from
      table1;
```

Copy

## Known Issues[¶](#known-issues)

1. Some properties on the tables may be adapted to or commented on because the behavior in Snowflake
   is different.

## Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0035](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035):
   Check statement not supported.
2. [SSC-FDM-0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
3. [SSC-FDM-0019](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0019):
   Sematic information could not be loaded.
4. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior.
5. [SSC-FDM-OR0006](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0006):
   Constraint state removed from not null inline constraint.
