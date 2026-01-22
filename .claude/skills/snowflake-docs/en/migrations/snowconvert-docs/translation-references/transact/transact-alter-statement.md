---
auto_generated: true
description: Translation reference for all the DDL statements that are preceded by
  the ALTER keyword.
last_scraped: '2026-01-14T16:53:59.062059+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-alter-statement
title: SnowConvert AI - SQL Server-Azure Synapse - ALTER | Snowflake Documentation
---

1. [Overview](../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../guides/overview-db.md)
8. [Data types](../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../README.md)

    * Tools

      * [SnowConvert AI](../../overview.md)

        + General

          + [About](../../general/about.md)
          + [Getting Started](../../general/getting-started/README.md)
          + [Terms And Conditions](../../general/terms-and-conditions/README.md)
          + [Release Notes](../../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../general/user-guide/snowconvert/README.md)
            + [Project Creation](../../general/user-guide/project-creation.md)
            + [Extraction](../../general/user-guide/extraction.md)
            + [Deployment](../../general/user-guide/deployment.md)
            + [Data Migration](../../general/user-guide/data-migration.md)
            + [Data Validation](../../general/user-guide/data-validation.md)
            + [Power BI Repointing](../../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../general/technical-documentation/README.md)
          + [Contact Us](../../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../general/README.md)
          + [Teradata](../teradata/README.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](README.md)

            - [ANSI NULLS](transact-ansi-nulls.md)
            - [QUOTED\_IDENTIFIER](transact-quoted-identifier.md)
            - [Built-in Functions](transact-built-in-functions.md)
            - [Built-in Procedures](transact-built-in-procedures.md)
            - Data Definition Language

              - [ALTER TABLE](transact-alter-statement.md)
              - [CONTINUE HANDLER](transact-continue-handler.md)
              - [EXIT HANDLER](transact-exit-handler.md)
              - [CREATE FUNCTION](transact-create-function.md)
              - [CREATE INDEX](transact-create-index.md)
              - [CREATE MATERIALIZED VIEW](transact-create-materialized-view.md)
              - [CREATE PROCEDURE (JavaScript)](transact-create-procedure.md)")
              - [CREATE PROCEDURE (Snowflake Scripting)](transact-create-procedure-snow-script.md)")
              - [CREATE TABLE](transact-create-table.md)
              - [CREATE VIEW](transact-create-view.md)
            - [Data Types](transact-data-types.md)
            - [Data Manipulation Language](transact-dmls.md)
            - [General Statements](transact-general-statements.md)
            - [SELECT](transact-select.md)
            - [SYSTEM TABLES](transact-system-tables.md)
            - ETL And BI Repointing

              - [Power BI Transact and Synapse Repointing](etl-bi-repointing/power-bi-transact-repointing.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](../db2/README.md)
          + [SSIS](../ssis/README.md)
        + [Migration Assistant](../../migration-assistant/README.md)
        + [Data Validation CLI](../../data-validation-cli/index.md)
        + [AI Verification](../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../guides/teradata.md)
      * [Databricks](../../../guides/databricks.md)
      * [SQL Server](../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../guides/redshift.md)
      * [Oracle](../../../guides/oracle.md)
      * [Azure Synapse](../../../guides/azuresynapse.md)
15. [Queries](../../../../guides/overview-queries.md)
16. [Listings](../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../guides/overview-alerts.md)
25. [Security](../../../../guides/overview-secure.md)
26. [Data Governance](../../../../guides/overview-govern.md)
27. [Privacy](../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../guides/overview-cost.md)

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)Data Definition LanguageALTER TABLE

# SnowConvert AI - SQL Server-Azure Synapse - ALTER[¶](#snowconvert-ai-sql-server-azure-synapse-alter "Link to this heading")

Translation reference for all the DDL statements that are preceded by the `ALTER` keyword.

## TABLE[¶](#table "Link to this heading")

### Description[¶](#description "Link to this heading")

Modifies a table definition by altering, adding, or dropping columns and constraints. ALTER TABLE also reassigns and rebuilds partitions, or disables and enables constraints and triggers. (<https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql>)

## CHECK CONSTRAINT[¶](#check-constraint "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

### Description[¶](#id1 "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

When the constraint that was being added in the SQL Server code is not supported at all in Snowflake, SnowConvert AI comments out the Check constraint statement, since it’s no longer valid.

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### SQL Server[¶](#sql-server "Link to this heading")

