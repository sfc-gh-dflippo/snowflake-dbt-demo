---
auto_generated: true
description: Updates a table by inserting one or more rows into the table. The values
  inserted into each column in the table can be explicitly-specified or the results
  of a query.
last_scraped: '2026-01-14T16:57:02.808984+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/insert
title: INSERT | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)
   * [Query operators](../operators.md)
   * [General DDL](../sql-ddl-summary.md)
   * [General DML](../sql-dml.md)

     + [INSERT](insert.md)

       - [Multi-table](insert-multi-table.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[General DML](../sql-dml.md)INSERT

# INSERT[¶](#insert "Link to this heading")

Updates a table by inserting one or more rows into the table. The values inserted into each column in the table can be explicitly-specified
or the results of a query.

See also:
:   [INSERT (multi-table)](insert-multi-table)

## Syntax[¶](#syntax "Link to this heading")

```
INSERT [ OVERWRITE ] INTO <target_table> [ ( <target_col_name> [ , ... ] ) ]
       {
         VALUES ( { <value> | DEFAULT | NULL } [ , ... ] ) [ , ( ... ) ]  |
         <query>
       }
```

Copy

## Required parameters[¶](#required-parameters "Link to this heading")

`target_table`
:   Specifies the target table into which to insert rows.

`VALUES ( value | DEFAULT | NULL [ , ... ] )  [ , ( ... ) ]`
:   Specifies one or more values to insert into the corresponding columns in the target table.

    In a `VALUES` clause, you can specify the following:

    * `value`: Inserts the explicitly-specified value. The value may be a literal or an expression.
    * `DEFAULT`: Inserts the default value for the corresponding column in the target table.
    * `NULL`: Inserts a `NULL` value.

    Each value in the clause must be separated by a comma.

    You can insert multiple rows by specifying additional sets of values in the clause. For more details, see the [Usage Notes](#usage-notes)
    and the [Examples](#examples) (in this topic).

`query`
:   Specify a [query](../constructs) statement that returns values to be inserted into the corresponding
    columns. This allows you to insert rows into a target table from one or more source tables.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`OVERWRITE`
:   Specifies that the target table should be truncated before inserting the values into the table. Note that specifying this option does
    not affect the access control privileges on the table.

    INSERT statements with `OVERWRITE` can be processed within the scope of the current transaction, which avoids DDL statements that
    commit a transaction, such as:

    > ```
    > DROP TABLE t;
    > CREATE TABLE t AS SELECT * FROM ... ;
    > ```
    >
    > Copy

    Default: No value (the target table is not truncated before performing the inserts).

`( target_col_name [ , ... ] )`
:   Specifies one or more columns in the target table into which the corresponding values are inserted. The number of target columns specified
    must match the number of specified values or columns (if the values are the results of a query) in the `VALUES` clause.

    Default: No value (all the columns in the target table are updated).

## Usage notes[¶](#usage-notes "Link to this heading")

* Using a single INSERT command, you can insert multiple rows into a table by specifying additional sets of values separated by commas in
  the `VALUES` clause.

  For example, the following clause would insert 3 rows in a 3-column table, with values `1`, `2`, and `3` in the first two rows and
  values `2`, `3`, and `4` in the third row:

  > ```
  > VALUES ( 1, 2, 3 ) ,
  >        ( 1, 2, 3 ) ,
  >        ( 2, 3, 4 )
  > ```
  >
  > Copy
* To use the OVERWRITE option on INSERT, you must use a role that has DELETE privilege on the table because OVERWRITE will delete the
  existing records in the table.
* Some expressions cannot be specified in the VALUES clause. As an alternative, specify the expression in a query clause. For example, you
  can replace:

  > ```
  > INSERT INTO table1 (ID, varchar1, variant1)
  >     VALUES (4, 'Fourier', PARSE_JSON('{ "key1": "value1", "key2": "value2" }'));
  > ```
  >
  > Copy

  with:

  > ```
  > INSERT INTO table1 (ID, varchar1, variant1)
  >     SELECT 4, 'Fourier', PARSE_JSON('{ "key1": "value1", "key2": "value2" }');
  > ```
  >
  > Copy
* The VALUES clause is limited to 16,384 rows. This limit applies to a single INSERT INTO … VALUES
  statement and a single INSERT INTO … SELECT … FROM VALUES statement. Consider using the
  [COPY INTO <table>](copy-into-table) command to perform a bulk data load. For more information
  about using the VALUES clause in a SELECT statement, see [VALUES](../constructs/values).
* For information about inserting data into hybrid tables, see [Loading data](../../user-guide/tables-hybrid-create.html#label-create-loading-data).

## Examples[¶](#examples "Link to this heading")

The following examples use the INSERT command.

### Single row insert using a query[¶](#single-row-insert-using-a-query "Link to this heading")

Convert three string values to dates or timestamps and insert them into a single row in the `mytable` table:

```
CREATE OR REPLACE TABLE mytable (
  col1 DATE,
  col2 TIMESTAMP_NTZ,
  col3 TIMESTAMP_NTZ);

DESC TABLE mytable;
```

Copy

```
+------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
| name | type             | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | privacy domain |
|------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------|
| COL1 | DATE             | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| COL2 | TIMESTAMP_NTZ(9) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
| COL3 | TIMESTAMP_NTZ(9) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL           |
+------+------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+----------------+
```

```
INSERT INTO mytable
  SELECT
    TO_DATE('2013-05-08T23:39:20.123'),
    TO_TIMESTAMP('2013-05-08T23:39:20.123'),
    TO_TIMESTAMP('2013-05-08T23:39:20.123');

SELECT * FROM mytable;
```

Copy

```
+------------+-------------------------+-------------------------+
| COL1       | COL2                    | COL3                    |
|------------+-------------------------+-------------------------|
| 2013-05-08 | 2013-05-08 23:39:20.123 | 2013-05-08 23:39:20.123 |
+------------+-------------------------+-------------------------+
```

Similar to previous example, but specify to update only the first and third columns in the table:

```
INSERT INTO mytable (col1, col3)
  SELECT
    TO_DATE('2013-05-08T23:39:20.123'),
    TO_TIMESTAMP('2013-05-08T23:39:20.123');

SELECT * FROM mytable;
```

Copy

```
+------------+-------------------------+-------------------------+
| COL1       | COL2                    | COL3                    |
|------------+-------------------------+-------------------------|
| 2013-05-08 | 2013-05-08 23:39:20.123 | 2013-05-08 23:39:20.123 |
| 2013-05-08 | NULL                    | 2013-05-08 23:39:20.123 |
+------------+-------------------------+-------------------------+
```

### Multi-row insert using explicitly-specified values[¶](#multi-row-insert-using-explicitly-specified-values "Link to this heading")

Create the `employees` table and insert four rows of data into it by providing sets of values in a
comma-separated list in the VALUES clause:

```
CREATE TABLE employees (
  first_name VARCHAR,
  last_name VARCHAR,
  workphone VARCHAR,
  city VARCHAR,
  postal_code VARCHAR);

INSERT INTO employees
  VALUES
    ('May', 'Franklin', '1-650-249-5198', 'San Francisco', 94115),
    ('Gillian', 'Patterson', '1-650-859-3954', 'San Francisco', 94115),
    ('Lysandra', 'Reeves', '1-212-759-3751', 'New York', 10018),
    ('Michael', 'Arnett', '1-650-230-8467', 'San Francisco', 94116);

SELECT * FROM employees;
```

Copy

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| May        | Franklin  | 1-650-249-5198 | San Francisco | 94115       |
| Gillian    | Patterson | 1-650-859-3954 | San Francisco | 94115       |
| Lysandra   | Reeves    | 1-212-759-3751 | New York      | 10018       |
| Michael    | Arnett    | 1-650-230-8467 | San Francisco | 94116       |
+------------+-----------+----------------+---------------+-------------+
```

In multi-row inserts, make sure that the data types of the inserted values are consistent across the rows because the data type of the
first row is used as a guide. Create a table and insert two rows:

```
CREATE OR REPLACE TABLE demo_insert_type_mismatch (v VARCHAR);
```

Copy

The first insert works as expected:

```
INSERT INTO demo_insert_type_mismatch (v) VALUES
  ('three'),
  ('four');
```

Copy

```
+-------------------------+
| number of rows inserted |
|-------------------------|
|                       2 |
+-------------------------+
```

The second insert fails because the data type of the value in the second row (`'d'`) is a string, which is
different from the numeric data type of the value in the first row (`3`). The insert fails even though both values
can be [coerced](../data-type-conversion) to VARCHAR, which is the data type of the column in
the table. The insert fails even though the data type of the value `'d'` is the same as the data type of column `v`:

```
INSERT INTO demo_insert_type_mismatch (v) VALUES
  (3),
  ('d');
```

Copy

```
100038 (22018): DML operation to table DEMO_INSERT_TYPE_MISMATCH failed on column V with error: Numeric value 'd' is not recognized
```

When the data types are consistent across the rows, the insert succeeds, and both numeric values are coerced to the VARCHAR data type:

```
INSERT INTO demo_insert_type_mismatch (v) VALUES
  (3),
  (4);
```

Copy

```
+-------------------------+
| number of rows inserted |
|-------------------------|
|                       2 |
+-------------------------+
```

### Multi-row insert using query[¶](#multi-row-insert-using-query "Link to this heading")

Insert multiple rows of data from the `contractors` table into the `employees` table:

* Select only those rows where the `worknum` column contains area code `650`.
* Insert a NULL value in the `city` column.

```
SELECT * FROM employees;
```

Copy

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| May        | Franklin  | 1-650-249-5198 | San Francisco | 94115       |
| Gillian    | Patterson | 1-650-859-3954 | San Francisco | 94115       |
| Lysandra   | Reeves    | 1-212-759-3751 | New York      | 10018       |
| Michael    | Arnett    | 1-650-230-8467 | San Francisco | 94116       |
+------------+-----------+----------------+---------------+-------------+
```

```
CREATE TABLE contractors (
  contractor_first VARCHAR,
  contractor_last VARCHAR,
  worknum VARCHAR,
  city VARCHAR,
  zip_code VARCHAR);

INSERT INTO contractors
  VALUES
    ('Bradley', 'Greenbloom', '1-650-445-0676', 'San Francisco', 94110),
    ('Cole', 'Simpson', '1-212-285-8904', 'New York', 10001),
    ('Laurel', 'Slater', '1-650-633-4495', 'San Francisco', 94115);

SELECT * FROM contractors;
```

Copy

```
+------------------+-----------------+----------------+---------------+----------+
| CONTRACTOR_FIRST | CONTRACTOR_LAST | WORKNUM        | CITY          | ZIP_CODE |
|------------------+-----------------+----------------+---------------+----------|
| Bradley          | Greenbloom      | 1-650-445-0676 | San Francisco | 94110    |
| Cole             | Simpson         | 1-212-285-8904 | New York      | 10001    |
| Laurel           | Slater          | 1-650-633-4495 | San Francisco | 94115    |
+------------------+-----------------+----------------+---------------+----------+
```

```
INSERT INTO employees(first_name, last_name, workphone, city, postal_code)
  SELECT contractor_first, contractor_last, worknum, NULL, zip_code
    FROM contractors
    WHERE CONTAINS(worknum,'650');

SELECT * FROM employees;
```

Copy

```
+------------+------------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME  | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+------------+----------------+---------------+-------------|
| May        | Franklin   | 1-650-249-5198 | San Francisco | 94115       |
| Gillian    | Patterson  | 1-650-859-3954 | San Francisco | 94115       |
| Lysandra   | Reeves     | 1-212-759-3751 | New York      | 10018       |
| Michael    | Arnett     | 1-650-230-8467 | San Francisco | 94116       |
| Bradley    | Greenbloom | 1-650-445-0676 | NULL          | 94110       |
| Laurel     | Slater     | 1-650-633-4495 | NULL          | 94115       |
+------------+------------+----------------+---------------+-------------+
```

Insert multiple rows of data from the `contractors` table into the `employees` table using a common table expression:

```
INSERT INTO employees (first_name, last_name, workphone, city, postal_code)
  WITH cte AS
    (SELECT contractor_first AS first_name,
            contractor_last AS last_name,
            worknum AS workphone,
            city,
            zip_code AS postal_code
       FROM contractors)
  SELECT first_name, last_name, workphone, city, postal_code
    FROM cte;
```

Copy

Insert columns from two tables (`emp_addr`, `emp_ph`) into a third table (`emp`) using an INNER JOIN on the `id`
column in the source tables:

```
INSERT INTO emp (id, first_name, last_name, city, postal_code, ph)
  SELECT a.id, a.first_name, a.last_name, a.city, a.postal_code, b.ph
    FROM emp_addr a
    INNER JOIN emp_ph b ON a.id = b.id;
```

Copy

### Multi-row insert for JSON data[¶](#multi-row-insert-for-json-data "Link to this heading")

Insert two JSON objects into a VARIANT column in a table:

```
CREATE TABLE prospects (column1 VARIANT);

INSERT INTO prospects
  SELECT PARSE_JSON(column1)
  FROM VALUES
  ('{
    "_id": "57a37f7d9e2b478c2d8a608b",
    "name": {
      "first": "Lydia",
      "last": "Williamson"
    },
    "company": "Miralinz",
    "email": "lydia.williamson@miralinz.info",
    "phone": "+1 (914) 486-2525",
    "address": "268 Havens Place, Dunbar, Rhode Island, 02801"
  }')
  , ('{
    "_id": "57a37f7d622a2b1f90698c01",
    "name": {
      "first": "Denise",
      "last": "Holloway"
    },
    "company": "DIGIGEN",
    "email": "denise.holloway@digigen.net",
    "phone": "+1 (979) 587-3021",
    "address": "441 Dover Street, Ada, New Mexico, 87105"
  }');
```

Copy

### Insert using OVERWRITE[¶](#insert-using-overwrite "Link to this heading")

This example uses INSERT with OVERWRITE to rebuild the `sf_employees` table from `employees` after new records were added
to the `employees` table.

Here is the initial data for both tables:

```
SELECT * FROM employees;
```

Copy

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| May        | Franklin  | 1-650-111-1111 | San Francisco | 94115       |
| Gillian    | Patterson | 1-650-222-2222 | San Francisco | 94115       |
| Lysandra   | Reeves    | 1-212-222-2222 | New York      | 10018       |
| Michael    | Arnett    | 1-650-333-3333 | San Francisco | 94116       |
+------------+-----------+----------------+---------------+-------------+
```

```
SELECT * FROM sf_employees;
```

Copy

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| Mary       | Smith     | 1-650-999-9999 | San Francisco | 94115       |
+------------+-----------+----------------+---------------+-------------+
```

This statement inserts rows into the `sf_employees` table using the OVERWRITE clause:

```
INSERT OVERWRITE INTO sf_employees
  SELECT * FROM employees
  WHERE city = 'San Francisco';
```

Copy

Because the INSERT used the OVERWRITE clause, the old rows from `sf_employees` are gone:

```
SELECT * FROM sf_employees;
```

Copy

```
+------------+-----------+----------------+---------------+-------------+
| FIRST_NAME | LAST_NAME | WORKPHONE      | CITY          | POSTAL_CODE |
|------------+-----------+----------------+---------------+-------------|
| May        | Franklin  | 1-650-111-1111 | San Francisco | 94115       |
| Gillian    | Patterson | 1-650-222-2222 | San Francisco | 94115       |
| Michael    | Arnett    | 1-650-333-3333 | San Francisco | 94116       |
+------------+-----------+----------------+---------------+-------------+
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
2. [Required parameters](#required-parameters)
3. [Optional parameters](#optional-parameters)
4. [Usage notes](#usage-notes)
5. [Examples](#examples)