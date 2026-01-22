---
auto_generated: true
description: 'SELECT can be used as either a statement or as a clause within other
  statements:'
last_scraped: '2026-01-14T16:55:00.374128+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/select
title: SELECT | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)

     + [SELECT](select.md)
     + [WITH](../constructs/with.md)
     + [TOP <n>](../constructs/top_n.md)
     + [INTO](../constructs/into.md)
     + [FROM](../constructs/from.md)
     + [AT](../constructs/at-before.md)
     + [BEFORE](../constructs/at-before.md)
     + [CHANGES](../constructs/changes.md)
     + [CONNECT BY](../constructs/connect-by.md)
     + [JOIN](../constructs/join.md)
     + [ASOF JOIN](../constructs/asof-join.md)
     + [LATERAL](../constructs/join-lateral.md)
     + [MATCH\_RECOGNIZE](../constructs/match_recognize.md)
     + [PIVOT](../constructs/pivot.md)
     + [UNPIVOT](../constructs/unpivot.md)
     + [VALUES](../constructs/values.md)
     + [SAMPLE / TABLESAMPLE](../constructs/sample.md)
     + [RESAMPLE](../constructs/resample.md)
     + [SEMANTIC\_VIEW](../constructs/semantic_view.md)
     + [WHERE](../constructs/where.md)
     + [GROUP BY](../constructs/group-by.md)
     + [GROUP BY CUBE](../constructs/group-by-cube.md)
     + [GROUP BY GROUPING SETS](../constructs/group-by-grouping-sets.md)
     + [GROUP BY ROLLUP](../constructs/group-by-rollup.md)
     + [HAVING](../constructs/having.md)
     + [QUALIFY](../constructs/qualify.md)
     + [ORDER BY](../constructs/order-by.md)
     + [LIMIT](../constructs/limit.md)
     + [FETCH](../constructs/limit.md)
     + [FOR UPDATE](../constructs/for-update.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)
   * [General DML](../sql-dml.md)
   * [All commands (alphabetical)](../sql-all.md)")
   * [Accounts](../commands-account.md)
   * [Users, roles, & privileges](../commands-user-role.md)
   * [Integrations](../commands-integration.md)
   * [Business continuity & disaster recovery](../commands-replication.md)
   * [Sessions](../commands-session.md)
   * [Transactions](../commands-transaction.md)
   * [Virtual warehouses & resource monitors](../commands-warehouse.md)
   * [Databases, schemas, & shares](../commands-database.md)
   * [Tables, views, & sequences](../commands-table.md)
   * [Functions, procedures, & scripting](../commands-function.md)
   * [Streams & tasks](../commands-stream.md)
   * [dbt Projects on Snowflake](../commands-dbt-projects-on-snowflake.md)
   * [Classes & instances](../commands-class.md)
   * [Machine learning](../commands-ml.md)
   * [Cortex](../commands-cortex.md)
   * [Listings](../commands-listings.md)
   * [Openflow data plane integration](../commands-ofdata-plane.md)
   * [Organization profiles](../commands-organization-profiles.md)
   * [Security](../commands-security.md)
   * [Data Governance](../commands-data-governance.md)
   * [Privacy](../commands-privacy.md)
   * [Data loading & unloading](../commands-data-loading.md)
   * [File staging](../commands-file.md)
   * [Storage lifecycle policies](../commands-storage-lifecycle-policies.md)
   * [Git](../commands-git.md)
   * [Alerts](../commands-alert.md)
   * [Native Apps Framework](../commands-native-apps.md)
   * [Streamlit](../commands-streamlit.md)
   * [Notebook](../commands-notebook.md)
   * [Snowpark Container Services](../commands-snowpark-container-services.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)SELECT

# SELECT[¶](#select "Link to this heading")

SELECT can be used as either a statement or as a clause within other statements:

* As a statement, the SELECT statement is the most commonly executed SQL statement; it queries the database and retrieves a set of rows.
* As a clause, SELECT defines the set of columns returned by a query.

