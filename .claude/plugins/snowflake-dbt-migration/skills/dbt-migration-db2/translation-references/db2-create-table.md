---
description:
  The complete CREATE TABLE syntax for IBM DB2 is big enough that it does not fit on one page.
  However, the following image shows an overview of the syntax with some logical grouping that is
  later refer
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-create-table
title: SnowConvert AI - IBM DB2 - CREATE TABLE | Snowflake Documentation
---

## Description

> The complete CREATE TABLE
> [syntax](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table) for IBM DB2 is big
> enough that it does not fit on one page. However, the following image shows an overview of the
> syntax with some logical grouping that is later referenced.

## Grammar Syntax

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/create_table_overview.png)

## As Result Table

### Description 2

> Specifies that the columns of the new table have the same name, data type, and optionally same
> data, as the resulting from the fullselect.

Warning

AS RESULT TABLE is partially supported in Snowflake. The Copy options do not apply in Snowflake.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-as-result-table)
to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax 2

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/result_table_syntax_1.png)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/result_table_syntax_2.png)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/result_table_syntax_3.png)

### Sample Source Patterns

#### IBM DB2

```sql
CREATE TABLE TestTable1
AS (SELECT * FROM OriginalTable) WITH NO DATA;
```

#### Snowflake

```sql
CREATE TABLE TestTable1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
AS (SELECT * FROM
  OriginalTable
 LIMIT 0
);
```

##### IBM DB2 2

```sql
 CREATE TABLE TestTable2
AS (SELECT * FROM OriginalTable) WITH DATA
INCLUDING COLUMN DEFAULTS
INCLUDING IDENTITY;
```

##### Snowflake 2

```sql
CREATE TABLE TestTable2
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
AS (SELECT * FROM
  OriginalTable
 );
```

## Materialized Query Definition

### Description 3

> Materialized query tables (MQTs) are tables whose definition is based on the result of a query.

Currently, translation for the IBM DB2 Materialized Query is not supported by SnowConvert AI

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_materialized-query-definition)
to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax 3

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/materialized_query_syntax_1.png)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/materialized_query_syntax_2.png)

### Sample Source Patterns 2

#### IBM DB2 3

```sql
 CREATE TABLE TestTable4 (ACCTID, LOCID, YEAR, CNT) AS
  (SELECT ACCOUNTID, LOCATIONID, YEAR, COUNT(*)
     FROM TRANS
     GROUP BY ACCOUNTID, LOCATIONID, YEAR )
     DATA INITIALLY DEFERRED
     REFRESH DEFERRED
     MAINTAINED BY SYSTEM
     ENABLE QUERY OPTIMIZATION;
```

#### Snowflake 3

```sql
  CREATE TABLE TestTable4 (ACCTID, LOCID, YEAR, CNT) AS
(SELECT ACCOUNTID, LOCATIONID, YEAR,
  COUNT(*)
FROM
  TRANS
GROUP BY ACCOUNTID, LOCATIONID, YEAR )
 !!!RESOLVE EWI!!! /*** SSC-EWI-DB0021 - MATERIALIZED QUERY IS NOT SUPPORTED ***/!!!
DATA INITIALLY DEFERRED
REFRESH DEFERRED
MAINTAINED BY SYSTEM
ENABLE QUERY OPTIMIZATION
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Related EWIs

1. [SSC-EWI-DB0021](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI):
   NODE NOT SUPPORTED

## Of Type

### Description 4

> Specifies that the columns of the table are based on the attributes of the structured type.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_of) to
navigate to the IBM DB2 documentation page for this syntax.

TYPED TABLES are not supported in Snowflake.

### Grammar Syntax 4

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/typed_tables_syntax_1.png)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/typed_tables_syntax_2.png)

### Sample Source Patterns 3

#### IBM DB2 4

```sql
    CREATE TABLE TestTable5 OF Student_t UNDER Person
   INHERIT SELECT PRIVILEGES;
