---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:57:33.598167+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/with.html
title: WITH | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)WITH

Categories:
:   [Query syntax](../constructs)

# WITH[¶](#with "Link to this heading")

The WITH clause is an optional clause that precedes the body of the [SELECT](../sql/select) statement, and defines one
or more [CTEs (common table expressions)](../../user-guide/queries-cte) that can be used later in the statement. For example,
CTEs can be referenced in the [FROM](from) clause.

Note

You can use a WITH clause when creating and calling an anonymous procedure similar to a stored procedure. That clause modifies
a CALL command rather than a SELECT command. For more information, see [CALL (with anonymous procedure)](../sql/call-with).

The WITH clause is used with machine learning model objects to create an alias to a specific version of the model,
which can then be used to call the methods of that version. See [Calling model methods](../commands-model-function.html#label-snowpark-model-registry-model-methods).

See also:
:   [CONNECT BY](connect-by), [Model commands](../commands-model)

## Syntax[¶](#syntax "Link to this heading")

Subquery:

```
[ WITH
       <cte_name1> [ ( <cte_column_list> ) ] AS ( SELECT ...  )
   [ , <cte_name2> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
   [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
]
SELECT ...
```

Copy

Recursive CTE:

```
[ WITH [ RECURSIVE ]
       <cte_name1> ( <cte_column_list> ) AS ( anchorClause UNION ALL recursiveClause )
   [ , <cte_name2> ( <cte_column_list> ) AS ( anchorClause UNION ALL recursiveClause ) ]
   [ , <cte_nameN> ( <cte_column_list> ) AS ( anchorClause UNION ALL recursiveClause ) ]
]
SELECT ...
```

Copy

Where:

> ```
> anchorClause ::=
>     SELECT <anchor_column_list> FROM ...
>
> recursiveClause ::=
>     SELECT <recursive_column_list> FROM ... [ JOIN ... ]
> ```
>
> Copy

## Parameters[¶](#parameters "Link to this heading")

`cte_name1` , `cte_nameN`
:   The CTE name must follow the rules for views and similar [object identifiers](../identifiers).

`cte_column_list`
:   The names of the columns in the CTE (common table expression).

`anchor_column_list`
:   The columns used in the anchor clause for the recursive CTE. The columns in this list must
    correspond to the columns defined in `cte_column_list`.

`recursive_column_list`
:   The columns used in the recursive clause for the recursive CTE. The columns in this list must
    correspond to the columns defined in `cte_column_list`.

For more details, see [Anchor Clause](#anchor-clause) and [Recursive Clause](#recursive-clause) (in this topic). For a detailed
explanation of how the anchor clause and recursive clause work together, see
[Working with CTEs (Common Table Expressions)](../../user-guide/queries-cte).

## Usage notes[¶](#usage-notes "Link to this heading")

### General usage[¶](#general-usage "Link to this heading")

* A WITH clause can refer recursively to itself, and to other CTEs that appear earlier in the same clause. For instance,
  `cte_name2` can refer to `cte_name1` and itself, while `cte_name1` can refer to itself, but not to
  `cte_name2`.
* You can mix recursive and non-recursive (iterative and non-iterative) CTE clauses in the WITH clause. The CTE clauses should
  be ordered such that, if a CTE needs to reference another CTE, the CTE to be referenced should be defined earlier in the
  statement (e.g. the second CTE can refer to the first CTE, but not vice versa).

  The CTEs do not need to be listed in order based on whether they are recursive or not. For example, a non-recursive CTE can
  be listed immediately after the keyword `RECURSIVE`, and a recursive CTE can come after that non-recursive CTE.

  Within a recursive CTE, either the anchor clause or the recursive clause (or both) can refer to another CTE(s).
* For recursive CTEs, the `cte_column_list` is required.
* For non-recursive CTEs, the `cte_column_list` is optional.
* Make sure to use `UNION ALL`, not `UNION`, in a recursive CTE.
* The keyword `RECURSIVE` is optional.

  > + CTEs can be recursive whether or not `RECURSIVE` was specified.
  > + You can use the keyword `RECURSIVE` even if no CTEs are recursive.
  > + If `RECURSIVE` is used, it must be used only once, even if more than one CTE is recursive.
  >
  > Although SQL statements work properly with or without the keyword `RECURSIVE`, using the keyword properly makes the
  > code easier to understand and maintain. Snowflake recommends using the keyword `RECURSIVE` if one or more CTEs are
  > recursive, and Snowflake strongly recommends omitting the keyword if none of the CTEs are recursive.

Attention

When using a recursive CTE, it is possible to create a query that goes into an infinite loop and consumes credits until the
query succeeds, the query times out (e.g. exceeds the number of seconds specified by the
[STATEMENT\_TIMEOUT\_IN\_SECONDS](../parameters.html#label-statement-timeout-in-seconds) parameter), or you [cancel the query](../../user-guide/querying-cancel-statements).

For information on how infinite loops can occur and for guidelines on how to avoid this problem, see
[Troubleshooting a Recursive CTE](../../user-guide/queries-cte.html#label-recursive-common-table-expression-troubleshoot).

For example, to limit the number of iterations to less than 10:

```
WITH cte AS (
  SELECT ..., 1 as level ...

  UNION ALL

  SELECT ..., cte.level + 1 as level
   FROM cte ...
   WHERE ... level < 10
) ...
```

Copy

### Limitations[¶](#limitations "Link to this heading")

* The Snowflake implementation of recursive CTEs does not support the following keywords that some other systems support:

  + `SEARCH DEPTH FIRST BY ...`
  + `CYCLE ... SET ...`

### Anchor clause[¶](#anchor-clause "Link to this heading")

The anchor clause in a recursive CTE is a [SELECT](../sql/select) statement.

The anchor clause is executed once during the execution of the statement in which it is embedded; it runs before the
recursive clause and generates the first set of rows from the recursive CTE. These rows are not only included in the output
of the query, but also referenced by the recursive clause.

The anchor clause can contain any SQL construct allowed in a SELECT clause. However, the anchor clause cannot reference
`cte_name1`; only the recursive clause can reference `cte_name1`.

Although the anchor clause usually selects from the same table as the recursive clause, this is not required. The anchor
clause can select from any table-like data source, including another table, a view, a UDTF, or a constant value.

The anchor clause selects a single “level” of the hierarchy, typically the top level, or the highest level of interest. For
example, if the query is intended to show the “parts explosion” of a car, the anchor clause returns the highest level component,
which is the car itself.

The output from the anchor clause represents one layer of the hierarchy, and this layer is stored as the content of the “view”
that is accessed in the first iteration of the recursive clause.

### Recursive clause[¶](#recursive-clause "Link to this heading")

The recursive clause is a [SELECT](../sql/select) statement. This SELECT is restricted to projections, filters, and
joins (inner joins and outer joins in which the recursive reference is on the preserved side of the outer join). The recursive
clause cannot contain:

* Aggregate or window functions,
* `GROUP BY`, `ORDER BY`, `LIMIT`, or `DISTINCT`.

The recursive clause can (and usually does) reference the `cte_name1` as though the CTE were a table or view.

The recursive clause usually includes a JOIN that joins the table that was used in the anchor clause to the CTE. However, the
JOIN can join more than one table or table-like data source (view, etc.).

The first iteration of the recursive clause starts with the data from the anchor clause. That data is then joined to the other
table(s) in the FROM clause of the recursive clause.

Each subsequent iteration starts with the data from the previous iteration.

You can think of the CTE clause or “view” as holding the contents from the previous iteration, so that those contents are available
to be joined. Note that during any one iteration, the CTE contains only the contents from the previous iteration, not the results accumulated
from all previous iterations. The accumulated results (including from the anchor clause) are
stored in a separate place.

### Column lists in a recursive CTE[¶](#column-lists-in-a-recursive-cte "Link to this heading")

There are three column lists in a recursive CTE:

* `cte_column_list`
* `anchor_column_list` (in the anchor clause)
* `recursive_column_list` (in the recursive clause)

A recursive CTE can contain other column lists (e.g. in a subquery), but these three column lists must be present.

These three column lists must all correspond to each other.

In pseudo-code, this looks similar to:

```
WITH RECURSIVE cte_name (X, Y) AS
(
  SELECT related_to_X, related_to_Y FROM table1
  UNION ALL
  SELECT also_related_to_X, also_related_to_Y
    FROM table1 JOIN cte_name ON <join_condition>
)
SELECT ... FROM ...
```

Copy

Columns `X` and `related_to_X` must correspond; the anchor clause generates the initial “contents” of the “view” that the
CTE represents, so each column from the anchor clause (e.g. column `related_to_x`) must generate output that will belong in
the corresponding column of the CTE (e.g. column `X`).

Columns `also_related_to_X` and `X` must correspond; on each iteration of the recursive clause, the output of that clause
becomes the new content of the CTE/view for the next iteration.

Also, columns `related_to_X` and `also_related_to_X` must correspond because they are each on one side of the `UNION ALL`
operator, and the columns on each side of a `UNION ALL` operator must correspond.

## Examples[¶](#examples "Link to this heading")

### Non-recursive examples[¶](#non-recursive-examples "Link to this heading")

This section provides sample queries and sample output. To keep the examples short, the code omits the statements to create
and load the tables.

This first example uses a simple WITH clause as a view to extract a subset of data, in this case the music albums that were
released in 1976. For this small database, the query output is the albums “Amigos” and “Look Into The Future”, both from the
year 1976:

> ```
> with
>   albums_1976 as (select * from music_albums where album_year = 1976)
> select album_name from albums_1976 order by album_name;
> +----------------------+
> | ALBUM_NAME           |
> |----------------------|
> | Amigos               |
> | Look Into The Future |
> +----------------------+
> ```
>
> Copy

This next example uses a WITH clause with an earlier WITH clause; the CTE named `journey_album_info_1976` uses the CTE named
`album_info_1976`. The output is the album “Look Into The Future”, with the name of the band:

> ```
> with
>    album_info_1976 as (select m.album_ID, m.album_name, b.band_name
>       from music_albums as m inner join music_bands as b
>       where m.band_id = b.band_id and album_year = 1976),
>    Journey_album_info_1976 as (select *
>       from album_info_1976 
>       where band_name = 'Journey')
> select album_name, band_name 
>    from Journey_album_info_1976;
> +----------------------+-----------+
> | ALBUM_NAME           | BAND_NAME |
> |----------------------+-----------|
> | Look Into The Future | Journey   |
> +----------------------+-----------+
> ```
>
> Copy

This example lists musicians who played on Santana albums and Journey albums. This example does not use the WITH clause.
For this query (and the next few queries, all of which are equivalent ways of running the same query), the output is the IDs and
names of musicians who played on Santana albums and Journey albums:

> ```
> select distinct musicians.musician_id, musician_name
>  from musicians inner join musicians_and_albums inner join music_albums inner join music_bands
>  where musicians.musician_ID = musicians_and_albums.musician_ID
>    and musicians_and_albums.album_ID = music_albums.album_ID
>    and music_albums.band_ID = music_bands.band_ID
>    and music_bands.band_name = 'Santana'
> intersect
> select distinct musicians.musician_id, musician_name
>  from musicians inner join musicians_and_albums inner join music_albums inner join music_bands
>  where musicians.musician_ID = musicians_and_albums.musician_ID
>    and musicians_and_albums.album_ID = music_albums.album_ID
>    and music_albums.band_ID = music_bands.band_ID
>    and music_bands.band_name = 'Journey'
> order by musician_ID;
> +-------------+---------------+
> | MUSICIAN_ID | MUSICIAN_NAME |
> |-------------+---------------|
> |         305 | Gregg Rolie   |
> |         306 | Neal Schon    |
> +-------------+---------------+
> ```
>
> Copy

As you can see, the previous query contains duplicate code. The next few examples show how to simplify this query by using
one or more explicit views, and then how to simplify it by using CTEs.

This query shows how to use views to reduce the duplication and complexity of the previous example (as in the previous example,
this does not use a WITH clause):

> ```
> create or replace view view_musicians_in_bands AS
>   select distinct musicians.musician_id, musician_name, band_name
>     from musicians inner join musicians_and_albums inner join music_albums inner join music_bands
>     where musicians.musician_ID = musicians_and_albums.musician_ID
>       and musicians_and_albums.album_ID = music_albums.album_ID
>       and music_albums.band_ID = music_bands.band_ID;
> ```
>
> Copy
>
> With this view, you can re-write the original query as:
>
> ```
> select musician_id, musician_name from view_musicians_in_bands where band_name = 'Santana'
> intersect
> select musician_id, musician_name from view_musicians_in_bands where band_name = 'Journey'
> order by musician_ID;
> +-------------+---------------+
> | MUSICIAN_ID | MUSICIAN_NAME |
> |-------------+---------------|
> |         305 | Gregg Rolie   |
> |         306 | Neal Schon    |
> +-------------+---------------+
> ```
>
> Copy

This example uses a WITH clause to do the equivalent of what the preceding query did:

> ```
> with
>   musicians_in_bands as (
>      select distinct musicians.musician_id, musician_name, band_name
>       from musicians inner join musicians_and_albums inner join music_albums inner join music_bands
>       where musicians.musician_ID = musicians_and_albums.musician_ID
>         and musicians_and_albums.album_ID = music_albums.album_ID
>         and music_albums.band_ID = music_bands.band_ID)
> select musician_ID, musician_name from musicians_in_bands where band_name = 'Santana'
> intersect
> select musician_ID, musician_name from musicians_in_bands where band_name = 'Journey'
> order by musician_ID
>   ;
> +-------------+---------------+
> | MUSICIAN_ID | MUSICIAN_NAME |
> |-------------+---------------|
> |         305 | Gregg Rolie   |
> |         306 | Neal Schon    |
> +-------------+---------------+
> ```
>
> Copy

These statements create more granular views (this example does not use a WITH clause):

> List the albums by a particular band:
>
> ```
> create or replace view view_album_IDs_by_bands AS
>  select album_ID, music_bands.band_id, band_name
>   from music_albums inner join music_bands
>   where music_albums.band_id = music_bands.band_ID;
> ```
>
> Copy
>
> List the musicians who played on albums:
>
> ```
> create or replace view view_musicians_in_bands AS
>  select distinct musicians.musician_id, musician_name, band_name
>   from musicians inner join musicians_and_albums inner join view_album_IDs_by_bands
>   where musicians.musician_ID = musicians_and_albums.musician_ID
>     and musicians_and_albums.album_ID = view_album_IDS_by_bands.album_ID;
> ```
>
> Copy
>
> Now use those views to query musicians who played on both Santana and Journey albums:
>
> ```
> select musician_id, musician_name from view_musicians_in_bands where band_name = 'Santana'
> intersect
> select musician_id, musician_name from view_musicians_in_bands where band_name = 'Journey'
> order by musician_ID;
> +-------------+---------------+
> | MUSICIAN_ID | MUSICIAN_NAME |
> |-------------+---------------|
> |         305 | Gregg Rolie   |
> |         306 | Neal Schon    |
> +-------------+---------------+
> ```
>
> Copy

These statements create more granular implicit views (this example uses a WITH clause):

> ```
> with
>   album_IDs_by_bands as (select album_ID, music_bands.band_id, band_name
>                           from music_albums inner join music_bands
>                           where music_albums.band_id = music_bands.band_ID),
>   musicians_in_bands as (select distinct musicians.musician_id, musician_name, band_name
>                           from musicians inner join musicians_and_albums inner join album_IDs_by_bands
>                           where musicians.musician_ID = musicians_and_albums.musician_ID
>                             and musicians_and_albums.album_ID = album_IDS_by_bands.album_ID)
> select musician_ID, musician_name from musicians_in_bands where band_name = 'Santana'
> intersect
> select musician_ID, musician_name from musicians_in_bands where band_name = 'Journey'
> order by musician_ID
>   ;
> +-------------+---------------+
> | MUSICIAN_ID | MUSICIAN_NAME |
> |-------------+---------------|
> |         305 | Gregg Rolie   |
> |         306 | Neal Schon    |
> +-------------+---------------+
> ```
>
> Copy

### Recursive examples[¶](#recursive-examples "Link to this heading")

This is a basic example of using a recursive CTE to generate a Fibonacci series:

> ```
> WITH RECURSIVE current_f (current_val, previous_val) AS
>     (
>     SELECT 0, 1
>     UNION ALL 
>     SELECT current_val + previous_val, current_val FROM current_f
>       WHERE current_val + previous_val < 100
>     )
>   SELECT current_val FROM current_f ORDER BY current_val;
> +-------------+
> | CURRENT_VAL |
> |-------------|
> |           0 |
> |           1 |
> |           1 |
> |           2 |
> |           3 |
> |           5 |
> |           8 |
> |          13 |
> |          21 |
> |          34 |
> |          55 |
> |          89 |
> +-------------+
> ```
>
> Copy

This example is a query with a recursive CTE that shows a “parts explosion” for an automobile:

> ```
> -- The components of a car.
> CREATE TABLE components (
>     description VARCHAR,
>     component_ID INTEGER,
>     quantity INTEGER,
>     parent_component_ID INTEGER
>     );
>
> INSERT INTO components (description, quantity, component_ID, parent_component_ID) VALUES
>     ('car', 1, 1, 0),
>        ('wheel', 4, 11, 1),
>           ('tire', 1, 111, 11),
>           ('#112 bolt', 5, 112, 11),
>           ('brake', 1, 113, 11),
>              ('brake pad', 1, 1131, 113),
>        ('engine', 1, 12, 1),
>           ('piston', 4, 121, 12),
>           ('cylinder block', 1, 122, 12),
>           ('#112 bolt', 16, 112, 12)   -- Can use same type of bolt in multiple places
>     ;
> ```
>
> Copy
>
> ```
> WITH RECURSIVE current_layer (indent, layer_ID, parent_component_ID, component_id, description, sort_key) AS (
>   SELECT 
>       '...', 
>       1, 
>       parent_component_ID, 
>       component_id, 
>       description, 
>       '0001'
>     FROM components WHERE component_id = 1
>   UNION ALL
>   SELECT indent || '...',
>       layer_ID + 1,
>       components.parent_component_ID,
>       components.component_id, 
>       components.description,
>       sort_key || SUBSTRING('000' || components.component_ID, -4)
>     FROM current_layer JOIN components 
>       ON (components.parent_component_id = current_layer.component_id)
>   )
> SELECT
>   -- The indentation gives us a sort of "side-ways tree" view, with
>   -- sub-components indented under their respective components.
>   indent || description AS description, 
>   component_id,
>   parent_component_ID
>   -- The layer_ID and sort_key are useful for debugging, but not
>   -- needed in the report.
> --  , layer_ID, sort_key
>   FROM current_layer
>   ORDER BY sort_key;
> +-------------------------+--------------+---------------------+
> | DESCRIPTION             | COMPONENT_ID | PARENT_COMPONENT_ID |
> |-------------------------+--------------+---------------------|
> | ...car                  |            1 |                   0 |
> | ......wheel             |           11 |                   1 |
> | .........tire           |          111 |                  11 |
> | .........#112 bolt      |          112 |                  11 |
> | .........brake          |          113 |                  11 |
> | ............brake pad   |         1131 |                 113 |
> | ......engine            |           12 |                   1 |
> | .........#112 bolt      |          112 |                  12 |
> | .........piston         |          121 |                  12 |
> | .........cylinder block |          122 |                  12 |
> +-------------------------+--------------+---------------------+
> ```
>
> Copy

For more examples, see [Working with CTEs (Common Table Expressions)](../../user-guide/queries-cte).

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