---
description: Creates a new view. (Vertica SQL Language Reference Create view statement)
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/vertica/vertica-create-view
title: SnowConvert AI - Vertica - CREATE VIEW | Snowflake Documentation
---

## Description[¶](#description)

Creates a new view.
([Vertica SQL Language Reference Create view statement](https://docs.vertica.com/25.2.x/en/sql-reference/statements/create-statements/create-view/))

## Grammar Syntax[¶](#grammar-syntax)

```
CREATE [ OR REPLACE ] VIEW [[database.]schema.]view [ (column[,...]) ]
  [ {INCLUDE|EXCLUDE} [SCHEMA] PRIVILEGES ] AS query
```

## Sample Source Patterns[¶](#sample-source-patterns)

Success

This syntax is fully supported in
[Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

### Vertica[¶](#vertica)

```
CREATE OR REPLACE VIEW mySchema.myuser(
userlastname
)
AS
SELECT lastname FROM users;
```

#### Snowflake[¶](#snowflake)

```
CREATE OR REPLACE VIEW mySchema.myuser
(
userlastname
)
AS
SELECT lastname FROM
    users;
```

### Inherited Schema Privileges Clause[¶](#inherited-schema-privileges-clause)

`INCLUDE SCHEMA PRIVILEGES` is a Vertica-specific feature that governs how privileges are inherited,
in this case, potentially from the schema level. Snowflake does not have a direct equivalent for
this clause within its `CREATE VIEW` syntax. Privileges in Snowflake are managed explicitly through
`GRANT` statements.

Warning

This syntax is not supported in Snowflake.

#### BigQuery[¶](#bigquery)

```
CREATE OR REPLACE VIEW mySchema.myuser(
userlastname
)
INCLUDE SCHEMA PRIVILEGES
AS
SELECT lastname FROM users;
```

#### Snowflake[¶](#id1)

```
CREATE OR REPLACE VIEW mySchema.myuser
(
userlastname
)
!!!RESOLVE EWI!!! /*** SSC-EWI-VT0001 - INHERITED PRIVILEGES CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
INCLUDE SCHEMA PRIVILEGES
AS
SELECT lastname FROM
    users;
```

### Known Issues[¶](#known-issues)

There are no known Issues.

### Related EWIs[¶](#related-ewis)

1. [SSC-EWI-VT0001](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/conversion-issues/verticaEWI#ssc-ewi-vt0001):
   Inherited privileges clause is not supported in Snowflake.
