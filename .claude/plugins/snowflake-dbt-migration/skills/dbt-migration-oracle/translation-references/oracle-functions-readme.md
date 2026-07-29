---
description: This section shows equivalents between functions in Oracle and in Snowflake.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/functions/README
title: SnowConvert AI - Oracle - Built-in functions | Snowflake Documentation
---

## Functions Details

### To_Char(datetime)

According to the format parameter, the function will be converted to:

<!-- prettier-ignore -->
|Format|Conversion|
|---|---|
|AD or BC A.D. or B.C.|The function will be converted to a **_conditional expression_** **_(CASE)_** where the **format** is added as a result of the **_’when’_** condition. **For Example:** `from: To_Char(DATE ‘1998-12-25’, ‘AD’)` `to: CASE WHEN YEAR(DATE ‘1998-12-25’) < 0 THEN`**`’BC’`**|
|CC or SCC|The function will be converted to a **_conditional expression_** where the original function body is added as a **_when_** condition but it will be between a **_MOD_** function, after that the original function is added as a **_then_** result but contained by a **_SUBSTR_** function. **For example:** `from: To_Char(DATE ‘1998-12-25’,’CC’)` `to: CASE WHEN MOD(YEAR(DATE ‘1998-12-25’), 100) = 0` `THEN SUBSTR(TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’), 1, 2)`|
|D|The function will be converted to the snowflake function equivalent but the function body will be between the **_DAYOFWEEK_** datetime part. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’D’)` `to: TO_CHAR(DAYOFWEEK(DATE ‘1998-12-25’) + 1)`|
|DAY|The function will be converted to a **_user-defined function_** inside of an **_UPPER_** function. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’DAY’)` `to: UPPER(SNOWCONVERT.PUBLIC.FULL_DAY_NAME_UDF(DATE ‘1998-12-25’))`|
|DDD|The function will be converted to the snowflake function equivalent but the function body will be between the **_DAYOFYEAR_** datetime part. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’DDD’)` `to: TO_CHAR(DAYOFYEAR(DATE ‘1998-12-25’))`|
|DD-MON-RR|The function will be converted to the snowflake function equivalent keeping the function body but changing the format to: _’DD-MON-YY’._ **For Example:** `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’DD-MON-RR’)` `to: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’DD-MON-YY’)`|
|DL|The function will be converted to a **_user-defined function_** plus the **_’OR’_** operator plus snowflake equivalent keeping the function body but changing the format to: \*’**, MMM DD, YYYY\*** **For example:** `from: To_Char(DATE ‘1998-12-25’,’DL’)` `to: SNOWCONVERT.PUBLIC.FULL_DAY_NAME_UDF(DATE ‘1998-12-25’)`|
|DS|The function will be converted to a combination of the snowflake function equivalent inside of the **_LTRIM_** function and the snowflake function equivalent. All the parts combined with the **_’OR’_** operator. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’DS’)` `to: LTRIM(TO_CHAR(DATE ‘1998-12-25’, ‘MM’), ‘0’)`|
|DY|The function will be converted to the snowflake function equivalent inside of the **_UPPER_** function. **For example:** `from: To_Char(DATE ‘1998-12-25’,’DY’)` `to: UPPER(TO_CHAR(DATE ‘1998-12-25’, ‘DY’))`|
|I|The function will be converted to into the snowflake function equivalent inside of the **_SUBSTR_** function. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’I’)` `to: SUBSTR(TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’), 4, 1)`|
|IW|The function will be converted to the snowflake function equivalent but the function body will be between the **_WEEKISO_** datetime part. **For Example:** `from:To_Char(DATE ‘1998-12-25’,’IW’)` `to: TO_CHAR(WEEKISO(DATE ‘1998-12-25’))`|
|IY|The function will be converted to the snowflake function equivalent keeping the function body but changing the format to: **\*’YY’**.\* **For example:** `from:To_Char(DATE ‘1998-12-25’, ‘IY’)` `to: TO_CHAR(DATE ‘1998-12-25’, ‘YY’)`|
|IYY|The function will be converted to the snowflake function equivalent inside of the **_SUBSTR_** function and change the format to: **_’YYYY’_**. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’IYY’)` `to: SUBSTR(TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’), 2, 3)`|
|IYYY|The function will be converted to the snowflake function equivalent keeping the function body but changing the format to: **\*’YYYY’**.\* **For example:** `from:To_Char(DATE ‘1998-12-25’, ‘IYYY’)` `to: TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’)`|
|J|The function will be converted to a conditional expression with ‘B.C.’ as a **_’then’_** result and **_’A.D._**’ as an else result. **For example:** `from: To_Char(DATE ‘1998-12-25’,’J’)` `to:` DATE_TO_JULIANDAYS_UDF(DATE ‘1998-12-25’)|
|MI|The function will be converted to the snowflake equivalent. If the function argument is **_SYSDATE_** it will be changed to **_CURRENT_TIMESTAMP_**, otherwise, if it is of type date, the function will return null. **For Example:** `from: To_Char(SYSDATE,’MI’);` `to: To_Char(CURRENT_TIMESTAMP,’MI’)`|
|MON|The function will be converted to the snowflake function equivalent inside of the **_UPPER_** function. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’MON’)` `to: UPPER(TO_CHAR(DATE ‘1998-12-25’, ‘MON’))`|
|MONTH|The function will be converted to the snowflake function equivalent inside of the **_UPPER_** function and change the format to: **_’MMMM’_**. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’MONTH’)` `to: UPPER(TO_CHAR(DATE ‘1998-12-25’, ‘MMMM’))`|
|Q|The function will be converted to the snowflake function equivalent inside of the **_QUARTER_** function. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’Q’)` `to: TO_CHAR(QUARTER(DATE ‘1998-12-25’))`|
|RM|The function will be converted to a **_user-defined function._** **For Example:** `from: To_Char(DATE ‘1998-12-25’,’RM’)` `to: SNOWCONVERT.PUBLIC.ROMAN_MONTH_UDF(DATE ‘1998-12-25’)`|
|RR|The function will be converted to the snowflake function equivalent keeping the function body but changing the format to: **\*’YY’**.\* **For Example:** `from: To_Char(DATE ‘1998-12-25’,’RR’)` `to: TO_CHAR(DATE ‘1998-12-25’, ‘YY’)`|
|RR-MON-DD|The function will be converted to the snowflake function equivalent keeping the function body but changing the format to: **\*’YY-MON-DD’**.\* **For Example:** `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’RR-MON-DD’)` `to: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’YY-MON-DD’)`|
|RRRR|The function will be converted to the snowflake function equivalent keeping the function body but changing the format to: **\*’YYYY’**.\* **For Example:** `from: To_Char(DATE ‘1998-12-25’,’RRRR’)` `to: TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’)`|
|SS|The function will be converted to a combination of a **_conditional expression_** and the snowflake function equivalent. All the parts combined with the **_’OR’_** operator. **For Example:** `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’SS’)` `to: CASE WHEN SECOND(TIMESTAMP ‘1998-12-25 09:26:50.12’) = 0` `THEN ‘00’ WHEN SECOND(TIMESTAMP ‘1998-12-25 09:26:50.12’) < 10` `THEN ‘0’`|
|SSSS|The function will be converted to the snowflake function equivalent but the function body will be a concatenation of **_SECOND_**, **_MINUTE,_** and **_HOUR_** datetime parts. **For Example:** `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’SSSS’)` `to: TO_CHAR(SECOND(TIMESTAMP ‘1998-12-25 09:26:50.12’) +` `MINUTE(TIMESTAMP ‘1998-12-25 09:26:50.12’) * 60 +` `HOUR(TIMESTAMP ‘1998-12-25 09:26:50.12’) * 3600)`|
|TS|The function will be converted to the snowflake function equivalent keeping the function body but changing the format to: **\*’HH:MI:SS PM’**.\* **For Example:** `from: To_Char(TIMESTAMP ‘1998-12-25 09:26:50.12’,’TS’)` `to: TO_CHAR(TIMESTAMP ‘1998-12-25 09:26:50.12’, ‘HH:MI:SS PM’)`|
|W|The function will be converted to the **_TRUNC_** function with the **_DAYOFMONTH_** datetime part. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’W’)` `to: TRUNC(DAYOFMONTH(DATE ‘1998-12-25’) / 7 + 1)`|
|WW|The function will be converted to the **_TRUNC_** function with the **_DAYOFYEAR_** datetime part. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’WW’)` `to: TRUNC(DAYOFYEAR(DATE ‘1998-12-25’) / 7 + 1)`|
|Y YYY|The function will be converted to the snowflake function equivalent inside of the **_SUBSTR_** function and change the format to: **_’YYYY’_**. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’Y’)` `to: SUBSTR(TO_CHAR(DATE ‘1998-12-25’, ‘YYYY’), 4, 1)`|
|Y,YYY|The function will be converted to a combination of the snowflake function equivalent inside of the **SUBSTR** function and a comma symbol. All the parts combined with the **_’OR’_** operator. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’Y,YYY’)` `to: SUBSTR(TO_CHAR(YEAR(DATE ‘1998-12-25’)), 1, 1)`|
|YEAR SYEAR|The function will be converted to a **_user-defined function_** inside of an **_UPPER_** function. **For Example:** `from: To_Char(DATE ‘1998-12-25’,’YEAR’)` `to: UPPER(SNOWCONVERT.PUBLIC.YEAR_NAME_UDF(DATE ‘1998-12-25’))`|

## MAX KEEP DENSE_RANK

### Description

The Oracle `MAX KEEP DENSE_RANK` function is an aggregate function that returns the maximum value
from a set of values while considering only the rows that have the first (smallest) rank according
to the specified ordering. The `KEEP (DENSE_RANK FIRST ORDER BY ...)` clause filters the rows to
include only those with the smallest rank value before applying the MAX function.
([Oracle Aggregate Functions Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Aggregate-Functions.html#GUID-62BE676B-AF18-4E63-BD14-25206FEA0848)).

### Sample Source Pattern

#### Syntax

##### Oracle

```sql
MAX(expression) KEEP (DENSE_RANK FIRST ORDER BY order_by_expression [ASC|DESC])
```

##### Snowflake SQL

```sql
FIRST_VALUE(expression) OVER (ORDER BY order_by_expression [ASC|DESC])
```

### Examples

#### Oracle 2

##### Code

```sql
SELECT department_id,
       MAX(salary) KEEP (DENSE_RANK FIRST ORDER BY hire_date) AS first_hired_max_salary
