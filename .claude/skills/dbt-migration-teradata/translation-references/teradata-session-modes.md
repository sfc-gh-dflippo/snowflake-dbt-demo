---
description:
  "The Teradata database has different modes for running queries: ANSI Mode (rules based on the ANSI
  SQL: 2011 specifications) and TERA mode (rules defined by Teradata). Please review the following
  Terad"
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/session-modes
title: SnowConvert AI - Teradata - Session Modes in Teradata | Snowflake Documentation
---

## Teradata session modes description

The Teradata database has different modes for running queries: ANSI Mode (rules based on the ANSI
SQL: 2011 specifications) and TERA mode (rules defined by Teradata). Please review the following
[Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Request-and-Transaction-Processing/Transaction-Processing/Transaction-Semantics-Differences-in-ANSI-and-Teradata-Session-Modes)
for more information.

### Teradata mode for strings informative table

For strings, the Teradata Mode works differently. As it is explained in the following table based on
the
[Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Request-and-Transaction-Processing/Transaction-Processing/Comparison-of-Transactions-in-ANSI-and-Teradata-Session-Modes):

<!-- prettier-ignore -->
|Feature|ANSI mode|Teradata mode|
|---|---|---|
|Default attribute for character comparisons|CASESPECIFIC|NOT CASESPECIFIC|
|Default TRIM behavior|TRIM(BOTH FROM)|TRIM(BOTH FROM)|

#### Translation specification summary

<!-- prettier-ignore -->
|Mode|Column constraint values|Teradata behavior|SC expected behavior|
|---|---|---|---|
|ANSI Mode|CASESPECIFIC|CASESPECIFIC|No constraint added.|
||NOT CASESPECIFIC|CASESPECIFIC|Add `COLLATE 'en-cs'` in column definition.|
|Teradata Mode|CASESPECIFIC|CASESPECIFIC|In most cases, do not add COLLATE, and convert its usages of string comparison to `RTRIM( expression )`|
||NOT CASESPECIFIC|NOT CASESPECIFIC|In most cases, do not add COLLATE, and convert its usages of string comparison to `RTRIM(UPPER( expression ))`|

### Available translation specification options

