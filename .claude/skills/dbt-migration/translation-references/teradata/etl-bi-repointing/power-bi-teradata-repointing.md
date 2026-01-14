---
description:
  The Power BI repointing is a feature that provides an easy way to redefine the connections from
  the M language in the Power Query Editor. This means that the connection parameters will be
  redefined to
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/etl-bi-repointing/power-bi-teradata-repointing
title: SnowConvert AI - Teradata - Power BI Repointing | Snowflake Documentation
---

## Description[¶](#description)

The Power BI repointing is a feature that provides an easy way to redefine the connections from the
[M language in the Power Query Editor](https://learn.microsoft.com/en-us/powerquery-m/). This means
that the connection parameters will be redefined to point to the Snowflake migration database
context. For Teradata, the method in [M Language](https://learn.microsoft.com/en-us/powerquery-m/)
that defined the connection is `Teradata.Database(...)`. In Snowflake, there is a connector that
depends on some other parameters and the main connection is defined by `Snowflake.Database(...)`
method. In addition, there is a limited support to `ODBC.Query` connector only for Teradata as a
source languge in the migration. This means that the source connection parameters (of Teradata
connections) will be redefine to point to the Snowflake migration database context.

## Source Pattern Samples[¶](#source-pattern-samples)

### Entity Repointing Case: Table[¶](#entity-repointing-case-table)

This case refers to connections that do not contain embedded SQL. This means that the user has
established a connection from Power BI to a table.

**Teradata Connection in the Power Query Editor**

```
let
    Source = Teradata.Database("the_teradata_server", [HierarchicalNavigation=true]),
    databaseTest = Source{[Schema="databaseTest"]}[Data],
    employees1 = databaseTest{[Name="employees"]}[Data]
in
    employees1
```

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="databaseTest", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="EMPLOYEES", Kind="Table"]}[Data],
    Employees1 = Table.RenameColumns(SourceSfTbl, {{ "EMPLOYEEID", "EmployeeID"}, { "FIRSTNAME", "FirstName"}, { "LASTNAME", "LastName"}, { "HIREDATE", "HireDate"}, { "SALARY", "Salary"}, { "DEPARTMENTID", "DepartmentID"}})
in
    Employees1
```

### Entity Repointing Case: View[¶](#entity-repointing-case-view)

This case refers to connections that do not contain embedded SQL. This means that the user has
established a connection from Power BI to a view.

**Teradata Connection in the Power Query Editor**

```
let
    Source = Teradata.Database("the_teradata_server", [HierarchicalNavigation=true]),
    databaseTest = Source{[Schema="databaseTest"]}[Data],
    EmployeeSalaryBonusView1 = databaseTest{[Name="EmployeeSalaryBonusView"]}[Data]
in
    EmployeeSalaryBonusView1
```

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="databaseTest", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="EMPLOYEESALARYBONUSVIEW", Kind="Table"]}[Data],
    EmployeeSalaryBonusView1 = Table.RenameColumns(SourceSfTbl, {{ "FIRSTNAME", "FirstName"}, { "LASTNAME", "LastName"}, { "HIREDATE", "HireDate"}})
in
    EmployeeSalaryBonusView1
```

### Embedded SQL Case[¶](#embedded-sql-case)

This case refers to connections that contains embedded SQL inside of them. This sample show a simple
query but SnowConvert AI covers a range of more larger scenarios. Besides, there may be warning
messages knows as EWI- PRF - FDM depending on the migrated query. This will help the user identifies
patterns that needs extra attention.

**Teradata Connection in the Power Query Editor**

```
let
    Source = Teradata.Database("the_teradata_server", [HierarchicalNavigation=true, Query="SELECT *#(lf)FROM databaseTest.employees"])
in
    Source
```

**Snowflake Connection in the Power Query Editor**

```
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "SELECT * FROM databaseTest.employees", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "EMPLOYEEID", "EmployeeID"}, { "FIRSTNAME", "FirstName"}, { "LASTNAME", "LastName"}, { "HIREDATE", "HireDate"}, { "SALARY", "Salary"}, { "DEPARTMENTID", "DepartmentID"}})
in
    Source
```

### ODBC.Query Case[¶](#odbc-query-case)

At the moment it is supported only `ODBC.Query` connector. Other connectors as `ODBC.DataSource` are
not supported.

This case refers to connections that contains embedded SQL inside of an `ODBC.Query` connector.
Notice that all connections with `ODBC.Query` will be taken as Teradata source when migrating
Teradata. Please, be aware of your report connection definitions.

**Teradata Connection in the Power Query Editor**

```
let
  Source = Odbc.Query("dsn=TERADATA_TEST", "SELECT * FROM TEST_TABLE")
in
  Source
```

**Snowflake Connection in the Power Query Editor**

```
let
   Source = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "SELECT * FROM TEST_TABLE", null, [EnableFolding=true])
in
   Source
```
