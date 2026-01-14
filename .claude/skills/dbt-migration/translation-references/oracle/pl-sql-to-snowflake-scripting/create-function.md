---
description: Oracle Create Function to Snowflake Snow Scripting
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pl-sql-to-snowflake-scripting/create-function
title: SnowConvert AI - Oracle - CREATE FUNCTION | Snowflake Documentation
---

## Description[¶](#description)

**Note:**

Some parts in the output code are omitted for clarity reasons.

> A **stored function** (also called a **user function** or **user-defined function**) is a set of
> PL/SQL statements you can call by name. Stored functions are very similar to procedures, except
> that a function returns a value to the environment in which it is called. User functions can be
> used as part of a SQL expression.
>
> A **call specification** declares a Java method or a third-generation language (3GL) routine so
> that it can be called from PL/SQL. You can also use the `CALL` SQL statement to call such a method
> or routine. The call specification tells Oracle Database which Java method, or which named
> function in which shared library, to invoke when a call is made. It also tells the database what
> type conversions to make for the arguments and return value.
> [Oracle SQL Language Reference Create Function](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/CREATE-FUNCTION.html).

### Oracle Syntax[¶](#oracle-syntax)

For more information regarding Oracle Create Function, check
[here](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/CREATE-FUNCTION-statement.html).

#### Oracle Create Function Syntax[¶](#oracle-create-function-syntax)

```
CREATE [ OR REPLACE ] [ EDITIONABLE | NONEDITIONABLE ]
FUNCTION
[ schema. ] function_name
  [ ( parameter_declaration [, parameter_declaration]... ) ] RETURN datatype
[ sharing_clause ]
  [ { invoker_rights_clause
    | accessible_by_clause
    | default_collation_clause
    | deterministic_clause
    | parallel_enable_clause
    | result_cache_clause
    | aggregate_clause
    | pipelined_clause
    | sql_macro_clause
       }...
  ]
{ IS | AS } { [ declare_section ]
    BEGIN statement ...
    [ EXCEPTION exception_handler [ exception_handler ]... ]
    END [ name ] ;
      |
    { java_declaration | c_declaration } } ;
```

### Snowflake Syntax[¶](#snowflake-syntax)

Snowflake allows 3 different languages in their user-defined functions:

- SQL
- JavaScript
- Java

For now, SnowConvert AI will support only `SQL` and `JavaScript` as target languages.