```

#### Snowflake 4

```sql
 !!!RESOLVE EWI!!! /*** SSC-EWI-DB0017 - TYPED TABLES ARE NOT SUPPORTED ***/!!!

CREATE TABLE TestTable5 OF Student_t UNDER Person
   INHERIT SELECT PRIVILEGES;
```

### Related EWIs 2

1. [SSC-EWI-DB0017](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI):
   NODE NOT SUPPORTED

## Staging Table Definition

### Description 5

> A _staging table_ allows incremental maintenance support for deferred materialized query table.

STAGING TABLES are not supported in Snowflake.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=tables-creating-staging-data) or
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_staging-table-definition)
to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax 5

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/staging_table_syntax.png)

### Sample Source Patterns 4

#### IBM DB2 5

```sql
create table TestTable6 for emp_summary propagate immediate;
```

#### Snowflake 5

```sql
 !!!RESOLVE EWI!!! /*** SSC-EWI-DB0018 - STAGING TABLES ARE NOT SUPPORTED ***/!!!
create table TestTable6 for emp_summary propagate immediate;
```

### Related EWIs 3

1. [SSC-EWI-DB0018](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI):
   NODE NOT SUPPORTED

## Element List

## Check Constraint

### Description 6

> Constraints are used to specify rules for the data in a table.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-column-options)
to navigate to the IBM DB2 documentation page for this syntax.

Warning

Some CONSTRAINT options are migrated as is to Snowflake but some of them are removed because of
platform differences. Check the code example to learn more.

### Grammar Syntax 6

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/check_constraint_syntax_1.png)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/check_constraint_syntax_2.png)

### Sample Source Patterns 5

#### IBM DB2 6

```sql
CREATE TABLE TestTable7(
    COL1 VARCHAR(1),
    CONSTRAINT CN1 CHECK(COL1<1),
    CONSTRAINT CN2 CHECK(SOMENAME DETERMINED BY OTHERNAME),
    CONSTRAINT CN2 CHECK((SOMENAME1, SOMENAME2) DETERMINED BY (SOMENAME3, SOMENAME4))
    );
```

#### Snowflake 6

```sql
CREATE TABLE TestTable7 (
    COL1 VARCHAR(1),
    !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
    CONSTRAINT CN1 CHECK(COL1<1),
    !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
    CONSTRAINT CN2 CHECK(SOMENAME DETERMINED BY OTHERNAME),
    !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
    CONSTRAINT CN2 CHECK((SOMENAME1, SOMENAME2) DETERMINED BY (SOMENAME3, SOMENAME4))
    )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Related EWIs 4

1. [SSC-EWI-0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0035):
   Check Statement Not Supported.

## Period Definition

### Description 7

Defines a period of time in which the data of a row is valid.

Warning

PERIOD-DEFINITION does not have a functional equivalent in Snowflake.

#### Note

Snowflake allows the storage of historical table data for up to 90 days, to know more about this see
[Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel.html).

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_period-definition)
to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax 7

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/period_definition_syntax.png)

### Sample Source Patterns 6

```sql
CREATE TABLE TestTable8(
COL1 DATE,
COL2 DATE,
PERIOD SYSTEM_TIME (COL1, COL2));
)
```

```sql
CREATE TABLE TestTable8 (
COL1 DATE,
    COL2 DATE,
    !!!RESOLVE EWI!!! /*** SSC-EWI-DB0003 - PERIOD SPECIFICATION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
    PERIOD SYSTEM_TIME (COL1, COL2))
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
 CREATE OR REPLACE TABLE TestTable9 (
    COL1 VARCHAR(1)
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
 ;
```

### Related EWIs 5

1. [SSC-EWI-DB0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0003):
   Period definition is not applicable in Snowflake.

## Referential Constraint

### Description 8

> Foreign Key Constraints are migrated via ALTER TABLE statements in order to remove dependencies at
> the table creation time and therefore facilitate database deployment.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-column-options)
to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax 8

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/referential_constraint_syntax_1.png)

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/referential_constraint_syntax_2.png)

