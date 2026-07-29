---
description: SQL Server
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-quoted-identifier
title: SnowConvert AI - SQL Server-Azure Synapse - QUOTED_IDENTIFIER | Snowflake Documentation
---

## Description

This statement controls whether double quotation marks are used to delimit identifiers (such as
table names, column names, etc.) or string literals in SQL Server. When `SET QUOTED_IDENTIFIER` is
ON, identifiers can be delimited by double quotation marks, and literals must be delimited by single
quotation marks. When OFF, double quotation marks are treated as string literal delimiters. Please
visit
[SET QUOTED_IDENTIFIER](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-quoted-identifier-transact-sql?view=sql-server-ver17)
to get more information about this statement.

## Transact-SQL Syntax

```sql
 SET QUOTED_IDENTIFIER { ON | OFF }
```

## Behavior Comparison

### SQL Server Behavior

In SQL Server, the `SET QUOTED_IDENTIFIER` setting determines how double quotes are interpreted:

- **When ON (default)**: Double quotes delimit identifiers, allowing special characters and reserved
  keywords in object names
- **When OFF**: Double quotes are treated as string literal delimiters (similar to single quotes)

### Snowflake Behavior

Snowflake always treats double quotes as identifier delimiters (equivalent to SQL Server’s
`QUOTED_IDENTIFIER ON`). There is no equivalent to the `OFF` setting. Key differences include:

1. **Case Sensitivity**:
   - Unquoted identifiers are automatically converted to uppercase
   - Quoted identifiers preserve exact case and become case-sensitive

2. **QUOTED_IDENTIFIERS_IGNORE_CASE Parameter**: Controls case sensitivity for quoted identifiers

## Sample Source Patterns

### SET QUOTED_IDENTIFIER ON

When `QUOTED_IDENTIFIER` is ON in SQL Server, double quotes can be used to delimit identifiers
containing spaces or special characters.

#### SQL Server

```sql
 SET QUOTED_IDENTIFIER ON;

 CREATE TABLE "Order Details" (
     "Order ID" INT,
     "Product Name" VARCHAR(50),
     "Unit Price" DECIMAL(10,2)
 );

 SELECT "Order ID", "Product Name" FROM "Order Details";
```

#### Snowflake

```sql
----** SSC-FDM-TS0033 - SET QUOTED_IDENTIFIER STATEMENT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE **
--SET QUOTED_IDENTIFIER ON

 CREATE OR REPLACE TABLE "Order Details" (
     "Order ID" INT,
     "Product Name" VARCHAR(50),
     "Unit Price" DECIMAL(10, 2)
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "09/22/2025",  "domain": "no-domain-provided" }}'
;

 SELECT
     "Order ID",
     "Product Name"
 FROM
     "Order Details";
```

##### Example of the Difference

Let’s assume you’ve migrated a table from a SQL Server database with a case-insensitive collation
(\_CI):

#### SQL Server (with \_CI collation)

```sql
-- This statement is valid
SELECT "MyColumn" FROM "MyTable";

-- This statement is also valid and returns the same result
SELECT "mycolumn" FROM "MyTable";
```

In this case, the \_CI collation makes the two SELECT statements interchangeable.

#### Snowflake 2

```sql
-- This statement is valid
SELECT "MyColumn" FROM "MyTable";

-- This statement will fail because "mycolumn" does not match "MyColumn"
SELECT "mycolumn" FROM "MyTable";
-- ERROR:  SQL compilation error: error in select clause: mycolumn does not exist
```

The Snowflake behavior is different because it respects the case of the quoted identifier by
default. It could be approachable by altering the session using.

```sql
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = TRUE;
```

If you want to set the parameter at the account level, you can use the following command:

```sql
ALTER ACCOUNT SET QUOTED_IDENTIFIERS_IGNORE_CASE = TRUE;
```

This will set the parameter for all sessions associated with the account. For further information,
check the following [documentation](https://docs.snowflake.com/en/sql-reference/identifiers-syntax);

### SET QUOTED_IDENTIFIER OFF

When `QUOTED_IDENTIFIER` is OFF in SQL Server, double quotes are treated as string delimiters.

#### SQL Server 2

```sql
 SET QUOTED_IDENTIFIER OFF;

 -- Double quotes treated as string literals
 SELECT * FROM customers WHERE name = "John Doe";

 -- Must use square brackets for identifiers with spaces
 SELECT [Order ID] FROM [Order Details];
```

#### Snowflake 2 2

```sql
 ----** SSC-FDM-TS0028 - QUOTED_IDENTIFIER OFF behavior not supported in Snowflake **
 -- Double quotes always delimit identifiers in Snowflake
 -- Use single quotes for string literals
 SELECT * FROM customers WHERE name = 'John Doe';

 -- Double quotes delimit identifiers (case-sensitive)
 SELECT "Order ID" FROM "Order Details";
```

## Migration Considerations

1. **Review Identifier Casing**: Ensure consistent casing when migrating to Snowflake, especially
   for quoted identifiers
2. **String Literals**: Replace double-quoted string literals with single-quoted literals
3. **Use QUOTED_IDENTIFIERS_IGNORE_CASE**: Consider setting this parameter to `TRUE` early in
   migration to reduce case sensitivity issues
4. **Test Thoroughly**: Verify all object references work correctly after migration

## Related EWIs and FDMs

1. **SSC-FDM-TS0028**: SET QUOTED_IDENTIFIER OFF behavior not supported in Snowflake - double quotes
   always delimit identifiers
