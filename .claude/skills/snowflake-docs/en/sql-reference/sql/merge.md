---
auto_generated: true
description: Inserts, updates, and deletes values in a table that are based on values
  in a second table or a subquery. Merging can be useful if the second table is a
  change log that contains new rows (to be insert
last_scraped: '2026-01-14T16:54:59.928938+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/merge
title: MERGE | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)
   * [General DML](../sql-dml.md)

     + [INSERT](insert.md)
     + [MERGE](merge.md)
     + [UPDATE](update.md)
     + [DELETE](delete.md)
     + [TRUNCATE](truncate-table.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[General DML](../sql-dml.md)MERGE

# MERGE[¶](#merge "Link to this heading")

Inserts, updates, and deletes values in a table that are based on values in a second table or a subquery. Merging can be
useful if the second table is a change log that contains new rows (to be inserted), modified rows (to be updated),
or marked rows (to be deleted) in the target table.

The command supports semantics for handling the following cases:

* Values that match (for updates and deletes).
* Values that don’t match (for inserts).

See also:
:   [DELETE](delete) , [UPDATE](update)

## Syntax[¶](#syntax "Link to this heading")

```
MERGE INTO <target_table>
  USING <source>
  ON <join_expr>
  { matchedClause | notMatchedClause } [ ... ]
```

Copy

Where:

> ```
> matchedClause ::=
>   WHEN MATCHED
>     [ AND <case_predicate> ]
>     THEN { UPDATE { ALL BY NAME | SET <col_name> = <expr> [ , <col_name> = <expr> ... ] } | DELETE } [ ... ]
> ```
>
> Copy
>
> ```
> notMatchedClause ::=
>    WHEN NOT MATCHED
>      [ AND <case_predicate> ]
>      THEN INSERT { ALL BY NAME | [ ( <col_name> [ , ... ] ) ] VALUES ( <expr> [ , ... ] ) }
> ```
>
> Copy

## Parameters[¶](#parameters "Link to this heading")

`target_table`
:   Specifies the table to merge.

`source`
:   Specifies the table or subquery to join with the target table.

`join_expr`
:   Specifies the expression on which to join the target table and source.

### `matchedClause` (for updates or deletes)[¶](#matchedclause-for-updates-or-deletes "Link to this heading")

`WHEN MATCHED ... AND case_predicate`
:   Optionally specifies an expression which, when true, causes the matching case to be executed.

    Default: No value (matching case is always executed)

`WHEN MATCHED ... THEN { UPDATE { ALL BY NAME | SET ... } | DELETE }`
:   Specifies the action to perform when the values match.

    `ALL BY NAME`
    :   Updates all columns in the target table with values from the source. Each column in
        the target table is updated with the values of the column with the same name from the source.

        The target table and source must have the same number of columns and the same names for all of the
        columns. However, the column order can be different between the target table and the source.

    `SET col_name = expr [ , col_name = expr ... ]`
    :   Updates the specified column in the target table by using the corresponding expression for the new column
        value (can refer to both the target and source relations).

        In a single `SET` subclause, you can specify multiple columns to update.

    `DELETE`
    :   Deletes the rows in the target table when they match the source.

### `notMatchedClause` (for inserts)[¶](#notmatchedclause-for-inserts "Link to this heading")

`WHEN NOT MATCHED ... AND case_predicate`
:   Optionally specifies an expression which, when true, causes the not-matching case to be executed.

    Default: No value (not-matching case is always executed)

`WHEN NOT MATCHED ... THEN INSERT` . `{ ALL BY NAME | [ ( col_name [ , ... ] ) ] VALUES ( expr [ , ... ] ) }`
:   Specifies the action to perform when the values don’t match.

    `ALL BY NAME`
    :   Inserts all columns in the target table with values from the source. Each column in
        the target table is inserted with the values of the column with the same name from the source.

        The target table and source must have the same number of columns and the same names for all of the
        columns. However, the column order can be different between the target table and the source.

    `( col_name [ , ... ] )`
    :   Optionally specifies one or more columns in the target table to be inserted with values from the source.

        Default: No value (all columns in the target table are inserted)

    `VALUES ( expr [ , ... ] )`
    :   Specifies the corresponding expressions for the inserted column values (must refer to the source relations).

## Usage notes[¶](#usage-notes "Link to this heading")

* A single MERGE statement can include multiple matching and not-matching clauses (that is, `WHEN MATCHED ...` and
  `WHEN NOT MATCHED ...`).
* Any matching or not-matching clause that omits the `AND` subclause (default behavior) must be the last of its clause
  type in the statement (for example, a `WHEN MATCHED ...` clause can’t be followed by a `WHEN MATCHED AND ...` clause). Doing
  so results in an unreachable case, which returns an error.

## Duplicate join behavior[¶](#duplicate-join-behavior "Link to this heading")

When multiple rows in the source table match a single row in the target table, the results can be deterministic or nondeterministic.
This section describes MERGE behavior for these use cases.

### Nondeterministic results for UPDATE and DELETE[¶](#nondeterministic-results-for-update-and-delete "Link to this heading")

When a merge joins a row in the target table against multiple rows in the source, the following join conditions produce nondeterministic
results (that is, the system is unable to determine the source value to use to update or delete the target row):

* A target row is selected to be updated with multiple values (for example, `WHEN MATCHED ... THEN UPDATE`).
* A target row is selected to be both updated and deleted (for example, `WHEN MATCHED ... THEN UPDATE` , `WHEN MATCHED ... THEN DELETE`).

In this situation, the outcome of the merge depends on the value specified for the [ERROR\_ON\_NONDETERMINISTIC\_MERGE](../parameters.html#label-error-on-nondeterministic-merge) session
parameter:

* If TRUE (default value), the merge returns an error.
* If FALSE, one row from among the duplicates is selected to perform the update or delete; the row selected is not defined.

### Deterministic results for UPDATE and DELETE[¶](#deterministic-results-for-update-and-delete "Link to this heading")

Deterministic merges always complete without error. A merge is deterministic if it meets *at least one* of the following conditions
for each target row:

* One or more source rows satisfy the `WHEN MATCHED ... THEN DELETE` clauses, and no other source rows satisfy any
  `WHEN MATCHED` clauses
* Exactly one source row satisfies a `WHEN MATCHED ... THEN UPDATE` clause, and no other source rows satisfy any
  `WHEN MATCHED` clauses.

This makes MERGE semantically equivalent to the [UPDATE](update) and [DELETE](delete) commands.

Note

To avoid errors when multiple rows in the data source (that is, the source table or subquery) match the target table based on the ON
condition, use [GROUP BY](../constructs/group-by) in the source clause to ensure that each target row joins against one row
(at most) in the source.

In the following example, assume `src` includes multiple rows with the same `k` value. It’s ambiguous which values (`v`) will
be used to update rows in the target row with the same value of `k`. By using the MAX function and GROUP BY, the query clarifies exactly
which value of `v` from `src` is used:

```
MERGE INTO target
  USING (SELECT k, MAX(v) AS v FROM src GROUP BY k) AS b
  ON target.k = b.k
  WHEN MATCHED THEN UPDATE SET target.v = b.v
  WHEN NOT MATCHED THEN INSERT (k, v) VALUES (b.k, b.v);
```

Copy

### Deterministic results for INSERT[¶](#deterministic-results-for-insert "Link to this heading")

Deterministic merges always complete without error.

If the MERGE statement contains a `WHEN NOT MATCHED ... THEN INSERT` clause, and if there are no matching rows in the target, and if the
source contains duplicate values, then the target gets one copy of the row for *each* copy in the source. For an example,
see [Perform a merge with source duplicates](#label-merge-example-source-duplicates).

## Examples[¶](#examples "Link to this heading")

The following examples use the MERGE command:

* [Perform a basic merge that updates values](#label-merge-example-basic-updates)
* [Perform a basic merge with multiple operations](#label-merge-example-basic-multiple-operations)
* [Perform a merge by using ALL BY NAME](#label-merge-example-all)
* [Perform a merge with source duplicates](#label-merge-example-source-duplicates)
* [Perform a merge with deterministic and nondeterministic results](#label-merge-example-deterministic-nondeterministic)
* [Perform a merge based on DATE values](#label-merge-example-date-values)

### Perform a basic merge that updates values[¶](#perform-a-basic-merge-that-updates-values "Link to this heading")

The following example performs a basic merge that updates values in the target table by using values from the source
table. Create and load two tables:

```
CREATE OR REPLACE TABLE merge_example_target (id INTEGER, description VARCHAR);

INSERT INTO merge_example_target (id, description) VALUES
  (10, 'To be updated (this is the old value)');

CREATE OR REPLACE TABLE merge_example_source (id INTEGER, description VARCHAR);

INSERT INTO merge_example_source (id, description) VALUES
  (10, 'To be updated (this is the new value)');
```

Copy

Display the values in the tables:

```
SELECT * FROM merge_example_target;
```

Copy

```
+----+---------------------------------------+
| ID | DESCRIPTION                           |
|----+---------------------------------------|
| 10 | To be updated (this is the old value) |
+----+---------------------------------------+
```

```
SELECT * FROM merge_example_source;
```

Copy

```
+----+---------------------------------------+
| ID | DESCRIPTION                           |
|----+---------------------------------------|
| 10 | To be updated (this is the new value) |
+----+---------------------------------------+
```

Run the MERGE statement:

```
MERGE INTO merge_example_target
  USING merge_example_source
  ON merge_example_target.id = merge_example_source.id
  WHEN MATCHED THEN
    UPDATE SET merge_example_target.description = merge_example_source.description;
```

Copy

```
+------------------------+
| number of rows updated |
|------------------------|
|                      1 |
+------------------------+
```

Display the new values in the target table (the source table is unchanged):

```
SELECT * FROM merge_example_target;
```

Copy

```
+----+---------------------------------------+
| ID | DESCRIPTION                           |
|----+---------------------------------------|
| 10 | To be updated (this is the new value) |
+----+---------------------------------------+
```

```
SELECT * FROM merge_example_source;
```

Copy

```
+----+---------------------------------------+
| ID | DESCRIPTION                           |
|----+---------------------------------------|
| 10 | To be updated (this is the new value) |
+----+---------------------------------------+
```

### Perform a basic merge with multiple operations[¶](#perform-a-basic-merge-with-multiple-operations "Link to this heading")

Perform a basic merge with a mix of operations (INSERT, UPDATE, and DELETE).

Create and load two tables:

```
CREATE OR REPLACE TABLE merge_example_mult_target (
  id INTEGER,
  val INTEGER,
  status VARCHAR);

INSERT INTO merge_example_mult_target (id, val, status) VALUES
  (1, 10, 'Production'),
  (2, 20, 'Alpha'),
  (3, 30, 'Production');

CREATE OR REPLACE TABLE merge_example_mult_source (
  id INTEGER,
  marked VARCHAR,
  isnewstatus INTEGER,
  newval INTEGER,
  newstatus VARCHAR);

INSERT INTO merge_example_mult_source (id, marked, isnewstatus, newval, newstatus) VALUES
  (1, 'Y', 0, 10, 'Production'),
  (2, 'N', 1, 50, 'Beta'),
  (3, 'N', 0, 60, 'Deprecated'),
  (4, 'N', 0, 40, 'Production');
```

Copy

Display the values in the tables:

```
SELECT * FROM merge_example_mult_target;
```

Copy

```
+----+-----+------------+
| ID | VAL | STATUS     |
|----+-----+------------|
|  1 |  10 | Production |
|  2 |  20 | Alpha      |
|  3 |  30 | Production |
+----+-----+------------+
```

```
SELECT * FROM merge_example_mult_source;
```

Copy

```
+----+--------+-------------+--------+------------+
| ID | MARKED | ISNEWSTATUS | NEWVAL | NEWSTATUS  |
|----+--------+-------------+--------+------------|
|  1 | Y      |           0 |     10 | Production |
|  2 | N      |           1 |     50 | Beta       |
|  3 | N      |           0 |     60 | Deprecated |
|  4 | N      |           0 |     40 | Production |
+----+--------+-------------+--------+------------+
```

The following merge example performs the following actions on the `merge_example_mult_target` table:

* Deletes the row with `id` set to `1` because the `marked` column for the row with the same `id` is
  `Y` in `merge_example_mult_source`.
* Updates the `val` and `status` values in the row with `id` set to `2` with values in the row with the same
  `id` in `merge_example_mult_source`, because `isnewstatus` is set to `1` for the same row in
  `merge_example_mult_source`.
* Updates the `val` value in the row with `id` set to `3` with the value in the row with the same
  `id` in `merge_example_mult_source`. The MERGE statement doesn’t update the `status` value in `merge_example_mult_target`
  because `isnewstatus` is set to `0` for this row in `merge_example_mult_source`.
* Inserts the row with `id` set to `4` because the row exists in `merge_example_mult_source` and there is no
  matching row in `merge_example_mult_target`.

```
MERGE INTO merge_example_mult_target
  USING merge_example_mult_source
  ON merge_example_mult_target.id = merge_example_mult_source.id
  WHEN MATCHED AND merge_example_mult_source.marked = 'Y'
    THEN DELETE
  WHEN MATCHED AND merge_example_mult_source.isnewstatus = 1
    THEN UPDATE SET val = merge_example_mult_source.newval, status = merge_example_mult_source.newstatus
  WHEN MATCHED
    THEN UPDATE SET val = merge_example_mult_source.newval
  WHEN NOT MATCHED
    THEN INSERT (id, val, status) VALUES (
      merge_example_mult_source.id,
      merge_example_mult_source.newval,
      merge_example_mult_source.newstatus);
```

Copy

```
+-------------------------+------------------------+------------------------+
| number of rows inserted | number of rows updated | number of rows deleted |
|-------------------------+------------------------+------------------------|
|                       1 |                      2 |                      1 |
+-------------------------+------------------------+------------------------+
```

To see the results of the merge, display the values in the `merge_example_mult_target` table:

```
SELECT * FROM merge_example_mult_target ORDER BY id;
```

Copy

```
+----+-----+------------+
| ID | VAL | STATUS     |
|----+-----+------------|
|  2 |  50 | Beta       |
|  3 |  60 | Production |
|  4 |  40 | Production |
+----+-----+------------+
```

### Perform a merge by using ALL BY NAME[¶](#perform-a-merge-by-using-all-by-name "Link to this heading")

The following example performs a merge that inserts and updates values in the target table by using values from the
source table. The example uses the `WHEN MATCHED ... THEN ALL BY NAME` and
`WHEN NOT MATCHED ... THEN ALL BY NAME` subclauses to specify that the merge applies to all columns.

Create two tables with the same number of columns and the same names for the columns,
but with a different order for two of the columns:

```
CREATE OR REPLACE TABLE merge_example_target_all (
  id INTEGER,
  x INTEGER,
  y VARCHAR);

CREATE OR REPLACE TABLE merge_example_source_all (
  id INTEGER,
  y VARCHAR,
  x INTEGER);
```

Copy

Load the tables:

```
INSERT INTO merge_example_target_all (id, x, y) VALUES
  (1, 10, 'Skiing'),
  (2, 20, 'Snowboarding');

INSERT INTO merge_example_source_all (id, y, x) VALUES
  (1, 'Skiing', 10),
  (2, 'Snowboarding', 25),
  (3, 'Skating', 30);
```

Copy

Display the values in the tables:

```
SELECT * FROM merge_example_target_all;
```

Copy

```
+----+----+--------------+
| ID |  X | Y            |
|----+----+--------------|
|  1 | 10 | Skiing       |
|  2 | 20 | Snowboarding |
+----+----+--------------+
```

```
SELECT * FROM merge_example_source_all;
```

Copy

```
+----+--------------+----+
| ID | Y            |  X |
|----+--------------+----|
|  1 | Skiing       | 10 |
|  2 | Snowboarding | 25 |
|  3 | Skating      | 30 |
+----+--------------+----+
```

Run the MERGE statement:

```
MERGE INTO merge_example_target_all
  USING merge_example_source_all
  ON merge_example_target_all.id = merge_example_source_all.id
  WHEN MATCHED THEN
    UPDATE ALL BY NAME
  WHEN NOT MATCHED THEN
    INSERT ALL BY NAME;
```

Copy

```
+-------------------------+------------------------+
| number of rows inserted | number of rows updated |
|-------------------------+------------------------|
|                       1 |                      2 |
+-------------------------+------------------------+
```

Display the new values in the target table:

```
SELECT *
  FROM merge_example_target_all
  ORDER BY id;
```

Copy

```
+----+----+--------------+
| ID |  X | Y            |
|----+----+--------------|
|  1 | 10 | Skiing       |
|  2 | 25 | Snowboarding |
|  3 | 30 | Skating      |
+----+----+--------------+
```

### Perform a merge with source duplicates[¶](#perform-a-merge-with-source-duplicates "Link to this heading")

Perform a merge in which the source has duplicate values and the target has no matching values. All copies of the source
record are inserted into the target. For more information, see [Deterministic results for INSERT](#label-merge-deterministic-results-for-insert).

Truncate both tables and load new rows into the source table that include duplicates:

```
TRUNCATE table merge_example_target;

TRUNCATE table merge_example_source;

INSERT INTO merge_example_source (id, description) VALUES
  (50, 'This is a duplicate in the source and has no match in target'),
  (50, 'This is a duplicate in the source and has no match in target');
```

Copy

The `merge_example_target` has no values. Display the values in the
`merge_example_source` table:

```
SELECT * FROM merge_example_source;
```

Copy

```
+----+--------------------------------------------------------------+
| ID | DESCRIPTION                                                  |
|----+--------------------------------------------------------------|
| 50 | This is a duplicate in the source and has no match in target |
| 50 | This is a duplicate in the source and has no match in target |
+----+--------------------------------------------------------------+
```

Run the MERGE statement:

```
MERGE INTO merge_example_target
  USING merge_example_source
  ON merge_example_target.id = merge_example_source.id
  WHEN MATCHED THEN
    UPDATE SET merge_example_target.description = merge_example_source.description
  WHEN NOT MATCHED THEN
    INSERT (id, description) VALUES
      (merge_example_source.id, merge_example_source.description);
```

Copy

```
+-------------------------+------------------------+
| number of rows inserted | number of rows updated |
|-------------------------+------------------------|
|                       2 |                      0 |
+-------------------------+------------------------+
```

Display the new values in the target table:

```
SELECT * FROM merge_example_target;
```

Copy

```
+----+--------------------------------------------------------------+
| ID | DESCRIPTION                                                  |
|----+--------------------------------------------------------------|
| 50 | This is a duplicate in the source and has no match in target |
| 50 | This is a duplicate in the source and has no match in target |
+----+--------------------------------------------------------------+
```

### Perform a merge with deterministic and nondeterministic results[¶](#perform-a-merge-with-deterministic-and-nondeterministic-results "Link to this heading")

Merge records by using joins that produce nondeterministic and deterministic results.

Create and load two tables:

```
CREATE OR REPLACE TABLE merge_example_target_orig (k NUMBER, v NUMBER);

INSERT INTO merge_example_target_orig VALUES (0, 10);

CREATE OR REPLACE TABLE merge_example_src (k NUMBER, v NUMBER);

INSERT INTO merge_example_src VALUES (0, 11), (0, 12), (0, 13);
```

Copy

When you perform the merge in the following example, multiple updates conflict with each other. If
the [ERROR\_ON\_NONDETERMINISTIC\_MERGE](../parameters.html#label-error-on-nondeterministic-merge) session parameter is set to `true`, the MERGE statement
returns an error. Otherwise, the MERGE statement updates `merge_example_target_clone.v` with a value
(for example, `11`, `12`, or `13`) from one of the duplicate rows (row not defined):

```
CREATE OR REPLACE TABLE merge_example_target_clone
  CLONE merge_example_target_orig;

MERGE INTO  merge_example_target_clone
  USING merge_example_src
  ON merge_example_target_clone.k = merge_example_src.k
  WHEN MATCHED THEN UPDATE SET merge_example_target_clone.v = merge_example_src.v;
```

Copy

Updates and deletes conflict with each other. If the [ERROR\_ON\_NONDETERMINISTIC\_MERGE](../parameters.html#label-error-on-nondeterministic-merge) session
parameter is set to `true`, the MERGE statement returns an error. Otherwise, the MERGE statement either deletes the row
or updates `merge_example_target_clone.v` with a value (for example, `12` or `13`) from one of the
duplicate rows (row not defined):

```
CREATE OR REPLACE TABLE merge_example_target_clone
  CLONE merge_example_target_orig;

MERGE INTO merge_example_target_clone
  USING merge_example_src
  ON merge_example_target_clone.k = merge_example_src.k
  WHEN MATCHED AND merge_example_src.v = 11 THEN DELETE
  WHEN MATCHED THEN UPDATE SET merge_example_target_clone.v = merge_example_src.v;
```

Copy

Multiple deletes don’t conflict with each other. Joined values that don’t match any clause don’t prevent
the delete (`merge_example_src.v = 13`). The MERGE statement succeeds and the target row is deleted:

```
CREATE OR REPLACE TABLE target CLONE merge_example_target_orig;

MERGE INTO merge_example_target_clone
  USING merge_example_src
  ON merge_example_target_clone.k = merge_example_src.k
  WHEN MATCHED AND merge_example_src.v <= 12 THEN DELETE;
```

Copy

Joined values that don’t match any clause don’t prevent an update (`merge_example_src.v = 12, 13`).
The MERGE statement succeeds and the target row is set to `target.v = 11`:

```
CREATE OR REPLACE TABLE merge_example_target_clone CLONE target_orig;

MERGE INTO merge_example_target_clone
  USING merge_example_src
  ON merge_example_target_clone.k = merge_example_src.k
  WHEN MATCHED AND merge_example_src.v = 11
    THEN UPDATE SET merge_example_target_clone.v = merge_example_src.v;
```

Copy

Use GROUP BY in the source clause to ensure that each target row joins against one row
in the source:

```
CREATE OR REPLACE TABLE merge_example_target_clone CLONE merge_example_target_orig;

MERGE INTO merge_example_target_clone
  USING (SELECT k, MAX(v) AS v FROM merge_example_src GROUP BY k) AS b
  ON merge_example_target_clone.k = b.k
  WHEN MATCHED THEN UPDATE SET merge_example_target_clone.v = b.v
  WHEN NOT MATCHED THEN INSERT (k, v) VALUES (b.k, b.v);
```

Copy

### Perform a merge based on DATE values[¶](#perform-a-merge-based-on-date-values "Link to this heading")

In the following example, the `members` table stores the names, addresses, and current fees (`members.fee`) paid to a
local gym. The `signup` table stores each member’s signup date (`signup.date`). The MERGE statement applies a standard
$40 fee to members who joined the gym more than 30 days ago, after the free trial expired:

```
MERGE INTO members m
  USING (SELECT id, date
    FROM signup
    WHERE DATEDIFF(day, CURRENT_DATE(), signup.date::DATE) < -30) s
  ON m.id = s.id
  WHEN MATCHED THEN UPDATE SET m.fee = 40;
```

Copy

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
3. [matchedClause (for updates or deletes)](#matchedclause-for-updates-or-deletes)
4. [notMatchedClause (for inserts)](#notmatchedclause-for-inserts)
5. [Usage notes](#usage-notes)
6. [Duplicate join behavior](#duplicate-join-behavior)
7. [Nondeterministic results for UPDATE and DELETE](#nondeterministic-results-for-update-and-delete)
8. [Deterministic results for UPDATE and DELETE](#deterministic-results-for-update-and-delete)
9. [Deterministic results for INSERT](#deterministic-results-for-insert)
10. [Examples](#examples)
11. [Perform a basic merge that updates values](#perform-a-basic-merge-that-updates-values)
12. [Perform a basic merge with multiple operations](#perform-a-basic-merge-with-multiple-operations)
13. [Perform a merge by using ALL BY NAME](#perform-a-merge-by-using-all-by-name)
14. [Perform a merge with source duplicates](#perform-a-merge-with-source-duplicates)
15. [Perform a merge with deterministic and nondeterministic results](#perform-a-merge-with-deterministic-and-nondeterministic-results)
16. [Perform a merge based on DATE values](#perform-a-merge-based-on-date-values)