### Sample Source Patterns 7

```sql
CREATE TABLE TestTable9(
    COL1 VARCHAR(1),
    CONSTRAINT FKCOL1 FOREIGN KEY (COL1) REFERENCES T1,
    CONSTRAINT FKCOL2 FOREIGN KEY (COL1) REFERENCES T1(COL1),
    CONSTRAINT FKCOL3 FOREIGN KEY (COL1) REFERENCES T1(COL1) ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT FKCOL4 FOREIGN KEY (COL1) REFERENCES T1(COL1) ENFORCED DISABLE QUERY OPTIMIZATION,
    FOREIGN KEY (COL1) REFERENCES T1
);
```

```sql
 CREATE OR REPLACE TABLE TestTable9 (
    COL1 VARCHAR(1)
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
 ;

 ALTER TABLE TestTable9
 ADD
    CONSTRAINT FKCOL1 FOREIGN KEY (COL1) REFERENCES T1 ;

 ALTER TABLE TestTable9
 ADD
    CONSTRAINT FKCOL2 FOREIGN KEY (COL1) REFERENCES T1 (COL1) ;

 ALTER TABLE TestTable9
 ADD
    CONSTRAINT FKCOL3 FOREIGN KEY (COL1) REFERENCES T1 (COL1) ON DELETE CASCADE ON UPDATE NO ACTION;

 ALTER TABLE TestTable9
 ADD
    CONSTRAINT FKCOL4 FOREIGN KEY (COL1) REFERENCES T1 (COL1) ENFORCED;

 ALTER TABLE TestTable9
 ADD CONSTRAINT TestTable9_COL1_T1
    FOREIGN KEY (COL1) REFERENCES T1 ;
```

## QUERY OPTIMIZATION

### Description 9

> Specifies whether the constraint or functional dependency can be used for query optimization under
> appropriate circumstances.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_without_overlaps)to
navigate to the IBM DB2 documentation page for this syntax.

Warning

ENABLE QUERY OPTIMIZATION Constraint attributes are removed because they are not applicable in
Snowflake.

### Grammar Syntax 9

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/query_optimization_syntax.png)

### Sample Source Patterns 8

#### IBM DB2 7

```sql
CREATE TABLE TestTable11
(
COL1 VARCHAR(10),
COL2 VARCHAR(10),
CONSTRAINT ConstraintName UNIQUE (COL1, COL2) ENABLE QUERY OPTIMIZATION
);
```

#### Snowflake 7

```sql
CREATE TABLE TestTable11
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10),
    CONSTRAINT ConstraintName UNIQUE (COL1, COL2)
    )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## WITHOUT OVERLAPS

### Description 10

> BUSINESS_TIME WITHOUT OVERLAPS means that for the other specified keys, the values are unique with
> respect to time for the BUSINESS_TIME period

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-column-options)
to navigate to the IBM DB2 documentation page for this syntax.

Warning

BUSINESS_TIME WITHOUT OVERLAPS Constraint attribute are removed because they are not applicable in
Snowflake.

### Grammar Syntax 10

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/without_overlaps_syntax.png)

### Sample Source Patterns 9

#### IBM DB2 8

```sql
 CREATE TABLE TestTable12
(
COL1 VARCHAR(10),
CONSTRAINT ConstraintName UNIQUE (COL1, COL2, BUSINESS_TIME WITHOUT OVERLAPS)
);
```

#### Snowflake 8

```sql
 CREATE TABLE TestTable12
(
COL1 VARCHAR(10),
    CONSTRAINT ConstraintName UNIQUE (COL1, COL2)
    )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## Column Options

## COMPRESS

### Description 11

> Specifies that system default values are to be stored using minimal space.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_compress_system_default)
to navigate to the IBM DB2 documentation page for this syntax.

Warning

COMPRESS SYSTEM DEFAULT is removed because it is not applicable in Snowflake

### Grammar Syntax 11

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/compress_system_default_syntax.png)

