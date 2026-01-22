---
auto_generated: true
description: Updates specified rows in the target table with new values.
last_scraped: '2026-01-14T16:57:35.275394+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/update.html
title: UPDATE | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[General DML](../sql-dml.md)UPDATE

# UPDATE[¶](#update "Link to this heading")

Updates specified rows in the target table with new values.

## Syntax[¶](#syntax "Link to this heading")

```
UPDATE <target_table>
       SET <col_name> = <value> [ , <col_name> = <value> , ... ]
        [ FROM <additional_tables> ]
        [ WHERE <condition> ]
```

Copy

## Required parameters[¶](#required-parameters "Link to this heading")

`target_table`
:   Specifies the table to update.

`col_name`
:   Specifies the name of a column in `target_table`. Do not include the table name. For example, `UPDATE t1 SET t1.col = 1`
    is invalid.

`value`
:   Specifies the new value to set in `col_name`.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`FROM additional_tables`
:   Specifies one or more tables to use for selecting rows to update or for setting new values. Note that repeating the target table results
    in a self-join.

`WHERE condition`
:   Expression that specifies the rows in the target table to update.

    Default: No value (all rows of the target table are updated)

## Usage notes[¶](#usage-notes "Link to this heading")

* When a [FROM](../constructs/from) clause contains a [JOIN](../constructs/join) between
  tables (e.g. `t1` and `t2`), a target row in `t1` may join against (i.e. match) more than one row in table `t2`. When
  this occurs, the target row is called a *multi-joined row*. When updating a multi-joined row, the
  [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](../parameters.html#label-error-on-nondeterministic-update) session parameter controls the outcome of the update:

  + If `FALSE` (default value), no error is returned and one of the joined rows is used to update the target row; however, the
    selected joined row is nondeterministic.
  + IF `TRUE`, an error is returned, including an example of the values of a target row that joins multiple rows.

  To set the parameter:

  > ```
  > ALTER SESSION SET ERROR_ON_NONDETERMINISTIC_UPDATE=TRUE;
  > ```
  >
  > Copy

## Examples[¶](#examples "Link to this heading")

Perform a standard update using two tables:

> ```
> UPDATE t1
>   SET number_column = t1.number_column + t2.number_column, t1.text_column = 'ASDF'
>   FROM t2
>   WHERE t1.key_column = t2.t1_key and t1.number_column < 10;
> ```
>
> Copy

Update with join that produces nondeterministic results:

> ```
> select * from target;
>
> +---+----+
> | K |  V |
> |---+----|
> | 0 | 10 |
> +---+----+
>
> Select * from src;
>
> +---+----+
> | K |  V |
> |---+----|
> | 0 | 11 |
> | 0 | 12 |
> | 0 | 13 |
> +---+----+
>
> -- Following statement joins all three rows in src against the single row in target
> UPDATE target
>   SET v = src.v
>   FROM src
>   WHERE target.k = src.k;
>
> +------------------------+-------------------------------------+
> | number of rows updated | number of multi-joined rows updated |
> |------------------------+-------------------------------------|
> |                      1 |                                   1 |
> +------------------------+-------------------------------------+
> ```
>
> Copy
>
> * With [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](../parameters.html#label-error-on-nondeterministic-update) = FALSE, the statement randomly updates the single row in `target` using
>   values from one of the following rows in `src`:
>
>   > `(0, 11)` , `(0, 12)` , `(0,13)`
> * With [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](../parameters.html#label-error-on-nondeterministic-update) = TRUE, an error is returned reporting a duplicate DML row `[0, 10]`.

To avoid this nondeterministic behavior and error, use a 1-to-1 join:

> ```
> UPDATE target SET v = b.v
>   FROM (SELECT k, MIN(v) v FROM src GROUP BY k) b
>   WHERE target.k = b.k;
> ```
>
> Copy
>
> This statement results in the single row in `target` updated to `(0, 11)` (values from the row with the minimum value for
> `v` in `src`) and will never result in an error.

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