FROM employees
GROUP BY department_id;
```

#### Snowflake SQL 2

##### Code 2

```sql
SELECT department_id,
       FIRST_VALUE(salary)
       OVER (
       ORDER BY hire_date) AS first_hired_max_salary
FROM
       employees
GROUP BY department_id;
```

##### Note

To ensure a deterministic order for the rows in a window function’s results, the ORDER BY clause
must include a key or combination of keys that makes each row unique.

## MIN KEEP DENSE_RANK

### Description 2

The Oracle `MIN KEEP DENSE_RANK` function is an aggregate function that returns the minimum value
from a set of values while considering only the rows that have the last (highest) rank according to
the specified ordering. The `KEEP (DENSE_RANK LAST ORDER BY ...)` clause filters the rows to include
only those with the highest rank value before applying the MIN function.
([Oracle Aggregate Functions Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Aggregate-Functions.html#GUID-62BE676B-AF18-4E63-BD14-25206FEA0848)).

### Sample Source Pattern 2

#### Syntax 2

##### Oracle 3

```sql
MIN(expression) KEEP (DENSE_RANK LAST ORDER BY order_by_expression [ASC|DESC])
```

##### Snowflake SQL 3

```sql
LAST_VALUE(expression) OVER (ORDER BY order_by_expression [ASC|DESC])
```

### Examples 2

#### Oracle 4

##### Code 3

```sql
SELECT department_id,
       MIN(salary) KEEP (DENSE_RANK LAST ORDER BY hire_date) AS first_hired_min_salary