See also:
:   [Query syntax](../constructs)

## Syntax[¶](#syntax "Link to this heading")

The following sections describe the syntax for this command:

* [Selecting all columns](#label-select-cmd-syntax-all-columns)
* [Selecting specific columns](#label-select-cmd-syntax-selected-columns)

### Selecting all columns[¶](#selecting-all-columns "Link to this heading")

```
[ ... ]
SELECT [ { ALL | DISTINCT } ]
       [ TOP <n> ]
       [{<object_name>|<alias>}.]*

       [ ILIKE '<pattern>' ]

       [ EXCLUDE
         {
           <col_name> | ( <col_name>, <col_name>, ... )
         }
       ]

       [ REPLACE
         {
           ( <expr> AS <col_name> [ , <expr> AS <col_name>, ... ] )
         }
       ]

       [ RENAME
         {
           <col_name> AS <col_alias>
           | ( <col_name> AS <col_alias>, <col_name> AS <col_alias>, ... )
         }
       ]
```

Copy

You can specify the following combinations of keywords after SELECT \*. The keywords must be in the order shown below:

```
SELECT * ILIKE ... REPLACE ...
```

Copy

```
SELECT * ILIKE ... RENAME ...
```

Copy

```
SELECT * ILIKE ... REPLACE ... RENAME ...
```

Copy

```
SELECT * EXCLUDE ... REPLACE ...
```

Copy

```
SELECT * EXCLUDE ... RENAME ...
```

Copy

```
SELECT * EXCLUDE ... REPLACE ... RENAME ...
```

Copy

```
SELECT * REPLACE ... RENAME ...
```

Copy

### Selecting specific columns[¶](#selecting-specific-columns "Link to this heading")

```
[ ... ]
SELECT [ { ALL | DISTINCT } ]
       [ TOP <n> ]
       {
         [{<object_name>|<alias>}.]<col_name>
         | [{<object_name>|<alias>}.]$<col_position>
         | <expr>
       }
       [ [ AS ] <col_alias> ]
       [ , ... ]
[ ... ]
```

Copy

A trailing comma is supported in a column list. For example, the following SELECT statement is supported:

```
SELECT emp_id,
       name,
       dept,
  FROM employees;
```

Copy

For more information about SELECT as a statement and the other clauses within the statement, see
[Query syntax](../constructs).

## Parameters[¶](#parameters "Link to this heading")

`ALL | DISTINCT`
:   Specifies whether to perform duplicate elimination on the result set:

    * `ALL` includes all values in the result set.
    * `DISTINCT` eliminates duplicate values from the result set.

    Default: `ALL`

`TOP n`
:   Specifies the maximum number of results to return. See [TOP <n>](../constructs/top_n).

`object_name` or . `alias`
:   Specifies the object identifier or object alias as defined in the [FROM](../constructs/from) clause.

`*`
:   The asterisk is shorthand to indicate that the output should include all columns of the specified object, or all columns of
    all objects if `*` is not qualified with an object name or alias. The columns are returned in the order shown by
    executing the [DESCRIBE](desc) command on the object.

    When you specify `*`, you can also specify `ILIKE`, `EXCLUDE`, `REPLACE`, and `RENAME`:

    `ILIKE 'pattern'`
    :   Specifies that only the columns that match `pattern` should be included in the results.

        In `pattern`, you can use the following SQL wildcards:

        * Use an underscore (`_`) to match any single character.
        * Use a percent sign (`%`) to match any sequence of zero or more characters.

        To match a sequence anywhere within the column name, begin and end the pattern with `%`.

        Matching is case-insensitive.

        If no columns match the specified pattern, a compilation error occurs (`001080 (42601): ... SELECT with no columns`).

    `EXCLUDE col_name` . `EXCLUDE (col_name, col_name, ...)`
    :   Specifies the columns that should be excluded from the results.

        If you are selecting from multiple tables, use `SELECT table_name.*` to specify that you want to select all columns
        from a specific table, and specify the unqualified column name in `EXCLUDE`. For example:

        ```
        SELECT table_a.* EXCLUDE column_in_table_a ,
          table_b.* EXCLUDE column_in_table_b
          ...
        ```

        Copy

    `REPLACE (expr AS col_name [ , expr AS col_name, ...] )`
    :   Replaces the value of `col_name` with the value of the evaluated expression `expr`.

        For example, to prepend the string `'DEPT-'` to the values in the `department_id` column, use:

        ```
        SELECT * REPLACE ('DEPT-' || department_id AS department_id) ...
        ```

        Copy

        For `col_name`:

        * The column must exist and cannot be filtered out by `ILIKE` or `EXCEPT`.
        * You cannot specify the same column more than once in the list of replacements.
        * If the column is in multiple tables (for example, in both tables in a join), the statement fails with an “ambiguous column”
          error.

        `expr` must evaluate to a single value.

    `RENAME col_name AS col_alias` . `RENAME (col_name AS col_alias, col_name AS col_alias, ...)`
    :   Specifies the column aliases that should be used in the results.

        If you are selecting from multiple tables, use `SELECT table_name.*` to specify that you want to select all columns
        from a specific table, and specify the unqualified column name in `RENAME`. For example:

        ```
        SELECT table_a.* RENAME column_in_table_a AS col_alias_a,
          table_b.* RENAME column_in_table_b AS col_alias_b
          ...
        ```

        Copy

    Note

    When specifying a combination of keywords after `SELECT *`:

    * You cannot specify both `ILIKE` and `EXCLUDE`.
    * If you specify `EXCLUDE` with `RENAME` or `REPLACE`:

      + You must specify `EXCLUDE` before `RENAME` or `REPLACE`:

        ```
        SELECT * EXCLUDE col_a RENAME col_b AS alias_b ...
        ```

        Copy

        ```
        SELECT * EXCLUDE employee_id REPLACE ('DEPT-' || department_id AS department_id) ...
        ```

        Copy
      + You cannot specify the same column in `EXCLUDE` and `RENAME`.
    * If you specify `ILIKE` with `RENAME` or `REPLACE`, you must specify `ILIKE` first:

      ```
      SELECT * ILIKE '%id%' RENAME department_id AS department ...
      ```

      Copy

      ```
      SELECT * ILIKE '%id%' REPLACE ('DEPT-' || department_id AS department_id) ...
      ```

      Copy
    * If you specify `REPLACE` and `RENAME`:

      + You must specify `REPLACE` first:

        ```
        SELECT * REPLACE ('DEPT-' || department_id AS department_id) RENAME employee_id as employee ...
        ```

        Copy
      + You can specify the same column name in `REPLACE` and `RENAME`:

        ```
        SELECT * REPLACE ('DEPT-' || department_id AS department_id) RENAME department_id as department ...
        ```

        Copy

`col_name`
:   Specifies the column identifier as defined in the [FROM](../constructs/from) clause.

`$col_position`
:   Specifies the position of the column (1-based) as defined in the [FROM](../constructs/from) clause. If a column is
    referenced from a table, this number can’t exceed the maximum number of columns in the table.

`expr`
:   Specifies an expression, such as a mathematical expression, that evaluates
    to a specific value for any given row.

`[ AS ] col_alias`
:   Specifies the column alias assigned to the resulting expression. This is used as the display name in a top-level SELECT list, and the column name in an inline view.

    Do not assign a column alias that is the same as the name of another column referenced in the query.
    For example, if you are selecting columns named `prod_id` and `product_id`, do not alias `prod_id` as `product_id`.
    See [Error case: Specifying an alias that matches another column name](#label-select-cmd-examples-matching-column-alias).

## Usage notes[¶](#usage-notes "Link to this heading")

* Aliases and identifiers are case-insensitive by default. To preserve case, enclose them within double quotes (`"`). For more
  information, see [Object identifiers](../identifiers).
* Without an ORDER BY clause, the results returned by SELECT are an unordered set. Running the same query repeatedly against the
  same tables might result in a different output order every time. If order matters, use the `ORDER BY` clause.
* SELECT can be used not only as an independent statement, but also as a clause in other statements, for example
  `INSERT INTO ... SELECT ...;`. SELECT can also be used in a
  [subquery](../../user-guide/querying-subqueries) within a statement.
* In many cases, when you use a column alias for an expression (i.e. `expr AS col_alias`) in other parts of the same
  query (in JOIN, FROM, WHERE, GROUP BY, other column expressions, etc.), the expression is evaluated only once.

  However, note that in some cases, the expression can be evaluated multiple times, which can result in different values for the
  alias used in different parts of the same query.

## Examples[¶](#examples "Link to this heading")

A few simple examples are provided below.

* [Setting up the data for the examples](#label-select-cmd-examples-data-setup)
* [Examples of selecting all columns (SELECT \*)](#label-select-cmd-examples-select-all)
* [Examples of selecting specific columns (SELECT colname)](#label-select-cmd-examples-select-specific)

Many additional examples are included in other parts of the documentation, including the detailed descriptions of
[Query syntax](../constructs).

For examples related to querying an event table (whose schema is predefined by Snowflake), refer to
[Viewing log messages](../../developer-guide/logging-tracing/logging-accessing-messages) and [Viewing trace data](../../developer-guide/logging-tracing/tracing-accessing-events).

### Setting up the data for the examples[¶](#setting-up-the-data-for-the-examples "Link to this heading")

Some of the queries below use the following tables and data:

> ```
> CREATE TABLE employee_table (
>     employee_ID INTEGER,
>     last_name VARCHAR,
>     first_name VARCHAR,
>     department_ID INTEGER
>     );
>
> CREATE TABLE department_table (
>     department_ID INTEGER,
>     department_name VARCHAR
>     );
> ```
>
> Copy
>
> ```
> INSERT INTO employee_table (employee_ID, last_name, first_name, department_ID) VALUES
>     (101, 'Montgomery', 'Pat', 1),
>     (102, 'Levine', 'Terry', 2),
>     (103, 'Comstock', 'Dana', 2);
>
> INSERT INTO department_table (department_ID, department_name) VALUES
>     (1, 'Engineering'),
>     (2, 'Customer Support'),
>     (3, 'Finance');
> ```
>
> Copy

### Examples of selecting all columns (SELECT \*)[¶](#examples-of-selecting-all-columns-select "Link to this heading")

* [Selecting all columns in the table](#label-select-cmd-examples-select-all-in-table)
* [Selecting all columns with names that match a pattern](#label-select-cmd-examples-select-all-in-table-matching)
* [Selecting all columns except one column](#label-select-cmd-examples-select-all-in-table-but-one)
* [Selecting all columns except two or more columns](#label-select-cmd-examples-select-all-in-table-but-two)
* [Selecting all columns and renaming one column](#label-select-cmd-examples-select-all-in-table-rename-one)
* [Selecting all columns and renaming multiple columns](#label-select-cmd-examples-select-all-in-table-rename-two)
* [Selecting all columns with names that match a pattern and renaming a column](#label-select-cmd-examples-select-all-in-table-matching-rename)
* [Selecting all columns, excluding a column, and renaming multiple columns](#label-select-cmd-examples-select-all-in-table-exclude-rename)
* [Selecting all columns and replacing the value of a column](#label-select-cmd-examples-select-all-in-table-replace)
* [Selecting all columns, replacing the value of a column, and renaming the column](#label-select-cmd-examples-select-all-in-table-replace-rename)
* [Selecting all columns with names that match a pattern and replacing the value in a column](#label-select-cmd-examples-select-all-in-table-matching-replace)
* [Selecting all columns from multiple tables, excluding a column, and renaming a column](#label-select-cmd-examples-select-all-multiple-tables)

#### Selecting all columns in the table[¶](#selecting-all-columns-in-the-table "Link to this heading")

This example shows how to select all columns in `employee_table`:

```
SELECT * FROM employee_table;
```

Copy

```
+-------------+------------+------------+---------------+
| EMPLOYEE_ID | LAST_NAME  | FIRST_NAME | DEPARTMENT_ID |
|-------------+------------+------------+---------------|
|         101 | Montgomery | Pat        |             1 |
|         102 | Levine     | Terry      |             2 |
|         103 | Comstock   | Dana       |             2 |
+-------------+------------+------------+---------------+
```

#### Selecting all columns with names that match a pattern[¶](#selecting-all-columns-with-names-that-match-a-pattern "Link to this heading")

This example shows how to select all columns in `employee_table` with names that contain `id`:

```
SELECT * ILIKE '%id%' FROM employee_table;
```

Copy

```
+-------------+---------------+
| EMPLOYEE_ID | DEPARTMENT_ID |
|-------------+---------------|
|         101 |             1 |
|         102 |             2 |
|         103 |             2 |
+-------------+---------------+
```

#### Selecting all columns except one column[¶](#selecting-all-columns-except-one-column "Link to this heading")

This example shows how to select all columns in `employee_table` except for the `department_id` column:

```
SELECT * EXCLUDE department_id FROM employee_table;
```

Copy

```
+-------------+------------+------------+
| EMPLOYEE_ID | LAST_NAME  | FIRST_NAME |
|-------------+------------+------------|
|         101 | Montgomery | Pat        |
|         102 | Levine     | Terry      |
|         103 | Comstock   | Dana       |
+-------------+------------+------------+
```

#### Selecting all columns except two or more columns[¶](#selecting-all-columns-except-two-or-more-columns "Link to this heading")

This example shows how to select all columns in `employee_table` except for the `department_id` and `employee_id` columns:

```
SELECT * EXCLUDE (department_id, employee_id) FROM employee_table;
```

Copy

```
+------------+------------+
| LAST_NAME  | FIRST_NAME |
|------------+------------|
| Montgomery | Pat        |
| Levine     | Terry      |
| Comstock   | Dana       |
+------------+------------+
```

#### Selecting all columns and renaming one column[¶](#selecting-all-columns-and-renaming-one-column "Link to this heading")

This example shows how to select all columns in `employee_table` and rename the `department_id` column:

```
SELECT * RENAME department_id AS department FROM employee_table;
```

Copy

```
+-------------+------------+------------+------------+
| EMPLOYEE_ID | LAST_NAME  | FIRST_NAME | DEPARTMENT |
|-------------+------------+------------+------------|
|         101 | Montgomery | Pat        |          1 |
|         102 | Levine     | Terry      |          2 |
|         103 | Comstock   | Dana       |          2 |
+-------------+------------+------------+------------+
```

#### Selecting all columns and renaming multiple columns[¶](#selecting-all-columns-and-renaming-multiple-columns "Link to this heading")

This example shows how to select all columns in `employee_table` and rename the `department_id` and `employee_id` columns:

```
SELECT * RENAME (department_id AS department, employee_id AS id) FROM employee_table;
```

Copy

```
+-----+------------+------------+------------+
|  ID | LAST_NAME  | FIRST_NAME | DEPARTMENT |
|-----+------------+------------+------------|
| 101 | Montgomery | Pat        |          1 |
| 102 | Levine     | Terry      |          2 |
| 103 | Comstock   | Dana       |          2 |
+-----+------------+------------+------------+
```

#### Selecting all columns, excluding a column, and renaming multiple columns[¶](#selecting-all-columns-excluding-a-column-and-renaming-multiple-columns "Link to this heading")

This example shows how to select all columns in `employee_table`, exclude the `first_name` column, and rename the
`department_id` and `employee_id` columns:

```
SELECT * EXCLUDE first_name RENAME (department_id AS department, employee_id AS id) FROM employee_table;
```

Copy

```
+-----+------------+------------+
|  ID | LAST_NAME  | DEPARTMENT |
|-----+------------+------------|
| 101 | Montgomery |          1 |
| 102 | Levine     |          2 |
| 103 | Comstock   |          2 |
+-----+------------+------------+
```

#### Selecting all columns with names that match a pattern and renaming a column[¶](#selecting-all-columns-with-names-that-match-a-pattern-and-renaming-a-column "Link to this heading")

This example shows how to select all columns in `employee_table` with names that contain `id` and rename the
`department_id` column:

```
SELECT * ILIKE '%id%' RENAME department_id AS department FROM employee_table;
```

Copy

```
+-------------+------------+
| EMPLOYEE_ID | DEPARTMENT |
|-------------+------------|
|         101 |          1 |
|         102 |          2 |
|         103 |          2 |
+-------------+------------+
```

#### Selecting all columns and replacing the value of a column[¶](#selecting-all-columns-and-replacing-the-value-of-a-column "Link to this heading")

This example shows how to select all columns in `employee_table` and replace the value in the `department_id` column with
the ID prepended with `DEPT-`:

```
SELECT * REPLACE ('DEPT-' || department_id AS department_id) FROM employee_table;
```

Copy

```
+-------------+------------+------------+---------------+
| EMPLOYEE_ID | LAST_NAME  | FIRST_NAME | DEPARTMENT_ID |
|-------------+------------+------------+---------------|
|         101 | Montgomery | Pat        | DEPT-1        |
|         102 | Levine     | Terry      | DEPT-2        |
|         103 | Comstock   | Dana       | DEPT-2        |
+-------------+------------+------------+---------------+
```

#### Selecting all columns, replacing the value of a column, and renaming the column[¶](#selecting-all-columns-replacing-the-value-of-a-column-and-renaming-the-column "Link to this heading")

This example shows how to select all columns in `employee_table`, replace the value in the `department_id` column with
the ID prepended with `DEPT-`, and rename the column:

```
SELECT * REPLACE ('DEPT-' || department_id AS department_id) RENAME department_id AS department FROM employee_table;
```

Copy

```
+-------------+------------+------------+------------+
| EMPLOYEE_ID | LAST_NAME  | FIRST_NAME | DEPARTMENT |
|-------------+------------+------------+------------|
|         101 | Montgomery | Pat        | DEPT-1     |
|         102 | Levine     | Terry      | DEPT-2     |
|         103 | Comstock   | Dana       | DEPT-2     |
+-------------+------------+------------+------------+
```

#### Selecting all columns with names that match a pattern and replacing the value in a column[¶](#selecting-all-columns-with-names-that-match-a-pattern-and-replacing-the-value-in-a-column "Link to this heading")

This example shows how to select all columns in `employee_table` with names that contain `id` and prepending `DEPT-` to the
values in the `department_id` column:

```
SELECT * ILIKE '%id%' REPLACE('DEPT-' || department_id AS department_id) FROM employee_table;
```

Copy

```
+-------------+---------------+
| EMPLOYEE_ID | DEPARTMENT_ID |
|-------------+---------------|
|         101 | DEPT-1        |
|         102 | DEPT-2        |
|         103 | DEPT-2        |
+-------------+---------------+
```

#### Selecting all columns from multiple tables, excluding a column, and renaming a column[¶](#selecting-all-columns-from-multiple-tables-excluding-a-column-and-renaming-a-column "Link to this heading")

This example joins two tables and selects all columns from both tables except one column from `employee_table`. The example also
renames one of the columns selected from `department_table`.

```
SELECT
  employee_table.* EXCLUDE department_id,
  department_table.* RENAME department_name AS department
FROM employee_table INNER JOIN department_table
  ON employee_table.department_id = department_table.department_id
ORDER BY department, last_name, first_name;
```

Copy

```
+-------------+------------+------------+---------------+------------------+
| EMPLOYEE_ID | LAST_NAME  | FIRST_NAME | DEPARTMENT_ID | DEPARTMENT       |
|-------------+------------+------------+---------------+------------------|
|         103 | Comstock   | Dana       |             2 | Customer Support |
|         102 | Levine     | Terry      |             2 | Customer Support |
|         101 | Montgomery | Pat        |             1 | Engineering      |
+-------------+------------+------------+---------------+------------------+
```

### Examples of selecting specific columns (SELECT colname)[¶](#examples-of-selecting-specific-columns-select-colname "Link to this heading")

* [Selecting a single column by name](#label-select-cmd-examples-select-specific-col-by-name)
* [Selecting multiple columns by name from joined tables](#label-select-cmd-examples-select-specific-multiple-col-by-name)
* [Selecting a column by position](#label-select-cmd-examples-select-specific-col-by-position)
* [Specifying an alias for a column in the output](#label-select-cmd-examples-select-specific-col-alias)
* [Error case: Specifying an alias that matches another column name](#label-select-cmd-examples-matching-column-alias)

#### Selecting a single column by name[¶](#selecting-a-single-column-by-name "Link to this heading")

This example shows how to look up an employee’s last name if you know their ID.

```
SELECT last_name FROM employee_table WHERE employee_ID = 101;
+------------+
| LAST_NAME  |
|------------|
| Montgomery |
+------------+
```

Copy

#### Selecting multiple columns by name from joined tables[¶](#selecting-multiple-columns-by-name-from-joined-tables "Link to this heading")

This example lists each employee and the name of the department that each employee works in. The output is in order by department
name, and within each department the employees are in order by name. This query uses a join to relate the information in one table
to the information in another table.

```
SELECT department_name, last_name, first_name
    FROM employee_table INNER JOIN department_table
        ON employee_table.department_ID = department_table.department_ID
    ORDER BY department_name, last_name, first_name;
+------------------+------------+------------+
| DEPARTMENT_NAME  | LAST_NAME  | FIRST_NAME |
|------------------+------------+------------|
| Customer Support | Comstock   | Dana       |
| Customer Support | Levine     | Terry      |
| Engineering      | Montgomery | Pat        |
+------------------+------------+------------+
```

Copy

#### Selecting a column by position[¶](#selecting-a-column-by-position "Link to this heading")

This example shows how to use `$` to specify a column by column number, rather than by column name:

```
SELECT $2 FROM employee_table ORDER BY $2;
+------------+
| $2         |
|------------|
| Comstock   |
| Levine     |
| Montgomery |
+------------+
```

Copy

#### Specifying an alias for a column in the output[¶](#specifying-an-alias-for-a-column-in-the-output "Link to this heading")

This example shows that the output columns do not need to be taken directly from the tables in the `FROM` clause; the output columns
can be general expressions. This example calculates the area of a circle that has a radius of 2.0. This example also shows how to use
a column alias so that the output has a meaningful column name:

```
SELECT pi() * 2.0 * 2.0 AS area_of_circle;
+----------------+
| AREA_OF_CIRCLE |
|----------------|
|   12.566370614 |
+----------------+
```

Copy

#### Error case: Specifying an alias that matches another column name[¶](#error-case-specifying-an-alias-that-matches-another-column-name "Link to this heading")

This example demonstrates why it is not recommended to use a column alias that matches
the name of another column that is used in the query. This GROUP BY query results in a
SQL compiler error, not an ambiguous column error.
The alias `prod_id` that is assigned to `product_id` in `table1` matches the name
of the `prod_id` column in `table2`. The simplest solution to this error is to give
the column a different alias.

```
CREATE OR REPLACE TABLE table1 (product_id NUMBER);

CREATE OR REPLACE TABLE table2 (prod_id NUMBER);

SELECT t1.product_id AS prod_id, t2.prod_id
  FROM table1 AS t1 JOIN table2 AS t2
    ON t1.product_id=t2.prod_id
  GROUP BY prod_id, t2.prod_id;
```

Copy

```
001104 (42601): SQL compilation error: error line 1 at position 7
'T1.PRODUCT_ID' in select clause is neither an aggregate nor in the group by clause.
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

1. [Syntax](#syntax)
2. [Parameters](#parameters)
3. [Usage notes](#usage-notes)
4. [Examples](#examples)