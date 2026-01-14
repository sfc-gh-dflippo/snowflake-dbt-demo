---
description: Translation from PostgreSql to Snowflake
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/ddls/create-table/postgresql-create-table
title: SnowConvert AI - PostgreSQL - CREATE TABLE | Snowflake Documentation
---

## Applies to[¶](#applies-to)

- PostgreSQL
- Greenplum
- Netezza

## Description[¶](#description)

Creates a new table in PostgreSQL. You define a list of columns, each of which holds data of a
distinct type. The owner of the table is the issuer of the CREATE TABLE command.

For more information, please refer to `CREATE TABLE` documentation.

## Grammar Syntax[¶](#grammar-syntax)

```
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name ( [
  { column_name data_type [ STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT } ] [ COMPRESSION compression_method ] [ COLLATE collation ] [ column_constraint [ ... ] ]
    | table_constraint
    | LIKE source_table [ like_option ... ] }
    [, ... ]
] )
[ INHERITS ( parent_table [, ... ] ) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    OF type_name [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    PARTITION OF parent_table [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ] { FOR VALUES partition_bound_spec | DEFAULT }
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

where column_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL |
  NULL |
  CHECK ( expression ) [ NO INHERIT ] |
  DEFAULT default_expr |
  GENERATED ALWAYS AS ( generation_expr ) STORED |
  GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] index_parameters |
  PRIMARY KEY index_parameters |
  REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
    [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

and table_constraint is:

[ CONSTRAINT constraint_name ]
{ CHECK ( expression ) [ NO INHERIT ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] ) index_parameters |
  PRIMARY KEY ( column_name [, ... ] ) index_parameters |
  EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ] |
  FOREIGN KEY ( column_name [, ... ] ) REFERENCES reftable [ ( refcolumn [, ... ] ) ]
    [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

and like_option is:

{ INCLUDING | EXCLUDING } { COMMENTS | COMPRESSION | CONSTRAINTS | DEFAULTS | GENERATED | IDENTITY | INDEXES | STATISTICS | STORAGE | ALL }

and partition_bound_spec is:

IN ( partition_bound_expr [, ...] ) |
FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )
  TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )

index_parameters in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

[ INCLUDE ( column_name [, ... ] ) ]
[ WITH ( storage_parameter [= value] [, ... ] ) ]
[ USING INDEX TABLESPACE tablespace_name ]

exclude_element in an EXCLUDE constraint is:

{ column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]

referential_action in a FOREIGN KEY/REFERENCES constraint is:

{ NO ACTION | RESTRICT | CASCADE | SET NULL [ ( column_name [, ... ] ) ] | SET DEFAULT [ ( column_name [, ... ] ) ] }
```

Copy

## Tables Options[¶](#tables-options)

### TEMPORARY | TEMP, or IF NOT EXISTS[¶](#temporary-temp-or-if-not-exists)

Hint

This syntax is fully supported in Snowflake.

### GLOBAL | LOCAL[¶](#global-local)

Note

This syntax is not needed in Snowflake.

According to PostgreSQL’s documentation, GLOBAL | LOCAL are present for SQL Standard compatibility,
but have no effect in PostgreSQL and are deprecated. For that reason, SnowConvert AI will remove
these keyworks during the migration process.

#### Sample Source[¶](#sample-source)

Input Code:

##### PostgreSQL[¶](#postgresql)

```
CREATE GLOBAL TEMP TABLE TABLE1 (
   COL1 integer
);
```

Copy

Output Code:

##### Snowflake[¶](#snowflake)

```
CREATE TEMPORARY TABLE TABLE1 (
   COL1 integer
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}';
```

Copy

### UNLOGGED TABLE[¶](#unlogged-table)

Note

This syntax is not needed in Snowflake.

UNLOGGED tables offer a significant speed advantage because they are not written to the write-ahead
log. Snowflake doesn’t support this functionality, so the `UNLOGGED` clause will be commented out.

### Code Example[¶](#code-example)

#### Input Code:[¶](#input-code)

##### Greenplum[¶](#greenplum)

```
CREATE UNLOGGED TABLE TABLE1 (
  COL1 integer
);
```

Copy

#### Output Code:[¶](#output-code)

##### Snowflake[¶](#id1)

```
CREATE
--       --** SSC-FDM-PG0005 - UNLOGGED TABLE IS NOT SUPPORTED IN SNOWFLAKE, DATA WRITTEN MAY HAVE DIFFERENT PERFORMANCE. **
--       UNLOGGED
                TABLE TABLE1 (
   COL1 integer
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}';
```

Copy

## Column Attributes[¶](#column-attributes)

### CHECK Attribute[¶](#check-attribute)

Danger

This syntax is not supported in Snowflake.

