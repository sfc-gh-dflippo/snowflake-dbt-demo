---
description:
  The Power BI repointing is a feature that provides an easy way to redefine the connections from
  the M language in the Power Query Editor. This means that the connection parameters will be
  redefined to
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/etl-bi-repointing/power-bi-redshift-repointing
title: SnowConvert AI - Redshift - Power BI Repointing | Snowflake Documentation
---

## Description[¶](#description)

The Power BI repointing is a feature that provides an easy way to redefine the connections from the
M language in the Power Query Editor. This means that the connection parameters will be redefined to
point to the Snowflake migration database context. For Redshift, the method in M Language that
defined the connection is `AmazonRedshift.Database(...).` In Snowflake, there is a connector that
depends on some other parameters and the main connection is defined by `Snowflake.Database(...)`
method.

## Source Pattern Samples[¶](#source-pattern-samples)

### Entity Repointing Case: Table[¶](#entity-repointing-case-table)

This case refers to connections that do not contain embedded SQL. This means that the user has
established a connection from Power BI to a table.

**Redshift Connection in the Power Query Editor**

```
let
    Source = AmazonRedshift.Database("your_connection","snowconvert"),
    public = Source{[Name="public"]}[Data],
    authors1 = public{[Name="authors"]}[Data]
in
    authors1
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="public", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="AUTHORS", Kind="Table"]}[Data],
    authors1 = Table.RenameColumns(SourceSfTbl, {{ "AUTHOR_ID", "author_id"}, { "FIRST_NAME", "first_name"}, { "LAST_NAME", "last_name"}, { "BIRTH_YEAR", "birth_year"}})
in
    authors1
```

Copy

### Entity Repointing Case: View[¶](#entity-repointing-case-view)

This case refers to connections that do not contain embedded SQL. This means that the user has
established a connection from Power BI to a view.

**Redshift Connection in the Power Query Editor**

```
let
    Source = AmazonRedshift.Database("your_connection","snowconvert"),
    public = Source{[Name="public"]}[Data],
    author_books_view1 = public{[Name="author_books_view"]}[Data]
in
    author_books_view1
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    Source = Snowflake.Databases(SF_SERVER_LINK, SF_WAREHOUSE_NAME),
    SourceSfDb = Source{[Name=SF_DB_NAME, Kind="Database"]}[Data],
    SourceSfSchema = SourceSfDb{[Name="public", Kind="Schema"]}[Data],
    SourceSfTbl = SourceSfSchema{[Name="AUTHOR_BOOKS_VIEW", Kind="Table"]}[Data],
    author_books_view1 = Table.RenameColumns(SourceSfTbl, {{ "BOOK_TITLE", "book_title"}, { "AUTHOR_FULL_NAME", "author_full_name"}, { "PUBLICATION_YEAR", "publication_year"}, { "GENRE", "genre"}})
in
    author_books_view1
```

Copy

### Embedded SQL Case[¶](#embedded-sql-case)

This case refers to connections that contain embedded SQL inside them. This sample shows a simple
query, but SnowConvert AI covers a range of larger scenarios. Besides, depending on the migrated
query, there may be warning messages known as EWI—PRF—FDM. This will help the user identify patterns
that need extra attention.

**Redshift Connection in the Power Query Editor**

```
let
    Source = Value.NativeQuery(AmazonRedshift.Database("your_connection","snowconvert"), "SELECT * FROM authors LIMIT 5", null, [EnableFolding=true])
in
    Source
```

Copy

**Snowflake Connection in the Power Query Editor**

```
let
    SfSource = Value.NativeQuery(Snowflake.Databases(SF_SERVER_LINK,SF_WAREHOUSE_NAME,[Implementation="2.0"]){[Name=SF_DB_NAME]}[Data], "--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT ""authors"" **
SELECT * FROM
authors
LIMIT 5", null, [EnableFolding=true]),
    Source = Table.RenameColumns(SfSource, {{ "AUTHOR_ID", "author_id"}, { "FIRST_NAME", "first_name"}, { "LAST_NAME", "last_name"}, { "BIRTH_YEAR", "birth_year"}})
in
    Source
```

Copy
