---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:55:03.300463+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/values
title: VALUES | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)

     + [SELECT](../sql/select.md)
     + [WITH](with.md)
     + [TOP <n>](top_n.md)
     + [INTO](into.md)
     + [FROM](from.md)
     + [AT](at-before.md)
     + [BEFORE](at-before.md)
     + [CHANGES](changes.md)
     + [CONNECT BY](connect-by.md)
     + [JOIN](join.md)
     + [ASOF JOIN](asof-join.md)
     + [LATERAL](join-lateral.md)
     + [MATCH\_RECOGNIZE](match_recognize.md)
     + [PIVOT](pivot.md)
     + [UNPIVOT](unpivot.md)
     + [VALUES](values.md)
     + [SAMPLE / TABLESAMPLE](sample.md)
     + [RESAMPLE](resample.md)
     + [SEMANTIC\_VIEW](semantic_view.md)
     + [WHERE](where.md)
     + [GROUP BY](group-by.md)
     + [GROUP BY CUBE](group-by-cube.md)
     + [GROUP BY GROUPING SETS](group-by-grouping-sets.md)
     + [GROUP BY ROLLUP](group-by-rollup.md)
     + [HAVING](having.md)
     + [QUALIFY](qualify.md)
     + [ORDER BY](order-by.md)
     + [LIMIT](limit.md)
     + [FETCH](limit.md)
     + [FOR UPDATE](for-update.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)VALUES

Categories:
:   [Query syntax](../constructs)

# VALUES[¶](#values "Link to this heading")

In the SELECT statement, the VALUES subclause of the FROM clause lets you
specify a set of constants to form a finite set of rows.

For information about the VALUES clause in the INSERT statement, see
the documentation for the [INSERT](../sql/insert) statement.

## Syntax[¶](#syntax "Link to this heading")

```
SELECT ...
FROM ( VALUES ( <expr> [ , <expr> [ , ... ] ] ) [ , ( ... ) ] )
  [ [ AS ] <table_alias> [ ( <column_alias> [ , ... ] ) ] ]
[ ... ]
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`expr`
:   Each expression must be a constant, or an expression that can be evaluated as a constant during compilation of the
    SQL statement.

    Most simple arithmetic expressions and string functions can be evaluated at compile time, but most other expressions
    can’t.

`table_alias`
:   An optional alias to give the set of rows a name, as though the set of rows were a table.

`column_alias`
:   Optional column aliases can specify the columns names.

## Usage notes[¶](#usage-notes "Link to this heading")

* Inside a [FROM](from) clause, a VALUES clause can’t contain the `DEFAULT` keyword. This limitation is in contrast
  to a VALUES clause in an [INSERT](../sql/insert) statement, which supports the use
  of `DEFAULT`; for example, `INSERT INTO table VALUES (10, DEFAULT, 'Name') ...`.
* When the VALUES clause includes multiple numeric values for the same column, and the values differ significantly in scale
  or precision, Snowflake might return an `out of range` error. The error might be returned even if each individual value
  wouldn’t result in an error for the target column’s data type.

  The error occurs because Snowflake determines a common, numeric data type that can encompass all of the numeric literals
  provided in a VALUES clause, and some values might be out of range for the determined common data type.

  For example, the following statement returns an `out of range` error:

  ```
  SELECT column1 FROM VALUES
    (3.469446951953614e-18),
    (115898.73);
  ```

  Copy

  ```
  100039 (22003): Numeric value '115898.73' is out of range
  ```

  You can avoid this type of error by making the following changes:

  + Separate the values in the VALUES clause into multiple SQL statements.
  + Cast values to a data type with a wider range of values, such as FLOAT. However, casting might result in less numeric precision.
  + Specify the values as text strings in quotation marks, and then convert the values to numeric values as needed.
* The VALUES clause is limited to 16,384 rows.

## Examples[¶](#examples "Link to this heading")

The following examples use the VALUES clause to generate a fixed, known set of rows:

```
SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three'));
```

Copy

```
+---------+---------+
| COLUMN1 | COLUMN2 |
|---------+---------|
|       1 | one     |
|       2 | two     |
|       3 | three   |
+---------+---------+
```

You can reference values either by column name (implicit) or column position. The following
example references the second column by column position:

```
SELECT column1, $2 FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three'));
```

Copy

```
+---------+-------+
| COLUMN1 | $2    |
|---------+-------|
|       1 | one   |
|       2 | two   |
|       3 | three |
+---------+-------+
```

The following example distinguishes multiple VALUES clauses by using aliases:

```
SELECT v1.$2, v2.$2
  FROM (VALUES (1, 'one'), (2, 'two')) AS v1
        INNER JOIN (VALUES (1, 'One'), (3, 'three')) AS v2
  WHERE v2.$1 = v1.$1;
```

Copy

You can also specify aliases for the column names, as shown in the following example:

```
SELECT c1, c2
  FROM (VALUES (1, 'one'), (2, 'two')) AS v1 (c1, c2);
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
3. [Usage notes](#usage-notes)
4. [Examples](#examples)