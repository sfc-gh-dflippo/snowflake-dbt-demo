---
description: Translation specification for Teradata grammar syntax to Snowflake
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/README
title: Teradata to Snowflake Translation Reference
---

## Teradata to Snowflake Translation Reference

This directory contains translation references for converting Teradata code to Snowflake-compatible
SQL.

## Contents

### SQL Translation Reference

- [Data Types](sql-translation-reference/data-types.md) - Data type mappings
- [DDL Statements](sql-translation-reference/ddl-teradata.md) - CREATE TABLE, VIEW, etc.
- [DML Statements](sql-translation-reference/dml-teradata.md) - INSERT, UPDATE, DELETE, MERGE
- [Built-in Functions](sql-translation-reference/teradata-built-in-functions.md) - Function
  equivalents
- [Analytic Functions](sql-translation-reference/analytic.md) - Window functions, QUALIFY
- [Database DBC](sql-translation-reference/database-dbc.md) - System catalog translations

### Procedure Translations

- [SQL to Snowflake Scripting](teradata-to-snowflake-scripting-translation-reference.md) - Stored
  procedure conversion
- [SQL to JavaScript](teradata-to-javascript-translation-reference.md) - JavaScript UDF conversion
- [Helpers for Procedures](helpers-for-procedures.md) - Common helper functions

### Script Translations

- [BTEQ to Snowflake SQL](scripts-to-snowflake-sql-translation-reference/bteq.md)
- [MultiLoad Translation](scripts-to-snowflake-sql-translation-reference/mload.md)
- [Scripts to Python](scripts-to-python/README.md) - Python conversion options

### Additional Resources

- [Data Migration Considerations](data-migration-considerations.md)
- [Session Modes](session-modes.md) - ANSI vs Teradata mode handling
- [Iceberg Table Transformations](sql-translation-reference/Iceberg-tables-transformations.md)
