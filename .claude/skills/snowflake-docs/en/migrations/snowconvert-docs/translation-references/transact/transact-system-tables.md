---
auto_generated: true
description: Translation spec for Transact-SQL System Tables
last_scraped: '2026-01-14T16:54:09.752858+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-system-tables
title: SnowConvert AI - SQL Server-Azure Synapse - System Tables | Snowflake Documentation
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[SQL Server-Azure Synapse](README.md)SYSTEM TABLES

# SnowConvert AI - SQL Server-Azure Synapse - System Tables[¶](#snowconvert-ai-sql-server-azure-synapse-system-tables "Link to this heading")

Translation spec for Transact-SQL System Tables

## System tables[¶](#system-tables "Link to this heading")

| Transact-SQL | Snowflake SQL | Notes |  |
| --- | --- | --- | --- |
| SYS.ALL\_VIEWS | INFORMATION\_SCHEMA.VIEWS |  |  |
| SYS.ALL\_COLUMNS | INFORMATION\_SCHEMA.COLUMNS |  |  |
| SYS.COLUMNS | INFORMATION\_SCHEMA.COLUMNS |  |  |
| SYS.OBJECTS | INFORMATION\_SCHEMA.OBJECT\_PRIVILEGES |  |  |
| SYS.PROCEDURES | INFORMATION\_SCHEMA.PROCEDURES |  |  |
| SYS.SEQUENCES | INFORMATION\_SCHEMA.SEQUENCES |  |  |
| SYS.ALL\_OBJECTS | INFORMATION\_SCHEMA.OBJECT\_PRIVILEGES |  |  |
| ALL\_PARAMETERS | **Not supported** |  |  |
| SYS.ALL\_SQL\_MODULES | **Not supported** |  |  |
| SYS.ALLOCATION\_UNITS | **Not supported** |  |  |
| SYS.ASSEMBLY\_MODULES | **Not supported** |  |  |
| SYS.CHECK\_CONSTRAINTS | **Not supported** |  |  |
| SYS.COLUMN\_STORE\_DICTIONARIES | **Not supported** |  |  |
| SYS.COLUMN\_STORE\_ROW\_GROUPS | **Not supported** |  |  |
| SYS.COLUMN\_STORE\_SEGMENTS | **Not supported** |  |  |
| SYS.COMPUTED\_COLUMNS | **Not supported** |  |  |
| SYS.DEFAULT\_CONSTRAINTS | **Not supported** |  |  |
| SYS.EVENTS | **Not supported** |  |  |
| SYS.EVENT\_NOTIFICATIONS | **Not supported** |  |  |
| SYS.EVENT\_NOTIFICATION\_EVENT\_TYPES | **Not supported** |  |  |
| SYS.EXTENDED\_PROCEDURES | **Not supported** |  |  |
| SYS.EXTERNAL\_LANGUAGE\_FILES | **Not supported** |  |  |
| SYS.EXTERNAL\_LANGUAGES | **Not supported** |  |  |
| SYS.EXTERNAL\_LIBRARIES | **Not supported** |  |  |
| SYS.EXTERNAL\_LIBRARY\_FILES | **Not supported** |  |  |
| SYS.FOREIGN\_KEYS | INFORMATION\_SCHEMA.TABLE\_CONSTRAINTS |  |  |
| SYS.FOREIGN\_KEY\_COLUMNS | **Not supported** |  |  |
| SYS.FUNCTION\_ORDER\_COLUMNS | **Not supported** |  |  |
| SYS.HASH\_INDEXES | **Not supported** |  |  |
| SYS.INDEXES | **Not supported** |  |  |
| SYS.INDEX\_COLUMNS | **Not supported** |  |  |
| SYS.INDEX\_RESUMABLE\_OPERATIONS | **Not supported** |  |  |
| SYS.INTERNAL\_PARTITIONS | **Not supported** |  |  |
| SYS.INTERNAL\_TABLES | **Not supported** |  |  |
| SYS.KEY\_CONSTRAINTS | **Not supported** |  |  |
| SYS.MASKED\_COLUMNS | **Not supported** |  |  |
| SYS.MEMORY\_OPTIMIZED\_TABLES\_INTERNAL\_ATTRIBUTES | **Not supported** |  |  |
| SYS.MODULE\_ASSEMBLY\_USAGES | **Not supported** |  |  |
| SYS.NUMBERED\_PROCEDURES | **Not supported** |  |  |
| SYS.NUMBERED\_PROCEDURE\_PARAMETERS | **Not supported** |  |  |
| SYS.PARAMETERS | **Not supported** |  |  |
| SYS.PARTITIONS | **Not supported** |  |  |
| SYS.PERIODS | **Not supported** |  |  |
| SYS.SERVER\_ASSEMBLY\_MODULES | **Not supported** |  |  |
| SYS.SERVER\_EVENTS | **Not supported** |  |  |
| SYS.SERVER\_EVENTT\_NOTIFICATIONS | **Not supported** |  |  |
| SYS.SERVER\_SQL\_MODULE | **Not supported** |  |  |
| SYS.SERVER\_TRIGGERS | **Not supported** |  |  |
| SYS.\_SERVER\_TRIGGER\_EVENTS | **Not supported** |  |  |
| SYS.SQL\_DEPENDENCIES | **Not supported** |  |  |
| SYS.SQL\_EXPRESSION\_DEPENDENCIES | **Not supported** |  |  |
| SYS.SQL\_MODULES | **Not supported** |  |  |
| SYS.STATS | **Not supported** |  |  |
| SYS.STATS\_COLUMNS | **Not supported** |  |  |
| SYS.SYNONYMS | **Not supported** |  |  |
| SYS.SYSTEM\_COLUMNS | **Not supported** |  |  |
| SYS.SYSTEM\_OBJECTS | **Not supported** |  |  |
| SYS.SYSTEM\_PARAMETERS | **Not supported** |  |  |
| SYS.SYSTEM\_SQL\_MODULES” | **Not supported** |  |  |

