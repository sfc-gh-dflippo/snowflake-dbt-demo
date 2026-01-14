---
description: Translation specification for SQL Server and Azure Synapse syntax to Snowflake
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/README
title: SQL Server / Azure Synapse to Snowflake Translation Reference
---

# SQL Server / Azure Synapse to Snowflake Translation Reference

This directory contains translation references for converting SQL Server and Azure Synapse code to Snowflake-compatible SQL.

## Contents

### Data Types

- [Data Types](transact-data-types.md) - Complete data type mapping table

### DDL Statements

- [CREATE TABLE](transact-create-table.md)
- [CREATE VIEW](transact-create-view.md)
- [CREATE INDEX](transact-create-index.md)
- [CREATE MATERIALIZED VIEW](transact-create-materialized-view.md)
- [ALTER TABLE](transact-alter-statement.md)

### Procedures and Functions

- [CREATE PROCEDURE (JavaScript)](transact-create-procedure.md) - JavaScript conversion
- [CREATE PROCEDURE (Snowflake Scripting)](transact-create-procedure-snow-script.md)
- [CREATE FUNCTION](transact-create-function.md)
- [Continue Handler](transact-continue-handler.md) - TRY/CATCH translation
- [Exit Handler](transact-exit-handler.md)

### DML and Queries

- [DML Statements](transact-dmls.md) - INSERT, UPDATE, DELETE, MERGE
- [SELECT](transact-select.md) - Query syntax
- [General Statements](transact-general-statements.md)

### Functions

- [Built-in Functions](transact-built-in-functions.md)
- [Built-in Procedures](transact-built-in-procedures.md)

### System Objects

- [System Tables](transact-system-tables.md) - sys.\* table equivalents

### Settings

- [ANSI_NULLS](transact-ansi-nulls.md)
- [QUOTED_IDENTIFIER](transact-quoted-identifier.md)
