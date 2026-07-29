---
description:
  An expression list is a combination of expressions, and can appear in membership and comparison
  conditions (WHERE clauses) and in GROUP BY clauses. (Redshift SQL Language Reference Expression
  lists).
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-expressions
title: SnowConvert AI - Redshift - Expressions | Snowflake Documentation
---

## Expression lists

### Description

> An expression list is a combination of expressions, and can appear in membership and comparison
> conditions (WHERE clauses) and in GROUP BY clauses.
> ([Redshift SQL Language Reference Expression lists](https://docs.aws.amazon.com/redshift/latest/dg/r_expression_lists.html)).

#### Note

This syntax is fully supported in Snowflake.

### Grammar Syntax

```sql
 expression , expression , ... | (expression, expression, ...)
```

### Sample Source Patterns

#### **Setup data**

##### Redshift

```sql
 CREATE TABLE table1 (
    quantity VARCHAR(50),
    fruit VARCHAR(50)
);

CREATE TABLE table2 (
    quantity VARCHAR(50),
    fruit VARCHAR(50)
);

CREATE TABLE table3 (
    id INT,
    name VARCHAR(50),
    quantity INT,
    fruit VARCHAR(50),
    price INT
);

INSERT INTO table1 (quantity, fruit)
VALUES
    ('one', 'apple'),
    ('two', 'banana'),
    ('three', 'cherry');

INSERT INTO table2 (quantity, fruit)
VALUES
    ('one', 'apple'),
    ('two', 'banana'),
    ('four', 'orange');

INSERT INTO table3 (id, name, quantity, fruit, price)
VALUES
    (1, 'Alice', 1, 'apple', 100),
    (2, 'Bob', 5, 'banana', 200),
    (3, 'Charlie', 10, 'cherry', 300),
    (4, 'David', 15, 'orange', 400);
```

#### IN Clause

##### Input Code

##### Redshift 2

```sql
SELECT *
FROM table3
WHERE quantity IN (1, 5, 10);
```

##### Result

<!-- prettier-ignore -->
|ID|NAME|QUANTITY|FRUIT|PRICE|
|---|---|---|---|---|
|1|Alice|1|apple|100|
|2|Bob|5|banana|200|
|3|Charlie|10|cherry|300|

##### Output Code

##### Snowflake

```sql
 SELECT *
FROM
    table3
WHERE quantity IN (1, 5, 10);
```

##### Result 2

<!-- prettier-ignore -->
|ID|NAME|QUANTITY|FRUIT|PRICE|
|---|---|---|---|---|
|1|Alice|1|apple|100|
|2|Bob|5|banana|200|
|3|Charlie|10|cherry|300|

#### Comparisons

##### Input Code: 2

##### Redshift 3

```sql
 SELECT *
FROM table3
WHERE (quantity, fruit) = (1, 'apple');
```

##### Result 3

<!-- prettier-ignore -->
|ID|NAME|QUANTITY|FRUIT|PRICE|
|---|---|---|---|---|
|1|Alice|1|apple|100|

##### Output Code: 2

##### Snowflake 2

```sql
 SELECT *
FROM
    table3
WHERE (quantity, fruit) = (1, 'apple');
```

##### Result 4

<!-- prettier-ignore -->
|ID|NAME|QUANTITY|FRUIT|PRICE|
|---|---|---|---|---|
|1|Alice|1|apple|100|

###### Note 2

Expression list comparisons with the following operators may have a different behavior in Snowflake.
( **`< , <= , > , >=`**). These operators are transformed into logical `AND` operations to achieve
full equivalence in Snowflake.

##### Input Code: 3

##### Redshift 4

```sql
 SELECT (1,8,20) < (2,2,0) as r1,
       (1,null,2) > (1,0,8) as r2,
       (null,null,2) < (1,0,8) as r3,
       (1,0,null) <= (1,1,0) as r4,
       (1,1,0) >= (1,1,20) as r5;
```

##### Result 5

<!-- prettier-ignore -->
|R1|R2|R3|R4|R5|
|---|---|---|---|---|
|FALSE|FALSE|NULL|NULL|FALSE|

##### Output Code: 3

##### Snowflake 3

```sql
 SELECT
    (1 < 2
    AND 8 < 2
    AND 20 < 0) as r1,
    (1 > 1
    AND null > 0
    AND 2 > 8) as r2,
    (null < 1
    AND null < 0
    AND 2 < 8) as r3,
    (1 <= 1
    AND 0 <= 1
    AND null <= 0) as r4,
    (1 >= 1
    AND 1 >= 1
    AND 0 >= 20) as r5;
```

##### Result 6

<!-- prettier-ignore -->
|R1|R2|R3|R4|R5|
|---|---|---|---|---|
|FALSE|FALSE|NULL|NULL|FALSE|

#### Nested tuples

##### Input Code: 4

##### Redshift 5

```sql
 SELECT *
FROM table3
WHERE (quantity, fruit) IN ((1, 'apple'), (5, 'banana'), (10, 'cherry'));
```

##### Result 7

<!-- prettier-ignore -->
|ID|NAME|QUANTITY|FRUIT|PRICE|
|---|---|---|---|---|
|1|Alice|1|apple|100|
|2|Bob|5|banana|200|
|3|Charlie|10|cherry|300|

##### Output Code 2

##### Snowflake 4

```sql
 SELECT *
FROM
    table3
WHERE (quantity, fruit) IN ((1, 'apple'), (5, 'banana'), (10, 'cherry'));
```

##### Result 8

<!-- prettier-ignore -->
|ID|NAME|QUANTITY|FRUIT|PRICE|
|---|---|---|---|---|
|1|Alice|1|apple|100|
|2|Bob|5|banana|200|
|3|Charlie|10|cherry|300|

#### Case statement

##### Input Code: 5

##### Redshift 6

```sql
 SELECT
    CASE
        WHEN quantity IN (1, 5, 10) THEN 'Found'
        ELSE 'Not Found'
    END AS result
FROM table3;
```

##### Result 9

<!-- prettier-ignore -->
|RESULT|
|---|
|Found|
|Found|
|Found|
|Not Found|
|Not Found|
|Not Found|

##### Output Code 2 2

##### Snowflake 5

```sql
 SELECT
    CASE
        WHEN quantity IN (1, 5, 10) THEN 'Found'
        ELSE 'Not Found'
    END AS result
FROM
    table3;
```

##### Result 10

<!-- prettier-ignore -->
|RESULT|
|---|
|Found|
|Found|
|Found|
|Not Found|
|Not Found|
|Not Found|

#### Multiple Expressions

##### Input Code: 6

##### Redshift 7

```sql
 SELECT *
FROM table3
WHERE (quantity, fruit) IN ((1, 'apple'), (5, 'banana'), (10, 'cherry'))
  AND price IN (100, 200, 300);
```

##### Result 11

<!-- prettier-ignore -->
|ID|NAME|QUANTITY|FRUIT|PRICE|
|---|---|---|---|---|
|1|Alice|1|apple|100|
|2|Bob|5|banana|200|
|3|Charlie|10|cherry|300|

##### Output Code 3

##### Snowflake 6

```sql
 SELECT *
FROM
    table3
WHERE (quantity, fruit) IN ((1, 'apple'), (5, 'banana'), (10, 'cherry'))
  AND price IN (100, 200, 300);
```

##### Result 12

<!-- prettier-ignore -->
|ID|NAME|QUANTITY|FRUIT|PRICE|
|---|---|---|---|---|
|1|Alice|1|apple|100|
|2|Bob|5|banana|200|
|3|Charlie|10|cherry|300|

#### Joins

##### Input Code: 7

##### Redshift 8

```sql
 SELECT *
FROM table1 t1
JOIN table2 t2
    ON (t1.quantity, t1.fruit) = (t2.quantity, t2.fruit)
WHERE t1.quantity = 'one' AND t1.fruit = 'apple';
```

##### Result 13

<!-- prettier-ignore -->
|QUANTITY|FRUIT|QUANTITY|FRUIT|
|---|---|---|---|
|one|apple|one|apple|

##### Output Code 4

##### Snowflake 7

```sql
 SELECT *
FROM
table1 t1
JOIN
        table2 t2
    ON (t1.quantity, t1.fruit) = (t2.quantity, t2.fruit)
WHERE t1.quantity = 'one' AND t1.fruit = 'apple';
```

##### Result 14

<!-- prettier-ignore -->
|QUANTITY|FRUIT|QUANTITY|FRUIT|
|---|---|---|---|
|one|apple|one|apple|

### Known Issues

No issues were found.

### Related EWIs

There are no known issues.

## Compound Expressions

### Description 2

> A compound expression is a series of simple expressions joined by arithmetic operators. A simple
> expression used in a compound expression must return a numeric value.
>
> ([RedShift SQL Language Reference Compound expressions](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html))

### Grammar Syntax 2

```sql
 expression operator {expression | (compound_expression)}
```

### Conversion Table

<!-- prettier-ignore -->
|Redshift|Snowflake|Comments|
|---|---|---|---|---|---|---|
|[`||`](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (Concatenation)|[`||`](https://docs.snowflake.com/en/sql-reference/functions/concat)|Fully supported by Snowflake|

### Sample Source Patterns 2

#### Input Code: 8

#### Redshift 9

```sql
 CREATE TABLE concatenation_demo (
    col1 VARCHAR(20),
    col2 INTEGER,
    col3 DATE
);

INSERT INTO concatenation_demo (col1, col2, col3) VALUES
('Hello', 42, '2023-12-01'),
(NULL, 0, '2024-01-01'),
('Redshift', -7, NULL);

SELECT
    col1 || ' has number ' || col2 AS concat_string_number
FROM concatenation_demo;

SELECT
    col1 || ' on ' || col3 AS concat_string_date
FROM concatenation_demo;

SELECT
    COALESCE(col1, 'Unknown') || ' with number ' || COALESCE(CAST(col2 AS VARCHAR), 'N/A') AS concat_with_null_handling
FROM concatenation_demo;
```

##### Results

<!-- prettier-ignore -->
|concat_string_number|
|---|
|Hello has number 42|
|```<NULL>```|
|Redshift has number -7|

<!-- prettier-ignore -->
|concat_string_date|
|---|
|Hello on 2023-12-01|
|```<NULL>```|
|```<NULL>```|

<!-- prettier-ignore -->
|concat_with_null_handling|
|---|
|Hello with number 42|
|Unknown with number 0|
|Redshift with number -7|

###### Output Code 3 2

##### Snowflake 8

```sql
 CREATE TABLE concatenation_demo (
    col1 VARCHAR(20),
    col2 INTEGER,
    col3 DATE
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "12/16/2024",  "domain": "test" }}';

INSERT INTO concatenation_demo (col1, col2, col3) VALUES
('Hello', 42, '2023-12-01'),
(NULL, 0, '2024-01-01'),
('Redshift', -7, NULL);

SELECT
    col1 || ' has number ' || col2 AS concat_string_number
FROM
    concatenation_demo;

SELECT
    col1 || ' on ' || col3 AS concat_string_date
FROM
    concatenation_demo;

SELECT
    COALESCE(col1, 'Unknown') || ' with number ' || COALESCE(CAST(col2 AS VARCHAR), 'N/A') AS concat_with_null_handling
FROM
    concatenation_demo;
```

##### Results 2

<!-- prettier-ignore -->
|concat_string_number|
|---|
|Hello has number 42|
|```<NULL>```|
|Redshift has number -7|

<!-- prettier-ignore -->
|concat_string_date|
|---|
|Hello on 2023-12-01|
|```<NULL>```|
|```<NULL>```|

<!-- prettier-ignore -->
|concat_with_null_handling|
|---|
|Hello with number 42|
|Unknown with number 0|
|Redshift with number -7|

### Known Issues 2

No issues were found.

### Related EWIs 2

There are no known issues.

### Arithmetic operators

Operators

Translation for Arithmetic Operators

#### Conversion Table 2

<!-- prettier-ignore -->
|Redshift|Snowflake|Comments|
|---|---|---|---|---|
|[+/-](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (positive and negative sign/operator)|[+/-](https://docs.snowflake.com/en/sql-reference/operators-arithmetic)|Fully supported by Snowflake|
|[^](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (exponentiation)|[POWER](https://docs.snowflake.com/en/sql-reference/functions/pow)|Fully supported by Snowflake|
|[\*](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (multiplication)|[\*](https://docs.snowflake.com/en/sql-reference/operators-arithmetic)|Fully supported by Snowflake|
|[/](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (division)|[/](https://docs.snowflake.com/en/sql-reference/operators-arithmetic)|Redshift division between integers always returns integer value, FLOOR function is added to emulate this behavior.|
|[%](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (modulo)|[%](https://docs.snowflake.com/en/sql-reference/operators-arithmetic)|Fully supported by Snowflake|
|[+](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (addition)|[+](https://docs.snowflake.com/en/sql-reference/operators-arithmetic) and [||](https://docs.snowflake.com/en/sql-reference/functions/concat)|Fully supported by Snowflake. When string are added, it is transformed to a concat.|
|[-](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (subtraction)|[-](https://docs.snowflake.com/en/sql-reference/operators-arithmetic)|Fully supported by Snowflake|
|[@](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (absolute value)|[ABS](https://docs.snowflake.com/en/sql-reference/functions/abs)|Fully supported by Snowflake|
|[|/](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (square root)|[SQRT](https://docs.snowflake.com/en/sql-reference/functions/sqrt)|Fully supported by Snowflake|
|[||/](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (cube root)|[CBRT](https://docs.snowflake.com/en/sql-reference/functions/cbrt)|Fully supported by Snowflake|

#### Sample Source Patterns 3

##### Addition, Subtraction, Positive & Negative

###### Input Code 2

##### Input Code: 9

##### Redshift 10

```sql
 CREATE TABLE test_math_operations (
    base_value DECIMAL(10, 2),
    multiplier INT,
    divisor INT,
    description VARCHAR(100),
    created_at TIMESTAMP,
    category VARCHAR(50)
);

INSERT INTO test_math_operations (base_value, multiplier, divisor, description, created_at, category)
VALUES
(100.50, 2, 5, 'Basic test', '2024-12-01 10:30:00', 'Type A'),
(250.75, 3, 10, 'Complex operations', '2024-12-02 15:45:00', 'Type B'),
(-50.25, 5, 8, 'Negative base value', '2024-12-03 20:00:00', 'Type C'),
(0, 10, 2, 'Zero base value', '2024-12-04 09:15:00', 'Type D');

SELECT +base_value AS positive_value,
       -base_value AS negative_value,
       (base_value + multiplier - divisor) AS add_sub_result,
       created_at + INTERVAL '1 day' AS next_day,
       created_at - INTERVAL '1 hour' AS one_hour_before,
       description + category as string_sum,
       base_value + '5' as int_string_sum,
       '5' + base_value as string_int_sum
FROM test_math_operations;
```

##### Results 3

<!-- prettier-ignore -->
|positive_value|negative_value|add_sub_result|next_day|one_hour_before|string_sum|int_string_sum|string_int_sum|
|---|---|---|---|---|---|---|---|
|100.50|-100.50|97.50|2024-12-02 10:30:00.000000|2024-12-01 09:30:00.000000|Basic testType A|105.5|105.5|
|250.75|-250.75|243.75|2024-12-03 15:45:00.000000|2024-12-02 14:45:00.000000|Complex operationsType B|255.75|255.75|
|-50.25|50.25|-53.25|2024-12-04 20:00:00.000000|2024-12-03 19:00:00.000000|Negative base valueType C|-45.25|-45.25|
|0.00|0.00|8.00|2024-12-05 09:15:00.000000|2024-12-04 08:15:00.000000|Zero base valueType D|5|5|

###### Output Code 4 2

##### Snowflake 9

```sql
 CREATE TABLE test_math_operations (
    base_value DECIMAL(10, 2),
    multiplier INT,
    divisor INT,
    description VARCHAR(100),
    created_at TIMESTAMP,
    category VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}';

INSERT INTO test_math_operations (base_value, multiplier, divisor, description, created_at, category)
VALUES
(100.50, 2, 5, 'Basic test', '2024-12-01 10:30:00', 'Type A'),
(250.75, 3, 10, 'Complex operations', '2024-12-02 15:45:00', 'Type B'),
(-50.25, 5, 8, 'Negative base value', '2024-12-03 20:00:00', 'Type C'),
(0, 10, 2, 'Zero base value', '2024-12-04 09:15:00', 'Type D');

SELECT +base_value AS positive_value,
       -base_value AS negative_value,
       (base_value + multiplier - divisor) AS add_sub_result,
       created_at + INTERVAL '1 day' AS next_day,
       created_at - INTERVAL '1 hour' AS one_hour_before,
       description + category as string_sum,
       base_value + '5' as int_string_sum,
       '5' + base_value as string_int_sum
FROM
       test_math_operations;
```

##### Results 4

<!-- prettier-ignore -->
|positive_value|negative_value|add_sub_result|next_day|one_hour_before|string_sum|int_string_sum|string_int_sum|
|---|---|---|---|---|---|---|---|
|100.5|-100.5|97.5|2024-12-02 10:30:00|2024-12-01 09:30:00|Basic testType A|105.5|105.5|
|250.75|-250.75|243.75|2024-12-03 15:45:00|2024-12-02 14:45:00|Complex operationsType B|255.75|255.75|
|-50.25|50.25|-53.25|2024-12-04 20:00:00|2024-12-03 19:00:00|Negative base valueType C|-45.25|-45.25|
|0|0|8|2024-12-05 09:15:00|2024-12-04 08:15:00|Zero base valueType D|5|5|

#### Exponentiation, multiplication, division & modulo

##### Input Code: 10

##### Redshift 11

```sql
 CREATE TABLE test_math_operations (
    base_value DECIMAL(10, 2),
    multiplier INT,
    divisor INT,
    mod_value INT,
    exponent INT
);

INSERT INTO test_math_operations (base_value, multiplier, divisor, mod_value, exponent)
VALUES
(100.50, 2, 5, 3, 2),
(250.75, 3, 10, 7, 3),
(-50.25, 5, 8, 4, 4),
(0, 10, 2, 1, 5);

SELECT
    base_value ^ exponent AS raised_to_exponent,
    (base_value * multiplier) AS multiplied_value,
    (base_value / divisor) AS divided_value,
    base_value::int / divisor as int_division,
    (mod_value % 2) AS modulo_result,
    (base_value + multiplier - divisor) AS add_sub_result,
    (base_value + (multiplier * (divisor - mod_value))) AS controlled_eval
FROM
    test_math_operations;
```

##### Results 5

<!-- prettier-ignore -->
|raised_to_exponent|multiplied_value|divided_value|int_division|modulo_result|add_sub_result|controlled_eval|
|---|---|---|---|---|---|---|
|10100.25|201|20.1|20|1|97.5|104.5|
|15766047.296875|752.25|25.075|25|1|243.75|259.75|
|6375940.62890625|-251.25|-6.28125|-6|0|-53.25|-30.25|
|0|0|0|0|1|8|10|

##### Output Code: 4

##### Snowflake 10

```sql
 CREATE TABLE test_math_operations (
    base_value DECIMAL(10, 2),
    multiplier INT,
    divisor INT,
    mod_value INT,
    exponent INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "12/10/2024",  "domain": "test" }}';

INSERT INTO test_math_operations (base_value, multiplier, divisor, mod_value, exponent)
VALUES
(100.50, 2, 5, 3, 2),
(250.75, 3, 10, 7, 3),
(-50.25, 5, 8, 4, 4),
(0, 10, 2, 1, 5);

SELECT
    POWER(
    base_value, exponent) AS raised_to_exponent,
    (base_value * multiplier) AS multiplied_value,
    (base_value / divisor) AS divided_value,
    FLOOR(
    base_value::int / divisor) as int_division,
    (mod_value % 2) AS modulo_result,
    (base_value + multiplier - divisor) AS add_sub_result,
    (base_value + (multiplier * (divisor - mod_value))) AS controlled_eval
FROM
    test_math_operations;
```

##### Results 6

<!-- prettier-ignore -->
|raised_to_exponent|multiplied_value|divided_value|int_division|modulo_result|add_sub_result|controlled_eval|
|---|---|---|---|---|---|---|
|10100.25|201|20.1|20|1|97.5|104.5|
|15766047.2969|752.25|25.075|25|1|243.75|259.75|
|6375940.6289|-251.25|-6.2812|-7|0|-53.25|-30.25|
|0|0|0|0|1|8|10|

#### Absolute value, Square root and Cube root

##### Input Code: 11

##### Redshift 12

```sql
 CREATE TABLE unary_operators
(
    col1 INTEGER,
    col2 INTEGER
);

INSERT INTO unary_operators VALUES
(14, 10),
(-8, 8),
(975, 173),
(-1273, 187);

SELECT
<!-- prettier-ignore -->
|/ col2 AS square_root,
||/ col1 AS cube_root,
@ col1 AS absolute_value
FROM unary_operators;
```

##### Results 7

```sql
+-------------------+--------------------+--------------+
<!-- prettier-ignore -->
|square_root|cube_root|absolute_value|
+-------------------+--------------------+--------------+
<!-- prettier-ignore -->
|3.1622776601683795|2.4101422641752306|14|
|2.8284271247461903|-2|8|
|13.152946437965905|9.915962413403873|975|
|13.674794331177344|-10.837841647592736|1273|
+-------------------+--------------------+--------------+
```

##### Output Code: 5

##### Snowflake 11

```sql
 CREATE TABLE unary_operators
(
    col1 INTEGER,
    col2 INTEGER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "12/17/2024",  "domain": "test" }}';

INSERT INTO unary_operators
VALUES
(14, 10),
(-8, 8),
(975, 173),
(-1273, 187);

SELECT
    SQRT(col2) AS square_root,
    CBRT(col1) AS cube_root,
    ABS(col1) AS absolute_value
FROM
    unary_operators;
```

##### Results 8

```sql
+-------------+--------------+--------------+
<!-- prettier-ignore -->
|square_root|cube_root|absolute_value|
+-------------+--------------+--------------+
<!-- prettier-ignore -->
|3.16227766|2.410142264|14|
|2.828427125|-2|8|
|13.152946438|9.915962413|975|
|13.674794331|-10.837841648|1273|
+-------------+--------------+--------------+
```

#### Known Issues 3

1. In Snowflake, it is possible to use the unary operators `+`and `-` with string values, however in
   Redshift it is not valid.

#### Related EWIs 3

No related EWIs.

## Bitwise operators

Operators

Translation for Bitwise Operators

### Conversion Table 3

<!-- prettier-ignore -->
|Redshift|Snowflake|Comments|
|---|---|---|---|
|[`&`](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (AND)|[`BITAND`](https://docs.snowflake.com/en/sql-reference/functions/bitand)|Fully supported by Snowflake|
|[`|`](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (OR)|[`BITOR`](https://docs.snowflake.com/en/sql-reference/functions/bitor)|Fully supported by Snowflake|
|[`<<`](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (Shift Left)|[`BITSHIFTLEFT`](https://docs.snowflake.com/en/sql-reference/functions/bitshiftleft)||
|[`>>`](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (Shift Right)|[`BITSHIFTRIGHT`](https://docs.snowflake.com/en/sql-reference/functions/bitshiftright)||
|[`#`](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html#r_compound_expressions-arguments) (XOR)|[`BITXOR`](https://docs.snowflake.com/en/sql-reference/functions/bitxor)|Fully supported by Snowflake|
|[`~`](https://docs.aws.amazon.com/redshift/latest/dg/r_compound_expressions.html) (NOT)|[`BITNOT`](https://docs.snowflake.com/en/sql-reference/functions/bitnot)|Fully supported by Snowflake|

### Sample Source Patterns 4

#### Setup data

##### Redshift 13

##### Query

```sql
 CREATE TABLE bitwise_demo (
    col1 INTEGER,
    col2 INTEGER,
    col3 INTEGER,
    col4 VARBYTE(5),
    col5 VARBYTE(7)
);

INSERT INTO bitwise_demo (col1, col2, col3, col4, col5) VALUES
-- Binary: 110, 011, 1111, 0100100001100101011011000110110001101111, 0100100001101001
(6, 3, 15, 'Hello'::VARBYTE, 'Hi'::VARBYTE),
-- Binary: 1010, 0101, 0111, 0100000101000010, 01000011
(10, 5, 7, 'AB'::VARBYTE, 'C'::VARBYTE),
-- Binary: 11111111, 10000000, 01000000, 010000100111100101100101, 01000111011011110110111101100100010000100111100101100101
(255, 128, 64, 'Bye'::VARBYTE, 'GoodBye'::VARBYTE),
-- Edge case with small numbers and a negative number
(1, 0, -1, 'Hey'::VARBYTE, 'Ya'::VARBYTE);
```

##### _Snowflake_

##### Query 2

```sql
 CREATE TABLE bitwise_demo (
    col1 INTEGER,
    col2 INTEGER,
    col3 INTEGER,
    col4 BINARY(5),
    col5 BINARY(7)
);

-- Binary: 110, 011, 1111, 0100100001100101011011000110110001101111, 0100100001101001
INSERT INTO bitwise_demo (col1, col2, col3, col4, col5) SELECT 6, 3, 15, TO_BINARY(HEX_ENCODE('Hello')), TO_BINARY(HEX_ENCODE('Hi'));
-- Binary: 1010, 0101, 0111, 0100000101000010, 01000011
INSERT INTO bitwise_demo (col1, col2, col3, col4, col5) SELECT 10, 5, 7, TO_BINARY(HEX_ENCODE('AB')), TO_BINARY(HEX_ENCODE('C'));
-- Binary: 11111111, 10000000, 01000000, 010000100111100101100101, 01000111011011110110111101100100010000100111100101100101
INSERT INTO bitwise_demo (col1, col2, col3, col4, col5) SELECT 255, 128, 64, TO_BINARY(HEX_ENCODE('Bye')), TO_BINARY(HEX_ENCODE('GoodBye'));
-- Edge case with small numbers and a negative number
INSERT INTO bitwise_demo (col1, col2, col3, col4, col5) SELECT 1, 0, -1, TO_BINARY(HEX_ENCODE('Hey')), TO_BINARY(HEX_ENCODE('Ya'));
```

#### Bitwise operators on integer values

##### Input Code: 12

##### Redshift 14

```sql
 SELECT
    -- Bitwise AND
    col1 & col2 AS bitwise_and,  -- col1 AND col2

    -- Bitwise OR
    col1 | col2 AS bitwise_or,   -- col1 OR col2

    -- Left Shift
    col3 << 1 AS left_shift_col3, -- col3 shifted left by 1

    -- Right Shift
    col3 >> 1 AS right_shift_col3, -- col3 shifted right by 1

    -- XOR
    col1 # col2 AS bitwise_xor, -- col1 XOR col2

    -- NOT
    ~ col3 AS bitwise_not -- NOT col3

FROM bitwise_demo;
```

##### Results 9

```sql
+-------------+------------+-----------------+------------------+-------------+-------------+
<!-- prettier-ignore -->
|bitwise_and|bitwise_or|left_shift_col3|right_shift_col3|bitwise_xor|bitwise_not|
+-------------+------------+-----------------+------------------+-------------+-------------+
<!-- prettier-ignore -->
|2|7|30|7|5|-16|
|0|15|14|3|15|-8|
|128|255|128|32|127|-65|
|0|1|-2|-1|1|0|
+-------------+------------+-----------------+------------------+-------------+-------------+
```

###### Output Code 5

##### Snowflake 12

```sql
 SELECT
        BITAND(
        -- Bitwise AND
        col1, col2) AS bitwise_and,  -- col1 AND col2
        BITOR(

        -- Bitwise OR
        col1, col2) AS bitwise_or,   -- col1 OR col2
        -- Left Shift
        --** SSC-FDM-PG0010 - RESULTS MAY VARY DUE TO THE BEHAVIOR OF SNOWFLAKE'S BITSHIFTLEFT BITWISE FUNCTION **
        BITSHIFTLEFT(
        col3, 1) AS left_shift_col3, -- col3 shifted left by 1
        -- Right Shift
        --** SSC-FDM-PG0010 - RESULTS MAY VARY DUE TO THE BEHAVIOR OF SNOWFLAKE'S BITSHIFTRIGHT BITWISE FUNCTION **
        BITSHIFTRIGHT(
        col3, 1) AS right_shift_col3, -- col3 shifted right by 1
        BITXOR(

        -- XOR
        col1, col2) AS bitwise_xor, -- col1 XOR col2
        -- NOT
        BITNOT(col3) AS bitwise_not -- NOT col3
FROM
        bitwise_demo;
```

##### Results 10

```sql
+-------------+------------+-----------------+------------------+-------------+-------------+
<!-- prettier-ignore -->
|bitwise_and|bitwise_or|left_shift_col3|right_shift_col3|bitwise_xor|bitwise_not|
+-------------+------------+-----------------+------------------+-------------+-------------+
<!-- prettier-ignore -->
|2|7|30|7|5|-16|
|0|15|14|3|15|-8|
|128|255|128|32|127|-65|
|0|1|-2|-1|1|0|
+-------------+------------+-----------------+------------------+-------------+-------------+
```

#### Bitwise operators on binary data

For the `BITAND`, `BITOR` and `BITXOR` functions the`'LEFT'` parameter is added to insert padding in
case both binary values have different length, this is done to avoid errors when comparing the
values in Snowflake.

##### Redshift 15

##### Query 3

```sql
 SELECT
    -- Bitwise AND
    col4 & col5 AS bitwise_and,  -- col4 AND col5

    -- Bitwise OR
    col4 | col5 AS bitwise_or,   -- col4 OR col5

    -- XOR
    col4 # col5 AS bitwise_xor, -- col4 XOR col5

    -- NOT
    ~ col4 AS bitwise_not -- NOT col4

FROM bitwise_demo;
```

##### Result 15

```sql
+-----------------+-----------------+-----------------+-------------+
<!-- prettier-ignore -->
|bitwise_and|bitwise_or|bitwise_xor|bitwise_not|
+-----------------+-----------------+-----------------+-------------+
<!-- prettier-ignore -->
|0x0000004869|0x48656C6C6F|0x48656C2406|0xB79A939390|
|0x0042|0x4143|0x4101|0xBEBD|
|0x00000000427965|0x476F6F64427965|0x476F6F64000000|0xBD869A|
|0x004161|0x487D79|0x483C18|0xB79A86|
+-----------------+-----------------+-----------------+-------------+
```

##### _Snowflake_ 2

##### Query 4

```sql
 SELECT
    BITAND(
    -- Bitwise AND
    col4, col5, 'LEFT') AS bitwise_and,  -- col4 AND col5
    BITOR(

    -- Bitwise OR
    col4, col5, 'LEFT') AS bitwise_or,   -- col4 OR col5

    -- XOR
    BITXOR(col4, col5, 'LEFT') AS bitwise_xor, -- col4 XOR col5

    -- NOT
    BITNOT(col4) AS bitwise_not -- NOT col4

    FROM bitwise_demo;
```

##### Result 16

```sql
+---------------+---------------+---------------+-------------+
<!-- prettier-ignore -->
|bitwise_and|bitwise_or|bitwise_xor|bitwise_not|
+---------------+---------------+---------------+-------------+
<!-- prettier-ignore -->
|0000004869|48656C6C6F|48656C2406|B79A939390|
|0042|4143|4101|BEBD|
|00000000427965|476F6F64427965|476F6F64000000|BD869A|
|004161|487D79|483C18|B79A86|
+---------------+---------------+---------------+-------------+
```

### Known Issues 4

No issues were found.

### Related EWIs 4

- [SSC-FDM-PG0010](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0010):
  Results may vary due to the behavior of Snowflake’s bitwise function.