- [TERA Mode For Strings Comparison - NO COLLATE](#tera-mode-for-string-comparison-and-no-collate-usages)
- [TERA Mode For Strings Comparison - COLLATE](#tera-mode-for-string-comparison-and-collate-usage)
- [ANSI Mode For Strings Comparison - NO COLLATE](#ansi-mode-for-string-comparison-and-no-colate-usages)
- [ANSI Mode For Strings Comparison - COLLATE](#ansi-mode-for-string-comparison-and-collate-usage)

## ANSI Mode For Strings Comparison - COLLATE

This section defines the translation specification for a string in ANSI mode with the use of
COLLATE.

### Description

#### ANSI mode for string comparison and COLLATE usage

The ANSI mode string comparison will apply the COLLATE constraint to the columns or statements as
required. The default case specification trim behavior may be taken into account.

Notice that in Teradata, the default case specification is ‘`CASESPECIFIC`’, the same default as in
Snowflake ‘`case-sensitive'`. Thus, these cases will not be translated with a `COLLATE` because it
will be redundant.

### Sample Source Patterns

#### Setup data

##### Teradata

```sql
 CREATE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT CASESPECIFIC,
    last_name VARCHAR(50) CASESPECIFIC,
    department VARCHAR(50)
);

INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (1, 'George', 'Snow', 'Sales');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (2, 'John', 'SNOW', 'Engineering');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (5, 'Mary', '   ', 'SaleS  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (6, 'GEORGE', '  ', 'sales  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (7, 'GEORGE   ', '  ', 'salEs  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (9, 'JOHN', '   SnoW', 'IT');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) NOT CASESPECIFIC,
    location VARCHAR(100) CASESPECIFIC,
    PRIMARY KEY (department_id)
);

INSERT INTO departments (department_id, department_name, location) VALUES (101, 'Information Technology', 'New York');
INSERT INTO departments (department_id, department_name, location) VALUES (102, 'Human Resources', 'Chicago');
INSERT INTO departments (department_id, department_name, location) VALUES (103, 'Sales', 'San Francisco');
INSERT INTO departments (department_id, department_name, location) VALUES (104, 'Finance', 'Boston');
```

##### Snowflake

```sql
 CREATE OR REPLACE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (1, 'George', 'Snow', 'Sales');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (2, 'John', 'SNOW', 'Engineering');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (5, 'Mary', '   ', 'SaleS  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (6, 'GEORGE', '  ', 'sales  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (7, 'GEORGE   ', '  ', 'salEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (9, 'JOHN', '   SnoW', 'IT');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE OR REPLACE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50),
    location VARCHAR(100),
       PRIMARY KEY (department_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO departments (department_id, department_name, location)
VALUES (101, 'Information Technology', 'New York');

INSERT INTO departments (department_id, department_name, location)
VALUES (102, 'Human Resources', 'Chicago');

INSERT INTO departments (department_id, department_name, location)
VALUES (103, 'Sales', 'San Francisco');

INSERT INTO departments (department_id, department_name, location)
VALUES (104, 'Finance', 'Boston');
```

#### Comparison operation

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode

##### Teradata 2

##### Query

```sql
 SELECT *
FROM employees
WHERE first_name = 'GEorge ';
```

##### Output

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 2

##### Query 2

```sql
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') = RTRIM('George');
```

##### Output 2

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode

##### Teradata 3

##### Query 3

```sql
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

##### Output 3

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake 3

##### Query 4

```sql
SELECT
 *
FROM
 employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

##### Output 4

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is ANSI Mode

##### Teradata 4

##### Query 5

```sql
 SELECT * FROM employees WHERE first_name = 'George   ' (CASESPECIFIC);
```

##### Output 5

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 4

###### Note

COLLATE ‘en-cs’ is required for functional equivalence.

##### Query 6

```sql
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') = 'George   ' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output 6

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode

##### Teradata 5

##### Query 7

```sql
 SELECT * FROM employees WHERE first_name = 'GEorge   ' (NOT CASESPECIFIC) ;
```

##### Output 7

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|
|7|GEORGE||salEs|

##### Snowflake 5

##### Query 8

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) = RTRIM('GEorge   ' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

##### Output 8

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|
|7|GEORGE||salEs|

##### Case 5: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode

##### Teradata 6

##### Query 9

```sql
 SELECT * FROM employees WHERE first_name (NOT CASESPECIFIC)  = 'George    ';
```

##### Output 9

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 6

###### Note 2

It requires COLLATE.

##### Query 10

```sql
 SELECT
   *
FROM
   employees
WHERE
   COLLATE(first_name /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/, 'en-cs-rtrim') = 'George    ';
```

##### Output 10

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

#### LIKE operation

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 2

##### Teradata 7

##### Query 11

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'George';
```

##### Output 11

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 7

##### Query 12

```sql
 SELECT *
FROM employees
WHERE COLLATE(first_name, 'en-cs-rtrim') LIKE 'George';
```

##### Output 12

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode 2

##### Teradata 8

##### Query 13

```sql
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output 13

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

##### Snowflake 8

##### Query 14

```sql
 SELECT *
FROM employees
WHERE RTRIM(last_name) LIKE RTRIM('Snow');
```

##### Output 14

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is ANSI Mode 2

##### Teradata 9

##### Query 15

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'Mary' (CASESPECIFIC);
```

##### Output 15

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|5|Mary||SaleS|

##### Snowflake 9

##### Query 16

```sql
 SELECT
   *
FROM
   employees
WHERE
   COLLATE(first_name, 'en-cs-rtrim') LIKE 'Mary' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output 16

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|5|Mary||SaleS|

##### Case 4: CAST CASESPECIFC column to NOT CASESPECIFIC and database mode is ANSI Mode

##### Teradata 10

##### Query 17

```sql
 SELECT *
FROM employees
WHERE last_name LIKE 'SNO%' (NOT CASESPECIFIC);
```

##### Output 17

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

##### Snowflake 10

##### Query 18

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) LIKE RTRIM('SNO%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

##### Output 18

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

#### IN Operation

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 3

##### Teradata 11

##### Query 19

```sql
 SELECT *
FROM employees
WHERE first_name IN ('George   ');
```

##### Output 19

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 11

###### Note 3

This case requires `COLLATE(`_`column_name`_`, 'en-cs-rtrim')`

##### Query 20

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) IN (COLLATE('George   ', 'en-cs-rtrim'));
```

##### Output 20

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode 3

##### Teradata 12

###### Note 4

For this case, the column does not have a column constraint, but the default constraint in Teradata
ANSI mode is `CASESPECIFIC`.

##### Query 21

```sql
 SELECT *
FROM employees
WHERE department IN ('EngineerinG    ');
```

##### Output 21

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

##### Snowflake 12

##### Query 22

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(department) IN (RTRIM('EngineerinG    '));
```

##### Output 22

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

#### ORDER BY clause

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 4

##### Teradata 13

##### Query 23

```sql
 SELECT first_name
FROM employees
ORDER BY first_name;
```

##### Output 23

<!-- prettier-ignore -->
|first_name|
|---|
|GeorgE|
|GEORGE|
|GEORGE|
|**George**|
|John|
|JOHN|
|JOHN|
|Marco|
|Mary|
|WIlle|

##### Snowflake 13

Warning

Please review FDM. **_Pending to add._**

##### Query 24

```sql
 SELECT
   first_name
FROM
   employees
ORDER BY first_name;
```

##### Output 24

<!-- prettier-ignore -->
|first_name|
|---|
|GeorgE|
|**George**|
|GEORGE|
|GEORGE|
|John|
|JOHN|
|JOHN|
|Marco|
|Mary|
|WIlle|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode 4

##### Teradata 14

##### Query 25

```sql
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output 25

<!-- prettier-ignore -->
|department|
|---|
|EngineerinG|
|Engineering|
|Finance|
|Human resources|
|IT|
|SalEs|
|SaleS|
|Sales|
|salEs|
|sales|

##### Snowflake 14

##### Query 26

```sql
 SELECT
   last_name
FROM
   employees
ORDER BY last_name;
```

##### Output 26

<!-- prettier-ignore -->
|department|
|---|
|EngineerinG|
|Engineering|
|Finance|
|Human resources|
|IT|
|SalEs|
|SaleS|
|Sales|
|salEs|
|sales|

#### GROUP BY clause

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 5

##### Teradata 15

##### Query 27

```sql
 SELECT first_name
FROM employees
GROUP BY first_name;
```

##### Output 27

<!-- prettier-ignore -->
|first_name|
|---|
|Mary|
|GeorgE|
|WIlle|
|**JOHN**|
|Marco|
|GEORGE|

##### Snowflake 15

Warning

**The case or order may differ in output.**

###### Note 5

`RTRIM` is required in selected columns.

##### Query 28

```sql
   SELECT
   first_name
  FROM
   employees
  GROUP BY first_name;
```

##### Output 28

<!-- prettier-ignore -->
|first_name|
|---|
|**John**|
|Marco|
|**George**|
|GeorgE|
|WIlle|
|Mary|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode 5

##### Teradata 16

##### Query 29

```sql
 SELECT last_name
FROM employees
GROUP BY last_name;
```

##### Output 29

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

##### Snowflake 16

###### Note 6

_The order may differ._

##### Query 30

```sql
 SELECT
   last_name
  FROM
   employees
  GROUP BY last_name;
```

##### Output 30

<!-- prettier-ignore -->
|first_name|
|---|
|Snow|
|SNOW|
|SnoW|
|            |
|SnoW|
|snow|

#### HAVING clause

The HAVING clause will use the patterns in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode

##### Teradata 17

##### Query 31

```sql
 SELECT first_name
FROM employees
GROUP BY first_name
HAVING first_name = 'Mary';
```

##### Output 31

```sql
Mary
```

##### Snowflake 17

##### Query 32

```sql
 SELECT
  first_name
FROM
  employees
GROUP BY first_name
HAVING
   COLLATE(first_name, 'en-cs-rtrim') = 'Mary';
```

##### Output 32

```sql
Mary
```

#### CASE WHEN statement

The `CASE WHEN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata 18

##### Query 33

```sql
 SELECT first_name,
      last_name,
      CASE
          WHEN department = 'EngineerinG' THEN 'Information Technology'
          WHEN first_name = '    GeorgE   ' THEN 'GLOBAL SALES'
          ELSE 'Other'
      END AS department_full_name
FROM employees
WHERE last_name = '';
```

##### Output 33

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||Other|
|Mary||Other|
|GeorgE||GLOBAL SALES|
|GEORGE||Other|

##### Snowflake 18

##### Query 34

```sql
    SELECT
   first_name,
   last_name,
   CASE
         WHEN RTRIM(department) = RTRIM('EngineerinG')
            THEN 'Information Technology'
         WHEN COLLATE(first_name, 'en-cs-rtrim')  = '    GeorgE   '
            THEN 'GLOBAL SALES'
       ELSE 'Other'
   END AS department_full_name
FROM
   employees
WHERE RTRIM(last_name) = RTRIM('');
```

##### Output 34

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|Mary||Other|
|GEORGE||Other|
|GEORGE||Other|
|GeorgE||GLOBAL SALES|

#### JOIN clause

Warning

Simple scenarios with evaluation operations are supported.

The `JOIN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 2

##### Teradata 19

##### Query 35

```sql
 SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM
    employees e
JOIN
    departments d
ON
    e.department = d.department_name;
```

##### Output 35

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|10|JOHN|snow|Finance|

##### Snowflake 19

###### Note 7

`d.department_name` is `NOT CASESPECIFIC`, so it requires `COLLATE`.

##### Query 36

```sql
    SELECT
   e.employee_id,
   e.first_name,
   e.last_name,
   d.department_name
FROM
   employees e
JOIN
   departments d
ON COLLATE(e.department, 'en-cs-rtrim') = d.department_name;
```

##### Output 36

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|10|JOHN|snow|Finance|

#### Related EWIs

[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0007):
GROUP BY IS NOT EQUIVALENT IN TERADATA MODE

[SC-FDM-TD0032](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0032)
: [NOT] CASESPECIFIC CLAUSE WAS REMOVED

## ANSI Mode For Strings Comparison - NO COLLATE

This section defines the translation specification for a string in ANSI mode without the use of
COLLATE.

### Description 2

#### ANSI mode for string comparison and NO COLATE usages

The ANSI mode string comparison without the use of COLLATE will apply RTRIM and UPPER as needed. The
default case specification trim behavior may be taken into account, so if a column does not have a
case specification in Teradata ANSI mode, Teradata will have as default `CASESPECIFIC`.

### Sample Source Patterns 2

#### Setup data 2

##### Teradata 20

```sql
 CREATE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT CASESPECIFIC,
    last_name VARCHAR(50) CASESPECIFIC,
    department VARCHAR(50)
);

INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (1, 'George', 'Snow', 'Sales');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (2, 'John', 'SNOW', 'Engineering');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (5, 'Mary', '   ', 'SaleS  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (6, 'GEORGE', '  ', 'sales  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (7, 'GEORGE   ', '  ', 'salEs  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (9, 'JOHN', '   SnoW', 'IT');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) NOT CASESPECIFIC,
    location VARCHAR(100) CASESPECIFIC,
    PRIMARY KEY (department_id)
);

INSERT INTO departments (department_id, department_name, location) VALUES (101, 'Information Technology', 'New York');
INSERT INTO departments (department_id, department_name, location) VALUES (102, 'Human Resources', 'Chicago');
INSERT INTO departments (department_id, department_name, location) VALUES (103, 'Sales', 'San Francisco');
INSERT INTO departments (department_id, department_name, location) VALUES (104, 'Finance', 'Boston');
```

##### Snowflake 20

```sql
 CREATE OR REPLACE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/30/2024",  "domain": "test" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (1, 'George', 'Snow', 'Sales');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (2, 'John', 'SNOW', 'Engineering');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (5, 'Mary', '   ', 'SaleS  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (6, 'GEORGE', '  ', 'sales  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (7, 'GEORGE   ', '  ', 'salEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (9, 'JOHN', '   SnoW', 'IT');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE OR REPLACE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50),
    location VARCHAR(100),
       PRIMARY KEY (department_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/30/2024",  "domain": "test" }}'
;

INSERT INTO departments (department_id, department_name, location)
VALUES (101, 'Information Technology', 'New York');

INSERT INTO departments (department_id, department_name, location)
VALUES (102, 'Human Resources', 'Chicago');

INSERT INTO departments (department_id, department_name, location)
VALUES (103, 'Sales', 'San Francisco');

INSERT INTO departments (department_id, department_name, location)
VALUES (104, 'Finance', 'Boston');
```

#### Comparison operation 2

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 6

##### Teradata 21

##### Query 37

```sql
 SELECT *
FROM employees
WHERE first_name = 'George      ';
```

##### Output 37

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 21

##### Query 38

```sql
 SELECT
 *
FROM
employees
WHERE
RTRIM(first_name) = RTRIM('George      ');
```

##### Output 38

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode 6

##### Teradata 22

##### Query 39

```sql
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

##### Output 39

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake 22

##### Query 40

```sql
 SELECT
 *
FROM
employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

##### Output 40

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is ANSI Mode 3

Warning

The (`CASESPECIFIC`) overwrite the column constraint in the table definition.

##### Teradata 23

##### Query 41

```sql
 SELECT * FROM employees WHERE first_name = 'GEorge   ' (CASESPECIFIC);
```

##### Output 41

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|6|GEORGE||sales|

##### Snowflake 23

##### Query 42

```sql
 SELECT * FROM workers
WHERE RTRIM(first_name) = RTRIM(UPPER('GEorge   '));
```

##### Output 42

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|6|GEORGE||sales|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode 2

##### Teradata 24

##### Query 43

```sql
 SELECT * FROM employees
WHERE last_name = 'SnoW   ' (NOT CASESPECIFIC) ;
```

##### Output 43

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

##### Snowflake 24

##### Query 44

```sql
 SELECT * FROM employees
WHERE RTRIM(last_name) = RTRIM('SnoW   ');
```

##### Output 44

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

#### LIKE operation 2

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 7

##### Teradata 25

##### Query 45

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'Georg%';
```

##### Output 45

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 25

##### Query 46

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'Georg%';
```

##### Output 46

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode 7

##### Teradata 26

##### Query 47

```sql
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output 47

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 26

##### Query 48

```sql
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output 48

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 3: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode

##### Teradata 27

##### Query 49

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'George' (NOT CASESPECIFIC);
```

##### Output 49

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 27

##### Query 50

```sql
 SELECT
   *
FROM
   employees
WHERE
   first_name ILIKE 'George' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output 50

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode 3

##### Teradata 28

##### Query 51

```sql
 SELECT *
FROM employees
WHERE last_name LIKE 'SNO%' (NOT CASESPECIFIC);
```

##### Output 51

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

##### Snowflake 28

##### Query 52

```sql
 SELECT
   *
FROM
   employees
WHERE
   last_name LIKE 'SNO%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output 52

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

#### IN Operation 2

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 8

##### Teradata 29

##### Query 53

```sql
 SELECT *
FROM employees
WHERE first_name IN ('GEORGE   ');
```

##### Output 53

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|6|GEORGE||sales|
|7|GEORGE||salEs|

##### Snowflake 29

##### Query 54

```sql
 SELECT *
FROM employees
WHERE RTRIM(first_name) IN (RTRIM('GEORGE   '));
```

##### Output 54

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|6|GEORGE||sales|
|7|GEORGE||salEs|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode 8

##### Teradata 30

##### Query 55

```sql
 SELECT *
FROM employees
WHERE department IN ('SaleS');
```

##### Output 55

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|5|Mary||SaleS|

##### Snowflake 30

##### Query 56

```sql
 SELECT *
FROM employees
WHERE RTRIM(department) IN (RTRIM('SaleS'));
```

##### Output 56

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|5|Mary||SaleS|

#### ORDER BY clause 2

##### Note 8

**Notice that this functional equivalence can differ.**

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 9

##### Teradata 31

##### Query 57

```sql
 SELECT department_name
FROM departments
ORDER BY department_name;
```

##### Output 57

<!-- prettier-ignore -->
|department|
|---|
|EngineerinG|
|Engineering|
|Finance|
|Human resources|
|IT|
|SalEs|
|SaleS|
|Sales|
|salEs|
|sales|

##### Snowflake 31

###### Note 9

**Please review FDM. The order differs in the order of insertion of data.**

##### Query 58

```sql
 SELECT
   department_name
FROM
   departments
ORDER BY
   UPPER(department_name);
```

##### Output 58

<!-- prettier-ignore -->
|department|
|---|
|EngineerinG|
|Engineering|
|Finance|
|Human resources|
|IT|
|SalEs|
|SaleS|
|Sales|
|salEs|
|sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode 9

##### Teradata 32

##### Query 59

```sql
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output 59

<!-- prettier-ignore -->
|department|
|---|
|Finance|
|Human Resources|
|Information Technology|
|Sales|

##### Snowflake 32

##### Query 60

```sql
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output 60

<!-- prettier-ignore -->
|department|
|---|
|Finance|
|Human Resources|
|Information Technology|
|Sales|

#### GROUP BY clause 2

Warning

**To ensure a functional equivalence, it is required to use the COLLATE expression.**

Please review the
[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0007)
for more information.

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 10

##### Teradata 33

##### Query 61

```sql
 SELECT first_name
FROM employees
GROUP BY first_name;
```

##### Output 61

<!-- prettier-ignore -->
|first_name|
|---|
|Mary|
|GeorgE|
|WIlle|
|John|
|Marco|
|GEORGE|

##### Snowflake 33

##### Query 62

```sql
 SELECT
   first_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY first_name;
```

##### Output 62

<!-- prettier-ignore -->
|FIRST_NAME|
|---|
|George|
|John|
|WIlle|
|Marco|
|Mary|
|GEORGE|
|GEORGE|
|GeorgE|
|JOHN|
|JOHN|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode 10

##### Teradata 34

##### Query 63

```sql
 SELECT last_name
FROM employees
GROUP BY last_name;
```

##### Output 63

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

##### Snowflake 34

##### Query 64

```sql
 SELECT
   last_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY last_name;
```

##### Output 64

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

#### HAVING clause 2

The HAVING clause will use the patterns in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode 3

##### Teradata 35

##### Query 65

```sql
 SELECT first_name
FROM employees
GROUP BY first_name
HAVING first_name = 'GEORGE';
```

##### Output 65

```sql
GEORGE
```

##### Snowflake 35

##### Query 66

```sql
 SELECT
   first_name
FROM
   employees
GROUP BY first_name
HAVING
   RTRIM(first_name) = RTRIM('GEORGE');
```

##### Output 66

```sql
GEORGE
```

#### CASE WHEN statement 2

The `CASE WHEN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata 36

##### Query 67

```sql
 SELECT first_name,
      last_name,
      CASE
          WHEN department = 'SaleS  ' THEN 'GLOBAL SALES'
          WHEN first_name = 'GEORGE   ' THEN 'Department Full Name'
          ELSE 'Other'
      END AS department_full_name
FROM employees
WHERE last_name = '   ';
```

##### Output 67

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||Department Full Name|
|Mary||GLOBAL SALES|
|GeorgE||Other|
|GEORGE||Department Full Name|

##### Snowflake 36

##### Query 68

```sql
 SELECT
      first_name,
      last_name,
      CASE
            WHEN UPPER(RTRIM(department)) = UPPER(RTRIM('SaleS  '))
                  THEN 'GLOBAL SALES'
            WHEN UPPER(RTRIM(first_name)) = UPPER(RTRIM('GEORGE   '))
                  THEN 'Department Full Name'
          ELSE 'Other'
      END AS department_full_name
FROM
      employees
WHERE
      UPPER(RTRIM( last_name)) = UPPER(RTRIM('   '));
```

##### Output 68

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||Department Full Name|
|Mary||GLOBAL SALES|
|GeorgE||Other|
|GEORGE||Department Full Name|

#### JOIN clause 2

Warning

Simple scenarios are supported.

The `JOIN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is CASESPECIFIC and database mode is ANSI Mode

##### Teradata 37

##### Query 69

```sql
 SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM
    employees e
JOIN
    departments d
ON
    e.department = d.department_name;
```

##### Output 69

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|10|JOHN|snow|Finance|

##### Snowflake 37

##### Query 70

```sql
 SELECT
   e.employee_id,
   e.first_name,
   e.last_name,
   d.department_name
FROM
   employees e
JOIN
      departments d
ON RTRIM(e.department) = RTRIM(d.department_name);
```

##### Output 70

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|10|JOHN|snow|Finance|

### Related EWIs 2

[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0007):
GROUP BY IS NOT EQUIVALENT IN TERADATA MODE

## TERA Mode For Strings Comparison - COLLATE

This section defines the translation specification for string in Tera mode with the use of COLLATE.

### Description 3

#### Tera Mode for string comparison and COLLATE usage

The Tera Mode string comparison will apply the COLLATE constraint to the columns or statements as
required. The default case specification trim behavior may be taken into account. The default case
specification in Teradata for TERA mode is `NOT CASESPECIFIC`. Thus, the columns without case
specification will have `COLLATE('en-ci')` constraints.

### Sample Source Patterns 3

#### Setup data 3

##### Teradata 38

```sql
 CREATE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT CASESPECIFIC,
    last_name VARCHAR(50) CASESPECIFIC,
    department VARCHAR(50)
);

INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (1, 'George', 'Snow', 'Sales');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (2, 'John', 'SNOW', 'Engineering');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (5, 'Mary', '   ', 'SaleS  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (6, 'GEORGE', '  ', 'sales  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (7, 'GEORGE   ', '  ', 'salEs  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (9, 'JOHN', '   SnoW', 'IT');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) NOT CASESPECIFIC,
    location VARCHAR(100) CASESPECIFIC,
    PRIMARY KEY (department_id)
);

INSERT INTO departments (department_id, department_name, location) VALUES (101, 'Information Technology', 'New York');
INSERT INTO departments (department_id, department_name, location) VALUES (102, 'Human Resources', 'Chicago');
INSERT INTO departments (department_id, department_name, location) VALUES (103, 'Sales', 'San Francisco');
INSERT INTO departments (department_id, department_name, location) VALUES (104, 'Finance', 'Boston');
```

##### Snowflake 38

```sql
 CREATE OR REPLACE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) COLLATE 'en-ci',
    last_name VARCHAR(50),
    department VARCHAR(50) COLLATE 'en-ci'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/01/2024",  "domain": "test" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (1, 'George', 'Snow', 'Sales');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (2, 'John', 'SNOW', 'Engineering');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (5, 'Mary', '   ', 'SaleS  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (6, 'GEORGE', '  ', 'sales  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (7, 'GEORGE   ', '  ', 'salEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (9, 'JOHN', '   SnoW', 'IT');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE OR REPLACE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) COLLATE 'en-ci',
    location VARCHAR(100),
       PRIMARY KEY (department_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/01/2024",  "domain": "test" }}'
;

INSERT INTO departments (department_id, department_name, location)
VALUES (101, 'Information Technology', 'New York');

INSERT INTO departments (department_id, department_name, location)
VALUES (102, 'Human Resources', 'Chicago');

INSERT INTO departments (department_id, department_name, location)
VALUES (103, 'Sales', 'San Francisco');

INSERT INTO departments (department_id, department_name, location)
VALUES (104, 'Finance', 'Boston');
```

#### Comparison operation 3

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode

##### Teradata 39

##### Query 71

```sql
 SELECT *
FROM employees
WHERE first_name = 'GEorge ';
```

##### Output 71

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 39

##### Query 72

```sql
 SELECT
 *
FROM
 employees
WHERE
 RTRIM(first_name) = RTRIM('GEorge ');
```

##### Output 72

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode

##### Teradata 40

##### Query 73

```sql
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

##### Output 73

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake 40

##### Query 74

```sql
SELECT
 *
FROM
 employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

##### Output 74

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is TERA Mode

###### Note 10

Notice that the following queries

- `SELECT * FROM employees WHERE first_name = 'JOHN ' (CASESPECIFIC)`
- `SELECT * FROM employees WHERE first_name (CASESPECIFIC) = 'JOHN '`

will return the same values.

##### Teradata 41

##### Query 75

```sql
 SELECT * FROM employees WHERE first_name = 'JOHN   ' (CASESPECIFIC);
```

##### Output 75

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|9|JOHN|SnoW|IT|
|10|JOHN|snow|Finance|

##### Snowflake 41

##### Query 76

```sql
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') = 'JOHN   ' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output 76

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|9|JOHN|SnoW|IT|
|10|JOHN|snow|Finance|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode

###### Note 11

CAST to a column on the left side of the comparison has priority.

For example:

- `SELECT * FROM employees WHERE last_name (NOT CASESPECIFIC) = 'snoW';` \*will return **5 rows.\***
- `SELECT * FROM employees WHERE last_name = 'snoW' (NOT CASESPECIFIC);` _will return **0 rows**
  with this setup data._

##### Teradata 42

##### Query 77

```sql
 SELECT * FROM employees WHERE last_name (NOT CASESPECIFIC)  = 'snoW' ;
```

##### Output 77

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|
|4|Marco|SnoW|EngineerinG|
|10|JOHN|snow|Finance|

##### Snowflake 42

##### Query 78

```sql
 SELECT
   *
FROM
   employees
WHERE
   COLLATE(last_name /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/, 'en-ci-rtrim') = 'snoW' ;
```

##### Output 78

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|
|4|Marco|SnoW|EngineerinG|
|10|JOHN|snow|Finance|

#### LIKE operation 3

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 2

##### Teradata 43

##### Query 79

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'GeorgE';
```

##### Output 79

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 43

##### Query 80

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) LIKE RTRIM('GeorgE');
```

##### Output 80

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode 2

##### Teradata 44

##### Query 81

```sql
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output 81

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 44

##### Query 82

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) LIKE RTRIM('Snow');
```

##### Output 82

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is TERA Mode 2

##### Teradata 45

##### Query 83

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'George' (CASESPECIFIC);
```

##### Output 83

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake 45

##### Query 84

```sql
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') LIKE 'George';
```

##### Output 84

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode 2

##### Teradata 46

##### Query 85

```sql
 SELECT *
FROM employees
WHERE last_name LIKE 'SNO%' (NOT CASESPECIFIC);
```

##### Output 85

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake 46

##### Query 86

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) LIKE RTRIM('SNO%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

##### Output 86

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

#### IN Operation 3

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 3

##### Teradata 47

##### Query 87

```sql
 SELECT *
FROM employees
WHERE first_name IN ('George   ');
```

##### Output 87

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 47

##### Query 88

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) IN (RTRIM('George   '));
```

##### Output 88

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is not defined and database mode is TERA Mode

###### Note 12

In Tera mode, not defined case specification means `NOT CASESPECIFIC`.

##### Teradata 48

##### Query 89

```sql
 SELECT *
FROM employees
WHERE department IN ('Sales    ');
```

##### Output 89

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|5|Mary||SaleS|
|6|GEORGE||sales|
|7|GEORGE||salEs|
|8|GeorgE||SalEs|

##### Snowflake 48

##### Query 90

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(department) IN (RTRIM('Sales    '));
```

##### Output 90

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|5|Mary||SaleS|
|6|GEORGE||sales|
|7|GEORGE||salEs|
|8|GeorgE||SalEs|

##### Case 3: Column constraint is CASESPECIFIC and database mode is TERA Mode

##### Teradata 49

##### Query 91

```sql
 SELECT *
FROM employees
WHERE last_name IN ('SNOW   ');
```

##### Output 91

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake 49

##### Query 92

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) IN (RTRIM('SNOW   '));
```

##### Output 92

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

#### ORDER BY clause 3

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 4

##### Teradata 50

##### Query 93

```sql
 SELECT employee_id, first_name
FROM employees
ORDER BY employee_id, first_name;
```

##### Output 93

<!-- prettier-ignore -->
|employee_id|first_name|
|---|---|
|1|George|
|2|John|
|3|WIlle|
|4|Marco|
|5|Mary|
|6|GEORGE|
|7|GEORGE|
|8|GeorgE|
|9|JOHN|
|10|JOHN|

##### Snowflake 50

##### Query 94

```sql
 SELECT employee_id, first_name
FROM employees
ORDER BY employee_id, first_name;
```

##### Output 94

<!-- prettier-ignore -->
|employee_id|first_name|
|---|---|
|1|George|
|2|John|
|3|WIlle|
|4|Marco|
|5|Mary|
|6|GEORGE|
|7|GEORGE|
|8|GeorgE|
|9|JOHN|
|10|JOHN|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode 3

##### Teradata 51

##### Query 95

```sql
 SELECT employee_id, last_name
FROM employees
ORDER BY employee_id, last_name;
```

##### Output 95

<!-- prettier-ignore -->
|employee_id|last_name|
|---|---|
|1|Snow|
|2|SNOW|
|3|SNOW|
|4|SnoW|
|5||
|6||
|7||
|8||
|9|SnoW|
|10|snow|

##### Snowflake 51

##### Query 96

```sql
 SELECT employee_id, last_name
FROM employees
ORDER BY employee_id, last_name;
```

##### Output 96

<!-- prettier-ignore -->
|employee_id|last_name|
|---|---|
|1|Snow|
|2|SNOW|
|3|SNOW|
|4|SnoW|
|5||
|6||
|7||
|8||
|9|SnoW|
|10|snow|

#### GROUP BY clause 3

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 5

##### Teradata 52

##### Query 97

```sql
 SELECT first_name
FROM employees
GROUP BY first_name;
```

##### Output 97

<!-- prettier-ignore -->
|first_name|
|---|
|Mary|
|GeorgE|
|WIlle|
|**JOHN**|
|Marco|
|**GEORGE**|

##### Snowflake 52

Warning

Case specification in output may vary depending on the number of columns selected.

##### Query 98

```sql
 SELECT
   first_name
FROM
   employees
GROUP BY first_name;
```

##### Output 98

<!-- prettier-ignore -->
|first_name|
|---|
|**John**|
|Marco|
|**George**|
|GeorgE|
|WIlle|
|Mary|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode 4

##### Teradata 53

##### Query 99

```sql
 SELECT last_name
FROM employees
GROUP BY last_name;
```

##### Output 99

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

##### Snowflake 53

##### Query 100

```sql
 SELECT
   last_name
FROM
   employees
GROUP BY last_name;
```

##### Output 100

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

#### HAVING clause 3

The HAVING clause will use the patterns in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode

##### Teradata 54

###### Note 13

Case specification in output may vary depending on the number of columns selected. This is also
related to the `GROUP BY` clause.

##### Query 101

```sql
 SELECT first_name
FROM employees
GROUP BY first_name
HAVING first_name = 'George  ';
```

##### Output 101

<!-- prettier-ignore -->
|employee_id|first_name|
|---|---|
|7|GEORGE|
|1|George|
|6|GEORGE|

##### Snowflake 54

##### Query 102

```sql
 SELECT
  employee_id,
  first_name
FROM
  employees
GROUP BY employee_id, first_name
HAVING
   RTRIM(first_name) = RTRIM('George  ');
```

##### Output 102

<!-- prettier-ignore -->
|employee_id|first_name|
|---|---|
|7|GEORGE|
|1|George|
|6|GEORGE|

#### CASE WHEN statement 3

The `CASE WHEN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata 55

##### Query 103

```sql
 SELECT first_name,
      last_name,
      CASE
          WHEN department = 'Engineering' THEN 'Information Technology'
          WHEN first_name = 'GeorgE' THEN 'GLOBAL SALES'
          ELSE 'Other'
      END AS department_full_name
FROM employees
WHERE last_name = '';
```

##### Output 103

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||GLOBAL SALES|
|Mary||Other|
|GeorgE||Other|
|GEORGE||GLOBAL SALES|

##### Snowflake 55

##### Query 104

```sql
 SELECT
   first_name,
   last_name,
   CASE
      WHEN RTRIM(department) = RTRIM('Engineering')
         THEN 'Information Technology'
      WHEN RTRIM(first_name) = RTRIM('GeorgE')
         THEN 'GLOBAL SALES'
      ELSE 'Other'
   END AS department_full_name
FROM
   employees
WHERE
   RTRIM( last_name) = RTRIM('');
```

##### Output 104

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||GLOBAL SALES|
|Mary||Other|
|GeorgE||Other|
|GEORGE||GLOBAL SALES|

#### JOIN clause 3

Warning

Simple scenarios with evaluation operations are supported.

The `JOIN` statement will use the patterns described in:

- EvaluaComparisonComparisontion operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 2

##### Teradata 56

##### Query 105

```sql
 SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM
    employees e
JOIN
    departments d
ON
    e.department = d.department_name;
```

##### Output 105

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|3|WIlle|SNOW|Human Resources|
|5|Mary||Sales|
|6|GEORGE||Sales|
|7|GEORGE||Sales|
|8|GeorgE||Sales|
|10|JOHN|snow|Finance|

##### Snowflake 56

##### Query 106

```sql
 SELECT
   e.employee_id,
   e.first_name,
   e.last_name,
   d.department_name
FROM
   employees e
JOIN
   departments d
ON RTRIM(e.department) = RTRIM(d.department_name);
```

##### Output 106

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|3|WIlle|SNOW|Human Resources|
|5|Mary||Sales|
|6|GEORGE||Sales|
|7|GEORGE||Sales|
|8|GeorgE||Sales|
|10|JOHN|snow|Finance|

### Related EWIs 3

[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0007):
GROUP BY REQUIRED COLLATE FOR CASE INSENSITIVE COLUMNS

[SC-FDM-TD0032](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0032)
: [NOT] CASESPECIFIC CLAUSE WAS REMOVED

## TERA Mode For Strings Comparison - NO COLLATE

This section defines the translation specification for string in Tera mode without using COLLATE.

### Description 4

#### Tera Mode for string comparison and NO COLLATE usages

The Tera Mode string comparison without the use of COLLATE will apply `RTRIM` and `UPPER` as needed.
The default case specification trim behavior may be taken into account.

### Sample Source Patterns 4

#### Setup data 4

##### Teradata 57

```sql
 CREATE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT CASESPECIFIC,
    last_name VARCHAR(50) CASESPECIFIC,
    department VARCHAR(50)
);

INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (1, 'George', 'Snow', 'Sales');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (2, 'John', 'SNOW', 'Engineering');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (5, 'Mary', '   ', 'SaleS  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (6, 'GEORGE', '  ', 'sales  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (7, 'GEORGE   ', '  ', 'salEs  ');
INSERT INTO employees(employee_id, first_name, last_name, department) VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (9, 'JOHN', '   SnoW', 'IT');
INSERT INTO employees (employee_id, first_name, last_name, department) VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50) NOT CASESPECIFIC,
    location VARCHAR(100) CASESPECIFIC,
    PRIMARY KEY (department_id)
);

INSERT INTO departments (department_id, department_name, location) VALUES (101, 'Information Technology', 'New York');
INSERT INTO departments (department_id, department_name, location) VALUES (102, 'Human Resources', 'Chicago');
INSERT INTO departments (department_id, department_name, location) VALUES (103, 'Sales', 'San Francisco');
INSERT INTO departments (department_id, department_name, location) VALUES (104, 'Finance', 'Boston');
```

##### Snowflake 57

```sql
 CREATE OR REPLACE TABLE employees (
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/30/2024",  "domain": "test" }}'
;

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (1, 'George', 'Snow', 'Sales');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (2, 'John', 'SNOW', 'Engineering');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (3, 'WIlle', 'SNOW', 'Human resources   ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (4, 'Marco', 'SnoW   ', 'EngineerinG');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (5, 'Mary', '   ', 'SaleS  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (6, 'GEORGE', '  ', 'sales  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (7, 'GEORGE   ', '  ', 'salEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (8, '    GeorgE   ', '  ', 'SalEs  ');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (9, 'JOHN', '   SnoW', 'IT');

INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (10, 'JOHN    ', 'snow', 'Finance   ');

CREATE OR REPLACE TABLE departments (
    department_id INTEGER NOT NULL,
    department_name VARCHAR(50),
    location VARCHAR(100),
       PRIMARY KEY (department_id)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/30/2024",  "domain": "test" }}'
;

INSERT INTO departments (department_id, department_name, location)
VALUES (101, 'Information Technology', 'New York');

INSERT INTO departments (department_id, department_name, location)
VALUES (102, 'Human Resources', 'Chicago');

INSERT INTO departments (department_id, department_name, location)
VALUES (103, 'Sales', 'San Francisco');

INSERT INTO departments (department_id, department_name, location)
VALUES (104, 'Finance', 'Boston');
```

#### Comparison operation 4

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 6

This example demonstrates the usage of a column set up as `NOT CASESPECIFIC` as it is a `first_name`
column. Even when asking for the string `'GEorge',` the query execution will retrieve results in
Teradata because the case specification is not considered.

To emulate this scenario in Snowflake, there are implemented two functions:
`RTRIM(UPPER(string_evaluation))`, `UPPER` is required in this scenario because the string does not
review the case specification.

##### Teradata 58

##### Query 107

```sql
 SELECT *
FROM employees
WHERE first_name = 'GEorge ';
```

##### Output 107

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 58

##### Query 108

```sql
 SELECT
 *
FROM
 employees
WHERE
 RTRIM(UPPER(first_name)) = RTRIM(UPPER('GEorge '));
```

##### Output 108

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode 5

For this example, the column constraint is `CASESPECIFIC`, for which the example does not retrieve
rows in Teradata because ‘`Snow`’ is not equal to ‘`SNOW`’.

In Snowflake, the resulting migration points only to the use of the `RTRIM` function since the case
specification is important.

##### Teradata 59

##### Query 109

```sql
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

##### Output 109

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake 59

##### Query 110

```sql
SELECT
 *
FROM
 employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

##### Output 110

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Case 3: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode

##### Teradata 60

Warning

The (`CASESPECIFIC`) overrides the column constraint in the table definition.

##### Query 111

```sql
 SELECT * FROM employees WHERE first_name = 'GEORGE   ' (CASESPECIFIC);
```

##### Output 111

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|6|GEORGE||sales|

##### Snowflake 60

###### Note 14

RTRIM is required on the left side, and RTRIM is required on the right side.

##### Query 112

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) = RTRIM('GEORGE   ' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

##### Output 112

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|6|GEORGE||sales|

##### Case 4: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode

##### Teradata 61

##### Query 113

```sql
 SELECT * FROM employees WHERE first_name = 'GEorge   ' (NOT CASESPECIFIC) ;
```

##### Output 113

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 61

##### Query 114

```sql
 SELECT
   *
FROM
   employees
WHERE
   UPPER(RTRIM(first_name)) = UPPER(RTRIM('GEorge   ' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/));
```

##### Output 114

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 5: Blank spaces case. Column constraint is NOT CASESPECIFIC, database mode is TERA Mode, and using equal operation

##### Teradata 62

##### Query 115

```sql
 SELECT *
FROM employees
WHERE last_name = '   ';
```

##### Output 115

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|5|Mary||SaleS|
|8|GeorgE||SalEs|
|6|GEORGE||sales|

##### Snowflake 62

##### Query 116

```sql
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) = RTRIM('   ');
```

##### Output 116

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|5|Mary||SaleS|
|8|GeorgE||SalEs|
|6|GEORGE||sales|

#### LIKE operation 4

##### Note 15

This operation works differently from another one. Blank spaces must be the same quantity to
retrieve information.

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 7

This example is expected to display one row because the case specification is not relevant.

###### Note 16

In Snowflake, the migration uses the
[ILIKE](https://docs.snowflake.com/en/sql-reference/functions/ilike) operation. This performs a
case-insensitive comparison.

##### Teradata 63

##### Query 117

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'GeorgE';
```

##### Output 117

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 63

##### Query 118

```sql
 SELECT *
FROM employees
WHERE first_name ILIKE 'GeorgE';
```

##### Output 118

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode 6

##### Teradata 64

##### Query 119

```sql
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output 119

<!-- prettier-ignore -->
|first_name|last_name|department|
|---|---|---|
|George|Snow|Sales|
|Jonh|Snow|Engineering|

##### Snowflake 64

##### Query 120

```sql
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output 120

<!-- prettier-ignore -->
|first_name|last_name|department|
|---|---|---|
|George|Snow|Sales|
|Jonh|Snow|Engineering|

##### Case 3: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode 2

##### Teradata 65

##### Query 121

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'George' (NOT CASESPECIFIC);
```

##### Output 121

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 65

##### Query 122

```sql
 SELECT
   *
FROM
   employees
WHERE
   first_name ILIKE 'George' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output 122

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 4: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode

###### Note 17

This case requires the translation to `ILIKE`.

##### Teradata 66

##### Query 123

```sql
 SELECT *
FROM employees
WHERE first_name LIKE 'GE%' (NOT CASESPECIFIC);
```

##### Output 123

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 66

##### Query 124

```sql
 SELECT
   *
FROM
   employees
WHERE
   first_name ILIKE 'GE%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output 124

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

#### IN Operation 4

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 8

##### Teradata 67

##### Query 125

```sql
 SELECT *
FROM employees
WHERE first_name IN ('GeorgE');
```

##### Output 125

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake 67

##### Query 126

```sql
 SELECT *
FROM employees
WHERE RTRIM(UPPER(first_name)) IN (RTRIM(UPPER('GeorgE')));
```

##### Output 126

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode 7

For this example, the usage of the UPPER function is not required since, in the Teradata database,
the case specification is relevant to the results.

##### Teradata 68

##### Query 127

```sql
 SELECT *
FROM employees
WHERE last_name IN ('SnoW');
```

##### Output 127

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

##### Snowflake 68

##### Query 128

```sql
 SELECT *
FROM employees
WHERE RTRIM(last_name) IN (RTRIM('SnoW'));
```

##### Output 128

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

#### ORDER BY clause 4

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 9

Danger

**Notice that this output order can differ.**

##### Teradata 69

##### Query 129

```sql
 SELECT department
FROM employees
ORDER BY department;
```

##### Output 129

<!-- prettier-ignore -->
|department|
|---|
|EngineerinG|
|Engineering|
|Finance|
|Human resources|
|IT|
|sales|
|SalEs|
|Sales|
|SaleS|
|salEs|

##### Snowflake 69

##### Query 130

```sql
 SELECT department
FROM employees
ORDER BY UPPER(department);
```

##### Output 130

<!-- prettier-ignore -->
|department|
|---|
|EngineerinG|
|Engineering|
|Finance|
|Human resources|
|IT|
|sales|
|SalEs|
|Sales|
|SaleS|
|salEs|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode 8

Danger

**Notice that this output can differ in order.**

##### Teradata 70

##### Query 131

```sql
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output 131

<!-- prettier-ignore -->
|last_name|
|---|
|           |
|           |
|           |
|           |
|SnoW|
|SNOW|
|SNOW|
|SnoW|
|Snow|
|snow|

##### Snowflake 70

##### Query 132

```sql
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output 132

<!-- prettier-ignore -->
|last_name|
|---|
|           |
|           |
|           |
|           |
|SnoW|
|SNOW|
|SNOW|
|SnoW|
|Snow|
|snow|

#### GROUP BY clause 4

Warning

**Notice that this output can differ. To ensure a functional equivalence, it is required to use the
COLLATE expression.**

Please review the SSC-EWI-TD0007 for more information.

_The following might be a workaround without `collate`:_

`SELECT RTRIM(UPPER(first_name))`

`FROM employees`

`GROUP BY RTRIM(UPPER(first_name));`

##### About the column behavior

Danger

Please review the insertion of data in Snowflake. Snowflake does allow the insertion of values as
‘`GEORGE`’ and ‘`georges`’ without showing errors because the case specification is not bound
explicitly with the column.

Assume a table and data as follows:

```sql
 CREATE TABLE students (
   first_name VARCHAR(50) NOT CASESPECIFIC
);

INSERT INTO students(first_name) VALUES ('George');
INSERT INTO students(first_name) VALUES ('   George');
```

Notice that this sample does not allow inserting values with upper and lower case letters in the
`NOT CASESPECIFIC` column because it takes it as the same value. Because the column does not
supervise the case specification, the ‘GEORGE’ and ‘george’ values are checked as the same
information.

The following rows are taken as **_duplicated row errors_**:

```sql
 INSERT INTO students(first_name) VALUES ('GEORGE');
INSERT INTO students(first_name) VALUES ('GeorGe');
INSERT INTO students(first_name) VALUES ('George  ');
INSERT INTO students(first_name) VALUES ('GeOrge');
INSERT INTO students(first_name) VALUES ('GEorge');
INSERT INTO students(first_name) VALUES ('George');
```

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 10

##### Teradata 71

##### Query 133

```sql
 SELECT first_name
FROM employees
GROUP BY first_name;
```

##### Output 133

<!-- prettier-ignore -->
|first_name|
|---|
|Mary|
|GeorgE|
|WIlle|
|JOHN|
|Marco|
|GEORGE|

##### Snowflake 71

##### Query 134

```sql
 SELECT
   first_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY first_name;
```

##### Output 134

<!-- prettier-ignore -->
|first_name|
|---|
|George|
|John|
|WIlle|
|Marco|
|Mary|
|GEORGE|
|GEORGE|
|GeorgE|
|JOHN|
|JOHN|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode 9

##### Teradata 72

##### Query 135

```sql
 SELECT last_name
FROM employees
GROUP BY last_name;
```

##### Output 135

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

##### Snowflake 72

##### Query 136

```sql
 SELECT
   last_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY last_name;
```

##### Output 136

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|SNOW|
|SnoW|
|           |
|           |
|Snow|
|snow|

#### HAVING clause 4

The HAVING clause will use the patterns in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is CASESPECIFIC and database mode is TERA Mode

##### Teradata 73

##### Query 137

```sql
 SELECT last_name
FROM employees
GROUP BY last_name
HAVING last_name = 'Snow';
```

##### Output 137

<!-- prettier-ignore -->
|last_name|
|---|
|Snow|

##### Snowflake 73

##### Query 138

```sql
 SELECT last_name
FROM employees
GROUP BY last_name
HAVING RTRIM(last_name) = RTRIM('Snow');
```

##### Output 138

<!-- prettier-ignore -->
|last_name|
|---|
|Snow|

#### CASE WHEN statement 4

The `CASE WHEN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata 74

##### Query 139

```sql
 SELECT first_name,
      last_name,
      CASE
          WHEN department = 'EngineerinG' THEN 'Information Technology'
          WHEN last_name = 'SNOW' THEN 'GLOBAL COOL SALES'
          ELSE 'Other'
      END AS department_full_name
FROM employees;
```

##### Output 139

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||Other|
|JOHN|SnoW|Other|
|Mary||Other|
|JOHN|snow|Other|
|WIlle|SNOW|GLOBAL COOL SALES|
|George|Snow|Other|
|GeorgE||Other|
|GEORGE||Other|
|Marco|SnoW|Information Technology|
|John|SNOW|Information Technology|

##### Snowflake 74

##### Query 140

```sql
 SELECT
   first_name,
   last_name,
   CASE
      WHEN UPPER(RTRIM(department)) = UPPER(RTRIM('EngineerinG'))
         THEN 'Information Technology'
      WHEN RTRIM(last_name) = RTRIM('SNOW')
         THEN 'GLOBAL COOL SALES'
      ELSE 'Other'
   END AS department_full_name
FROM
   employees;
```

##### Output 140

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||Other|
|JOHN|SnoW|Other|
|Mary||Other|
|JOHN|snow|Other|
|WIlle|SNOW|GLOBAL COOL SALES|
|George|Snow|Other|
|GeorgE||Other|
|GEORGE||Other|
|Marco|SnoW|Information Technology|
|John|SNOW|Information Technology|

#### JOIN clause 4

Warning

Simple scenarios are supported.

The `JOIN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode 3

##### Teradata 75

##### Query 141

```sql
 SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name
FROM
    employees e
JOIN
    departments d
ON
    e.department = d.department_name;
```

##### Output 141

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|3|WIlle|SNOW|Human Resources|
|5|Mary||Sales|
|6|GEORGE||Sales|
|7|GEORGE||Sales|
|8|GeorgE||Sales|
|10|JOHN|snow|Finance|

##### Snowflake 75

##### Query 142

```sql
 SELECT
   e.employee_id,
   e.first_name,
   e.last_name,
   d.department_name
FROM
   employees e
JOIN
   departments d
ON UPPER(RTRIM(e.department)) = UPPER(RTRIM(d.department_name));
```

##### Output 142

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|3|WIlle|SNOW|Human Resources|
|5|Mary||Sales|
|6|GEORGE||Sales|
|7|GEORGE||Sales|
|8|GeorgE||Sales|
|10|JOHN|snow|Finance|

### Known Issues

1. there are some mode-specific SQL statement restrictions: `BEGIN TRANSACTION`, `END TRANSACTION`,
   `COMMIT [WORK]`.
2. Data insertion may differ in Snowflake since the case specification is not bound to the column
   declaration.
3. `GROUP BY` may differ in order, but group the correct values.
4. `ORDER BY` behaves differently in Snowflake.
5. If a function has a TRIM() from the source code, this workaround will add the required functions
   to the source code. So, RTRIM will be applied to the TRIM() source function.

### Related EWIs 4

[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0007):
GROUP BY IS NOT EQUIVALENT IN TERADATA MODE
