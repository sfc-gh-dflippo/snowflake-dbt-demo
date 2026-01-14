---
description:
  "The Teradata database has different modes for running queries: ANSI Mode (rules based on the ANSI
  SQL: 2011 specifications) and TERA mode (rules defined by Teradata). Please review the following
  Terad"
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/session-modes
title: SnowConvert AI - Teradata - Session Modes in Teradata | Snowflake Documentation
---

## Teradata session modes description[¶](#teradata-session-modes-description)

The Teradata database has different modes for running queries: ANSI Mode (rules based on the ANSI
SQL: 2011 specifications) and TERA mode (rules defined by Teradata). Please review the following
[Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Request-and-Transaction-Processing/Transaction-Processing/Transaction-Semantics-Differences-in-ANSI-and-Teradata-Session-Modes)
for more information.

### Teradata mode for strings informative table[¶](#teradata-mode-for-strings-informative-table)

For strings, the Teradata Mode works differently. As it is explained in the following table based on
the
[Teradata documentation](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Request-and-Transaction-Processing/Transaction-Processing/Comparison-of-Transactions-in-ANSI-and-Teradata-Session-Modes):

<!-- prettier-ignore -->
|Feature|ANSI mode|Teradata mode|
|---|---|---|
|Default attribute for character comparisons|CASESPECIFIC|NOT CASESPECIFIC|
|Default TRIM behavior|TRIM(BOTH FROM)|TRIM(BOTH FROM)|

#### Translation specification summary[¶](#translation-specification-summary)

<!-- prettier-ignore -->
|Mode|Column constraint values|Teradata behavior|SC expected behavior|
|---|---|---|---|
|ANSI Mode|CASESPECIFIC|CASESPECIFIC|No constraint added.|
||NOT CASESPECIFIC|CASESPECIFIC|Add `COLLATE 'en-cs'` in column definition.|
|Teradata Mode|CASESPECIFIC|CASESPECIFIC|In most cases, do not add COLLATE, and convert its usages of string comparison to `RTRIM( expression )`|
||NOT CASESPECIFIC|NOT CASESPECIFIC|In most cases, do not add COLLATE, and convert its usages of string comparison to `RTRIM(UPPER( expression ))`|

### Available translation specification options[¶](#available-translation-specification-options)

