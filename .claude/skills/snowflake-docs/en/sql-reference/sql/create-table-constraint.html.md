---
auto_generated: true
description: 'This topic describes how to create constraints by specifying a CONSTRAINT
  clause in a CREATE TABLE, CREATE HYBRID TABLE, or ALTER TABLE statement:'
last_scraped: '2026-01-14T16:57:15.172671+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/sql/create-table-constraint.html
title: CREATE | ALTER TABLE … CONSTRAINT | Snowflake Documentation
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

       - [CREATE TABLE ... CONSTRAINT](create-table-constraint.md)
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

[Reference](../../reference.md)[SQL command reference](../../sql-reference-commands.md)[Tables, views, & sequences](../commands-table.md)[CREATE TABLE](create-table.md)CREATE TABLE ... CONSTRAINT

# CREATE | ALTER TABLE … CONSTRAINT[¶](#create-alter-table-constraint "Link to this heading")

This topic describes how to create constraints by specifying a CONSTRAINT clause in a
[CREATE TABLE](create-table), [CREATE HYBRID TABLE](create-hybrid-table),
or [ALTER TABLE](alter-table) statement:

* An inline constraint is specified as part of the individual column definition.
* An out-of-line constraint is specified as an independent clause:

  + When creating a table, the clause is part of the column definitions for the table.
  + When altering a table, the clause is specified as an explicit `ADD` action for the table.

For more information, see [Constraints](../constraints).

If you are creating or altering [hybrid tables](../../user-guide/tables-hybrid), the syntax for defining constraints is the same; however, the rules and requirements are different.

## Syntax for inline constraints[¶](#syntax-for-inline-constraints "Link to this heading")

```
CREATE TABLE <name> ( <col1_name> <col1_type>    [ NOT NULL ] { inlineUniquePK | inlineFK }
                     [ , <col2_name> <col2_type> [ NOT NULL ] { inlineUniquePK | inlineFK } ]
                     [ , ... ] )

ALTER TABLE <name> ADD COLUMN <col_name> <col_type> [ NOT NULL ] { inlineUniquePK | inlineFK }
```

Copy

Where:

> ```
> inlineUniquePK ::=
>   [ CONSTRAINT <constraint_name> ]
>   { UNIQUE | PRIMARY KEY }
>   [ [ NOT ] ENFORCED ]
>   [ [ NOT ] DEFERRABLE ]
>   [ INITIALLY { DEFERRED | IMMEDIATE } ]
>   [ { ENABLE | DISABLE } ]
>   [ { VALIDATE | NOVALIDATE } ]
>   [ { RELY | NORELY } ]
> ```
>
> Copy
>
> ```
> inlineFK :=
>   [ CONSTRAINT <constraint_name> ]
>   [ FOREIGN KEY ]
>   REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
>   [ MATCH { FULL | SIMPLE | PARTIAL } ]
>   [ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
>        [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
>   [ [ NOT ] ENFORCED ]
>   [ [ NOT ] DEFERRABLE ]
>   [ INITIALLY { DEFERRED | IMMEDIATE } ]
>   [ { ENABLE | DISABLE } ]
>   [ { VALIDATE | NOVALIDATE } ]
>   [ { RELY | NORELY } ]
> ```
>
> Copy

## Syntax for out-of-line constraints[¶](#syntax-for-out-of-line-constraints "Link to this heading")

```
CREATE TABLE <name> ... ( <col1_name> <col1_type>
                         [ , <col2_name> <col2_type> , ... ]
                         [ , { outoflineUniquePK | outoflineFK } ]
                         [ , { outoflineUniquePK | outoflineFK } ]
                         [ , ... ] )

ALTER TABLE <name> ... ADD { outoflineUniquePK | outoflineFK }
```

Copy

Where:

