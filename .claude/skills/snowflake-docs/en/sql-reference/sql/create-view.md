---
auto_generated: true
description: Creates a new view in the current/specified schema, based on a query
  of one or more existing tables (or any other valid query expression).
last_scraped: '2026-01-14T16:56:05.117775+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/create-view
title: CREATE VIEW | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)

   * [Query syntax](../constructs.md)
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

     + [SHOW OBJECTS](show-objects.md)
     + Table
     + [CREATE TABLE](create-table.md)
     + [ALTER TABLE](alter-table.md)
     + [DROP TABLE](drop-table.md)
     + [UNDROP TABLE](undrop-table.md)
     + [SHOW TABLES](show-tables.md)
     + [SHOW COLUMNS](show-columns.md)
     + [SHOW PRIMARY KEYS](show-primary-keys.md)
     + [DESCRIBE TABLE](desc-table.md)
     + [DESCRIBE SEARCH OPTIMIZATION](desc-search-optimization.md)
     + [TRUNCATE TABLE](truncate-table.md)
     + Dynamic table
     + [CREATE DYNAMIC TABLE](create-dynamic-table.md)
     + [ALTER DYNAMIC TABLE](alter-dynamic-table.md)
     + [DESCRIBE DYNAMIC TABLE](desc-dynamic-table.md)
     + [DROP DYNAMIC TABLE](drop-dynamic-table.md)
     + [UNDROP DYNAMIC TABLE](undrop-dynamic-table.md)
     + [SHOW DYNAMIC TABLES](show-dynamic-tables.md)
     + Event table
     + [CREATE EVENT TABLE](create-event-table.md)
     + [ALTER TABLE (Event Table)](alter-table-event-table.md)")
     + [SHOW EVENT TABLES](show-event-tables.md)
     + [DESCRIBE EVENT TABLE](desc-event-table.md)
     + External table
     + [CREATE EXTERNAL TABLE](create-external-table.md)
     + [ALTER EXTERNAL TABLE](alter-external-table.md)
     + [DROP EXTERNAL TABLE](drop-external-table.md)
     + [SHOW EXTERNAL TABLES](show-external-tables.md)
     + [DESCRIBE EXTERNAL TABLE](desc-external-table.md)
     + Hybrid table
     + [CREATE HYBRID TABLE](create-hybrid-table.md)
     + [CREATE INDEX](create-index.md)
     + [DROP INDEX](drop-index.md)
     + [SHOW HYBRID TABLES](show-hybrid-tables.md)
     + [SHOW INDEXES](show-indexes.md)
     + Apache Iceberg™ table
     + [CREATE ICEBERG TABLE](create-iceberg-table.md)
     + [ALTER ICEBERG TABLE](alter-iceberg-table.md)
     + [DROP ICEBERG TABLE](drop-iceberg-table.md)
     + [UNDROP ICEBERG TABLE](undrop-iceberg-table.md)
     + [SHOW ICEBERG TABLES](show-iceberg-tables.md)
     + [DESCRIBE ICEBERG TABLE](desc-iceberg-table.md)
     + Interactive tables and warehouses
     + [CREATE INTERACTIVE TABLE](create-interactive-table.md)
     + [CREATE INTERACTIVE WAREHOUSE](create-interactive-warehouse.md)
     + View
     + [CREATE VIEW](create-view.md)
     + [ALTER VIEW](alter-view.md)
     + [DROP VIEW](drop-view.md)
     + [SHOW VIEWS](show-views.md)
     + [DESCRIBE VIEW](desc-view.md)
     + Materialized view
     + [CREATE MATERIALIZED VIEW](create-materialized-view.md)
     + [ALTER MATERIALIZED VIEW](alter-materialized-view.md)
     + [DROP MATERIALIZED VIEW](drop-materialized-view.md)
     + [SHOW MATERIALIZED VIEWS](show-materialized-views.md)
     + [DESCRIBE MATERIALIZED VIEW](desc-materialized-view.md)
     + [TRUNCATE MATERIALIZED VIEW](truncate-materialized-view.md)
     + Semantic view
     + [CREATE SEMANTIC VIEW](create-semantic-view.md)
     + [ALTER SEMANTIC VIEW](alter-semantic-view.md)
     + [DROP SEMANTIC VIEW](drop-semantic-view.md)
     + [SHOW SEMANTIC VIEWS](show-semantic-views.md)
     + [SHOW SEMANTIC DIMENSIONS](show-semantic-dimensions.md)
     + [SHOW SEMANTIC DIMENSIONS FOR METRIC](show-semantic-dimensions-for-metric.md)
     + [SHOW SEMANTIC FACTS](show-semantic-facts.md)
     + [SHOW SEMANTIC METRICS](show-semantic-metrics.md)
     + [DESCRIBE SEMANTIC VIEW](desc-semantic-view.md)
     + Sequence
     + [CREATE SEQUENCE](create-sequence.md)
     + [ALTER SEQUENCE](alter-sequence.md)
     + [DROP SEQUENCE](drop-sequence.md)
     + [SHOW SEQUENCES](show-sequences.md)
     + [DESCRIBE SEQUENCE](desc-sequence.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Tables, views, & sequences](../commands-table.md)CREATE VIEW