For more information regarding Snowflake Create Function, check
[here](https://docs.snowflake.com/en/developer-guide/udf/udf-overview).

#### SQL[¶](#sql)

**Note:**

SQL user-defined functions only support one query as their body. They can read from the database but
are not allowed to write to or modify it
([Scalar SQL UDFs](https://docs.snowflake.com/en/developer-guide/udf/sql/udf-sql-scalar-functions.html)).

```
CREATE [ OR REPLACE ] [ SECURE ] FUNCTION <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<function_definition>'
```

##### JavaScript[¶](#javascript)

**Note:**

JavaScript user-defined functions allow multiple statements in their bodies but cannot perform
queries to the database.
([Scalar JavaScript UDFs](https://docs.snowflake.com/en/developer-guide/udf/javascript/udf-javascript-scalar-functions)).

```
CREATE [ OR REPLACE ] [ SECURE ] FUNCTION <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE JAVASCRIPT
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<function_definition>'
```

## Sample Source Patterns[¶](#sample-source-patterns)

### Sample auxiliary data[¶](#sample-auxiliary-data)

**Note:**

This code was executed for a better understanding of the examples:

#### Oracle[¶](#oracle)

```
CREATE TABLE table1 (col1 int, col2 int, col3 varchar2(250), col4 varchar2(250), col5 date);

INSERT INTO table1 VALUES (1, 11, 'val1_1', 'val1_2', TO_DATE('2004/05/03', 'yyyy-MM-dd'));
INSERT INTO table1 VALUES (2, 22, 'val2_1', 'val2_2', TO_DATE('2014/05/03', 'yyyy-MM-dd'));
INSERT INTO table1 VALUES (3, 33, 'val3_1', 'val3_2', TO_DATE('2024/05/03', 'yyyy-MM-dd'));
```

##### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE TABLE table1 (col1 int,
col2 int,
col3 VARCHAR(250),
col4 VARCHAR(250),
col5 TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/25/2024" }}'
;

INSERT INTO table1
VALUES (1, 11, 'val1_1', 'val1_2', TO_DATE('2004/05/03', 'yyyy-MM-dd'));

INSERT INTO table1
VALUES (2, 22, 'val2_1', 'val2_2', TO_DATE('2014/05/03', 'yyyy-MM-dd'));

INSERT INTO table1
VALUES (3, 33, 'val3_1', 'val3_2', TO_DATE('2024/05/03', 'yyyy-MM-dd'));
```

## Known Issues[¶](#known-issues)

No issues were found.

## Related EWIS[¶](#related-ewis)

1. [SSC-FDM-OR0042](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior

## Cursor for a return variable[¶](#cursor-for-a-return-variable)

**Note:**

Some parts in the output code are omitted for clarity reasons.

This pattern defines a function in Oracle PL/SQL that uses a cursor to fetch a single value and
return it.

**Components:**

1. **Function Declaration:**

   - `CREATE FUNCTION functionName(parameters) RETURN returnType`
   - Declares the function with input parameters and the return type.

2. **Variable Declarations:**

   - Declares variables, including the return variable.

3. **Cursor Declaration:**

   - `CURSOR cursorName IS SELECT singleColumn FROM ... WHERE ... [AND col1 = localVar1];`
   - Defines a cursor to select a single column from a table with optional filtering conditions.

4. **BEGIN-END Block:**

   - Variables assignment.
   - Opens the cursor.
   - Fetch the result into the return variable.
   - Closes the cursor.
   - Returns the fetched value.

In this case, the variables are transformed into a common table expression (CTE). As well as the
query within the cursor to which, in addition, the `FETCH FIRST 1 ROW ONLY` clause is added to
simulate the `FETCH CURSOR` behavior.

`RETURN` statement is transformed to the final select.

### Queries[¶](#queries)

#### Oracle[¶](#id1)

```
CREATE OR REPLACE FUNCTION func1 (
   company_ IN VARCHAR2,
   book_id_ IN DATE,
   object_id_ IN VARCHAR2 ) RETURN INTEGER
IS
   temp_ table1.col2%TYPE;
   CURSOR get_attr IS
      SELECT col2
      FROM table1
      WHERE col3 = company_
      AND   col4 = object_id_
      AND   col5 = book_id_;
BEGIN
   OPEN get_attr;
   FETCH get_attr INTO temp_;
   CLOSE get_attr;
   RETURN temp_;
END func1;
```

##### Snowflake[¶](#id2)

```
CREATE OR REPLACE FUNCTION func1 (company_ VARCHAR, book_id_ TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/, object_id_ VARCHAR)
RETURNS INTEGER
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         (
         SELECT col2
         FROM table1
         WHERE col3 = company_
         AND   col4 = object_id_
         AND   col5 = book_id_
         FETCH FIRST 1 ROW ONLY) AS temp_
   )
   SELECT
      temp_
   FROM
      declaration_variables_cte1
$$;
```

##### Result[¶](#result)

<!-- prettier-ignore -->
|FUNC1()|
|---|
|2004-05-03.|

##### Oracle[¶](#id3)

```
CREATE FUNCTION func2 (
   fa_period_   IN NUMBER,
   to_date_     IN DATE DEFAULT NULL,
   from_date_   IN DATE DEFAULT NULL ) RETURN NUMBER
IS
   value_                    NUMBER;
   cond_date_to_             DATE;
   cond_date_from_           DATE;
   CURSOR get_acq_value IS
      SELECT NVL(SUM(col1),0)
      FROM   table1
      WHERE  col3                   IN (DECODE(fa_period_, 1, 'val1_1', 'val2_1'))
      AND    col5           <= cond_date_to_
      AND    col5           >= cond_date_from_;
BEGIN
   value_ := 0;
   cond_date_to_       := Get_Cond_Date( to_date_, 'MAX' );
   cond_date_from_     := Get_Cond_Date( from_date_, 'MIN' );
   OPEN get_acq_value;
   FETCH get_acq_value INTO value_;
   CLOSE get_acq_value;
   RETURN (NVL(value_,0));
END func2;
```

##### Snowflake[¶](#id4)

```
CREATE OR REPLACE FUNCTION func2 (fa_period_ NUMBER(38, 18),
  to_date_ TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/ DEFAULT NULL,
  from_date_ TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/ DEFAULT NULL )
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         0 AS
         value_,
         Get_Cond_Date( to_date_, 'MAX' ) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Get_Cond_Date' NODE ***/!!! AS
         cond_date_to_,
         Get_Cond_Date( from_date_, 'MIN' ) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Get_Cond_Date' NODE ***/!!! AS
         cond_date_from_
   ),
   declaration_variables_cte2 AS
   (
      SELECT
         (
         SELECT NVL(SUM(col1),0)
         FROM   table1
         WHERE  col3                   IN (DECODE(fa_period_, 1, 'val1_1', 'val2_1'))
         AND    col5           <= cond_date_to_
         AND    col5           >= cond_date_from_
         FETCH FIRST 1 ROW ONLY) AS value_,
         cond_date_to_,
         cond_date_from_
      FROM
         declaration_variables_cte1
   )
   SELECT
      (NVL(value_,0))
   FROM
      declaration_variables_cte2
$$;
```

##### Result[¶](#id5)

<!-- prettier-ignore -->
|FUNC1()|
|---|
|2004-05-03.|

### Known Issues[¶](#id6)

No issues were found.

### Related EWIS[¶](#id7)

1. [SSC-FDM-OR0042](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior.
2. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.

## Cursor with IF statement[¶](#cursor-with-if-statement)

**Note:**

Some parts in the output code are omitted for clarity reasons.

This pattern defines a function that conditionally uses a cursor to fetch and return a value based
on an `IF` statement.

**Components:**

1. **Function Declaration:**

   - `CREATE FUNCTION functionName(parameters) RETURN returnType`
   - Declares the function with input parameters and the return type.

2. **Cursor Declaration:**

   - `CURSOR cursorName IS SELECT singleColumn FROM ... WHERE ... [AND col1 = localVar1];`
   - Defines a cursor to select a single column from a table with optional filtering conditions.

3. **Variable Declaration:**

   - Declares variables, including the return variable.

4. **BEGIN-END Block with IF Statement:**

   - Variables assignment.
   - Check if a condition is true.
   - If true, opens the cursor, fetches the result into the return variable, closes the cursor, and
     returns the fetched value. (The cursor can also be opened in the `ELSE` block and must meet the
     same conditions)
   - The `ELSE` Block is optional, if it exists, it should only contain a single statement that can
     be an assignment or a `RETURN` statement.

The variables are transformed into a common table expression (CTE). As well as the query within the
cursor to which, in addition, the `FETCH FIRST 1 ROW ONLY` clause is added to simulate the
`FETCH CURSOR` behavior.

`IF/ELSE` statement can be handled using the
[`CASE EXPRESSION`](https://docs.snowflake.com/en/sql-reference/functions/case) inside the select
allowing conditionals inside the queries. `RETURN` statement is transformed to the final select..

### Queries[¶](#id8)

#### Oracle[¶](#id9)

```
CREATE OR REPLACE FUNCTION func1 (
   company_          IN NUMBER) RETURN NUMBER
IS
   CURSOR getmaxperiod IS
      SELECT max(col2)
      FROM   table1;
   max_period_               NUMBER := 12;
BEGIN
   IF 1 = 1 THEN
      OPEN   getmaxperiod;
      FETCH  getmaxperiod INTO max_period_ ;
      CLOSE  getmaxperiod;
      RETURN max_period_;
   ELSE
      RETURN NULL;
   END IF;
END func1;
```

##### Snowflake[¶](#id10)

```
CREATE OR REPLACE FUNCTION func1 (company_ NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte0 AS
   (
      SELECT
         12 AS
         max_period_
   ),
   declaration_variables_cte1 AS
   (
      SELECT
         CASE
            WHEN 1 = 1
               THEN (
               SELECT max(col2)
               FROM   table1
               FETCH FIRST 1 ROW ONLY)
            ELSE NULL
         END AS max_period_
      FROM
         declaration_variables_cte0
   )
   SELECT
      max_period_
   FROM
      declaration_variables_cte1
$$;
```

##### Result[¶](#id11)

<!-- prettier-ignore -->
|FUNC2(0)|
|---|
|NULL|

<!-- prettier-ignore -->
|FUNC2(1)|
|---|
|33|

##### Oracle[¶](#id12)

```
CREATE OR REPLACE FUNCTION func2(
   company_          IN NUMBER) RETURN NUMBER
IS
   CURSOR getmaxperiod IS
      SELECT max(col2)
      FROM   table1;
   max_period_               NUMBER := 1;
BEGIN
   max_period_:= 2;
   IF company_ = 1 THEN
      RETURN max_period_ * 2;
   ELSE
      OPEN   getmaxperiod;
      FETCH  getmaxperiod INTO max_period_ ;
      CLOSE  getmaxperiod;
      RETURN max_period_;
   END IF;
END func2;
```

##### Snowflake[¶](#id13)

```
CREATE OR REPLACE FUNCTION func2 (company_ NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte0 AS
   (
      SELECT
         1 AS
         max_period_
   ),
   declaration_variables_cte1 AS
   (
      SELECT
         2 AS
         max_period_
      FROM
         declaration_variables_cte0
   ),
   declaration_variables_cte2 AS
   (
      SELECT
         CASE
            WHEN company_ = 1
               THEN max_period_ * 2
            ELSE (
            SELECT max(col2)
            FROM   table1
            FETCH FIRST 1 ROW ONLY)
         END AS max_period_
      FROM
         declaration_variables_cte1
   )
   SELECT
      max_period_
   FROM
      declaration_variables_cte2
$$;
```

##### Result[¶](#id14)

<!-- prettier-ignore -->
|FUNC2(0)|
|---|
|33|

<!-- prettier-ignore -->
|FUNC2(1)|
|---|
|2|

##### Oracle[¶](#id15)

```
CREATE OR REPLACE FUNCTION func3 (
   company_          IN NUMBER) RETURN NUMBER
IS
   CURSOR getmaxperiod IS
      SELECT max(col2)
      FROM   table1;
   max_period_               NUMBER := 0;
BEGIN
   IF company_ = 1 THEN
      OPEN   getmaxperiod;
      FETCH  getmaxperiod INTO max_period_ ;
      CLOSE  getmaxperiod;
   END IF;
   RETURN max_period_;
END func10;
```

##### Snowflake[¶](#id16)

```
CREATE OR REPLACE FUNCTION func3 (company_ NUMBER(38, 18))
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte0 AS
   (
      SELECT
         0 AS
         max_period_
   ),
   declaration_variables_cte1 AS
   (
      SELECT
         CASE
            WHEN company_ = 1
               THEN (
               SELECT max(col2)
               FROM   table1
               FETCH FIRST 1 ROW ONLY)
            ELSE max_period_
         END AS max_period_
      FROM
         declaration_variables_cte0
   )
   SELECT
      max_period_
   FROM
      declaration_variables_cte1
$$;
```

##### Result[¶](#id17)

<!-- prettier-ignore -->
|FUNC2(0)|
|---|
|0|

<!-- prettier-ignore -->
|FUNC2(1)|
|---|
|33|

### Known Issues[¶](#id18)

No issues were found.

### Related EWIS[¶](#id19)

No EWIs related.

## Multiples IFs statement[¶](#multiples-ifs-statement)

This pattern defines a function that uses conditional statements over local variables.

**Components:**

1. **Function Declaration:**

   - `CREATE FUNCTION functionName(parameters) RETURN returnType`
   - Declares the function with input parameters and the return type.

2. **Variable Declaration:**

   - Declares variables, including the return variable.

3. **BEGIN-END Block with IF Statement:**

   - Check if a condition is true.
   - Each case is used to assign a value over the same variable.

### Conversion:[¶](#conversion)

**`DECLARE SECTION`** : variables with default an expression are moved to a common table expression.

**`IF/ELSE`** statement can be handled using the
[`CASE EXPRESSION`](https://docs.snowflake.com/en/sql-reference/functions/case) inside the select
allowing conditionals inside the queries.

**`RETURN`** statement is transformed to the final select.

#### Oracle[¶](#id20)

```
CREATE OR REPLACE FUNCTION Case1 (
   in_date_ IN DATE,
   min_max_ IN VARCHAR2 )
RETURN DATE
IS
   cond_date_  DATE := CURRENT_DATE;
BEGIN
   IF ( in_date_ IS NULL ) THEN
      IF ( min_max_ = 'MIN' ) THEN
         cond_date_ := FOO1();
      ELSE
         cond_date_ := FOO2();
      END IF;
   ELSE
      cond_date_ := TRUNC(in_date_);
   END IF;
   RETURN cond_date_;
END Case1;
```

#### Snowflake[¶](#id21)

```
CREATE OR REPLACE FUNCTION Case1 (in_date_ TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/, min_max_ VARCHAR)
RETURNS TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte0 AS
   (
      SELECT
         CURRENT_DATE AS
         cond_date_
   ),
   declaration_variables_cte1 AS
   (
      SELECT
         CASE
            WHEN ( in_date_ IS NULL )
               THEN CASE
                  WHEN ( min_max_ = 'MIN' )
                     THEN FOO1() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO1' NODE ***/!!!
                  ELSE FOO2() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO2' NODE ***/!!!
               END
            ELSE TRUNC(in_date_, 'DD')
         END AS cond_date_
      FROM
         declaration_variables_cte0
   )
   SELECT
      cond_date_
   FROM
      declaration_variables_cte1
$$;
```

#### Oracle[¶](#id22)

```
CREATE OR REPLACE FUNCTION Case2 (
   year_        IN NUMBER,
   id           IN NUMBER)
   RETURN VARCHAR2
IS
   base_value_        NUMBER;
   fully_depritiated_ VARCHAR2(5);
   residual_value_    NUMBER;
   acc_depr_prev_     NUMBER;
   acc_depr_          NUMBER;
BEGIN

   base_value_     := FOO1(year_, id);
   acc_depr_       := FOO2(year_, id);
   acc_depr_prev_  := FOO3(year_, id);
   residual_value_ := NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_);

   IF (residual_value_=0 AND base_value_!=0) THEN
      fully_depritiated_ := 'TRUE';
   ELSE
      fully_depritiated_ := 'FALSE';
   END IF;

   RETURN fully_depritiated_;
END Case2;
```

#### Snowflake[¶](#id23)

```
CREATE OR REPLACE FUNCTION Case2 (year_ NUMBER(38, 18), id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         FOO1(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO1' NODE ***/!!! AS

         base_value_,
         FOO2(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO2' NODE ***/!!! AS
         acc_depr_,
         FOO3(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO3' NODE ***/!!! AS
         acc_depr_prev_,
         !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN NUMBER AND unknown ***/!!!
         NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_) AS
         residual_value_,
         CASE
            WHEN (residual_value_=0 AND base_value_!=0)
               THEN 'TRUE'
            ELSE 'FALSE'
         END AS fully_depritiated_
   )
   SELECT
      fully_depritiated_
   FROM
      declaration_variables_cte1
$$;
```

#### Oracle[¶](#id24)

```
CREATE OR REPLACE FUNCTION Case2_1 (
   year_        IN NUMBER,
   id           IN NUMBER)
   RETURN VARCHAR2
IS
   base_value_        NUMBER;
   fully_depritiated_ VARCHAR2(5);
   residual_value_    NUMBER;
   acc_depr_prev_     NUMBER;
   acc_depr_          NUMBER;
BEGIN

   base_value_     := FOO1(year_, id);
   acc_depr_       := FOO2(year_, id);
   acc_depr_prev_  := FOO3(year_, id);
   residual_value_ := NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_);

   IF (residual_value_=0 AND base_value_!=0) THEN
      fully_depritiated_ := 'TRUE';
   ELSE
      fully_depritiated_ := 'FALSE';
   END IF;

   fully_depritiated := fully_depritiated || ' CONCAT FOR TESTING';
   fully_depritiated := fully_depritiated || ' CONCAT FOR TESTING2';
   RETURN fully_depritiated_;
END Case2;
```

#### Snowflake[¶](#id25)

```
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "FOO1", "FOO2", "FOO3" **
CREATE OR REPLACE FUNCTION Case2_1 (year_ NUMBER(38, 18), id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         FOO1(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO1' NODE ***/!!! AS

         base_value_,
         FOO2(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO2' NODE ***/!!! AS
         acc_depr_,
         FOO3(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO3' NODE ***/!!! AS
         acc_depr_prev_,
         !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN NUMBER AND unknown ***/!!!
         NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_) AS
         residual_value_,
         CASE
            WHEN (residual_value_=0 AND base_value_!=0)
               THEN 'TRUE'
            ELSE 'FALSE'
         END AS fully_depritiated_,
         NVL(fully_depritiated :: STRING, '') || ' CONCAT FOR TESTING' AS

         fully_depritiated
   ),
   declaration_variables_cte2 AS
   (
      SELECT
         NVL(fully_depritiated :: STRING, '') || ' CONCAT FOR TESTING2' AS
         fully_depritiated,
         base_value_,
         acc_depr_,
         acc_depr_prev_,
         residual_value_
      FROM
         declaration_variables_cte1
   )
   SELECT
      fully_depritiated_
   FROM
      declaration_variables_cte2
$$;
```

#### Oracle[¶](#id26)

```
CREATE OR REPLACE FUNCTION Case2_1 (
   year_        IN NUMBER,
   id           IN NUMBER)
   RETURN VARCHAR2
IS
   base_value_        NUMBER;
   fully_depritiated_ VARCHAR2(5);
   residual_value_    NUMBER;
   acc_depr_prev_     NUMBER;
   acc_depr_          NUMBER;
BEGIN

   base_value_     := FOO1(year_, id);
   acc_depr_       := FOO2(year_, id);
   acc_depr_prev_  := FOO3(year_, id);
   residual_value_ := NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_);

   IF (residual_value_=0 AND base_value_!=0) THEN
      fully_depritiated_ := 'TRUE';
   ELSE
      fully_depritiated_ := 'FALSE';
   END IF;

   fully_depritiated := fully_depritiated || ' CONCAT FOR TESTING';
   fully_depritiated := fully_depritiated || ' CONCAT FOR TESTING2';
   RETURN fully_depritiated_;
END Case2;
```

#### Snowflake[¶](#id27)

```
CREATE OR REPLACE FUNCTION Case2_1 (year_ NUMBER(38, 18), id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "09/06/2024" }}'
AS
$$
   WITH declaration_variables_cte1 AS
   (
      SELECT
         FOO1(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO1' NODE ***/!!! AS

         base_value_,
         FOO2(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO2' NODE ***/!!! AS
         acc_depr_,
         FOO3(year_, id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'FOO3' NODE ***/!!! AS
         acc_depr_prev_,
         !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN NUMBER AND unknown ***/!!!
         NVL(base_value_,0) -(acc_depr_ + acc_depr_prev_) AS
         residual_value_,
         CASE
            WHEN (residual_value_=0 AND base_value_!=0)
               THEN 'TRUE'
            ELSE 'FALSE'
         END AS fully_depritiated_,
         NVL(fully_depritiated :: STRING, '') || ' CONCAT FOR TESTING' AS

         fully_depritiated
   ),
   declaration_variables_cte2 AS
   (
      SELECT
         NVL(fully_depritiated :: STRING, '') || ' CONCAT FOR TESTING2' AS
         fully_depritiated,
         base_value_,
         acc_depr_,
         acc_depr_prev_,
         residual_value_
      FROM
         declaration_variables_cte1
   )
   SELECT
      fully_depritiated_
   FROM
      declaration_variables_cte2
$$;
```

### Known Issues[¶](#id28)

No issues were found.

### Related EWIS[¶](#id29)

1. [SSC-FDM-OR0042](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior.
2. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
3. [SSC-EWI-OR0036](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0036):
   Types resolution issues, the arithmetic operation may not behave correctly between string and
   date.

## Snowflake Script UDF (SCALAR)[¶](#snowflake-script-udf-scalar)

Translation reference for Oracle User Defined Functions to
[Snowflake Scripting UDFs](https://docs.snowflake.com/en/migrations/snowconvert-docs/developer-guide/udf/sql/udf-sql-procedural-functions)

**Note:**

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id30)

SnowConvert now supports translating Oracle PL/SQL User Defined Functions directly to **Snowflake
Scripting UDFs** (SnowScript UDFs) when they meet specific criteria.

**Snowflake Scripting UDFs** are user-defined functions written using Snowflake’s procedural
language syntax (Snowscript) within a SQL UDF body. They support variables, loops, conditional
logic, and exception handling without requiring database access.

#### When Functions Become SnowScript UDFs[¶](#when-functions-become-snowscript-udfs)

SnowConvert analyzes each Oracle function and automatically determines the appropriate Snowflake
target. A function becomes a SnowScript UDF when it contains **only** procedural logic without data
access operations.

### Sample Source Patterns[¶](#id31)

#### Simple Calculation Function[¶](#simple-calculation-function)

A basic function that performs calculations without querying data.

##### Oracle[¶](#id32)

```
CREATE OR REPLACE FUNCTION CalculateTax (
    amount_ IN NUMBER,
    tax_rate_ IN NUMBER
) RETURN NUMBER
IS
    tax_amount_ NUMBER;
BEGIN
    tax_amount_ := amount_ * (tax_rate_ / 100);
    RETURN tax_amount_;
END CalculateTax;
```

##### Result[¶](#id33)

<!-- prettier-ignore -->
|CALCULATETAX(1000, 15)|
|---|
|150|

##### Snowflake (SnowScript UDF)[¶](#snowflake-snowscript-udf)

```
CREATE OR REPLACE FUNCTION CalculateTax (amount_ NUMBER(38, 18), tax_rate_ NUMBER(38, 18)
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "zsqZAVE5n32hZZFtsi0zsg==" }}'
AS
$$
   DECLARE
      tax_amount_ NUMBER(38, 18);
   BEGIN
      tax_amount_ := :amount_ * (:tax_rate_ / 100);
      RETURN :tax_amount_;
   END;
$$;
```

##### Result[¶](#id34)

<!-- prettier-ignore -->
|CALCULATETAX(1000, 15)|
|---|
|150|

#### Function with IF/ELSIF/ELSE Logic[¶](#function-with-if-elsif-else-logic)

Functions using conditional statements for business logic.

##### Oracle[¶](#id35)

```
CREATE OR REPLACE FUNCTION GetShippingCost (
    distance_ IN NUMBER,
    weight_ IN NUMBER
) RETURN NUMBER
IS
    shipping_cost_ NUMBER := 0;
BEGIN
    IF distance_ < 50 THEN
        shipping_cost_ := 10;
    ELSIF distance_ < 100 THEN
        shipping_cost_ := 20;
    ELSIF distance_ < 200 THEN
        shipping_cost_ := 35;
    ELSE
        shipping_cost_ := 50;
    END IF;

    IF weight_ > 20 THEN
        shipping_cost_ := shipping_cost_ * 1.5;
    END IF;

    RETURN shipping_cost_;
END GetShippingCost;
```

##### Result[¶](#id36)

<!-- prettier-ignore -->
|GETSHIPPINGCOST(75, 25)|
|---|
|30|

##### Snowflake (SnowScript UDF)[¶](#id37)

```
CREATE OR REPLACE FUNCTION GetShippingCost (distance_ NUMBER(38, 18), weight_ NUMBER(38, 18)
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "zsqZAVE5n32hZZFtsi0zsg==" }}'
AS
$$
   DECLARE
      shipping_cost_ NUMBER(38, 18) := 0;
   BEGIN
      IF (:distance_ < 50) THEN
         shipping_cost_ := 10;
      ELSEIF (:distance_ < 100) THEN
         shipping_cost_ := 20;
      ELSEIF (:distance_ < 200) THEN
         shipping_cost_ := 35;
    ELSE
         shipping_cost_ := 50;
      END IF;
      IF (:weight_ > 20) THEN
         shipping_cost_ := :shipping_cost_ * 1.5;
      END IF;
      RETURN :shipping_cost_;
   END;
$$;
```

##### Result[¶](#id38)

<!-- prettier-ignore -->
|GETSHIPPINGCOST(75, 25)|
|---|
|30|

#### Function with FOR Loop[¶](#function-with-for-loop)

Functions using loops for iterative calculations.

##### Oracle[¶](#id39)

```
CREATE OR REPLACE FUNCTION CalculateCompoundInterest (
    principal_ IN NUMBER,
    rate_ IN NUMBER,
    years_ IN NUMBER
) RETURN NUMBER
IS
    amount_ NUMBER;
    i NUMBER;
BEGIN
    amount_ := principal_;

    FOR i IN 1..years_ LOOP
        amount_ := amount_ * (1 + rate_ / 100);
    END LOOP;

    RETURN ROUND(amount_, 2);
END CalculateCompoundInterest;
```

##### Result[¶](#id40)

<!-- prettier-ignore -->
|CALCULATECOMPOUNDINTEREST(1000, 5, 3)|
|---|
|1157.63|

##### Snowflake (SnowScript UDF)[¶](#id41)

```
CREATE OR REPLACE FUNCTION CalculateCompoundInterest (principal_ NUMBER(38, 18), rate_ NUMBER(38, 18), years_ NUMBER(38, 18)
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "zsqZAVE5n32hZZFtsi0zsg==" }}'
AS
$$
   DECLARE
      amount_ NUMBER(38, 18);
      i NUMBER(38, 18);
   BEGIN
      amount_ := :principal_;
      --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
      FOR i IN 1 TO :years_
                            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                            LOOP
         amount_ := :amount_ * (
                                !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN Number AND unknown ***/!!!1 + :rate_ / 100);
                               END LOOP;
      RETURN ROUND(:amount_, 2);
   END;
$$;
```

##### Result[¶](#id42)

<!-- prettier-ignore -->
|CALCULATECOMPOUNDINTEREST(1000, 5, 3)|
|---|
|1157.63|

#### CASE and DECODE Logic[¶](#case-and-decode-logic)

Functions using CASE expressions and DECODE for categorization.

##### Oracle[¶](#id43)

```
CREATE OR REPLACE FUNCTION GetCustomerTier (
    annual_spend_ IN NUMBER,
    years_active_ IN NUMBER
) RETURN VARCHAR2
IS
    tier_ VARCHAR2(20);
    base_tier_ VARCHAR2(20);
BEGIN
    -- Determine base tier by spending
    base_tier_ := CASE
        WHEN annual_spend_ >= 10000 THEN 'PLATINUM'
        WHEN annual_spend_ >= 5000 THEN 'GOLD'
        WHEN annual_spend_ >= 2000 THEN 'SILVER'
        ELSE 'BRONZE'
    END;

    -- Upgrade tier if customer is loyal (5+ years)
    IF years_active_ >= 5 THEN
        tier_ := DECODE(base_tier_,
            'GOLD', 'PLATINUM',
            'SILVER', 'GOLD',
            'BRONZE', 'SILVER',
            base_tier_);
    ELSE
        tier_ := base_tier_;
    END IF;

    RETURN tier_;
END GetCustomerTier;
```

##### Result[¶](#id44)

<!-- prettier-ignore -->
|GETCUSTOMERTIER(3000, 6)|
|---|
|GOLD|

##### Snowflake (SnowScript UDF)[¶](#id45)

```
CREATE OR REPLACE FUNCTION GetCustomerTier (annual_spend_ NUMBER(38, 18), years_active_ NUMBER(38, 18)
)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "10/09/2025",  "domain": "no-domain-provided",  "migrationid": "zsqZAVE5n32hZZFtsi0zsg==" }}'
AS
$$
   DECLARE
      tier_ VARCHAR(20);
      base_tier_ VARCHAR(20);
   BEGIN
      -- Determine base tier by spending
      base_tier_ := CASE
                WHEN :annual_spend_ >= 10000 THEN 'PLATINUM'
                WHEN :annual_spend_ >= 5000 THEN 'GOLD'
                WHEN :annual_spend_ >= 2000 THEN 'SILVER'
                ELSE 'BRONZE'
            END;
      -- Upgrade tier if customer is loyal (5+ years)
      IF (:years_active_ >= 5) THEN
                tier_ := DECODE(:base_tier_,
                           'GOLD', 'PLATINUM',
                           'SILVER', 'GOLD',
                           'BRONZE', 'SILVER', :base_tier_);
      ELSE
                tier_ := :base_tier_;
      END IF;
      RETURN :tier_;
   END;
$$;
```

##### Result[¶](#id46)

<!-- prettier-ignore -->
|GETCUSTOMERTIER(3000, 6)|
|---|
|GOLD|

#### Select Into variable assingment[¶](#select-into-variable-assingment)

Functions using simple select into for variable assignment.

##### Oracle[¶](#id47)

```
CREATE OR REPLACE FUNCTION CalculatePrice
(
    p_BasePrice NUMBER,
    p_Quantity NUMBER
)
RETURN NUMBER
IS
    v_Discount NUMBER;
    v_Subtotal NUMBER;
    v_FinalPrice NUMBER;
BEGIN

    SELECT CASE
               WHEN p_Quantity >= 10 THEN 0.15
               WHEN p_Quantity >= 5 THEN 0.10
               ELSE 0.05
           END,
           p_BasePrice * p_Quantity
    INTO v_Discount, v_Subtotal
    FROM DUAL;

    v_FinalPrice := v_Subtotal * (1 - v_Discount);

    RETURN v_FinalPrice;
END;
```

##### Result[¶](#id48)

<!-- prettier-ignore -->
|CALCULATEPRICE(100, 3)|
|---|
|285|

##### Snowflake (SnowScript UDF)[¶](#id49)

```
CREATE OR REPLACE FUNCTION CalculatePrice
(p_BasePrice NUMBER(38, 18), p_Quantity NUMBER(38, 18)
)
RETURNS NUMBER(38, 18)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "11/26/2025",  "domain": "no-domain-provided",  "migrationid": "DsGaAXVMinypPa0FTZmrKQ==" }}'
AS
$$
    DECLARE
        v_Discount NUMBER(38, 18);
        v_Subtotal NUMBER(38, 18);
        v_FinalPrice NUMBER(38, 18);
    BEGIN
        v_Discount := CASE
                          WHEN :p_Quantity >= 10 THEN 0.15
                          WHEN :p_Quantity >= 5 THEN 0.10
                          ELSE 0.05
                      END;
        v_Subtotal := :p_BasePrice * :p_Quantity;
        v_FinalPrice := :v_Subtotal * (1 - :v_Discount);
        RETURN :v_FinalPrice;
    END;
$$;
```

##### Result[¶](#id50)

<!-- prettier-ignore -->
|CALCULATEPRICE(100, 3)|
|---|
|285|

### Known Issues[¶](#id51)

Warning

**SnowConvert AI will not translate UDFs containing the following elements into SnowScripting UDFs,
as these features are unsupported in SnowScripting UDFs:**

- Access database tables
- Use cursors
- Call other UDFs
- Contain aggregate or window functions
- Perform DML operations (INSERT/UPDATE/DELETE)
- Return result sets

### Related EWIs[¶](#id52)

1. [SSC-EWI-0067](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0067):
   UDF was transformed to Snowflake procedure, calling procedures inside a query is not supported.
2. [SSC-EWI-0068](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0068):
   User defined function was transformed to a Snowflake procedure.
3. [SSC-EWI-0073](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073):
   Pending Functional Equivalence Review.
4. [SSC-FDM-OR0042](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0042):
   Date Type Transformed To Timestamp Has A Different Behavior.
