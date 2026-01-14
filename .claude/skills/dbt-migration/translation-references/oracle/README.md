---
description: Translation specification for Oracle grammar syntax to Snowflake
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/README
title: Oracle to Snowflake Translation Reference
---

# Oracle to Snowflake Translation Reference

This directory contains translation references for converting Oracle code to Snowflake-compatible SQL.

## Contents

### Basic Elements

- [Data Types](basic-elements-of-oracle-sql/data-types/README.md) - Data type mappings
- [Literals](basic-elements-of-oracle-sql/literals.md) - Literal syntax conversion

### SQL Statements

- [SQL Translation Reference](sql-translation-reference/README.md) - DDL statements
- [CREATE TABLE](sql-translation-reference/create-table.md)
- [CREATE VIEW](sql-translation-reference/create-view.md)
- [CREATE MATERIALIZED VIEW](sql-translation-reference/create-materialized-view.md)

### Functions

- [Built-in Functions](functions/README.md) - Function equivalents
- [Built-in Packages](built-in-packages.md) - DBMS\_\* package translations

### PL/SQL Translation

- [PL/SQL to Snowflake Scripting](pl-sql-to-snowflake-scripting/README.md) - Procedure conversion
- [PL/SQL to JavaScript](pl-sql-to-javascript/README.md) - JavaScript UDF conversion
- [Cursors](pl-sql-to-snowflake-scripting/cursor.md)
- [Collections and Records](pl-sql-to-snowflake-scripting/collections-and-records.md)
- [Packages](pl-sql-to-snowflake-scripting/packages.md)

### Queries

- [SQL Queries and Subqueries](sql-queries-and-subqueries/selects.md)
- [Joins](sql-queries-and-subqueries/joins.md)

### Additional Resources

- [Pseudocolumns](pseudocolumns.md) - ROWNUM, ROWID, etc.
- [SQL\*Plus](sql-plus.md) - SQL\*Plus command handling
- [Wrapped Objects](wrapped-objects.md) - Encrypted code handling
- [Sample Data](sample-data.md)