# CREATE VIEW[¶](#create-view "Link to this heading")

Creates a new view in the current/specified schema, based on a query of one or more existing tables (or any other valid query expression).

This command supports the following variants:

* [CREATE OR ALTER VIEW](#label-create-or-alter-view-syntax): Creates a view if it doesn’t exist or alters an existing view.

See also:
:   [ALTER VIEW](alter-view) , [DROP VIEW](drop-view) , [SHOW VIEWS](show-views) , [DESCRIBE VIEW](desc-view)

    [CREATE OR ALTER <object>](create-or-alter)

## Syntax[¶](#syntax "Link to this heading")

```
CREATE [ OR REPLACE ] [ SECURE ] [ { [ { LOCAL | GLOBAL } ] TEMP | TEMPORARY | VOLATILE } ] [ RECURSIVE ] VIEW [ IF NOT EXISTS ] <name>
  [ ( <column_list> ) ]
  [ <col1> [ WITH ] MASKING POLICY <policy_name> [ USING ( <col1> , <cond_col1> , ... ) ]
           [ WITH ] PROJECTION POLICY <policy_name>
           [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ , <col2> [ ... ] ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
  [ CHANGE_TRACKING = { TRUE | FALSE } ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> [ ENTITY KEY ( <col_name> [ , <col_name> ... ] ) ] ]
  [ [ WITH ] JOIN POLICY <policy_name> [ ALLOWED JOIN KEYS ( <col_name> [ , ... ] ) ] ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  AS <select_statement>
```

Copy

## Variant syntax[¶](#variant-syntax "Link to this heading")

### CREATE OR ALTER VIEW[¶](#create-or-alter-view "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

Creates a new view if it doesn’t already exist, or updates the properties of an existing view to match those defined in the statement.
A CREATE OR ALTER VIEW statement follows the syntax rules of a CREATE VIEW statement and has the same limitations as an
[ALTER VIEW](alter-view) statement.

The CREATE OR ALTER VIEW command doesn’t support changing a view definition once a view is created. This limitation is inherited
from the ALTER VIEW command.

The following modifications are supported:

* Converting to (or reverting from) a secure view.
* Adding, overwriting, removing a comment for a view or a view’s columns.
* Enabling or disabling change tracking for a view.

For more information, see [CREATE OR ALTER VIEW usage notes](#label-create-or-alter-view-usage-notes) and [CREATE OR ALTER <object>](create-or-alter).

```
CREATE OR ALTER [ SECURE ] [ { [ { LOCAL | GLOBAL } ] TEMP | TEMPORARY | VOLATILE } ] [ RECURSIVE ] VIEW <name>
  [ ( <column_list> ) ]
  [ CHANGE_TRACKING =  { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  AS <select_statement>
```

Copy

## Required parameters[¶](#required-parameters "Link to this heading")

`name`
:   Specifies the identifier for the view; must be unique for the schema in which the view is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](../identifiers-syntax).

`select_statement`
:   Specifies the query used to create the view. Can be on one or more source tables or any other valid [SELECT](select) statement. This
    query serves as the text/definition for the view and is displayed in the [SHOW VIEWS](show-views) output and the
    [VIEWS](../info-schema/views) Information Schema view.

## Optional parameters[¶](#optional-parameters "Link to this heading")

`SECURE`
:   Specifies that the view is secure. For more information about secure views, see [Working with Secure Views](../../user-guide/views-secure).

    Default: No value (view is not secure)

`{ [ { LOCAL | GLOBAL } ] TEMP | TEMPORARY | VOLATILE }`
:   Specifies that the view persists only for the duration of the [session](../../user-guide/session-policies) that you created it in. A
    temporary view and all its contents are dropped at the end of the session.

    The synonyms and abbreviations for `TEMPORARY` (e.g. `GLOBAL TEMPORARY`) are provided for compatibility with other databases
    (e.g. to prevent errors when migrating CREATE VIEW statements). Views created with any of these keywords appear and behave identically to
    a view created with the `TEMPORARY` keyword.

    Default: No value. If a view is not declared as `TEMPORARY`, the view is permanent.

    If you want to avoid unexpected conflicts, avoid naming temporary views after views that already exist in the schema.

    If you created a temporary view with the same name as another view in the schema, all queries and operations used on the view only affect
    the temporary view in the session, until you drop the temporary view. If you drop the view, you drop the temporary view, and not the view
    that already exists in the schema.

`RECURSIVE`
:   Specifies that the view can refer to itself using recursive syntax without necessarily using a CTE (common table
    expression). For more information about recursive views in general, and the RECURSIVE keyword in particular,
    see [Recursive Views (Non-materialized Views Only)](../../user-guide/views-introduction.html#label-views-recursive) and the recursive view examples below.

    Default: No value (view is not recursive, or is recursive only by using a CTE)

`column_list`
:   If you want to change the name of a column or add a comment to a column in the new view,
    include a column list that specifies the column names and (if needed) comments about
    the columns. (You do not need to specify the data types of the columns.)

    If any of the columns in the view are based on expressions (not just simple column names), then you must supply
    a column name for each column in the view. For example, the column names are required in the following case:

    ```
    CREATE VIEW v1 (pre_tax_profit, taxes, after_tax_profit) AS
        SELECT revenue - cost, (revenue - cost) * tax_rate, (revenue - cost) * (1.0 - tax_rate)
        FROM table1;
    ```

    Copy

    You can specify an optional comment for each column. For example:

    ```
    CREATE VIEW v1 (pre_tax_profit COMMENT 'revenue minus cost',
                    taxes COMMENT 'assumes taxes are a fixed percentage of profit',
                    after_tax_profit)
        AS
        SELECT revenue - cost, (revenue - cost) * tax_rate, (revenue - cost) * (1.0 - tax_rate)
        FROM table1;
    ```

    Copy

    Comments are particularly helpful when column names are cryptic.

    To view comments, use [DESCRIBE VIEW](desc-view).

`MASKING POLICY = policy_name`
:   Specifies the [masking policy](../../user-guide/security-column-intro) to set on a column.

`USING ( col_name , cond_col_1 ... )`
:   Specifies the arguments to pass into the conditional masking policy SQL expression.

    The first column in the list specifies the column for the policy conditions to mask or tokenize the data and must match the
    column to which the masking policy is set.

    The additional columns specify the columns to evaluate to determine whether to mask or tokenize the data in each row of the query result
    when a query is made on the first column.

    If the USING clause is omitted, Snowflake treats the conditional masking policy as a normal
    [masking policy](../../user-guide/security-column-intro).

`PROJECTION POLICY policy_name`
:   Specifies the [projection policy](../../user-guide/projection-policies) to set on a column.

`CHANGE_TRACKING = { TRUE | FALSE }`
:   Specifies whether to enable change tracking on the view.

    * `TRUE` enables change tracking on the view. This setting adds a pair of hidden columns to the source table and begins
      storing change tracking metadata in the columns. These columns consume a small amount of storage.

      The change-tracking metadata can be queried using the [CHANGES](../constructs/changes) clause for
      [SELECT](select) statements, or by creating and querying one or more streams on the table.
    * `FALSE` does not enable change tracking on the view.

`COPY GRANTS`
:   Retains the access permissions from the original view when a new view is created using the `OR REPLACE` clause.

    The parameter copies all privileges, except OWNERSHIP, from the existing view to the new view. The new view does not
    inherit any future grants defined for the object type in the schema. By default, the role that executes the CREATE VIEW statement owns
    the new view.

    If the parameter is not included in the CREATE VIEW statement, then the new view does not inherit any explicit access
    privileges granted on the original view but does inherit any future grants defined for the object type in the schema.

    Note that the operation to copy grants occurs atomically with the CREATE VIEW statement (i.e. within the same transaction).

    Default: No value (grants are not copied)

`COMMENT = 'string_literal'`
:   Specifies a comment for the view.

    Default: No value

`ROW ACCESS POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Specifies the [row access policy](../../user-guide/security-row-intro) to set on a view.

`AGGREGATION POLICY policy_name [ ENTITY KEY ( col_name [ , col_name ... ] ) ]`
:   Specifies the [aggregation policy](../../user-guide/aggregation-policies) to set on a view.

    Use the optional ENTITY KEY parameter to define which columns uniquely identity an entity within the view. For more information, see
    [Implementing entity-level privacy with aggregation policies](../../user-guide/aggregation-policies-entity-privacy).

`JOIN POLICY policy_name [ ALLOWED JOIN KEYS ( col_name [ , ... ] ) ]`
:   Specifies the [join policy](../../user-guide/join-policies) to set on a view.

    Use the optional ALLOWED JOIN KEYS parameter to define which columns are allowed to be used as joining columns when
    this policy is in effect. For more information, see [Join policies](../../user-guide/join-policies).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](../../user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](../../user-guide/object-tagging/introduction.html#label-object-tagging-quota).

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](../../user-guide/contacts-using).

## Access control requirements[¶](#access-control-requirements "Link to this heading")

A [role](../../user-guide/security-access-control-overview.html#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](../../user-guide/security-access-control-overview.html#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE VIEW | Schema | Required to create a new view. |
| SELECT | Table, external table, view | Required on any tables and/or views queried in the view definition. |
| APPLY | Masking policy, row access policy, tag | Required only when applying a masking policy, row access policy, object tags, or any combination of these [governance](../../guides-overview-govern) features when creating views. |
| OWNERSHIP | View | * A role must be granted or inherit the OWNERSHIP privilege on the object to create a temporary object that has the same name as the object   that already exists in the schema. * Required to execute a [CREATE OR ALTER VIEW](#label-create-or-alter-view-syntax) statement for an *existing* view.   OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege).  Note that in a [managed access schema](../../user-guide/security-access-control-configure.html#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](../../user-guide/security-access-control-configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](../../user-guide/security-access-control-overview.html#label-access-control-securable-objects), see [Overview of Access Control](../../user-guide/security-access-control-overview).

## General usage notes[¶](#general-usage-notes "Link to this heading")

* A view definition can include an [ORDER BY](../constructs/order-by) clause
  (e.g. `create view v1 as select * from t1 ORDER BY column1`). However, Snowflake recommends excluding
  the `ORDER BY` clause from most view definitions. If the view is used in contexts that don’t benefit from sorting,
  then the `ORDER BY` clause adds unnecessary costs. For example, when the view is used in a join, and the join
  column is not the same as the `ORDER BY` column, the extra cost to sort the view’s results is typically wasted.
  If you need to sort the query results, it’s usually more efficient to specify `ORDER BY` in the query that uses
  the view, rather than in the view itself.
* If you specify the [CURRENT\_DATABASE](../functions/current_database) or [CURRENT\_SCHEMA](../functions/current_schema) function in the
  definition of the view, the function returns the database or schema that contains the view, not the database or schema in
  use for the session.
* The definition for a view is limited to 95KB.
* Nesting levels are limited to a maximum of 20. An attempt to create a view that is nested more than 20 times will fail.
* View definitions are not dynamic. A view is not automatically updated if the underlying sources are modified such that they no longer
  match the view definition, particularly when columns are dropped. For example:

  + A view is created referencing a specific column in a source table, and the column is subsequently dropped from the table.
  + A view is created using `SELECT *` from a table, and changes are made to the columns in the table, such as:

    - A column is dropped.
    - A column is added.
    - The column order changes.

  In these scenarios, querying the view returns a column-related error.
* If a source table for a view is dropped, querying the view returns an `object does not exist` error.
* A schema cannot contain a table and view with the same name. A CREATE VIEW statement produces an error if a table with the same name
  already exists in the schema.
* When a view is created, [unqualified](../name-resolution) references to tables and other database
  objects are resolved in the view’s schema, not in the session’s current schema. Similarly, objects that are
  partially qualified (i.e. schema.object) are resolved in the view’s database, not in the session’s current database.

  The `SEARCH_PATH` session parameter (if present) is ignored.
* Using `OR REPLACE` is the equivalent of using [DROP VIEW](drop-view) on the existing view and then creating a new view with the same
  name.

  CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

  This means that any queries concurrent with the CREATE OR REPLACE VIEW operation use either the old or new view version.

  Recreating or swapping a view drops its change data, which makes any stream on the view stale. A
  [stale](../../user-guide/streams-intro.html#label-streams-staleness) stream is unreadable.
* The `OR REPLACE` and `IF NOT EXISTS` clauses are mutually exclusive. They can’t both be used in the same statement.
* Using `COPY GRANTS`:

  + Data sharing:

    - If the existing secure view was shared to another account, the replacement view is also shared.
    - If the existing secure view was shared with your account as a data consumer, and access was further granted to other roles in the
      account (using GRANT IMPORTED PRIVILEGES on the parent database), access is also granted to the replacement view.
  + The [SHOW GRANTS](show-grants) output for the replacement view lists the grantee for the copied privileges as the role
    that executed the CREATE VIEW statement, with the current timestamp when the statement was executed.
* When you create a view and then grant privileges on that view to a role, the role can use the view even if the role does not have
  privileges on the underlying table(s) that the view accesses. This means that you can create a view to give a role access to only
  a subset of a table. For example, you can create a view that accesses medical billing information but not medical diagnosis
  information in the same table. Then you can grant privileges on that view to the “accountant” role so that the accountants
  can look at the billing information without seeing the patient’s diagnosis.
* By design, the [SHOW VIEWS](show-views) command does not provide information about secure views. To view information about a secure view,
  you must use the [VIEWS](../info-schema/views) view in the Information Schema and you must use the role that owns
  the view.
* A recursive view must provide a column name list.
* When defining recursive views, prevent infinite recursion. The WHERE clause in the recursive view definition should enable the
  recursion to stop eventually, typically by running out of data after processing the last level of a hierarchy of data.
* Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](../metadata).
* When creating a view with a masking policy on one or more view columns, or a row access policy added to the view, use the
  [POLICY\_CONTEXT](../functions/policy_context) function to simulate a query on the column(s) protected by a masking policy and the
  view protected by a row access policy.
* Do not create views with streams as source objects unless the same role owns both the view and source streams (i.e. the same role,
  or a lower role in a role hierarchy, has the OWNERSHIP privilege on the view and source streams). Instead, create views that have
  the objects to track as the source objects. Then, create streams on those views. For more information, see
  [Streams on Views](../../user-guide/streams-intro.html#label-streams-views).

## Porting notes[¶](#porting-notes "Link to this heading")

* Some vendors support the `FORCE` keyword:

  > ```
  > CREATE OR REPLACE FORCE VIEW ...
  > ```
  >
  > Copy

  Snowflake accepts the `FORCE` keyword, but does not support it. In other words, you do not get a syntax error if you use this
  keyword, but using `FORCE` does not force the creation of a view if the underlying database objects (table(s) or view(s))
  do not already exist. Attempting to create a view of a non-existent table or view results in an error message even if the
  `FORCE` keyword is used.
* When looking up the tables in a view, some vendors search for unqualified table names in the active schema; Snowflake searches
  for unqualified table names
  [in the same schema as the view](../../user-guide/views-introduction.html#label-views-introduction-unqualified-table-schema-equals-view-schema).
  When porting to Snowflake, consider updating views to use fully-qualified table names.

## CREATE OR ALTER VIEW usage notes[¶](#create-or-alter-view-usage-notes "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.

* All limitations of the [ALTER VIEW](alter-view) command apply.
* This command doesn *not* support the following:

  + Changing the definition of a view.
  + Renaming a view using the RENAME TO parameter.
  + Adding or changing tags and policies. Any existing tags and policies are preserved.
  + Converting a TEMPORARY view into a permanent view, or vice versa.

## Examples[¶](#examples "Link to this heading")

### Basic examples[¶](#basic-examples "Link to this heading")

Create a view in the current schema, with a comment, that selects all the rows from a table:

> ```
> CREATE VIEW myview COMMENT='Test view' AS SELECT col1, col2 FROM mytable;
>
> SHOW VIEWS;
>
> +---------------------------------+-------------------+----------+---------------+-------------+----------+-----------+--------------------------------------------------------------------------+
> | created_on                      | name              | reserved | database_name | schema_name | owner    | comment   | text                                                                     |
> |---------------------------------+-------------------+----------+---------------+-------------+----------+-----------+--------------------------------------------------------------------------|
> | Thu, 19 Jan 2017 15:00:37 -0800 | MYVIEW            |          | MYTEST1       | PUBLIC      | SYSADMIN | Test view | CREATE VIEW myview COMMENT='Test view' AS SELECT col1, col2 FROM mytable |
> +---------------------------------+-------------------+----------+---------------+-------------+----------+-----------+--------------------------------------------------------------------------+
> ```
>
> Copy

The next example is the same as the previous example, except the view is secure:

> ```
> CREATE OR REPLACE SECURE VIEW myview COMMENT='Test secure view' AS SELECT col1, col2 FROM mytable;
>
> SELECT is_secure FROM information_schema.views WHERE table_name = 'MYVIEW';
> ```
>
> Copy

The following shows two ways of creating recursive views:

> First, create and load the table:
>
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
>
> Create a view using a recursive CTE, and then query the view.
>
> ```
> CREATE VIEW employee_hierarchy (title, employee_ID, manager_ID, "MGR_EMP_ID (SHOULD BE SAME)", "MGR TITLE") AS (
>    WITH RECURSIVE employee_hierarchy_cte (title, employee_ID, manager_ID, "MGR_EMP_ID (SHOULD BE SAME)", "MGR TITLE") AS (
>       -- Start at the top of the hierarchy ...
>       SELECT title, employee_ID, manager_ID, NULL AS "MGR_EMP_ID (SHOULD BE SAME)", 'President' AS "MGR TITLE"
>         FROM employees
>         WHERE title = 'President'
>       UNION ALL
>       -- ... and work our way down one level at a time.
>       SELECT employees.title, 
>              employees.employee_ID, 
>              employees.manager_ID, 
>              employee_hierarchy_cte.employee_id AS "MGR_EMP_ID (SHOULD BE SAME)", 
>              employee_hierarchy_cte.title AS "MGR TITLE"
>         FROM employees INNER JOIN employee_hierarchy_cte
>        WHERE employee_hierarchy_cte.employee_ID = employees.manager_ID
>    )
>    SELECT * 
>       FROM employee_hierarchy_cte
> );
> ```
>
> Copy
>
> ```
> SELECT * 
>     FROM employee_hierarchy 
>     ORDER BY employee_ID;
> +----------------------------+-------------+------------+-----------------------------+----------------------------+
> | TITLE                      | EMPLOYEE_ID | MANAGER_ID | MGR_EMP_ID (SHOULD BE SAME) | MGR TITLE                  |
> |----------------------------+-------------+------------+-----------------------------+----------------------------|
> | President                  |           1 |       NULL |                        NULL | President                  |
> | Vice President Engineering |          10 |          1 |                           1 | President                  |
> | Vice President HR          |          20 |          1 |                           1 | President                  |
> | Programmer                 |         100 |         10 |                          10 | Vice President Engineering |
> | QA Engineer                |         101 |         10 |                          10 | Vice President Engineering |
> | Health Insurance Analyst   |         200 |         20 |                          20 | Vice President HR          |
> +----------------------------+-------------+------------+-----------------------------+----------------------------+
> ```
>
> Copy
>
> Create a view using the keyword RECURSIVE, and then query the view.
>
> ```
> CREATE RECURSIVE VIEW employee_hierarchy_02 (title, employee_ID, manager_ID, "MGR_EMP_ID (SHOULD BE SAME)", "MGR TITLE") AS (
>       -- Start at the top of the hierarchy ...
>       SELECT title, employee_ID, manager_ID, NULL AS "MGR_EMP_ID (SHOULD BE SAME)", 'President' AS "MGR TITLE"
>         FROM employees
>         WHERE title = 'President'
>       UNION ALL
>       -- ... and work our way down one level at a time.
>       SELECT employees.title, 
>              employees.employee_ID, 
>              employees.manager_ID, 
>              employee_hierarchy_02.employee_id AS "MGR_EMP_ID (SHOULD BE SAME)", 
>              employee_hierarchy_02.title AS "MGR TITLE"
>         FROM employees INNER JOIN employee_hierarchy_02
>         WHERE employee_hierarchy_02.employee_ID = employees.manager_ID
> );
> ```
>
> Copy
>
> ```
> SELECT * 
>     FROM employee_hierarchy_02 
>     ORDER BY employee_ID;
> +----------------------------+-------------+------------+-----------------------------+----------------------------+
> | TITLE                      | EMPLOYEE_ID | MANAGER_ID | MGR_EMP_ID (SHOULD BE SAME) | MGR TITLE                  |
> |----------------------------+-------------+------------+-----------------------------+----------------------------|
> | President                  |           1 |       NULL |                        NULL | President                  |
> | Vice President Engineering |          10 |          1 |                           1 | President                  |
> | Vice President HR          |          20 |          1 |                           1 | President                  |
> | Programmer                 |         100 |         10 |                          10 | Vice President Engineering |
> | QA Engineer                |         101 |         10 |                          10 | Vice President Engineering |
> | Health Insurance Analyst   |         200 |         20 |                          20 | Vice President HR          |
> +----------------------------+-------------+------------+-----------------------------+----------------------------+
> ```
>
> Copy

### CREATE OR ALTER VIEW examples[¶](#create-or-alter-view-examples "Link to this heading")

#### Basic example[¶](#basic-example "Link to this heading")

Create a table `my_table` with one column:

```
CREATE OR ALTER TABLE my_table(a INT);
```

Copy

Create a view named `v2` that selects column `a` from table `my_table`:

```
CREATE OR ALTER VIEW v2(one)
  AS SELECT a FROM my_table;
```

Copy

Create or alter view `v2`. Add or update the COMMENT and CHANGE\_TRACKING properties for the view:

```
CREATE OR ALTER VIEW v2(one)
  COMMENT = 'fff'
  CHANGE_TRACKING = true
  AS SELECT a FROM my_table;
```

Copy

Create or alter view `v2` to add a comment to a column:

```
CREATE OR ALTER VIEW v2(one COMMENT 'bar')
  COMMENT = 'foo'
  AS SELECT a FROM my_table;
```

Copy

#### Unset a property previously set on view[¶](#unset-a-property-previously-set-on-view "Link to this heading")

The [absence of a previously set property](create-or-alter.html#label-create-or-alter-usage-notes) in the CREATE OR ALTER VIEW statement results
in unsetting it. In the following example, unset the COMMENT property for the view `v2` from the previous example:

```
CREATE OR ALTER VIEW v2(one COMMENT 'bar')
  CHANGE_TRACKING = true
  AS SELECT a FROM my_table;
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
2. [Variant syntax](#variant-syntax)
3. [CREATE OR ALTER VIEW](#create-or-alter-view)
4. [Required parameters](#required-parameters)
5. [Optional parameters](#optional-parameters)
6. [Access control requirements](#access-control-requirements)
7. [General usage notes](#general-usage-notes)
8. [Porting notes](#porting-notes)
9. [CREATE OR ALTER VIEW usage notes](#create-or-alter-view-usage-notes)
10. [Examples](#examples)
11. [Basic examples](#basic-examples)
12. [CREATE OR ALTER VIEW examples](#create-or-alter-view-examples)
13. [Basic example](#basic-example)
14. [Unset a property previously set on view](#unset-a-property-previously-set-on-view)