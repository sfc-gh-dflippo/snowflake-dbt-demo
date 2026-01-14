---
description:
  This section describe important consideration when migration data from Teradata to Snowflake.
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/data-migration-considerations
title: SnowConvert AI - Teradata - Data Migration Considerations | Snowflake Documentation
---

## UNION ALL Data Migration[¶](#union-all-data-migration)

Data migration considerations for UNION ALL.

UNION ALL is a SQL operator that allows the combination of multiple resultsets. The syntax is the
following:

```
 query_expression_1 UNION [ ALL ] query_expression_2
```

For more information, please review the following
[Teradata](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/Set-Operators/UNION-Operator/UNION-Operator-Syntax)
documentation.

### Column Size differences[¶](#column-size-differences)

Even though the operator is translated into the same operator in Snowflake, there could be detailed
differences in functional equivalence. For example, the union of different columns which have
different column sizes. Teradata does truncate the values when the first SELECT statement contains
less space in the columns.

#### Teradata behavior[¶](#teradata-behavior)

**Note:**

**Same behavior in ANSI and TERA session modes.**

For this example, the following input will show the Teradata behavior.

##### Teradata setup data[¶](#teradata-setup-data)

```
 CREATE TABLE table1
(
col1 VARCHAR(20)
);

INSERT INTO table1 VALUES('value 1 abcdefghijk');
INSERT INTO table1 VALUES('value 2 abcdefghijk');

CREATE TABLE table2
(
col1 VARCHAR(10)
);

INSERT INTO table2 VALUES('t2 row 1 a');
INSERT INTO table2 VALUES('t2 row 2 a');
INSERT INTO table2 VALUES('t2 row 3 a');
```

##### Snowflake setup data[¶](#snowflake-setup-data)

```
 CREATE OR REPLACE TABLE table1
(
col1 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table1
VALUES ('value 1 abcdefghijk');

INSERT INTO table1
VALUES ('value 2 abcdefghijk');

CREATE OR REPLACE TABLE table2
(
col1 VARCHAR(10)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table2
VALUES ('t2 row 1 a');

INSERT INTO table2
VALUES ('t2 row 2 a');

INSERT INTO table2
VALUES ('t2 row 3 a');
```

#### **Case 1 - one single column: UNION ALL for a column varchar (20) over a column varchar (10)**[¶](#case-1-one-single-column-union-all-for-a-column-varchar-20-over-a-column-varchar-10)

SuccessPlaceholder

For this case, the functional equivalence is the same

##### Teradata input[¶](#teradata-input)

```
 SELECT col1 FROM table1
UNION ALL
SELECT col1 FROM table2;
```

##### Teradata output[¶](#teradata-output)

```
value 1 abcdefghijk
t2 row 3 a
value 2 abcdefghijk
t2 row 1 a
t2 row 2 a
```

##### Snowflake input[¶](#snowflake-input)

```
 SELECT
col1 FROM
table1
UNION ALL
SELECT
col1 FROM
table2;
```

##### Snowflake output[¶](#snowflake-output)

```
value 1 abcdefghijk
t2 row 3 a
value 2 abcdefghijk
t2 row 1 a
t2 row 2 a
```

#### **Case 2 - one single column: UNION ALL for a column varchar (10) over a column varchar (20)**[¶](#case-2-one-single-column-union-all-for-a-column-varchar-10-over-a-column-varchar-20)

Danger

In this case, the function equivalence is not the same.

The following case does not show functional equivalence in Snowflake. The column values should be
truncated as in the Teradata sample.

##### Teradata input[¶](#id1)

```
 SELECT col1 FROM table2
UNION ALL
SELECT col1 FROM table1;
```

##### Teradata output[¶](#id2)

```
t2 row 3 a
value 1 ab --> truncated
t2 row 1 a
t2 row 2 a
value 2 ab --> truncated
```

##### Snowflake input[¶](#id3)

```
 SELECT
col1 FROM
table2
UNION ALL
SELECT
col1 FROM
table1;
```

##### Snowflake output[¶](#id4)

```
t2 row 3 a
value 1 abcdefghijk --> NOT truncated
t2 row 1 a
t2 row 2 a
value 2 abcdefghijk --> NOT truncated
```

**Workaround to get the same functionality**

