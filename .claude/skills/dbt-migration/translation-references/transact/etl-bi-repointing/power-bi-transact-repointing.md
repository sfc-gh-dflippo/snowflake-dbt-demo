---
description: SQL Server
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/etl-bi-repointing/power-bi-transact-repointing
title: SnowConvert AI - Transact - Power BI Repointing | Snowflake Documentation
---

## Description[¶](#description)

The Power BI repointing is a feature that provides an easy way to redefine the connections from the
M language in the Power Query Editor. This means that the connection parameters will be redefined to
point to the Snowflake migration database context. For SQL Server and Azure Synapse, the method in M
Language that defined the connection is `Sql.Database(...)`. In Snowflake, there is a connector that
depends on some other parameters and the main connection is defined by `Snowflake.Database(...)`
method.

## Source Pattern Samples[¶](#source-pattern-samples)

This section will explain the cases currently addressed by SnowConvert AI.

### Simple Entity Repointing Case[¶](#simple-entity-repointing-case)

Even a simple connection to a table from Power BI requires many transformations to be used with the
implicit Power BI connector from Snowflake. In this case, SnowConvert AI adds new information
variables such as database and schema, and calls the source table with the implicit type (it can
also be a view).

Also, SnowConvert AI generates a mapping between the columns to match the text case with the
database migration context or, if possible, with the Power BI report internal information.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

```
let
    Source = Sql.Database("your_connection", "LibraryDatabase"),
    dbo_Authors = Source{[Schema="dbo",Item="Authors"]}[Data]
in
    dbo_Authors
```

Copy

**Snowflake SQL Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="DBO", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="BOOKS", Kind="Table"]}[Data],
    dbo_Books = Table.RenameColumns(SourceSfTbl, {{ "BOOKID", "BookID"}, { "TITLE", "Title"}, { "AUTHORID", "AuthorID"}, { "PUBLICATIONYEAR", "PublicationYear"}})
in
    dbo_Books
```

Copy

### Simple Entity With Multiple Lines Repointing Case[¶](#simple-entity-with-multiple-lines-repointing-case)

In this case “Filtered Rows” is an aditional step into the logic of the query. In the repointing
version, the additional logic is preserved as it is.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

```
let
  Source = Sql.Database("your_connection", "mytestdb"),
  dbo_Employee = Source{[Schema="dbo",
  Item="Employee"]}[Data],
  #"Filtered Rows" = Table.SelectRows(dbo_Employee, each Text.StartsWith([name], "John"))
in
  #"Filtered Rows"
```

Copy

**Snowflake SQL Connection in the Power Query Editor**

```
let
  Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
  SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
  SourceSfSchema = SourceSfDb{[Name="DBO", Kind="Schema"]}[Data],
  SourceSfTbl = SourceSfSchema{[Name="EMPLOYEE", Kind="Table"]}[Data],
  dbo_Employee = SourceSfTbl,
  #"Filtered Rows" = Table.SelectRows(dbo_Employee, each Text.StartsWith([name], "John"))
in
  #"Filtered Rows"
```

Copy

### Embedded SQL Query Repointing Case[¶](#embedded-sql-query-repointing-case)

For the SQL queries embedded inside the connections, SnowConvert AI will extract, migrate, and
re-insert these queries. Warning messages in the migrated queries may require extra attention. In
this case, the warning message does not stop the query from being run in the Snowflake database.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

```
let
    Source = Sql.Database("your_connection", "LibraryDatabase", [Query="SELECT DISTINCT#(lf)    B.Title#(lf)FROM#(lf)    DBO.Books AS B#(lf)JOIN#(lf)    DBO.Authors AS A ON B.AuthorID = A.AuthorID#(lf)JOIN#(lf)    DBO.BookGenres AS BG ON B.BookID = BG.BookID#(lf)JOIN#(lf)    DBO.Genres AS G ON BG.GenreID = G.GenreID#(lf)WHERE#(lf)    A.Nationality = 'American' AND G.Origin = 'USA'#(lf)ORDER BY#(lf)    B.Title;", CreateNavigationProperties=false])
in
    Source
```

Copy

**Snowflake SQL Connection in the Power Query Editor**

```
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS ""DBO.Books"", ""DBO.Authors"", ""DBO.BookGenres"", ""DBO.Genres"" **
SELECT DISTINCT
    B.Title
