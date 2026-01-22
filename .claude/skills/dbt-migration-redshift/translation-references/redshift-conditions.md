---
description:
  A BETWEEN condition tests expressions for inclusion in a range of values, using the keywords
  BETWEEN and AND. (Redshift SQL Language Reference BETWEEN condition)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-conditions
title: SnowConvert AI - Redshift - Conditions | Snowflake Documentation
---

## BETWEEN

### Description

> A `BETWEEN` condition tests expressions for inclusion in a range of values, using the keywords
> `BETWEEN` and `AND`.
> ([Redshift SQL Language Reference BETWEEN condition](https://docs.aws.amazon.com/redshift/latest/dg/r_range_condition.html))

### Grammar Syntax

```sql
 expression [ NOT ] BETWEEN expression AND expression
```

#### Note

This function is fully supported by
[Snowflake](https://docs.snowflake.com/en/sql-reference/functions/coalesce).

### Sample Source Patterns

#### Setup Table

##### Redshift

```sql
 CREATE TABLE sales (
    id INTEGER IDENTITY(1,1),
    price FLOAT,
    departmentId INTEGER,
    saleDate DATE
);

INSERT INTO sales (price, departmentId, saleDate) VALUES
(5000, 1, '2008-01-01'),
(8000, 1, '2018-01-01'),
(5000, 2, '2010-01-01'),
(7000, 3, '2010-01-01'),
(5000, 1, '2018-01-01'),
(4000, 4, '2010-01-01'),
(3000, 4, '2018-01-01'),
(9000, 5, '2008-01-01'),
(7000, 5, '2018-01-01'),
(6000, 5, '2006-01-01'),
(5000, 5, '2008-01-01'),
(5000, 4, '2018-01-01'),
(8000, 3, '2006-01-01'),
(7000, 3, '2016-01-01'),
(2000, 2, '2018-01-01');
```

##### Snowflake

```sql
 CREATE TABLE sales (
    id INTEGER IDENTITY(1,1) ORDER,
    price FLOAT,
    departmentId INTEGER,
    saleDate DATE
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/08/2025",  "domain": "test" }}';

INSERT INTO sales (price, departmentId, saleDate) VALUES
(5000, 1, '2008-01-01'),
(8000, 1, '2018-01-01'),
(5000, 2, '2010-01-01'),
(7000, 3, '2010-01-01'),
(5000, 1, '2018-01-01'),
(4000, 4, '2010-01-01'),
(3000, 4, '2018-01-01'),
(9000, 5, '2008-01-01'),
(7000, 5, '2018-01-01'),
(6000, 5, '2006-01-01'),
(5000, 5, '2008-01-01'),
(5000, 4, '2018-01-01'),
(8000, 3, '2006-01-01'),
(7000, 3, '2016-01-01'),
(2000, 2, '2018-01-01');
```

##### Input Code

##### Redshift 2

```sql
 SELECT COUNT(*) FROM sales
WHERE departmentId BETWEEN 2 AND 4;

SELECT * FROM sales
WHERE departmentId BETWEEN 4 AND 2;

SELECT * FROM sales
WHERE departmentId NOT BETWEEN 4 AND 2;

SELECT * FROM sales
WHERE departmentId BETWEEN 2 AND 4
AND saleDate BETWEEN '2010-01-01' and '2016-01-01';

select 'some ' between c_start and c_end
from( select 'same' as c_start, 'some' as c_end );
```

##### Results

<!-- prettier-ignore -->
|count|
|---|
|8|

<!-- prettier-ignore -->
|id|price|departmentid|saledate|
|---|---|---|---|
|     |       |              |          |

<!-- prettier-ignore -->
|id|price|departmentid|saledate|
|---|---|---|---|
|1|5000|1|2008-01-01|
|2|8000|1|2018-01-01|
|3|5000|2|2010-01-01|
|4|7000|3|2010-01-01|
|5|5000|1|2018-01-01|
|6|4000|4|2010-01-01|
|7|3000|4|2018-01-01|
|8|9000|5|2008-01-01|
|9|7000|5|2018-01-01|
|10|6000|5|2006-01-01|
|11|5000|5|2008-01-01|
|12|5000|4|2018-01-01|
|13|8000|3|2006-01-01|
|14|7000|3|2016-01-01|
|15|2000|2|2018-01-01|

<!-- prettier-ignore -->
|id|price|departmentid|saledate|
|---|---|---|---|
|3|5000|2|2010-01-01|
|4|7000|3|2010-01-01|
|6|4000|4|2010-01-01|
|14|7000|3|2016-01-01|

##### Output Code

##### Snowflake 2

```sql
 SELECT COUNT(*) FROM
    sales
WHERE departmentId BETWEEN 2 AND 4;

SELECT * FROM
    sales
WHERE departmentId BETWEEN 4 AND 2;

SELECT * FROM
    sales
WHERE departmentId NOT BETWEEN 4 AND 2;

SELECT * FROM
    sales
WHERE departmentId BETWEEN 2 AND 4
AND saleDate BETWEEN '2010-01-01' and '2016-01-01';

select
    RTRIM( 'some ') between c_start and c_end
from( select 'same' as c_start, 'some' as c_end );
```

##### Results 2

<!-- prettier-ignore -->
|count|
|---|
|8|

<!-- prettier-ignore -->
|id|price|departmentid|saledate|
|---|---|---|---|
|     |       |              |          |

<!-- prettier-ignore -->
|id|price|departmentid|saledate|
|---|---|---|---|
|1|5000|1|2008-01-01|
|2|8000|1|2018-01-01|
|3|5000|2|2010-01-01|
|4|7000|3|2010-01-01|
|5|5000|1|2018-01-01|
|6|4000|4|2010-01-01|
|7|3000|4|2018-01-01|
|8|9000|5|2008-01-01|
|9|7000|5|2018-01-01|
|10|6000|5|2006-01-01|
|11|5000|5|2008-01-01|
|12|5000|4|2018-01-01|
|13|8000|3|2006-01-01|
|14|7000|3|2016-01-01|
|15|2000|2|2018-01-01|

<!-- prettier-ignore -->
|id|price|departmentid|saledate|
|---|---|---|---|
|3|5000|2|2010-01-01|
|4|7000|3|2010-01-01|
|6|4000|4|2010-01-01|
|14|7000|3|2016-01-01|

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## Comparison Condition

Conditions

### Description 2

> Comparison conditions state logical relationships between two values. All comparison conditions
> are binary operators with a Boolean return type.
>
> ([RedShift SQL Language Reference Comparison Condition](https://docs.aws.amazon.com/redshift/latest/dg/r_comparison_condition.html))

### Grammar Syntax 2

Redshift supports the comparison operators described in the following table:

<!-- prettier-ignore -->
|Operator|Syntax|Description|
|---|---|---|---|---|
|<|a < b|Value a is less than value b.|
|>|a > b|Value a is greater than value b.|
|<=|a <= b|Value a is less than or equal to value b.|
|>=|a >= b|Value a is greater than or equal to value b.|
|=|a = b|Value a is equal to value b.|
|<>|!=|a <> b|a != b|Value a is not equal to value b.|
|ANY|SOME|a = ANY(subquery)|Value a is equal to any value returned by the subquery.|
|ALL|a <> ALL or != ALL (subquery)|Value a is not equal to any value returned by the subquery.|
|IS TRUE|FALSE|UNKNOWN|a IS TRUE|Value a is Boolean TRUE.|

### Use of comparison operators on Strings

It is important to note that in Redshift, comparison operators on strings ignore trailing blank
spaces. To replicate this behavior in Snowflake, the transformation applies the `RTRIM` function to
remove trailing spaces, ensuring equivalent functionality. For more information:
[Significance of trailing blanks](https://docs.aws.amazon.com/redshift/latest/dg/r_Character_types.html#r_Character_types-significance-of-trailing-blanks)

### Conversion Table

Most of the operators are directly supported by Snowflake; however, the following operators require
transformation:

<!-- prettier-ignore -->
|Redshift|Snowflake|Comments|
|---|---|---|
|(expression) IS TRUE|expression|Condition is `TRUE`.|
|(expression) IS FALSE|NOT (expression)|Condition is `FALSE`.|
|(expression) IS UNKNOWN|expression IS NULL|Expression evaluates to `NULL` (same as `UNKNOWN`).|

### Sample Source Patterns 2

#### Input Code: 2

##### Redshift 3

```sql
 CREATE TABLE example_data (
    id INT,
    value INT,
    status BOOLEAN,
    category VARCHAR(10)
);

INSERT INTO example_data (id, value, status, category) VALUES
(1, 50, TRUE, 'A'),
(2, 30, FALSE, 'B'),
(3, 40, NULL, 'C'),
(4, 70, TRUE, 'A '),
(5, 60, FALSE, 'B');

SELECT *
FROM example_data
WHERE value < 60 AND value > 40;

SELECT *
FROM example_data
WHERE value <= 60 AND value >= 40;

SELECT *
FROM example_data
WHERE category = 'A';

SELECT *
FROM example_data
WHERE category != 'A' AND category <> 'B';

SELECT *
FROM example_data
WHERE category = ANY(SELECT category FROM example_data WHERE value > 60); --SOME

SELECT *
FROM example_data
WHERE value <> ALL (SELECT value FROM example_data WHERE status = TRUE);

SELECT *
FROM example_data
WHERE status IS TRUE;

SELECT *
FROM example_data
WHERE status IS FALSE;

SELECT *
FROM example_data
WHERE status IS UNKNOWN;
```

##### Results 3

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|
|3|40|null|C|
|5|60|false|B|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|
|4|70|true|A|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|3|40|null|C|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|
|4|70|true|A|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|2|30|false|B|
|4|40|null|C|
|5|60|false|B|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|
|4|70|true|A|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|2|30|false|B|
|5|60|false|B|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|4|40|null|C|

###### Output Code 2

##### Snowflake 3

```sql
 CREATE TABLE example_data (
    id INT,
    value INT,
    status BOOLEAN,
    category VARCHAR(10)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}';

INSERT INTO example_data (id, value, status, category) VALUES
(1, 50, TRUE, 'A'),
(2, 30, FALSE, 'B'),
(3, 40, NULL, 'C'),
(4, 70, TRUE, 'A '),
(5, 60, FALSE, 'B');

SELECT *
FROM
    example_data
WHERE value < 60 AND value > 40;

SELECT *
FROM
    example_data
WHERE value <= 60 AND value >= 40;

SELECT *
FROM
    example_data
WHERE category = 'A';

SELECT *
FROM
    example_data
WHERE category != 'A' AND category <> 'B';

SELECT *
FROM
    example_data
WHERE category = ANY(SELECT category FROM
            example_data
        WHERE value > 60); --SOME

SELECT *
FROM
    example_data
WHERE value <> ALL (SELECT value FROM
            example_data
        WHERE status = TRUE);

SELECT *
FROM
    example_data
WHERE status;

SELECT *
FROM
    example_data
WHERE
    NOT status;

SELECT *
FROM
    example_data
WHERE status IS NULL;
```

##### Results 4

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|
|3|40|null|C|
|5|60|false|B|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|
|4|70|true|A|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|3|40|null|C|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|
|4|70|true|A|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|2|30|false|B|
|4|40|null|C|
|5|60|false|B|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|1|50|true|A|
|4|70|true|A|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|2|30|false|B|
|5|60|false|B|

<!-- prettier-ignore -->
|id|value|status|category|
|---|---|---|---|
|4|40|null|C|

### Known Issues 2

No issues were found.

### Related EWIs 2

There are no known issues.

## EXISTS

### Description 3

> EXISTS conditions test for the existence of rows in a subquery, and return true if a subquery
> returns at least one row. If NOT is specified, the condition returns true if a subquery returns no
> rows.
> ([Redshift SQL Language Reference EXISTS condition](https://docs.aws.amazon.com/redshift/latest/dg/r_exists_condition.html))

### Grammar Syntax 3

```sql
 [ NOT ] EXISTS (table_subquery)
```

#### Note 2

This function is fully supported by
[Snowflake](https://docs.snowflake.com/en/sql-reference/functions/coalesce).

### Sample Source Patterns 3

#### Setup Table 2

```sql
 CREATE TABLE ExistsTest (
    id INTEGER,
    name VARCHAR(30),
    lastname VARCHAR(30)
);

INSERT INTO ExistsTest (id, name, lastname) VALUES
 (1, 'name1', 'lastname1'),
 (2, 'name2', NULL),
 (3, 'name3', 'lastname3'),
 (4, 'name4', NULL);
```

```sql
 CREATE TABLE ExistsTest (
    id INTEGER,
    name VARCHAR(30),
    lastname VARCHAR(30)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/08/2025",  "domain": "test" }}'

INSERT INTO ExistsTest (id, name, lastname) VALUES
 (1, 'name1', 'lastname1'),
 (2, 'name2', NULL),
 (3, 'name3', 'lastname3'),
 (4, 'name4', NULL);
```

##### Input Code: 3

##### Redshift 4

```sql
 SELECT * FROM ExistsTest
WHERE EXISTS (
SELECT 1 FROM ExistsTest
WHERE lastname = 'lastname1'
)
ORDER BY id;
```

##### Results 5

<!-- prettier-ignore -->
|ID|NAME|LASTNAME|
|---|---|---|
|1|name1|lastname1|
|2|name2|NULL|
|3|name3|lastname3|
|4|name4|NULL|

##### Output Code: 2

##### Snowflake 4

```sql
 SELECT * FROM
ExistsTest
WHERE EXISTS (
SELECT 1 FROM
ExistsTest
WHERE lastname = 'lastname1'
)
ORDER BY id;
```

##### Results 6

<!-- prettier-ignore -->
|ID|NAME|LASTNAME|
|---|---|---|
|1|name1|lastname1|
|2|name2|NULL|
|3|name3|lastname3|
|4|name4|NULL|

### Related EWIs 3

No related EWIs.

### Known Issues 3

No issues were found.

## IN

### Description 4

> An IN condition tests a value for membership in a set of values or in a subquery.
> ([Redshift SQL Language Reference IN condition](https://docs.aws.amazon.com/redshift/latest/dg/r_in_condition.html))

### Grammar Syntax 4

```sql
 expression [ NOT ] IN (expr_list | table_subquery)
```

#### Note 3

This function is fully supported by
[Snowflake](https://docs.snowflake.com/en/sql-reference/functions/coalesce).

### Sample Source Patterns 4

#### Setup Table 3

##### Redshift 5

```sql
 CREATE TABLE sales (
    id INTEGER IDENTITY(1,1),
    price FLOAT,
    saleDate DATE
);

INSERT INTO sales (price, saleDate) VALUES
(5000, '12/19/2024'),
(4000, '12/18/2024'),
(2000, '12/17/2024'),
(1000, '11/11/2024'),
(7000, '10/10/2024'),
(7000, '05/12/2024');

CREATE TABLE InTest (
col1 Varchar(20) COLLATE CASE_INSENSITIVE,
col2 Varchar(30) COLLATE CASE_SENSITIVE,
d1 date,
num integer,
idx integer);

INSERT INTO InTest values ('A', 'A', ('2012-03-02'), 4,6);
INSERT INTO InTest values ('a', 'a', ('2014-01-02'), 41,7);
```

##### Snowflake 5

```sql
 CREATE TABLE InTest (
    id INTEGER IDENTITY(1,1) ORDER,
    price FLOAT,
    saleDate DATE
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/09/2025",  "domain": "test" }}';

INSERT INTO InTest (price, saleDate) VALUES
(5000, '12/19/2024'),
(4000, '12/18/2024'),
(2000, '12/17/2024'),
(1000, '11/11/2024'),
(7000, '10/10/2024'),
(7000, '05/12/2024');

CREATE TABLE InTest (
col1 Varchar(20) COLLATE 'en-ci',
col2 Varchar(30) COLLATE 'en-cs',
d1 date,
num integer,
idx integer)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/16/2025",  "domain": "test" }}';

INSERT INTO InTest
values ('A', 'A', ('2012-03-02'), 4,6);
INSERT INTO InTest
values ('a', 'a', ('2014-01-02'), 41,7);
```

##### Input Code: 4

##### Redshift 6

```sql
 SELECT * FROM sales
WHERE id IN (2,3);

SELECT 5 IN (
SELECT id FROM sales
WHERE price = 7000
) AS ValidId;

select t.col1 in ('a ','b','c') as r1, t.col2 in ('a ','b','c') as r2 from InTest t order by t.idx;
```

##### Results 7

<!-- prettier-ignore -->
|ID|PRICE|SALEDATE|
|---|---|---|
|2|4000|2024-12-18|
|3|2000|2024-12-17|

<!-- prettier-ignore -->
|VALIDID|
|---|
|TRUE|

<!-- prettier-ignore -->
|R1|R2|
|---|---|
|TRUE|FALSE|
|TRUE|TRUE|

##### Output Code: 3

##### Snowflake 6

```sql
 SELECT * FROM
    sales
WHERE id IN (2,3);

SELECT 5 IN (
SELECT id FROM
 sales
WHERE price = 7000
) AS ValidId;

select t.col1 in (RTRIM('a '), RTRIM('b'), RTRIM('c')) as r1, t.col2 in (RTRIM('a '), RTRIM('b'), RTRIM('c')) as r2 from
InTest t order by t.idx;
```

##### Results 8

<!-- prettier-ignore -->
|ID|PRICE|SALEDATE|
|---|---|---|
|2|4000|2024-12-18|
|3|2000|2024-12-17|

<!-- prettier-ignore -->
|VALIDID|
|---|
|TRUE|

<!-- prettier-ignore -->
|R1|R2|
|---|---|
|TRUE|FALSE|
|TRUE|TRUE|

### Related EWIs 4

No related EWIs.

### Known Issues 4

No issues were found.

## Logical Conditions

### Description 5

> Logical conditions combine the result of two conditions to produce a single result. All logical
> conditions are binary operators with a Boolean return type.
> ([Redshift SQL Language reference Logical Conditions](https://docs.aws.amazon.com/redshift/latest/dg/r_logical_condition.html)).

#### Note 4

This grammar is fully supported in
[Snowflake](https://docs.snowflake.com/en/sql-reference/operators-logical).

### Grammar Syntax 5

```sql
expression
{ AND | OR }
expression
NOT expression
```

<!-- prettier-ignore -->
|E1|E2|E1 AND E2|E1 OR E2|NOT E2|
|---|---|---|---|---|
|TRUE|TRUE|TRUE|TRUE|FALSE|
|TRUE|FALSE|FALSE|TRUE|TRUE|
|TRUE|UNKNOWN|UNKNOWN|TRUE|UNKNOWN|
|FALSE|TRUE|FALSE|TRUE||
|FALSE|FALSE|FALSE|FALSE||
|FALSE|UNKNOWN|FALSE|UNKNOWN||
|UNKNOWN|TRUE|UNKNOWN|TRUE||
|UNKNOWN|FALSE|FALSE|UNKNOWN||
|UNKNOWN|UNKNOWN|UNKNOWN|UNKNOWN||

### Sample Source Patterns 5

#### Setup data

##### Redshift 7

```sql
 CREATE TABLE employee (
    employee_id INT,
    active BOOLEAN,
    department VARCHAR(100),
    hire_date DATE,
    salary INT
);

INSERT INTO employee (employee_id, active, department, hire_date, salary) VALUES
    (1, TRUE, 'Engineering', '2021-01-15', 70000),
    (2, FALSE, 'HR', '2020-03-22', 50000),
    (3, NULL, 'Marketing', '2019-05-10', 60000),
    (4, TRUE, 'Engineering', NULL, 65000),
    (5, TRUE, 'Sales', '2018-11-05', NULL);
```

##### Input Code: 5

##### Redshift 8

```sql
 SELECT
    employee_id,
    (active AND department = 'Engineering') AS is_active_engineering,
    (department = 'HR' OR salary > 60000) AS hr_or_high_salary,
    NOT active AS is_inactive,
    (hire_date IS NULL) AS hire_date_missing,
    (salary IS NULL OR salary < 50000) AS low_salary_or_no_salary
FROM employee;
```

##### Results 9

<!-- prettier-ignore -->
|EMPLOYEE_ID|IS_ACTIVE_ENGINEERING|HR_OR_HIGH_SALARY|IS_INACTIVE|HIRE_DATE_MISSING|LOW_SALARY_OR_NO_SALARY|
|---|---|---|---|---|---|
|1|TRUE|TRUE|FALSE|FALSE|FALSE|
|2|FALSE|TRUE|TRUE|FALSE|FALSE|
|3|FALSE|FALSE|NULL|FALSE|FALSE|
|4|TRUE|TRUE|FALSE|TRUE|FALSE|
|5|FALSE|NULL|FALSE|FALSE|TRUE|

###### Output Code 3

##### Snowflake 7

```sql
 SELECT
    employee_id,
    (active AND department = 'Engineering') AS is_active_engineering,
    (department = 'HR' OR salary > 60000) AS hr_or_high_salary,
    NOT active AS is_inactive,
    (hire_date IS NULL) AS hire_date_missing,
    (salary IS NULL OR salary < 50000) AS low_salary_or_no_salary
FROM
    employee;
```

##### Results 10

<!-- prettier-ignore -->
|EMPLOYEE_ID|IS_ACTIVE_ENGINEERING|HR_OR_HIGH_SALARY|IS_INACTIVE|HIRE_DATE_MISSING|LOW_SALARY_OR_NO_SALARY|
|---|---|---|---|---|---|
|1|TRUE|TRUE|FALSE|FALSE|FALSE|
|2|FALSE|TRUE|TRUE|FALSE|FALSE|
|3|FALSE|FALSE|NULL|FALSE|FALSE|
|4|TRUE|TRUE|FALSE|TRUE|FALSE|
|5|FALSE|NULL|FALSE|FALSE|TRUE|

### Known Issues 5

No issues were found.

### Related EWIs 5

There are no known issues.

## NULL

### Description 6

> The null condition tests for nulls, when a value is missing or unknown.
> ([Redshift SQL Language Reference NULL condition](https://docs.aws.amazon.com/redshift/latest/dg/r_null_condition.html))

### Grammar Syntax 6

```sql
 expression IS [ NOT ] NULL
```

#### Note 5

This function is fully supported by
[Snowflake](https://docs.snowflake.com/en/sql-reference/functions/coalesce).

### Sample Source Patterns 6

#### Setup Table 4

##### Redshift 9

```sql
 CREATE TABLE NullTest (
    id INTEGER,
    name VARCHAR(30),
    lastname VARCHAR(30)
);

INSERT INTO NullTest (id, name, lastname) VALUES
 (1, 'name1', 'lastname1'),
 (2, 'name2', NULL),
 (3, 'name3', 'lastname3'),
 (4, 'name4', NULL);
```

##### Snowflake 8

```sql
 CREATE TABLE NullTest (
    id INTEGER,
    name VARCHAR(30),
    lastname VARCHAR(30)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/08/2025",  "domain": "test" }}';

INSERT INTO NullTest (id, name, lastname) VALUES
 (1, 'name1', 'lastname1'),
 (2, 'name2', NULL),
 (3, 'name3', 'lastname3'),
 (4, 'name4', NULL);
```

##### Input Code: 6

##### Redshift 10

```sql
 SELECT * FROM nulltest
WHERE lastname IS NULL;
```

##### Results 11

<!-- prettier-ignore -->
|ID|NAME|LASTNAME|
|---|---|---|
|2|name2|NULL|
|4|name4|NULL|

##### Output Code: 4

##### Snowflake 9

```sql
 SELECT * FROM
    nulltest
WHERE lastname IS NULL;
```

##### Results 12

<!-- prettier-ignore -->
|ID|NAME|LASTNAME|
|---|---|---|
|2|name2|NULL|
|4|name4|NULL|

### Known Issues 6

No issues were found.

### Related EWIs 6

No related EWIs.

## Pattern-matching conditions

### Description 7

A pattern-matching operator searches a string for a pattern specified in the conditional expression
and returns true or false depend on whether it finds a match. Amazon Redshift uses three methods for
pattern matching:

- [LIKE expressions](#like) The LIKE operator compares a string expression, such as a column name,
  with a pattern that uses the wildcard characters `%` (percent) and `_` (underscore). LIKE pattern
  matching always covers the entire string. LIKE performs a case-sensitive match and ILIKE performs
  a case-insensitive match.
- [SIMILAR TO regular expressions](#similar-to) The SIMILAR TO operator matches a string expression
  with a SQL standard regular expression pattern, which can include a set of pattern-matching
  metacharacters that includes the two supported by the LIKE operator. SIMILAR TO matches the entire
  string and performs a case-sensitive match.
- [POSIX-style regular expressions](#posix-operators) POSIX regular expressions provide a more
  powerful means for pattern matching than the LIKE and SIMILAR TO operators. POSIX regular
  expression patterns can match any portion of the string and performs a case-sensitive match.
  ([Redshift SQL Language reference Pattern-matching conditions](https://docs.aws.amazon.com/redshift/latest/dg/pattern-matching-conditions.html)).

### Known Issues 7

- In Snowflake, the behavior for scenarios such as (`LIKE`, `SIMILAR` TO, and `POSIX Operators`) can
  vary when the column is of type CHAR. For example:

### Code

```sql
 CREATE TEMPORARY TABLE pattern_matching_sample (
  col1 CHAR(10),
  col2 VARCHAR(10)
);

INSERT INTO pattern_matching_sample VALUES ('1','1');
INSERT INTO pattern_matching_sample VALUES ('1234567891','1234567891');
INSERT INTO pattern_matching_sample VALUES ('234567891','234567891');

SELECT
col1 LIKE '%1' as "like(CHAR(10))",
COL2 LIKE '%1' as "like(VARCHAR(10))"
FROM
pattern_matching_sample;
```

#### Redshift Results

<!-- prettier-ignore -->
|like(CHAR(10))|like(VARCHAR(10))|
|---|---|
|FALSE|TRUE|
|TRUE|TRUE|
|FALSE|TRUE|

##### Snowflake Results

<!-- prettier-ignore -->
|like(CHAR(10))|like(VARCHAR(10))|
|---|---|
|TRUE|TRUE|
|TRUE|TRUE|
|TRUE|TRUE|

It appears that, because CHAR(10) is “fixed-length,” it assumes the ‘%1’ pattern must match a ‘1’ in
the 10th position of a CHAR(10) column. However, in Snowflake, it matches if a ‘1’ exists in the
string, with any sequence of zero or more characters preceding it.

## LIKE

Pattern-matching conditions

### Description 8

> The LIKE operator compares a string expression, such as a column name, with a pattern that uses
> the wildcard characters % (percent) and \_ (underscore). LIKE pattern matching always covers the
> entire string. To match a sequence anywhere within a string, the pattern must start and end with a
> percent sign.
> ([Redshift SQL Language reference LIKE](https://docs.aws.amazon.com/redshift/latest/dg/r_patternmatching_condition_like.html)).

#### Note 6

This grammar is fully supported in
[Snowflake](https://docs.snowflake.com/en/sql-reference/operators-logical).

#### Note 7

In Snowflake the cases where the escape character is not provided, the default Redshift escape
character `'\\'` will be added for full equivalence.

### Grammar Syntax 7

```sql
 expression [ NOT ] LIKE | ILIKE pattern [ ESCAPE 'escape_char' ]
```

### Sample Source Patterns 7

#### **Setup data**

##### Redshift 11

```sql
 CREATE TABLE like_ex(name VARCHAR(20));

INSERT INTO like_ex VALUES
  ('John  Dddoe'),
  ('Joe   Doe'),
  ('Joe   Doe '),
  (' Joe   Doe '),
  (' Joe \n Doe '),
  ('John_down'),
  ('Joe down'),
  ('Elaine'),
  (''),
  (null),
  ('1000 times'),
  ('100%');
```

#### Like 2

##### Input Code: 7

##### Redshift 12

```sql
SELECT name
  FROM like_ex
  WHERE name LIKE '%Jo%oe%'
  ORDER BY name;
```

##### Results 13

<!-- prettier-ignore -->
|NAME|
|---|
|Joe Doe|
|Joe Doe|
|Joe Doe|
|Joe Doe|
|John Dddoe|

###### Output Code 4

##### Snowflake 10

```sql
 SELECT name
  FROM like_ex
  WHERE name LIKE '%Jo%oe%' ESCAPE '\\'
  ORDER BY name;
```

##### Results 14

<!-- prettier-ignore -->
|NAME|
|---|
|Joe Doe|
|Joe Doe|
|Joe Doe|
|Joe Doe|
|John Dddoe|

#### Not like

##### Input Code: 8

##### Redshift 13

```sql
 SELECT name
  FROM like_ex
  WHERE name NOT LIKE '%Jo%oe%'
  ORDER BY name;
```

##### Results 15

<!-- prettier-ignore -->
|NAME|
|---|
|            |
|100%|
|1000 times|
|Elaine|
|Joe down|
|John_down|

dd

###### Output Code 5

##### Snowflake 11

```sql
 SELECT name
  FROM like_ex
  WHERE name NOT LIKE '%Jo%oe%' ESCAPE '\\'
  ORDER BY name;
```

##### Results 16

<!-- prettier-ignore -->
|NAME|
|---|
|            |
|100%|
|1000 times|
|Elaine|
|Joe down|
|John_down|

#### Escape characters

##### Input Code: 9

##### Redshift 14

```sql
 SELECT name
  FROM like_ex
  WHERE name LIKE '%J%h%^_do%' ESCAPE '^'
  ORDER BY name;

SELECT name
 FROM like_ex
 WHERE name LIKE '100\\%'
 ORDER BY 1;
```

##### Results 17

<!-- prettier-ignore -->
|NAME|
|---|
|John_down|

<!-- prettier-ignore -->
|NAME|
|---|
|100%|

###### Output Code 6

##### Snowflake 12

```sql
 SELECT name
  FROM like_ex
  WHERE name LIKE '%J%h%^_do%' ESCAPE '^'
  ORDER BY name;

SELECT name
 FROM like_ex
 WHERE name LIKE '100\\%' ESCAPE '\\'
 ORDER BY 1;
```

##### Results 18

<!-- prettier-ignore -->
|NAME|
|---|
|John_down|

<!-- prettier-ignore -->
|NAME|
|---|
|100%|

#### ILike

##### Input Code: 10

##### Redshift 15

```sql
 SELECT 'abc' LIKE '_B_' AS r1,
       'abc' ILIKE '_B_' AS r2;
```

##### Results 19

<!-- prettier-ignore -->
|R1|R2|
|---|---|
|FALSE|TRUE|

###### Output Code 7

##### Snowflake 13

```sql
 SELECT 'abc' LIKE '_B_' ESCAPE '\\' AS r1,
       'abc' ILIKE '_B_' ESCAPE '\\' AS r2;
```

##### Results 20

<!-- prettier-ignore -->
|R1|R2|
|---|---|
|FALSE|TRUE|

#### Operators

The following operators are translated as follows:

<!-- prettier-ignore -->
|Redshift|Snowflake|
|---|---|
|~~|LIKE|
|!~~|NOT LIKE|
|~~\*|ILIKE|
|!~~\*|NOT ILIKE|

##### Input Code: 11

##### Redshift 16

```sql
 SELECT 'abc' ~~ 'abc' AS r1,
       'abc' !~~ 'a%' AS r2,
       'abc' ~~* '_B_' AS r3,
       'abc' !~~* '_B_' AS r4;
```

##### Results 21

<!-- prettier-ignore -->
|R1|R2|R3|R4|
|---|---|---|---|
|TRUE|FALSE|TRUE|FALSE|

###### Output Code 8

##### Snowflake 14

```sql
 SELECT 'abc' LIKE 'abc' ESCAPE '\\' AS r1,
       'abc' NOT LIKE 'a%' ESCAPE '\\' AS r2,
       'abc' ILIKE '_B_' ESCAPE '\\' AS r3,
       'abc' NOT ILIKE '_B_' ESCAPE '\\' AS r4;
```

##### Results 22

<!-- prettier-ignore -->
|R1|R2|R3|R4|
|---|---|---|---|
|TRUE|FALSE|TRUE|FALSE|

### Known Issues 8

1. The behavior of fixed char types may differ. Click [here](#id12) for more information.

### Related EWIs 7

There are no known issues.

## POSIX Operators

Pattern-matching conditions

### Description 9

> A POSIX regular expression is a sequence of characters that specifies a match pattern. A string
> matches a regular expression if it is a member of the regular set described by the regular
> expression. POSIX regular expression patterns can match any portion of a string.
> ([Redshift SQL Language reference POSIX Operators](https://docs.aws.amazon.com/redshift/latest/dg/pattern-matching-conditions-posix.html)).

Warning

This grammar is partially supported in
[Snowflake](https://docs.snowflake.com/en/sql-reference/operators-logical). POSIX Operators are
transformed to [REGEXP_COUNT](https://docs.snowflake.com/en/sql-reference/functions/regexp_count) in
Snowflake.

### Grammar Syntax 8

```sql
 expression [ ! ] ~ pattern
```

### POSIX pattern-matching metacharacters

POSIX pattern matching supports the following metacharacters (all the cases are supported in
Snowflake):

<!-- prettier-ignore -->
|POSIX|Description|
|---|---|---|
|.|Matches any single character.|
|`*`|Matches zero or more occurrences.|
|`+`|Matches one or more occurrences.|
|`?`|Matches zero or one occurrence.|
|`|`|Specifies alternative matches.|
|`^`|Matches the beginning-of-line character.|
|`$`|Matches the end-of-line character.|
|`$`|Matches the end of the string.|
|[ ]|Brackets specify a matching list, that should match one expression in the list.|
|`( )`|Parentheses group items into a single logical item.|
|`{m}`|Repeat the previous item exactly _m_ times.|
|`{m,}`|Repeat the previous item _m_ or more times.|
|`{m,n}`|Repeat the previous item at least _m_ and not more than _n_ times.|
|`[: :]`|Matches any character within a POSIX character class. In the following character classes, Amazon Redshift supports only ASCII characters, just like Snowflake: `[:alnum:]`, `[:alpha:]`, `[:lower:]`, `[:upper:]`|

The parameters ‘m’ (enables multiline mode) and ‘s’ (allows the POSIX wildcard character `.` to
match new lines) are used to achieve full equivalence in Snowflake. For more information please
refer to
[Specifying the parameters for the regular expression in Snowflake](https://docs.snowflake.com/en/sql-reference/functions-regexp#specifying-the-parameters-for-the-regular-expression).

### Sample Source Patterns 8

#### **Setup data** 2

##### Redshift 17

```sql
 CREATE TABLE posix_test_table (
    id INT,
    column_name VARCHAR(255)
);

INSERT INTO posix_test_table (id, column_name)
VALUES
    (1, 'abc123\nhello world'),
    (2, 'test string\nwith multiple lines\nin this entry'),
    (3, '123abc\nanother line\nabc123'),
    (4, 'line1\nline2\nline3'),
    (5, 'start\nmiddle\nend'),
    (6, 'a@b#c!\nmore text here'),
    (7, 'alpha\nbeta\ngamma'),
    (8, 'uppercase\nlowercase'),
    (9, 'line1\nline2\nline3\nline4'),
    (10, '1234567890\nmore digits'),
    (11, 'abc123\nabc456\nabc789'),
    (12, 'start\nend\nmiddle'),
    (13, 'this is the first line\nthis is the second line'),
    (14, 'special characters\n!@#$%^&*()');
```

#### . : Matches any character

##### Input Code: 12

##### Redshift 18

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE column_name ~ 'a.c';
```

##### Results 23

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|1|abc123 hello world|
|3|123abc another line abc123|
|11|abc123 abc456 abc789|

###### Output Code 9

##### Snowflake 15

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, 'a.c', 1, 'ms') > 0;
```

##### Results 24

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|1|abc123 hello world|
|3|123abc another line abc123|
|11|abc123 abc456 abc789|

#### \* : Matches zero or more occurrences

##### Input Code: 13

##### Redshift 19

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE column_name ~ 'a*b';
```

##### Results 25

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|1|abc123 hello world|
|3|123abc another line abc123|
|6|a@b#c! more text here|
|7|alpha beta gamma|
|11|abc123 abc456 abc789|

###### Output Code 10

##### Snowflake 16

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, 'a*b', 1, 'ms') > 0;
```

##### Results 26

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|1|abc123 hello world|
|3|123abc another line abc123|
|6|a@b#c! more text here|
|7|alpha beta gamma|
|11|abc123 abc456 abc789|

#### ? : Matches zero or one occurrence

##### Input Code: 14

##### Redshift 20

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE column_name !~ 'a?b';
```

##### Results 27

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|2|test string with multiple lines in this entry|
|4|line1 line2 line3|
|5|start middle end|
|8|uppercase lowercase|
|9|line1 line2 line3 line4|
|10|1234567890 more digits|
|12|start end middle|
|13|this is the first line this is the second line|
|14|special characters !@#$%^&\*()|

###### Output Code 11

##### Snowflake 17

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, 'a?b', 1, 'ms') = 0;
```

##### Results 28

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|2|test string with multiple lines in this entry|
|4|line1 line2 line3|
|5|start middle end|
|8|uppercase lowercase|
|9|line1 line2 line3 line4|
|10|1234567890 more digits|
|12|start end middle|
|13|this is the first line this is the second line|
|14|special characters !@#$%^&\*()|

#### ^ : Matches the beginning-of-line character

##### Input Code: 15

##### Redshift 21

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE column_name ~ '^abc';
```

##### Results 29

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|1|abc123 hello world|
|3|123abc another line abc123|
|11|abc123 abc456 abc789|

###### Output Code 12

##### Snowflake 18

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, '^abc', 1, 'ms') > 0;
```

##### Results 30

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|1|abc123 hello world|
|3|123abc another line abc123|
|11|abc123 abc456 abc789|

#### $ : Matches the end of the string

##### Input Code: 16

##### Redshift 22

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE column_name !~ '123$';
```

##### Results 31

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|2|test string with multiple lines in this entry|
|4|line1 line2 line3|
|5|start middle end|
|6|a@b#c! more text here|
|7|alpha beta gamma|
|8|uppercase lowercase|
|9|line1 line2 line3 line4|
|10|1234567890 more digits|
|12|start end middle|
|13|this is the first line this is the second line|
|14|special characters !@#$%^&\*()|

###### Output Code 13

##### Snowflake 19

```sql
 SELECT id, column_name
FROM posix_test_table
WHERE REGEXP_COUNT(column_name, '123$', 1, 'ms') = 0;
```

##### Results 32

<!-- prettier-ignore -->
|ID|COLUMN_NAME|
|---|---|
|2|test string with multiple lines in this entry|
|4|line1 line2 line3|
|5|start middle end|
|6|a@b#c! more text here|
|7|alpha beta gamma|
|8|uppercase lowercase|
|9|line1 line2 line3 line4|
|10|1234567890 more digits|
|12|start end middle|
|13|this is the first line this is the second line|
|14|special characters !@#$%^&\*()|

#### Usage of collate columns

Arguments with COLLATE specifications are not currently supported in the RLIKE function. As a
result, the COLLATE clause must be disabled to use this function. However, this may lead to
differences in the results.

##### Input Code: 17

##### Redshift 23

```sql
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE CASE_INSENSITIVE,
col2 VARCHAR(30) COLLATE CASE_SENSITIVE);

INSERT INTO collateTable values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
col1 ~ 'Hello.*' as ci,
col2 ~ 'Hello.*' as cs
FROM collateTable;
```

##### Results 33

<!-- prettier-ignore -->
|CI|CS|
|---|---|
|TRUE|FALSE|

###### Output Code 14

##### Snowflake 20

```sql
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE 'en-ci',
col2 VARCHAR(30) COLLATE 'en-cs'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/16/2025",  "domain": "test" }}';

INSERT INTO collateTable
values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
REGEXP_COUNT(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col1, ''), 'Hello.*', 1, 'ms') > 0 as ci,
REGEXP_COUNT(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col2, ''), 'Hello.*', 1, 'ms') > 0 as cs
FROM
collateTable;
```

##### Results 34

<!-- prettier-ignore -->
|CI|CS|
|---|---|
|FALSE|FALSE|

If you require equivalence for these scenarios, you can manually add the following parameters to the
function to achieve functional equivalence:

<!-- prettier-ignore -->
|Parameter|Description|
|---|---|
|`c`|Case-sensitive matching|
|`i`|Case-insensitive matching|

### Known Issues 9

### Known Issues 10

1. The behavior of fixed char types may differ. Click [here](#id12) for more information.
2. Arguments with COLLATE specifications are not currently supported in the REGEXP_COUNT function.

### Related EWIs 8

- [SSC-FDM-PG0011](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0011):
  The use of the COLLATE column constraint has been disabled for this pattern-matching condition.

## SIMILAR TO

Pattern-matching conditions

### Description 10

> The SIMILAR TO operator matches a string expression, such as a column name, with a SQL standard
> regular expression pattern. A SQL regular expression pattern can include a set of pattern-matching
> metacharacters, including the two supported by the
> [LIKE](https://docs.aws.amazon.com/redshift/latest/dg/r_patternmatching_condition_like.html)
> operator.
> ([Redshift SQL Language reference SIMILAR TO](https://docs.aws.amazon.com/redshift/latest/dg/pattern-matching-conditions-similar-to.html)).

Warning

This grammar is partially supported in
[Snowflake](https://docs.snowflake.com/en/sql-reference/operators-logical). SIMILAR TO is
transformed to [RLIKE](https://docs.snowflake.com/en/sql-reference/functions/rlike) in Snowflake.

### Grammar Syntax 9

```sql
 expression [ NOT ] SIMILAR TO pattern [ ESCAPE 'escape_char' ]
```

### Pattern-matching metacharacters

<!-- prettier-ignore -->
|Redshift|Snowflake|Notes|
|---|---|---|---|---|
|`{code} sql :force: % `|`{code} sql :force: .\* `|Matches any sequence of zero or more characters. To achieve full equivalence in Snowflake, we need to replace the '%' operator with '.\*' in the pattern.|
|`{code} sql :force: \_ `|`{code} sql :force: . `|Matches any single character. To achieve full equivalence in Snowflake, we need to replace the `_` operator with `.` and add the `s` parameter to enable the POSIX wildcard character `.` to match newline characters.|
|```{code} sql :force:|```|```{code} sql :force:|```|Denotes alternation. This case is fully supported in Snowflake.|
|`{code} sql :force: \* `|`{code} sql :force: \* `|Repeat the previous item zero or more times. This can have a different behavior when newline characters are included.|
|`{code} sql :force: + `|`{code} sql :force: + `|Repeat the previous item one or more times. This can have a different behavior when newline characters are included.|
|`{code} sql :force: ? `|`{code} sql :force: ? `|Repeat the previous item zero or one time. This can have a different behavior when newline characters are included.|
|`{code} sql :force: {m} `|`{code} sql :force: {m} `|Repeat the previous item exactly _m_ times and it is fully supported in Snowflake.|
|`{code} sql :force: {m,} `|`{code} sql :force: {m,} `|Repeat the previous item at least _m_ and not more than _n_ times and it is fully supported in Snowflake.|
|`{code} sql :force: {m,n} `|`{code} sql :force: {m,n} `|Repeat the previous item _m_ or more times and it is fully supported in Snowflake.|
|`{code} sql :force: () `|`{code} sql :force: () `|Parentheses group items into a single logical item and it is fully supported in Snowflake.|
|`{code} sql :force: [...] `|`{code} sql :force: [...] `|A bracket expression specifies a character class, just as in POSIX regular expressions.|

### Sample Source Patterns 9

#### **Setup data** 3

##### Redshift 24

```sql
 CREATE TABLE similar_table_ex (
    column_name VARCHAR(255)
);

INSERT INTO similar_table_ex (column_name)
VALUES
    ('abc_123'),
    ('a_cdef'),
    ('bxyz'),
    ('abcc'),
    ('start_hello'),
    ('apple'),
    ('banana'),
    ('xyzabc'),
    ('abc\ncccc'),
    ('\nabccc'),
    ('abc%def'),
    ('abc_xyz'),
    ('abc_1_xyz'),
    ('applepie'),
    ('start%_abc'),
    ('ab%_xyz'),
    ('abcs_123_xyz'),
    ('aabc123'),
    ('xyzxyz'),
    ('123abc\nanother line\nabc123');
```

#### % : Matches any sequence of zero or more characters

##### Input Code: 18

##### Redshift 25

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO '%abc%';
```

##### Results 35

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|abcc|
|xyzabc|
|abc cccc|
|abc%def|
|abc_xyz|
|abc_1_xyz|
|start%\_abc|
|abcs_123_xyz|
|aabc123|

###### Output Code 15

##### Snowflake 21

```sql
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, '.*abc.*', 's');
```

##### Results 36

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|abcc|
|xyzabc|
|abc cccc|
|abc%def|
|abc_xyz|
|abc_1_xyz|
|start%\_abc|
|abcs_123_xyz|
|aabc123|

#### \_ : Matches any single character

##### Input Code: 19

##### Redshift 26

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'a_c%';
```

##### Results 37

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|a_cdef|
|abcc|
|abc cccc|
|abc%def|
|abc_xyz|
|abc_1_xyz|
|abcs_123_xyz|

###### Output Code 16

##### Snowflake 22

```sql
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'a.c.*', 's');
```

##### Results 38

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|a_cdef|
|abcc|
|abc cccc|
|abc%def|
|abc_xyz|
|abc_1_xyz|
|abcs_123_xyz|

#### | : Denotes alternation

##### Input Code: 20

##### Redshift 27

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'a|b%';
```

##### Results 39

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|bxyz|
|banana|

###### Output Code 17

##### Snowflake 23

```sql
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'a|b.*', 's');
```

##### Results 40

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|bxyz|
|banana|

#### {m, n} : Repeat the previous item exactly _m_ times

##### Input Code: 21

##### Redshift 28

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'abc{2,4}';
```

##### Results 41

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abcc|

###### Output Code 18

##### Snowflake 24

```sql
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'abc{2,4}', 's');
```

##### Results 42

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abcc|

#### + : Repeat the previous item one or more times

##### Input Code: 22

##### Redshift 29

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'abc+';
```

##### Results 43

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abcc|
|abc cccc|

###### Output Code 19

##### Snowflake 25

```sql
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'abc+', 's');
```

##### Results 44

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abcc|

#### \* : Repeat the previous item zero or more times

##### Input Code: 23

##### Redshift 30

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'abc*c';
```

##### Results 45

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abcc|
|abc cccc|

###### Output Code 20

##### Snowflake 26

```sql
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, 'abc*c', 's');
```

##### Results 46

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abcc|

#### ? : Repeat the previous item zero or one time

##### Input Code: 24

##### Redshift 31

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO 'abc?c';
```

##### Results 47

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abcc|
|abc ccc|

###### Output Code 21

##### Snowflake 27

```sql
 SELECT column_name
FROM
similar_table_ex
WHERE
RLIKE( column_name, 'abc?c', 's');
```

##### Results 48

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abcc|

#### () : Parentheses group items into a single logical item

##### Input Code: 25

##### Redshift 32

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO '(abc|xyz)%';
```

##### Results 49

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|abcc|
|xyzabc|
|abc cccc|
|abc%def|
|abc_xyz|
|abc_1_xyz|
|abcs_123_xyz|
|xyzxyz|

###### Output Code 22

##### Snowflake 28

```sql
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, '(abc|xyz).*', 's');
```

##### Results 50

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|abcc|
|xyzabc|
|abc cccc|
|abc%def|
|abc_xyz|
|abc_1_xyz|
|abcs_123_xyz|
|xyzxyz|

#### […] : Specifies a character class

##### Input Code: 26

##### Redshift 33

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO '[a-c]%';
```

##### Results 51

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|a_cdef|
|bxyz|
|abcc|
|apple|
|banana|
|abc cccc|
|abc%def|
|abc_xyz|
|abc_1_xyz|
|applepie|
|ab%\_xyz|
|abcs_123_xyz|
|aabc123|

###### Output Code 23

##### Snowflake 29

```sql
 SELECT column_name
FROM similar_table_ex
WHERE RLIKE (column_name, '[a-c].*', 's');
```

##### Results 52

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|a_cdef|
|bxyz|
|abcc|
|apple|
|banana|
|abc cccc|
|abc%def|
|abc_xyz|
|abc_1_xyz|
|applepie|
|ab%\_xyz|
|abcs_123_xyz|
|aabc123|

#### Escape characters 2

The following characters will be escaped if they appear in the pattern and are not the escape
character itself:

- .
- $
- ^

##### Input Code: 27

##### Redshift 34

```sql
 SELECT column_name
FROM similar_table_ex
WHERE column_name SIMILAR TO '%abc^_%' ESCAPE '^';

SELECT '$0.87' SIMILAR TO '$[0-9]+(.[0-9][0-9])?' r1;
```

##### Results 53

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|abc_xyz|
|abc_1_xyz|

<!-- prettier-ignore -->
|R1|
|---|
|TRUE|

###### Output Code 24

##### Snowflake 30

```sql
 SELECT column_name
FROM
similar_table_ex
WHERE
RLIKE( column_name, '.*abc\\_.*', 's');

SELECT
RLIKE( '$0.87', '\\$[0-9]+(\\.[0-9][0-9])?', 's') r1;
```

##### Results 54

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|abc_xyz|
|abc_1_xyz|

<!-- prettier-ignore -->
|R1|
|---|
|TRUE|

#### Pattern stored in a variable

If these patterns are stored in a variable, the required adjustments for equivalence will not be
applied. You can refer to the recommendations outlined in the
[table](#pattern-matching-metacharacters) at the beginning of this document for additional
equivalence guidelines.

##### Input Code: 28

##### Redshift 35

```sql
 WITH pattern AS (
    SELECT '%abc%'::VARCHAR AS search_pattern
)
SELECT column_name
FROM similar_table_ex, pattern
WHERE column_name SIMILAR TO pattern.search_pattern;
```

##### Results 55

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|abc_123|
|abcc|
|xyzabc|
|abc cccc|
|abccc|
|abc%def|
|abc_xyz|
|abc_1_xyz|
|start%\_abc|
|abcs_123_xyz|
|aabc123|
|123abc another line abc123|

###### Output Code 25

##### Snowflake 31

```sql
 WITH pattern AS (
    SELECT '%abc%'::VARCHAR AS search_pattern
)
SELECT column_name
FROM
similar_table_ex,
pattern
WHERE
RLIKE( column_name,
                    --** SSC-FDM-0032 - PARAMETER 'search_pattern' IS NOT A LITERAL VALUE, TRANSFORMATION COULD NOT BE FULLY APPLIED **
                    pattern.search_pattern, 's');
```

##### Results 56

<!-- prettier-ignore -->
|COLUMN_NAME|
|---|
|Query produced no results|

#### Usage of collate columns 2

Arguments with COLLATE specifications are not currently supported in the RLIKE function. As a
result, the COLLATE clause must be disabled to use this function. However, this may lead to
differences in the results.

##### Input Code: 29

##### Redshift 36

```sql
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE CASE_INSENSITIVE,
col2 VARCHAR(30) COLLATE CASE_SENSITIVE);

INSERT INTO collateTable values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
col1 SIMILAR TO 'Hello%' as ci,
col2 SIMILAR TO 'Hello%' as cs
FROM collateTable;
```

##### Results 57

<!-- prettier-ignore -->
|CI|CS|
|---|---|
|TRUE|FALSE|

###### Output Code 26

##### Snowflake 32

```sql
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE 'en-ci',
col2 VARCHAR(30) COLLATE 'en-cs'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/16/2025",  "domain": "test" }}';

INSERT INTO collateTable
values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
RLIKE(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col1, ''), 'Hello.*', 's') as ci,
RLIKE(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col2, ''), 'Hello.*', 's') as cs
FROM
collateTable;
```

##### Results 58

<!-- prettier-ignore -->
|CI|CS|
|---|---|
|FALSE|FALSE|

If you require equivalence for these scenarios, you can manually add the following parameters to the
function to achieve functional equivalence:

<!-- prettier-ignore -->
|Parameter|Description|
|---|---|
|`c`|Case-sensitive matching|
|`i`|Case-insensitive matching|

### Known Issues 11

1. The behavior of fixed char types may differ.
2. The `RLIKE` function uses POSIX extended regular expressions, which may result in different
   behavior in certain cases, especially when line breaks are involved. It appears that when line
   breaks are present in the string and a match occurs on one line, it returns a positive result for
   the entire string, even though the match only occurred on a single line and not across the whole
   string. For example:

#### Redshift code

```sql
 CREATE TABLE table1 (
col1 VARCHAR(20)
);

INSERT INTO table1 values ('abcccc'), ('abc\neab'), ('abc\nccc');

SELECT col1
FROM table1
WHERE col1 SIMILAR TO 'abc*c';
```

##### Snowflake code

```sql
 CREATE TABLE table1 (
col1 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "01/14/2025",  "domain": "test" }}';

INSERT INTO table1
values ('abcccc'), ('abc\neab'), ('abc\nccc');

SELECT col1
FROM
table1
WHERE
RLIKE( col1, 'abc*c', 's');
```

##### Redshift Results 2

<!-- prettier-ignore -->
|COL1|
|---|
|abcccc|
|abc eab|
|abc ccc|

##### Snowflake Results 2

<!-- prettier-ignore -->
|COL1|
|---|
|abcccc|

1. To achieve maximum equivalence, some modifications are made to the pattern operators.
2. If these patterns are stored in a variable, SnowConvert AI does not apply the necessary
   adjustments for equivalence.
3. Arguments with COLLATE specifications are not currently supported in the RLIKE function.

### Related EWIs 9

- [SSC-FDM-0032](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0032):
  Parameter is not a literal value, transformation could not be fully applied.
- [SSC-FDM-PG0011](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0011):
  The use of the COLLATE column constraint has been disabled for this pattern-matching condition.