In this case, the size of the column of the `table2` is 10 and the `table1` is 20. So, the size of
the first column in the query should be the element to complete the `LEFT()` function used here.
Review more information about the Snowflake LEFT function
[HERE](https://docs.snowflake.com/en/sql-reference/functions/left).

##### Snowflake input[¶](#id5)

```
 SELECT col1 FROM table2 -- size (10)
UNION ALL
SELECT LEFT(col1, 10) AS col1 FROM table1;
```

##### Snowflake output[¶](#id6)

```
t2 row 1 a
t2 row 2 a
t2 row 3 a
value 1 ab
value 2 ab
```

#### **Case 3 - multiple columns - same size by table: UNION ALL for columns varchar (20) over columns varchar (10)**[¶](#case-3-multiple-columns-same-size-by-table-union-all-for-columns-varchar-20-over-columns-varchar-10)

For this case, it is required to set up new data as follows:

##### Teradata setup data[¶](#id7)

```
 CREATE TABLE table3
(
col1 VARCHAR(20),
col2 VARCHAR(20)
);

INSERT INTO table3 VALUES('value 1 abcdefghijk', 'value 1 abcdefghijk');
INSERT INTO table3 VALUES('value 2 abcdefghijk', 'value 2 abcdefghijk');

CREATE TABLE table4
(
col1 VARCHAR(10),
col2 VARCHAR(10)
);

INSERT INTO table4 VALUES('t2 row 1 a', 't2 row 1 b');
INSERT INTO table4 VALUES('t2 row 2 a', 't2 row 2 b');
INSERT INTO table4 VALUES('t2 row 3 a', 't2 row 3 b');
```

##### Snowflake setup data[¶](#id8)

```
 CREATE OR REPLACE TABLE table3
(
col1 VARCHAR(20),
col2 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table3
VALUES ('value 1 abcdefghijk', 'value 1 abcdefghijk');

INSERT INTO table3
VALUES ('value 2 abcdefghijk', 'value 2 abcdefghijk');

CREATE OR REPLACE TABLE table4
(
col1 VARCHAR(10),
col2 VARCHAR(10)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table4
VALUES ('t2 row 1 a', 't2 row 1 b');

INSERT INTO table4
VALUES ('t2 row 2 a', 't2 row 2 b');

INSERT INTO table4
VALUES ('t2 row 3 a', 't2 row 3 b');
```

Once the new tables and data are created, the following query can be evaluated.

**Note:**

For this case, the functional equivalence is the same

##### Teradata input[¶](#id9)

```
 select col1, col2 from table3
union all
select col1, col2 from table4;
```

##### Teradata output[¶](#id10)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|value 1 abcdefghijk|value 1 abcdefghijk|
|t2 row 3 a|t2 row 3 b|
|value 2 abcdefghijk|value 2 abcdefghijk|
|t2 row 1 a|t2 row 1 b|
|t2 row 2 a|t2 row 2 b|

##### Snowflake input[¶](#id11)

```
 SELECT
col1, col2 FROM
table3
UNION ALL
SELECT
col1, col2 FROM
table4;
```

##### Snowflake output[¶](#id12)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|value 1 abcdefghijk|value 1 abcdefghijk|
|value 2 abcdefghijk|value 2 abcdefghijk|
|t2 row 1 a|t2 row 1 b|
|t2 row 2 a|t2 row 2 b|
|t2 row 3 a|t2 row 3 b|

#### Case 4 - multiple columns - same size by table: UNION ALL for columns varchar (10) over columns varchar (20)[¶](#case-4-multiple-columns-same-size-by-table-union-all-for-columns-varchar-10-over-columns-varchar-20)

Warning

In this case, the function equivalence is not the same.

##### Teradata input[¶](#id13)

```
 select col1, col2 from table4
union all
select col1, col2 from table3;
```

##### Teradata output[¶](#id14)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|t2 row 3 a|t2 row 3 b|
|value 1 ab|value 1 ab|
|t2 row 1 a|t2 row 1 b|
|t2 row 2 a|t2 row 2 b|
|value 2 ab|value 2 ab|

##### Snowflake input[¶](#id15)

```
 SELECT
col1, col2 FROM
table4
UNION ALL
SELECT
col1, col2 FROM
table3;
```

##### Snowflake output[¶](#id16)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|t2 row 1 a|t2 row 1 b|
|t2 row 2 a|t2 row 2 b|
|t2 row 3 a|t2 row 3 b|
|value 1 abcdefghijk|value 1 abcdefghijk|
|value 2 abcdefghijk|value 2 abcdefghijk|

**Workaround to get the same functionality**

Apply the column size to the second `SELECT` on the columns to get the same functionality.

##### Snowflake input[¶](#id17)

```
 SELECT col1, col2 FROM table4 -- size (10)
UNION ALL
SELECT LEFT(col1, 10) AS col1, LEFT(col2, 10) AS col2 FROM table3;
```

##### Snowflake output[¶](#id18)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|t2 row 1 a|t2 row 1 b|
|t2 row 2 a|t2 row 2 b|
|t2 row 3 a|t2 row 3 b|
|value 1 ab|value 1 ab|
|value 2 ab|value 2 ab|

#### Case 5 - multiple columns - different sizes by table: UNION ALL for columns varchar (10) over columns varchar (20)[¶](#case-5-multiple-columns-different-sizes-by-table-union-all-for-columns-varchar-10-over-columns-varchar-20)

For this case, it is required to set up new data as follows:

##### Teradata setup data[¶](#id19)

```
 CREATE TABLE table5
(
col1 VARCHAR(20),
col2 VARCHAR(12)
);

INSERT INTO table5 VALUES('value 1 abcdefghijk', 'value 1 abcdefghijk');
INSERT INTO table5 VALUES('value 2 abcdefghijk', 'value 2 abcdefghijk');

CREATE TABLE table6
(
col1 VARCHAR(10),
col2 VARCHAR(5)
);

INSERT INTO table6 VALUES('t2 row 1 a', 't2 row 1 b');
INSERT INTO table6 VALUES('t2 row 2 a', 't2 row 2 b');
INSERT INTO table6 VALUES('t2 row 3 a', 't2 row 3 b');
```

##### Snowflake setup data[¶](#id20)

```
 CREATE OR REPLACE TABLE table5
(
col1 VARCHAR(20),
col2 VARCHAR(12)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table5
VALUES ('value 1 abcdefghijk', 'value 1 abcd');

INSERT INTO table5
VALUES ('value 2 abcdefghijk', 'value 2 abcd');

CREATE OR REPLACE TABLE table6
(
col1 VARCHAR(10),
col2 VARCHAR(5)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table6
VALUES ('t2 row 1 a', 't2 1b');

INSERT INTO table6
VALUES ('t2 row 2 a', 't2 2b');

INSERT INTO table6
VALUES ('t2 row 3 a', 't2 3b');
```

Once the new tables and data are created, the following query can be evaluated.

**Note:**

For this case, the functional equivalence is the same

##### Teradata input[¶](#id21)

```
 select col1, col2 from table5
union all
select col1, col2 from table6;
```

##### Teradata output[¶](#id22)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|value 1 abcdefghijk|value 1 abcd|
|t2 row 3 a|t2 3b|
|value 2 abcdefghijk|value 2 abcd|
|t2 row 1 a|t2 1b|
|t2 row 2 a|t2 2b|

##### Snowflake input[¶](#id23)

```
 SELECT
col1, col2 FROM
table5
UNION ALL
SELECT
col1, col2 FROM
table6;
```

##### Snowflake output[¶](#id24)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|value 1 abcdefghijk|value 1 abcd|
|value 2 abcdefghijk|value 2 abcd|
|t2 row 1 a|t2 1b|
|t2 row 2 a|t2 2b|
|t2 row 3 a|t2 3b|

#### Case 6 - multiple columns - different sizes by table: UNION ALL for columns varchar (20), varchar(10) over columns varchar (10), varchar(5)[¶](#case-6-multiple-columns-different-sizes-by-table-union-all-for-columns-varchar-20-varchar-10-over-columns-varchar-10-varchar-5)

Warning

In this case, the function equivalence is not the same.

##### Teradata input[¶](#id25)

```
 select col1, col2 from table6
union all
select col1, col2 from table5;
```

##### Teradata output[¶](#id26)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|t2 row 3 a|t2 3b|
|**value 1 ab**|**value**|
|t2 row 1 a|t2 1b|
|t2 row 2 a|t2 2b|
|**value 2 ab**|**value**|

##### Snowflake input[¶](#id27)

```
 SELECT
col1, col2 FROM
table6
UNION ALL
SELECT
col1, col2 FROM
table5;
```

##### Snowflake output[¶](#id28)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|t2 row 1 a|t2 1b|
|t2 row 2 a|t2 2b|
|t2 row 3 a|t2 3b|
|**value 1 abcdefghijk**|**value 1 abcd**|
|**value 2 abcdefghijk**|**value 2 abcd**|

**Workaround to get the same functionality**

The column with the smallest size from the first `SELECT` is used to determine the size of the
columns from the second `SELECT`.

##### Snowflake input[¶](#id29)

```
 SELECT
col1, col2 FROM
table6
UNION ALL
SELECT
LEFT(col1, 5) as col1, LEFT(col2, 5) AS col2 FROM
table5;
```

##### Snowflake output[¶](#id30)

<!-- prettier-ignore -->
|col1|col2|
|---|---|
|t2 row 3 a|t2 3b|
|**value 1 ab**|**value**|
|t2 row 1 a|t2 1b|
|t2 row 2 a|t2 2b|
|**value 2 ab**|**value**|

#### Case 7 - multiple columns _expression_ - different sizes by table: UNION ALL for columns varchar (20), varchar(20) over columns varchar (10), varchar(10)[¶](#case-7-multiple-columns-expression-different-sizes-by-table-union-all-for-columns-varchar-20-varchar-20-over-columns-varchar-10-varchar-10)

Use the data set up
[here](#case-3-multiple-columns-same-size-by-table-union-all-for-columns-varchar-20-over-columns-varchar-10).
Once the new tables and data are created, the following query can be evaluated.

**Note:**

For this case, the functional equivalence is the same

##### Teradata input[¶](#id31)

```
 select col1 || col2 from table3
union all
select col1 || col2 from table4;
```

##### Teradata output[¶](#id32)

<!-- prettier-ignore -->
|col1||col2|
|---|---|---|
|value 1 abcdefghijkvalue 1 abcdefghijk|
|t2 row 3 at2 row 3 b|
|value 2 abcdefghijkvalue 2 abcdefghijk|
|t2 row 1 at2 row 1 b|
|t2 row 2 at2 row 2 b|

##### Snowflake input[¶](#id33)

```
 SELECT
col1 || col2 FROM
table3
UNION ALL
SELECT
col1 || col2 FROM
table4;
```

##### Snowflake output[¶](#id34)

<!-- prettier-ignore -->
|col1||col2|
|---|---|---|
|value 1 abcdefghijkvalue 1 abcdefghijk|
|value 2 abcdefghijkvalue 2 abcdefghijk|
|t2 row 1 at2 row 1 b|
|t2 row 2 at2 row 2 b|
|t2 row 3 at2 row 3 b|

#### Case 8 - multiple columns _expression_ - different sizes by table: UNION ALL for columns varchar (20), varchar(20) over columns varchar (10), varchar(10)[¶](#case-8-multiple-columns-expression-different-sizes-by-table-union-all-for-columns-varchar-20-varchar-20-over-columns-varchar-10-varchar-10)

Warning

This case has functional differences.

##### Teradata input[¶](#id35)

```
 select col1 || col2 from table4
union all
select col1 || col2 from table3;
```

##### Teradata output[¶](#id36)

<!-- prettier-ignore -->
|col1||col2|
|---|---|---|
|t2 row 1 at2 row 1 b|
|t2 row 2 at2 row 2 b|
|t2 row 3 at2 row 3 b|
|value 1 abcdefghijkv|
|value 2 abcdefghijkv|

##### Snowflake input[¶](#id37)

```
 SELECT
col1 || col2 FROM
table4
UNION ALL
SELECT
col1 || col2 FROM
table3;
```

##### Snowflake output[¶](#id38)

<!-- prettier-ignore -->
|col1||col2|
|---|---|---|
|t2 row 1 at2 row 1 b|
|t2 row 2 at2 row 2 b|
|t2 row 3 at2 row 3 b|
|value 1 abcdefghijkvalue 1 abcdefghijk|
|value 2 abcdefghijkvalue 2 abcdefghijk|

**Workaround to get the same functionality**

The sum of the column sizes of the less big column should be used in the `LEFT` function. For
example, the less big column is varchar(10), so the limit of the `LEFT` function should be 20 (10 +
10).

Warning

The sum of the first `SELECT` if this is less big, it would be used for the truncation of the
values.

##### Snowflake input[¶](#id39)

```
 SELECT
col1 || col2 FROM
table4
UNION ALL
SELECT
LEFT(col1 || col2, 20) FROM
table3;
```

##### Snowflake output[¶](#id40)

<!-- prettier-ignore -->
|col1||col2|
|---|---|---|
|t2 row 1 at2 row 1 b|
|t2 row 2 at2 row 2 b|
|t2 row 3 at2 row 3 b|
|value 1 abcdefghijkv|
|value 2 abcdefghijkv|

#### Other considerations about column size differences[¶](#other-considerations-about-column-size-differences)

- `CHAR` and `VARCHAR` behave the same.
- Number columns may behave differently. The numbers cannot be truncated, so there is an overflow in
  the Teradata environment. So, this is not applied to these data types. Review the following
  example:

```
-- Teradata number sample
CREATE TABLE table11
(
col1 NUMBER(2)
);

INSERT INTO table11 VALUES(10);
INSERT INTO table11 VALUES(10);

CREATE TABLE table12
(
col1 NUMBER(1)
);

INSERT INTO table12 VALUES(1);
INSERT INTO table12 VALUES(1);
INSERT INTO table12 VALUES(1);

-- ERROR!  Overflow occurred when computing an expression involving table11.col1
SELECT col1 FROM table12
UNION ALL
SELECT col1 FROM table11;
```