## SYS.FOREIGN\_KEYS[¶](#sys-foreign-keys "Link to this heading")

Applies to

* SQL Server
* Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description[¶](#description "Link to this heading")

Contains a row per object that is a FOREIGN KEY constraint ([SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16)).

The columns for **FOREIGN KEY** (sys.foreign\_keys) are the following:

| Column name | Data type | Description | Has equivalent column in Snowflake |
| --- | --- | --- | --- |
|  | - | For a list of columns that this view inherits, see [sys.objects (Transact-SQL).](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-objects-transact-sql?view=sql-server-ver16) | Partial |
| referenced\_object\_id | int | ID of the referenced object. | No |
| key\_index\_id | int | ID of the key index within the referenced object. | No |
| is\_disabled | bit | FOREIGN KEY constraint is disabled. | No |
| is\_not\_for\_replication | bit | FOREIGN KEY constraint was created by using the NOT FOR REPLICATION option. | No |
| is\_not\_trusted | bit | FOREIGN KEY constraint has not been verified by the system. | No |
| delete\_referential\_action | tinyint | The referential action that was declared for this FOREIGN KEY when a delete happens. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16). | No |
| delete\_referential\_action\_desc | nvarchar(60) | Description of the referential action that was declared for this FOREIGN KEY when a delete occurs. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16). | No |
| update\_referential\_action | tinyint | The referential action that was declared for this FOREIGN KEY when an update happens. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16). | No |
| update\_referential\_action\_desc | nvarchar(60) | Description of the referential action that was declared for this FOREIGN KEY when an update happens. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16). | No |
| is\_system\_named | bit | 1 = Name was generated by the system.  0 = Name was supplied by the user. | No |

The inherited columns from **sys.objects** are the following:

For more information, review the [sys.objects documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-objects-transact-sql?view=sql-server-ver16).

| Column name | Data type | Description | Has equivalent column in Snowflake |
| --- | --- | --- | --- |
| name | sysname | Object name. | Yes |
| object\_id | int | Object identification number. Is unique within a database. | No |
| principal\_id | int | ID of the individual owner, if different from the schema owner. | No |
| schema\_id | int | ID of the schema that the object is contained in. | No |
| parent\_object\_id | int | ID of the object to which this object belongs. | No |
| type | char(2) | Object type | Yes |
| type\_desc | nvarchar(60) | Description of the object type | Yes |
| create\_date | datetime | Date the object was created. | Yes |
| modify\_date | datetime | Date the object was last modified by using an ALTER statement. | Yes |
| is\_ms\_shipped | bit | Object is created by an internal SQL Server component. | No |
| is\_published | bit | Object is created by an internal SQL Server component. | No |
| is\_schema\_published | bit | Only the schema of the object is published. | No |

Warning

