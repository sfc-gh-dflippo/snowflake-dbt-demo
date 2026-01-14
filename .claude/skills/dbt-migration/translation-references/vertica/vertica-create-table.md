---
description: Creates a table in the logical schema. (Vertica SQL Language Reference Create Table).
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/vertica/vertica-create-table
title: SnowConvert AI - Vertica - CREATE TABLE | Snowflake Documentation
---

## Description[¶](#description)

Creates a table in the logical schema.
([Vertica SQL Language Reference Create Table](https://docs.vertica.com/23.3.x/en/sql-reference/statements/create-statements/create-table/)).

Warning

This syntax is partially supported in Snowflake. Translation pending for these clauses:

```
DISK_QUOTA quota
SET USING expression
ENCODING encoding-type
ACCESSRANK integer
```

## Grammar Syntax[¶](#grammar-syntax)

```
CREATE TABLE [ IF NOT EXISTS ] [[database.]schema.]table
   ( column-definition[,...] [, table-constraint [,...]] )
   [ ORDER BY column[,...] ]
   [ segmentation-spec ]
   [ KSAFE [safety] ]
   [ partition-clause]
   [ {INCLUDE | EXCLUDE} [SCHEMA] PRIVILEGES ]
   [ DISK_QUOTA quota ]

<column-definition> ::=
column-name data-type
    [ column-constraint ][...]
    [ ENCODING encoding-type ]
    [ ACCESSRANK integer ]

<column-constraint> ::=
[ { AUTO_INCREMENT | IDENTITY } [ (args) ] ]
[ CONSTRAINT constraint-name ] {
   [ CHECK (expression) [ ENABLED | DISABLED ] ]
   [ [ DEFAULT expression ] [ SET USING expression } | DEFAULT USING expression ]
   [ NULL | NOT NULL ]
   [ { PRIMARY KEY [ ENABLED | DISABLED ] REFERENCES table [( column )] } ]
   [ UNIQUE [ ENABLED | DISABLED ] ]
}

<table-constraint>::=
[ CONSTRAINT constraint-name ]
{
... PRIMARY KEY (column[,... ]) [ ENABLED | DISABLED ]
... | FOREIGN KEY (column[,... ] ) REFERENCES table [ (column[,...]) ]
... | UNIQUE (column[,...]) [ ENABLED | DISABLED ]
... | CHECK (expression) [ ENABLED | DISABLED ]
}
```

## Tables Options[¶](#tables-options)

### Order By[¶](#order-by)

In Vertica, this `ORDER BY` clause specifies how data is physically sorted within a
**superprojection**, an optimized storage structure for a table. This explicit physical ordering at
table creation is not directly supported in Snowflake. For more information please refer to
[SSC-EWI-VT0002.](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI#ssc-ewi-vt0002)

#### Sample Source[¶](#sample-source)

##### Vertica[¶](#vertica)

```
CREATE TABLE metrics
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
ORDER BY measurement_date, business_unit, metric_category;
```

##### Snowflake[¶](#snowflake)

```
CREATE TABLE metrics
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
!!!RESOLVE EWI!!! /*** SSC-EWI-VT0002 - ORDER BY TABLE OPTION IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
ORDER BY measurement_date, business_unit, metric_category
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

### Projections Clauses[¶](#projections-clauses)

Vertica’s projections are a mechanism to define and maintain the physical sort order of data on
disk, thereby optimizing query performance for specific access patterns. Snowflake, however,
utilizes a fundamentally different storage and optimization strategy. Data in Snowflake is
automatically broken down into immutable **micro-partitions**, which are then organized and managed
by the cloud service.

While an inherent order might exist within these micro-partitions due to insertion or the
application of **clustering keys**, Snowflake’s query optimizer and its underlying architecture are
designed to efficiently prune these micro-partitions during query execution, regardless of a
pre-defined global sort order. This approach, combined with automatic caching and a columnar storage
format, allows Snowflake to achieve high performance without requiring users to manually define and
manage physical data structures like Vertica’s projections, thus simplifying data management and
optimizing for a broader range of query patterns without explicit physical sort definitions.

Due to these reasons, the following clauses aren’t necessary in Snowflake and are removed from the
original code:

```
[ segmentation-spec ]
[ KSAFE [safety] ]
[ partition-clause]
```

### Inherited Schema Privileges Clause[¶](#inherited-schema-privileges-clause)

`INCLUDE SCHEMA PRIVILEGES` is a Vertica-specific feature that governs how privileges are inherited,
in this case, potentially from the schema level. Snowflake does not have a direct equivalent for
this clause within its `CREATE TABLE` syntax. Privileges in Snowflake are managed explicitly through
`GRANT` statements.

Warning

This syntax is not supported in Snowflake.

#### Sample Source[¶](#id1)

##### Vertica[¶](#id2)

```
CREATE TABLE metrics
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
INCLUDE SCHEMA PRIVILEGES;
```

##### Snowflake[¶](#id3)

```
CREATE TABLE metrics
(
  metric_id INT,
  business_unit VARCHAR(100),
  metric_category VARCHAR(50) NOT NULL,
  measurement_date DATE NOT NULL
)
!!!RESOLVE EWI!!! /*** SSC-EWI-VT0001 - INHERITED PRIVILEGES CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
INCLUDE SCHEMA PRIVILEGES
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

## Constraints[¶](#constraints)

### IDENTITY - AUTO_INCREMENT[¶](#identity-auto-increment)

Creates a table column whose values are automatically generated by and managed by the database. You
cannot change or load values in this column. You can set this constraint on only one table column.

Success

This syntax is fully supported in Snowflake.

#### Sample Source[¶](#id4)

##### Vertica[¶](#id5)

```
CREATE TABLE customers (
  id AUTO_INCREMENT(1, 2),
  name VARCHAR(50)
);

CREATE TABLE customers2 (
  id IDENTITY(1, 2),
  name VARCHAR(50)
);
```

##### Snowflake[¶](#id6)

```
CREATE TABLE customers (
  id INT AUTOINCREMENT(1, 2) ORDER,
  name VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';

CREATE TABLE customers2 (
  id INT IDENTITY(1, 2) ORDER,
  name VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

### CHECK Constraint[¶](#check-constraint)

The `CHECK` clause in Vertica requires new or updated rows to satisfy a Boolean expression.
Snowflake doesn’t have an equivalent to this clause; therefore, SnowConvert AI will add an EWI. This
will be applied as a `CHECK` attribute or table constraint in the converted code.

Danger

This syntax is not supported in Snowflake.

#### Sample Source[¶](#id7)

##### Vertica[¶](#id8)

```
CREATE TABLE table1 (
    product_id INT PRIMARY KEY,
    quantity INT CHECK (quantity >= 0)
);
```

##### Snowflake[¶](#id9)

```
CREATE TABLE table1 (
    product_id INT PRIMARY KEY,
    quantity INT
                 !!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!! CHECK (quantity >= 0)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

### DEFAULT Constraint[¶](#default-constraint)

Warning

This syntax is partially supported in Snowflake.

The basic `DEFAULT` clause from Vertica is fully supported and translates directly to Snowflake. For
Vertica’s `DEFAULT USING` clause, however, the translation is partial. Snowflake will correctly
apply the `DEFAULT` value when new rows are inserted, but the deferred refresh capability from the
`USING` portion has no direct equivalent and some expressions might not be supported in Snowflake.
Therefore, a warning is added to highlight this functional difference.

#### Sample Source[¶](#id10)

##### Vertica[¶](#id11)

```
CREATE TABLE table1 (
    base_value INT,
    status_code INT DEFAULT 0,
    derived_value INT DEFAULT USING (base_value + 100)
);
```

##### Snowflake[¶](#id12)

```
CREATE TABLE table1 (
    base_value INT,
    status_code INT DEFAULT 0,
    derived_value INT DEFAULT (base_value + 100) /*** SSC-FDM-VT0001 - EXPRESSION IN USING CONSTRAINT MIGHT NOT BE SUPPORTED IN SNOWFLAKE ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

### PRIMARY KEY - UNIQUE - FOREIGN KEY[¶](#primary-key-unique-foreign-key)

SnowConvert AI keeps the constraint definitions; however, in Snowflake, these properties are
provided to facilitate migrating from other databases. They are not enforced or maintained by
Snowflake. This means that the defaults can be changed for these properties, but changing the
defaults results in Snowflake not creating the constraint.

Warning

This syntax is partially supported in Snowflake.

#### Sample Source[¶](#id13)

##### Vertica[¶](#id14)

```
CREATE OR REPLACE TABLE employees (
    emp_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    CONSTRAINT pk_employees_enabled PRIMARY KEY (emp_id) ENABLED
);
```

##### Snowflake[¶](#id15)

```
CREATE OR REPLACE TABLE employees (
    emp_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    CONSTRAINT pk_employees_enabled PRIMARY KEY (emp_id) ENABLE
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

## Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0035):
   Check statement not supported.
2. [SSC-EWI-VT0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI#ssc-ewi-vt0001):
   Inherited privileges clause is not supported in Snowflake.
3. [SSC-EWI-VT0002](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI#ssc-ewi-vt0002):
   Order by table option is not supported in Snowflake.
4. [SSC-FDM-VT0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/verticaFDM#ssc-fdm-vt0001):
   Expression in USING constraint might not be supported in Snowflake.

## CREATE TABLE AS[¶](#create-table-as)

### Description[¶](#id16)

Creates and loads a table from the
[results of a query](https://docs.vertica.com/23.3.x/en/admin/working-with-native-tables/creating-table-from-other-tables/creating-table-from-query/).
([Vertica SQL Language Reference Create Table](https://docs.vertica.com/23.3.x/en/sql-reference/statements/create-statements/create-table/)).

Warning

This syntax is partially supported in Snowflake. Translation pending for the following clauses

```
[ /*+ LABEL */ ]
[ AT epoch ]
[ ENCODED BY column-ref-list ]
[ ENCODING encoding-type ]
[ ACCESSRANK integer ]
[ GROUPED ( column-reference[,...] ) ]
```

### Grammar Syntax[¶](#id17)

```
CREATE TABLE [ IF NOT EXISTS ] [[database.]schema.]table
[ ( column-name-list ) ]
[ {INCLUDE | EXCLUDE} [SCHEMA] PRIVILEGES ]
AS  [ /*+ LABEL */ ] [ AT epoch ] query [ ENCODED BY column-ref-list ] [ segmentation-spec ]

<column-name-list> ::=
column-name-list
    [ ENCODING encoding-type ]
    [ ACCESSRANK integer ]
    [ GROUPED ( column-reference[,...] ) ]
```

### Tables Options[¶](#id18)

#### Segmentation Clause[¶](#segmentation-clause)

This syntax isn’t required in Snowflake and is removed from the original code. For more information,
please refer to [**Projections Clauses**](#projections-clauses).

**Note:**

This syntax is not required in Snowflake.

#### Inherited Schema Privileges Clause[¶](#id19)

`INCLUDE SCHEMA PRIVILEGES` is a Vertica-specific feature that governs how privileges are inherited,
in this case, potentially from the schema level. Snowflake does not have a direct equivalent for
this clause within its `CREATE TABLE` syntax. For more information please refer to
[Inherited Schema Privileges Clause.](#inherited-schema-privileges-clause)

Warning

This syntax is not supported in Snowflake.

### Related EWIs[¶](#id20)

1. [SSC-EWI-VT0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI#ssc-ewi-vt0001):
   Inherited privileges clause is not supported in Snowflake.

## CREATE TABLE LIKE[¶](#create-table-like)

### Description[¶](#id21)

Creates the table by
[replicating an existing table](https://docs.vertica.com/23.3.x/en/admin/working-with-native-tables/creating-table-from-other-tables/replicating-table/).
([Vertica SQL Language Reference Create Table](https://docs.vertica.com/23.3.x/en/sql-reference/statements/create-statements/create-table/)).

Warning

This syntax is partially supported in Snowflake. Translation pending for the following clause:

```
DISK_QUOTA quota
```

### Grammar Syntax[¶](#id22)

```
CREATE TABLE [ IF NOT EXISTS ] [[database.]schema.]table
  LIKE [[database.]schema.]existing-table
  [ {INCLUDING | EXCLUDING} PROJECTIONS ]
  [ {INCLUDE | EXCLUDE} [SCHEMA] PRIVILEGES ]
  [ DISK_QUOTA quota ]
```

### Tables Options[¶](#id23)

#### Projections[¶](#projections)

This syntax isn’t required in Snowflake and is removed from the original code. For more information,
please refer to [**Projections Clauses**](#projections-clauses).

Warning

This syntax is not required in Snowflake.

#### Inherited Schema Privileges Clause[¶](#id24)

`INCLUDE SCHEMA PRIVILEGES` is a Vertica-specific feature that governs how privileges are inherited,
in this case, potentially from the schema level. Snowflake does not have a direct equivalent for
this clause within its `CREATE TABLE` syntax. For more information please refer to
[Inherited Schema Privileges Clause.](#inherited-schema-privileges-clause)

Warning

This syntax is not supported in Snowflake.

### Related EWIs[¶](#id25)

1. [SSC-EWI-VT0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI#ssc-ewi-vt0001):
   Inherited privileges clause is not supported in Snowflake.
