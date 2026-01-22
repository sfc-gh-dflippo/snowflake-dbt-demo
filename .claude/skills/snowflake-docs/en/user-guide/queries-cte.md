---
auto_generated: true
description: CONNECT BY , WITH
last_scraped: '2026-01-14T16:55:25.954193+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/queries-cte
title: Working with CTEs (Common Table Expressions) | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](tables-iceberg.md)
      - [Snowflake Open Catalog](opencatalog/overview.md)
11. Data engineering

    - [Data loading](../guides/overview-loading-data.md)
    - [Dynamic Tables](dynamic-tables-about.md)
    - [Streams and Tasks](data-pipelines-intro.md)
    - [dbt Projects on Snowflake](data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](../guides/overview-queries.md)

    * [Joins](querying-joins.md)
    * [Subqueries](querying-subqueries.md)
    * [Querying Hierarchical Data](queries-hierarchical.md)
    * [Common Table Expressions (CTE)](queries-cte.md)")
    * [Querying Semi-structured Data](querying-semistructured.md)
    * [Using full-text search](querying-with-search-functions.md)
    * [Constructing SQL at Runtime](querying-construct-at-runtime.md)
    * [Analyzing time-series data](querying-time-series-data.md)
    * [Analyzing data with window functions](functions-window-using.md)
    * [Match Recognize](match-recognize-introduction.md)
    * [Sequences](querying-sequences.md)
    * [Persisted Query Results](querying-persisted-results.md)
    * [Distinct Counts](querying-distinct-counts.md)
    * [Similarity Estimation](querying-approximate-similarity.md)
    * [Frequency Estimation](querying-approximate-frequent-values.md)
    * [Estimating Percentile Values](querying-approximate-percentile-values.md)
    * [Monitor query activity with Query History](ui-snowsight-activity.md)
    * [Using query insights to improve performance](query-insights.md)
    * [Query Hash](query-hash.md)
    * [Top-K pruning](querying-top-k-pruning-optimization.md)
    * [Cancel Statements](querying-cancel-statements.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](../guides/overview-sharing.md)
19. [Snowflake AI & ML](../guides/overview-ai-features.md)
21. [Snowflake Postgres](snowflake-postgres/about.md)
23. [Alerts & Notifications](../guides/overview-alerts.md)
25. [Security](../guides/overview-secure.md)
26. [Data Governance](../guides/overview-govern.md)
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Queries](../guides/overview-queries.md)Common Table Expressions (CTE)

# Working with CTEs (Common Table Expressions)[¶](#working-with-ctes-common-table-expressions "Link to this heading")

See also:
:   [CONNECT BY](../sql-reference/constructs/connect-by) , [WITH](../sql-reference/constructs/with)

## What is a CTE?[¶](#what-is-a-cte "Link to this heading")

A CTE (common table expression) is a named subquery defined in a [WITH](../sql-reference/constructs/with) clause. You can
think of the CTE as a temporary [view](views-introduction) for use in the statement that defines the
CTE. The CTE defines the temporary view’s name, an optional list of column names, and a query expression (i.e. a SELECT
statement). The result of the query expression is effectively a table. Each column of that table corresponds to a column
in the (optional) list of column names.

The following code is an example of a query that uses a CTE:

```
WITH
    my_cte (cte_col_1, cte_col_2) AS (
        SELECT col_1, col_2
            FROM ...
    )
SELECT ... FROM my_cte;
```

Copy

In the example above, the CTE starts on the line containing `my_cte (cte_col_1, cte_col_2) AS (`, and ends on the line containing
`)`.

Avoid choosing CTE names that match the following:

* [SQL function names](../sql-reference/functions-all)
* Tables, views, or materialized views. If a query defines a CTE with a particular name, the CTE takes precedence over tables, etc.

A CTE can be recursive or non-recursive. A recursive CTE is a CTE that references itself. A recursive CTE can join a
table to itself as many times as necessary to process hierarchical data in the table.

CTEs increase modularity and simplify maintenance.

## Recursive CTEs and Hierarchical Data[¶](#recursive-ctes-and-hierarchical-data "Link to this heading")

Recursive CTEs enable you to process hierarchical data, such as a parts explosion (component, sub-components) or a
management hierarchy (manager, employees). For more information about hierarchical data, and other ways to query
hierarchical data, see [Querying Hierarchical Data](queries-hierarchical).