Notice that, in this case, for the sys.foreign\_keys, there is no equivalence in Snowflake. But, the equivalence is made under the columns inherited from sys.objects.

#### Applicable column equivalence[¶](#applicable-column-equivalence "Link to this heading")

| SQLServer | Snowflake | Limitations | Applicable |
| --- | --- | --- | --- |
| name | CONSTRAINT\_NAME | Names auto-generated by the database may be reviewed to the target Snowflake auto-generated name, | Yes |
| type | CONSTRAINT\_TYPE | The type column has a variety of options. But, in this case, the support is only for the letter ‘F’ which represents the foreign keys. | No. Because of the extra validation to determine the foreign keys from all table constraints, it is not applicable. |
| type\_desc | CONSTRAINT\_TYPE | No limitions found. | No. Because of the extra validation to determine the foreign keys from all table constraints, it is not applicable. |
| create\_date | CREATED | Data type differences. | Yes |
| modify\_date | LAST\_ALTERED | Data type differences. | Yes |
| parent\_object\_id | CONSTRAINT\_CATALOG, CONSTRAINT\_SCHEMA, TABLE\_NAME | Columns are generated only for the cases that use the OBJECT\_ID() function and, the name has a valid pattern. | Yes |

##### Syntax in SQL Server[¶](#syntax-in-sql-server "Link to this heading")

```
SELECT ('column_name' | * )
FROM sys.foreign_keys;
```

Copy

##### Syntax in Snowflake[¶](#syntax-in-snowflake "Link to this heading")

```
SELECT ('column_name' | * )
FROM information_schema.table_constraints 
WHERE CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

Note

Since the equivalence for the system foreign keys is the catalog view in Snowflake for in ormation\_schema.table\_constraints, it is necessary to define the type of the constraint in an additional ‘WHERE’ clause to identify foreign key constraints from other constraints.

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

To accomplish correctly the following samples, it is required to run the following statements:

#### SQL Server[¶](#sql-server "Link to this heading")

```
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


INSERT INTO Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);
```

Copy

##### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

CREATE OR REPLACE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
       CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID)
   )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

INSERT INTO Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);
```

Copy

#### 1. Simple Select Case[¶](#simple-select-case "Link to this heading")

##### SQL Server[¶](#id1 "Link to this heading")

```
SELECT *
FROM sys.foreign_keys;
```

Copy

##### Result[¶](#result "Link to this heading")

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 1 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

##### Snowflake[¶](#id2 "Link to this heading")

```
SELECT *
FROM
INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id3 "Link to this heading")

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBTEST | PUBLIC | FK\_Name\_Test | DATETEST | PUBLIC | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

Warning

Results differ due to the differences in column objects and missing equivalence. The result may be checked.

#### 2. Name Column Case[¶](#name-column-case "Link to this heading")

##### SQL Server[¶](#id4 "Link to this heading")

```
SELECT * FROM sys.foreign_keys WHERE name = 'FK_Name_Test';
```

Copy

##### Result[¶](#id5 "Link to this heading")

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 1 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

##### Snowflake[¶](#id6 "Link to this heading")

```
SELECT * FROM
INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
CONSTRAINT_NAME = 'FK_NAME_TEST'
AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id7 "Link to this heading")

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBTEST | PUBLIC | FK\_Name\_Test | DATETEST | PUBLIC | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

Warning

