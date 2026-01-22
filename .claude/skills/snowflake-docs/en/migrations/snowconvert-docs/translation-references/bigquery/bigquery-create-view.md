---
auto_generated: true
description: Creates a new view. (BigQuery SQL Language Reference Create view statement)
last_scraped: '2026-01-14T16:53:03.171604+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/bigquery/bigquery-create-view
title: SnowConvert AI - BigQuery - CREATE VIEW | Snowflake Documentation
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
          + [BigQuery](README.md)

            - [Built-in Functions](bigquery-functions.md)
            - [Data Types](bigquery-data-types.md)
            - [CREATE TABLE](bigquery-create-table.md)
            - [CREATE VIEW](bigquery-create-view.md)
            - [Identifier differences between BigQuery and Snowflake](bigquery-identifiers.md)
            - [Operators](bigquery-operators.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[BigQuery](README.md)CREATE VIEW

# SnowConvert AI - BigQuery - CREATE VIEW[¶](#snowconvert-ai-bigquery-create-view "Link to this heading")

## Description[¶](#description "Link to this heading")

Creates a new view. ([BigQuery SQL Language Reference Create view statement](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=en#create_view_statement))

Success

This syntax is fully supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

```
CREATE [ OR REPLACE ] VIEW [ IF NOT EXISTS ] view_name
[(view_column_name_list)]
[OPTIONS(view_option_list)]
AS query_expression

view_column_name_list :=
  view_column[, ...]

view_column :=
  column_name [OPTIONS(view_column_option_list)]
```

Copy

### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

#### BigQuery[¶](#bigquery "Link to this heading")

```
CREATE VIEW myuser
AS 
SELECT lastname FROM users;

CREATE OR REPLACE VIEW myuser2
AS 
SELECT lastname FROM users2;

CREATE VIEW IF NOT EXISTS myuser2
AS 
SELECT lastname FROM users2;
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE VIEW myuser
AS
SELECT lastname FROM
users;

CREATE OR REPLACE VIEW myuser2
AS
SELECT lastname FROM
users2;

CREATE VIEW myuser3
AS
SELECT lastname FROM
users3;
```

Copy

### Known Issues[¶](#known-issues "Link to this heading")

There are no known Issues.

### Related EWIs[¶](#related-ewis "Link to this heading")

There are no related EWIs.

## View column name list[¶](#view-column-name-list "Link to this heading")

### Description[¶](#id1 "Link to this heading")

The view’s column name list is optional. The names must be unique but do not have to be the same as the column names of the underlying SQL query. ([BigQuery SQL Language Reference View column name list](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=en#view_column_name_list))

Success

This syntax is fully supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

### Grammar Syntax[¶](#id2 "Link to this heading")

```
view_column_name_list :=
  view_column [OPTIONS(view_column_option_list)] [, ...]

view_column_option_list :=
  DESCRIPTION = value
```

Copy

### Sample Source Patterns[¶](#id3 "Link to this heading")

#### BigQuery[¶](#id4 "Link to this heading")

```
CREATE VIEW `myproject.mydataset.newview` (
  column_1_new_name OPTIONS (DESCRIPTION='Description of the column 1 contents'),
  column_2_new_name OPTIONS (DESCRIPTION='Description of the column 2 contents'),
  column_3_new_name OPTIONS (DESCRIPTION='Description of the column 3 contents')
)
AS SELECT column_1, column_2, column_3 FROM `myproject.mydataset.mytable`
```

Copy

#### Snowflake[¶](#id5 "Link to this heading")

```
 CREATE VIEW myproject.mydataset.newview
(
  column_1_new_name COMMENT 'Description of the column 1 contents',
  column_2_new_name COMMENT 'Description of the column 2 contents',
  column_3_new_name COMMENT 'Description of the column 3 contents'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "03/25/2025",  "domain": "test" }}'
AS SELECT column_1, column_2, column_3 FROM
  myproject.mydataset.mytable
```

Copy

### Known Issues[¶](#id6 "Link to this heading")

There are no known Issues.

### Related EWIs[¶](#id7 "Link to this heading")

There are no related EWIs.

## View Options[¶](#view-options "Link to this heading")

### Description[¶](#id8 "Link to this heading")

> The option list allows you to set view options such as a label and an expiration time. You can include multiple options using a comma-separated list. ([BigQuery SQL Language Reference View Options](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=en#view_option_list))

Warning

This syntax is partially supported in [Snowflake](https://docs.snowflake.com/en/sql-reference/sql/create-view).

### Grammar Syntax[¶](#id9 "Link to this heading")

```
OPTIONS(view_option_list [,...])

view_option_list :=
  NAME = value
```

Copy

| NAME | Value | Supported |
| --- | --- | --- |
| expiration\_timestamp | TIMESTAMP | false |
| friendly\_name | STRING | true |
| description | STRING | true |
| labels | ARRAY<STRUCT<STRING, STRING>> | true |
| privacy\_policy | JSON-formatted STRING | false |

### Sample Source Patterns[¶](#id10 "Link to this heading")

#### Description & Friendly\_name:[¶](#description-friendly-name "Link to this heading")

The description and friendly\_name options are include into the Comment Clause generated by SnowConvert AI .

##### BigQuery[¶](#id11 "Link to this heading")

```
CREATE VIEW my_view
OPTIONS (
  description="This is a view description",
  friendly_name="my_friendly_view") AS
SELECT column1, column2
FROM my_table;
```

Copy

##### Snowflake[¶](#id12 "Link to this heading")

```
CREATE VIEW my_view
COMMENT = '{ "description": "This is a view description", "friendly_name": "my_friendly_view", "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "03/25/2025",  "domain": "test" }}'
AS
SELECT column1, column2
FROM
 my_table;
```

Copy

#### Labels:[¶](#labels "Link to this heading")

In BigQuery the labels associated with a view can be used to organize and group tables in the database administrative environment, in Snowflake the Tags can be used for the same functionality. But to ensure that the tag exists, SnowConvert AI will add the corresponding CREATE TAG before the CREATE VIEW if it contains labels. It is important to know that the `CREATE TAG` feature requires Enterprise Edition or higher

##### BigQuery[¶](#id13 "Link to this heading")

```
CREATE VIEW my_view 
OPTIONS(
    labels=[("label1", "value1"), ("label2", "value2")]
)
AS
SELECT column1, column2
FROM table1;
```

Copy

##### Snowflake[¶](#id14 "Link to this heading")

```
CREATE TAG IF NOT EXISTS "label1";
CREATE TAG IF NOT EXISTS "label2";

CREATE VIEW my_view
WITH TAG( "label1" = "value1","label2" = "value2" )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "03/26/2025",  "domain": "test" }}'
AS
SELECT column1, column2
FROM
  table1;
```

Copy

#### Unsupported Options:[¶](#unsupported-options "Link to this heading")

When an option clause includes elements not supported by Snowflake, An EWI will be added.

##### BigQuery[¶](#id15 "Link to this heading")

```
CREATE VIEW my_view
OPTIONS (
  expiration_timestamp=TIMESTAMP "2026-01-01 00:00:00 UTC",
  privacy_policy='{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_columns": "ID"}}'
) AS
SELECT column1, column2
FROM my_table;
```

Copy

##### Snowflake[¶](#id16 "Link to this heading")

```
CREATE VIEW my_view10
!!!RESOLVE EWI!!! /*** SSC-EWI-BQ0001 - SNOWFLAKE DOES NOT SUPPORT THE OPTIONS: EXPIRATION_TIMESTAMP, PRIVACY_POLICY ***/!!!
OPTIONS(
  expiration_timestamp=TIMESTAMP "2026-01-01 00:00:00 UTC",
  privacy_policy='{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_columns": "ID"}}'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "bigquery",  "convertedOn": "03/26/2025",  "domain": "test" }}'
AS
SELECT column1, column2
FROM
  my_table;
```

Copy

#### Known Issues[¶](#id17 "Link to this heading")

* The label-to-tag transformation could lead to errors if the Snowflake account is not Enterprise Edition or higher.

#### Related EWIs[¶](#id18 "Link to this heading")

1. [SSC-EWI-BQ0001](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/bigqueryEWI.html#ssc-ewi-bq0001): The OPTIONS clause within View is not supported in Snowflake.

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
3. [View column name list](#view-column-name-list)
4. [View Options](#view-options)