### Sample Source Patterns 10

#### IBM DB2 9

```sql
 CREATE TABLE TestTable13
(
COL1 VARCHAR(10) COMPRESS SYSTEM DEFAULT
);
```

#### Snowflake 9

```sql
 CREATE TABLE TestTable13
(
COL1 VARCHAR(10)
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Known issues

There are no known issues.

## HIDDEN

### Description 12

> Specifies whether the column is to be defined as hidden. The hidden attribute determines whether
> the column is included in an implicit reference to the table, or whether it can be explicitly
> referenced in SQL statements.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_not_hidden) to
navigate to the IBM DB2 documentation page for this syntax.

Warning

HIDDEN Option is removed because it is not applicable in Snowflake

### Grammar Syntax 12

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/hidden_column_syntax.png)

### Sample Source Patterns 11

#### IBM DB2 10

```sql
 CREATE TABLE TestTable14
(
COL1 VARCHAR(10) IMPLICITLY HIDDEN
);
```

#### Snowflake 10

```sql
 CREATE TABLE TestTable14
(
COL1 VARCHAR(10)
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## INLINE LENGTH

### Description 13

> Identifies the Inline Lenght of the reference type column.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_inline_length)
to navigate to the IBM DB2 documentation page for this syntax

Warning

INLINE LENGTH is removed because it is not applicable in Snowflake.

### Grammar Syntax 13

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/inline_length_syntax.png)

```sql
CREATE TABLE T1
(
COL1 VARCHAR(10) INLINE LENGTH 1024
);
```

### Sample Source Patterns 12

#### IBM DB2 11

```sql
 CREATE TABLE TestTable15
(
COL1 VARCHAR(10) INLINE LENGTH 1024
);
```

#### Snowflake 11

```sql
 CREATE TABLE TestTable15
(
COL1 VARCHAR(10)
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Known issues 2

There are no known issues.

## LOB OPTIONS

### Description 14

> Options for the LOB (Large Object Binary) data types

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-lob-options)
to navigate to the IBM DB2 documentation page for this syntax.

Warning

LOB OPTIONS are removed because they are not applicable in Snowflake.

### Grammar Syntax 14

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/lob_options_syntax.png)

### Sample Source Patterns 13

#### IBM DB2 12

```sql
 CREATE TABLE TestTable16
(
COL1 VARCHAR(10) LOGGED,
COL2 VARCHAR(10) NOT LOGGED,
COL3 VARCHAR(10) COMPACT,
COL4 VARCHAR(10) NOT COMPACT
)
```

#### Snowflake 12

```sql
 CREATE TABLE TestTable16
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10),
    COL3 VARCHAR(10),
    COL4 VARCHAR(10)
    )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## SCOPE

### Description 15

> Identifies the scope of the reference type column.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-column-options)to
navigate to the IBM DB2 documentation page for this syntax.

Warning

SCOPE options are removed because they are not applicable in Snowflake.

### Grammar Syntax 15

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/scope_syntax.png)

### Sample Source Patterns 14

#### IBM DB2 13

```sql
 CREATE TABLE TestTable17
(
COL1 VARCHAR(10) SCOPE TABLE2,
COL2 VARCHAR(10) SCOPE VIEW1
);
```

#### Snowflake 13