This translation may require verification if the constraint name is auto-generated by the database and used in the query. For more information review the [Know Issues](#known-issues) section.

#### 3. Parent Object ID Case[¶](#parent-object-id-case "Link to this heading")

In this example, a database and schema were created to exemplify the processing of the names to create different and equivalent columns.

##### SQL Server[¶](#id8 "Link to this heading")

```
use database_name_test
create schema schema_name_test

CREATE TABLE schema_name_test.Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
);

CREATE TABLE schema_name_test.Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES schema_name_test.Customers(CustomerID)
);

INSERT INTO schema_name_test.Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO schema_name_test.Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);

SELECT * FROM sys.foreign_keys WHERE name = 'FK_Name_Test' AND parent_object_id = OBJECT_ID(N'database_name_test.schema_name_test.Orders')
```

Copy

##### Result[¶](#id9 "Link to this heading")

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 1 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

##### Snowflake[¶](#id10 "Link to this heading")

```
USE DATABASE database_name_test;

CREATE SCHEMA IF NOT EXISTS schema_name_test
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

CREATE OR REPLACE TABLE schema_name_test.Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

CREATE OR REPLACE TABLE schema_name_test.Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
       CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES schema_name_test.Customers (CustomerID)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO schema_name_test.Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO schema_name_test.Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);

SELECT * FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CONSTRAINT_NAME = 'FK_NAME_TEST'
    AND CONSTRAINT_CATALOG = 'DATABASE_NAME_TEST'
    AND CONSTRAINT_SCHEMA = 'SCHEMA_NAME_TEST'
    AND TABLE_NAME = 'ORDERS'
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id11 "Link to this heading")

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DATABASE\_NAME\_TEST | SCHEMA\_NAME\_TEST | FK\_Name\_Test | DATABASE\_NAME\_TEST | SCHEMA\_NAME\_TEST | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

Warning

If the name coming inside the OBJECT\_ID() function does not have a valid pattern, it will not be converted due to name processing limitations on special characters.

Warning

Review the database that is being used in Snowflake.

#### 4. Type Column Case[¶](#type-column-case "Link to this heading")

The ‘F’ in SQL Server means ‘Foreign Key’ and it is removed due to the validation at the ending to specify the foreign key from all the table constraints.

##### SQL Server[¶](#id12 "Link to this heading")

```
 SELECT * FROM sys.foreign_keys WHERE type = 'F';
```

Copy

##### Result[¶](#id13 "Link to this heading")

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 3 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

##### Snowflake[¶](#id14 "Link to this heading")

```
 SELECT * FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    type = 'F' AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id15 "Link to this heading")

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBTEST | PUBLIC | FK\_Name\_Test | DATETEST | PUBLIC | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

#### 5. Type Desc Column Case[¶](#type-desc-column-case "Link to this heading")

The ‘type\_desc’ column is removed due to the validation at the ending to specify the foreign key from all the table constraints.

##### SQL Server[¶](#id16 "Link to this heading")

```
SELECT
    * 
FROM
    sys.foreign_keys 
WHERE 
    type_desc = 'FOREIGN_KEY_CONSTRAINT';
```

Copy

##### Result[¶](#id17 "Link to this heading")

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 3 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

##### Snowflake[¶](#id18 "Link to this heading")

```
SELECT
    *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    type_desc = 'FOREIGN_KEY_CONSTRAINT' AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id19 "Link to this heading")

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBTEST | PUBLIC | FK\_Name\_Test | DATETEST | PUBLIC | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

#### 6. Modify Date Column Simple Case[¶](#modify-date-column-simple-case "Link to this heading")

##### SQL Server[¶](#id20 "Link to this heading")

```
SELECT *
FROM sys.foreign_keys
WHERE modify_date = CURRENT_TIMESTAMP;
```

Copy

##### Result[¶](#id21 "Link to this heading")

```
The query produced no results.
```

Copy

##### Snowflake[¶](#id22 "Link to this heading")

```
SELECT *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    LAST_ALTERED = CURRENT_TIMESTAMP()
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id23 "Link to this heading")

```
The query produced no results.
```

Copy

#### 7. Modify Date Column with DATEDIFF() Case[¶](#modify-date-column-with-datediff-case "Link to this heading")

The following example shows a more complex scenario where the columns from sys.foreign\_keys (inherited from sys.objects) are inside a function DATEDIFF. In this case, the argument corresponding to the applicable equivalence is changed to the corresponding column from the information.schema in Snowflake.

##### SQL Server[¶](#id24 "Link to this heading")

```
SELECT *
FROM sys.foreign_keys
WHERE DATEDIFF(DAY, modify_date, GETDATE()) <= 30;
```

Copy

##### Result[¶](#id25 "Link to this heading")

```
The foreign keys altered in the last 30 days.
```

Copy

##### Snowflake[¶](#id26 "Link to this heading")

```
SELECT *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    DATEDIFF(DAY, LAST_ALTERED, CURRENT_TIMESTAMP() :: TIMESTAMP) <= 30
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id27 "Link to this heading")

```
The foreign keys altered in the last 30 days.
```

Copy

#### 8. Create Date Column Case[¶](#create-date-column-case "Link to this heading")

##### SQL Server[¶](#id28 "Link to this heading")

```
SELECT *
FROM sys.foreign_keys
WHERE create_date = '2023-09-12 14:36:38.060';
```

Copy

##### Result[¶](#id29 "Link to this heading")

```
The foreign keys that were created on the specified date and time.
```

Copy

##### Snowflake[¶](#id30 "Link to this heading")

```
SELECT *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CREATED = '2023-09-12 14:36:38.060'
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id31 "Link to this heading")