> ```
> outoflineUniquePK ::=
>   [ CONSTRAINT <constraint_name> ]
>   { UNIQUE | PRIMARY KEY } ( <col_name> [ , <col_name> , ... ] )
>   [ [ NOT ] ENFORCED ]
>   [ [ NOT ] DEFERRABLE ]
>   [ INITIALLY { DEFERRED | IMMEDIATE } ]
>   [ { ENABLE | DISABLE } ]
>   [ { VALIDATE | NOVALIDATE } ]
>   [ { RELY | NORELY } ]
>   [ COMMENT '<string_literal>' ]
> ```
>
> Copy
>
> ```
> outoflineFK :=
>   [ CONSTRAINT <constraint_name> ]
>   FOREIGN KEY ( <col_name> [ , <col_name> , ... ] )
>   REFERENCES <ref_table_name> [ ( <ref_col_name> [ , <ref_col_name> , ... ] ) ]
>   [ MATCH { FULL | SIMPLE | PARTIAL } ]
>   [ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
>        [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
>   [ [ NOT ] ENFORCED ]
>   [ [ NOT ] DEFERRABLE ]
>   [ INITIALLY { DEFERRED | IMMEDIATE } ]
>   [ { ENABLE | DISABLE } ]
>   [ { VALIDATE | NOVALIDATE } ]
>   [ { RELY | NORELY } ]
>   [ COMMENT '<string_literal>' ]
> ```
>
> Copy

## Constraint properties[¶](#constraint-properties "Link to this heading")

For compatibility with other databases, and for use with hybrid tables, Snowflake provides constraint properties.
The properties that can be specified for a constraint depend on the type:

* Some properties apply to all keys (unique, primary, and foreign).
* Other properties apply only to foreign keys.

Important

For standard Snowflake tables, these properties are provided to facilitate migrating from other databases. They are not
enforced or maintained by Snowflake. This means that the defaults can be changed for these properties, but changing the
defaults results in Snowflake not creating the constraint.