```sql
 CREATE TABLE TestTable17
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10)
    )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## SECURED

### Description 16

> Identifies a security label that exists for the security policy that is associated with the table.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_security-label-name)
to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax 16

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/security_label_syntax.png)

### Sample Source Patterns 15

#### IBM DB2 14

```sql
CREATE TABLE TestTable18
(
COL1 VARCHAR(10) COLUMN SECURED WITH securityLabel,
COL2 VARCHAR(10) COLUMN SECURED WITH securityLabel
);
```

#### Snowflake 14

```sql
 CREATE TABLE TestTable18
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10)
    )
 WITH ROW ACCESS POLICY securityLabel ON (
    COL1,
    COL2
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Known issues 3

If multiple security labels are declared an
[SSC-EWI-DB0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0001)will
appear in the Snowflake output code as shown below

#### IBM DB2 15

```sql
CREATE TABLE TestTable19
(
COL1 VARCHAR(10) COLUMN SECURED WITH securityLabel1,
COL2 VARCHAR(10) COLUMN SECURED WITH securityLabel2
);
```

#### Snowflake 15

```sql
CREATE TABLE TestTable19
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10)
    )
 WITH ROW ACCESS POLICY securityLabel1 ON (
    COL1
 )
 !!!RESOLVE EWI!!! /*** SSC-EWI-DB0001 - WITH ROW ACCESS POLICY CLAUSE DOES NOT SUPPORT MULTIPLE DECLARATION IN SNOWFLAKE ***/!!!
 WITH ROW ACCESS POLICY securityLabel2 ON (
    COL2
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

#### Related EWIs 6

1. [SSC-EWI-DB0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0001)Multiple
   Row Access policies

## Table Options

## CCSID

### Description 17

> Specifies the encoding scheme for string data that is stored in the table.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_ccsid) to
navigate to the IBM DB2 documentation page for this syntax.

Warning

CCSID is not applicable in Snowflake.

### Grammar Syntax 17

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/ccsid_syntax.png)

### Sample Source Patterns 16

#### IBM DB2 16

```sql
CREATE TABLE TestTable20 (
COL1 INT
) CCSID ASCII;
```

#### Snowflake 16

```sql
 CREATE TABLE TestTable20 (
COL1 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- CCSID ASCII
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Related EWIs 7

1. [SSC-FDM-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027):
   REMOVED STATEMENT, NOT APPLICABLE IN SNOWFLAKE.

## Compression Options

### Description 18

> Specifies whether row compression is to be used for the table.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_tablespace-name)
to navigate to the IBM DB2 documentation page for this syntax.

Warning

The Compression Options are not applicable in Snowflake.

### Grammar Syntax 18

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/compression_options_syntax.png)

### Sample Source Patterns 17

#### IBM DB2 17

```sql
CREATE TABLE TestTable21_01 (
COl1 INT,
COL2 INT
)
COMPRESS YES
;

CREATE TABLE TestTable21_02 (
COl1 INT,
COL2 INT
)
COMPRESS YES ADAPTIVE
;

CREATE TABLE TestTable21_03 (
COl1 INT,
COL2 INT
)
COMPRESS YES STATIC
;

CREATE TABLE TestTable21_04 (
COl1 INT,
COL2 INT
)
COMPRESS NO
;

CREATE TABLE TestTable21_05 (
COl1 INT,
COL2 INT
)
VALUE COMPRESSION
;
```

#### Snowflake 17

```sql
CREATE TABLE TestTable21_01 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--COMPRESS YES
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;

CREATE TABLE TestTable21_02 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--COMPRESS YES ADAPTIVE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;

CREATE TABLE TestTable21_03 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--COMPRESS YES STATIC
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;

CREATE TABLE TestTable21_04 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--COMPRESS NO
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;

CREATE TABLE TestTable21_05 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--VALUE COMPRESSION
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;
```

### Related EWIs 8

1. [SSC-FDM-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027):
   REMOVED STATEMENT, NOT APPLICABLE IN SNOWFLAKE.

## Data Capture

### Description 19

> Indicates whether extra information for inter-database data replication is to be written to the
> log.

Click
[here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_data_capture) to
navigate to the IBM DB2 documentation page for this syntax.

DATA CAPTURE is not supported

### Grammar Syntax 19