A recursive CTE allows you to join all the levels of a hierarchy without knowing in advance how many levels there are.

### Overview of Recursive CTE Syntax[¶](#overview-of-recursive-cte-syntax "Link to this heading")

This section provides an overview of the syntax and how the syntax relates to the way that the recursion works:

```
WITH [ RECURSIVE ] <cte_name> AS
(
  <anchor_clause> UNION ALL <recursive_clause>
)
SELECT ... FROM ...;
```

Copy

Where:
:   `anchor_clause`
    :   Selects an initial row or set of rows that represent the top of the hierarchy. For
        example, if you are trying to display all the employees in a company, the anchor clause would select the President
        of the company.

        The anchor clause is a [SELECT](../sql-reference/sql/select) statement and can contain any supported SQL constructs.
        The anchor clause cannot reference the `cte_name`.

    `recursive_clause`
    :   Selects the next layer of the hierarchy based on the previous layer. In the first iteration, the previous layer is the
        result set from the anchor clause. In subsequent iterations, the previous layer is the most recent completed iteration.

        The `recursive_clause` is a [SELECT](../sql-reference/sql/select) statement; however, the statement is restricted
        to projections, joins, and filters. In addition, the following are not allowed in the statement:

        * Aggregate or window functions.
        * `GROUP BY`, `ORDER BY`, `LIMIT`, or `DISTINCT`.

        The recursive clause can reference the `cte_name` like a regular table or view.

For a more detailed description of the syntax, see [WITH](../sql-reference/constructs/with).

Logically, the recursive CTE is evaluated as follows:

1. The `anchor_clause` is evaluated and its result is written to both the final result set and to a working table.
   The `cte_name` is effectively an alias to the working table; in other words, a query referencing the
   `cte_name` reads from the working table.
2. While the working table is not empty:

   1. The `recursive_clause` is evaluated, using the current contents of the working table wherever `cte_name`
      is referenced.
   2. The result of `recursive_clause` is written to both the final result set and a temp table.
   3. The working table is overwritten by the content of the temp table.

Effectively, the output of the previous iteration is stored in a working table named `cte_name`, and that table is
then one of the inputs to the next iteration. The working table contains only the result of the most recent iteration.
The accumulated results from all iterations so far are stored elsewhere.

After the final iteration, the accumulated results are available to the main SELECT statement by referencing `cte_name`.

### Recursive CTE Considerations[¶](#recursive-cte-considerations "Link to this heading")

#### Potential for Infinite Loops[¶](#potential-for-infinite-loops "Link to this heading")