The CHECK clause specifies an expression producing a Boolean result that new or updated rows must
satisfy for an insert or update operation to succeed. Snowflake does not have an equivalence with
this clause; SnowConvert AI will add an EWI. This will be applied as a CHECK attribute or table
constraint.

Grammar Syntax

```
CHECK  ( <expression> )
```

Copy

#### Sample Source[¶](#id2)

Input Code:

##### PostgreSQL[¶](#id3)

```
CREATE TABLE table1 (
    product_id INT PRIMARY KEY,
    quantity INT CHECK (quantity >= 0)
);
```

Copy

Output Code:

##### Snowflake[¶](#id4)

```
CREATE TABLE table1 (
    product_id INT PRIMARY KEY,
    quantity INT
                 !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!! CHECK (quantity >= 0)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}';
```

Copy

### GENERATED BY DEFAULT AS IDENTITY[¶](#generated-by-default-as-identity)

Hint

This syntax is fully supported in Snowflake.

Specifies that the column is a default IDENTITY column and enables you to assign a unique value to
the column automatically.

Grammar Syntax

```
 GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( <sequence_options> ) ]
```

Copy

#### Sample Source[¶](#id5)

Input Code:

##### PostgreSQL[¶](#id6)

```
CREATE TABLE table1 (
idValue INTEGER GENERATED ALWAYS AS IDENTITY)
```

Copy

Output Code:

##### Snowflake[¶](#id7)

```
CREATE TABLE table1 (
idValue INTEGER IDENTITY(1, 1) ORDER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}'
```

Copy

## Table Constraints[¶](#table-constraints)

### Primary Key, Foreign Key, and Unique[¶](#primary-key-foreign-key-and-unique)

Warning

This syntax is partially supported in Snowflake.

SnowConvert AI keeps the constraint definitions; however, in Snowflake, unique, primary, and foreign
keys are used for documentation and do not enforce constraints or uniqueness. They help describe
table relationships but don’t impact data integrity or performance.

## Table Attributes[¶](#table-attributes)

### LIKE option[¶](#like-option)

Warning

This syntax is partially supported in Snowflake.

The `LIKE` clause specifies a table from which the new table automatically copies all column names,
their data types, and their not-null constraints. PostgreSQL supports several options, while
Snowflake does not so that SnowConvert AI will remove the options like.

#### Grammar Syntax[¶](#id8)

```
  LIKE source_table { INCLUDING | EXCLUDING }
  { AM | COMMENTS | CONSTRAINTS | DEFAULTS | ENCODING | GENERATED | IDENTITY | INDEXES | RELOPT | STATISTICS | STORAGE | ALL }
```

Copy

#### Sample Source Patterns[¶](#sample-source-patterns)

Input Code:

##### PostgreSQL[¶](#id9)

```
CREATE TABLE source_table (
    id INT,
    name VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN
);

CREATE TABLE target_table_no_constraints (LIKE source_table INCLUDING DEFAULTS EXCLUDING CONSTRAINTS EXCLUDING INDEXES);
```

Copy

Output Code:

##### Snowflake[¶](#id10)

```
CREATE TABLE source_table (
    id INT,
    name VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/12/2025",  "domain": "no-domain-provided" }}';
CREATE TABLE target_table_no_constraints LIKE source_table;
```

Copy

### ON COMMIT[¶](#on-commit)

Warning

This syntax is partially supported.

Specifies the behaviour of the temporary table when a commit is done.

#### Grammar Syntax[¶](#id11)

```
ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP }
```

Copy

## Sample Source Patterns[¶](#id12)

### Input Code:[¶](#id13)

#### PostgreSQL[¶](#id14)

```
CREATE GLOBAL TEMPORARY TABLE temp_data_delete (
    id INT,
    data TEXT
) ON COMMIT DELETE ROWS;
```

Copy

#### Output Code:[¶](#id15)

##### Snowflake[¶](#id16)

```
CREATE TEMPORARY TABLE temp_data_delete (
    id INT,
    data TEXT
)
----** SSC-FDM-0008 - ON COMMIT NOT SUPPORTED **
--ON COMMIT DELETE ROWS
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/12/2025",  "domain": "no-domain-provided" }}';
```

Copy

### PARTITION BY, USING, TABLESPACE, and WITH[¶](#partition-by-using-tablespace-and-with)

Note

This syntax is not needed in Snowflake.

These clauses in Snowflake are unnecessary because they automatically handle the data storage,
unlike PostgreSQL, which could be set up manually. For this reason, these clauses are removed during
migration.

## Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0035](../../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035):
   Check statement not supported.
2. [SSC-FDM-PG0005](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM.html#ssc-fdm-pg0005):
   UNLOGGED Table is not supported in Snowflake; data written may have different performance.
3. [SSC-FDM-0008](../../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0008):
   On Commit not supported.