FROM
    DBO.Books AS B
    JOIN
        DBO.Authors AS A
        ON B.AuthorID = A.AuthorID
    JOIN
        DBO.BookGenres AS BG
        ON B.BookID = BG.BookID
    JOIN
        DBO.Genres AS G
        ON BG.GenreID = G.GenreID
WHERE
    A.Nationality = 'American' AND G.Origin = 'USA'
ORDER BY B.Title", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "TITLE", "Title"}})
in
    Source
```

Copy

### Embedded SQL Query With Multiple Lines Repointing Case[¶](#embedded-sql-query-with-multiple-lines-repointing-case)

This case showcases the connection with SQL queries and multiple lines of logic after the connection
logic.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

```
let
  Source = Sql.Database("your_connection", "mytestdb", [Query="SELECT DISTINCT#(lf)    P.ProductName,#(lf)    P.Category,#(lf)    P.StockQuantity#(lf)FROM#(lf)    Products AS P#(lf)WHERE#(lf)    P.StockQuantity > 0#(lf)ORDER BY#(lf)    P.Category ASC;"]),
  #"Filtered Rows" = Table.SelectRows(Source, each Text.StartsWith([Name], "Cards"))
in
 #"Filtered Rows"
```

Copy

**Snowflake SQL Connection in the Power Query Editor**

```
let
  Source = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT ""Products"" **
SELECT DISTINCT
    P.ProductName,
    P.Category,
    P.StockQuantity
FROM
    Products AS P
WHERE
    P.StockQuantity > 0
ORDER BY P.Category ASC", null, [EnableFolding=true]),
  #"Filtered Rows" = Table.SelectRows(Source, each Text.StartsWith([Name], "Cards"))
in
  #"Filtered Rows"
```

Copy

### Embedded SQL Query With Column Renaming Repointing Case[¶](#embedded-sql-query-with-column-renaming-repointing-case)

At the moment, column renaing for SQL queries cases are only applied if the internal infromation of
the provided Power BI report contains this information.

**Transact-SQL | Azure Synapse Connection in the Power Query Editor**

```
let
    Source = Sql.Database("your_connection", "SalesSampleDB", [Query="SELECT DISTINCT#(lf)    P.ProductName,#(lf)    P.Category,#(lf)    P.StockQuantity#(lf)FROM#(lf)    Products AS P#(lf)WHERE#(lf)    P.StockQuantity > 0#(lf)ORDER BY#(lf)    P.Category ASC;"])
in
    Source
```

Copy

**Snowflake SQL Connection in the Power Query Editor**

```
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT ""Products"" **
SELECT DISTINCT
    P.ProductName,
    P.Category,
    P.StockQuantity
FROM
    Products AS P
WHERE
    P.StockQuantity > 0
ORDER BY P.Category ASC", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "PRODUCTNAME", "ProductName"}, { "CATEGORY", "Category"}, { "STOCKQUANTITY", "StockQuantity"}})
in
    Source
```

Copy

### Function For Entity Case Repointing Case[¶](#function-for-entity-case-repointing-case)

Currently, the functions are only supported for entities import case, and Transact only.

**Transact-SQL Connection in the Power Query Editor**

```
let
  Source = Sql.Database("your_connection", "mytestdb"),
  dbo_MultiParam = Source{[Schema="dbo",Item="MultiParam"]}[Data],
  #"Invoked Functiondbo_MultiParam1" = dbo_MultiParam(1,"HELLO")
in
  #"Invoked Functiondbo_MultiParam1"
```

Copy

**Snowflake SQL Connection in the Power Query Editor**

```
let
  Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
  SourceSfDb = Source{[Name="mytestdb, Kind="Database"]}[Data],
  SourceSfFunc = (x, y) => Value.NativeQuery(SourceSfDb, "SELECT DBO.MultiParam(" & Text.From(x) & "," &  (if y = null then null else ("'" & y & "'"))  & ")"),
  dbo_MultiParam = SourceSfFunc,
  #"Invoked Functiondbo_MultiParam1" = dbo_MultiParam(1,"HELLO")
in
  #"Invoked Functiondbo_MultiParam1"
```

Copy