```
ALTER TABLE
    [Person].[EmailAddress] CHECK CONSTRAINT [FK_EmailAddress_Person_BusinessEntityID]
GO
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
ALTER TABLE IF EXISTS Person.EmailAddress CHECK CONSTRAINT FK_EmailAddress_Person_BusinessEntityID;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

* 1. The invalid CHECK CONSTRAINT is commented out leaving an invalid ALTER TABLE statement.

### Related EWIs[¶](#related-ewis "Link to this heading")

* [SSC-EWI-0035](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035): Check statement not supported.

## ADD[¶](#add "Link to this heading")

### Description[¶](#id2 "Link to this heading")

Note

In SQL Server, the ADD clause permits multiple actions per ADD, whereas Snowflake only allows a sequence of ADD column actions. Consequently, SnowConvert AI divides the ALTER TABLE ADD clause into individual ALTER TABLE statements.

There is a subset of functionalities provided by the ADD keyword, allowing the addition of different elements to the target table. These include:

* Column definition
* Computed column definition
* Table constraint
* Column set definition

## TABLE CONSTRAINT[¶](#table-constraint "Link to this heading")

Applies to

* SQL Server

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id3 "Link to this heading")

Specifies the properties of a PRIMARY KEY, FOREIGN KEY, UNIQUE, or CHECK constraint that is part of a new column definition added to a table by using [ALTER TABLE](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16). (<https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-column-constraint-transact-sql>)

Translation for column constraints is relatively straightforward. There are several parts of the syntax that are not required or not supported in Snowflake.

These parts include:

* `CLUSTERED | NONCLUSTERED`
* `WITH FILLFACTOR = fillfactor`
* `WITH ( index_option [, ...n ] )`
* `ON { partition_scheme_name ( partition\_column\_name ) | filegroup | "default" }`
* `NOT FOR REPLICATION`
* `CHECK [ NOT FOR REPLICATION ]`

#### Syntax in SQL Server[¶](#syntax-in-sql-server "Link to this heading")

```
 [ CONSTRAINT constraint_name ]   
{   
    { PRIMARY KEY | UNIQUE }   
        [ CLUSTERED | NONCLUSTERED ]   
        (column [ ASC | DESC ] [ ,...n ] )  
        [ WITH FILLFACTOR = fillfactor   
        [ WITH ( <index_option>[ , ...n ] ) ]  
        [ ON { partition_scheme_name ( partition_column_name ... )  | filegroup | "default" } ]   
    | FOREIGN KEY   
        ( column [ ,...n ] )  
        REFERENCES referenced_table_name [ ( ref_column [ ,...n ] ) ]   
        [ ON DELETE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]   
        [ ON UPDATE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]   
        [ NOT FOR REPLICATION ]   
    | CONNECTION
        ( { node_table TO node_table } 
          [ , {node_table TO node_table }]
          [ , ...n ]
        )
        [ ON DELETE { NO ACTION | CASCADE } ]
    | DEFAULT constant_expression FOR column [ WITH VALUES ]   
    | CHECK [ NOT FOR REPLICATION ] ( logical_expression )  
}
```

Copy

#### Syntax in [**Snowflake**](https://docs.snowflake.com/en/sql-reference/sql/create-table-constraint.html#inline-unique-primary-foreign-key)[¶](#syntax-in-snowflake "Link to this heading")

```
 inlineUniquePK ::=
  [ CONSTRAINT <constraint_name> ]
  { UNIQUE | PRIMARY KEY }
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]

 [ CONSTRAINT <constraint_name> ]
  { UNIQUE | PRIMARY KEY }
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]
```

Copy

### Sample Source Patterns[¶](#id4 "Link to this heading")

#### Multiple ALTER TABLE instances[¶](#multiple-alter-table-instances "Link to this heading")

##### SQL Server[¶](#id5 "Link to this heading")

```
 -- PRIMARY KEY
ALTER TABLE
    [Person]
ADD
    CONSTRAINT [PK_EmailAddress_BusinessEntityID_EmailAddressID] PRIMARY KEY CLUSTERED (
        [BusinessEntityID] ASC,
        [EmailAddressID] ASC
    ) ON [PRIMARY]
GO

-- FOREING KEY TO ANOTHER TABLE
ALTER TABLE
    [Person].[EmailAddress] WITH CHECK
ADD
    CONSTRAINT [FK_EmailAddress_Person_BusinessEntityID] FOREIGN KEY([BusinessEntityID]) REFERENCES [Person].[Person] ([BusinessEntityID]) ON DELETE CASCADE
GO
```

Copy

##### Snowflake[¶](#id6 "Link to this heading")

```
 -- PRIMARY KEY
ALTER TABLE Person
ADD
    CONSTRAINT PK_EmailAddress_BusinessEntityID_EmailAddressID PRIMARY KEY (BusinessEntityID, EmailAddressID);

-- FOREING KEY TO ANOTHER TABLE
ALTER TABLE Person.EmailAddress
!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
WITH CHECK
ADD
    CONSTRAINT FK_EmailAddress_Person_BusinessEntityID FOREIGN KEY(BusinessEntityID) REFERENCES Person.Person (BusinessEntityID) ON DELETE CASCADE ;
```

Copy

#### DEFAULT within constraints[¶](#default-within-constraints "Link to this heading")

##### SQL Server[¶](#id7 "Link to this heading")

```
CREATE TABLE Table1
(
   COL_VARCHAR VARCHAR,
   COL_INT INT,
   COL_DATE DATE
);

ALTER TABLE
    Table1
ADD
    CONSTRAINT [DF_Table1_COL_INT] DEFAULT ((0)) FOR [COL_INT]
GO

ALTER TABLE
    Table1
ADD
    COL_NEWCOLUMN VARCHAR,
    CONSTRAINT [DF_Table1_COL_VARCHAR] DEFAULT ('NOT DEFINED') FOR [COL_VARCHAR]
GO

ALTER TABLE
    Table1
ADD
    CONSTRAINT [DF_Table1_COL_DATE] DEFAULT (getdate()) FOR [COL_DATE]    
