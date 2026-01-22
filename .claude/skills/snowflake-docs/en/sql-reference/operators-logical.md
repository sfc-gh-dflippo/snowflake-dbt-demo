---
auto_generated: true
description: Logical operators return the result of a particular Boolean operation
  on one or two input expressions. Logical operators are also referred to as Boolean
  operators.
last_scraped: '2026-01-14T16:56:52.404784+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/operators-logical
title: Logical operators | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)
3. [SQL command reference](../sql-reference-commands.md)

   * [Query syntax](constructs.md)
   * [Query operators](operators.md)

     + [Arithmetic](operators-arithmetic.md)
     + [Comparison](operators-comparison.md)
     + [Expansion](operators-expansion.md)
     + [Flow](operators-flow.md)
     + [Logical](operators-logical.md)
     + [Set](operators-query.md)
     + [Subquery](operators-subquery.md)
   * [General DDL](sql-ddl-summary.md)
   * [General DML](sql-dml.md)
   * [All commands (alphabetical)](sql-all.md)")
   * [Accounts](commands-account.md)
   * [Users, roles, & privileges](commands-user-role.md)
   * [Integrations](commands-integration.md)
   * [Business continuity & disaster recovery](commands-replication.md)
   * [Sessions](commands-session.md)
   * [Transactions](commands-transaction.md)
   * [Virtual warehouses & resource monitors](commands-warehouse.md)
   * [Databases, schemas, & shares](commands-database.md)
   * [Tables, views, & sequences](commands-table.md)
   * [Functions, procedures, & scripting](commands-function.md)
   * [Streams & tasks](commands-stream.md)
   * [dbt Projects on Snowflake](commands-dbt-projects-on-snowflake.md)
   * [Classes & instances](commands-class.md)
   * [Machine learning](commands-ml.md)
   * [Cortex](commands-cortex.md)
   * [Listings](commands-listings.md)
   * [Openflow data plane integration](commands-ofdata-plane.md)
   * [Organization profiles](commands-organization-profiles.md)
   * [Security](commands-security.md)
   * [Data Governance](commands-data-governance.md)
   * [Privacy](commands-privacy.md)
   * [Data loading & unloading](commands-data-loading.md)
   * [File staging](commands-file.md)
   * [Storage lifecycle policies](commands-storage-lifecycle-policies.md)
   * [Git](commands-git.md)
   * [Alerts](commands-alert.md)
   * [Native Apps Framework](commands-native-apps.md)
   * [Streamlit](commands-streamlit.md)
   * [Notebook](commands-notebook.md)
   * [Snowpark Container Services](commands-snowpark-container-services.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[SQL command reference](../sql-reference-commands.md)[Query operators](operators.md)Logical

# Logical operators[¶](#logical-operators "Link to this heading")

Logical operators return the result of a particular Boolean operation on one or two input expressions. Logical operators are also
referred to as Boolean operators.

Logical operators can only be used as a predicate (for example, in the [WHERE](constructs/where) clause). Input expressions must be predicates.

See also:
:   [BOOLAND](functions/booland) , [BOOLNOT](functions/boolnot) , [BOOLOR](functions/boolor) , [BOOLXOR](functions/boolxor)

## List of logical operators[¶](#list-of-logical-operators "Link to this heading")

| Operator | Syntax example | Description |
| --- | --- | --- |
| `AND` | `a AND b` | Matches both expressions (`a` and `b`). |
| `NOT` | `NOT a` | Doesn’t match the expression. |
| `OR` | `a OR b` | Matches either expression. |

The order of precedence of these operators is shown below (from highest to
lowest):

* NOT
* AND
* OR

## Examples[¶](#examples "Link to this heading")

The following examples use logical operators:

* [Use logical operators in queries on table data](#label-operators-logical-examples-table-data)
* [Use logical operators in queries on Boolean values](#label-operators-logical-examples-boolean-values)
* [Show “truth tables” for the logical operators](#label-operators-logical-examples-truth-tables)

### Use logical operators in queries on table data[¶](#use-logical-operators-in-queries-on-table-data "Link to this heading")

Create a table and insert data:

```
CREATE OR REPLACE TABLE logical_test1 (id INT, a INT, b VARCHAR);

INSERT INTO logical_test1 (id, a, b) VALUES (1, 8, 'Up');
INSERT INTO logical_test1 (id, a, b) VALUES (2, 25, 'Down');
INSERT INTO logical_test1 (id, a, b) VALUES (3, 15, 'Down');
INSERT INTO logical_test1 (id, a, b) VALUES (4, 47, 'Up');

SELECT * FROM logical_test1;
```

Copy

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  2 | 25 | Down |
|  3 | 15 | Down |
|  4 | 47 | Up   |
+----+----+------+
```

#### Execute queries that use a single logical operator[¶](#execute-queries-that-use-a-single-logical-operator "Link to this heading")

Use a single logical operator in the WHERE clause of various queries:

```
SELECT *
  FROM logical_test1
  WHERE a > 20 AND
        b = 'Down';
```

Copy

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  2 | 25 | Down |
+----+----+------+
```

```
SELECT *
  FROM logical_test1
  WHERE a > 20 OR
        b = 'Down';
```

Copy

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  2 | 25 | Down |
|  3 | 15 | Down |
|  4 | 47 | Up   |
+----+----+------+
```

```
SELECT *
  FROM logical_test1
  WHERE a > 20 OR
        b = 'Up';
```

Copy

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  2 | 25 | Down |
|  4 | 47 | Up   |
+----+----+------+
```

```
SELECT *
  FROM logical_test1
  WHERE NOT a > 20;
```

Copy

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  3 | 15 | Down |
+----+----+------+
```

#### Show the precedence of logical operators[¶](#show-the-precedence-of-logical-operators "Link to this heading")

The following examples show the precedence of the logical operators.

The first example shows that the precedence of AND is higher than the
precedence of OR. The query returns the rows that match these conditions:

* `b` equals `Down`.

OR

* `a` equals `8` AND `b` equals `Up`.

```
SELECT *
  FROM logical_test1
  WHERE b = 'Down' OR
        a = 8 AND b = 'Up';
```

Copy

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  2 | 25 | Down |
|  3 | 15 | Down |
+----+----+------+
```

You can use parentheses in the WHERE clause to change the precedence. For example,
the following query returns the rows that match these conditions:

* `b` equals `Down` OR `a` equals `8`.

AND

* `b` equals `Up`.

```
SELECT *
  FROM logical_test1
  WHERE (b = 'Down' OR a = 8) AND b = 'Up';
```

Copy

```
+----+---+----+
| ID | A | B  |
|----+---+----|
|  1 | 8 | Up |
+----+---+----+
```

The next example shows that the precedence of NOT is higher than the precedence of AND. For example,
the following query returns the rows that match these conditions:

* `a` does NOT equal `15`.

AND

* `b` equals `Down`.

```
SELECT *
  FROM logical_test1
  WHERE NOT a = 15 AND b = 'Down';
```

Copy

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  2 | 25 | Down |
+----+----+------+
```

You can use parentheses in the WHERE clause to change the precedence. For example,
the following query returns the rows that do NOT match both of these conditions:

* `a` equals `15`.

AND

* `b` equals `Down`.

```
SELECT *
  FROM logical_test1
  WHERE NOT (a = 15 AND b = 'Down');
```

Copy

```
+----+----+------+
| ID |  A | B    |
|----+----+------|
|  1 |  8 | Up   |
|  2 | 25 | Down |
|  4 | 47 | Up   |
+----+----+------+
```

### Use logical operators in queries on Boolean values[¶](#use-logical-operators-in-queries-on-boolean-values "Link to this heading")

Create a table and insert data:

```
CREATE OR REPLACE TABLE logical_test2 (a BOOLEAN, b BOOLEAN);

INSERT INTO logical_test2 VALUES (0, 1);

SELECT * FROM logical_test2;
```

Copy

```
+-------+------+
| A     | B    |
|-------+------|
| False | True |
+-------+------+
```

The following query uses the OR operator to return rows where either `a` or `b`
is TRUE:

```
SELECT a, b FROM logical_test2 WHERE a OR b;
```

Copy

```
+-------+------+
| A     | B    |
|-------+------|
| False | True |
+-------+------+
```

The following query uses the AND operator to return rows where both `a` and `b`
are both TRUE:

```
SELECT a, b FROM logical_test2 WHERE a AND b;
```

Copy

```
+---+---+
| A | B |
|---+---|
+---+---+
```

The following query uses the AND operator and the NOT operator to return rows where
`b` is TRUE and `a` is FALSE:

```
SELECT a, b FROM logical_test2 WHERE b AND NOT a;
```

Copy

```
+-------+------+
| A     | B    |
|-------+------|
| False | True |
+-------+------+
```

The following query uses the AND operator and the NOT operator to return rows where
`a` is TRUE and `b` is FALSE:

```
SELECT a, b FROM logical_test2 WHERE a AND NOT b;
```

Copy

```
+---+---+
| A | B |
|---+---|
+---+---+
```

### Show “truth tables” for the logical operators[¶](#show-truth-tables-for-the-logical-operators "Link to this heading")

The next few examples show “truth tables” for the logical operators on a Boolean column. For more information about the
behavior of Boolean values in Snowflake, see [Ternary logic](ternary-logic).

Create a new table and data:

```
CREATE OR REPLACE TABLE logical_test3 (x BOOLEAN);

INSERT INTO logical_test3 (x) VALUES
  (False),
  (True),
  (NULL);
```

Copy

This shows the truth table for the OR operator:

```
SELECT x AS "OR",
       x OR False AS "FALSE",
       x OR True AS "TRUE",
       x OR NULL AS "NULL"
  FROM logical_test3;
```

Copy

```
+-------+-------+------+------+
| OR    | FALSE | TRUE | NULL |
|-------+-------+------+------|
| False | False | True | NULL |
| True  | True  | True | True |
| NULL  | NULL  | True | NULL |
+-------+-------+------+------+
```

This shows the truth table for the AND operator:

```
SELECT x AS "AND",
       x AND False AS "FALSE",
       x AND True AS "TRUE",
       x AND NULL AS "NULL"
  FROM logical_test3;
```

Copy

```
+-------+-------+-------+-------+
| AND   | FALSE | TRUE  | NULL  |
|-------+-------+-------+-------|
| False | False | False | False |
| True  | False | True  | NULL  |
| NULL  | False | NULL  | NULL  |
+-------+-------+-------+-------+
```

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [List of logical operators](#list-of-logical-operators)
2. [Examples](#examples)
3. [Use logical operators in queries on table data](#use-logical-operators-in-queries-on-table-data)
4. [Use logical operators in queries on Boolean values](#use-logical-operators-in-queries-on-boolean-values)
5. [Show “truth tables” for the logical operators](#show-truth-tables-for-the-logical-operators)