![image](https://docs.snowflake.com/en/migrations/snowconvert-docs/_images/data_capture_syntax.png)

### Sample Source Patterns 18

#### IBM DB2 18

```sql
 CREATE TABLE TestTable22
(
    COL1 INT
) DATA CAPTURE CHANGES;
```

#### Snowflake 18

```sql
 CREATE TABLE TestTable22
(
    COL1 INT
)
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0020 - DATA CAPTURE IS NOT SUPPORTED ***/!!!
 DATA CAPTURE CHANGES
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Related EWIs 9

1. [SSC-EWI-DB0020](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI):
   NODE NOT SUPPORTED

## REMOVED CLAUSES

### Description 20

The following clauses are removed in SnowConvert AI since they are not applicable in Snowflake:

- `Distribution` Clause
- `Not Logged Initially` Clause
- `Options` Clause
- `Organize by` Clause
- `Partition by` Clause
- `Security Policy` Clause
- `In` Clause
- `Long In` Clause
- `Index In` Clause
- `With Restrict On` Clause

### Sample Source Patterns 19

#### IBM DB2 19

```sql
-- Distribution Clause
 CREATE TABLE TestTable23
(
    COL1 INT
) DISTRIBUTE BY REPLICATION;

-- Not Logged Initially Clause
 CREATE TABLE TestTable24 (
COL1 INT
) NOT LOGGED INITIALLY;

-- Options Clause
 CREATE TABLE TestTable25 (
COL1 INT
) OPTIONS(tableOptionName 'stringConst', tableOptionName2 'stringConst');

-- Organize By Clause
 CREATE TABLE TestTable26
(
    COL1 INT,
    COL2 INT,
    COL3 INT
) ORGANIZE BY ROW;

-- Partition By Clause
 CREATE TABLE TestTable27_01 (
COl1 INT,
COL2 INT
)
PARTITION BY RANGE (COL1 NULLS LAST, COL2 NULLS FIRST)
(PARTITION partitionName STARTING FROM (MINVALUE, MAXVALUE, 3) EXCLUSIVE ENDING AT MAXVALUE EXCLUSIVE IN tablespaceName INDEX IN tablespaceName LONG IN tablespaceName);

-- Partition By Clause
CREATE TABLE TestTable27_02 (
COl1 INT,
COL2 INT
) PARTITION BY (COL1 NULLS LAST) (STARTING MINVALUE INCLUSIVE ENDING 3 EXCLUSIVE IN tablespaceName);

-- Partition By Clause
CREATE TABLE TestTable27_03 (
COL1 INT,
COL2 INT
) PART BY (COL1) (STARTING 1 ENDING 3);

-- Partition By Clause
CREATE TABLE TestTable27_04 (
COL1 INT,
COL2 INT
) PART BY (COL1) (PARTITION 5 STARTING 1 ENDING 3);

-- Partition By Clause
CREATE TABLE TestTable27_05 (
COL1 INT,
COL2 INT
) PARTITION BY (COL1 NULLS LAST)
(STARTING MINVALUE INCLUSIVE ENDING 3 EXCLUSIVE EVERY 3 YEAR);

-- Partition By Clause
CREATE TABLE TestTable27_06 (
COL1 INT,
COL2 INT
)
PARTITION BY (COL1 NULLS LAST)
(STARTING MINVALUE INCLUSIVE VALUES 3 EXCLUSIVE);

-- Partition By Clause
CREATE TABLE TestTable27_07 (
JYEARS INT
)
PARTITION BY RANGE (SKACDY_DAY ASC)
(
PARTITION 1 ENDING AT ('16.10.2019') HASH SPACE 2G,
PARTITION 2 ENDING AT ('17.10.2019')
);

-- Partition By Clause
CREATE TABLE TestTable27_08 (
TRANS_DATE DATE NOT NULL
)
PARTITION BY RANGE ("TRANS_DATE")
(
PART "PART_2019_03_01" STARTING ('2019-03-01') ENDING ('2019-03-01') IN "SLTPAYMFACTD1903",
PART "PART_2021_08_19" STARTING ('2021-08-19') ENDING ('2021-08-19') IN "SLTPAYMFACTD2108",
PARTITION "PART_2021_08_19" STARTING ('2021-08-19') ENDING ('2021-08-19') IN "SLTPAYMFACTD2108"
);

-- Security Policy Clause
 CREATE TABLE TestTable28 (
COL1 INT
) SECURITY POLICY PolicyName;

-- In Clause
 CREATE TABLE TestTable29
(
    COL1 INT
) IN TablescapeName;

-- Long In Clause
 CREATE TABLE TestTable29
(
    COL1 INT
) LONG IN TablespaceName;

-- Index In Clause
 CREATE TABLE TestTable30
(
    COL1 INT
) INDEX IN TablespaceName;

-- With Restrict On Drop Clause
 CREATE TABLE TestTable31 (
COL1 INT
) WITH RESTRICT ON DROP;
```

#### Snowflake 19

```sql
 -- Distribution Clause
 CREATE TABLE TestTable23
 (
    COL1 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- DISTRIBUTE BY REPLICATION
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Not Logged Initially Clause
 CREATE TABLE TestTable24 (
COL1 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- NOT LOGGED INITIALLY
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Options Clause
 CREATE TABLE TestTable25 (
COL1 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- OPTIONS(tableOptionName 'stringConst', tableOptionName2 'stringConst')
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Organize By Clause
 CREATE TABLE TestTable26
 (
    COL1 INT,
COL2 INT,
COL3 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- ORGANIZE BY ROW
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
 CREATE TABLE TestTable27_01 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY RANGE (COL1 NULLS LAST, COL2 NULLS FIRST)
--(PARTITION partitionName STARTING FROM (MINVALUE, MAXVALUE, 3) EXCLUSIVE ENDING AT MAXVALUE EXCLUSIVE IN tablespaceName INDEX IN tablespaceName LONG IN tablespaceName)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_02 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY (COL1 NULLS LAST) (STARTING MINVALUE INCLUSIVE ENDING 3 EXCLUSIVE IN tablespaceName)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_03 (
COL1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PART BY (COL1) (STARTING 1 ENDING 3)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_04 (
COL1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PART BY (COL1) (PARTITION 5 STARTING 1 ENDING 3)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_05 (
COL1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY (COL1 NULLS LAST)
--(STARTING MINVALUE INCLUSIVE ENDING 3 EXCLUSIVE EVERY 3 YEAR)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_06 (
COL1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY (COL1 NULLS LAST)
--(STARTING MINVALUE INCLUSIVE VALUES 3 EXCLUSIVE)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_07 (
JYEARS INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY RANGE (SKACDY_DAY ASC)
--(
--PARTITION 1 ENDING AT ('16.10.2019') HASH SPACE 2G,
--PARTITION 2 ENDING AT ('17.10.2019')
--)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_08 (
TRANS_DATE DATE NOT NULL
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY RANGE ("TRANS_DATE")
--(
--PART "PART_2019_03_01" STARTING ('2019-03-01') ENDING ('2019-03-01') IN "SLTPAYMFACTD1903",
--PART "PART_2021_08_19" STARTING ('2021-08-19') ENDING ('2021-08-19') IN "SLTPAYMFACTD2108",
--PARTITION "PART_2021_08_19" STARTING ('2021-08-19') ENDING ('2021-08-19') IN "SLTPAYMFACTD2108"
--)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Security Policy Clause
 CREATE TABLE TestTable28 (
COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--SECURITY POLICY PolicyName
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- In Clause
 CREATE TABLE TestTable29
(
    COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--IN TablescapeName
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Long In Clause
--** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR TestTable29. CHECK IF THE NAME IS INVALID OR DUPLICATED. **
 CREATE TABLE TestTable29
(
    COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--LONG IN TablespaceName
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Index In Clause
 CREATE TABLE TestTable30
(
    COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--INDEX IN TablespaceName
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- With Restrict On Drop Clause
 CREATE TABLE TestTable31 (
COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--WITH RESTRICT ON DROP
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Related EWIs 10

1. [SSC-FDM-0027](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027):
   REMOVED STATEMENT, NOT APPLICABLE IN SNOWFLAKE.