FROM employees
GROUP BY department_id;
```

#### Snowflake SQL 4

##### Code 4

```sql
SELECT department_id,
       LAST_VALUE(salary)
       OVER (
       ORDER BY hire_date) AS first_hired_min_salary
FROM
       employees
GROUP BY department_id;
```

##### Note 2

To ensure a deterministic order for the rows in a window function’s results, the ORDER BY clause
must include a key or combination of keys that makes each row unique.

## NLSSORT

### Description 3

NLSSORT returns a collation key for the character value char and an explicitly or implicitly
specified collation. A collation key is a string of bytes used to sort char according to the
specified collation. The property of the collation keys is that mutual ordering of two such keys
generated for the given collation when compared according to their binary order is the same as
mutual ordering of the source character values when compared according to the given collation..
([NLSSORT in Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/NLSSORT.html#GUID-781C6FE8-0924-4617-AECB-EE40DE45096D)).

### Sample Source Pattern 3

#### Syntax 3

##### Oracle 5

```sql
NLSSORT(char [, 'nlsparam' ])
```

##### Snowflake SQL 5

[Snowflake SQL Documentation](https://docs.snowflake.com/en/sql-reference/functions/collate)

```sql
COLLATE(`<string_expression>`, '`<collation_specification>`')
```

### Examples 3

#### Oracle 6

##### Code 5

```sql
CREATE TABLE test (name VARCHAR2(15));
INSERT INTO test VALUES ('Gaardiner');
INSERT INTO test VALUES ('Gaberd');
INSERT INTO test VALUES ('Gaasten');

SELECT *
  FROM test
  ORDER BY NLSSORT(name, 'NLS_SORT = XDanish');
