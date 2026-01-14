---
description:
  User-defined data types use Oracle built-in data types and other user-defined data types as the
  building blocks of object types that model the structure and behavior of data in applications. The
  secti
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/data-types/user-defined-types
title: SnowConvert AI - Oracle - User-Defined Types | Snowflake Documentation
---

## Description[¶](#description)

> User-defined data types use Oracle built-in data types and other user-defined data types as the
> building blocks of object types that model the structure and behavior of data in applications. The
> sections that follow describe the various categories of user-defined types.
> ([Oracle SQL Language Reference User-defined Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-7CF27C66-9908-4C02-9401-06C2F2C4021C))

Warning

Snowflake does not have any support for User-defined Types. This page is meant to be a summary of
Oracle’s features. For the current status of User-defined Types in the SnowConvert AI tool please
refer to the [Create Type Statement Page](../../sql-translation-reference/create_type) and its
subpages.

## Object Types[¶](#object-types)

**Note:**

SnowConvert AI offers partial translation for Object Types, for more information on this, please
refer to the next section:
[Object type definition](../../sql-translation-reference/create_type.html#object-type-definition)

## REF Data Types[¶](#ref-data-types)

Danger

Ref Data Types are not recognized by SnowConvert AI, and are instead shown as unrecognized
“User-defined Functions”. For more information about them, please read the
[REF Data Types subpage](#ref-data-types).

> An object identifier (represented by the keyword `OID`) uniquely identifies an object and enables
> you to reference the object from other objects or from relational tables. A data type category
> called `REF` represents such references. A `REF` data type is a container for an object
> identifier. `REF` values are pointers to objects.
> ([Oracle SQL Language Reference REF Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-C9818949-BB51-4EB1-9A6D-2BE1F53B105D))

## Varrays[¶](#varrays)

Warning

SnowConvert AI only recognizes these elements but does not offer any translation for them, for more
information on this, please refer to the next section:
[Array type definition](../../sql-translation-reference/create_type.html#array-type-definition)

## Nested Tables[¶](#nested-tables)

Warning

SnowConvert AI only recognizes these elements but does not offer any translation for them since
there are no known workarounds for them, for more information on this, please refer to the next
section:[Nested table type definition](../../sql-translation-reference/create_type.html#nested-table-type-definition)

## Known Issues[¶](#known-issues)

### 1. DML usages for Object Types are not being transformed[¶](#dml-usages-for-object-types-are-not-being-transformed)

As of now, only DDL definitions that use User-Defined Types are being transformed into Variant. This
means that any Inserts, Updates or Deletes using User-defined Types are not being transformed and
need to be manually transformed. There is no EWI for this but there is a work item to add this
corresponding EWI.

#### 2. Nested Table types are not being transformed[¶](#nested-table-types-are-not-being-transformed)

There is no known workaround for implementing Nested Tables, for this reason SnowConvert AI only
offers recognition of these elements.

#### 3. Array types are not being transformed[¶](#array-types-are-not-being-transformed)

For now SnowConvert AI only recognizes these elements. A known workaround exists and there is a work
item to implement them.

#### 4. REF Data Types are not supported by SnowConvert AI, but there is no EWI related to them[¶](#ref-data-types-are-not-supported-by-snowconvert-ai-but-there-is-no-ewi-related-to-them)

They are not supported, and instead are reported as an unknown User-Defined Function, but there is a
work item to add this corresponding EWI.

## Related EWIs[¶](#related-ewis)

No related EWIs.

## REF Data Types[¶](#id1)

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id2)

> An object identifier (represented by the keyword `OID`) uniquely identifies an object and enables
> you to reference the object from other objects or relational tables. A data type category called
> `REF` represents such references. A `REF` data type is a container for an object identifier. `REF`
> values are pointers to objects.
> ([Oracle SQL Language Reference REF Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-C9818949-BB51-4EB1-9A6D-2BE1F53B105D))

REF Data types are not supported in Snowflake, and there is no current workaround to implement a
similar component.

As of now, they are currently being recognized as user-defined functions and “DANGLING” clauses are
not being recognized. Finally, the OID clause in view is being removed, as there is no workaround
for them.

```
CREATE VIEW generic_view AS
SELECT REF(type) AS ref_col, MAKE_REF(type, identifier_column) AS make_ref_col
FROM generic_table;

SELECT v.ref_col, v.make_ref_col
FROM generic_view v
WHERE v.ref_col IS NOT DANGLING AND v.make_ref_col IS NOT DANGLING
```

### Sample Source Patterns[¶](#sample-source-patterns)

#### Types and Tables for References[¶](#types-and-tables-for-references)

Please consider the following types, tables, inserts and view. They will be used for the next
pattern section.

##### Oracle[¶](#oracle)

```
CREATE TYPE email_typ_demo AS OBJECT
	( email_id INTEGER
	, email VARCHAR2(30)
	);

CREATE TYPE customer_typ_demo AS OBJECT
    ( customer_id        INTEGER
    , cust_first_name    VARCHAR2(20)
    , cust_last_name     VARCHAR2(20)
    , email_id			 INTEGER
    ) ;

CREATE TABLE email_table_demo OF email_typ_demo;
CREATE TABLE customer_table_demo OF customer_typ_demo;

INSERT INTO customer_table_demo VALUES
(customer_typ_demo(1, 'First Name 1', 'Last Name 1', 1));

INSERT INTO customer_table_demo VALUES
(customer_typ_demo(2, 'First Name 2', 'Last Name 2', 2));

INSERT INTO email_table_demo VALUES
(email_typ_demo(1, 'abc@def.com'));

CREATE VIEW email_object_view OF email_typ_demo WITH OBJECT IDENTIFIER (email_id) AS
SELECT * FROM email_table_demo;
```

#### Selects and Views using REFs[¶](#selects-and-views-using-refs)

##### Oracle[¶](#id3)

```
CREATE VIEW email_object_view OF email_typ_demo WITH OBJECT IDENTIFIER (email_id) AS
SELECT * FROM email_table_demo;

CREATE VIEW customer_view AS
SELECT REF(ctb) AS customer_reference
     , MAKE_REF(email_object_view, ctb.email_id) AS email_ref
FROM customer_table_demo ctb;

SELECT c.customer_reference.cust_first_name, c.email_ref.email
FROM customer_view c;

SELECT c.customer_reference.cust_first_name, c.email_ref.email
FROM customer_view c
WHERE c.email_ref IS NOT DANGLING;
```

##### Result with danglings[¶](#result-with-danglings)

<!-- prettier-ignore -->
|CUSTOMER_REFERENCE.CUST_FIRST_NAME|EMAIL_REF.EMAIL|
|---|---|
|First Name 1|abc@def.com|
|First Name 2||

##### Result with no danglings[¶](#result-with-no-danglings)

<!-- prettier-ignore -->
|CUSTOMER_REFERENCE.CUST_FIRST_NAME|EMAIL_REF.EMAIL|
|---|---|
|First Name 1|abc@def.com|

##### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE VIEW email_object_view
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT * FROM
     email_table_demo;

CREATE OR REPLACE VIEW customer_view
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
AS
SELECT REF(ctb) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'REF' NODE ***/!!! AS customer_reference
     , MAKE_REF(email_object_view, ctb.email_id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'MAKE_REF' NODE ***/!!! AS email_ref
FROM
     customer_table_demo ctb;

     SELECT c.customer_reference.cust_first_name, c.email_ref.email
     FROM
     customer_view c;

     SELECT c.customer_reference.cust_first_name, c.email_ref.email
FROM
     customer_view c
WHERE c.email_ref;
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '14' COLUMN '19' OF THE SOURCE CODE STARTING AT 'IS'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS ';' ON LINE '10' COLUMN '21'. FAILED TOKEN WAS 'IS' ON LINE '14' COLUMN '19'. CODE '94'. **
--                   IS NOT DANGLING
```

### Known Issues[¶](#id4)

**1. REF and MAKE_REF are not being recognized**

Instead they are currently being marked as user-defined functions.

**2. DANGLING clause is not being recognized**

DANGLING clauses are causing parsing errors when running SnowConvert.

#### 3. OID Clauses in view are not supported by SnowConvert AI, but there is no EWI related to them[¶](#oid-clauses-in-view-are-not-supported-by-snowconvert-ai-but-there-is-no-ewi-related-to-them)

The OID clause is not supported by either SnowConvert AI, nor Snowflake but there should be an EWI
related to them.

### Related EWIs[¶](#id5)

1. [SSC-EWI-0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0001):
   Unrecognized token on the line of the source code.
2. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
3. [SSC-FDM-0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0001):
   Views selecting all columns from a single table are not required in Snowflake.
