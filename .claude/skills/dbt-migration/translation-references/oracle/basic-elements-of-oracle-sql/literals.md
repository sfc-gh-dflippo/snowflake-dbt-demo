---
description:
  The terms literal and constant value are synonymous and refer to a fixed data value. (Oracle SQL
  Language Reference Literals)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/literals
title: SnowConvert AI - Oracle - Literals | Snowflake Documentation
---

## Interval Literal[¶](#interval-literal)

Interval Literal Not Supported In Current Scenario

### Description[¶](#description)

Snowflake Intervals can only be used in arithmetic operations. Intervals used in any other scenario
are not supported.

#### Example Code[¶](#example-code)

##### Oracle[¶](#oracle)

```
SELECT INTERVAL '1-5' YEAR TO MONTH FROM DUAL;
```

Copy

##### Snowflake[¶](#snowflake)

```
SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-0107 - INTERVAL LITERAL IS NOT SUPPORTED BY SNOWFLAKE IN THIS SCENARIO  ***/!!!
 INTERVAL '1-5' YEAR TO MONTH FROM DUAL;
```

Copy

### Known Issues[¶](#known-issues)

No issues were found.

### Related EWIS[¶](#related-ewis)

1. [SSC-EWI-0107](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0107):
   Interval Literal Not Supported In Current Scenario.

## Interval Type and Date Type[¶](#interval-type-and-date-type)

Operation Between Interval Type and Date Type not Supported

### Description[¶](#id1)

`INTERVAL YEAR TO MONTH` and `INTERVAL DAY TO SECOND` are not a supported data type, they are
transformed to `VARCHAR(20)`. Therefore all arithmetic operations between **Date Types** and the
original **Interval Type Columns** are not supported.

Furthermore, operations between an Interval Type and Date Type (in this order) are not supported in
Snowflake; and these operations use this EWI as well.

#### Example Code[¶](#id2)

##### Oracle[¶](#id3)

```
CREATE TABLE table_with_intervals
(
    date_col DATE,
    time_col TIMESTAMP,
    intervalYearToMonth_col INTERVAL YEAR TO MONTH,
    intervalDayToSecond_col INTERVAL DAY TO SECOND
);

-- Date + Interval Y to M
SELECT date_col + intervalYearToMonth_col FROM table_with_intervals;

-- Date - Interval D to S
SELECT date_col - intervalDayToSecond_col FROM table_with_intervals;

-- Timestamp + Interval D to S
SELECT time_col + intervalDayToSecond_col FROM table_with_intervals;

-- Timestamp - Interval Y to M
SELECT time_col - intervalYearToMonth_col FROM table_with_intervals;
```

Copy

##### Snowflake[¶](#id4)

```
CREATE OR REPLACE TABLE table_with_intervals
    (
        date_col TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/,
        time_col TIMESTAMP(6),
        intervalYearToMonth_col VARCHAR(20) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL YEAR TO MONTH DATA TYPE CONVERTED TO VARCHAR ***/!!!,
        intervalDayToSecond_col VARCHAR(20) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - INTERVAL DAY TO SECOND DATA TYPE CONVERTED TO VARCHAR ***/!!!
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;

    -- Date + Interval Y to M
    SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!! date_col + intervalYearToMonth_col FROM
    table_with_intervals;

    -- Date - Interval D to S
SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!! date_col - intervalDayToSecond_col FROM
    table_with_intervals;

    -- Timestamp + Interval D to S
SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!! time_col + intervalDayToSecond_col FROM
    table_with_intervals;

    -- Timestamp - Interval Y to M
SELECT
    !!!RESOLVE EWI!!! /*** SSC-EWI-OR0095 - OPERATION BETWEEN INTERVAL TYPE AND DATE TYPE NOT SUPPORTED ***/!!! time_col - intervalYearToMonth_col FROM
    table_with_intervals;
```

Copy

#### Recommendations[¶](#recommendations)

