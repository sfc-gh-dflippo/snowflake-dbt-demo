---
description: SQL Server
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-ansi-nulls
title: SnowConvert AI - SQL Server-Azure Synapse - ANSI_NULLS | Snowflake Documentation
---

## Description[¶](#description)

This statement specifies the ISO-compliant behavior of the Equals and Not Equal to comparison
operators when used with null values in SQLServer. Please visit
[SET ANSI_NULLS](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-ansi-nulls-transact-sql?view=sql-server-ver16)
to get more information about this statement.

## Transact-SQL Syntax[¶](#transact-sql-syntax)

```
 SET ANSI_NULLS { ON | OFF }
```

## Sample Source Patterns[¶](#sample-source-patterns)

### SET ANSI_NULLS ON[¶](#set-ansi-nulls-on)

_“SET ANSI_NULLS ON affects a comparison only if one of the operands of the comparison is either a
variable that is NULL or a literal NULL. If both sides of the comparison are columns or compound
expressions, the setting does not affect the comparison._” (SQLServer ANSI_NULLS article).

Snowflake does not support this statement, so in the case of ANSI_NULLS ON, this is marked with an
FDM
([SSC-FDM-TS0027](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0027))
because it does not have relevance in executing equal and not equal comparison operations. Here, you
can find an explanation of the
[NULL treatment in Snowflake](https://community.snowflake.com/s/article/NULL-handling-in-Snowflake).

#### SQL Server[¶](#sql-server)

```
 SET ANSI_NULLS ON;
```

#### Snowflake[¶](#snowflake)

```
 ----** SSC-FDM-TS0027 - SET ANSI_NULLS ON STATEMENT MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE **
--SET ANSI_NULLS ON
```

### SET ANSI_NULLS OFF[¶](#set-ansi-nulls-off)

“_When ANSI_NULLS is OFF, the Equals (`=`) and Not Equal To (`<>`) comparison operators do not
follow the ISO standard. A SELECT statement that uses `WHERE column_name = NULL` returns the rows
that have null values in column_name. A SELECT statement that uses `WHERE column_name <> NULL`
returns the rows that have non-NULL values in the column_”. (SQLServer ANSI_NULLS article).

In the case of the ANSI_NULLS OFF statement, this one is marked with an EWI
([SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040))
because it requires extra manual effort.

#### SQL Server[¶](#id1)

```
 SET ANSI_NULLS OFF;
```

#### Snowflake[¶](#id2)

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'SIMPLE SET STATEMENT' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
SET ANSI_NULLS OFF;
```

## Related EWIs[¶](#related-ewis)

1. [SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040):
   The statement is not supported in Snowflake
2. [SSC-FDM-0027](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0027):
   SET ANSI_NULLS ON statement may have different behavior in Snowflake
