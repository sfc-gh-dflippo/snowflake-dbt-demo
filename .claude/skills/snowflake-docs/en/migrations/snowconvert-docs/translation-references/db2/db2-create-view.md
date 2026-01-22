---
auto_generated: true
description: The CREATE VIEW statement defines a view on one or more tables, views
  or nicknames.
last_scraped: '2026-01-14T16:53:07.516913+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-create-view
title: SnowConvert AI - IBM DB2 - CREATE VIEW | Snowflake Documentation
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
          + [SQL Server-Azure Synapse](../transact/README.md)
          + [Sybase IQ](../sybase/README.md)
          + [Hive-Spark-Databricks SQL](../hive/README.md)
          + [Redshift](../redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../postgres/README.md)
          + [BigQuery](../bigquery/README.md)
          + [Vertica](../vertica/README.md)
          + [IBM DB2](README.md)

            - [CONTINUE HANDLER](db2-continue-handler.md)
            - [EXIT HANDLER](db2-exit-handler.md)
            - [CREATE TABLE](db2-create-table.md)
            - [CREATE VIEW](db2-create-view.md)
            - [CREATE PROCEDURE](db2-create-procedure.md)
            - [CREATE FUNCTION](db2-create-function.md)
            - [Data Types](db2-data-types.md)
            - [SELECT](db2-select-statement.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[IBM DB2](README.md)CREATE VIEW

# SnowConvert AI - IBM DB2 - CREATE VIEW[¶](#snowconvert-ai-ibm-db2-create-view "Link to this heading")

## Description[¶](#description "Link to this heading")

> The CREATE VIEW statement defines a view on one or more tables, views or nicknames.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-view) to navigate to the IBM DB2 documentation page for this syntax.

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

![image](../../../../_images/create_view_overview.png)

Navigate to the following pages to get more details about the translation spec for the subsections of the CREATE VIEW grammar.

## Examples of Supported Create Views[¶](#examples-of-supported-create-views "Link to this heading")

In order to test a CREATE VIEW, we need a Table with some values. Let’s look at the following code for a table with some inserts.

```
 CREATE TABLE PUBLIC.TestTable
(
	ID INT,
	NAME VARCHAR(10)
);

Insert into TestTable Values(1,'MARCO');
Insert into TestTable Values(2,'ESTEBAN');
Insert into TestTable Values(3,'JEFF');
Insert into TestTable Values(4,'OLIVER');
```

Copy

Now that we have a Table with some data, we can do a couple of examples about a Create View.

### IBM DB2[¶](#ibm-db2 "Link to this heading")

```
CREATE VIEW ViewTest1 AS 
SELECT *  
FROM TestTable
WHERE ID > 2;
```

Copy

### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE VIEW ViewTest1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/03/2025",  "domain": "no-domain-provided" }}'
AS SELECT *  FROM
 TestTable
WHERE ID > 2;
```

Copy

## OF type-name[¶](#of-type-name "Link to this heading")

### Description[¶](#id1 "Link to this heading")

> Specifies that the columns of the view are based on the attributes of the structured type identified by type-name.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-view#sdx-synid_type-name) to navigate to the IBM DB2 documentation page for this syntax.

CREATE VIEW OF type-name is not supported in Snowflake.

### Grammar Syntax

![image](../../../../_images/create_view_of_type_syntax_1.png)

![image](../../../../_images/create_view_of_type_syntax_2.png)

### Sample Source Patterns

#### IBM DB2

```
CREATE VIEW ViewTest2
OF Rootview MODE DB2SQL(REF IS oidColumn USER GENERATED)
AS SELECT * FROM TestTable;
```

Copy

##### Snowflake

```
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0015 - CREATE VIEW OF TYPE IS NOT SUPPORTED ***/!!!
 CREATE VIEW ViewTest2
OF Rootview MODE DB2SQL(REF IS oidColumn USER GENERATED)
AS SELECT * FROM TestTable;
```

Copy

### Related EWIs

1. [SSC-EWI-DB0015](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI): CREATE VIEW OF TYPE IS NOT SUPPORTED

## WITH CHECK OPTION

### Description

> Specifies the constraint that every row that is inserted or updated through the view must conform to the definition of the view. A row that does not conform to the definition of the view is a row that does not satisfy the search conditions of the view.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-view#sdx-synid_cascaded) to navigate to the IBM DB2 documentation page for this syntax.

WITH CHECK OPTION is not supported in Snowflake.

### Grammar Syntax[¶](#id6 "Link to this heading")

![image](../../../../_images/create_view_check_option_syntax.png)

### Sample Source Patterns[¶](#id7 "Link to this heading")

#### IBM DB2[¶](#id8 "Link to this heading")

```
CREATE VIEW ViewTest3 AS 
Select * from TestTable 
WITH CASCADED CHECK OPTION;
```

Copy

##### Snowflake[¶](#id9 "Link to this heading")

```
CREATE VIEW ViewTest3
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/03/2025",  "domain": "no-domain-provided" }}'
AS
Select * from
 TestTable;
```

Copy

## WITH ROW MOVEMENT[¶](#with-row-movement "Link to this heading")

### Description[¶](#id10 "Link to this heading")

> Specifies the action to take for an updatable UNION ALL view when a row is updated in a way that violates a check constraint on the underlying table.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-view#sdx-synid_with_no_row_movement) to navigate to the IBM DB2 documentation page for this syntax.

WITH ROW MOVEMENT is not supported in Snowflake.

### Grammar Syntax

![image](../../../../_images/create_view_row_movement_syntax.png)

### Sample Source Patterns

#### IBM DB2

```
CREATE VIEW ViewTest4 
AS Select * 
from TestTableId1 
WITH ROW MOVEMENT;
```

Copy

##### Snowflake

```
CREATE VIEW ViewTest4
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/03/2025",  "domain": "no-domain-provided" }}'
AS Select *
from
 TestTableId1
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0005 - MANIPULATION OF DATA IN VIEWS IS NOT SUPPORTED. ***/!!!
WITH ROW MOVEMENT;
```

Copy

### Related EWIs

1. [SSC-EWI-DB0005](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/db2EWI.html#ssc-ewi-db0005): MANIPULATION OF DATA IN VIEWS IS NOT SUPPORTED

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

1. [Description](#description)
2. [Grammar Syntax](#grammar-syntax)
3. [Examples of Supported Create Views](#examples-of-supported-create-views)
4. [OF type-name](#of-type-name)
5. [WITH CHECK OPTION](#)
6. [WITH ROW MOVEMENT](#with-row-movement)