---
auto_generated: true
description: SQL statements are tagged to monitor usage and consumption.
last_scraped: '2026-01-14T16:51:51.334087+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/translation-reference/sit-tagging/sql-statements
title: 'Snowpark Migration Accelerator:  SQL statements | Snowflake Documentation'
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

      * [SnowConvert AI](../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../README.md)

        + General

          + [Introduction](../../general/introduction.md)
          + [Getting started](../../general/getting-started/README.md)
          + [Conversion software terms of use](../../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../../general/release-notes/README.md)
          + [Roadmap](../../general/roadmap.md)
        + User guide

          + [Overview](../../user-guide/overview.md)
          + [Before using the SMA](../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../user-guide/project-overview/README.md)
          + [Technical discovery](../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../user-guide/chatbot.md)
          + [Assessment](../../user-guide/assessment/README.md)
          + [Conversion](../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../use-cases/conversion-walkthrough.md)
          + [Migration lab](../../use-cases/migration-lab/README.md)
          + [Sample project](../../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../issue-analysis/approach.md)
          + [Issue code categorization](../../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../../issue-analysis/workarounds.md)
          + [Deploying the output code](../../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../translation-reference-overview.md)
          + [SIT tagging](README.md)

            - [SQL statements](sql-statements.md)
          + [SQL embedded code](../sql-embedded-code.md)
          + [HiveSQL](../hivesql/README.md)
          + [Spark SQL](../spark-sql/README.md)
        + Workspace estimator

          + [Overview](../../workspace-estimator/overview.md)
          + [Getting started](../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../interactive-assessment-application/overview.md)
          + [Installation guide](../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../support/glossary.md)
          + [Contact us](../../support/contact-us.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[Snowpark Migration Accelerator](../../README.md)Translation reference[SIT tagging](README.md)SQL statements

# Snowpark Migration Accelerator: SQL statements[¶](#snowpark-migration-accelerator-sql-statements "Link to this heading")

## Tagged elements [¶](#tagged-elements "Link to this heading")

SQL statements are tagged to monitor usage and consumption.

| Statements | HiveSQL | SparkSQL | SnowSQL |
| --- | --- | --- | --- |
| **CREATE TABLE** | SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |
| **CREATE VIEW** | SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |
| **CREATE FUNCTION** | NOT SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |
| **ALTER TABLE** | SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |
| **ALTER VIEW** | SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |

Note

When a comment is marked as “FUNCTIONAL EQUIVALENT,” it means that only the comment’s transformation to Snowflake has been validated. Any other statements within the comment are not included in this status assessment.

### Usages [¶](#usages "Link to this heading")

The tool identifies and tags the following statements:

#### CREATE STATEMENTS[¶](#create-statements "Link to this heading")

CREATE statements will include tags in two scenarios:

1. The SQL statement is missing the COMMENT property.
2. The SQL statement includes a `COMMENT` property, but no value has been assigned to it.

If a SQL statement includes a comment, the comment will be preserved during the conversion process.

##### Example [¶](#example "Link to this heading")

**Input (Apache SparkSQL)**

```
CREATE OR REPLACE VIEW some_view
AS
SELECT id, name FROM some_table WHERE some_column > 5;

CREATE OR REPLACE FUNCTION blue()
RETURNS STRING
LANGUAGE SQL
COMMENT ''
RETURN '0000FF';

CREATE TABLE my_varchar (
    COL1 VARCHAR(5)
) COMMENT 'The Table';
```

Copy

**Output (Snowflake SQL)**

```
CREATE OR REPLACE VIEW some_view
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":1,"minor":2,"patch":3},"attributes":{"language":"HiveSql"}}'
AS
SELECT
   id,
   name
FROM
   some_table
WHERE
   some_column > 5;
   
CREATE OR REPLACE FUNCTION blue()
RETURNS STRING LANGUAGE SQL
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}'
RETURN '0000FF';

CREATE TABLE my_varchar
(COL1 VARCHAR(5))
COMMENT = 'The Table';
```

Copy

The formatting of the generated code may appear different from the source code due to formatting differences in the original file.

---

##### Create Table [¶](#create-table "Link to this heading")

**Input code (SparkSQL)**

```
CREATE TABLE SOME_TABLE
(COL1 VARCHAR(5));
```

Copy

**Output code (Snowflake SQL)**

```
CREATE TABLE SOME_TABLEA
(COL1 VARCHAR(5))
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}';
```

Copy

---

##### CREATE VIEW [¶](#create-view "Link to this heading")

**Source Code (HiveSQL)**

```
CREATE OR REPLACE VIEW experienced_employee
AS
SELECT id, name FROM all_employee
WHERE working_years > 5;
```

Copy

**Output code (Snowflake SQL)**

```
CREATE OR REPLACE VIEW experienced_employee
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":1,"minor":2,"patch":3},"attributes":{"language":"HiveSql"}}'
AS
SELECT
   id,
   name
FROM
   all_employee
WHERE
   working_years > 5;
```

Copy

---

##### CREATE FUNCTION [¶](#create-function "Link to this heading")

**Input code (SparkSQL)**

```
CREATE OR REPLACE FUNCTION blue()
RETURNS STRING
LANGUAGE SQL RETURN '0000FF';
```

Copy

**Output (Snowflake SQL)**

```
CREATE OR REPLACE FUNCTION blue()
RETURNS STRING
LANGUAGE SQL
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}'
RETURN '0000FF';
```

Copy

#### ALTER STATEMENTS[¶](#alter-statements "Link to this heading")

ALTER statements include a tag when the comment property is empty. This occurs in two scenarios in SparkSQL:

1. When using `SET TBLPROPERTIES` with an empty comment
2. When using `UNSET TBLPROPERTIES`

##### Examples[¶](#examples "Link to this heading")

**SET TBLPROPERTIES (ALTER VIEW and ALTER TABLE)**

**Input (Apache Spark SQL)**

```
ALTER TABLE SOME_TABLE SET TBLPROPERTIES ('comment'= ' ');
-- ALTER VIEW
ALTER VIEW SOME_VIEW SET TBLPROPERTIES ('comment'= ' ');
```

Copy

**Output (Snowflake SQL)**

```
-- ALTER TABLE
ALTER TABLE SOME_TABLE
SET TBLPROPERTIES ('comment' = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}');

-- ALTER VIEW
ALTER VIEW SOME_VIEW
SET TBLPROPERTIES ('comment' = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}');

**Input (Apache HiveSQL)**

```{code} sql
:force:
-- ALTER TABLE
ALTER TABLE SOME_TABLE SET TBLPROPERTIES ('comment'= ' ');

-- ALTER VIEW
ALTER VIEW SOME_VIEW SET TBLPROPERTIES ('comment'= ' ');
```

Copy

**Output (Snowflake SQL)**

```
-- ALTER TABLE
ALTER TABLE SOME_TABLE
SET TBLPROPERTIES ('comment' = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"HiveSql"}}');

-- ALTER VIEW
ALTER VIEW SOME_VIEW
SET TBLPROPERTIES ('comment' = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"HiveSql"}}');
```

Copy

**UNSET TBLPROPERTIES (ALTER VIEW and ALTER TABLE)**

**Input (Apache Spark SQL)**

```
-- ALTER TABLE
ALTER TABLE SOME_TABLE UNSET TBLPROPERTIES ('comment');

-- ALTER VIEW
ALTER VIEW SOME_VIEW UNSET TBLPROPERTIES ('comment');

**Output (Snowflake SQL)**

```{code} sql
:force:
-- ALTER TABLE
ALTER TABLE SOME_TABLE
UNSET TBLPROPERTIES ('comment')
ALTER TABLE SOME_TABLE
SET COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}'

-- ALTER VIEW
ALTER VIEW SOME_VIEW
UNSET TBLPROPERTIES ('comment')
ALTER VIEW SOME_VIEW
SET COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}'
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

The Snowpark Migration Accelerator tool (SMA) is subject to the [Conversion Software Terms of Use](https://www.snowflake.com/en/legal/technical-services-and-education/conversion-software-terms/).

On this page

1. [Tagged elements](#tagged-elements)