GO
```

Copy

##### Snowflake[¶](#id8 "Link to this heading")

```
CREATE OR REPLACE TABLE Table1 (
   COL_VARCHAR VARCHAR DEFAULT ('NOT DEFINED'),
   COL_INT INT DEFAULT ((0)),
   COL_DATE DATE DEFAULT (CURRENT_TIMESTAMP() :: TIMESTAMP)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE Table1
--ADD
--    CONSTRAINT DF_Table1_COL_INT DEFAULT ((0)) FOR COL_INT
                                                          ;

ALTER TABLE Table1
ADD COL_NEWCOLUMN VARCHAR;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE Table1
--ADD
--CONSTRAINT DF_Table1_COL_VARCHAR DEFAULT ('NOT DEFINED') FOR COL_VARCHAR
                                                                        ;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE Table1
--ADD
--    CONSTRAINT DF_Table1_COL_DATE DEFAULT (CURRENT_TIMESTAMP() :: TIMESTAMP) FOR COL_DATE
                                                                                         ;
```

Copy

### Known Issues[¶](#id9 "Link to this heading")

**1. DEFAULT is only supported within** `CREATE TABLE` and `ALTER TABLE ... ADD COLUMN`

SQL Server supports defining a `DEFAULT` property within a constraint, while Snowflake only allows that when adding the column via `CREATE TABLE` or `ALTER TABLE ... ADD COLUMN`. `DEFAULT` properties within the `ADD CONSTRAINT` syntax are not supported and will be translated to ALTER TABLE ALTER COLUMN.

### Related EWIs[¶](#id10 "Link to this heading")

1. [SSC-EWI-0035](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035): Check statement not supported.
2. [SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040): Statement Not Supported.
3. [SSC-FDM-TS0020](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0020): Default constraint was commented out and may have been added to a table definition.

## CHECK[¶](#check "Link to this heading")

Applies to

* SQL Server

### Description[¶](#id11 "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

When CHECK clause is in the ALTER statement, SnowConvert AI will comments out the entire statement, since it is not supported.

### Sample Source Patterns[¶](#id12 "Link to this heading")

#### SQL Server[¶](#id13 "Link to this heading")

```
ALTER TABLE dbo.doc_exd    
ADD CONSTRAINT exd_check CHECK NOT FOR REPLICATION (column_a > 1);
```

Copy

#### Snowflake[¶](#id14 "Link to this heading")

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
ALTER TABLE dbo.doc_exd
ADD CONSTRAINT exd_check CHECK NOT FOR REPLICATION (column_a > 1);
```

Copy

### Known Issues[¶](#id15 "Link to this heading")

**1.** **ALTER TABLE CHECK clause is not supported in Snowflake.**

The entire ALTER TABLE CHECK clause is commented out, since it is not supported in Snowflake.

### Related EWIs[¶](#id16 "Link to this heading")

* [SSC-EWI-0035](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035): Check statement not supported.

## CONNECTION[¶](#connection "Link to this heading")

Applies to

* SQL Server

### Description[¶](#id17 "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

When CONNECTION clause is in the ALTER statement, SnowConvert AI will comment out the entire statement, since it is not supported.

### Sample Source Patterns[¶](#id18 "Link to this heading")

#### SQL Server[¶](#id19 "Link to this heading")

```
ALTER TABLE bought 
ADD COL2 VARCHAR(32), CONSTRAINT EC_BOUGHT1 CONNECTION (Customer TO Product, Supplier TO Product) 
ON DELETE NO ACTION;
```

Copy

#### Snowflake[¶](#id20 "Link to this heading")

```
ALTER TABLE bought
ADD COL2 VARCHAR(32);

!!!RESOLVE EWI!!! /*** SSC-EWI-0109 - ALTER TABLE SYNTAX NOT APPLICABLE IN SNOWFLAKE ***/!!!
ALTER TABLE bought
ADD
CONSTRAINT EC_BOUGHT1 CONNECTION (Customer TO Product, Supplier TO Product)
ON DELETE NO ACTION;
```

Copy

### Known Issues[¶](#id21 "Link to this heading")

**1.** **ALTER TABLE CONNECTION clause is not supported in Snowflake.**

The entire ALTER TABLE CONNECTION clause is commented out, since it is not supported in Snowflake.

### Related EWIs[¶](#id22 "Link to this heading")

* [SSC-EWI-0109](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0109): Alter Table syntax is not applicable in Snowflake.

## DEFAULT[¶](#default "Link to this heading")

Applies to

* SQL Server

### Description[¶](#id23 "Link to this heading")

When DEFAULT clause is in the ALTER statement, SnowConvert AI will comment out the entire statement, since it is not supported.

The only functional scenario happens when the table definition is on the same file, in this way the default is added in the column definition.

### Sample Source Patterns[¶](#id24 "Link to this heading")

#### SQL Server[¶](#id25 "Link to this heading")

```
CREATE TABLE table1
(
  col1 integer not null,
  col2 varchar collate Latin1_General_CS,
  col3 date not null
)

ALTER TABLE table1
ADD CONSTRAINT col1_constraint DEFAULT 50 FOR col1;

ALTER TABLE table1
ADD CONSTRAINT col2_constraint DEFAULT 'hello world' FOR col2;

ALTER TABLE table1
ADD CONSTRAINT col3_constraint DEFAULT getdate() FOR col3;
```

Copy

#### Snowflake[¶](#id26 "Link to this heading")

```
CREATE OR REPLACE TABLE table1 (
  col1 INTEGER not null DEFAULT 50,
  col2 VARCHAR COLLATE 'EN-CS' DEFAULT 'hello world',
  col3 DATE not null DEFAULT CURRENT_TIMESTAMP() :: TIMESTAMP
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE table1
--ADD CONSTRAINT col1_constraint DEFAULT 50 FOR col1
                                                  ;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE table1
--ADD CONSTRAINT col2_constraint DEFAULT 'hello world' FOR col2
                                                             ;

----** SSC-FDM-TS0020 - DEFAULT CONSTRAINT MAY HAVE BEEN ADDED TO TABLE DEFINITION **

--ALTER TABLE table1
--ADD CONSTRAINT col3_constraint DEFAULT CURRENT_TIMESTAMP() :: TIMESTAMP FOR col3
                                                                                ;
```

Copy

### Known Issues[¶](#id27 "Link to this heading")

**1. ALTER TABLE DEFAULT clause is not supported in Snowflake.**

The entire ALTER TABLE DEFAULT clause is commented out, since it is not supported in Snowflake.

### Related EWIs[¶](#id28 "Link to this heading")

1. [SSC-FDM-TS0020](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0020): Default constraint was commented out and may have been added to a table definition.

## FOREIGN KEY[¶](#foreign-key "Link to this heading")

Applies to

* SQL Server

### Description[¶](#id29 "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

Snowflake supports the grammar for Referential Integrity Constraints, and their properties to facilitate the migration from other databases.

#### SQL Server[¶](#id30 "Link to this heading")

```
FOREIGN KEY   
        ( column [ ,...n ] )  
        REFERENCES referenced_table_name [ ( ref_column [ ,...n ] ) ]   
        [ ON DELETE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]   
        [ ON UPDATE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]   
        [ NOT FOR REPLICATION ]
```

Copy

#### Snowflake[¶](#id31 "Link to this heading")

```
  [ FOREIGN KEY ]
  REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
  [ MATCH { FULL | SIMPLE | PARTIAL } ]
  [ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
       [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]
```

Copy

### Sample Source Patterns[¶](#id32 "Link to this heading")

#### SQL Server[¶](#id33 "Link to this heading")

```
ALTER TABLE [Tests].[dbo].[Employee]
ADD CONSTRAINT FK_Department FOREIGN KEY(DepartmentID) REFERENCES Department(DepartmentID) 
ON UPDATE CASCADE
ON DELETE NO ACTION
NOT FOR REPLICATION;
```

Copy

#### Snowflake[¶](#id34 "Link to this heading")

```
ALTER TABLE Tests.dbo.Employee
ADD CONSTRAINT FK_Department FOREIGN KEY(DepartmentID) REFERENCES Department (DepartmentID)
ON UPDATE CASCADE
ON DELETE NO ACTION;
```

Copy

Note

Constraints are not enforced in Snowflake, excepting NOT NULL.

Primary and Foreign Key are only used for documentation purposes more than design constraints.

## ON PARTITION[¶](#on-partition "Link to this heading")

Applies to

* SQL Server

Note

Non-relevant statement.

Warning

Notice that this statement is removed from the migration because it is a non-relevant syntax. It means that it is not required in Snowflake.

### Description[¶](#id35 "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

In Transact SQL Server, the `on partition` statement is used inside `alter` statements and is used to divide the data across the database. Review more information [here](https://learn.microsoft.com/en-us/sql/relational-databases/partitions/partitioned-tables-and-indexes?view=sql-server-ver16).

### Sample Source Patterns[¶](#id36 "Link to this heading")

#### On Partition[¶](#id37 "Link to this heading")

Notice that in this example the `ON PARTITION` has been removed. This is because Snowflake provides an integrated partitioning methodology. Thus, the syntax is not relevant.

##### SQL SERVER[¶](#id38 "Link to this heading")

```
ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE
ON partition_scheme_name (partition_column_name);
```

Copy

##### Snowflake[¶](#id39 "Link to this heading")

```
ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;
```

Copy

## PRIMARY KEY[¶](#primary-key "Link to this heading")

Applies to

* SQL Server

### Description[¶](#id40 "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

SQL Server primary key has many clauses that are not applicable for Snowflake. So, most of the statement will be commented out.

#### Syntax in SQL Server[¶](#id41 "Link to this heading")

```
{ PRIMARY KEY | UNIQUE }   
[ CLUSTERED | NONCLUSTERED ]   
(column [ ASC | DESC ] [ ,...n ] )  
[ WITH FILLFACTOR = fillfactor   
[ WITH ( <index_option>[ , ...n ] ) ]  
[ ON { partition_scheme_name ( partition_column_name ... )  | filegroup | "default" } ]
```

Copy

#### Syntax in Snowflake[¶](#id42 "Link to this heading")

```
[ CONSTRAINT <constraint_name> ]
{ UNIQUE | PRIMARY KEY } ( <col_name> [ , <col_name> , ... ] )
[ [ NOT ] ENFORCED ]
[ [ NOT ] DEFERRABLE ]
[ INITIALLY { DEFERRED | IMMEDIATE } ]
[ ENABLE | DISABLE ]
[ VALIDATE | NOVALIDATE ]
[ RELY | NORELY ]
```

Copy

### Sample Source Patterns[¶](#id43 "Link to this heading")

Warning

Notice that `WITH FILLFACTOR` statement has been removed from the translation because it is not relevant in Snowflake syntax.

#### SQL Server[¶](#id44 "Link to this heading")

```
ALTER TABLE Production.TransactionHistoryArchive
   ADD CONSTRAINT PK_TransactionHistoryArchive_TransactionID PRIMARY KEY 
   CLUSTERED (TransactionID)
   WITH (FILLFACTOR = 75, ONLINE = ON, PAD_INDEX = ON)
   ON "DEFAULTLOCATION";
```

Copy

#### Snowflake[¶](#id45 "Link to this heading")

```
ALTER TABLE Production.TransactionHistoryArchive
   ADD CONSTRAINT PK_TransactionHistoryArchive_TransactionID PRIMARY KEY (TransactionID);
```

Copy

## COLUMN DEFINITION[¶](#column-definition "Link to this heading")

ALTER TABLE ADD column\_name

Applies to

* SQL Server
* Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#id46 "Link to this heading")

Specifies the properties of a column that are added to a table by using [ALTER TABLE](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16).

Adding a [column definition](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-column-definition-transact-sql?view=sql-server-ver16) in Snowflake does have some differences compared to SQL Server.

For instance, several parts of the SQL Server grammar are not required or entirely not supported by Snowflake. These include:

* [FILESTREAM](#unsupported-clauses)
* [ROWGUIDCOL](https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-column-definition-transact-sql?view=sql-server-ver16)
* [ENCRYPTED WITH …](#encrypted-with)
* [SPARSE](#sparse)

Additionally, a couple other parts are partially supported, and require additional work to be implemented in order to properly emulate the original functionality. Specifically, we’re talking about the [`MASKED WITH` property](#masked-with), which will be covered in the [patterns section](#sample-source-patterns) of this page.

#### SQL Server[¶](#id47 "Link to this heading")

```
column_name <data_type>  
[ FILESTREAM ]  
[ COLLATE collation_name ]   
[ NULL | NOT NULL ]  
[
    [ CONSTRAINT constraint_name ] DEFAULT constant_expression [ WITH VALUES ]   
    | IDENTITY [ ( seed , increment ) ] [ NOT FOR REPLICATION ]   
]
[ ROWGUIDCOL ]   
[ SPARSE ]   
[ ENCRYPTED WITH  
  ( COLUMN_ENCRYPTION_KEY = key_name ,  
      ENCRYPTION_TYPE = { DETERMINISTIC | RANDOMIZED } ,   
      ALGORITHM =  'AEAD_AES_256_CBC_HMAC_SHA_256'   
  ) ]  
[ MASKED WITH ( FUNCTION = ' mask_function ') ]  
[ <column_constraint> [ ...n ] ]
```

Copy

#### Snowflake[¶](#id48 "Link to this heading")

```
ADD [ COLUMN ] <col_name> <col_type>
        [ { DEFAULT <expr> | { AUTOINCREMENT | IDENTITY } [ { ( <start_num> , <step_num> ) | START <num> INCREMENT <num> } ] } ]
                            /* AUTOINCREMENT (or IDENTITY) supported only for columns with numeric data types (NUMBER, INT, FLOAT, etc.). */
                            /* Also, if the table is not empty (i.e. rows exist in the table), only DEFAULT can be altered.               */
        [ inlineConstraint ]
        [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col1_name> , cond_col_1 , ... ) ] ]
```

Copy

### Sample Source Patterns[¶](#id49 "Link to this heading")

#### Basic pattern[¶](#basic-pattern "Link to this heading")

This pattern showcases the removal of elements from the original ALTER TABLE.

##### SQL Server[¶](#id50 "Link to this heading")

```
ALTER TABLE table_name
ADD column_name INTEGER;
```

Copy

##### Snowflake[¶](#id51 "Link to this heading")

```
ALTER TABLE IF EXISTS table_name
ADD column_name INTEGER;
```

Copy

#### COLLATE[¶](#collate "Link to this heading")

Collation allows you to specify broader rules when talking about string comparison.

##### SQL Server[¶](#id52 "Link to this heading")

```
ALTER TABLE table_name
ADD COLUMN new_column_name VARCHAR
COLLATE Latin1_General_CI_AS;
```

Copy

Since the collation rule nomenclature varies from SQL Server to Snowflake, it is necessary to make adjustments.

##### Snowflake[¶](#id53 "Link to this heading")

```
ALTER TABLE IF EXISTS table_name
ADD COLUMN new_column_name VARCHAR COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/;
```

Copy

#### MASKED WITH[¶](#masked-with "Link to this heading")

This pattern showcases the translation for MASKED WITH property. CREATE OR REPLACE MASKING POLICY is inserted somewhere before the first usage, and then referenced by a SET MASKING POLICY clause.

The name of the new MASKING POLICY will be the concatenation of the name and arguments of the original MASKED WITH FUNCTION, as seen below:

##### SQL Server[¶](#id54 "Link to this heading")

```
ALTER TABLE table_name
ALTER COLUMN column_name
ADD MASKED WITH ( FUNCTION = ' random(1, 999) ' );
```

Copy

##### Snowflake[¶](#id55 "Link to this heading")

```
--** SSC-FDM-TS0022 - MASKING ROLE MUST BE DEFINED PREVIOUSLY BY THE USER **
CREATE OR REPLACE MASKING POLICY "random_1_999" AS
(val SMALLINT)
RETURNS SMALLINT ->
CASE
WHEN current_role() IN ('YOUR_DEFINED_ROLE_HERE')
THEN val
ELSE UNIFORM(1, 999, RANDOM()) :: SMALLINT
END;

ALTER TABLE IF EXISTS table_name MODIFY COLUMN column_name/*** SSC-FDM-TS0021 - A MASKING POLICY WAS CREATED AS SUBSTITUTE FOR MASKED WITH ***/  SET MASKING POLICY "random_1_999";
```

Copy

#### DEFAULT[¶](#id56 "Link to this heading")

This pattern showcases some of the basic translation scenarios for DEFAULT property.

##### SQL Server[¶](#id57 "Link to this heading")

```
ALTER TABLE table_name
ADD intcol INTEGER DEFAULT 0;

ALTER TABLE table_name
ADD varcharcol VARCHAR(20) DEFAULT '';

ALTER TABLE table_name
ADD datecol DATE DEFAULT CURRENT_TIMESTAMP;
```

Copy

##### Snowflake[¶](#id58 "Link to this heading")

```
ALTER TABLE IF EXISTS table_name
ADD intcol INTEGER DEFAULT 0;

ALTER TABLE IF EXISTS table_name
ADD varcharcol VARCHAR(20) DEFAULT '';

ALTER TABLE IF EXISTS table_name
ADD datecol DATE
                 !!!RESOLVE EWI!!! /*** SSC-EWI-TS0078 - DEFAULT OPTION NOT ALLOWED IN SNOWFLAKE ***/!!!
                 DEFAULT CURRENT_TIMESTAMP;
```

Copy

#### ENCRYPTED WITH[¶](#encrypted-with "Link to this heading")

This pattern showcases the translation for ENCRYPTED WITH property, which is commented out in the output code.

##### SQL Server[¶](#id59 "Link to this heading")

```
ALTER TABLE table_name
ADD encryptedcol VARCHAR(20)
ENCRYPTED WITH  
  ( COLUMN_ENCRYPTION_KEY = key_name ,  
      ENCRYPTION_TYPE = RANDOMIZED ,  
      ALGORITHM =  'AEAD_AES_256_CBC_HMAC_SHA_256'  
  );
```

Copy

##### Snowflake[¶](#id60 "Link to this heading")

```
ALTER TABLE IF EXISTS table_name
ADD encryptedcol VARCHAR(20)
----** SSC-FDM-TS0009 - ENCRYPTED WITH NOT SUPPORTED IN SNOWFLAKE **
--ENCRYPTED WITH
--  ( COLUMN_ENCRYPTION_KEY = key_name ,
--      ENCRYPTION_TYPE = RANDOMIZED ,
--      ALGORITHM =  'AEAD_AES_256_CBC_HMAC_SHA_256'
--  )
   ;
```

Copy

#### NOT NULL[¶](#not-null "Link to this heading")

The SQL Server NOT NULL clause has the same pattern and functionality as the Snowflake NOT NULL clause

##### SQL Server[¶](#id61 "Link to this heading")

```
ALTER TABLE table2 ADD 
column_test INTEGER NOT NULL,
column_test2 INTEGER NULL,
column_test3 INTEGER;
```

Copy

##### Snowflake[¶](#id62 "Link to this heading")

```
ALTER TABLE IF EXISTS table2 ADD column_test INTEGER NOT NULL;

ALTER TABLE IF EXISTS table2 ADD column_test2 INTEGER NULL;

ALTER TABLE IF EXISTS table2 ADD column_test3 INTEGER;
```

Copy

#### IDENTITY[¶](#identity "Link to this heading")

This pattern showcases the translation for IDENTITY. The `NOT FOR REPLICATION` portion is removed in Snowflake.

##### SQL Server[¶](#id63 "Link to this heading")

```
ALTER TABLE table3 ADD 
column_test INTEGER IDENTITY(1, 100) NOT FOR REPLICATION;
```

Copy

##### Snowflake[¶](#id64 "Link to this heading")

```
ALTER TABLE IF EXISTS table3 ADD column_test INTEGER IDENTITY(1, 100) ORDER;
```

Copy

### Unsupported clauses[¶](#unsupported-clauses "Link to this heading")

#### FILESTREAM[¶](#filestream "Link to this heading")

The original behavior of `FILESTREAM` is not replicable in Snowflake, and merits commenting out the entire `ALTER TABLE` statement.

##### SQL Server[¶](#id65 "Link to this heading")

```
ALTER TABLE table2
ADD column1 varbinary(max)
FILESTREAM;
```

Copy

##### Snowflake[¶](#id66 "Link to this heading")

```
ALTER TABLE IF EXISTS table2
ADD column1 VARBINARY
!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'FILESTREAM COLUMN OPTION' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FILESTREAM;
```

Copy

#### SPARSE[¶](#sparse "Link to this heading")

In SQL Server, [SPARSE](https://docs.microsoft.com/en-us/sql/relational-databases/tables/use-sparse-columns) is used to define columns that are optimized for NULL storage. However, when we’re using Snowflake, we are not required to use this clause.

Snowflake performs [optimizations over tables](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions.html#benefits-of-micro-partitioning) automatically, which mitigates the need for manual user-made optimizations.

##### SQL Server[¶](#id67 "Link to this heading")

```
-- ADD COLUMN DEFINITION form
ALTER TABLE table3
ADD column1 int NULL SPARSE;

----------------------------------------
/* It also applies to the other forms */
----------------------------------------

-- CREATE TABLE form
CREATE TABLE table3
(
    column1 INT SPARSE NULL
);

-- ALTER COLUMN form
ALTER TABLE table3
ALTER COLUMN column1 INT NULL SPARSE;
```

Copy

##### Snowflake[¶](#id68 "Link to this heading")

```
-- ADD COLUMN DEFINITION form
ALTER TABLE IF EXISTS table3
ALTER COLUMN column1
                     !!!RESOLVE EWI!!! /*** SSC-EWI-TS0061 - ALTER COLUMN COMMENTED OUT BECAUSE SPARSE COLUMN IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                     INT NULL SPARSE;

----------------------------------------
/* It also applies to the other forms */
----------------------------------------

-- CREATE TABLE form
CREATE OR REPLACE TABLE table3
(
    column1 INT
                !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'SPARSE COLUMN OPTION' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                SPARSE NULL
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;

-- ALTER COLUMN form
ALTER TABLE IF EXISTS table3
ALTER COLUMN column1
                     !!!RESOLVE EWI!!! /*** SSC-EWI-TS0061 - ALTER COLUMN COMMENTED OUT BECAUSE SPARSE COLUMN IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                     INT NULL SPARSE;
```

Copy

#### ROWGUIDCOL[¶](#rowguidcol "Link to this heading")

##### SQL Server[¶](#id69 "Link to this heading")

```
ALTER TABLE table_name
ADD column_name UNIQUEIDENTIFIER 
ROWGUIDCOL;
```

Copy

##### Snowflake[¶](#id70 "Link to this heading")

```
ALTER TABLE IF EXISTS table_name
ADD column_name VARCHAR
!!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'ROWGUIDCOL COLUMN OPTION' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
ROWGUIDCOL;
```

Copy

### Known Issues[¶](#id71 "Link to this heading")

**1. Roles and users have to be previously set up for masking policies**

Snowflake’s Masking Policies can be applied to columns only after the policies were created. This requires the user to create the policies and assign them to roles, and these roles to users, in order to work properly. Masking Policies can behave differently depending on which user is querying.

Warning

SnowConvert AI does not perform this setup automatically.

**2. Masking policies require a Snowflake Enterprise account or higher.**

higher-rankThe Snowflake documentation states that masking policies are available on Entreprise or higher rank accounts.

Note

For further details visit [CREATE MASKING POLICY — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-masking-policy.html#create-masking-policy).

**3. DEFAULT only supports constant values**

SQL Server’s DEFAULT property is partially supported by Snowflake, as long as its associated value is a constant.

**4.** **FILESTREAM clause is not supported in Snowflake.**

The entire FILESTSTREAM clause is commented out, since it is not supported in Snowflake.

**5.** **SPARSE clause is not supported in Snowflake.**

The entire SPARSE clause is commented out, since it is not supported in Snowflake. When it is added within an ALTER COLUMN statement, and it’s the only modification being made to the column, the entire statement is removed since it’s no longer adding anything.

### Related EWIs[¶](#id72 "Link to this heading")

1. [SSC-EWI-0040](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0040): Statement Not Supported.
2. [SSC-EWI-TS0061](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sqlServerEWI.html#ssc-ewi-ts0061): ALTER COLUMN not supported.
3. [SSC-EWI-TS0078](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/sqlServerEWI.html#ssc-ewi-ts0078): Default value not allowed in Snowflake.
4. [SSC-FDM-TS0009](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0009): Encrypted with not supported in Snowflake.
5. [SSC-FDM-TS0021](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0021): A MASKING POLICY was created as a substitute for MASKED WITH.
6. [SSC-FDM-TS0022](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/sqlServerFDM.html#ssc-fdm-ts0022): The user must previously define the masking role.
7. [SSC-PRF-0002](../../general/technical-documentation/issues-and-troubleshooting/performance-review/generalPRF.html#ssc-prf-0002): Case-insensitive columns can decrease the performance of queries.

## COLUMN CONSTRAINT[¶](#column-constraint "Link to this heading")

ALTER TABLE ADD COLUMN … COLUMN CONSTRAINT

Applies to

* SQL Server
* Azure Synapse Analytics

### Description[¶](#id73 "Link to this heading")

Specifies the properties of a PRIMARY KEY, FOREIGN KEY or CHECK that is part of a new [column constraint](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-column-constraint-transact-sql?view=sql-server-ver16) added to a table by using [Alter Table.](https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16)

#### SQL Server[¶](#id74 "Link to this heading")

```
[ CONSTRAINT constraint_name ]   
{   
    [ NULL | NOT NULL ]   
    { PRIMARY KEY | UNIQUE }   
        [ CLUSTERED | NONCLUSTERED ]   
        [ WITH FILLFACTOR = fillfactor ]   
        [ WITH ( index_option [, ...n ] ) ]  
        [ ON { partition_scheme_name (partition_column_name)   
            | filegroup | "default" } ]   
    | [ FOREIGN KEY ]   
        REFERENCES [ schema_name . ] referenced_table_name   
            [ ( ref_column ) ]   
        [ ON DELETE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]   
        [ ON UPDATE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]   
        [ NOT FOR REPLICATION ]   
    | CHECK [ NOT FOR REPLICATION ] ( logical_expression )  
}
```

Copy

#### Snowflake[¶](#id75 "Link to this heading")

```
CREATE TABLE <name> ( <col1_name> <col1_type>    [ NOT NULL ] { inlineUniquePK | inlineFK }
                     [ , <col2_name> <col2_type> [ NOT NULL ] { inlineUniquePK | inlineFK } ]
                     [ , ... ] )

ALTER TABLE <name> ADD COLUMN <col_name> <col_type> [ NOT NULL ] { inlineUniquePK | inlineFK }
```

Copy

Where:

```
inlineUniquePK ::=
  [ CONSTRAINT <constraint_name> ]
  { UNIQUE | PRIMARY KEY }
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]
```

Copy

```
inlineFK :=
  [ CONSTRAINT <constraint_name> ]
  [ FOREIGN KEY ]
  REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
  [ MATCH { FULL | SIMPLE | PARTIAL } ]
  [ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
       [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
  [ [ NOT ] ENFORCED ]
  [ [ NOT ] DEFERRABLE ]
  [ INITIALLY { DEFERRED | IMMEDIATE } ]
  [ ENABLE | DISABLE ]
  [ VALIDATE | NOVALIDATE ]
  [ RELY | NORELY ]
```

Copy

## CHECK[¶](#id76 "Link to this heading")

Applies to

* SQL Server

### Description[¶](#id77 "Link to this heading")

Note

Some parts in the output code are omitted for clarity reasons.

When CHECK clause is in the ALTER statement, SnowConvert AI will comments out the entire statement, since it is not supported.

### Sample Source Patterns[¶](#id78 "Link to this heading")

#### SQL Server[¶](#id79 "Link to this heading")

```
ALTER TABLE table_name
ADD column_name VARCHAR(255) 
CONSTRAINT constraint_name 
CHECK NOT FOR REPLICATION (column_name > 1);
```

Copy

#### Snowflake[¶](#id80 "Link to this heading")

```
ALTER TABLE IF EXISTS table_name
ADD column_name VARCHAR(255)
!!!RESOLVE EWI!!! /*** SSC-EWI-0035 - CHECK STATEMENT NOT SUPPORTED ***/!!!
CONSTRAINT constraint_name
CHECK NOT FOR REPLICATION (column_name > 1);
```

Copy

### Known Issues[¶](#id81 "Link to this heading")

**1.** **ALTER TABLE CHECK clause is not supported in Snowflake.**

The entire ALTER TABLE CHECK clause is commented out, since it is not supported in Snowflake.

### Related EWIs[¶](#id82 "Link to this heading")

* [SSC-EWI-0035](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0035): Check statement not supported.

## FOREIGN KEY[¶](#id83 "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

### Description[¶](#id84 "Link to this heading")

The syntax for the Foreign Key is fully supported by SnowFlake, except for the `[ NOT FOR REPLICATION ]` and the `WITH CHECK` clauses.

#### SQL Server[¶](#id85 "Link to this heading")

Review the following [SQL Server documentation](https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16#syntax-for-memory-optimized-tables) for more information.

```
[ FOREIGN KEY ]  
REFERENCES [ schema_name . ] referenced_table_name  
[ ( ref_column ) ]  
[ ON DELETE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]  
[ ON UPDATE { NO ACTION | CASCADE | SET NULL | SET DEFAULT } ]  
[ NOT FOR REPLICATION ]
```

Copy

#### Snowflake[¶](#id86 "Link to this heading")

```
[ FOREIGN KEY ]
REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
[ MATCH { FULL | SIMPLE | PARTIAL } ]
[ ON [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
     [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
[ [ NOT ] ENFORCED ]
[ [ NOT ] DEFERRABLE ]
[ INITIALLY { DEFERRED | IMMEDIATE } ]
[ ENABLE | DISABLE ]
[ VALIDATE | NOVALIDATE ]
[ RELY | NORELY ]
```

Copy

### Sample Source Patterns[¶](#id87 "Link to this heading")

#### General case[¶](#general-case "Link to this heading")

##### SQL Server[¶](#id88 "Link to this heading")

```
ALTER TABLE dbo.student 
ADD CONSTRAINT Fk_empid FOREIGN KEY(emp_id)
REFERENCES dbo.emp(id);

ALTER TABLE dbo.student 
ADD CONSTRAINT Fk_empid FOREIGN KEY(emp_id)
REFERENCES dbo.emp(id)
NOT FOR REPLICATION;
```

Copy

##### Snowflake[¶](#id89 "Link to this heading")

```
ALTER TABLE dbo.student
ADD CONSTRAINT Fk_empid FOREIGN KEY(emp_id)
REFERENCES dbo.emp (id);

ALTER TABLE dbo.student
ADD CONSTRAINT Fk_empid FOREIGN KEY(emp_id)
REFERENCES dbo.emp (id);
```

Copy

#### WITH CHECK / NO CHECK case[¶](#with-check-no-check-case "Link to this heading")

Notice that Snowflake logic does not support the CHECK clause in the creation of foreign keys. The `WITH CHECK` statement is marked as not supported. Besides, the `WITH NO CHECK` clause is removed because it is the default behavior in Snowflake and the equivalence is the same.

Please, review the following examples to have a better understanding of the translation.

##### SQL Server[¶](#id90 "Link to this heading")

```
ALTER TABLE testTable
WITH CHECK ADD CONSTRAINT testFK1 FOREIGN KEY (table_id)
REFERENCES otherTable (Othertable_id);

ALTER TABLE testTable
WITH NOCHECK ADD CONSTRAINT testFK2 FOREIGN KEY (table_id)
REFERENCES otherTable (Othertable_id);
```

Copy

##### Snowflake[¶](#id91 "Link to this heading")

```
ALTER TABLE testTable
----** SSC-FDM-0014 - CHECK STATEMENT NOT SUPPORTED **
--WITH CHECK
           ADD CONSTRAINT testFK1 FOREIGN KEY (table_id)
REFERENCES otherTable (Othertable_id);


ALTER TABLE testTable
ADD CONSTRAINT testFK2 FOREIGN KEY (table_id)
REFERENCES otherTable (Othertable_id);
```

Copy

### Known Issues[¶](#id92 "Link to this heading")

**1.** **NOT FOR REPLICATION clause.**

Snowflake has a different approach to the replication cases. Please, review the following [documentation](https://docs.snowflake.com/en/user-guide/account-replication-considerations).

**2. WITH CHECK clause.**

Snowflake does not support the `WITH CHECK` statement. Review the following [documentation](https://docs.snowflake.com/en/sql-reference/constraints-overview) for more information.

## PRIMARY KEY / UNIQUE[¶](#primary-key-unique "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

### Description[¶](#id93 "Link to this heading")

All of the optional clauses of the PRIMARY KEY / UNIQUE constraint are removed in Snowflake.

**Syntax in SQL Server**

```
{ PRIMARY KEY | UNIQUE }
    [ CLUSTERED | NONCLUSTERED ]
    [ WITH FILLFACTOR = fillfactor ]
    [ WITH ( index_option [, ...n ] ) ]
    [ ON { partition_scheme_name (partition_column_name)
        | filegroup | "default" } ]
```

Copy

### Sample Source Patterns[¶](#id94 "Link to this heading")

#### SQL Server[¶](#id95 "Link to this heading")

```
ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;

ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name PRIMARY KEY
NONCLUSTERED;

ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE
WITH FILLFACTOR = 80;

ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name PRIMARY KEY
WITH (PAD_INDEX = off);

ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE
ON partition_scheme_name (partition_column_name);
```

Copy

#### Snowflake[¶](#id96 "Link to this heading")

```
ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;


ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name PRIMARY KEY;


ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;


ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name PRIMARY KEY;


ALTER TABLE table_name
ADD column_name INTEGER
CONSTRAINT constraint_name UNIQUE;
```

Copy

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

Terms of Use

The SnowConvert AI tool is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [TABLE](#table)
2. [CHECK CONSTRAINT](#check-constraint)
3. [ADD](#add)
4. [TABLE CONSTRAINT](#table-constraint)
5. [CHECK](#check)
6. [CONNECTION](#connection)
7. [DEFAULT](#default)
8. [FOREIGN KEY](#foreign-key)
9. [ON PARTITION](#on-partition)
10. [PRIMARY KEY](#primary-key)
11. [COLUMN DEFINITION](#column-definition)
12. [COLUMN CONSTRAINT](#column-constraint)
13. [CHECK](#id76)
14. [FOREIGN KEY](#id83)
15. [PRIMARY KEY / UNIQUE](#primary-key-unique)