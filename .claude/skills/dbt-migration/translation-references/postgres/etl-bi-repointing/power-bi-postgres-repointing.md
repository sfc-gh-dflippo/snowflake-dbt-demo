---
description:
  The Power BI repointing is a feature that provides an easy way to redefine the connections from
  the M language in the Power Query Editor. This means that the connection parameters will be
  redefined to
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/etl-bi-repointing/power-bi-postgres-repointing
title: SnowConvert AI - PostgreSQL - Power BI Repointing | Snowflake Documentation
---

## Description[¶](#description)

The Power BI repointing is a feature that provides an easy way to redefine the connections from the
M language in the Power Query Editor. This means that the connection parameters will be redefined to
point to the Snowflake migration database context. For Postgres, the method in M Language that
defined the connection is `PostgreSQL.Database(...).` In Snowflake, there is a connector that
depends on some other parameters and the main connection is defined by `Snowflake.Database(...)`
method.

## Source Pattern Samples[¶](#source-pattern-samples)

### Entity Repointing Case: Table[¶](#entity-repointing-case-table)

This case refers to connections that do not contain embedded SQL. This means that the user has
established a connection from Power BI to a table.

**PostgreSQL Connection in the Power Query Editor**

```
let
    Source = PostgreSQL.Database("your_connection", "mydatabase"),
    public_products = Source{[Schema="public",Item="products"]}[Data]
in
    public_products
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="public", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="PRODUCTS", Kind="Table"]}[Data],
    public_products = Table.RenameColumns(SourceSfTbl, {{ "PRODUCT_ID", "product_id"}, { "PRODUCT_NAME", "product_name"}, { "PRICE", "price"}, { "STOCK_QUANTITY", "stock_quantity"}})
in
    public_products
```

Copy

### Entity Repointing Case: View[¶](#entity-repointing-case-view)

This case refers to connections that do not contain embedded SQL. This means that the user has
established a connection from Power BI to a view. The view uses the same pattern as the tables. It
will only be validated with the symbol table; otherwise, it will be converted to a table. DDLs are
important to this pattern.

**PostgreSQL Connection in the Power Query Editor**

```
let
    Source = PostgreSQL.Database("your_connection", "mydatabase"),
    public_expensive_products = Source{[Schema="public",Item="expensive_products"]}[Data]
in
    public_expensive_products
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="public", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="EXPENSIVE_PRODUCTS", Kind="View"]}[Data],
    public_expensive_products = Table.RenameColumns(SourceSfTbl, {{ "PRODUCT_ID", "product_id"}, { "PRODUCT_NAME", "product_name"}, { "PRICE", "price"}})
in
    public_expensive_products
```

Copy

### Embedded SQL Case[¶](#embedded-sql-case)

This case refers to connections that contain embedded SQL inside them. This sample shows a simple
query, but SnowConvert AI covers a range of larger scenarios. Besides, depending on the migrated
query, there may be warning messages known as EWI—PRF—FDM. This will help the user identify patterns
that need extra attention.

**PostgreSQL Connection in the Power Query Editor**

```
let
    Source = Value.NativeQuery(PostgreSQL.Database("your_connection", "mydatabase"), "SELECT * FROM expensive_products", null, [EnableFolding=true])
in
    Source
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "SELECT * FROM
expensive_products", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "PRODUCT_ID", "product_id"}, { "PRODUCT_NAME", "product_name"}, { "PRICE", "price"}})
in
    Source
```

Copy
