---
description: Translation reference to convert Oracle COLLECTIONS and RECORDS to Snowflake Scripting
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/collections-and-records
title: SnowConvert AI - Oracle - COLLECTIONS AND RECORDS | Snowflake Documentation
---

## General Description

> PL/SQL lets you define two kinds of composite data types: collection and record, where composite
> is a data type that stores values that have internal components.
>
> In a collection, the internal components always have the same data type, and are called elements.
>
> In a record, the internal components can have different data types, and are called fields.
> ([Oracle PL/SQL Language Reference COLLECTIONS AND RECORDS](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/plsql-collections-and-records.html#GUID-7115C8B6-62F9-496D-BEC3-F7441DFE148A))

### Note

Please take into account the
[CREATE TYPE statement translation reference](../sql-translation-reference/create_type) since some
workarounds can overlap and may be functional in both scenarios.

## Limitations

Snowflake doesn’t support user-defined data types, which includes PL Collections and Records,
according to its online documentation
[Unsupported Data Types](https://docs.snowflake.com/en/sql-reference/data-types-unsupported.html),
but it supports
[Semi-structured Data Types](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html),
which can be used to mimic both the hierarchy-like structure of Record and the element structure of
Collection User-defined types. For this reason, there are multiple types of features that have no
workaround.

Following are the features for which **NO** workaround is proposed:

### Variable size cannot exceed 16MB

Snowflake sets VARIANT, OBJECT, and ARRAY’s maximum size on 16MBs. This means that if a Record, a
Collection, or any element of either exceeds this size it will cause a Runtime Error.

### Varray capacity cannot be limited

Oracle’s varrays offer the capacity to limit the number of elements within them. This is not
supported by Snowflake.

## Proposed Workaround

### About Record types definition

The proposed workaround is to use an “OBJECT” semi-structured data type to mimic Oracle’s data type.

### About Collection types definition

There are two different workarounds that depend on the type of collection to be migrated:

- Associative Arrays are proposed to be changed into an “OBJECT” semi-structured data type.
- Varrays and Nested Table Arrays are proposed to be changed into an “ARRAY” semi-structured data
  type.

## Current SnowConvert AI Support

The next table shows a summary of the current support provided by the SnowConvert AI tool. Please
keep into account that translations may still not be final, and more work may be needed.

<!-- prettier-ignore -->
|Sub-Feature|Current recognition status|Current translation status|Has Known Workarounds|
|---|---|---|---|
|[Record Type Definitions](#record-type-definition)|Recognized.|Not Translated.|Yes.|
|[Associative Array Type Definitions](#associative-array-type-definition)|Not Recognized.|Not Translated.|Yes.|
|[Varray Type Definitions](#varray-type-definition)|Recognized.|Not Translated.|Yes.|
|[Nested Table Array Type Definitions](#nested-table-array-type-definition)|Recognized.|Not Translated.|Yes.|

## Known Issues

### 1. Associate Arrays are considered a Nested Table

As of now, SnowConvert AI doesn’t differentiate between an Associative Array and a Nested Table
meaning they are mixed up in the same assessment counts.

## Related EWIs

No related EWIs.

## Associative Array Type Definition

This is a translation reference to convert the Oracle Associative Array Declaration to Snowflake

Warning

This section is a work in progress, information may change in the future.

### Note 2

Some parts in the output code are omitted for clarity reasons.

### Description

> An associative array (formerly called PL/SQL table or index-by table) is a set of key-value pairs.
> Each key is a unique index, used to locate the associated value with the syntax
> `variable_name(index)`.
>
> The data type of `index` can be either a string type (`VARCHAR2`, `VARCHAR`, `STRING`, or `LONG`)
> or `PLS_INTEGER`. Indexes are stored in sort order, not creation order. For string types, sort
> order is determined by the initialization parameters `NLS_SORT` and `NLS_COMP`.
>
> ([Oracle PL/SQL Language Reference ASSOCIATIVE ARRAYS](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/plsql-collections-and-records.html#GUID-8060F01F-B53B-48D4-9239-7EA8461C2170))

Warning

Not to be confused with the
[PL/SQL NESTED TABLE Type definition](#nested-table-array-type-definition).

For the translation, the type definition is replaced by an OBJECT
[Semi-structured Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html)
and then its usages are changed accordingly across any operations.

In order to define an Associative Array type, the syntax is as follows:

```sql
type_definition := TYPE IS TABLE OF datatype INDEX BY indexing_datatype;

indexing_datatype := { PLS_INTEGER
                     | BINARY_INTEGER
                     | string_datatype
                     }
```

To declare a variable of this type:

```sql
variable_name collection_type;
```

### Sample Source Patterns

#### Varchar-indexed Associative Array

##### Oracle

```sql
CREATE OR REPLACE PROCEDURE associative_array
IS
    TYPE associate_array_typ IS TABLE OF INTEGER
        INDEX BY VARCHAR2(50);

    associate_array associate_array_typ := associate_array_typ();
    associate_index VARCHAR2(50);
BEGIN
    associate_array('abc') := 1;
    associate_array('bca') := 2;
    associate_array('def') := 3;

    DBMS_OUTPUT.PUT_LINE(associate_array('abc'));
    associate_array('abc') := 4;
    --THROWS 'NO DATA FOUND'
    --DBMS_OUTPUT.PUT_LINE(associate_array('no exists'));

    DBMS_OUTPUT.PUT_LINE(associate_array.COUNT);

    associate_index := associate_array.FIRST;
    WHILE associate_index IS NOT NULL
    LOOP
        DBMS_OUTPUT.PUT_LINE(associate_array(associate_index));
        associate_index := associate_array.NEXT(associate_index);
    END LOOP;
END;

CALL associative_array();
```

##### Result

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|1|
|3|
|4|
|2|
|3|

##### Snowflake

Please note the ‘true’ parameter in the OBJECT_INSERT. This is so that the element is updated if it
is already present in the array.

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.associative_array ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
      associate_array OBJECT := OBJECT_CONSTRUCT();
      associate_index VARCHAR(50);
   BEGIN
      associate_array := OBJECT_INSERT(associate_array, 'abc', 1, true);
      associate_array := OBJECT_INSERT(associate_array, 'bca', 2, true);
      associate_array := OBJECT_INSERT(associate_array, 'def', 3, true);

      CALL DBMS_OUTPUT.PUT_LINE(:associate_array['abc']);
      CALL DBMS_OUTPUT.PUT_LINE(:associate_array['not found']);

      associate_array := OBJECT_INSERT(:associate_array, 'abc', 4, true);

      CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(OBJECT_KEYS(:associate_array)));

      FOR i IN 1 TO ARRAY_SIZE(OBJECT_KEYS(:associate_array))
      LOOP
         associate_index := OBJECT_KEYS(:associate_array)[:i-1];
         CALL DBMS_OUTPUT.PUT_LINE(:associate_array[:associate_index]);
      END LOOP;
   END;
$$;

CALL PUBLIC.associative_array();
SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG;
```

##### Result 2

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|1|
|3|
|4|
|2|
|3|

#### Numeric-indexed Associative Array

##### Oracle 2

```sql
CREATE OR REPLACE PROCEDURE numeric_associative_array
IS
    TYPE numeric_associative_array_typ IS TABLE OF INTEGER
        INDEX BY PLS_INTEGER;

    associate_array numeric_associativ
    e_array_typ := numeric_associative_array_typ();
    associate_index PLS_INTEGER;
BEGIN
    associate_array(1) := -1;
    associate_array(2) := -2;
    associate_array(3) := -3;

    DBMS_OUTPUT.PUT_LINE(associate_array(1));
    associate_array(1) := -4;

    DBMS_OUTPUT.PUT_LINE(associate_array.COUNT);

    associate_index := associate_array.FIRST;
    WHILE associate_index IS NOT NULL
    LOOP
        DBMS_OUTPUT.PUT_LINE(associate_array(associate_index));
        associate_index := associate_array.NEXT(associate_index);
    END LOOP;
END;

CALL numeric_associative_array();
```

##### Result 3

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|-1|
|3|
|-4|
|-2|
|-3|

##### Snowflake 2

Please note that the numeric value is converted to varchar accordingly when the operation needs it.
Additionally, note the ‘true’ parameter in the OBJECT_INSERT. This is so that the element is updated
if it is already present in the array.

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.numeric_associative_array ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
      associate_array OBJECT := OBJECT_CONSTRUCT();
      associate_index NUMBER;
   BEGIN
      associate_array := OBJECT_INSERT(associate_array, '1', -1, true);
      associate_array := OBJECT_INSERT(associate_array, '2', -2, true);
      associate_array := OBJECT_INSERT(associate_array, '3', -3, true);

      CALL DBMS_OUTPUT.PUT_LINE(:associate_array['1']);

      associate_array := OBJECT_INSERT(:associate_array, '1', -4, true);

      CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(OBJECT_KEYS(:associate_array)));

      FOR i IN 1 TO ARRAY_SIZE(OBJECT_KEYS(:associate_array))
      LOOP
         associate_index := OBJECT_KEYS(:associate_array)[:i-1];
         CALL DBMS_OUTPUT.PUT_LINE(:associate_array[:associate_index::VARCHAR]);
      END LOOP;
   END;
$$;

CALL PUBLIC.numeric_associative_array();
SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG;
```

##### Result 4

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|-1|
|3|
|-4|
|-2|
|-3|

#### Record-element Numeric-indexed Associative Array

In this case, the associative array is composed of a Record-structure, and this structure needs to
be preserved. For this purpose, further operations on insertions were added.

##### Oracle 3

```sql
CREATE OR REPLACE PROCEDURE record_associative_array
IS
    TYPE record_typ IS RECORD(col1 INTEGER);
    TYPE record_associative_array_typ IS TABLE OF record_typ
        INDEX BY PLS_INTEGER;

    associate_array record_associati ve_array_typ := record_associative_array_typ();
    associate_index PLS_INTEGER;
BEGIN
    associate_array(1).col1 := -1;
    associate_array(2).col1 := -2;
    associate_array(3).col1 := -3;

    DBMS_OUTPUT.PUT_LINE(associate_array(1).col1);
    associate_array(4).col1 := -4;

    DBMS_OUTPUT.PUT_LINE(associate_array.COUNT);

    associate_index := associate_array.FIRST;
    WHILE associate_index IS NOT NULL
    LOOP
        DBMS_OUTPUT.PUT_LINE(associate_array(associate_index).col1);
        associate_index := associate_array.NEXT(associate_index);
    END LOOP;
END;
/

CALL record_associative_array();
```

##### Result 5

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|-1|
|3|
|-4|
|-2|
|-3|

##### Snowflake 3

In this scenario, the insertion/update assumes an automatic creation of the record within the
associative array and this needs to be taken into account when creating new records.

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.record_associative_array ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   DECLARE
      associate_array OBJECT := OBJECT_CONSTRUCT();
      associate_index NUMBER;
   BEGIN
      associate_array := OBJECT_INSERT(associate_array, '1', OBJECT_INSERT(NVL(associate_array['1'], OBJECT_CONSTRUCT()), 'col1', -1, true), true);
      associate_array := OBJECT_INSERT(associate_array, '2', OBJECT_INSERT(NVL(associate_array['2'], OBJECT_CONSTRUCT()), 'col1', -2, true), true);
      associate_array := OBJECT_INSERT(associate_array, '3', OBJECT_INSERT(NVL(associate_array['3'], OBJECT_CONSTRUCT()), 'col1', -3, true), true);

      CALL DBMS_OUTPUT.PUT_LINE(:associate_array['1']:col1);

      associate_array := OBJECT_INSERT(associate_array, '1', OBJECT_INSERT(NVL(associate_array['1'], OBJECT_CONSTRUCT()), 'col1', -4, true), true);

      CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(OBJECT_KEYS(:associate_array)));

      FOR i IN 1 TO ARRAY_SIZE(OBJECT_KEYS(:associate_array))
      LOOP
         associate_index := OBJECT_KEYS(:associate_array)[:i-1];
         CALL DBMS_OUTPUT.PUT_LINE(:associate_array[:associate_index::VARCHAR]:col1);
      END LOOP;
   END;
$$;

CALL PUBLIC.record_associative_array();
SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG;
```

##### Result 6

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|-1|
|3|
|-4|
|-2|
|-3|

### Known Issues 2

#### 1. They are currently not being recognized

SnowConvert AI treats these collections as Nested Table Arrays. There is a work item to fix this.

### Related EWIs 2

No related EWIs.

## Collection Methods

This is a translation reference to convert the Oracle Collection Methods to Snowflake

Warning

This section is a work in progress, information may change in the future

### Note 3

Some parts in the output code are omitted for clarity reasons.

### Description 2

> A collection method is a PL/SQL subprogram—either a function that returns information about a
> collection or a procedure that operates on a collection. Collection methods make collections
> easier to use and your applications easier to maintain.
>
> ([Oracle PL/SQL Language Reference COLLECTION METHODS](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/plsql-collections-and-records.html#GUID-0452FBDC-D9C1-486E-B432-49AF84743A9F))

Some of these methods can be mapped to native Snowflake semi-structured operations. The ones that
can’t or have differences will be mapped to a UDF implementation.

### Current SnowConvert AI Support 2

The next table shows a summary of the current support provided by the SnowConvert AI tool. Please
keep into account that translations may still not be final, and more work may be needed.

<!-- prettier-ignore -->
|Method|Current recognition status|Current translation status|Mapped to|
|---|---|---|---|
|[DELETE](#delete)|Not Recognized.|Not Translated.|UDF|
|[TRIM](#trim)|Not Recognized.|Not Translated.|UDF (To be defined)|
|[EXTEND](#extend)|Not Recognized.|Not Translated.|UDF|
|[EXISTS](#exists)|Not Recognized.|Not Translated.|[ARRAY_CONTAINS](https://docs.snowflake.com/en/sql-reference/functions/array_contains.html)|
|[FIRST](#first-last)|Not Recognized.|Not Translated.|UDF|
|[LAST](#first-last)|Not Recognized.|Not Translated.|UDF|
|[COUNT](#count)|Not Recognized.|Not Translated.|[ARRAY_SIZE](https://docs.snowflake.com/en/sql-reference/functions/array_size.html)|
|[LIMIT](#limit)|Not Recognized.|Not Translated.|Not Supported.|
|[PRIOR](#prior-next)|Not Recognized.|Not Translated.|UDF (To be defined)|
|[NEXT](#prior-next)|Not Recognized.|Not Translated.|UDF (To be defined)|

### Sample Source Patterns 2

#### COUNT

This method returns the count of “non-undefined” (not to be confused with null) elements within a
collection (nested tables can become sparse leaving these elements in between). In associative
arrays, it returns the number of keys in the array.

##### Oracle 4

```sql
CREATE OR REPLACE PROCEDURE collection_count
IS
    TYPE varray_typ IS VARRAY(5) OF INTEGER;
    TYPE nt_typ IS TABLE OF INTEGER;
    TYPE aa_typ IS TABLE OF INTEGER INDEX BY VARCHAR2(20);

    associative_array aa_typ := aa_typ('abc'=>1, 'bca'=>1);
    varray_variable varray_typ := varray_typ(1, 2, 3);
    nt_variable nt_typ := nt_typ(1, 2, 3, 4);
BEGIN
    DBMS_OUTPUT.PUT_LINE(associative_array.COUNT);
    DBMS_OUTPUT.PUT_LINE(varray_variable.COUNT);
    DBMS_OUTPUT.PUT_LINE(nt_variable.COUNT);
END;

CALL collection_count();
```

##### Result 7

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|2|
|3|
|4|

##### Snowflake 4

The snowflake equivalent is the
[ARRAY_SIZE](https://docs.snowflake.com/en/sql-reference/functions/array_size.html) method.

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.collection_count()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    associative_array OBJECT := OBJECT_CONSTRUCT('abc', 1, 'bca', 1);
    varray_variable ARRAY := ARRAY_CONSTRUCT(1, 2, 3);
    nt_variable ARRAY := ARRAY_CONSTRUCT(1, 2, 3, 4);
BEGIN
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(OBJECT_KEYS(:associative_array)));
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(:varray_variable));
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(:nt_variable));
END;
$$;

CALL PUBLIC.collection_count();
SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG;
```

##### Result 8

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|2|
|3|
|4|

#### EXISTS

This method returns true if the given element is contained within the collection. In associative
arrays, it tests if the key is contained.

##### Oracle 5

```sql
CREATE OR REPLACE PROCEDURE collection_exists
IS
    TYPE nt_typ IS TABLE OF INTEGER;
    TYPE aa_typ IS TABLE OF INTEGER INDEX BY VARCHAR2(20);

    associative_array aa_typ := aa_typ('abc'=>1, 'bca'=>1);
    nt_variable nt_typ := nt_typ(1, 2, 3, 4);
BEGIN
    IF associative_array.EXISTS('abc')
    THEN DBMS_OUTPUT.PUT_LINE('Found');
    END IF;

    IF NOT associative_array.EXISTS('not found')
    THEN DBMS_OUTPUT.PUT_LINE('Not found');
    END IF;

    IF nt_variable.EXISTS(1)
    THEN DBMS_OUTPUT.PUT_LINE('Found');
    END IF;

    IF NOT nt_variable.EXISTS(5)
    THEN DBMS_OUTPUT.PUT_LINE('Not found');
    END IF;
END;
/

CALL collection_exists();
```

##### Result 9

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|2|
|3|
|4|

##### Snowflake 5

The snowflake equivalent is the
[ARRAY_CONTAINS](https://docs.snowflake.com/en/sql-reference/functions/array_contains.html) method.
Note that, when using Varchar elements, casting to Variant is necessary.

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.collection_exists()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    associative_array OBJECT := OBJECT_CONSTRUCT('abc', 1, 'bca', 1);
    nt_variable ARRAY := ARRAY_CONSTRUCT(1, 2, 3, 4);
BEGIN
    IF (ARRAY_CONTAINS('abc'::VARIANT, OBJECT_KEYS(associative_array)))
    THEN CALL DBMS_OUTPUT.PUT_LINE('Found');
    END IF;

    IF (NOT ARRAY_CONTAINS('not found'::VARIANT, OBJECT_KEYS(associative_array)))
    THEN CALL DBMS_OUTPUT.PUT_LINE('Not found');
    END IF;

    IF (ARRAY_CONTAINS(1, nt_variable))
    THEN CALL DBMS_OUTPUT.PUT_LINE('Found');
    END IF;

    IF (NOT ARRAY_CONTAINS(5, nt_variable))
    THEN CALL DBMS_OUTPUT.PUT_LINE('Not found');
    END IF;
END;
$$;

CALL PUBLIC.collection_exists();
SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG;
```

##### Result 10

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|2|
|3|
|4|

#### FIRST/LAST

These two methods return the First/Last element of the collection, respectively. If the collection
is empty it returns null. This operation is mapped to a UDF, which will be added in further
revisions.

##### Oracle 6

```sql
CREATE OR REPLACE PROCEDURE collection_first_last
IS
    TYPE nt_typ IS TABLE OF INTEGER;
    TYPE aa_typ IS TABLE OF INTEGER INDEX BY VARCHAR2(20);

    associative_array aa_typ := aa_typ('abc'=>1, 'bca'=>1);
    nt_variable nt_typ := nt_typ();
BEGIN
    DBMS_OUTPUT.PUT_LINE(associative_array.FIRST);
    DBMS_OUTPUT.PUT_LINE(associative_array.LAST);

    DBMS_OUTPUT.PUT_LINE(nt_variable.FIRST);
    DBMS_OUTPUT.PUT_LINE(nt_variable.LAST);
    nt_variable := nt_typ(1, 2, 3, 4);
    DBMS_OUTPUT.PUT_LINE(nt_variable.FIRST);
    DBMS_OUTPUT.PUT_LINE(nt_variable.LAST);
END;
/

CALL collection_first_last();
```

##### Result 11

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|abc|
|bca|
|–These empty spaces are due to it evaluating to null|
|                                                      |
|1|
|4|

##### Snowflake 6

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.collection_first_last()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    associative_array OBJECT := OBJECT_CONSTRUCT('abc', 1, 'bca', 1);
    nt_variable ARRAY := ARRAY_CONSTRUCT();
BEGIN
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_FIRST(:associative_array));
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_LAST(:associative_array));

    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_FIRST(:nt_variable));
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_LAST(:nt_variable));
    nt_variable := ARRAY_CONSTRUCT(1, 2, 3, 4);
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_FIRST(:nt_variable));
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_LAST(:nt_variable));
END;
$$;

CALL PUBLIC.collection_first_last();
SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG;
```

##### UDFs

```sql
CREATE OR REPLACE FUNCTION ARRAY_FIRST(array_variable VARIANT)
RETURNS VARIANT
LANGUAGE SQL
AS
$$
    IFF (IS_OBJECT(array_variable),
        ARRAY_FIRST(OBJECT_KEYS(array_variable)),
        IFF (ARRAY_SIZE(array_variable) = 0, null, array_variable[0]))
$$;

CREATE OR REPLACE FUNCTION ARRAY_LAST(array_variable VARIANT)
RETURNS VARIANT
LANGUAGE SQL
AS
$$
    IFF (IS_OBJECT(array_variable),
        ARRAY_LAST(OBJECT_KEYS(array_variable)),
        IFF (ARRAY_SIZE(array_variable) = 0, null, array_variable[ARRAY_SIZE(array_variable)-1]))
$$;
```

##### Result 12

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|abc|
|bca|
|–These empty spaces are due to it evaluating to null|
|                                                      |
|1|
|4|

#### DELETE

This method is used to remove elements from a Collection. It has three possible variants:

- .DELETE removes all elements.
- .DELETE(n) removes the element whose index matches ‘n’.
- .DELETE(n, m) removes in the indexes from ‘n’ through ‘m’.

##### Note 4

In Oracle, using this operation on Nested Tables causes it to have “undefined” elements within it
due to them being sparse.

Warning

Please note that the second and third versions do not apply to Varrays.

##### Oracle 7

For the sake of simplicity, this sample only checks on the number of elements but may be modified to
display the contents of each collection.

```sql
CREATE OR REPLACE PROCEDURE collection_delete
IS
    TYPE varray_typ IS VARRAY(5) OF INTEGER;
    TYPE nt_typ IS TABLE OF INTEGER;
    TYPE aa_typ IS TABLE OF INTEGER INDEX BY VARCHAR2(20);

    associative_array1 aa_typ := aa_typ('abc'=>1, 'def'=>2, 'ghi'=>3, 'jkl'=>4);
    associative_array2 aa_typ := aa_typ('abc'=>1, 'def'=>2, 'ghi'=>3, 'jkl'=>4);
    associative_array3 aa_typ := aa_typ('abc'=>1, 'def'=>2, 'ghi'=>3, 'jkl'=>4);

    varray_variable1 varray_typ := varray_typ(1, 2, 3, 4);

    nt_variable1 nt_typ := nt_typ(1, 2, 3, 4);
    nt_variable2 nt_typ := nt_typ(1, 2, 3, 4);
    nt_variable3 nt_typ := nt_typ(1, 2, 3, 4);
BEGIN
    varray_variable1.DELETE;--delete everything

    nt_variable1.DELETE;--delete everything
    nt_variable2.DELETE(2);--delete second position
    nt_variable3.DELETE(2, 3);--delete range

    associative_array1.DELETE;--delete everything
    associative_array2.DELETE('def');--delete second position
    associative_array3.DELETE('def', 'jkl');--delete range

    DBMS_OUTPUT.PUT_LINE(varray_variable1.COUNT);
    DBMS_OUTPUT.PUT_LINE(nt_variable1.COUNT);
    DBMS_OUTPUT.PUT_LINE(nt_variable2.COUNT);
    DBMS_OUTPUT.PUT_LINE(nt_variable3.COUNT);

    DBMS_OUTPUT.PUT_LINE(associative_array1.COUNT);
    DBMS_OUTPUT.PUT_LINE(associative_array2.COUNT);
    DBMS_OUTPUT.PUT_LINE(associative_array3.COUNT);
END;
/

CALL collection_delete();
```

##### Result 13

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|0|
|0|
|3|
|2|
|0|
|3|
|1|

##### Snowflake 7

Snowflake does not support deletions from an existing ARRAY and for this reason, the only offered
workaround is to rebuild a new ARRAY depending on the original parameters of the DELETE.

###### Note 5

Note that a UDF was added to implement the functionality for the update of the element.

This UDF will be added in later revisions.

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.collection_delete()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    associative_array1 OBJECT := OBJECT_CONSTRUCT('abc'=>1, 'def'=>2, 'ghi'=>3, 'jkl'=>4);
    associative_array2 OBJECT := OBJECT_CONSTRUCT('abc'=>1, 'def'=>2, 'ghi'=>3, 'jkl'=>4);
    associative_array3 OBJECT := OBJECT_CONSTRUCT('abc'=>1, 'def'=>2, 'ghi'=>3, 'jkl'=>4);

    varray_variable1 ARRAY := ARRAY_CONSTRUCT(1, 2, 3, 4);

    nt_variable1 ARRAY := ARRAY_CONSTRUCT(1, 2, 3, 4);
    nt_variable2 ARRAY := ARRAY_CONSTRUCT(1, 2, 3, 4);
    nt_variable3 ARRAY := ARRAY_CONSTRUCT(1, 2, 3, 4);
BEGIN
    varray_variable1 := ARRAY_CONSTRUCT();--delete everything

    nt_variable1 := ARRAY_CONSTRUCT();--delete everything
    nt_variable2 := ARRAY_DELETE_UDF(nt_variable2, 2);--delete second position
    nt_variable3 := ARRAY_DELETE_UDF(nt_variable3, 2, 3);--delete range

    associative_array1 := OBJECT_CONSTRUCT();--delete everything
    associative_array2 := ASSOCIATIVE_ARRAY_DELETE_UDF('def');--delete second position
    associative_array3 := ASSOCIATIVE_ARRAY_DELETE_UDF('def', 'jkl');--delete range

    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(varray_variable1));
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(nt_variable1);
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(nt_variable2);
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(nt_variable3);

    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(associative_array1));
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(associative_array2));
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(associative_array3));
END;
$$;

CALL PUBLIC.collection_first_last();
SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG;
```

##### Result 14

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|0|
|0|
|3|
|2|
|0|
|3|
|1|

#### EXTEND

This method is used to append new elements to a Nested Table or a Varray. It has three possible
variants:

- .EXTEND inserts a null element.
- .EXTEND(n) inserts ‘n’ null elements.
- .EXTEND(n, i) inserts ‘n’ copies of the element at ‘i’.

##### Oracle 8

```sql
CREATE OR REPLACE PROCEDURE collection_extend
IS
    TYPE varray_typ IS VARRAY(5) OF INTEGER;
    TYPE nt_typ IS TABLE OF INTEGER;

    nt_variable1 nt_typ := nt_typ(1, 2, 3, 4);
    varray_variable1 varray_typ := varray_typ(1, 2, 3);
    varray_variable2 varray_typ := varray_typ(1, 2, 3);
BEGIN
    nt_variable1.EXTEND;
    varray_variable1.EXTEND(2);
    varray_variable2.EXTEND(2, 1);

    DBMS_OUTPUT.PUT_LINE(nt_variable1.COUNT);
    DBMS_OUTPUT.PUT_LINE(varray_variable1.COUNT);
    DBMS_OUTPUT.PUT_LINE(varray_variable2.COUNT);
END;
/

CALL collection_extend();
```

##### Result 15

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|5|
|5|
|5|

##### Snowflake 8

###### Note 6

Note that a UDF was added to implement the functionality for the update of the element.

This UDF will be added in later revisions.

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.collection_first_last()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    nt_variable1 ARRAY := ARRAY_CONSTRUCT(1, 2, 3, 4);
    varray_variable1 ARRAY := ARRAY_CONSTRUCT(1, 2, 3);
    varray_variable2 ARRAY := ARRAY_CONSTRUCT(1, 2, 3);
BEGIN
    nt_variable1 := ARRAY_EXTEND_UDF(nt_variable);
    varray_variable1 := ARRAY_EXTEND_UDF(varray_variable1, 2);
    varray_variable2 := ARRAY_EXTEND_UDF(varray_variable2, 2, 1);

    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(nt_variable1);
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(varray_variable1));
    CALL DBMS_OUTPUT.PUT_LINE(ARRAY_SIZE(varray_variable2));
END;
$$;

CALL PUBLIC.collection_first_last();
SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG;
```

##### Result 16

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|5|
|5|
|5|

#### TRIM

This method is used to remove the last elements from a Nested Table or a Varray. It has two possible
variants:

- .TRIM removes the last element.
- .TRIM(n) removes the last ‘n’ elements.

##### Note 7

This functionality may be implemented using
[ARRAY_SLICE](https://docs.snowflake.com/en/sql-reference/functions/array_slice.html)

##### Oracle 9

```sql
CREATE OR REPLACE PROCEDURE collection_trim
IS
    TYPE varray_typ IS VARRAY(5) OF INTEGER;
    TYPE nt_typ IS TABLE OF INTEGER;

    varray_variable1 varray_typ := varray_typ(1, 2, 3);
    nt_variable1 nt_typ := nt_typ(1, 2, 3, 4);
BEGIN
    varray_variable1.TRIM;
    nt_variable1.TRIM(2);

    DBMS_OUTPUT.PUT_LINE(nt_variable1.COUNT);
    DBMS_OUTPUT.PUT_LINE(varray_variable1.COUNT);
END;
/

CALL collection_trim();
```

##### Result 17

```sql
DBMS OUTPUT
-----------
2
2
```

#### LIMIT

This method returns the maximum limit of a Varray.

Danger

This method is not supported in Snowflake.

##### Oracle 10

```sql
CREATE OR REPLACE PROCEDURE collection_limit
IS
    TYPE varray_typ1 IS VARRAY(5) OF INTEGER;
    TYPE varray_typ2 IS VARRAY(6) OF INTEGER;

    varray_variable1 varray_typ1 := varray_typ1(1, 2, 3);
    varray_variable2 varray_typ2 := varray_typ2(1, 2, 3, 4);
BEGIN
    DBMS_OUTPUT.PUT_LINE(varray_variable1.LIMIT);
    DBMS_OUTPUT.PUT_LINE(varray_variable2.LIMIT);
END;
/

CALL collection_limit();
```

##### Result 18

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|5|
|6|

#### PRIOR/NEXT

This method returns the prior/next index, given an index. If there is not a prior/next then it
returns null. It is most frequently used to traverse a collection.

##### Oracle 11

```sql
CREATE OR REPLACE PROCEDURE collection_prior_next
IS
    TYPE varray_typ1 IS VARRAY(5) OF INTEGER;
    TYPE aa_typ IS TABLE OF INTEGER INDEX BY VARCHAR2(20);

    varray_variable1 varray_typ1 := varray_typ1(-1, -2, -3);
    associative_array1 aa_typ := aa_typ('abc'=>1, 'def'=>2, 'ghi'=>3, 'jkl'=>4);
BEGIN
    DBMS_OUTPUT.PUT_LINE(varray_variable1.PRIOR(1));
    DBMS_OUTPUT.PUT_LINE(varray_variable1.PRIOR(2));
    DBMS_OUTPUT.PUT_LINE(varray_variable1.NEXT(2));
    DBMS_OUTPUT.PUT_LINE(varray_variable1.NEXT(3));

    DBMS_OUTPUT.PUT_LINE(associative_array1.PRIOR('abc'));
    DBMS_OUTPUT.PUT_LINE(associative_array1.PRIOR('def'));
    DBMS_OUTPUT.PUT_LINE(associative_array1.NEXT('ghi'));
    DBMS_OUTPUT.PUT_LINE(associative_array1.NEXT('jkl'));
    DBMS_OUTPUT.PUT_LINE(associative_array1.PRIOR('not found'));
END;
/

CALL collection_prior_next();
```

##### Result 19

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|– Empty spaces are due to null results|
|1|
|3|
|                                        |
|                                        |
|abc|
|jkl|
|                                        |
|jkl|

### Known Issues 3

#### 1. Limit method is not supported in Snowflake

Snowflake does not have support for limited-space varrays. For this reason, this method is not
supported.

### Related EWIs 3

No EWIs related.

## Nested Table Array Type Definition

This is a translation reference to convert the Oracle Nested Table Array Declaration to Snowflake

Warning

This section is a work in progress, information may change in the future.

### Note 8

This section is for the PL/SQL Version of the Nested Table Arrays, for the Standalone Version please
see
[Nested Table Type Definition](../sql-translation-reference/create_type.html#nested-table-type-definition).

### Note 9

Some parts in the output code are omitted for clarity reasons.

### Description 3

> In the database, a nested table is a column type that stores an unspecified number of rows in no
> particular order.
>
> When you retrieve a nested table value from the database into a PL/SQL nested table variable,
> PL/SQL gives the rows consecutive indexes, starting at 1. Using these indexes, you can access the
> individual rows of the nested table variable. The syntax is `variable_name(index)`. The indexes
> and row order of a nested table might not remain stable as you store and retrieve the nested table
> from the database.
>
> ([Oracle PL/SQL Language Reference NESTED TABLES](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/plsql-collections-and-records.html#GUID-5ADB7EE2-71F6-4172-ACD8-FFDCF2787A37))

For the translation, the type definition is replaced by an ARRAY
[Semi-structured Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html)
and then its usages are changed accordingly across any operations. Please note how the translation
for Nested Tables and Varrays are the same.

In order to define a Nested Table Array type, the syntax is as follows:

```sql
type_definition := TYPE IS TABLE OF datatype;
```

To declare a variable of this type:

```sql
variable_name collection_type;
```

### Sample Source Patterns 3

#### Nested Table Array definitions

This illustrates how to create different nested table arrays, and how to migrate the definitions for
the variables.

##### Oracle 12

```sql
CREATE OR REPLACE PROCEDURE nested_table_procedure
IS
    TYPE nested_table_array_typ IS TABLE OF INTEGER;
    TYPE nested_table_array_typ2 IS TABLE OF DATE;

    nested_table_array nested_table_array_typ;
    nested_table_array2 nested_table_array_typ2;
BEGIN
    NULL;
END;
```

##### Snowflake 9

```sql
CREATE OR REPLACE PROCEDURE nested_table_procedure()
RETURNS INTEGER
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    -- NO LONGER NEEDED
    /*
    TYPE associative_array_typ IS TABLE OF INTEGER INDEX BY VARCHAR2(30);
    TYPE associative_array_typ2 IS TABLE OF INTEGER INDEX BY PLS_INTEGER;
    */

    associative_array ARRAY;
    associative_array2 ARRAY;
BEGIN
    NULL;
END;
$$;
```

#### Nested Table iteration

##### Oracle 13

```sql
CREATE OR REPLACE PROCEDURE nested_table_iteration
IS
    TYPE nested_table_typ IS TABLE OF INTEGER;
    nested_table_variable nested_table_typ := nested_table_typ (10, 20, 30);
BEGIN
    FOR i IN 1..nested_table_variable.COUNT
    LOOP
        DBMS_OUTPUT.PUT_LINE(nested_table_variable(i));
    END LOOP;

    nested_table_variable (1) := 40;

    FOR i IN 1..nested_table_variable.COUNT
    LOOP
        DBMS_OUTPUT.PUT_LINE(nested_table_variable(i));
    END LOOP;
END;
/

CALL nested_table_iteration();
```

##### Result 20

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|10|
|20|
|30|
|40|
|20|
|30|

##### Snowflake 10

###### Note 10

Note that a UDF was added to implement the functionality for the update of the element.

This UDF will be added in later revisions.

```sql
CREATE OR REPLACE PROCEDURE PUBLIC.nested_table_iteration()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    nested_table_variable ARRAY := ARRAY_CONSTRUCT(10, 20, 30);
BEGIN
    FOR i IN 1 TO ARRAY_SIZE(nested_table_variable)
    LOOP
        CALL DBMS_OUTPUT.PUT_LINE(:nested_table_variable[:i-1]);
    END LOOP;

    nested_table_variable:= INSERT_REPLACE_COLLECTION_ELEMENT_UDF(nested_table_variable, 1, 40);

    FOR i IN 1 TO ARRAY_SIZE(nested_table_variable)
    LOOP
        CALL DBMS_OUTPUT.PUT_LINE(:nested_table_variable[:i-1]);
    END LOOP;
END;
$$;

CALL PUBLIC.nested_table_iteration();
SELECT * FROM DBMS_OUTPUT.DBMS_OUTPUT_LOG;
```

##### UDF

```sql
CREATE OR REPLACE FUNCTION PUBLIC.INSERT_REPLACE_COLLECTION_ELEMENT_UDF(varray ARRAY, position INTEGER, newValue VARIANT)
RETURNS ARRAY
LANGUAGE SQL
AS
$$
    ARRAY_CAT(
        ARRAY_APPEND(ARRAY_SLICE(varray, 0, (position)-1), newValue),
        ARRAY_SLICE(varray, position, ARRAY_SIZE(varray)))
$$;
```

##### Result 21

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|10|
|20|
|30|
|40|
|20|
|30|

### Known Issues 4

#### 1. They are currently not being converted

SnowConvert AI does not support translating these elements.

##### 2. Indexing needs to be modified

Oracle’s indexes start at 1, on Snowflake they will begin at 0.

### Related EWIs 4

No EWIs related.

## Record Type Definition

This is a translation reference to convert the Oracle Record Declaration to Snowflake

Warning

This section is a work in progress, information may change in the future.

### Note 11

Some parts in the output code are omitted for clarity reasons.

### Description 4

> A record variable is a composite variable whose internal components, called fields, can have
> different data types. The value of a record variable and the values of its fields can change.
>
> You reference an entire record variable by its name. You reference a record field with the syntax
> `record.field`.
>
> You can create a record variable in any of these ways:
>
> - Define a record type and then declare a variable of that type.
> - Use `%ROWTYPE` to declare a record variable that represents either a full or partial row of a
>   database table or view.
> - Use `%TYPE` to declare a record variable of the same type as a previously declared record
>   variable.
>
> ([Oracle PL/SQL Language Reference RECORD VARIABLES](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/plsql-collections-and-records.html#GUID-75875E26-FC7B-4513-A5E2-EDA26F1D67B1))

For the translation, the type definition is replaced by an OBJECT
[Semi-structured Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html)
and then its usages are changed accordingly across any operations.

In order to define a Record type, the syntax is as follows:

```sql
type_definition := TYPE IS RECORD ( field_definition [, field_definition...] );

field_definition := field_name datatype [ { [NOT NULL default ] | default } ]

default := [ { := | DEFAULT } expression]
```

To declare a variable of this type:

```sql
variable_name { record_type
              | rowtype_attribute
              | record_variable%TYPE
              };
```

### Sample Source Patterns 4

#### Note 12

Some parts in the output code are omitted for clarity reasons.

#### Record initialization and assignment

This sample attempts to insert two new rows using a record variable which is reassigned
mid-procedure.

##### Oracle 14

```sql
CREATE TABLE record_table(col1 FLOAT, col2 INTEGER);

CREATE OR REPLACE PROCEDURE record_procedure
IS
    TYPE record_typ IS RECORD(col1 INTEGER, col2 FLOAT);
    record_variable record_typ := record_typ(1, 1.5);--initialization
BEGIN
    INSERT INTO record_table(col1, col2)
        VALUES (record_variable.col2, record_variable.col1);--usage

    --reassignment of properties
    record_variable.col1 := 2;
    record_variable.col2 := 2.5;

    INSERT INTO record_table(col1, col2)
        VALUES (record_variable.col2, record_variable.col1);--usage
END;

CALL record_procedure();
SELECT * FROM record_table;
```

##### Result 22

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|1.5|1|
|2.5|2|

##### Snowflake 11

Notice how the reassignments are replaced by an OBJECT_INSERT that updates if the column already
exists, and how the VALUES clause is replaced by a SELECT.

```sql
CREATE OR REPLACE TABLE record_table (col1 FLOAT,
    col2 INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE record_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!
        TYPE record_typ IS RECORD(col1 INTEGER, col2 FLOAT);
        record_variable OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - record_typ DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT('COL1', 1, 'COL2', 1.5);--initialization

    BEGIN
        INSERT INTO record_table(col1, col2)
        SELECT
            :record_variable:COL2,
            :record_variable:COL1;--usage

        --reassignment of properties
        record_variable := OBJECT_INSERT(record_variable, 'COL1', 2, true);
        record_variable := OBJECT_INSERT(record_variable, 'COL2', 2.5, true);

        INSERT INTO record_table(col1, col2)
        SELECT
            :record_variable:COL2,
            :record_variable:COL1;--usage

    END;
$$;

CALL record_procedure();

SELECT * FROM
    record_table;
```

##### Result 23

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|1.5|1|
|2.5|2|

#### %ROWTYPE Record and Values Record

Since the operations are the ones that define the structure, these definitions can be replaced by an
OBJECT datatype, but the values of the record need to be decomposed as inserting the record “as-is”
is not supported.

##### Oracle 15

```sql
CREATE TABLE record_table(col1 INTEGER, col2 VARCHAR2(50), col3 DATE);
CREATE OR REPLACE PROCEDURE insert_record
IS
    record_variable record_table%ROWTYPE;
BEGIN
    record_variable.col1 := 1;
    record_variable.col2 := 'Hello';
    record_variable.col3 := DATE '2020-12-25';

    INSERT INTO record_table VALUES record_variable;
END;

CALL insert_record();
SELECT * FROM record_table;
```

##### Result 24

<!-- prettier-ignore -->
|COL1|COL2|COL3|
|---|---|---|
|1|“Hello”|25-DEC-20|

##### Snowflake 12

Please note finally how the OBJECT variable needs to be initialized in order to add the information
to it.

```sql
CREATE OR REPLACE TABLE record_table (col1 INTEGER,
    col2 VARCHAR(50),
    col3 TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE insert_record ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        record_variable OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWTYPE DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
    BEGIN
        record_variable := OBJECT_INSERT(record_variable, 'COL1', 1, true);
        record_variable := OBJECT_INSERT(record_variable, 'COL2', 'Hello', true);
        record_variable := OBJECT_INSERT(record_variable, 'COL3', DATE '2020-12-25', true);
        INSERT INTO record_table
        SELECT
            :record_variable:COL1,
            :record_variable:COL2,
            :record_variable:COL3;
    END;
$$;

CALL insert_record();

SELECT * FROM
    record_table;
```

##### Result 25

<!-- prettier-ignore -->
|COL1|COL2|COL3|
|---|---|---|
|1|“Hello”|25-DEC-20|

#### Fetching data into a Record

##### Oracle 16

```sql
CREATE TABLE record_table(col1 INTEGER, col2 VARCHAR2(50), col3 DATE);
INSERT INTO record_table(col1, col2 , col3)
    VALUES (1, 'Hello', DATE '2020-12-25');

CREATE OR REPLACE PROCEDURE load_cursor_record
IS
    CURSOR record_cursor IS
        SELECT *
        FROM record_table;

    record_variable record_cursor%ROWTYPE;
BEGIN
    OPEN record_cursor;
    LOOP
        FETCH record_cursor INTO record_variable;
        EXIT WHEN record_cursor%NOTFOUND;

        DBMS_OUTPUT.PUT_LINE(record_variable.col1);
        DBMS_OUTPUT.PUT_LINE(record_variable.col2);
        DBMS_OUTPUT.PUT_LINE(record_variable.col3);
    END LOOP;
    CLOSE record_cursor;
END;

CALL load_cursor_record();
```

##### Result 26

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|1|
|Hello|
|25-DEC-20|

##### Snowflake 13

Please note the additional OBJECT_CONSTRUCT in the Cursor definition, this is what allows to extract
an OBJECT, which then can be used to seamlessly migrate the FETCH statement.

```sql
CREATE OR REPLACE TABLE record_table (col1 INTEGER,
    col2 VARCHAR(50),
    col3 TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

INSERT INTO record_table(col1, col2 , col3)
    VALUES (1, 'Hello', DATE '2020-12-25');

CREATE OR REPLACE PROCEDURE load_cursor_record ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        record_cursor CURSOR
        FOR
            SELECT
                OBJECT_CONSTRUCT( *) sc_cursor_record
            FROM
                record_table;
    record_variable OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWTYPE DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
    BEGIN
        OPEN record_cursor;
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        FETCH record_cursor INTO
                :record_variable;
        IF (record_variable IS NULL) THEN
                EXIT;
        END IF;
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF(:record_variable:COL1);
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF(:record_variable:COL2);
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF(:record_variable:COL3::DATE);
    END LOOP;
    CLOSE record_cursor;
    END;
$$;

CALL load_cursor_record();
```

##### Result 27

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|1|
|Hello|
|25-DEC-20|

#### Assigning a Record Variable in a SELECT INTO

This transformation consists in taking advantage of the OBJECT_CONTRUCT function to initialize the
record using the SELECT columns as the arguments.

#### Sample auxiliary code

##### Oracle 17

```sql
create table sample_table(ID number, NAME varchar2(23));
CREATE TABLE RESULTS (COL1 VARCHAR(20), COL2 VARCHAR(40));
insert into sample_table values(1, 'NAME 1');
insert into sample_table values(2, 'NAME 2');
insert into sample_table values(3, 'NAME 3');
insert into sample_table values(4, 'NAME 4');
```

##### Snowflake 14

```sql
CREATE OR REPLACE TABLE sample_table (ID NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
NAME VARCHAR(23))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE TABLE RESULTS (COL1 VARCHAR(20),
COL2 VARCHAR(40))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

insert into sample_table
values(1, 'NAME 1');

insert into sample_table
values(2, 'NAME 2');

insert into sample_table
values(3, 'NAME 3');

insert into sample_table
values(4, 'NAME 4');
```

##### Oracle 18

```sql
CREATE OR REPLACE PROCEDURE sp_sample1 AS
-- Rowtype variable
rowtype_variable sample_table%rowtype;

--Record variable
TYPE record_typ_def IS RECORD(ID number, NAME varchar2(23));
record_variable_def record_typ_def;

-- Auxiliary variable
name_var VARCHAR(20);
BEGIN
   SELECT * INTO rowtype_variable FROM sample_table WHERE ID = 1 FETCH NEXT 1 ROWS ONLY;
   name_var := rowtype_variable.NAME;
   INSERT INTO RESULTS(COL1, COL2) VALUES('SELECT 1', name_var);

   SELECT ID, NAME INTO rowtype_variable FROM sample_table WHERE ID = 2 FETCH NEXT 1 ROWS ONLY;
   name_var := rowtype_variable.NAME;
   INSERT INTO RESULTS(COL1, COL2) VALUES('SELECT 2', name_var);

   SELECT * INTO record_variable_def FROM sample_table WHERE ID = 3 FETCH NEXT 1 ROWS ONLY;
   name_var := record_variable_def.NAME;
   INSERT INTO RESULTS(COL1, COL2) VALUES('SELECT 3', name_var);

   SELECT ID, NAME INTO record_variable_def FROM sample_table WHERE ID = 4 FETCH NEXT 1 ROWS ONLY;
   name_var := record_variable_def.NAME;
   INSERT INTO RESULTS(COL1, COL2) VALUES('SELECT 4', name_var);
END;

call sp_sample1();

SELECT * FROM results;
```

##### Result 28

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|SELECT 1|NAME 1|
|SELECT 2|NAME 2|
|SELECT 3|NAME 3|
|SELECT 4|NAME 4|

##### Snowflake 15

```sql
CREATE OR REPLACE PROCEDURE sp_sample1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   DECLARE
      -- Rowtype variable
      rowtype_variable OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWTYPE DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();

      --Record variable
      !!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO OBJECT ***/!!!
      TYPE record_typ_def IS RECORD(ID number, NAME varchar2(23));
      record_variable_def OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - record_typ_def DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();

      -- Auxiliary variable
      name_var VARCHAR(20);
   BEGIN
      SELECT
         OBJECT_CONSTRUCT( *) INTO
         :rowtype_variable
      FROM
         sample_table
      WHERE ID = 1
      FETCH NEXT 1 ROWS ONLY;
      name_var := :rowtype_variable:NAME;
      INSERT INTO RESULTS(COL1, COL2) VALUES('SELECT 1', :name_var);

      SELECT
         OBJECT_CONSTRUCT()
      INTO
         :rowtype_variable
      FROM
         sample_table
      WHERE ID = 2
      FETCH NEXT 1 ROWS ONLY;
      name_var := :rowtype_variable:NAME;
      INSERT INTO RESULTS(COL1, COL2) VALUES('SELECT 2', :name_var);

      SELECT
         OBJECT_CONSTRUCT( *) INTO
         :record_variable_def
      FROM
         sample_table
      WHERE ID = 3
      FETCH NEXT 1 ROWS ONLY;
      name_var := :record_variable_def:NAME;
      INSERT INTO RESULTS(COL1, COL2) VALUES('SELECT 3', :name_var);

      SELECT
         OBJECT_CONSTRUCT('ID', ID, 'NAME', NAME) INTO
         :record_variable_def
      FROM
         sample_table
      WHERE ID = 4
      FETCH NEXT 1 ROWS ONLY;
      name_var := :record_variable_def:NAME;
      INSERT INTO RESULTS(COL1, COL2) VALUES('SELECT 4', :name_var);
   END;
$$;

call sp_sample1();

SELECT * FROM
   results;
```

##### Result 29

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
|SELECT 1|NAME 1|
|SELECT 2|NAME 2|
|SELECT 3|NAME 3|
|SELECT 4|NAME 4|

### Known Issues 5

#### 1. The following functionalities are currently not being converted

- Fetching data into a Record.
- Nested records (Records inside records).
- Collections inside records.

### Related EWIs 5

1. [SSC-EWI-0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036):
   Data type converted to another data type.
2. [SSC-EWI-0056](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0056):
   Create Type Not Supported
3. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
4. [SSC-FDM-OR0042](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior.
5. [SSC-FDM-OR0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation.
6. [SSC-PRF-0003](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0003):
   Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance.

## Varray Type Definition

This is a translation reference to convert the Oracle Varray Declaration to Snowflake

Warning

This section is a work in progress, information may change in the future.

### Note 13

This section is for the PL/SQL Version of the Varrays, for the Standalone Version please see
[Array Type Definition](../sql-translation-reference/create_type.html#array-type-definition).

### Note 14

Some parts in the output code are omitted for clarity reasons.

### Description 5

> A varray (variable-size array) is an array whose number of elements can vary from zero (empty) to
> the declared maximum size.
>
> To access an element of a varray variable, use the syntax `variable_name(index)`. The lower bound
> of `index` is 1; the upper bound is the current number of elements. The upper bound changes as you
> add or delete elements, but it cannot exceed the maximum size. When you store and retrieve a
> varray from the database, its indexes and element order remain stable.
>
> ([Oracle PL/SQL Language Reference VARRAYS](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/plsql-collections-and-records.html#GUID-E932FC04-C7AD-4562-9555-8BA05446C0B8))

For the translation, the type definition is replaced by an ARRAY
[Semi-structured Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html)
and then its usages are changed accordingly across any operations. Please note how the translation
for Nested Tables and Varrays are the same.

In order to define a varray type, the syntax is as follows:

```sql
type_definition := { VARRAY | [VARYING] ARRAY } (size_limit) OF datatype
            [NOT NULL];
```

To declare a variable of this type:

```sql
variable_name collection_type;
```

### Sample Source Patterns 5

#### Varray definitions

This illustrates how three different ways to create a varray, and how to migrate these definitions
for the variables.

##### Oracle 19

```sql
CREATE OR REPLACE PROCEDURE associative_array_procedure
IS
    TYPE varray_typ IS ARRAY(10) OF INTEGER;
    TYPE varray_typ2 IS VARRAY(10) OF INTEGER;
    TYPE varray_typ3 IS VARYING ARRAY(10) OF INTEGER;

    array_variable varray_typ;
    array_variable2 varray_typ2;
    array_variable3 varray_typ3;
BEGIN
    NULL;
END;
```

##### Snowflake 16

```sql
CREATE OR REPLACE PROCEDURE associative_array_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--        TYPE varray_typ IS ARRAY(10) OF INTEGER;
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--        TYPE varray_typ2 IS VARRAY(10) OF INTEGER;
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--        TYPE varray_typ3 IS VARYING ARRAY(10) OF INTEGER;

        array_variable VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'varray_typ' USAGE CHANGED TO VARIANT ***/!!!;
        array_variable2 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'varray_typ2' USAGE CHANGED TO VARIANT ***/!!!;
        array_variable3 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'varray_typ3' USAGE CHANGED TO VARIANT ***/!!!;
    BEGIN
        NULL;
    END;
$$;
```

#### Varray iteration

##### Oracle 20

```sql
CREATE OR REPLACE PROCEDURE varray_iteration
IS
    TYPE varray_typ IS VARRAY(3) OF INTEGER;
    varray_variable varray_typ := varray_typ(10, 20, 30);
BEGIN
    FOR i IN 1..varray_variable.COUNT
    LOOP
        DBMS_OUTPUT.PUT_LINE(varray_variable(i));
    END LOOP;

    varray_variable(1) := 40;

    FOR i IN 1..varray_variable.COUNT
    LOOP
        DBMS_OUTPUT.PUT_LINE(varray_variable(i));
    END LOOP;
END;
/

CALL varray_iteration();
```

##### Result 30

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|10|
|20|
|30|
|40|
|20|
|30|

##### Snowflake 17

###### Note 15

Note that a UDF was added to implement the functionality for the update of the element.

This UDF will be added in later revisions.

```sql
CREATE OR REPLACE PROCEDURE varray_iteration ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
--        !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--        TYPE varray_typ IS VARRAY(3) OF INTEGER;
        varray_variable VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'varray_typ' USAGE CHANGED TO VARIANT ***/!!! := varray_typ(10, 20, 30);
    BEGIN
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        FOR i IN 1 TO 0 /*varray_variable.COUNT*/!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'VARRAY CUSTOM TYPE EXPRESSION' NODE ***/!!!
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        LOOP
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            CALL DBMS_OUTPUT.PUT_LINE_UDF(varray_variable(i));
        END LOOP;
            !!!RESOLVE EWI!!! /*** SSC-EWI-OR0108 - THE FOLLOWING ASSIGNMENT STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
            varray_variable(1) := 40;
            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
            FOR i IN 1 TO 0 /*varray_variable.COUNT*/!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'VARRAY CUSTOM TYPE EXPRESSION' NODE ***/!!!
            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
               LOOP
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            CALL DBMS_OUTPUT.PUT_LINE_UDF(varray_variable(i));
               END LOOP;
    END;
$$;

CALL varray_iteration();
```

##### UDF 2

```sql
CREATE OR REPLACE FUNCTION PUBLIC.INSERT_REPLACE_COLLECTION_ELEMENT_UDF(varray ARRAY, position INTEGER, newValue VARIANT)
RETURNS ARRAY
LANGUAGE SQL
AS
$$
    ARRAY_CAT(
        ARRAY_APPEND(ARRAY_SLICE(varray, 0, (position)-1), newValue),
        ARRAY_SLICE(varray, position, ARRAY_SIZE(varray)))
$$;
```

##### Result 31

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|10|
|20|
|30|
|40|
|20|
|30|

### Known Issues 6

#### 1. They are currently not being converted 2

SnowConvert AI does not support translating these elements.

##### 2. Indexing needs to be modified 2

Oracle’s indexes start at 1, on Snowflake they will begin at 0.

##### 3. Array Density may not match the original

Since the ARRAY datatype can become sparse, care should be taken when performing additions or
deletions of the array. Using
[ARRAY_COMPACT()](https://docs.snowflake.com/en/sql-reference/functions/array_compact.html) after
such operations can be helpful if the density is a concern.

### Related EWIs 6

1. [SSC-EWI-0058](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058):
   Functionality is not currently supported by Snowflake Scripting.
2. [SSC-EWI-0062](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062):
   Custom type usage changed to variant.
3. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
4. [SSC-EWI-OR0108](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0108):
   The Following Assignment Statement is Not Supported by Snowflake Scripting.
5. [SSC-FDM-OR0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation.

## Collection Bulk Operations

This is a translation reference to convert the Oracle Collection Bulk Operations to Snowflake

Warning

This section is a work in progress, information may change in the future

### Note 16

Some parts in the output code are omitted for clarity reasons.

### Description 6

> The `BULK` `COLLECT` clause, a feature of bulk SQL, returns results from SQL to PL/SQL in batches
> rather than one at a time.
>
> The `BULK` `COLLECT` clause can appear in:
>
> - `SELECT` `INTO` statement
> - `FETCH` statement
> - `RETURNING` `INTO` clause of:
>   - `DELETE` statement
>   - `INSERT` statement
>   - `UPDATE` statement
>   - `EXECUTE` `IMMEDIATE` statement
>
> With the `BULK` `COLLECT` clause, each of the preceding statements retrieves an entire result set
> and stores it in one or more collection variables in a single operation (which is more efficient
> than using a loop statement to retrieve one result row at a time).

([Oracle PL/SQL Language Reference BULK COLLECT CLAUSE](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/plsql-optimization-and-tuning.html#GUID-19F50644-C88E-49AF-B31C-3EE4B4432714))

This section has some workarounds for SELECTs and FETCH Cursor with Bulk Clauses.

### Sample Source Patterns 6

#### Source Table

##### Oracle 21

```sql
CREATE TABLE bulk_collect_table(col1 INTEGER);

INSERT INTO bulk_collect_table VALUES(1);
INSERT INTO bulk_collect_table VALUES(2);
INSERT INTO bulk_collect_table VALUES(3);
INSERT INTO bulk_collect_table VALUES(4);
INSERT INTO bulk_collect_table VALUES(5);
INSERT INTO bulk_collect_table VALUES(6);
```

##### Snowflake 18

```sql
CREATE OR REPLACE TABLE bulk_collect_table (col1 INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO bulk_collect_table
VALUES(1);

INSERT INTO bulk_collect_table
VALUES(2);

INSERT INTO bulk_collect_table
VALUES(3);

INSERT INTO bulk_collect_table
VALUES(4);

INSERT INTO bulk_collect_table
VALUES(5);

INSERT INTO bulk_collect_table
VALUES(6);
```

#### Bulk Collect from a Table

##### Oracle 22

```sql
CREATE OR REPLACE PROCEDURE bulk_collect_procedure
IS
    CURSOR record_cursor IS
        SELECT *
        FROM bulk_collect_table;

    TYPE fetch_collection_typ IS TABLE OF record_cursor%ROWTYPE;
    fetch_collection_variable fetch_collection_typ;

    TYPE collection_typ IS TABLE OF bulk_collect_table%ROWTYPE;
    collection_variable collection_typ;
BEGIN
    SELECT * BULK COLLECT INTO collection_variable FROM bulk_collect_table;

    FOR i IN 1..collection_variable.COUNT
    LOOP
        DBMS_OUTPUT.PUT_LINE(collection_variable(i).col1);
    END LOOP;

    collection_variable := null;
    OPEN record_cursor;
    FETCH record_cursor BULK COLLECT INTO collection_variable;
    CLOSE record_cursor;

    FOR i IN 1..collection_variable.COUNT
    LOOP
        DBMS_OUTPUT.PUT_LINE(collection_variable(i).col1+6);
    END LOOP;

    collection_variable := null;
    EXECUTE IMMEDIATE 'SELECT * FROM bulk_collect_table' BULK COLLECT INTO collection_variable;

    FOR i IN 1..collection_variable.COUNT
    LOOP
        DBMS_OUTPUT.PUT_LINE(collection_variable(i).col1+12);
    END LOOP;
END;
/

CALL bulk_collect_procedure();
```

##### Result 32

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|1|
|2|
|3|
|4|
|5|
|6|
|7|
|8|
|9|
|10|
|11|
|12|
|13|
|14|
|15|
|16|
|17|
|18|

##### Snowflake 19

Danger

EXECUTE IMMEDIATE with Bulk Collect clause has no workarounds offered.

###### Note 17

Please note, that while the FETCH Cursor can be mostly preserved, it is advised to be changed into
SELECT statements whenever possible for performance issues.

```sql
CREATE OR REPLACE PROCEDURE bulk_collect_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
        record_cursor CURSOR
        FOR
            SELECT *
            FROM
                bulk_collect_table;
--                !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--                TYPE fetch_collection_typ IS TABLE OF record_cursor%ROWTYPE;
    fetch_collection_variable VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'fetch_collection_typ' USAGE CHANGED TO VARIANT ***/!!!;
--                !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!

--    TYPE collection_typ IS TABLE OF bulk_collect_table%ROWTYPE;
    collection_variable VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'collection_typ' USAGE CHANGED TO VARIANT ***/!!!;
    BEGIN
                !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'RECORDS AND COLLECTIONS' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
                SELECT * BULK COLLECT INTO collection_variable FROM bulk_collect_table;
                --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                FOR i IN 1 TO 0 /*collection_variable.COUNT*/!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NESTED TABLE CUSTOM TYPE EXPRESSION' NODE ***/!!!
                --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                   LOOP
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            CALL DBMS_OUTPUT.PUT_LINE_UDF(:collection_variable(i).col1);
                   END LOOP;
                !!!RESOLVE EWI!!! /*** SSC-EWI-OR0108 - THE FOLLOWING ASSIGNMENT STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!

                collection_variable := null;
                OPEN record_cursor;
                --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
                record_cursor := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:record_cursor)
                );
                collection_variable := :record_cursor:RESULT;
                CLOSE record_cursor;
                --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                FOR i IN 1 TO 0 /*collection_variable.COUNT*/!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NESTED TABLE CUSTOM TYPE EXPRESSION' NODE ***/!!!
                --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                   LOOP
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            CALL DBMS_OUTPUT.PUT_LINE_UDF(
            !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!!
            :collection_variable(i).col1+6);
                   END LOOP;
                !!!RESOLVE EWI!!! /*** SSC-EWI-OR0108 - THE FOLLOWING ASSIGNMENT STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!

                collection_variable := null;
                !!!RESOLVE EWI!!! /*** SSC-EWI-0030 - THE STATEMENT BELOW HAS USAGES OF DYNAMIC SQL. ***/!!!
                EXECUTE IMMEDIATE 'SELECT * FROM
   bulk_collect_table'
                      !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'EXECUTE IMMEDIATE RETURNING CLAUSE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
                      BULK COLLECT INTO collection_variable;
                --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                FOR i IN 1 TO 0 /*collection_variable.COUNT*/!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NESTED TABLE CUSTOM TYPE EXPRESSION' NODE ***/!!!
                --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                   LOOP
            --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
            CALL DBMS_OUTPUT.PUT_LINE_UDF(
            !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!!
            :collection_variable(i).col1+12);
                   END LOOP;
    END;
$$;

CALL bulk_collect_procedure();
```

##### Result 33

<!-- prettier-ignore -->
|DBMS OUTPUT|
|---|
|1|
|2|
|3|
|4|
|5|
|6|
|7|
|8|
|9|
|10|
|11|
|– EXECUTE IMMEDIATE NOT EXECUTED, it’s not supported|

#### SELECT INTO statement case

In this case, the translation specification uses RESULTSETs. Review the documentation for WITH,
SELECT, and BULK COLLECT INTO statements here:

[with-select-and-bulk-collect-into-statements.md](#with-select-and-bulk-collect-into-statements)

### Known Issues 7

#### 1. Heavy performance issues on FETCH Cursor workaround

The workaround for the Fetch cursor has heavy performance requirements due to the Temporary table.
It is advised for them to be manually migrated to SELECT statements

##### 2. Execute immediate statements are not transformed

They are not supported by SnowConvert AI but may be manually changed to SELECT statements.

### Related EWIs 7

1. [SSC-EWI-0058](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058):
   Functionality is not currently supported by Snowflake Scripting.
2. [SSC-EWI-0062](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062):
   Custom type usage changed to variant.
3. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review
4. [SSC-EWI-OR0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0036):
   Types resolution issues, the arithmetic operation may not behave correctly between string and
   date.
5. [SSC-EWI-OR0108](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0108):
   The Following Assignment Statement is Not Supported by Snowflake Scripting.
6. [SSC-FDM-OR0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation.
7. [SSC-PRF-0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0001):
   This statement has usages of cursor fetch bulk operations.
8. [SSC-EWI-0030](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0030):
   The statement below has usages of dynamic SQL

## WITH, SELECT, and BULK COLLECT INTO statements

Danger

This section is a translation specification. Information may change in the future.

### Note 18

Some parts in the output code are omitted for clarity reasons.

### Description 7

This section is a translation specification for the statement WITH subsequent to a SELECT statement
which uses a BULK COLLECT INTO statement. For more information review the following documentation:

- [SELECT INTO Statement Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/SELECT-INTO-statement.html#GUID-6E14E04D-4344-45F3-BE80-979DD26C7A90).
- [SnowConvert AI Bulk Collect translation](#bulk-collect-from-a-table).

### Sample Source Patterns 7

#### Note 19

Some parts in the output code are omitted for clarity reasons.

The following query is used for the following examples.

#### Oracle 23

```sql
-- Sample MySampleTable table
CREATE TABLE MySampleTable (
  MySampleID NUMBER PRIMARY KEY,
  FirstName VARCHAR2(50),
  Salary NUMBER,
  Department VARCHAR2(50)
);

-- Insert some sample data
INSERT INTO MySampleTable (MySampleID, FirstName, Salary, Department)
VALUES (1, 'Bob One', 50000, 'HR');

INSERT INTO MySampleTable (MySampleID, FirstName, Salary, Department)
VALUES (2, 'Bob Two', 60000, 'HR');

INSERT INTO MySampleTable (MySampleID, FirstName, Salary, Department)
VALUES (3, 'Bob Three', 75000, 'IT');

INSERT INTO MySampleTable (MySampleID, FirstName, Salary, Department)
VALUES (4, 'Bob Four', 80000, 'IT');
```

##### Snowflake 20

```sql
-- Sample MySampleTable table
CREATE OR REPLACE TABLE MySampleTable (
   MySampleID NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/ PRIMARY KEY,
   FirstName VARCHAR(50),
   Salary NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
   Department VARCHAR(50)
 )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

-- Insert some sample data
INSERT INTO MySampleTable(MySampleID, FirstName, Salary, Department)
VALUES (1, 'Bob One', 50000, 'HR');

INSERT INTO MySampleTable(MySampleID, FirstName, Salary, Department)
VALUES (2, 'Bob Two', 60000, 'HR');

INSERT INTO MySampleTable(MySampleID, FirstName, Salary, Department)
VALUES (3, 'Bob Three', 75000, 'IT');

INSERT INTO MySampleTable(MySampleID, FirstName, Salary, Department)
VALUES (4, 'Bob Four', 80000, 'IT');
```

#### 1. Inside procedure simple case

Danger

This is an approach that uses a resultset data type. User-defined types must be reviewed. Review the
following
[Snowflake documentation](https://docs.snowflake.com/developer-guide/snowflake-scripting/resultsets)
to review more information about RESULTSETs.

The following example uses a User-defined type and it is declared indirectly as a table. The
translation for this case implements a RESULTSET as a data type in Snowflake. The resultset is
stored on a variable which must be returned wrapped on a `TABLE()` function.

##### Oracle 24

```sql
CREATE OR REPLACE PROCEDURE simple_procedure
IS
  TYPE salary_collection IS TABLE OF NUMBER;
  v_salaries salary_collection := salary_collection();

BEGIN
  WITH IT_Employees AS (
    SELECT Salary
    FROM MySampleTable
    WHERE Department = 'IT'
  )
  SELECT Salary BULK COLLECT INTO v_salaries
  FROM IT_Employees;
END;

CALL simple_procedure();
```

##### Result 34

###### Note 20

The query does not return results but the expected gathered information would be the IT Salary
Information used for the example:

<!-- prettier-ignore -->
|IT_Salary|
|---|
|75000|
|80000|

Danger

One of the limitations of the RESULTSETs is that they cannot be used as tables. E.g.:
`select * from my_result_set;` (This is an error, review the following
[documentation](https://docs.snowflake.com/developer-guide/snowflake-scripting/resultsets#limitations-of-the-resultset-data-type)
for more information).

##### Snowflake 21

```sql
CREATE OR REPLACE PROCEDURE simple_procedure ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  // SnowConvert AI Helpers Code section is omitted.

  !!!RESOLVE EWI!!! /*** SSC-EWI-OR0072 - PROCEDURAL MEMBER TYPE DEFINITION NOT SUPPORTED. ***/!!!
  /*   TYPE salary_collection IS TABLE OF NUMBER */
  ;
  !!!RESOLVE EWI!!! /*** SSC-EWI-OR0104 - UNUSABLE VARIABLE, ITS TYPE WAS NOT TRANSFORMED ***/!!!
  /*   v_salaries salary_collection := salary_collection() */
  ;
  EXEC(`SELECT Salary
    FROM
       MySampleTable
    WHERE Department = 'IT'`);
  [
    !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PlBulkCollectionItem' NODE ***/!!!
    //v_salaries
    null,V_SALARIES] = EXEC(`SELECT
   Salary
 FROM IT_Employees`);
$$;

CALL simple_procedure();
```

##### Result 35

<!-- prettier-ignore -->
|SALARY|
|---|
|77500|
|80000|

#### 2. Simple case for iterations: FOR LOOP statement

The following case is to define a translation for iteration with `FOR...LOOP`. In this case, the
User-defined type is implicitly a table, thus, it is possible to use a cursor to iterate. Review the
following documentation to learn more:

- Snowflake documentation about Returning a
  [Table for a Cursor.](https://docs.snowflake.com/developer-guide/snowflake-scripting/cursors#returning-a-table-for-a-cursor)
- In this case, there is a need to create a cursor for the iteration. Review the following
  [Cursor Assignment Syntax](https://docs.snowflake.com/sql-reference/snowflake-scripting/let#cursor-assignment-syntax)
  documentation.

##### Oracle 25

```sql
CREATE OR REPLACE PROCEDURE simple_procedure
IS
  TYPE salary_collection IS TABLE OF NUMBER;
  v_salaries salary_collection := salary_collection();
  v_average_salary NUMBER;
  salaries_count NUMBER;

BEGIN
  salaries_count := 0;
  WITH IT_Employees AS (
    SELECT Salary
    FROM MySampleTable
    WHERE Department = 'IT'
  )
  SELECT Salary BULK COLLECT INTO v_salaries
  FROM IT_Employees;

  -- Calculate the average salary
  IF v_salaries.COUNT > 0 THEN
    v_average_salary := 0;
    FOR i IN 1..v_salaries.COUNT LOOP
  v_average_salary := v_average_salary + v_salaries(i);
  salaries_count := salaries_count + 1;
    END LOOP;
    v_average_salary := v_average_salary / salaries_count;
  END IF;

  -- Display the average salary
  DBMS_OUTPUT.PUT_LINE('Average Salary for IT Department: ' || v_average_salary);
END;
/

CALL simple_procedure();
```

##### Result 36

```sql
Statement processed.
Average Salary for IT Department: 77500
```

##### Snowflake 22

```sql
CREATE OR REPLACE PROCEDURE simple_procedure ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
 DECLARE
--  !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'PL COLLECTION TYPE DEFINITION' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
--  TYPE salary_collection IS TABLE OF NUMBER;
  v_salaries VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'salary_collection' USAGE CHANGED TO VARIANT ***/!!! := salary_collection();
  v_average_salary NUMBER(38, 18);
  salaries_count NUMBER(38, 18);
 BEGIN
  salaries_count := 0;
  WITH IT_Employees AS
  (
    SELECT Salary
    FROM
     MySampleTable
    WHERE Department = 'IT'
  )
  !!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'RECORDS AND COLLECTIONS' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
  SELECT Salary BULK COLLECT INTO v_salaries
  FROM IT_Employees;
  -- Calculate the average salary
  IF (null /*v_salaries.COUNT*/!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NESTED TABLE CUSTOM TYPE EXPRESSION' NODE ***/!!! > 0) THEN
    v_average_salary := 0;
    --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    FOR i IN 1 TO 0 /*v_salaries.COUNT*/!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'NESTED TABLE CUSTOM TYPE EXPRESSION' NODE ***/!!!
                                                                                                                                                                           --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                                                                                                                                                           LOOP
     v_average_salary :=
     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN NUMBER AND salary_collection ***/!!!
     :v_average_salary + v_salaries(i);
     salaries_count := :salaries_count + 1;
                                                                                                                                                                              END LOOP;
    v_average_salary := :v_average_salary / :salaries_count;
  END IF;
  -- Display the average salary
  --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
  CALL DBMS_OUTPUT.PUT_LINE_UDF('Average Salary for IT Department: ' || NVL(:v_average_salary :: STRING, ''));
 END;
$$;

CALL simple_procedure();
```

##### Result 37

<!-- prettier-ignore -->
|SIMPLE_PROCEDURE|
|---|
|Average Salary for IT Department: 77500|

### Known Issues 8

#### 1. Resulset limitations

There are limitations while using the RESULTSET data type. Review the following
[Snowflake documentation](https://docs.snowflake.com/developer-guide/snowflake-scripting/resultsets#limitations-of-the-resultset-data-type)
to learn more. Markable limitations are the following:

- Declaring a column of type RESULTSET.
- Declaring a parameter of type RESULTSET.
- Declaring a stored procedure’s return type as a RESULTSET.

##### 2. Execute statements with Bulk Collect clause are not supported

Review the following [documentation](#bulk-collect-from-a-table).

### Related EWIs 8

1. [SSC-EWI-0058](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0058):
   Functionality is not currently supported by Snowflake Scripting.
2. [SSC-EWI-0062](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062):
   Custom type usage changed to variant.
3. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review
4. [SSC-EWI-OR0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0036):
   Types resolution issues, the arithmetic operation may not behave correctly between string and
   date.
5. [SSC-EWI-OR0072](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0072):
   Procedural Member not supported
6. [SSC-EWI-OR0104](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0104):
   Unusable collection variable.
7. [SSC-FDM-0006](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006):
   Number type column may not behave similarly in Snowflake.
8. [SSC-FDM-OR0035](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0035):
   DBMS_OUTPUT.PUTLINE check UDF implementation.