```

##### Result

<!-- prettier-ignore -->
|NAME|
|---|
|Gaberd|
|Gaardiner.|
|Gaasten|

##### Snowflake SQL 6

###### Code 6

```sql
CREATE OR REPLACE TABLE test (name VARCHAR(15))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

INSERT INTO test
VALUES ('Gaardiner');

INSERT INTO test
VALUES ('Gaberd');

INSERT INTO test
VALUES ('Gaasten');

SELECT *
  FROM
  test
ORDER BY
COLLATE(name, '');
```

###### Result 2

<!-- prettier-ignore -->
|NAME|
|---|
|Gaberd|
|Gaardiner|
|Gaasten|

## TO_NUMBER

### Description 4

Converts an input expression to a fixed-point number. For NULL input, the output is NULL.

#### Arguments

##### Required

&#xNAN;_`<expr>`_

An expression of a numeric, character, or variant type.

##### Optional

_`<format>`_

The SQL format model used to parse the input _`expr`_ and return. For more information, see
[SQL Format Models](https://docs.snowflake.com/en/sql-reference/sql-format-models).

_`<precision>`_

The maximal number of decimal digits in the resulting number; from 1 to 38. In Snowflake, precision
is not used for determination of the number of bytes needed to store the number and does not have
any effect on efficiency, so the default is the maximum (38).

_`<scale>`_

The number of fractional decimal digits (from 0 to _`precision`_ - 1). 0 indicates no fractional
digits (i.e. an integer number). The default scale is 0.

#### Returns

The function returns `NUMBER(`_`precision`_` ,`` `` `_`scale`_`)`.

- If the _`precision`_ is not specified, then it defaults to 38.
- If the _`scale`_ is not specified, then it defaults to 0.

To more information check the
[TO_NUMBER](https://docs.snowflake.com/en/sql-reference/functions/to_decimal) in snowflake
documentation.

```sql
SELECT CAST('123,456E+40' AS NUMBER, '999,999EEE') FROM DUAL;
SELECT CAST('12sdsd3,456E+40' AS NUMBER, '999,999EEE') FROM DUAL;
SELECT CAST('12345sdsd' AS NUMBER, '99999') FROM DUAL;
SELECT CAST('12.345678912345678912345678912345678912' AS NUMBER, '99.999999999999999999999999999999999999') FROM DUAL;
SELECT CAST('               12.345678912345678912345678912345678912' AS NUMBER, '99.999999999999999999999999999999999999') FROM DUAL;
SELECT CAST('               -12.345678912345678912345678912345678912' AS NUMBER, '99.999999999999999999999999999999999999') FROM DUAL;
SELECT CAST('12.34567891234567891234567891234567891267' AS NUMBER, '99.999999999999999999999999999999999999') FROM DUAL;
SELECT CAST('123.456E-40' AS NUMBER, '999.9999EEE') FROM DUAL;
select cast('12,345,678,912,345,678,912,345,678,912,345,678,912' as number, '99,999,999,999,999,999,999,999,999,999,999,999,999') from dual;
SELECT CAST('  123.456E-40' AS NUMBER, '999.9999EEE') FROM DUAL;
select cast('       12,345,678,912,345,678,912,345,678,912,345.678912' as number, '99,999,999,999,999,999,999,999,999,999,999.999999') from dual;

SELECT CAST('12.34567891234567891234567891234567891267+' AS NUMBER, '99.999999999999999999999999999999999999S') FROM DUAL;
select cast('12,345,678,912,345,678,912,345,678,912,345,678,912+' as number, '99,999,999,999,999,999,999,999,999,999,999,999,999S') from dual;

select cast('12.48+' as number, '99.99S') from dual;
select cast('  12.48+' as number, '99.99S') from dual;
select cast('12.48+   ' as number, '99.99S') from dual;

SELECT CAST('123.456+E-2' AS NUMBER, '999.9999SEEE') FROM DUAL;
SELECT CAST('123.456+E-2-' AS NUMBER, '999.9999SEEE') FROM DUAL;

SELECT CAST('12356-' AS NUMBER, '99999S') FROM DUAL;

