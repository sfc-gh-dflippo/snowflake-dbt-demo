---
description:
  This is a translation reference to convert Oracle Create Type Statements (UDT’s) to snowflake
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/sql-translation-reference/create_type
title: SnowConvert AI - Oracle - Create Type | Snowflake Documentation
---

## General Description[¶](#general-description)

One of the most important features the Oracle database engine offers is an Object-Oriented approach.
PL/SQL offers capabilities beyond other relational databases in the form of OOP by using Java-like
statements in the form of packages, functions, tables and types. This document will cover the last
one and how SnowConvert AI solves it, remaining compliant to functionality.

Oracle supports the following specifications:

- Abstract Data Type (_ADT_) (_including an SQLJ object type_).
- Standalone varying array (_varray_) type.
- Standalone nested table type.
- Incomplete object type.

All this according to the information found in
[Oracle Create Type Statement Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/CREATE-TYPE-statement.html#GUID-389D603D-FBD0-452A-8414-240BBBC57034)

```
CREATE [ OR REPLACE ] [ EDITIONABLE | NONEDITIONAL ] TYPE <type name>
[ <type source creation options> ]
[<type definition>]
[ <type properties> ]
```

Copy

## Limitations[¶](#limitations)

Snowflake doesn’t support user-defined data types, according to its online documentation
[Unsupported Data Types](https://docs.snowflake.com/en/sql-reference/data-types-unsupported.html),
but it supports
[Semi-structured Data Types](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html),
which can be used to mimic the hierarchy-like structure of most User-defined types. For this reason,
there are multiple type features that have no workaround.

Following are the User Defined Types features for which **NO** workaround is proposed:

### Subtypes: Type Hierarchy[¶](#subtypes-type-hierarchy)

These statements aren’t supported in Snowflake. SnowConvert AI only recognizes them, but no
translation is offered.

```
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn NUMBER)
   NOT FINAL;
/

CREATE TYPE employee_t UNDER person_t
   (department_id NUMBER, salary NUMBER)
   NOT FINAL;
/

CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs NUMBER);
/
```

Copy

### Type properties[¶](#type-properties)

These refer to the options that are normally used when using OOP in PL/SQL: Persistable,
Instantiable and Final.

```
CREATE OR REPLACE TYPE type1 AS OBJECT () NOT FINAL NOT INSTANTIABLE NOT PERSISTABLE;
CREATE OR REPLACE TYPE type2 AS OBJECT () FINAL INSTANTIABLE PERSISTABLE;
```

Copy

### Nested Table Type[¶](#nested-table-type)

These statements aren’t supported in Snowflake. SnowConvert AI only recognizes them, but no
translation is offered.

```
CREATE TYPE textdoc_typ AS OBJECT
    ( document_typ      VARCHAR2(32)
    , formatted_doc     BLOB
    ) ;
/

CREATE TYPE textdoc_tab AS TABLE OF textdoc_typ;
/
```

Copy

### Type Source Creation Options[¶](#type-source-creation-options)

These options stand for custom options regarding access and querying the type.

```
CREATE TYPE type1 FORCE OID 'abc' SHARING = METADATA DEFAULT COLLATION schema1.collation ACCESSIBLE BY (schema1.unitaccesor) AS OBJECT ();
CREATE TYPE type2 FORCE OID 'abc' SHARING = NONE DEFAULT COLLATION collation ACCESSIBLE BY (PROCEDURE unitaccesor) AS OBJECT ();
CREATE TYPE type3 AUTHID CURRENT_USER AS OBJECT ();
CREATE TYPE type4 AUTHID DEFINER AS OBJECT ();
```

Copy

## Proposed workarounds[¶](#proposed-workarounds)

### About types definition[¶](#about-types-definition)

For the definition, the proposed workaround is to create semi-structure data type to mimic Oracle’s
data type.

### About types member function[¶](#about-types-member-function)

For the member functions containing logic and DML, the proposed workaround relies on helpers to
translate this into stored procedures.

## Current SnowConvert AI Support[¶](#current-snowconvert-ai-support)

The next table shows a summary of the current support provided by the SnowConvert AI tool. Please
keep into account that translations may still not be final, and more work may be needed.

<!-- prettier-ignore -->
|Type Statement Element|Current recognition status|Current translation status|Has Known Workarounds|
|---|---|---|---|
|[Object Type Definitions](#object-type-definition)|Recognized.|Partially Translated.|Yes.|
|[Subtype Definitions](#subtype-definition)|Recognized.|Not Translated.|No.|
|[Array Type Definitions](#array-type-definition)|Recognized.|Not Translated.|Yes.|
|[Nested Table Definitions](#nested-table-type)|Recognized.|Not Translated.|No.|
|[Member Function Definitions](#member-function-definitions)|Recognized.|Not Translated.|Yes.|

## Known Issues[¶](#known-issues)

### 1. DML usages for Object Types are not being transformed[¶](#dml-usages-for-object-types-are-not-being-transformed)

As of now, only DDL definitions that use User-Defined Types are being transformed into Variant. This
means that any Inserts, Updates or Deletes using User-defined Types are not being transformed and
need to be manually transformed. There is no EWI for this but there is a work item to add this
corresponding EWI.

#### 2. Create Type creation options are not supported[¶](#create-type-creation-options-are-not-supported)

Currently, there is no known workaround for any of the creation options, for these reasons they are
not taken into account when defining the type.

## Related EWIs[¶](#related-ewis)

No related EWIs.

## Array Type Definition[¶](#array-type-definition)

This is a translation reference to convert the Array Variant of the Oracle Create Type Statements
(UDT’s) to Snowflake

Danger

SnowConvert AI only recognizes these definitions and for the moment does not support any translation
for them. This page is only used as a future reference for translations.

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#description)

Array Types define an array structure of a previously existing datatype (including other Custom
Types).

For the translation of array types, the type definition is replaced by a
[Semi-structured Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html)
and then it is expanded on any usages across the code. This means taking type’s definition and then
expanding it on the original code.

```
CREATE TYPE <type name>
AS { VARRAY | [VARYING] ARRAY } ( <size limit> ) OF <data type>
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns)

#### Inserts for the array usage[¶](#inserts-for-the-array-usage)

The next data will be inserted inside the table before querying the select. Please note these
Inserts currently need to be manually migrated into Snowflake.

##### Oracle[¶](#oracle)

```
INSERT INTO customer_table_demo(customer_table_id, customer_data) VALUES
(1, phone_list_typ_demo('2000-0000', '4000-0000', '0000-0000'));

INSERT INTO customer_table_demo(customer_table_id, customer_data) VALUES
(1, phone_list_typ_demo('8000-2000', '0000-0000', '5000-0000'));
```

Copy

##### Snowflake[¶](#snowflake)

```
INSERT INTO customer_table_demo(customer_table_id, customer_data)
SELECT 1, ARRAY_CONSTRUCT('2000-0000', '4000-0000', '0000-0000');

INSERT INTO customer_table_demo(customer_table_id, customer_data)
SELECT 1, ARRAY_CONSTRUCT('8000-2000', '0000-0000', '5000-0000');
```

Copy

#### Array Type usage[¶](#array-type-usage)

##### Oracle[¶](#id1)

```
CREATE TYPE phone_list_typ_demo AS VARRAY(3) OF VARCHAR2(25);
/

CREATE TABLE customer_table_demo (
    customer_table_id INTEGER,
    customer_data phone_list_typ_demo
);
/

SELECT * FROM customer_table_demo;
/
```

Copy

##### Results[¶](#results)

<!-- prettier-ignore -->
|CUSTOMER_TABLE_ID|CUSTOMER_DATA|
|---|---|
|1|[[‘2000-0000’,’4000-0000’,’0000-0000’]]|
|1|[[‘8000-2000’,’0000-0000’,’5000-0000’]]|

##### Snowflake[¶](#id2)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'VARYING ARRAY' NODE ***/!!!
CREATE TYPE phone_list_typ_demo AS VARRAY(3) OF VARCHAR2(25);

CREATE OR REPLACE TABLE customer_table_demo (
        customer_table_id INTEGER,
        customer_data VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'phone_list_typ_demo' USAGE CHANGED TO VARIANT ***/!!!
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE VIEW PUBLIC.customer_table_demo_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
        customer_table_id,
        customer_data
FROM
        customer_table_demo;

    SELECT * FROM
        customer_table_demo_view;
```

Copy

##### Results[¶](#id3)

<!-- prettier-ignore -->
|CUSTOMER_TABLE_ID|CUSTOMER_DATA|
|---|---|
|1|[[‘2000-0000’, ‘4000-0000’, ‘0000-0000’]]|
|1|[[‘8000-2000’, ‘0000-0000’, ‘5000-0000’]]|

### Known Issues[¶](#id4)

#### 1. Create Type creation options are not supported[¶](#id5)

Currently, there is no known workaround for any of the creation options, for these reasons they are
not taken into account when defining the type.

##### 2. Migrated code output is not functional[¶](#migrated-code-output-is-not-functional)

The statements are being changed unnecessarily, which makes them no longer be functional on the
output code. This will be addressed when a proper transformation for them is in place.

### Related EWIs[¶](#id6)

1. [SSC-EWI-0062](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0062):
   Custom type usage changed to variant.
2. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Member Function Definitions[¶](#member-function-definitions)

This is a translation reference to convert the Member Functions of the Oracle Create Type Statements
(UDT’s) to Snowflake

Danger

SnowConvert AI still does not recognize type member functions nor type body definitions. This page
is only used as a future reference for translation.

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id7)

Like other Class definitions, Oracle’s TYPE can implement methods to expose behaviors based on its
attributes. MEMBER FUCTION will be transformed to Snowflake’s Stored Procedures, to maintain
functional equivalence due to limitations.

Since functions are being transformed into procedures, the
[transformation reference for PL/SQL](../pl-sql-to-snowflake-scripting/README) also applies here.

### Sample Source Patterns[¶](#id8)

#### Inserts for Simple square() member function[¶](#inserts-for-simple-square-member-function)

The next data will be inserted inside the table before querying the select. Please note these
Inserts currently need to be manually migrated into Snowflake.

##### Oracle[¶](#id9)

```
INSERT INTO table_member_function_demo(column1) VALUES
(type_member_function_demo(5));
```

Copy

##### Snowflake[¶](#id10)

```
INSERT INTO table_member_function_demo (column1)
SELECT OBJECT_CONSTRUCT('a1', 5);
```

Copy

#### Simple square() member function[¶](#simple-square-member-function)

##### Oracle[¶](#id11)

```
-- TYPE DECLARATION
CREATE TYPE type_member_function_demo AS OBJECT (
    a1 NUMBER,
    MEMBER FUNCTION get_square RETURN NUMBER
);
/

-- TYPE BODY DECLARATION
CREATE TYPE BODY type_member_function_demo IS
   MEMBER FUNCTION get_square
   RETURN NUMBER
   IS x NUMBER;
   BEGIN
      SELECT c.column1.a1*c.column1.a1 INTO x
      FROM table_member_function_demo c;
      RETURN (x);
   END;
END;
/

-- TABLE
CREATE TABLE table_member_function_demo (column1 type_member_function_demo);
/

-- QUERYING DATA
SELECT
    t.column1.get_square()
FROM
    table_member_function_demo t;
/
```

Copy

##### Results[¶](#id12)

<!-- prettier-ignore -->
|T.COLUMN1.GET_SQUARE()|
|---|
|25|

##### Snowflake[¶](#id13)

```
-- TYPE DECLARATION
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE type_member_function_demo AS OBJECT (
    a1 NUMBER,
    MEMBER FUNCTION get_square RETURN NUMBER
)
;

---- TYPE BODY DECLARATION
--!!!RESOLVE EWI!!! /*** SSC-EWI-OR0007 - CREATE TYPE WITHOUT BODY IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
--CREATE TYPE BODY type_member_function_demo IS
--   MEMBER FUNCTION get_square
--   RETURN NUMBER
--   IS x NUMBER;
--   BEGIN
--      SELECT c.column1.a1*c.column1.a1 INTO x
--      FROM table_member_function_demo c;
--      RETURN (x);
--   END;
--END
   ;

-- TABLE
CREATE OR REPLACE TABLE table_member_function_demo (column1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'type_member_function_demo' USAGE CHANGED TO VARIANT ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE VIEW PUBLIC.table_member_function_demo_view
<strong>COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
</strong><strong>AS
</strong>SELECT
    column1:a1 :: NUMBER AS a1
FROM
    table_member_function_demo;

-- QUERYING DATA
SELECT
    t.column1.get_square() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 't.column1.get_square' NODE ***/!!!
FROM
    table_member_function_demo t;
```

Copy

##### Results[¶](#id14)

<!-- prettier-ignore -->
|GET_SQUARE()|
|---|
|25|

### Known Issues[¶](#id15)

No Known issues.

### Related EWIs[¶](#id16)

1. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056):
   Create Type Not Supported.
2. [SSC-EWI-0062](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0062):
   Custom type usage changed to variant.
3. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review.
4. [SSC-EWI-OR0007](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0007):
   Create Type Not Supported in Snowflake

## Nested Table Type Definition[¶](#nested-table-type-definition)

This is a translation reference to convert the Nested Table Variant of the Oracle Create Type
Statements (UDT’s) to Snowflake

Danger

SnowConvert AI only recognizes these definitions, does not support any translation and there is no
known workaround for them.

### Description[¶](#id17)

Nested Table Types define an embedded table structure of a previously existing datatype (including
other Custom Types). They can be used as a more powerful version of the
[Array Type](#array-type-definition).

Unlike any of the other types, there is still no known workaround or any possible translation for
them.

```
CREATE TYPE <type name> AS TABLE OF <data type>
```

Copy

### Sample Source Patterns[¶](#id18)

#### Nested Table Type usage[¶](#nested-table-type-usage)

##### Oracle[¶](#id19)

```
CREATE TYPE textdoc_typ AS OBJECT (
    document_typ VARCHAR2(32),
    formatted_doc BLOB
);
/

CREATE TYPE textdoc_tab AS TABLE OF textdoc_typ;
/
```

Copy

##### Snowflake[¶](#id20)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE textdoc_typ AS OBJECT (
    document_typ VARCHAR2(32),
    formatted_doc BLOB
)
;

!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NESTED TABLE' NODE ***/!!!

CREATE TYPE textdoc_tab AS TABLE OF textdoc_typ;
```

Copy

### Known Issues[¶](#id21)

#### 1. Create Type creation options are not supported[¶](#id22)

Currently, there is no known workaround for any of the creation options; for these reasons, they are
not taken into account when defining the type.

### Related EWIs[¶](#id23)

1. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review
2. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056):
   Create Type Not Supported.

## Object Type Definition[¶](#object-type-definition)

This is a translation reference to convert the Object Variant of the Oracle Create Type Statements
(UDT’s) to Snowflake

Note

SnowConvert AI supports a translation for Object Type Definitions itself. However, their usages are
still a work in progress.

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id24)

Object Types define a structure of data similar to a record, with the added advantages of the member
function definitions. Meaning that their data may be used along some behavior within the type.

For the translation of object types, the type definition is replaced by a
[Semi-structured Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html)
and then it is expanded on any usages across the code. For tables this means replacing the column
for a Variant, adding a View so that selects (and also Views) to the original table can still
function.

```
CREATE TYPE <type name> AS OBJECT
( [{<type column definition> | type method definition } , ...]);
```

Copy

### Sample Source Patterns[¶](#id25)

#### Inserts for Simple Type usage[¶](#inserts-for-simple-type-usage)

The next data will be inserted inside the table before querying the select. Please note these
Inserts currently need to be manually migrated into Snowflake.

##### Oracle[¶](#id26)

```
INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 1, customer_typ_demo(1, 'First Name 1', 'Last Name 1'));

INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 2, customer_typ_demo(2, 'First Name 2', 'Last Name 2'));
```

Copy

##### Snowflake[¶](#id27)

```
INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 1, customer_typ_demo(1, 'First Name 1', 'Last Name 1') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);

INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 2, customer_typ_demo(2, 'First Name 2', 'Last Name 2') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);
```

Copy

#### Simple Type usage[¶](#simple-type-usage)

##### Oracle[¶](#id28)

```
CREATE TYPE customer_typ_demo AS OBJECT (
    customer_id INTEGER,
    cust_first_name VARCHAR2(20),
    cust_last_name VARCHAR2(20)
);

CREATE TABLE customer_table_demo (
    customer_table_id INTEGER,
    customer_data customer_typ_demo
);

SELECT * FROM customer_table_demo;
```

Copy

##### Results[¶](#id29)

<!-- prettier-ignore -->
|CUSTOMER_TABLE_ID|CUSTOMER_DATA|
|---|---|
|1|[1, First Name 1, Last Name 1]|
|2|[2, First Name 2, Last Name 2]|

##### Snowflake[¶](#id30)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE customer_typ_demo AS OBJECT (
    customer_id INTEGER,
    cust_first_name VARCHAR2(20),
    cust_last_name VARCHAR2(20)
)
;

CREATE OR REPLACE TABLE customer_table_demo (
        customer_table_id INTEGER,
        customer_data VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'customer_typ_demo' USAGE CHANGED TO VARIANT ***/!!!
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

CREATE OR REPLACE VIEW PUBLIC.customer_table_demo_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
        customer_table_id,
        customer_data:customer_id :: INTEGER AS customer_id,
        customer_data:cust_first_name :: VARCHAR AS cust_first_name,
        customer_data:cust_last_name :: VARCHAR AS cust_last_name
FROM
        customer_table_demo;

    SELECT * FROM
        customer_table_demo_view;
```

Copy

##### Results[¶](#id31)

<!-- prettier-ignore -->
|CUSTOMER_TABLE_ID|CUST_ID|CUST_FIRST_NAME|CUST_LAST_NAME|
|---|---|---|---|
|1|1|First Name 1|Last Name 1|
|2|2|First Name 2|Last Name 2|

#### Inserts for Nested Type Usage[¶](#inserts-for-nested-type-usage)

These statements need to be placed between the table creation and the select statement to test the
output.

##### Oracle[¶](#id32)

```
INSERT INTO customer_table_demo(customer_id, customer_data) values
(1, customer_typ_demo('Customer 1', email_typ_demo('email@domain.com')));

INSERT INTO customer_table_demo(customer_id, customer_data) values
(2, customer_typ_demo('Customer 2', email_typ_demo('email2@domain.com')));
```

Copy

##### Snowflake[¶](#id33)

```
INSERT INTO customer_table_demo(customer_id, customer_data) values
(1, customer_typ_demo('Customer 1', email_typ_demo('email@domain.com') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'email_typ_demo' NODE ***/!!!) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);

INSERT INTO customer_table_demo(customer_id, customer_data) values
(2, customer_typ_demo('Customer 2', email_typ_demo('email2@domain.com') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'email_typ_demo' NODE ***/!!!) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);
```

Copy

#### Nested Type Usage[¶](#nested-type-usage)

##### Oracle[¶](#id34)

```
CREATE TYPE email_typ_demo AS OBJECT (email VARCHAR2(20));

CREATE TYPE customer_typ_demo AS OBJECT (
    cust_name VARCHAR2(20),
    cust_email email_typ_demo
);

CREATE TABLE customer_table_demo (
    customer_id INTEGER,
    customer_data customer_typ_demo
);

SELECT * FROM customer_table_demo;
```

Copy

##### Results[¶](#id35)

<!-- prettier-ignore -->
|CUSTOMER_ID|CUSTOMER_DATA|
|---|---|
|1|[Customer 1, [email@domain.com]]|
|2|[Customer 2, [email2@domain.com]]|

##### Snowflake[¶](#id36)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE email_typ_demo AS OBJECT (email VARCHAR2(20))
;

!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!

CREATE TYPE customer_typ_demo AS OBJECT (
    cust_name VARCHAR2(20),
    cust_email email_typ_demo
)
;

CREATE OR REPLACE TABLE customer_table_demo (
    customer_id INTEGER,
    customer_data VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'customer_typ_demo' USAGE CHANGED TO VARIANT ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

CREATE OR REPLACE VIEW PUBLIC.customer_table_demo_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
    customer_id,
    customer_data:cust_name :: VARCHAR AS cust_name,
    customer_data:cust_email:email :: VARCHAR AS email
FROM
    customer_table_demo;

SELECT * FROM
    customer_table_demo_view;
```

Copy

##### Results[¶](#id37)

<!-- prettier-ignore -->
|CUSTOMER_ID|CUST_NAME|CUST_EMAIL|
|---|---|---|
|1|Customer 1|email@domain.com|
|2|Customer 2|email2@domain.com|

### Known Issues[¶](#id38)

#### 1. Migrated code output is not the same[¶](#migrated-code-output-is-not-the-same)

The view statement is being changed unnecessarily, which makes the table no longer have the same
behavior in the output code. There is a work item to fix this issue.

##### 2. DML for User-defined Types is not being transformed[¶](#dml-for-user-defined-types-is-not-being-transformed)

DML that interacts with elements that have User-defined types within them (like a table) are not
being transformed. There is a work item to implement this in the future.

##### 3. Create Type creation options are not supported[¶](#id39)

Currently, there is no known workaround for any of the creation options, for these reasons they are
not taken into account when defining the type.

### Related EWIs[¶](#id40)

1. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056):
   Create Type Not Supported.
2. [SSC-EWI-0062](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0062):
   Custom type usage changed to variant.
3. [SSC-EWI-0073](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Subtype Definition[¶](#subtype-definition)

This is a translation reference to convert the Subtype Variant of the Oracle Create Type Statements
(UDT’s) to Snowflake

Danger

Since there are no known workarounds, SnowConvert AI only recognizes these definitions and does not
support any translation for them.

### Description[¶](#id41)

Subtypes define a structure of data similar to a record, with the added advantages of the member
function definitions. Meaning that their data may be used along some behavior within the type.
Unlike Object Types, Subtypes are built as an extension to another existing type.

Regarding subtype definitions, there is still no translation, but there might be a way to
reimplement them using [Object Type Definitions](#object-type-definition) and then using their
respective translation.

```
CREATE TYPE <type name> UNDER <super type name>
( [{<type column definition> | type method definition } , ...]);
```

Copy

### Sample Source Patterns[¶](#id42)

#### Subtypes under an Object Type[¶](#subtypes-under-an-object-type)

##### Oracle[¶](#id43)

```
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn INTEGER)
   NOT FINAL;
/

CREATE TYPE employee_t UNDER person_t
   (department_id INTEGER, salary INTEGER)
   NOT FINAL;
/

CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs INTEGER);
/
```

Copy

##### Snowflake[¶](#id44)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn INTEGER)
   NOT FINAL;

--!!!RESOLVE EWI!!! /*** SSC-EWI-OR0007 - CREATE TYPE SUBTYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!

--CREATE TYPE employee_t UNDER person_t
--   (department_id INTEGER, salary INTEGER)
--   NOT FINAL
            ;

--!!!RESOLVE EWI!!! /*** SSC-EWI-OR0007 - CREATE TYPE SUBTYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!

--CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs INTEGER)
                                                              ;
```

Copy

### Known Issues[¶](#id45)

#### 1. Create Type creation options are not supported[¶](#id46)

Currently, there is no known workaround for any of the creation options, for these reasons they are
not taken into account when defining the type.

### Related EWIs[¶](#id47)

1. [SSC-EWI-0056](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0056):
   Create Type Not Supported.
2. [SSC-EWI-OR0007](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0007):
   Create Type Not Supported in Snowflake.