Constructing a recursive CTE incorrectly can cause an infinite loop. In these cases, the query continues to run until the query
succeeds, the query times out (e.g. exceeds the number of seconds specified by the
[STATEMENT\_TIMEOUT\_IN\_SECONDS](../sql-reference/parameters.html#label-statement-timeout-in-seconds) parameter), or you [cancel the query](querying-cancel-statements).

For information on how infinite loops can occur and for guidelines on how to avoid this problem, see
[Troubleshooting a Recursive CTE](#label-recursive-common-table-expression-troubleshoot).

#### Non-Contiguous Hierarchies[¶](#non-contiguous-hierarchies "Link to this heading")

This topic described hierarchies and how parent-child relationships can be used by recursive CTEs. In all of the examples
in this topic, the hierarchies are contiguous.

For information about non-contiguous hierarchies, see [Querying Hierarchical Data](queries-hierarchical).

## Examples[¶](#examples "Link to this heading")

This section includes both non-recursive and recursive CTEs examples to contrast the two types.

### Non-Recursive, Two-Level, Self-joining CTE[¶](#non-recursive-two-level-self-joining-cte "Link to this heading")

This example uses a table of employees and managers:

> ```
> CREATE OR REPLACE TABLE employees (title VARCHAR, employee_ID INTEGER, manager_ID INTEGER);
> ```
>
> Copy
>
> ```
> INSERT INTO employees (title, employee_ID, manager_ID) VALUES
>     ('President', 1, NULL),  -- The President has no manager.
>         ('Vice President Engineering', 10, 1),
>             ('Programmer', 100, 10),
>             ('QA Engineer', 101, 10),
>         ('Vice President HR', 20, 1),
>             ('Health Insurance Analyst', 200, 20);
> ```
>
> Copy

A two-level self-join of this employee table looks like:

> ```
> SELECT
>      emps.title,
>      emps.employee_ID,
>      mgrs.employee_ID AS MANAGER_ID, 
>      mgrs.title AS "MANAGER TITLE"
>   FROM employees AS emps LEFT OUTER JOIN employees AS mgrs
>     ON emps.manager_ID = mgrs.employee_ID
>   ORDER BY mgrs.employee_ID NULLS FIRST, emps.employee_ID;
> +----------------------------+-------------+------------+----------------------------+
> | TITLE                      | EMPLOYEE_ID | MANAGER_ID | MANAGER TITLE              |
> |----------------------------+-------------+------------+----------------------------|
> | President                  |           1 |       NULL | NULL                       |
> | Vice President Engineering |          10 |          1 | President                  |
> | Vice President HR          |          20 |          1 | President                  |
> | Programmer                 |         100 |         10 | Vice President Engineering |
> | QA Engineer                |         101 |         10 | Vice President Engineering |
> | Health Insurance Analyst   |         200 |         20 | Vice President HR          |
> +----------------------------+-------------+------------+----------------------------+
> ```
>
> Copy

The query above shows all the employees. Each manager’s employees appear near their manager in the report. However, the
report doesn’t visually show the hierarchy. Without looking carefully at the data, you don’t know how many levels there
are in the organization, and you need to read each row in order to see which employees are associated with a specific
manager.

A recursive CTE can display this hierarchical data as a sideways tree, as shown in the next section.

### Recursive CTE with Indented Output[¶](#recursive-cte-with-indented-output "Link to this heading")

Below are two examples of using a recursive CTE:

* The first uses indentation to show the different levels of the hierarchy. To simplify this example, the code does not
  produce the rows in a particular order.
* The second example uses indentation and shows each manager’s employees immediately below their manager.

#### Unordered Output[¶](#unordered-output "Link to this heading")

Here is the first example.

```
WITH RECURSIVE managers                                     -- Line 1
    (indent, employee_ID, manager_ID, employee_title)       -- Line 2
  AS                                                        -- Line 3
    (                                                       -- Line 4
                                                            -- Line 5
      SELECT '' AS indent,                                  -- Line 6
             employee_ID,                                   -- Line 7
             manager_ID,                                    -- Line 8
             title AS employee_title                        -- Line 9
        FROM employees                                      -- Line 10
        WHERE title = 'President'                           -- Line 11
                                                            -- Line 12
        UNION ALL                                           -- Line 13
                                                            -- Line 14
        SELECT indent || '--- ',                            -- Line 15
               employees.employee_ID,                       -- Line 16
               employees.manager_ID,                        -- Line 17
               employees.title                              -- Line 18
          FROM employees JOIN managers                      -- Line 19
            ON employees.manager_ID = managers.employee_ID  -- Line 20
    )                                                       -- Line 21
                                                            -- Line 22
SELECT indent || employee_title AS Title,                   -- Line 23
       employee_ID,                                         -- Line 24
       manager_ID                                           -- Line 25
  FROM managers;                                            -- Line 26
```

Copy

The query includes the following sections:

* Line 2 contains the column names for the “view” (CTE).
* Lines 4 - 21 contain the CTE.
* Lines 6 - 11 contain the anchor clause of the CTE.
* Lines 15 - 21 contain the recursive clause of the CTE.
* Lines 23 - 26 contain the main SELECT that uses the CTE as a view. This SELECT references:

  + The CTE name (`managers`), defined in line 1.
  + The CTE’s columns (`indent`, `employee_id`, etc.) defined in line 2.

The CTE contains two SELECT statements:

* The SELECT statement in the anchor clause is executed once and provides the set of rows from the
  first (top) level of the hierarchy.
* The SELECT in the recursive clause can reference the CTE. You can think of the query as
  iterating, with each iteration building on the previous iterations’ query results.

In the manager/employee example, the anchor clause emits the first row, which is the row that describes the company
president.

In the next iteration of the recursive clause, the recursive clause finds all the rows whose manager is the company
president (i.e. it finds all of the vice presidents). The 3rd iteration finds all the employees whose manager is one
of the vice presidents. Iteration continues until there is an iteration in which all of the rows retrieved are rows of
leaf-level employees who do not manage anyone. The statement does one more iteration, looking for (but not finding)
any employees whose managers are leaf-level employees. That iteration produces 0 rows, and the iteration stops.

Throughout these iterations, the UNION ALL clause accumulates the results. The results of each iteration are added
to the results of the previous iterations. After the last iteration completes, the accumulated rows (like any rows
produced in a WITH clause) are made available to the main SELECT clause in the query. That main SELECT can then query
those rows.

This particular example query uses indentation to show the hierarchical nature of the data. If you look at the output,
you see that the lower the level of the employee, the further that employee’s data is indented.

The indentation is controlled by the column named `indent`. The indentation starts at 0 characters (an empty string
in the anchor clause), and increases by 4 characters (`---`) for each iteration (i.e. for each level in the hierarchy).

Not surprisingly, it is very important to construct the join(s) correctly, and to select the correct columns in the
recursive clause. The columns in the SELECT of the recursive clause must correspond correctly to the columns in
the anchor clause. Remember that the query starts with the President, then selects the Vice Presidents, and then
selects the people who report directly to the Vice Presidents, etc. Each iteration looks for employees whose
`manager_id` field corresponds to one of the `managers.employee_id` values produced in the previous iteration.

Expressed another way, the employee ID in the managers “view” is the manager ID for the next level of employees. The
employee IDs must progress downward through the hierarchy (President, Vice President, senior manager, junior manager, etc.)
during each iteration. If the employee IDs don’t progress, then the query can loop infinitely (if the same `manager_ID`
keeps appearing in the `managers.employee_ID` column in different iterations), or skip a level, or fail in other ways.

#### Ordered Output[¶](#ordered-output "Link to this heading")

The previous example had no ORDER BY clause, so even though each employee’s record is indented properly, each employee did
not necessarily appear directly underneath their manager. The example below generates output with correct indentation, and
with each manager’s employees directly underneath their manager.

The query’s ORDER BY clause uses an additional column, named `sort_key`. The sort key accumulates as the recursive clause
iterates; you can think of the sort key as a string that contains the entire chain of command above you (your manager, your
manager’s manager, etc.). The most senior person in that chain of command (the President) is at the beginning of the sort
key string. Although you normally wouldn’t display the sort key, the query below includes the sort key in the output so that
it is easier to understand the output.

Each iteration should increase the length of the sort key by the same amount (same number of characters), so the query uses
a UDF (user-defined function) named `skey`, with the following definition, to generate consistent-length segments of the
sort key:

> > ```
> > CREATE OR REPLACE FUNCTION skey(ID VARCHAR)
> >   RETURNS VARCHAR
> >   AS
> >   $$
> >     SUBSTRING('0000' || ID::VARCHAR, -4) || ' '
> >   $$
> >   ;
> > ```
> >
> > Copy
>
> Here is an example of output from the `SKEY` function:
>
> > ```
> > SELECT skey(12);
> > +----------+
> > | SKEY(12) |
> > |----------|
> > | 0012     |
> > +----------+
> > ```
> >
> > Copy

Here is the final version of the query. This puts each manager’s employees immediately underneath that manager, and indents based
on the “level” of the employee:

> ```
> WITH RECURSIVE managers 
>       -- Column list of the "view"
>       (indent, employee_ID, manager_ID, employee_title, sort_key) 
>     AS 
>       -- Common Table Expression
>       (
>         -- Anchor Clause
>         SELECT '' AS indent, 
>             employee_ID, manager_ID, title AS employee_title, skey(employee_ID)
>           FROM employees
>           WHERE title = 'President'
>
>         UNION ALL
>
>         -- Recursive Clause
>         SELECT indent || '--- ',
>             employees.employee_ID, employees.manager_ID, employees.title, 
>             sort_key || skey(employees.employee_ID)
>           FROM employees JOIN managers 
>             ON employees.manager_ID = managers.employee_ID
>       )
>
>   -- This is the "main select".
>   SELECT 
>          indent || employee_title AS Title, employee_ID, 
>          manager_ID, 
>          sort_key
>     FROM managers
>     ORDER BY sort_key
>   ;
> +----------------------------------+-------------+------------+-----------------+
> | TITLE                            | EMPLOYEE_ID | MANAGER_ID | SORT_KEY        |
> |----------------------------------+-------------+------------+-----------------|
> | President                        |           1 |       NULL | 0001            |
> | --- Vice President Engineering   |          10 |          1 | 0001 0010       |
> | --- --- Programmer               |         100 |         10 | 0001 0010 0100  |
> | --- --- QA Engineer              |         101 |         10 | 0001 0010 0101  |
> | --- Vice President HR            |          20 |          1 | 0001 0020       |
> | --- --- Health Insurance Analyst |         200 |         20 | 0001 0020 0200  |
> +----------------------------------+-------------+------------+-----------------+
> ```
>
> Copy

The next query shows how to reference a field from the previous (higher) level in the hierarchy; pay particular attention to the
`mgr_title` column:

> ```
> WITH RECURSIVE managers 
>       -- Column names for the "view"/CTE
>       (employee_ID, manager_ID, employee_title, mgr_title) 
>     AS
>       -- Common Table Expression
>       (
>
>         -- Anchor Clause
>         SELECT employee_ID, manager_ID, title AS employee_title, NULL AS mgr_title
>           FROM employees
>           WHERE title = 'President'
>
>         UNION ALL
>
>         -- Recursive Clause
>         SELECT 
>             employees.employee_ID, employees.manager_ID, employees.title, managers.employee_title AS mgr_title
>           FROM employees JOIN managers 
>             ON employees.manager_ID = managers.employee_ID
>       )
>
>   -- This is the "main select".
>   SELECT employee_title AS Title, employee_ID, manager_ID, mgr_title
>     FROM managers
>     ORDER BY manager_id NULLS FIRST, employee_ID
>   ;
> +----------------------------+-------------+------------+----------------------------+
> | TITLE                      | EMPLOYEE_ID | MANAGER_ID | MGR_TITLE                  |
> |----------------------------+-------------+------------+----------------------------|
> | President                  |           1 |       NULL | NULL                       |
> | Vice President Engineering |          10 |          1 | President                  |
> | Vice President HR          |          20 |          1 | President                  |
> | Programmer                 |         100 |         10 | Vice President Engineering |
> | QA Engineer                |         101 |         10 | Vice President Engineering |
> | Health Insurance Analyst   |         200 |         20 | Vice President HR          |
> +----------------------------+-------------+------------+----------------------------+
> ```
>
> Copy

### Parts Explosion[¶](#parts-explosion "Link to this heading")

Manager/employee hierarchies are not the only type of variable-depth hierarchies that you can store in a single table and process
with a recursive CTE. Another common example of hierarchical data is a “parts explosion”, in which each component can be listed with
its sub-components, each of which can be listed with its sub-sub-components.

For example, suppose that your table contains hierarchical data, such as the components of a car. Your car probably contains
components such as an engine, wheels, etc. Many of those components contain sub-components (e.g. an engine might contain a fuel pump).
The fuel pump might contain a motor, tubing, etc. You could list all the components and their sub-components using a recursive CTE.

For an example of a query that produces a parts explosion, see [WITH](../sql-reference/constructs/with).

## Troubleshooting a Recursive CTE[¶](#troubleshooting-a-recursive-cte "Link to this heading")

### Recursive CTE Query Runs Until It Succeeds or Times Out[¶](#recursive-cte-query-runs-until-it-succeeds-or-times-out "Link to this heading")

This issue can be caused by two different scenarios:

* Your data hierarchy might have a cycle.
* You might have created an infinite loop.

#### Cause 1: Cyclic Data Hierarchy[¶](#cause-1-cyclic-data-hierarchy "Link to this heading")

If your data hierarchy contains a cycle (i.e. it is not a true tree), there are multiple possible solutions:

Solution 1.1:
:   If the data is not supposed to contain a cycle, correct the data.

Solution 1.2:
:   Limit the query in some way (e.g. limit the number of rows of output). For example:

    > ```
    > WITH RECURSIVE t(n) AS
    >     (
    >     SELECT 1
    >     UNION ALL
    >     SELECT N + 1 FROM t
    >    )
    >  SELECT n FROM t LIMIT 10;
    > ```
    >
    > Copy

Solution 1.3:
:   Do not use a query that contains a recursive CTE, which expects hierarchical data.

#### Cause 2: Infinite Loop[¶](#cause-2-infinite-loop "Link to this heading")

An infinite loop can happen if the projection clause in the `recursive_clause` outputs a value
from the “parent” (the previous iteration) instead of the “child” (the current iteration) and then the next
iteration uses that value in a join when it should use the current iteration’s value in the join.

The following pseudo-code shows an approximate example of this:

> ```
> CREATE TABLE employees (employee_ID INT, manager_ID INT, ...);
> INSERT INTO employees (employee_ID, manager_ID) VALUES
>         (1, NULL),
>         (2, 1);
>
> WITH cte_name (employee_ID, manager_ID, ...) AS
>   (
>      -- Anchor Clause
>      SELECT employee_ID, manager_ID FROM table1
>      UNION ALL
>      SELECT manager_ID, employee_ID   -- <<< WRONG
>          FROM table1 JOIN cte_name
>            ON table1.manager_ID = cte_name.employee_ID
>   )
> SELECT ...
> ```
>
> Copy

In this example, the recursive clause passes its parent value (`manager_id`) in the column that should have the
current/child value (`employee_id`). The parent will show up as the “current” value in the next iteration, and will
be passed again as the “current” value to the following generation, so the query never progresses down through the
levels; it keeps processing the same level each time.

Step 1:
:   Suppose that the anchor clause selects the values `employee_id = 1` and `manager_id = NULL`.

    CTE:

    > ```
    > employee_ID  manager_ID
    > -----------  ---------
    >       1         NULL
    > ```
    >
    > Copy

Step 2:
:   During the first iteration of the recursive clause, `employee_id = 2` and `manager_id = 1` in `table1`.

    CTE:

    > ```
    > employee_ID  manager_ID
    > -----------  ----------
    >        1         NULL
    > ```
    >
    > Copy

    `table1`:

    > ```
    > employee_ID  manager_ID
    > -----------  ----------
    >  ...
    >        2         1
    >  ...
    > ```
    >
    > Copy

    Result of the join in the recursive clause:

    > ```
    > table1.employee_ID  table1.manager_ID  cte.employee_ID  cte.manager_ID
    > -----------------   -----------------  ---------------  --------------
    >  ...
    >        2                   1                 1                NULL
    >  ...
    > ```
    >
    > Copy

    Projection:

    > ```
    > employee_ID  manager_ID
    > -----------  ----------
    >  ...
    >        2         1
    >  ...
    > ```
    >
    > Copy

    However, because the `employee_id` and `manager_id` columns are reversed in the projection, the actual output of
    the query (and thus the content of the CTE at the start of the next iteration) is:

    > ```
    > employee_ID  manager_ID
    > -----------  ----------
    >  ...
    >        1         2        -- Because manager and employee IDs reversed
    >  ...
    > ```
    >
    > Copy

Step 3:
:   During the second iteration of the recursive clause:

    CTE:

    > ```
    > employee_ID  manager_ID
    > -----------  ----------
    >        1         2
    > ```
    >
    > Copy

    `table1`:

    > ```
    > employee_ID  manager_ID
    > -----------  ----------
    >  ...
    >        2         1
    >  ...
    > ```
    >
    > Copy

    Result of join in recursive clause:

    > ```
    > table1.employee_ID  table1.manager_ID  cte.employee_ID  cte.manager_ID
    > -----------------   -----------------  ---------------  --------------
    >  ...
    >        2                   1                 1                2
    >  ...
    > ```
    >
    > Copy

    Projection:

    > ```
    > employee_ID  manager_ID
    > -----------  ----------
    >  ...
    >        2         1
    >  ...
    > ```
    >
    > Copy

    Result of the query (contents of CTE at start of next iteration):

    > ```
    > employee_ID  manager_ID
    > -----------  ----------
    >  ...
    >        1         2        -- Because manager and employee IDs reversed
    >  ...
    > ```
    >
    > Copy

    As you can see, at the end of the second iteration, the row in the CTE is the same as it was at the start of the
    iteration:

    * `employee_id` is `1`.
    * `manager_id` is `2`.

    Thus, the result of the join during the next iteration will be the same as the result of the join during the current
    iteration, and the query loops infinitely.

If you have created an infinite loop:

Solution 2:
:   Make sure that the recursive clause passes the correct variables in the correct order.

    Also make sure that the JOIN condition in the recursive clause is correct. In a typical case, the parent of the
    “current” row should be joined to the child/current value of the parent row.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [What is a CTE?](#what-is-a-cte)
2. [Recursive CTEs and Hierarchical Data](#recursive-ctes-and-hierarchical-data)
3. [Examples](#examples)
4. [Troubleshooting a Recursive CTE](#troubleshooting-a-recursive-cte)