---
auto_generated: true
description: Remove rows from a table. You can use a WHERE clause to specify which
  rows should be removed. If you need to use a subquery(s) or additional table(s)
  to identify the rows to be removed, specify the su
last_scraped: '2026-01-14T16:57:41.246292+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/delete
title: DELETE | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[General DML](../sql-dml.md)DELETE

# DELETE[¶](#delete "Link to this heading")

Remove rows from a table. You can use a WHERE clause to specify which rows should be removed. If you need to use a subquery(s) or
additional table(s) to identify the rows to be removed, specify the subquery(s) or table(s) in a USING clause.

Important

Unlike [TRUNCATE TABLE](truncate-table), this command does not delete the external file load history. If you delete rows
loaded into the table from a staged file, you cannot load the data from that file again unless you modify the file and stage it again.

## Syntax[¶](#syntax "Link to this heading")

```
DELETE FROM <table_name>
            [ USING <additional_table_or_query> [, <additional_table_or_query> ] ]
            [ WHERE <condition> ]
```

Copy

## Required parameters[¶](#required-parameters "Link to this heading")

`table_name`
:   Specifies the table from which rows are removed.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`USING additional_table_or_query [, ... ]`
:   If you need to refer to additional tables in the WHERE clause to help identify the rows to be removed, then specify those table names in
    the USING clause. You can also use the USING clause to specify subqueries that identify the rows to be removed.

    If you specify a subquery, then put the subquery in parentheses.

    If you specify more than one table or query, use a comma to separate them.

`WHERE condition`
:   Specifies a condition to use to select rows for removal. If this parameter is omitted, all rows in the table are removed, but the table
    remains.

## Usage notes[¶](#usage-notes "Link to this heading")

* When deleting based on a JOIN (by specifying a `USING` clause), it is possible that a row in the target table joins against several
  rows in the `USING` table(s). If the DELETE condition is satisfied for any of the joined combinations, the target row is deleted.

  For example, given tables `tab1` and `tab2` with columns `(k number, v number)`:

  > ```
  > select * from tab1;
  >
  > -------+-------+
  >    k   |   v   |
  > -------+-------+
  >    0   |   10  |
  > -------+-------+
  >
  > Select * from tab2;
  >
  > -------+-------+
  >    k   |   v   |
  > -------+-------+
  >    0   |   20  |
  >    0   |   30  |
  > -------+-------+
  > ```
  >
  > Copy

  If you run the following query, the row in `tab1` is joined against both rows of `tab2`:

  > ```
  > DELETE FROM tab1 USING tab2 WHERE tab1.k = tab2.k
  > ```
  >
  > Copy

  Because at least one joined pair satisfies the condition, the row is deleted. As a result, after the statement completes, `tab1`
  is empty.

## Examples[¶](#examples "Link to this heading")

Suppose that an organization that leases bicycles uses the following tables:

* The table named leased\_bicycles lists the bicycles that were leased out.
* The table named returned\_bicycles lists bicycles that have been returned recently. These bicycles need be removed from the table of
  leased bicycles.

Create tables:

> ```
> CREATE TABLE leased_bicycles (bicycle_id INTEGER, customer_id INTEGER);
> CREATE TABLE returned_bicycles (bicycle_id INTEGER);
> ```
>
> Copy

Load data:

> ```
> INSERT INTO leased_bicycles (bicycle_ID, customer_ID) VALUES
>     (101, 1111),
>     (102, 2222),
>     (103, 3333),
>     (104, 4444),
>     (105, 5555);
> INSERT INTO returned_bicycles (bicycle_ID) VALUES
>     (102),
>     (104);
> ```
>
> Copy

This example shows how to use the `WHERE` clause to delete a specified row(s). This example deletes by bicycle\_ID:

> ```
> DELETE FROM leased_bicycles WHERE bicycle_ID = 105;
> +------------------------+
> | number of rows deleted |
> |------------------------|
> |                      1 |
> +------------------------+
> ```
>
> Copy

Show the data after the delete:

> ```
> SELECT * FROM leased_bicycles ORDER BY bicycle_ID;
> +------------+-------------+
> | BICYCLE_ID | CUSTOMER_ID |
> |------------+-------------|
> |        101 |        1111 |
> |        102 |        2222 |
> |        103 |        3333 |
> |        104 |        4444 |
> +------------+-------------+
> ```
>
> Copy

This example shows how to use the `USING` clause to specify rows to be deleted. This `USING` clause specifies the returned\_bicycles
table, which lists the IDs of the bicycles to be deleted from the leased\_bicycles table. The `WHERE` clause joins the leased\_bicycles
table to the returned\_bicycles table, and the rows in leased\_bicycles that have the same bicycle\_ID as the corresponding rows in
returned\_bicycles are deleted.

> ```
> BEGIN WORK;
> DELETE FROM leased_bicycles 
>     USING returned_bicycles
>     WHERE leased_bicycles.bicycle_ID = returned_bicycles.bicycle_ID;
> TRUNCATE TABLE returned_bicycles;
> COMMIT WORK;
> ```
>
> Copy

(To avoid trying to remove the same rows again in the future when it might be unnecessary or inappropriate, the returned\_bicycles table is
truncated as part of the same transaction.)

Show the data after the delete:

> ```
> SELECT * FROM leased_bicycles ORDER BY bicycle_ID;
> +------------+-------------+
> | BICYCLE_ID | CUSTOMER_ID |
> |------------+-------------|
> |        101 |        1111 |
> |        103 |        3333 |
> +------------+-------------+
> ```
>
> Copy

Now suppose that another bicycle(s) is returned:

> ```
> INSERT INTO returned_bicycles (bicycle_ID) VALUES (103);
> ```
>
> Copy

The following query shows a `USING` clause that contains a subquery (rather than a table) to specify which bicycle\_IDs to remove from
the leased\_bicycles table:

> ```
> BEGIN WORK;
> DELETE FROM leased_bicycles 
>     USING (SELECT bicycle_ID AS bicycle_ID FROM returned_bicycles) AS returned
>     WHERE leased_bicycles.bicycle_ID = returned.bicycle_ID;
> TRUNCATE TABLE returned_bicycles;
> COMMIT WORK;
> ```
>
> Copy

Show the data after the delete:

> ```
> SELECT * FROM leased_bicycles ORDER BY bicycle_ID;
> +------------+-------------+
> | BICYCLE_ID | CUSTOMER_ID |
> |------------+-------------|
> |        101 |        1111 |
> +------------+-------------+
> ```
>
> Copy

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
2. [Required parameters](#required-parameters)
3. [Optional parameters](#optional-parameters)
4. [Usage notes](#usage-notes)
5. [Examples](#examples)