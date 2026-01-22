---
auto_generated: true
description: Query syntax
last_scraped: '2026-01-14T16:55:00.877666+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/constructs/group-by-grouping-sets
title: GROUP BY GROUPING SETS | Snowflake Documentation
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Query syntax](../constructs.md)GROUP BY GROUPING SETS

Categories:
:   [Query syntax](../constructs)

# GROUP BY GROUPING SETS[¶](#group-by-grouping-sets "Link to this heading")

GROUP BY GROUPING SETS is a powerful extension of the [GROUP BY](group-by) clause that computes multiple group-by clauses in a single statement. The group set is a set of dimension columns.

GROUP BY GROUPING SETS is equivalent to the `UNION` of two or more [GROUP BY](group-by) operations in the same result set:

* `GROUP BY GROUPING SETS(a)` is equivalent to the single grouping set operation `GROUP BY a`.
* `GROUP BY GROUPING SETS(a,b)` is equivalent to `GROUP BY a UNION ALL GROUP BY b`.

## Syntax[¶](#syntax "Link to this heading")

```
SELECT ...
FROM ...
[ ... ]
GROUP BY GROUPING SETS ( groupSet [ , groupSet [ , ... ] ] )
[ ... ]
```

Copy

Where:

> ```
> groupSet ::= { <column_alias> | <position> | <expr> }
> ```
>
> Copy

## Parameters[¶](#parameters "Link to this heading")

`column_alias`
:   Column alias appearing in the query block’s [SELECT](../sql/select) list.

`position`
:   Position of an expression in the [SELECT](../sql/select) list.

`expr`
:   Any expression on tables in the current scope.

## Usage notes[¶](#usage-notes "Link to this heading")

* Snowflake allows up to 128 grouping sets in the same query block.
* The output typically contains some NULL values. Because `GROUP BY ROLLUP`
  merges the results of two or more result sets, each of which was
  grouped by different criteria, some columns that have a single value
  in one result set might have many corresponding values in the
  other result set. For example, if you do a `UNION` of a set of
  employees grouped by department with a set grouped by seniority, the
  members of the set with the greatest seniority are not necessarily all
  in the same department, so the value of department\_name is set to
  NULL. The following examples contain NULLs for this reason.

## Examples[¶](#examples "Link to this heading")

These examples use a table of information about nurses who are trained to
assist in disasters. All of these nurses have a license as nurses (e.g.
an RN has a license as a “Registered Nurse”), and an additional license
in a disaster-related specialty, such as search and rescue, radio
communications, etc. This example simplifies and uses just two categories
of licenses:

* Nursing: RN (Registered Nurse) and LVN (Licensed Vocational Nurse).
* Amateur (“ham”) Radio: Ham radio licenses include “Technician”, “General”, and “Amateur Extra”.

Here are the commands to create and load the table:

> ```
> CREATE or replace TABLE nurses (
>   ID INTEGER,
>   full_name VARCHAR,
>   medical_license VARCHAR,   -- LVN, RN, etc.
>   radio_license VARCHAR      -- Technician, General, Amateur Extra
>   )
>   ;
>
> INSERT INTO nurses
>     (ID, full_name, medical_license, radio_license)
>   VALUES
>     (201, 'Thomas Leonard Vicente', 'LVN', 'Technician'),
>     (202, 'Tamara Lolita VanZant', 'LVN', 'Technician'),
>     (341, 'Georgeann Linda Vente', 'LVN', 'General'),
>     (471, 'Andrea Renee Nouveau', 'RN', 'Amateur Extra')
>     ;
> ```
>
> Copy

This query uses `GROUP BY GROUPING SETS`:

> ```
> SELECT COUNT(*), medical_license, radio_license
>   FROM nurses
>   GROUP BY GROUPING SETS (medical_license, radio_license);
> ```
>
> Copy
>
> Output:
>
> > The first two rows show the count of RNs and LVNs (two types of nursing
> > licenses). The NULL values in the RADIO\_LICENSE column for
> > those two rows are deliberate; the query grouped all of the LVNs together
> > (and all the RNs together) regardless of their radio license, so the
> > results can’t show one value in the RADIO\_LICENSE column for each
> > row that necessarily applies to all the LVNs or RNs grouped in that row.
> >
> > The next three rows show the number of nurses with each type of ham radio
> > license (“Technician”, “General”, and “Amateur Extra”). The NULL value
> > for MEDICAL\_LICENSE in each of those three rows is deliberate because
> > no single medical license necessarily applies to all members of each
> > of those rows.
>
> ```
> +----------+-----------------+---------------+
> | COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
> |----------+-----------------+---------------|
> |        3 | LVN             | NULL          |
> |        1 | RN              | NULL          |
> |        2 | NULL            | Technician    |
> |        1 | NULL            | General       |
> |        1 | NULL            | Amateur Extra |
> +----------+-----------------+---------------+
> ```

The next example shows what happens when some columns contain NULL values.
Start by adding three new nurses who don’t yet have ham radio licenses.

> ```
> INSERT INTO nurses
>     (ID, full_name, medical_license, radio_license)
>   VALUES
>     (101, 'Lily Vine', 'LVN', NULL),
>     (102, 'Larry Vancouver', 'LVN', NULL),
>     (172, 'Rhonda Nova', 'RN', NULL)
>     ;
> ```
>
> Copy
>
> Then run the same query as before:
>
> ```
> SELECT COUNT(*), medical_license, radio_license
>   FROM nurses
>   GROUP BY GROUPING SETS (medical_license, radio_license);
> ```
>
> Copy
>
> Output:
>
> > The first 5 lines are the same as in the previous query.
> >
> > The last line might be confusing at first – why is there a line that has
> > NULL in both columns? And if all the values are NULL, why is the COUNT(\*)
> > equal to 3?
> >
> > The answer is that the NULL in the RADIO\_LICENSE column of that row
> > occurs because three nurses don’t have any radio license.
> > (“SELECT DISTINCT RADIO\_LICENSE FROM nurses” now returns four distinct
> > values: “Technician”, “General”, “Amateur Extra”, and “NULL”.)
> >
> > The NULL in the MEDICAL\_LICENSES column occurs for the same reason that
> > NULL values occur in the earlier query results: the nurses counted in this
> > row have different MEDICAL\_LICENSES, so no one value (“RN” or “LVN”)
> > necessarily applies to all of the nurses counted in this row.
>
> ```
> +----------+-----------------+---------------+
> | COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
> |----------+-----------------+---------------|
> |        5 | LVN             | NULL          |
> |        2 | RN              | NULL          |
> |        2 | NULL            | Technician    |
> |        1 | NULL            | General       |
> |        1 | NULL            | Amateur Extra |
> |        3 | NULL            | NULL          |
> +----------+-----------------+---------------+
> ```

If you’d like, you can compare this output to the output of a `GROUP BY` without the `GROUPING SETS` clause:

> ```
> SELECT COUNT(*), medical_license, radio_license
>   FROM nurses
>   GROUP BY medical_license, radio_license;
> ```
>
> Copy
>
> Output:
>
> ```
> +----------+-----------------+---------------+
> | COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
> |----------+-----------------+---------------|
> |        2 | LVN             | Technician    |
> |        1 | LVN             | General       |
> |        1 | RN              | Amateur Extra |
> |        2 | LVN             | NULL          |
> |        1 | RN              | NULL          |
> +----------+-----------------+---------------+
> ```

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