```
The foreign keys that were created on the specified date and time.
```

Copy

Warning

The result may change if the creation date is specific due to the time on which the queries were executed. It is possible to execute a specified query at one time on the origin database and then execute the objects at another time in the new Snowflake queries.

#### 9. Selected Columns Single Name Case[¶](#selected-columns-single-name-case "Link to this heading")

##### SQL Server[¶](#id32 "Link to this heading")

```
SELECT name
FROM sys.foreign_keys;
```

Copy

##### Result[¶](#id33 "Link to this heading")

| name |
| --- |
| FK\_Name\_Test |

##### Snowflake[¶](#id34 "Link to this heading")

```
SELECT
    CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id35 "Link to this heading")

| CONSTRAINT\_NAME |
| --- |
| FK\_Name\_Test |

#### 10. Selected Columns Qualified Name Case[¶](#selected-columns-qualified-name-case "Link to this heading")

##### SQL Server[¶](#id36 "Link to this heading")

```
SELECT
    fk.name
FROM sys.foreign_keys AS fk;
```

Copy

##### Result[¶](#id37 "Link to this heading")

| name |
| --- |
| FK\_Name\_Test |

##### Snowflake[¶](#id38 "Link to this heading")

```
SELECT
    fk.CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS fk
WHERE
    CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### Result[¶](#id39 "Link to this heading")

| CONSTRAINT\_NAME |
| --- |
| FK\_Name\_Test |

### Known Issues[¶](#known-issues "Link to this heading")

#### 1. The ‘name’ column may not show a correct output if the constraint does not have a user-created name[¶](#the-name-column-may-not-show-a-correct-output-if-the-constraint-does-not-have-a-user-created-name "Link to this heading")

If the referenced name is one auto-generated from the database, it would be probable to review it and use the wanted value.

##### 2. When selecting columns, there is a limitation that depends on the applicable columns that are equivalent in Snowflake[¶](#when-selecting-columns-there-is-a-limitation-that-depends-on-the-applicable-columns-that-are-equivalent-in-snowflake "Link to this heading")

Since the columns from sys.foreign\_keys are not completely equivalent in Snowflake, some results may change due to the limitations on the equivalence.

##### 3. The OBJECT\_ID() function may have a valid pattern to be processed or the database, schema or table could not be extracted[¶](#the-object-id-function-may-have-a-valid-pattern-to-be-processed-or-the-database-schema-or-table-could-not-be-extracted "Link to this heading")

Based on the name that receives the OBJECT\_ID() function, the processing of this name will be limited and dependent on formatting.

##### 4. Name Column With OBJECT\_NAME() Function Case[¶](#name-column-with-object-name-function-case "Link to this heading")

Since the OBJECT\_NAME() function is not supported yet, the transformations related to this function are not supported.

##### SQL Server[¶](#id40 "Link to this heading")

```
SELECT name AS ForeignKeyName,
    OBJECT_NAME(parent_object_id) AS ReferencingTable,
    OBJECT_NAME(referenced_object_id) AS ReferencedTable
FROM sys.foreign_keys;
```

Copy

##### Snowflake[¶](#id41 "Link to this heading")

```
SELECT
    name AS ForeignKeyName,
    OBJECT_NAME(parent_object_id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'OBJECT_NAME' NODE ***/!!! AS ReferencingTable,
    OBJECT_NAME(referenced_object_id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'OBJECT_NAME' NODE ***/!!! AS ReferencedTable
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Copy

##### 5. SCHEMA\_NAME() and TYPE\_NAME() functions are also not supported yet.[¶](#schema-name-and-type-name-functions-are-also-not-supported-yet "Link to this heading")

##### 6. Different Join statement types may be not supported if the system table is not supported. Review the supported system tables.[¶](#different-join-statement-types-may-be-not-supported-if-the-system-table-is-not-supported-review-the-supported-system-tables "Link to this heading")

##### 7. Cases with JOIN statements are not supported.[¶](#cases-with-join-statements-are-not-supported "Link to this heading")

##### 8. Names with alias AS are not supported.[¶](#names-with-alias-as-are-not-supported "Link to this heading")

### Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-EWI-0073](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0073): Pending Functional Equivalence Review.

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

1. [System tables](#system-tables)
2. [SYS.FOREIGN\_KEYS](#sys-foreign-keys)