- Implement the UDF to simulate the Oracle behavior.
- Extract the already transformed value that was stored in the column during migration, and use it
  as a Snowflake
  [**Interval Constant**](https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#interval-constants)
  when possible.
- If you need more support, you can email us at
  [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)

### Related EWIS[¶](#id5)

1. [SSC-EWI-0036](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0036):
   Data type converted to another data type.
2. [SSC-EWI-OR0095](../../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI.html#ssc-ewi-or0095):
   Operation Between Interval Type and Date Type not Supported.
3. [SSC-FDM-OR0042](../../../general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM.html#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior.

## Text literals[¶](#text-literals)

### Description[¶](#id6)

> Use the text literal notation to specify values whenever `string` appears in the syntax of
> expressions, conditions, SQL functions, and SQL statements in other parts of this reference.
>
> ([Oracle SQL Language Reference Text literals](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Literals.html#GUID-1824CBAA-6E16-4921-B2A6-112FB02248DA))

```
[ {N | n} ]
{ '[ c ]...'
<!-- prettier-ignore -->
|{ Q|q } 'quote_delimiter c [ c ]... quote_delimiter'
}
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns)

#### Empty string (‘’)[¶](#empty-string)

The empty strings are equivalent to _NULL_ in Oracle, so in order to emulate the behavior in
Snowflake, the empty strings are converted to _NULL_ or _undefined_ depending if the literal is used
inside a procedure or not.

##### Oracle[¶](#id7)

```
SELECT UPPER('') FROM DUAL;
```

Copy

##### Result[¶](#result)

<!-- prettier-ignore -->
|UPPER(‘’)|
|---|
|           |

##### Snowflake[¶](#id8)

```
SELECT UPPER(NULL) FROM DUAL;
```

Copy

##### Result[¶](#id9)

<!-- prettier-ignore -->
|UPPER(NULL)|
|---|
|             |

#### Empty string in stored procedures[¶](#empty-string-in-stored-procedures)

##### Oracle[¶](#id10)

```
CREATE TABLE empty_string_table(
col1 VARCHAR(10),
col2 VARCHAR(10));

CREATE OR REPLACE PROCEDURE null_proc AS
    var1 INTEGER := '';
    var3 INTEGER := null;
    var2 VARCHAR(20) := 'hello';
BEGIN
    var1 := var1 + 456;
    var2 := var2 || var1;
    IF var1 IS NULL THEN
        INSERT INTO empty_string_table VALUES (var1, var2);
    END IF;
END;

CALL null_proc();

SELECT * FROM empty_string_table;
```

Copy

##### Result[¶](#id11)

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
||hello|

##### Snowflake[¶](#id12)

```
CREATE OR REPLACE TABLE empty_string_table (
    col1 VARCHAR(10),
    col2 VARCHAR(10))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

CREATE OR REPLACE PROCEDURE null_proc ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        var1 INTEGER := NULL;
        var3 INTEGER := null;
        var2 VARCHAR(20) := 'hello';
    BEGIN
        var1 := :var1 + 456;
        var2 := NVL(:var2 :: STRING, '') || NVL(:var1 :: STRING, '');
        IF (:var1 IS NULL) THEN
            INSERT INTO empty_string_table
            VALUES (:var1, :var2);
        END IF;
    END;
$$;

CALL null_proc();

SELECT * FROM
    empty_string_table;
```

Copy

##### Result[¶](#id13)

<!-- prettier-ignore -->
|COL1|COL2|
|---|---|
||hello|

#### Empty string in built-in functions[¶](#empty-string-in-built-in-functions)

Warning

The transformation does not apply when the empty string is used as an argument of the _REPLACE_ and
_CONCAT_ functions in order to keep the functional equivalence.

##### Oracle[¶](#id14)

```
SELECT REPLACE('Hello world', '', 'l'), CONCAT('A','') FROM DUAL;
```

Copy

##### Result[¶](#id15)

<!-- prettier-ignore -->
|REPLACE(‘HELLOWORLD’,’’,’L’)|CONCAT(‘A’,’’)|
|---|---|
|Hello world|A|

##### Snowflake[¶](#id16)

```
SELECT REPLACE('Hello world', '', 'l'), CONCAT('A','') FROM DUAL;
```

Copy

##### Result[¶](#id17)

<!-- prettier-ignore -->
|REPLACE(‘HELLO WORLD’, ‘’, ‘L’)|CONCAT(‘A’,’’)|
|---|---|
|Hello world|A|

Note

If the empty strings are replaced by NULL for these cases, the results of the queries will be
different.

### Known Issues[¶](#id18)

No issues were found.

### Related EWIs[¶](#id19)

No related EWIs.