An exception is the RELY property. If you have ensured that the data in your standard tables complies with UNIQUE, PRIMARY
KEY, and FOREIGN KEY constraints, you can set the RELY property for those constraints. See also
[Setting the RELY Constraint Property to Eliminate Unnecessary Joins](../../user-guide/join-elimination.html#label-join-elimination-setting-rely).

If you are creating or altering [hybrid tables](../../user-guide/tables-hybrid), the rules and requirements are different.
See [Overview of Constraints](../constraints-overview).

Most of the supported constraint properties are ANSI SQL standard properties; however, the following properties are Snowflake extensions:

* ENABLE | DISABLE
* VALIDATE | NOVALIDATE
* RELY | NORELY

You can also define a comment within an out-of-line constraint definition; see [Comments on constraints](#label-comments-on-constraints).

### Properties (for all constraints)[¶](#properties-for-all-constraints "Link to this heading")

The following properties apply to all constraints (the order of the properties is interchangeable):

```
[ NOT ] ENFORCED
[ NOT ] DEFERRABLE
INITIALLY { DEFERRED | IMMEDIATE }
{ ENABLE | DISABLE }
{ VALIDATE | NOVALIDATE }
{ RELY | NORELY }
```

Copy

`{ ENFORCED | NOT ENFORCED }`
:   Specifies whether the constraint is enforced in a transaction. For standard tables, NOT NULL is the
    *only* type of constraint that is enforced by Snowflake, regardless of this property.

    For hybrid tables, you cannot set the NOT ENFORCED property on PRIMARY KEY, FOREIGN KEY, and UNIQUE constraints.
    Setting this property results in an “invalid constraint property” error.

    See also [Referential Integrity Constraints](../../user-guide/table-considerations.html#label-table-considerations-referential-integrity-constraints).

    Default: NOT ENFORCED

`{ DEFERRABLE | NOT DEFERRABLE }`
:   Specifies whether, in subsequent transactions, the constraint check can be deferred until the end of the transaction.

    Default: NOT DEFERRABLE

`INITIALLY { DEFERRED | IMMEDIATE }`
:   For DEFERRABLE constraints, specifies whether the check for the constraints can be deferred, starting from the next transaction.

    Default: INITIALLY DEFERRED

`{ ENABLE | DISABLE }`
:   Specifies whether the constraint is enabled or disabled. These properties are provided for compatibility with Oracle.

    Default: DISABLE

`{ VALIDATE | NOVALIDATE }`
:   Specifies whether to validate existing data on the table when a constraint is created. Applies only when either
    `{ ENFORCED | NOT ENFORCED }` or `{ ENABLE | DISABLE }` is specified.

    Default: NOVALIDATE

`{ RELY | NORELY }`
:   Specifies whether a constraint in NOVALIDATE mode is taken into account during query rewrite.

    If you have ensured that the data in the table complies with the constraints, you can change this property
    to RELY to indicate that the query optimizer should expect such data integrity. For standard tables, it is your responsibility to
    enforce RELY constraints; otherwise, you might risk unintended behavior and unexpected results.

    If the RELY property is set for a constraint and a violation of referential integrity occurs, DML and CTAS statements might insert
    incorrect data.

    Setting the RELY property might improve query
    performance (for example, by [eliminating unnecessary joins](../../user-guide/join-elimination)).

    For related PRIMARY KEY and FOREIGN KEY constraints, set this property on both constraints. For example:

    ```
    ALTER TABLE table_with_primary_key ALTER CONSTRAINT a_primary_key_constraint RELY;
    ALTER TABLE table_with_foreign_key ALTER CONSTRAINT a_foreign_key_constraint RELY;
    ```

    Copy

    Default: NORELY

### Properties (for foreign key constraints only)[¶](#properties-for-foreign-key-constraints-only "Link to this heading")

The following constraint properties apply only to foreign keys (the order of the properties is interchangeable):

```
MATCH { FULL | SIMPLE | PARTIAL }
ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
   [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
```

Copy

`MATCH { FULL | PARTIAL | SIMPLE }`
:   Specifies whether the foreign key constraint is satisfied with regard to NULL values in one or more of the columns.

    Default: MATCH FULL

`UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION }`
:   Specifies the action performed when the primary/unique key for the foreign key is updated.

    Default: UPDATE NO ACTION

`DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION }`
:   Specifies the action performed when the primary/unique key for the foreign key is deleted.

    Default: DELETE NO ACTION

### Non-default values for ENABLE and VALIDATE properties[¶](#non-default-values-for-enable-and-validate-properties "Link to this heading")

For syntax compatibility with other databases, Snowflake supports specifying non-default values for constraint properties.

However, if you specify ENABLE or VALIDATE (the non-default values for these properties) when creating a new
constraint, *the constraint is not created*. This does not apply to RELY. Specifying RELY does result in
the creation of the new constraint.

Note that Snowflake provides a session parameter, [UNSUPPORTED\_DDL\_ACTION](../parameters.html#label-unsupported-ddl-action), which determines whether specifying non-default
values during constraint creation generates an error.

## Comments on constraints[¶](#comments-on-constraints "Link to this heading")

Similar to other database objects and constructs, Snowflake supports comments on constraints:

* Out-of-line constraints support the COMMENT clause within the constraint definition.

  ```
  CREATE OR REPLACE TABLE uni (c1 INT, c2 int, CONSTRAINT uni1 UNIQUE(C1) COMMENT 'Unique column');
  ```

  Copy
* A COMMENT clause within the column definition can be used to comment on the column itself or its constraint:

  ```
  CREATE OR REPLACE TABLE uni (c1 INT UNIQUE COMMENT 'Unique column', c2 int);
  ```

  Copy

Note the following limitations:

* You cannot set comments on constraints by using the [COMMENT](comment) command.
* The [DESCRIBE TABLE](desc-table) command shows comments defined on columns, but not comments defined on constraints.
  To see comments on constraints, select from the [TABLE\_CONSTRAINTS view](../info-schema/table_constraints) or the
  [REFERENTIAL\_CONSTRAINTS view](../info-schema/referential_constraints).
* The COMMENT clause within column and constraint definitions does not support the equals sign (`=`). Do not specify:

  ```
  COMMENT = 'My comment'
  ```

  Copy

  Use the syntax shown in the previous examples:

  ```
  COMMENT 'My comment'
  ```

  Copy

## Usage notes[¶](#usage-notes "Link to this heading")

* NOT NULL specifies that the column does not allow NULL values:

  > + For standard Snowflake tables, this is the only constraint that is enforced. See [Referential Integrity Constraints](../../user-guide/table-considerations.html#label-table-considerations-referential-integrity-constraints).
  > + It can be specified only as an inline constraint within the column definition.
  > + The default is to allow NULL values in columns.
* Multi-column constraints (composite unique or primary keys) can only be defined out-of-line.
* When defining foreign keys, either inline or out-of-line, column name(s) for the referenced table do not need to be specified if the
  signature (name and data type) of the foreign key column(s) and the referenced table’s primary key column(s) exactly match.

* If you create a foreign key, the columns in the REFERENCES clause must be listed in the same order as they were
  listed for the primary key. For example:

  ```
  CREATE TABLE parent ... CONSTRAINT primary_key_1 PRIMARY KEY (c_1, c_2) ...
  CREATE TABLE child  ... CONSTRAINT foreign_key_1 FOREIGN KEY (...) REFERENCES parent (c_1, c_2) ...
  ```

  Copy

  In both cases, the order of the columns is `c_1, c_2`. If the order of the columns in the foreign key had been different
  (for example, `c_2, c_1`), the attempt to create the foreign key would have failed.

## Access control requirements[¶](#access-control-requirements "Link to this heading")

For creating primary key or unique constraints:

* When altering an existing table to add the constraint, you must use a role that has the OWNERSHIP privilege on the table.
* When creating a new table, you must use a role that has the CREATE TABLE privilege on the schema where the table will be created.

For creating foreign key constraints:

* You must use a role that has the OWNERSHIP privilege on the foreign key table.
* You must use a role that has the REFERENCES privilege on the unique/primary key table.

The REFERENCES privilege can be granted to and revoked from roles using the [GRANT <privileges> … TO ROLE](grant-privilege) and
[REVOKE <privileges> … FROM ROLE](revoke-privilege) commands:

> ```
> GRANT REFERENCES ON TABLE <pk_table_name> TO ROLE <role_name>
>
> REVOKE REFERENCES ON TABLE <pk_table_name> FROM ROLE <role_name>
> ```
>
> Copy

## Examples with standard tables[¶](#examples-with-standard-tables "Link to this heading")

For examples of constraints with hybrid tables, see [CREATE HYBRID TABLE](create-hybrid-table).

The example below shows how to create a simple NOT NULL constraint while creating a table, and another NOT NULL
constraint while altering a table:

Create a table and create a constraint at the same time:

```
CREATE TABLE table1 (col1 INTEGER NOT NULL);
```

Copy

Alter the table to add a column with a constraint:

```
ALTER TABLE table1 ADD COLUMN col2 VARCHAR NOT NULL;
```

Copy

The following example specifies that the intent of the column is to hold unique values, but makes clear that the
constraint is not actually enforced. This example also demonstrates how to specify a name for the constraint
(“uniq\_col3” in this case.)

```
ALTER TABLE table1 
  ADD COLUMN col3 VARCHAR NOT NULL CONSTRAINT uniq_col3 UNIQUE NOT ENFORCED;
```

Copy

The following creates a parent table with a primary key constraint and another table with a foreign key constraint
that points to the same columns as the first table’s primary key constraint.

```
CREATE TABLE table2 (
  col1 INTEGER NOT NULL,
  col2 INTEGER NOT NULL,
  CONSTRAINT pkey_1 PRIMARY KEY (col1, col2) NOT ENFORCED
);
CREATE TABLE table3 (
  col_a INTEGER NOT NULL,
  col_b INTEGER NOT NULL,
  CONSTRAINT fkey_1 FOREIGN KEY (col_a, col_b) REFERENCES table2 (col1, col2) NOT ENFORCED
);
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

1. [Syntax for inline constraints](#syntax-for-inline-constraints)
2. [Syntax for out-of-line constraints](#syntax-for-out-of-line-constraints)
3. [Constraint properties](#constraint-properties)
4. [Comments on constraints](#comments-on-constraints)
5. [Usage notes](#usage-notes)
6. [Access control requirements](#access-control-requirements)
7. [Examples with standard tables](#examples-with-standard-tables)