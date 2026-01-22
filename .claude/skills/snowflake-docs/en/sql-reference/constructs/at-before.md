---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:56:46.184529+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/at-before
title: AT | BEFORE | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)AT

Categories:
:   [Query syntax](../constructs)

# AT | BEFORE[¶](#at-before "Link to this heading")

The AT or BEFORE clause is used for Snowflake Time Travel. In a query, it is specified in the [FROM](from) clause
immediately after the table name, and it determines the point in the past from which historical data is requested for the object:

* The AT keyword specifies that the request is inclusive of any changes made by a statement or transaction with a timestamp equal to the
  specified parameter.
* The BEFORE keyword specifies that the request refers to a point immediately preceding the specified parameter. This point in time is just
  before the statement, identified by its query ID, is completed. For more information, see [Using the BEFORE clause](#label-before-clause-with-query-id).

You can use the same syntax to clone objects; see [CREATE <object> … CLONE](../sql/create-clone). If you don’t
specify a point in time for a clone, the clone defaults to the state of the object as of now
(the [CURRENT\_TIMESTAMP](../functions/current_timestamp) value).

For more information, see [Understanding & using Time Travel](../../user-guide/data-time-travel).

See also:
:   [FROM](from)

## Syntax[¶](#syntax "Link to this heading")

```
SELECT ...
FROM ...
  { AT | BEFORE }
  (
    { TIMESTAMP => <timestamp> |
      OFFSET => <time_difference> |
      STATEMENT => <id> |
      STREAM => '<name>' }
  )
[ ... ]
```

Copy

## Parameters[¶](#parameters "Link to this heading")

`TIMESTAMP => timestamp`
:   Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP,
    TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, or TIMESTAMP\_TZ data type.

    If no explicit cast is specified, the timestamp in the AT clause is treated as a timestamp with the UTC time zone (equivalent to
    TIMESTAMP\_NTZ). Using the TIMESTAMP data type for an explicit cast may also result in the value being treated as a TIMESTAMP\_NTZ
    value. For details, see [Date & time data types](../data-types-datetime).

`OFFSET => time_difference`
:   Specifies the difference in seconds from the current time to use for Time Travel, in the form `-N` where `N`
    can be an integer or arithmetic expression (e.g. `-120` is 120 seconds, `-30*60` is 1800 seconds or 30 minutes).

`STATEMENT => id`
:   Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the
    following types:

    * DML (e.g. INSERT, UPDATE, DELETE)
    * TCL (BEGIN, COMMIT transaction)
    * SELECT

    The query ID must reference a query that has been executed within the last 14 days. If the query ID references a query over 14 days old,
    the following error is returned:

    ```
    Error: statement <query_id> not found
    ```

    To work around this limitation, use the timestamp for the referenced query.

`STREAM => 'name'`
:   Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in
    the stream is used as the `AT` or `BEFORE` point in time for returning change data for the source object.

    This keyword is supported only when creating a stream (using [CREATE STREAM](../sql/create-stream)) or querying change data (using
    the [CHANGES](changes) clause). For examples, see those topics.

## Using the AT TIMESTAMP parameter[¶](#using-the-at-timestamp-parameter "Link to this heading")

In the AT clause, you can specify the TIMESTAMP keyword followed by a string that represents a timestamp and an optional explicit cast to
the TIMESTAMP, TIMESTAMP\_TZ, TIMESTAMP\_LTZ, or TIMESTAMP\_NTZ data type. The following examples are all valid:

```
AT ( TIMESTAMP => '2024-06-05 12:30:00'::TIMESTAMP_LTZ )

AT ( TIMESTAMP => '2024-06-05 12:30:00'::TIMESTAMP )

AT ( TIMESTAMP => '2024-06-05 12:30:00' )
```

Copy

If no explicit cast is specified, the timestamp in the AT clause is treated as a timestamp with the UTC time zone (equivalent to TIMESTAMP\_NTZ).
Using the TIMESTAMP data type for an explicit cast may also result in the value being treated as a TIMESTAMP\_NTZ value, as discussed in
[Date & time data types](../data-types-datetime).

The explicit cast that you choose affects the results of Time Travel queries because timestamps are interpreted with respect to the
current time zone for the session and the value of the TIMESTAMP\_TYPE\_MAPPING parameter. For more details about this behavior, see
[Querying Time Travel data in a session with a non-UTC time zone](https://community.snowflake.com/s/article/Querying-time-travel-data-in-a-session-with-a-non-UTC-timezone).

For example, you are running queries in a SQL session where the current time zone is `America/Los_Angeles` and TIMESTAMP\_TYPE\_MAPPING is set to
`TIMESTAMP_NTZ`. Create a table and immediately insert two rows:

```
CREATE OR REPLACE TABLE tt1 (c1 INT, c2 INT);
INSERT INTO tt1 VALUES(1,2);
INSERT INTO tt1 VALUES(2,3);
```

Copy

Check the creation time of the table with a SHOW TABLES command:

```
SHOW TERSE TABLES LIKE 'tt1';
```

Copy

```
+-------------------------------+------+-------+---------------+----------------+
| created_on                    | name | kind  | database_name | schema_name    |
|-------------------------------+------+-------+---------------+----------------|
| 2024-06-05 15:25:35.557 -0700 | TT1  | TABLE | TRAVEL_DB     | TRAVEL_SCHEMA  |
+-------------------------------+------+-------+---------------+----------------+
```

Note the time zone offset in the `created_on` column. Five minutes later, insert another row:

```
INSERT INTO tt1 VALUES(3,4);
```

Copy

Now run the following Time Travel query, expecting it to return the first two rows:

```
SELECT * FROM tt1 at(TIMESTAMP => '2024-06-05 15:29:00'::TIMESTAMP);
```

Copy

```
000707 (02000): Time travel data is not available for table TT1. The requested time is either beyond the allowed time travel period or before the object creation time.
```

The query fails because the time zone of the session is UTC, and the explicit cast to TIMESTAMP honors that time zone.
Therefore, the table is assumed to have been created *after* the specified timestamp. To solve this problem, run the
query again with an explicit cast to TIMESTAMP\_LTZ (local time zone):

```
SELECT * FROM tt1 at(TIMESTAMP => '2024-06-05 15:29:00'::TIMESTAMP_LTZ);
```

Copy

```
+----+----+
| C1 | C2 |
|----+----|
|  1 |  2 |
|  2 |  3 |
+----+----+
```

As expected, the query returns the first two rows that were inserted. Finally, run the same query but specify a slightly later timestamp:

```
SELECT * FROM tt1 at(TIMESTAMP => '2024-06-05 15:31:00'::TIMESTAMP_LTZ);
```

Copy

```
+----+----+
| C1 | C2 |
|----+----|
|  1 |  2 |
|  2 |  3 |
|  3 |  4 |
+----+----+
```

This query returns all three rows, given the later timestamp.

## Using the BEFORE clause[¶](#using-the-before-clause "Link to this heading")

The STATEMENT parameter in the BEFORE clause must refer to a query ID. The point in the past used by Time Travel is just before the
statement for that query ID is completed rather than before the statement is started. If concurrent queries commit modifications to
the data between the start and end of the statement, these changes are included in your results.

For example, the following statements are being executed on table `my_table` in parallel in two separate threads:

| Time | Thread | Operation | Phase | Description |
| --- | --- | --- | --- | --- |
| `t1` | 1 | INSERT INTO my\_table(id) VALUE(1) | Start | Insert starts execution by performing required checks. |
| `t2` | 1 | INSERT INTO my\_table(id) VALUE(1) | End | Insert updated `my_table`. |
| `t3` | 1 | DELETE FROM my\_table | Start | Delete identifies the list of records to delete (id=1). |
| `t4` | 2 | INSERT INTO my\_table(id) VALUE(2) | Start | Insert starts execution by performing required checks. |
| `t5` | 2 | INSERT INTO my\_table(id) VALUE(2) | End | Insert updated `my_table`. |
| `t6` | 2 | SELECT \* FROM my\_table | End | Thread `2` selects rows from `my_table`. The results include all rows (id=1, id=2). |
| `t7` | 1 | DELETE FROM my\_table | End | Delete updates `my_table` deleting all old records present before time `t3` when the delete statement started in thread `1` (id=1). |
| `t8` | 1 | SELECT \* FROM my\_table BEFORE(STATEMENT => LAST\_QUERY\_ID()) | End | SELECT statement uses Time Travel to retrieve historical data from before the completion of the delete operation. The results include the row from the 2nd insert statement that happened concurrently in thread `2` (id=1, id=2). |

As a workaround, you can use a TIMESTAMP parameter that specifies a point in time just before the start of the statement.

## Usage notes[¶](#usage-notes "Link to this heading")

* Data in Snowflake is identified by timestamps that can differ slightly from the exact value of system time.
* The value for TIMESTAMP or OFFSET must be a constant expression.
* The smallest time resolution for TIMESTAMP is milliseconds.
* If requested data is beyond the Time Travel retention period (default is 1 day), the statement fails.

  In addition, if the requested data is within the Time Travel retention period but no historical data is available (e.g. if the retention
  period was extended), the statement fails.
* If the specified Time Travel time is at or before the point in time when the object was created, the statement fails. See
  [Using the AT TIMESTAMP parameter](#label-at-before-timestamp).
* When you access historical table data, the results include the columns, default values, etc. from the current definition of the table.
  The same applies to non-materialized views. For example, if you alter a table to add a column, querying for historical data before
  the point in time when the column was added returns results that include the new column.
* Historical data has the same access control requirements as current data. Any changes are applied retroactively.
* The AT and BEFORE clauses do not support selecting historical data from a [CTE](../../user-guide/queries-cte).

  For example, the following query is not supported:

  ```
  WITH mycte AS
    (SELECT mytable.* FROM mytable)
  SELECT * FROM mycte AT(TIMESTAMP => '2024-03-13 13:56:09.553 +0100'::TIMESTAMP_TZ);
  ```

  Copy

  However, these clauses are supported in a query in a [WITH](with) clause. For example, the following
  query is supported:

  ```
  WITH mycte AS
    (SELECT * FROM mytable AT(TIMESTAMP => '2024-03-13 13:56:09.553 +0100'::TIMESTAMP_TZ))
  SELECT * FROM mycte;
  ```

  Copy
* Time Travel queries against hybrid tables have the following limitations:

  + Only the TIMESTAMP parameter is supported in the AT clause. The OFFSET, STATEMENT, and STREAM parameters are not supported.
  + The value of the TIMESTAMP parameter must be the same for all tables that belong to the same database. If the tables belong
    to different databases, different TIMESTAMP values may be used.
  + The BEFORE clause is not supported.
* CREATE DATABASE … CLONE and CREATE SCHEMA … CLONE commands that use Time Travel and specify the time with the STATEMENT parameter
  return an error if any hybrid tables exist in the specified database. The error prompts you to run the command using the
  [IGNORE HYBRID TABLES parameter](../sql/create-clone.html#label-ignore-hybrid-tables-parameter). When you include this parameter, the command will
  create the cloned database or schema but skip any hybrid tables.

## Troubleshooting[¶](#troubleshooting "Link to this heading")

|  |  |
| --- | --- |
| Error | ``` Time travel data is not available for table <tablename> ``` |
| Cause | In some cases, this is caused by using a string where a timestamp is expected. |
| Solution | Cast the string to a timestamp.  ``` ... AT(TIMESTAMP => '2018-07-27 12:00:00')               -- fails ... AT(TIMESTAMP => '2018-07-27 12:00:00'::TIMESTAMP)    -- succeeds ```  Copy |

## Examples[¶](#examples "Link to this heading")

Select historical data from a table using a specific timestamp. In the first two
examples, which use the TIMESTAMP parameter, `my_table` could be a standard table or a hybrid table.
Subsitute a recent date, time, or timestamp that’s within the retention period.

```
SELECT * FROM my_table AT(TIMESTAMP => 'Wed, 26 Jun 2024 09:20:00 -0700'::TIMESTAMP_LTZ);
```

Copy

```
SELECT * FROM my_table AT(TIMESTAMP => TO_TIMESTAMP(1432669154242, 3));
```

Copy

Select historical data from a table as of 5 minutes ago:

```
SELECT * FROM my_table AT(OFFSET => -60*5) AS T WHERE T.flag = 'valid';
```

Copy

Select historical data from a table up to, but not including any changes made by the specified transaction:

```
SELECT * FROM my_table BEFORE(STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726');
```

Copy

Return the difference in table data resulting from the specified transaction:

```
SELECT oldt.* ,newt.*
  FROM my_table BEFORE(STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726') AS oldt
    FULL OUTER JOIN my_table AT(STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726') AS newt
    ON oldt.id = newt.id
  WHERE oldt.id IS NULL OR newt.id IS NULL;
```

Copy

The following example runs a Time Travel join query against two tables in the same database, one of
which is a hybrid table. The same TIMESTAMP expression must be used for both tables.
Subsitute a recent date, time, or timestamp that’s within the retention period.

```
SELECT *
  FROM db1.public.htt1
    AT(TIMESTAMP => '2024-06-05 17:50:00'::TIMESTAMP_LTZ) h
    JOIN db1.public.tt1
    AT(TIMESTAMP => '2024-06-05 17:50:00'::TIMESTAMP_LTZ) t
    ON h.c1=t.c1;
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
3. [Using the AT TIMESTAMP parameter](#using-the-at-timestamp-parameter)
4. [Using the BEFORE clause](#using-the-before-clause)
5. [Usage notes](#usage-notes)
6. [Troubleshooting](#troubleshooting)
7. [Examples](#examples)