- [TERA Mode For Strings Comparison - NO COLLATE](#tera-mode-for-string-comparison-and-no-collate-usages)
- [TERA Mode For Strings Comparison - COLLATE](#tera-mode-for-string-comparison-and-collate-usage)
- [ANSI Mode For Strings Comparison - NO COLLATE](#ansi-mode-for-string-comparison-and-no-colate-usages)
- [ANSI Mode For Strings Comparison - COLLATE](#ansi-mode-for-string-comparison-and-collate-usage)

## ANSI Mode For Strings Comparison - COLLATE[¶](#ansi-mode-for-strings-comparison-collate)

This section defines the translation specification for a string in ANSI mode with the use of
COLLATE.

### Description [¶](#description)

#### ANSI mode for string comparison and COLLATE usage[¶](#ansi-mode-for-string-comparison-and-collate-usage)

The ANSI mode string comparison will apply the COLLATE constraint to the columns or statements as
required. The default case specification trim behavior may be taken into account.

Notice that in Teradata, the default case specification is ‘`CASESPECIFIC`’, the same default as in
Snowflake ‘`case-sensitive'`. Thus, these cases will not be translated with a `COLLATE` because it
will be redundant.

### Sample Source Patterns [¶](#sample-source-patterns)

#### Setup data[¶](#setup-data)

##### Teradata[¶](#teradata)

```
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

##### Snowflake[¶](#snowflake)

```
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

#### Comparison operation[¶](#comparison-operation)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-1-column-constraint-is-not-casespecific-and-database-mode-is-ansi-mode)

##### Teradata[¶](#id1)

##### Query[¶](#query)

```
 SELECT *
FROM employees
WHERE first_name = 'GEorge ';
```

##### Output[¶](#output)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id2)

##### Query[¶](#id3)

```
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') = RTRIM('George');
```

##### Output[¶](#id4)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#case-2-column-constraint-is-casespecific-and-database-mode-is-ansi-mode)

##### Teradata[¶](#id5)

##### Query[¶](#id6)

```
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

##### Output[¶](#id7)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake[¶](#id8)

##### Query[¶](#id9)

```
SELECT
 *
FROM
 employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

##### Output[¶](#id10)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is ANSI Mode[¶](#case-3-cast-not-casespecific-column-to-casespecific-and-database-mode-is-ansi-mode)

##### Teradata[¶](#id11)

##### Query[¶](#id12)

```
 SELECT * FROM employees WHERE first_name = 'George   ' (CASESPECIFIC);
```

##### Output[¶](#id13)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id14)

**Note:**

COLLATE ‘en-cs’ is required for functional equivalence.

##### Query[¶](#id15)

```
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') = 'George   ' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output[¶](#id16)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-4-cast-casespecific-column-to-not-casespecific-and-database-mode-is-ansi-mode)

##### Teradata[¶](#id17)

##### Query[¶](#id18)

```
 SELECT * FROM employees WHERE first_name = 'GEorge   ' (NOT CASESPECIFIC) ;
```

##### Output[¶](#id19)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|
|7|GEORGE||salEs|

##### Snowflake[¶](#id20)

##### Query[¶](#id21)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) = RTRIM('GEorge   ' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

##### Output[¶](#id22)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|
|7|GEORGE||salEs|

##### Case 5: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-5-cast-not-casespecific-column-to-not-casespecific-and-database-mode-is-ansi-mode)

##### Teradata[¶](#id23)

##### Query[¶](#id24)

```
 SELECT * FROM employees WHERE first_name (NOT CASESPECIFIC)  = 'George    ';
```

##### Output[¶](#id25)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id26)

**Note:**

It requires COLLATE.

##### Query[¶](#id27)

```
 SELECT
   *
FROM
   employees
WHERE
   COLLATE(first_name /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/, 'en-cs-rtrim') = 'George    ';
```

##### Output[¶](#id28)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

#### LIKE operation[¶](#like-operation)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id29)

##### Teradata[¶](#id30)

##### Query[¶](#id31)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'George';
```

##### Output[¶](#id32)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id33)

##### Query[¶](#id34)

```
 SELECT *
FROM employees
WHERE COLLATE(first_name, 'en-cs-rtrim') LIKE 'George';
```

##### Output[¶](#id35)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id36)

##### Teradata[¶](#id37)

##### Query[¶](#id38)

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output[¶](#id39)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

##### Snowflake[¶](#id40)

##### Query[¶](#id41)

```
 SELECT *
FROM employees
WHERE RTRIM(last_name) LIKE RTRIM('Snow');
```

##### Output[¶](#id42)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is ANSI Mode[¶](#id43)

##### Teradata[¶](#id44)

##### Query[¶](#id45)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'Mary' (CASESPECIFIC);
```

##### Output[¶](#id46)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|5|Mary||SaleS|

##### Snowflake[¶](#id47)

##### Query[¶](#id48)

```
 SELECT
   *
FROM
   employees
WHERE
   COLLATE(first_name, 'en-cs-rtrim') LIKE 'Mary' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output[¶](#id49)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|5|Mary||SaleS|

##### Case 4: CAST CASESPECIFC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-4-cast-casespecifc-column-to-not-casespecific-and-database-mode-is-ansi-mode)

##### Teradata[¶](#id50)

##### Query[¶](#id51)

```
 SELECT *
FROM employees
WHERE last_name LIKE 'SNO%' (NOT CASESPECIFIC);
```

##### Output[¶](#id52)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

##### Snowflake[¶](#id53)

##### Query[¶](#id54)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) LIKE RTRIM('SNO%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

##### Output[¶](#id55)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

#### IN Operation[¶](#in-operation)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id56)

##### Teradata[¶](#id57)

##### Query[¶](#id58)

```
 SELECT *
FROM employees
WHERE first_name IN ('George   ');
```

##### Output[¶](#id59)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id60)

**Note:**

This case requires `COLLATE(`_`column_name`_`, 'en-cs-rtrim')`

##### Query[¶](#id61)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) IN (COLLATE('George   ', 'en-cs-rtrim'));
```

##### Output[¶](#id62)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id63)

##### Teradata[¶](#id64)

**Note:**

For this case, the column does not have a column constraint, but the default constraint in Teradata
ANSI mode is `CASESPECIFIC`.

##### Query[¶](#id65)

```
 SELECT *
FROM employees
WHERE department IN ('EngineerinG    ');
```

##### Output[¶](#id66)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

##### Snowflake[¶](#id67)

##### Query[¶](#id68)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(department) IN (RTRIM('EngineerinG    '));
```

##### Output[¶](#id69)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

#### ORDER BY clause[¶](#order-by-clause)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id70)

##### Teradata[¶](#id71)

##### Query[¶](#id72)

```
 SELECT first_name
FROM employees
ORDER BY first_name;
```

##### Output[¶](#id73)

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

##### Snowflake[¶](#id74)

Warning

Please review FDM. **_Pending to add._**

##### Query[¶](#id75)

```
 SELECT
   first_name
FROM
   employees
ORDER BY first_name;
```

##### Output[¶](#id76)

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

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id77)

##### Teradata[¶](#id78)

##### Query[¶](#id79)

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output[¶](#id80)

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

##### Snowflake[¶](#id81)

##### Query[¶](#id82)

```
 SELECT
   last_name
FROM
   employees
ORDER BY last_name;
```

##### Output[¶](#id83)

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

#### GROUP BY clause[¶](#group-by-clause)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id84)

##### Teradata[¶](#id85)

##### Query[¶](#id86)

```
 SELECT first_name
FROM employees
GROUP BY first_name;
```

##### Output[¶](#id87)

<!-- prettier-ignore -->
|first_name|
|---|
|Mary|
|GeorgE|
|WIlle|
|**JOHN**|
|Marco|
|GEORGE|

##### Snowflake[¶](#id88)

Warning

**The case or order may differ in output.**

**Note:**

`RTRIM` is required in selected columns.

##### Query[¶](#id89)

```
   SELECT
   first_name
  FROM
   employees
  GROUP BY first_name;
```

##### Output[¶](#id90)

<!-- prettier-ignore -->
|first_name|
|---|
|**John**|
|Marco|
|**George**|
|GeorgE|
|WIlle|
|Mary|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id91)

##### Teradata[¶](#id92)

##### Query[¶](#id93)

```
 SELECT last_name
FROM employees
GROUP BY last_name;
```

##### Output[¶](#id94)

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

##### Snowflake[¶](#id95)

**Note:**

_The order may differ._

##### Query[¶](#id96)

```
 SELECT
   last_name
  FROM
   employees
  GROUP BY last_name;
```

##### Output[¶](#id97)

<!-- prettier-ignore -->
|first_name|
|---|
|Snow|
|SNOW|
|SnoW|
|            |
|SnoW|
|snow|

#### HAVING clause[¶](#having-clause)

The HAVING clause will use the patterns in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#sample-column-constraint-is-not-casespecific-and-database-mode-is-ansi-mode)

##### Teradata[¶](#id98)

##### Query[¶](#id99)

```
 SELECT first_name
FROM employees
GROUP BY first_name
HAVING first_name = 'Mary';
```

##### Output[¶](#id100)

```
Mary
```

##### Snowflake[¶](#id101)

##### Query[¶](#id102)

```
 SELECT
  first_name
FROM
  employees
GROUP BY first_name
HAVING
   COLLATE(first_name, 'en-cs-rtrim') = 'Mary';
```

##### Output[¶](#id103)

```
Mary
```

#### CASE WHEN statement[¶](#case-when-statement)

The `CASE WHEN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata[¶](#id104)

##### Query[¶](#id105)

```
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

##### Output[¶](#id106)

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||Other|
|Mary||Other|
|GeorgE||GLOBAL SALES|
|GEORGE||Other|

##### Snowflake[¶](#id107)

##### Query[¶](#id108)

```
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

##### Output[¶](#id109)

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|Mary||Other|
|GEORGE||Other|
|GEORGE||Other|
|GeorgE||GLOBAL SALES|

#### JOIN clause[¶](#join-clause)

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

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id110)

##### Teradata[¶](#id111)

##### Query[¶](#id112)

```
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

##### Output[¶](#id113)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|10|JOHN|snow|Finance|

##### Snowflake[¶](#id114)

**Note:**

`d.department_name` is `NOT CASESPECIFIC`, so it requires `COLLATE`.

##### Query[¶](#id115)

```
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

##### Output[¶](#id116)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|10|JOHN|snow|Finance|

#### Related EWIs[¶](#related-ewis)

[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0007):
GROUP BY IS NOT EQUIVALENT IN TERADATA MODE

[SC-FDM-TD0032](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0032)
: [NOT] CASESPECIFIC CLAUSE WAS REMOVED

## ANSI Mode For Strings Comparison - NO COLLATE[¶](#ansi-mode-for-strings-comparison-no-collate)

This section defines the translation specification for a string in ANSI mode without the use of
COLLATE.

### Description [¶](#id117)

#### ANSI mode for string comparison and NO COLATE usages.[¶](#ansi-mode-for-string-comparison-and-no-colate-usages)

The ANSI mode string comparison without the use of COLLATE will apply RTRIM and UPPER as needed. The
default case specification trim behavior may be taken into account, so if a column does not have a
case specification in Teradata ANSI mode, Teradata will have as default `CASESPECIFIC`.

### Sample Source Patterns [¶](#id118)

#### Setup data[¶](#id119)

##### Teradata[¶](#id120)

```
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

##### Snowflake[¶](#id121)

```
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

#### Comparison operation[¶](#id122)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id123)

##### Teradata[¶](#id124)

##### Query[¶](#id125)

```
 SELECT *
FROM employees
WHERE first_name = 'George      ';
```

##### Output[¶](#id126)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id127)

##### Query[¶](#id128)

```
 SELECT
 *
FROM
employees
WHERE
RTRIM(first_name) = RTRIM('George      ');
```

##### Output[¶](#id129)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id130)

##### Teradata[¶](#id131)

##### Query[¶](#id132)

```
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

##### Output[¶](#id133)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake[¶](#id134)

##### Query[¶](#id135)

```
 SELECT
 *
FROM
employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

##### Output[¶](#id136)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is ANSI Mode[¶](#id137)

Warning

The (`CASESPECIFIC`) overwrite the column constraint in the table definition.

##### Teradata[¶](#id138)

##### Query[¶](#id139)

```
 SELECT * FROM employees WHERE first_name = 'GEorge   ' (CASESPECIFIC);
```

##### Output[¶](#id140)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|6|GEORGE||sales|

##### Snowflake[¶](#id141)

##### Query[¶](#id142)

```
 SELECT * FROM workers
WHERE RTRIM(first_name) = RTRIM(UPPER('GEorge   '));
```

##### Output[¶](#id143)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|6|GEORGE||sales|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id144)

##### Teradata[¶](#id145)

##### Query[¶](#id146)

```
 SELECT * FROM employees
WHERE last_name = 'SnoW   ' (NOT CASESPECIFIC) ;
```

##### Output[¶](#id147)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

##### Snowflake[¶](#id148)

##### Query[¶](#id149)

```
 SELECT * FROM employees
WHERE RTRIM(last_name) = RTRIM('SnoW   ');
```

##### Output[¶](#id150)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

#### LIKE operation[¶](#id151)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id152)

##### Teradata[¶](#id153)

##### Query[¶](#id154)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'Georg%';
```

##### Output[¶](#id155)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id156)

##### Query[¶](#id157)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'Georg%';
```

##### Output[¶](#id158)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id159)

##### Teradata[¶](#id160)

##### Query[¶](#id161)

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output[¶](#id162)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id163)

##### Query[¶](#id164)

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output[¶](#id165)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 3: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-3-cast-not-casespecific-column-to-not-casespecific-and-database-mode-is-ansi-mode)

##### Teradata[¶](#id166)

##### Query[¶](#id167)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'George' (NOT CASESPECIFIC);
```

##### Output[¶](#id168)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id169)

##### Query[¶](#id170)

```
 SELECT
   *
FROM
   employees
WHERE
   first_name ILIKE 'George' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output[¶](#id171)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id172)

##### Teradata[¶](#id173)

##### Query[¶](#id174)

```
 SELECT *
FROM employees
WHERE last_name LIKE 'SNO%' (NOT CASESPECIFIC);
```

##### Output[¶](#id175)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

##### Snowflake[¶](#id176)

##### Query[¶](#id177)

```
 SELECT
   *
FROM
   employees
WHERE
   last_name LIKE 'SNO%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output[¶](#id178)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|

#### IN Operation[¶](#id179)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id180)

##### Teradata[¶](#id181)

##### Query[¶](#id182)

```
 SELECT *
FROM employees
WHERE first_name IN ('GEORGE   ');
```

##### Output[¶](#id183)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|6|GEORGE||sales|
|7|GEORGE||salEs|

##### Snowflake[¶](#id184)

##### Query[¶](#id185)

```
 SELECT *
FROM employees
WHERE RTRIM(first_name) IN (RTRIM('GEORGE   '));
```

##### Output[¶](#id186)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|6|GEORGE||sales|
|7|GEORGE||salEs|

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id187)

##### Teradata[¶](#id188)

##### Query[¶](#id189)

```
 SELECT *
FROM employees
WHERE department IN ('SaleS');
```

##### Output[¶](#id190)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|5|Mary||SaleS|

##### Snowflake[¶](#id191)

##### Query[¶](#id192)

```
 SELECT *
FROM employees
WHERE RTRIM(department) IN (RTRIM('SaleS'));
```

##### Output[¶](#id193)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|5|Mary||SaleS|

#### ORDER BY clause[¶](#id194)

**Note:**

**Notice that this functional equivalence can differ.**

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id195)

##### Teradata[¶](#id196)

##### Query[¶](#id197)

```
 SELECT department_name
FROM departments
ORDER BY department_name;
```

##### Output[¶](#id198)

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

##### Snowflake[¶](#id199)

**Note:**

**Please review FDM. The order differs in the order of insertion of data.**

##### Query[¶](#id200)

```
 SELECT
   department_name
FROM
   departments
ORDER BY
   UPPER(department_name);
```

##### Output[¶](#id201)

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

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id202)

##### Teradata[¶](#id203)

##### Query[¶](#id204)

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output[¶](#id205)

<!-- prettier-ignore -->
|department|
|---|
|Finance|
|Human Resources|
|Information Technology|
|Sales|

##### Snowflake[¶](#id206)

##### Query[¶](#id207)

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output[¶](#id208)

<!-- prettier-ignore -->
|department|
|---|
|Finance|
|Human Resources|
|Information Technology|
|Sales|

#### GROUP BY clause[¶](#id209)

Warning

**To ensure a functional equivalence, it is required to use the COLLATE expression.**

Please review the
[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0007)
for more information.

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id210)

##### Teradata[¶](#id211)

##### Query[¶](#id212)

```
 SELECT first_name
FROM employees
GROUP BY first_name;
```

##### Output[¶](#id213)

<!-- prettier-ignore -->
|first_name|
|---|
|Mary|
|GeorgE|
|WIlle|
|John|
|Marco|
|GEORGE|

##### Snowflake[¶](#id214)

##### Query[¶](#id215)

```
 SELECT
   first_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY first_name;
```

##### Output[¶](#id216)

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

##### Case 2: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#id217)

##### Teradata[¶](#id218)

##### Query[¶](#id219)

```
 SELECT last_name
FROM employees
GROUP BY last_name;
```

##### Output[¶](#id220)

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

##### Snowflake[¶](#id221)

##### Query[¶](#id222)

```
 SELECT
   last_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY last_name;
```

##### Output[¶](#id223)

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

#### HAVING clause[¶](#id224)

The HAVING clause will use the patterns in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is ANSI Mode[¶](#id225)

##### Teradata[¶](#id226)

##### Query[¶](#id227)

```
 SELECT first_name
FROM employees
GROUP BY first_name
HAVING first_name = 'GEORGE';
```

##### Output[¶](#id228)

```
GEORGE
```

##### Snowflake[¶](#id229)

##### Query[¶](#id230)

```
 SELECT
   first_name
FROM
   employees
GROUP BY first_name
HAVING
   RTRIM(first_name) = RTRIM('GEORGE');
```

##### Output[¶](#id231)

```
GEORGE
```

#### CASE WHEN statement[¶](#id232)

The `CASE WHEN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata[¶](#id233)

##### Query[¶](#id234)

```
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

##### Output[¶](#id235)

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||Department Full Name|
|Mary||GLOBAL SALES|
|GeorgE||Other|
|GEORGE||Department Full Name|

##### Snowflake[¶](#id236)

##### Query[¶](#id237)

```
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

##### Output[¶](#id238)

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||Department Full Name|
|Mary||GLOBAL SALES|
|GeorgE||Other|
|GEORGE||Department Full Name|

#### JOIN clause[¶](#id239)

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

##### Sample: Column constraint is CASESPECIFIC and database mode is ANSI Mode[¶](#sample-column-constraint-is-casespecific-and-database-mode-is-ansi-mode)

##### Teradata[¶](#id240)

##### Query[¶](#id241)

```
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

##### Output[¶](#id242)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|10|JOHN|snow|Finance|

##### Snowflake[¶](#id243)

##### Query[¶](#id244)

```
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

##### Output[¶](#id245)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department_name|
|---|---|---|---|
|1|George|Snow|Sales|
|10|JOHN|snow|Finance|

### Related EWIs[¶](#id246)

[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0007):
GROUP BY IS NOT EQUIVALENT IN TERADATA MODE

## TERA Mode For Strings Comparison - COLLATE[¶](#tera-mode-for-strings-comparison-collate)

This section defines the translation specification for string in Tera mode with the use of COLLATE.

### Description [¶](#id247)

#### Tera Mode for string comparison and COLLATE usage[¶](#tera-mode-for-string-comparison-and-collate-usage)

The Tera Mode string comparison will apply the COLLATE constraint to the columns or statements as
required. The default case specification trim behavior may be taken into account. The default case
specification in Teradata for TERA mode is `NOT CASESPECIFIC`. Thus, the columns without case
specification will have `COLLATE('en-ci')` constraints.

### Sample Source Patterns [¶](#id248)

#### Setup data[¶](#id249)

##### Teradata[¶](#id250)

```
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

##### Snowflake[¶](#id251)

```
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

#### Comparison operation[¶](#id252)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#case-1-column-constraint-is-not-casespecific-and-database-mode-is-tera-mode)

##### Teradata[¶](#id253)

##### Query[¶](#id254)

```
 SELECT *
FROM employees
WHERE first_name = 'GEorge ';
```

##### Output[¶](#id255)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id256)

##### Query[¶](#id257)

```
 SELECT
 *
FROM
 employees
WHERE
 RTRIM(first_name) = RTRIM('GEorge ');
```

##### Output[¶](#id258)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#case-2-column-constraint-is-casespecific-and-database-mode-is-tera-mode)

##### Teradata[¶](#id259)

##### Query[¶](#id260)

```
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

##### Output[¶](#id261)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake[¶](#id262)

##### Query[¶](#id263)

```
SELECT
 *
FROM
 employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

##### Output[¶](#id264)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is TERA Mode[¶](#case-3-cast-not-casespecific-column-to-casespecific-and-database-mode-is-tera-mode)

**Note:**

Notice that the following queries

- `SELECT * FROM employees WHERE first_name = 'JOHN ' (CASESPECIFIC)`
- `SELECT * FROM employees WHERE first_name (CASESPECIFIC) = 'JOHN '`

will return the same values.

##### Teradata[¶](#id265)

##### Query[¶](#id266)

```
 SELECT * FROM employees WHERE first_name = 'JOHN   ' (CASESPECIFIC);
```

##### Output[¶](#id267)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|9|JOHN|SnoW|IT|
|10|JOHN|snow|Finance|

##### Snowflake[¶](#id268)

##### Query[¶](#id269)

```
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') = 'JOHN   ' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output[¶](#id270)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|9|JOHN|SnoW|IT|
|10|JOHN|snow|Finance|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#case-4-cast-casespecific-column-to-not-casespecific-and-database-mode-is-tera-mode)

**Note:**

CAST to a column on the left side of the comparison has priority.

For example:

- `SELECT * FROM employees WHERE last_name (NOT CASESPECIFIC) = 'snoW';` \*will return **5 rows.\***
- `SELECT * FROM employees WHERE last_name = 'snoW' (NOT CASESPECIFIC);` _will return **0 rows**
  with this setup data._

##### Teradata[¶](#id271)

##### Query[¶](#id272)

```
 SELECT * FROM employees WHERE last_name (NOT CASESPECIFIC)  = 'snoW' ;
```

##### Output[¶](#id273)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|
|4|Marco|SnoW|EngineerinG|
|10|JOHN|snow|Finance|

##### Snowflake[¶](#id274)

##### Query[¶](#id275)

```
 SELECT
   *
FROM
   employees
WHERE
   COLLATE(last_name /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/, 'en-ci-rtrim') = 'snoW' ;
```

##### Output[¶](#id276)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|2|John|SNOW|Engineering|
|3|WIlle|SNOW|Human resources|
|4|Marco|SnoW|EngineerinG|
|10|JOHN|snow|Finance|

#### LIKE operation[¶](#id277)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id278)

##### Teradata[¶](#id279)

##### Query[¶](#id280)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'GeorgE';
```

##### Output[¶](#id281)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id282)

##### Query[¶](#id283)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) LIKE RTRIM('GeorgE');
```

##### Output[¶](#id284)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id285)

##### Teradata[¶](#id286)

##### Query[¶](#id287)

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output[¶](#id288)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id289)

##### Query[¶](#id290)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) LIKE RTRIM('Snow');
```

##### Output[¶](#id291)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 3: CAST NOT CASESPECIFIC column to CASESPECIFIC and database mode is TERA Mode[¶](#id292)

##### Teradata[¶](#id293)

##### Query[¶](#id294)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'George' (CASESPECIFIC);
```

##### Output[¶](#id295)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Snowflake[¶](#id296)

##### Query[¶](#id297)

```
 SELECT
    *
FROM
    employees
WHERE
    COLLATE(first_name, 'en-cs-rtrim') LIKE 'George';
```

##### Output[¶](#id298)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|

##### Case 4: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#id299)

##### Teradata[¶](#id300)

##### Query[¶](#id301)

```
 SELECT *
FROM employees
WHERE last_name LIKE 'SNO%' (NOT CASESPECIFIC);
```

##### Output[¶](#id302)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake[¶](#id303)

##### Query[¶](#id304)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) LIKE RTRIM('SNO%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

##### Output[¶](#id305)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

#### IN Operation[¶](#id306)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id307)

##### Teradata[¶](#id308)

##### Query[¶](#id309)

```
 SELECT *
FROM employees
WHERE first_name IN ('George   ');
```

##### Output[¶](#id310)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id311)

##### Query[¶](#id312)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) IN (RTRIM('George   '));
```

##### Output[¶](#id313)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is not defined and database mode is TERA Mode[¶](#case-2-column-constraint-is-not-defined-and-database-mode-is-tera-mode)

**Note:**

In Tera mode, not defined case specification means `NOT CASESPECIFIC`.

##### Teradata[¶](#id314)

##### Query[¶](#id315)

```
 SELECT *
FROM employees
WHERE department IN ('Sales    ');
```

##### Output[¶](#id316)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|5|Mary||SaleS|
|6|GEORGE||sales|
|7|GEORGE||salEs|
|8|GeorgE||SalEs|

##### Snowflake[¶](#id317)

##### Query[¶](#id318)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(department) IN (RTRIM('Sales    '));
```

##### Output[¶](#id319)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|5|Mary||SaleS|
|6|GEORGE||sales|
|7|GEORGE||salEs|
|8|GeorgE||SalEs|

##### Case 3: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#case-3-column-constraint-is-casespecific-and-database-mode-is-tera-mode)

##### Teradata[¶](#id320)

##### Query[¶](#id321)

```
 SELECT *
FROM employees
WHERE last_name IN ('SNOW   ');
```

##### Output[¶](#id322)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake[¶](#id323)

##### Query[¶](#id324)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) IN (RTRIM('SNOW   '));
```

##### Output[¶](#id325)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

#### ORDER BY clause[¶](#id326)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id327)

##### Teradata[¶](#id328)

##### Query[¶](#id329)

```
 SELECT employee_id, first_name
FROM employees
ORDER BY employee_id, first_name;
```

##### Output[¶](#id330)

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

##### Snowflake[¶](#id331)

##### Query[¶](#id332)

```
 SELECT employee_id, first_name
FROM employees
ORDER BY employee_id, first_name;
```

##### Output[¶](#id333)

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

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id334)

##### Teradata[¶](#id335)

##### Query[¶](#id336)

```
 SELECT employee_id, last_name
FROM employees
ORDER BY employee_id, last_name;
```

##### Output[¶](#id337)

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

##### Snowflake[¶](#id338)

##### Query[¶](#id339)

```
 SELECT employee_id, last_name
FROM employees
ORDER BY employee_id, last_name;
```

##### Output[¶](#id340)

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

#### GROUP BY clause[¶](#id341)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id342)

##### Teradata[¶](#id343)

##### Query[¶](#id344)

```
 SELECT first_name
FROM employees
GROUP BY first_name;
```

##### Output[¶](#id345)

<!-- prettier-ignore -->
|first_name|
|---|
|Mary|
|GeorgE|
|WIlle|
|**JOHN**|
|Marco|
|**GEORGE**|

##### Snowflake[¶](#id346)

Warning

Case specification in output may vary depending on the number of columns selected.

##### Query[¶](#id347)

```
 SELECT
   first_name
FROM
   employees
GROUP BY first_name;
```

##### Output[¶](#id348)

<!-- prettier-ignore -->
|first_name|
|---|
|**John**|
|Marco|
|**George**|
|GeorgE|
|WIlle|
|Mary|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id349)

##### Teradata[¶](#id350)

##### Query[¶](#id351)

```
 SELECT last_name
FROM employees
GROUP BY last_name;
```

##### Output[¶](#id352)

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

##### Snowflake[¶](#id353)

##### Query[¶](#id354)

```
 SELECT
   last_name
FROM
   employees
GROUP BY last_name;
```

##### Output[¶](#id355)

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

#### HAVING clause[¶](#id356)

The HAVING clause will use the patterns in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#sample-column-constraint-is-not-casespecific-and-database-mode-is-tera-mode)

##### Teradata[¶](#id357)

**Note:**

Case specification in output may vary depending on the number of columns selected. This is also
related to the `GROUP BY` clause.

##### Query[¶](#id358)

```
 SELECT first_name
FROM employees
GROUP BY first_name
HAVING first_name = 'George  ';
```

##### Output[¶](#id359)

<!-- prettier-ignore -->
|employee_id|first_name|
|---|---|
|7|GEORGE|
|1|George|
|6|GEORGE|

##### Snowflake[¶](#id360)

##### Query[¶](#id361)

```
 SELECT
  employee_id,
  first_name
FROM
  employees
GROUP BY employee_id, first_name
HAVING
   RTRIM(first_name) = RTRIM('George  ');
```

##### Output[¶](#id362)

<!-- prettier-ignore -->
|employee_id|first_name|
|---|---|
|7|GEORGE|
|1|George|
|6|GEORGE|

#### CASE WHEN statement[¶](#id363)

The `CASE WHEN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata[¶](#id364)

##### Query[¶](#id365)

```
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

##### Output[¶](#id366)

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||GLOBAL SALES|
|Mary||Other|
|GeorgE||Other|
|GEORGE||GLOBAL SALES|

##### Snowflake[¶](#id367)

##### Query[¶](#id368)

```
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

##### Output[¶](#id369)

<!-- prettier-ignore -->
|first_name|last_name|department_full_name|
|---|---|---|
|GEORGE||GLOBAL SALES|
|Mary||Other|
|GeorgE||Other|
|GEORGE||GLOBAL SALES|

#### JOIN clause[¶](#id370)

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

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id371)

##### Teradata[¶](#id372)

##### Query[¶](#id373)

```
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

##### Output[¶](#id374)

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

##### Snowflake[¶](#id375)

##### Query[¶](#id376)

```
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

##### Output[¶](#id377)

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

### Related EWIs[¶](#id378)

[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0007):
GROUP BY REQUIRED COLLATE FOR CASE INSENSITIVE COLUMNS

[SC-FDM-TD0032](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0032)
: [NOT] CASESPECIFIC CLAUSE WAS REMOVED

## TERA Mode For Strings Comparison - NO COLLATE[¶](#tera-mode-for-strings-comparison-no-collate)

This section defines the translation specification for string in Tera mode without using COLLATE.

### Description [¶](#id379)

#### Tera Mode for string comparison and NO COLLATE usages[¶](#tera-mode-for-string-comparison-and-no-collate-usages)

The Tera Mode string comparison without the use of COLLATE will apply `RTRIM` and `UPPER` as needed.
The default case specification trim behavior may be taken into account.

### Sample Source Patterns [¶](#id380)

#### Setup data[¶](#id381)

##### Teradata[¶](#id382)

```
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

##### Snowflake[¶](#id383)

```
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

#### Comparison operation[¶](#id384)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id385)

This example demonstrates the usage of a column set up as `NOT CASESPECIFIC` as it is a `first_name`
column. Even when asking for the string `'GEorge',` the query execution will retrieve results in
Teradata because the case specification is not considered.

To emulate this scenario in Snowflake, there are implemented two functions:
`RTRIM(UPPER(string_evaluation))`, `UPPER` is required in this scenario because the string does not
review the case specification.

##### Teradata[¶](#id386)

##### Query[¶](#id387)

```
 SELECT *
FROM employees
WHERE first_name = 'GEorge ';
```

##### Output[¶](#id388)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id389)

##### Query[¶](#id390)

```
 SELECT
 *
FROM
 employees
WHERE
 RTRIM(UPPER(first_name)) = RTRIM(UPPER('GEorge '));
```

##### Output[¶](#id391)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id392)

For this example, the column constraint is `CASESPECIFIC`, for which the example does not retrieve
rows in Teradata because ‘`Snow`’ is not equal to ‘`SNOW`’.

In Snowflake, the resulting migration points only to the use of the `RTRIM` function since the case
specification is important.

##### Teradata[¶](#id393)

##### Query[¶](#id394)

```
 SELECT *
FROM employees
WHERE last_name = 'SNOW ';
```

##### Output[¶](#id395)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Snowflake[¶](#id396)

##### Query[¶](#id397)

```
SELECT
 *
FROM
 employees
WHERE
 RTRIM(last_name) = RTRIM('SNOW ');
```

##### Output[¶](#id398)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|3|WIlle|SNOW|Human resources|
|2|John|SNOW|Engineering|

##### Case 3: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#case-3-cast-casespecific-column-to-not-casespecific-and-database-mode-is-tera-mode)

##### Teradata[¶](#id399)

Warning

The (`CASESPECIFIC`) overrides the column constraint in the table definition.

##### Query[¶](#id400)

```
 SELECT * FROM employees WHERE first_name = 'GEORGE   ' (CASESPECIFIC);
```

##### Output[¶](#id401)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|6|GEORGE||sales|

##### Snowflake[¶](#id402)

**Note:**

RTRIM is required on the left side, and RTRIM is required on the right side.

##### Query[¶](#id403)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(first_name) = RTRIM('GEORGE   ' /*** SSC-FDM-TD0032 - CASESPECIFIC CLAUSE WAS REMOVED ***/);
```

##### Output[¶](#id404)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|6|GEORGE||sales|

##### Case 4: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#case-4-cast-not-casespecific-column-to-not-casespecific-and-database-mode-is-tera-mode)

##### Teradata[¶](#id405)

##### Query[¶](#id406)

```
 SELECT * FROM employees WHERE first_name = 'GEorge   ' (NOT CASESPECIFIC) ;
```

##### Output[¶](#id407)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id408)

##### Query[¶](#id409)

```
 SELECT
   *
FROM
   employees
WHERE
   UPPER(RTRIM(first_name)) = UPPER(RTRIM('GEorge   ' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/));
```

##### Output[¶](#id410)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 5: Blank spaces case. Column constraint is NOT CASESPECIFIC, database mode is TERA Mode, and using equal operation[¶](#case-5-blank-spaces-case-column-constraint-is-not-casespecific-database-mode-is-tera-mode-and-using-equal-operation)

##### Teradata[¶](#id411)

##### Query[¶](#id412)

```
 SELECT *
FROM employees
WHERE last_name = '   ';
```

##### Output[¶](#id413)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|5|Mary||SaleS|
|8|GeorgE||SalEs|
|6|GEORGE||sales|

##### Snowflake[¶](#id414)

##### Query[¶](#id415)

```
 SELECT
   *
FROM
   employees
WHERE
   RTRIM(last_name) = RTRIM('   ');
```

##### Output[¶](#id416)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|5|Mary||SaleS|
|8|GeorgE||SalEs|
|6|GEORGE||sales|

#### LIKE operation[¶](#id417)

**Note:**

This operation works differently from another one. Blank spaces must be the same quantity to
retrieve information.

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id418)

This example is expected to display one row because the case specification is not relevant.

**Note:**

In Snowflake, the migration uses the
[ILIKE](https://docs.snowflake.com/en/sql-reference/functions/ilike) operation. This performs a
case-insensitive comparison.

##### Teradata[¶](#id419)

##### Query[¶](#id420)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'GeorgE';
```

##### Output[¶](#id421)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id422)

##### Query[¶](#id423)

```
 SELECT *
FROM employees
WHERE first_name ILIKE 'GeorgE';
```

##### Output[¶](#id424)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id425)

##### Teradata[¶](#id426)

##### Query[¶](#id427)

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output[¶](#id428)

<!-- prettier-ignore -->
|first_name|last_name|department|
|---|---|---|
|George|Snow|Sales|
|Jonh|Snow|Engineering|

##### Snowflake[¶](#id429)

##### Query[¶](#id430)

```
 SELECT *
FROM employees
WHERE last_name LIKE 'Snow';
```

##### Output[¶](#id431)

<!-- prettier-ignore -->
|first_name|last_name|department|
|---|---|---|
|George|Snow|Sales|
|Jonh|Snow|Engineering|

##### Case 3: CAST CASESPECIFIC column to NOT CASESPECIFIC and database mode is TERA Mode[¶](#id432)

##### Teradata[¶](#id433)

##### Query[¶](#id434)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'George' (NOT CASESPECIFIC);
```

##### Output[¶](#id435)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id436)

##### Query[¶](#id437)

```
 SELECT
   *
FROM
   employees
WHERE
   first_name ILIKE 'George' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output[¶](#id438)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 4: CAST NOT CASESPECIFIC column to NOT CASESPECIFIC and database mode is ANSI Mode[¶](#case-4-cast-not-casespecific-column-to-not-casespecific-and-database-mode-is-ansi-mode)

**Note:**

This case requires the translation to `ILIKE`.

##### Teradata[¶](#id439)

##### Query[¶](#id440)

```
 SELECT *
FROM employees
WHERE first_name LIKE 'GE%' (NOT CASESPECIFIC);
```

##### Output[¶](#id441)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id442)

##### Query[¶](#id443)

```
 SELECT
   *
FROM
   employees
WHERE
   first_name ILIKE 'GE%' /*** SSC-FDM-TD0032 - NOT CASESPECIFIC CLAUSE WAS REMOVED ***/;
```

##### Output[¶](#id444)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

#### IN Operation[¶](#id445)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id446)

##### Teradata[¶](#id447)

##### Query[¶](#id448)

```
 SELECT *
FROM employees
WHERE first_name IN ('GeorgE');
```

##### Output[¶](#id449)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Snowflake[¶](#id450)

##### Query[¶](#id451)

```
 SELECT *
FROM employees
WHERE RTRIM(UPPER(first_name)) IN (RTRIM(UPPER('GeorgE')));
```

##### Output[¶](#id452)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|7|GEORGE||salEs|
|1|George|Snow|Sales|
|6|GEORGE||sales|

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id453)

For this example, the usage of the UPPER function is not required since, in the Teradata database,
the case specification is relevant to the results.

##### Teradata[¶](#id454)

##### Query[¶](#id455)

```
 SELECT *
FROM employees
WHERE last_name IN ('SnoW');
```

##### Output[¶](#id456)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

##### Snowflake[¶](#id457)

##### Query[¶](#id458)

```
 SELECT *
FROM employees
WHERE RTRIM(last_name) IN (RTRIM('SnoW'));
```

##### Output[¶](#id459)

<!-- prettier-ignore -->
|employee_id|first_name|last_name|department|
|---|---|---|---|
|4|Marco|SnoW|EngineerinG|

#### ORDER BY clause[¶](#id460)

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id461)

Danger

**Notice that this output order can differ.**

##### Teradata[¶](#id462)

##### Query[¶](#id463)

```
 SELECT department
FROM employees
ORDER BY department;
```

##### Output[¶](#id464)

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

##### Snowflake[¶](#id465)

##### Query[¶](#id466)

```
 SELECT department
FROM employees
ORDER BY UPPER(department);
```

##### Output[¶](#id467)

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

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id468)

Danger

**Notice that this output can differ in order.**

##### Teradata[¶](#id469)

##### Query[¶](#id470)

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output[¶](#id471)

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

##### Snowflake[¶](#id472)

##### Query[¶](#id473)

```
 SELECT last_name
FROM employees
ORDER BY last_name;
```

##### Output[¶](#id474)

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

#### GROUP BY clause[¶](#id475)

Warning

**Notice that this output can differ. To ensure a functional equivalence, it is required to use the
COLLATE expression.**

Please review the SSC-EWI-TD0007 for more information.

_The following might be a workaround without `collate`:_

`SELECT RTRIM(UPPER(first_name))`

`FROM employees`

`GROUP BY RTRIM(UPPER(first_name));`

**About the column behavior**

Danger

Please review the insertion of data in Snowflake. Snowflake does allow the insertion of values as
‘`GEORGE`’ and ‘`georges`’ without showing errors because the case specification is not bound
explicitly with the column.

Assume a table and data as follows:

```
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

```
 INSERT INTO students(first_name) VALUES ('GEORGE');
INSERT INTO students(first_name) VALUES ('GeorGe');
INSERT INTO students(first_name) VALUES ('George  ');
INSERT INTO students(first_name) VALUES ('GeOrge');
INSERT INTO students(first_name) VALUES ('GEorge');
INSERT INTO students(first_name) VALUES ('George');
```

##### Case 1: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id476)

##### Teradata[¶](#id477)

##### Query[¶](#id478)

```
 SELECT first_name
FROM employees
GROUP BY first_name;
```

##### Output[¶](#id479)

<!-- prettier-ignore -->
|first_name|
|---|
|Mary|
|GeorgE|
|WIlle|
|JOHN|
|Marco|
|GEORGE|

##### Snowflake[¶](#id480)

##### Query[¶](#id481)

```
 SELECT
   first_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY first_name;
```

##### Output[¶](#id482)

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

##### Case 2: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#id483)

##### Teradata[¶](#id484)

##### Query[¶](#id485)

```
 SELECT last_name
FROM employees
GROUP BY last_name;
```

##### Output[¶](#id486)

<!-- prettier-ignore -->
|last_name|
|---|
|SnoW|
|           |
|SNOW|
|SnoW|
|Snow|
|snow|

##### Snowflake[¶](#id487)

##### Query[¶](#id488)

```
 SELECT
   last_name
FROM
   employees
!!!RESOLVE EWI!!! /*** SSC-EWI-TD0007 - GROUP BY IS NOT EQUIVALENT IN TERADATA MODE ***/!!!
GROUP BY last_name;
```

##### Output[¶](#id489)

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

#### HAVING clause[¶](#id490)

The HAVING clause will use the patterns in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Sample: Column constraint is CASESPECIFIC and database mode is TERA Mode[¶](#sample-column-constraint-is-casespecific-and-database-mode-is-tera-mode)

##### Teradata[¶](#id491)

##### Query[¶](#id492)

```
 SELECT last_name
FROM employees
GROUP BY last_name
HAVING last_name = 'Snow';
```

##### Output[¶](#id493)

<!-- prettier-ignore -->
|last_name|
|---|
|Snow|

##### Snowflake[¶](#id494)

##### Query[¶](#id495)

```
 SELECT last_name
FROM employees
GROUP BY last_name
HAVING RTRIM(last_name) = RTRIM('Snow');
```

##### Output[¶](#id496)

<!-- prettier-ignore -->
|last_name|
|---|
|Snow|

#### CASE WHEN statement[¶](#id497)

The `CASE WHEN` statement will use the patterns described in:

- Evaluation operations.

  - For example: `=, !=, <, >.`

- LIKE operation.
- IN Operation.
- CAST to evaluation operation.
- CAST to LIKE operation.

The following sample showcases a pattern with evaluation operation.

##### Teradata[¶](#id498)

##### Query[¶](#id499)

```
 SELECT first_name,
      last_name,
      CASE
          WHEN department = 'EngineerinG' THEN 'Information Technology'
          WHEN last_name = 'SNOW' THEN 'GLOBAL COOL SALES'
          ELSE 'Other'
      END AS department_full_name
FROM employees;
```

##### Output[¶](#id500)

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

##### Snowflake[¶](#id501)

##### Query[¶](#id502)

```
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

##### Output[¶](#id503)

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

#### JOIN clause[¶](#id504)

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

##### Sample: Column constraint is NOT CASESPECIFIC and database mode is TERA Mode[¶](#id505)

##### Teradata[¶](#id506)

##### Query[¶](#id507)

```
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

##### Output[¶](#id508)

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

##### Snowflake[¶](#id509)

##### Query[¶](#id510)

```
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

##### Output[¶](#id511)

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

### Known Issues[¶](#known-issues)

1. there are some mode-specific SQL statement restrictions: `BEGIN TRANSACTION`, `END TRANSACTION`,
   `COMMIT [WORK]`.
2. Data insertion may differ in Snowflake since the case specification is not bound to the column
   declaration.
3. `GROUP BY` may differ in order, but group the correct values.
4. `ORDER BY` behaves differently in Snowflake.
5. If a function has a TRIM() from the source code, this workaround will add the required functions
   to the source code. So, RTRIM will be applied to the TRIM() source function.

### Related EWIs[¶](#id512)

[SSC-EWI-TD0007](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/teradataEWI#ssc-ewi-td0007):
GROUP BY IS NOT EQUIVALENT IN TERADATA MODE