select cast(' 1.0E+123' as number, '9.9EEEE') from dual;
select cast('1.2E+02' as number, 'FM9.9EEEE') from dual;
select cast('123.45' as number, 'FM999.009') from dual;
select cast('123.00' as number, 'FM999.009') from dual;
select cast(' $123.45' as number, 'L999.99') from dual;
select cast('$123.45' as number, 'FML999.99') from dual;
select cast('1234567890+' as number, '9999999999S') from dual;
```

```sql
 SELECT
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0050 - INPUT EXPRESSION IS OUT OF THE RANGE '123,456E+40' ***/!!!
 CAST('123,456E+40' AS NUMBER(38, 18) , '999,999EEE') FROM DUAL;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0053 - INCORRECT INPUT FORMAT '12sdsd3,456E+40' ***/!!! CAST('12sdsd3,456E+40' AS NUMBER(38, 18) , '999,999EEE') FROM DUAL;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0053 - INCORRECT INPUT FORMAT '12345sdsd' ***/!!! CAST('12345sdsd' AS NUMBER(38, 18) , '99999') FROM DUAL;

SELECT
 TO_NUMBER('12.345678912345678912345678912345678912', '99.999999999999999999999999999999999999', 38, 36)
FROM DUAL;

SELECT
 TO_NUMBER('               12.345678912345678912345678912345678912', '99.999999999999999999999999999999999999', 38, 36)
FROM DUAL;

SELECT
 TO_NUMBER('               -12.345678912345678912345678912345678912', '99.999999999999999999999999999999999999', 38, 36)
FROM DUAL;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0050 - INPUT EXPRESSION IS OUT OF THE RANGE '12.34567891234567891234567891234567891267' ***/!!! CAST('12.34567891234567891234567891234567891267' AS NUMBER(38, 18) , '99.999999999999999999999999999999999999') FROM DUAL;

SELECT
 TO_NUMBER('123.456E-40', '999.9999EEE', 38, 37)
FROM DUAL;

select
 TO_NUMBER('12,345,678,912,345,678,912,345,678,912,345,678,912', '99,999,999,999,999,999,999,999,999,999,999,999,999', 38, 0)
from dual;

SELECT
 TO_NUMBER('  123.456E-40', '999.9999EEE', 38, 37)
FROM DUAL;

select
 TO_NUMBER('       12,345,678,912,345,678,912,345,678,912,345.678912', '99,999,999,999,999,999,999,999,999,999,999.999999', 38, 6)
from dual;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0050 - INPUT EXPRESSION IS OUT OF THE RANGE '12.34567891234567891234567891234567891267+' ***/!!! CAST('12.34567891234567891234567891234567891267+' AS NUMBER(38, 18) , '99.999999999999999999999999999999999999S') FROM DUAL;

select
 TO_NUMBER('12,345,678,912,345,678,912,345,678,912,345,678,912+', '99,999,999,999,999,999,999,999,999,999,999,999,999S', 38, 0)
from dual;

select
 TO_NUMBER('12.48+', '99.99S', 38, 2)
from dual;

select
 TO_NUMBER('  12.48+', '99.99S', 38, 2)
from dual;

select
 TO_NUMBER('12.48+   ', '99.99S', 38, 2)
from dual;

SELECT
 TO_NUMBER('123.456+E-2', '999.9999SEEE', 38, 5)
FROM DUAL;

SELECT
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0053 - INCORRECT INPUT FORMAT '123.456+E-2-' ***/!!! CAST('123.456+E-2-' AS NUMBER(38, 18) , '999.9999SEEE') FROM DUAL;

SELECT
 TO_NUMBER('12356-', '99999S', 38, 0)
FROM DUAL;

select
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0050 - INPUT EXPRESSION IS OUT OF THE RANGE ' 1.0E+123' ***/!!! cast(' 1.0E+123' as NUMBER(38, 18) , '9.9EEEE') from dual;

select
 TO_NUMBER('1.2E+02', 'FM9.9EEEE', 38, 0)
from dual;

select
 TO_NUMBER('123.45', 'FM999.009', 38, 2)
from dual;

select
 TO_NUMBER('123.00', 'FM999.009', 38, 2)
from dual;

select
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0045 - CAST TYPE L AND FML NOT SUPPORTED ***/!!! cast(' $123.45' as NUMBER(38, 18) , 'L999.99') from dual;

select
 !!!RESOLVE EWI!!! /*** SSC-EWI-OR0045 - CAST TYPE L AND FML NOT SUPPORTED ***/!!! cast('$123.45' as NUMBER(38, 18) , 'FML999.99') from dual;

select
 TO_NUMBER('1234567890+', '9999999999S', 38, 0)
from dual;
```

#### Recommendations

- No additional user actions are required.
- If you need more support, you can email us at
  [snowconvert-support@snowflake.com](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/functions/mailto:snowconvert-support%40snowflake.com).

### Related EWIs

1. [SSC-EWI-OR0045](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0045):
   Cast type L and FML are not supported.
2. [SSC-EWI-OR0050](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0050):
   Input Expression is out of the range.
3. [SSC-EWI-OR0053](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0053):
   Incorrect input format.
