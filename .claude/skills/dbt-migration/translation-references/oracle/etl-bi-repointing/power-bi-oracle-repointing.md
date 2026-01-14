---
description:
  The Power BI repointing is a feature that provides an easy way to redefine the connections from
  the M language in the Power Query Editor. This means that the connection parameters will be
  redefined to
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/etl-bi-repointing/power-bi-oracle-repointing
title: SnowConvert AI - Oracle - Power BI Repointing | Snowflake Documentation
---

## Description[¶](#description)

The Power BI repointing is a feature that provides an easy way to redefine the connections from the
M language in the Power Query Editor. This means that the connection parameters will be redefined to
point to the Snowflake migration database context. For Oracle, the method in M Language that defined
the connection is `Oracle.Database(...).` In Snowflake, there is a connector that depends on some
other parameters and the main connection is defined by `Snowflake.Database(...)` method.

## Source Pattern Samples[¶](#source-pattern-samples)

### Entity Repointing Case: Table[¶](#entity-repointing-case-table)

This case refers to connections that do not contain embedded SQL. This means that the user has
established a connection from Power BI to a table.

**Oracle Connection in the Power Query Editor**

```
let
    Source = Oracle.Database("the_oracle_server", [HierarchicalNavigation=true]),
    #"C##POWERBI_USER" = Source{[Schema="C##POWERBI_USER"]}[Data],
    EMPLOYEES_B1 = #"C##POWERBI_USER"{[Name="EMPLOYEES_B"]}[Data]
in
    EMPLOYEES_B1
```

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="C##POWERBI_USER", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="EMPLOYEES_B", Kind="Table"]}[Data],
    EMPLOYEES_B1 = Table.RenameColumns(SourceSfTbl, {{ "EMPLOYEE_ID", "EMPLOYEE_ID"}, { "FIRST_NAME", "FIRST_NAME"}, { "LAST_NAME", "LAST_NAME"}, { "DEPARTMENT_ID", "DEPARTMENT_ID"}})
in
    EMPLOYEES_B1
```

### Entity Repointing Case: View[¶](#entity-repointing-case-view)

This case refers to connections that do not contain embedded SQL. This means that the user has
established a connection from Power BI to a view.

**Oracle Connection in the Power Query Editor**

```
let
    Source = Oracle.Database("the_oracle_server", [HierarchicalNavigation=true]),
    #"C##POWERBI_USER" = Source{[Schema="C##POWERBI_USER"]}[Data],
    DEPARTMENTS_V1 = #"C##POWERBI_USER"{[Name="DEPARTMENTS_V"]}[Data]
in
    DEPARTMENTS_V1
```

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="C##POWERBI_USER", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="DEPARTMENTS_V", Kind="View"]}[Data],
    DEPARTMENTS_V1 = Table.RenameColumns(SourceSfTbl, {{ "DEPARTMENT_ID", "DEPARTMENT_ID"}, { "DEPARTMENT_NAME", "DEPARTMENT_NAME"}})
in
    DEPARTMENTS_V1
```

### Embedded SQL Case[¶](#embedded-sql-case)

This case refers to connections that contain embedded SQL inside them. This sample shows a simple
query, but SnowConvert AI covers a range of larger scenarios. Besides, depending on the migrated
query, there may be warning messages known as EWI—PRF—FDM. This will help the user identify patterns
that need extra attention.

**Oracle Connection in the Power Query Editor**

```
let
    Source = Oracle.Database("the_oracle_server", [HierarchicalNavigation=true, Query="SELECT * FROM DEPARTMENTS_V"])
in
    Source
```

**Snowflake Connection in the Power Query Editor**

```
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "SELECT * FROM
DEPARTMENTS_V", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "DEPARTMENT_ID", "DEPARTMENT_ID"}, { "DEPARTMENT_NAME", "DEPARTMENT_NAME"}})
in
    Source
```
