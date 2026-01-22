---
auto_generated: true
description: Note
last_scraped: '2026-01-14T16:51:50.602955+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/translation-reference/sql-embedded-code
title: 'Snowpark Migration Accelerator:  SQL Embedded code | Snowflake Documentation'
---

1. [Overview](../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../guides/overview-db.md)
8. [Data types](../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../README.md)

    * Tools

      * [SnowConvert AI](../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../README.md)

        + General

          + [Introduction](../general/introduction.md)
          + [Getting started](../general/getting-started/README.md)
          + [Conversion software terms of use](../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../general/release-notes/README.md)
          + [Roadmap](../general/roadmap.md)
        + User guide

          + [Overview](../user-guide/overview.md)
          + [Before using the SMA](../user-guide/before-using-the-sma/README.md)
          + [Project overview](../user-guide/project-overview/README.md)
          + [Technical discovery](../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../user-guide/chatbot.md)
          + [Assessment](../user-guide/assessment/README.md)
          + [Conversion](../user-guide/conversion/README.md)
          + [Using the SMA CLI](../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../use-cases/conversion-walkthrough.md)
          + [Migration lab](../use-cases/migration-lab/README.md)
          + [Sample project](../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../issue-analysis/approach.md)
          + [Issue code categorization](../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../issue-analysis/workarounds.md)
          + [Deploying the output code](../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](translation-reference-overview.md)
          + [SIT tagging](sit-tagging/README.md)
          + [SQL embedded code](sql-embedded-code.md)
          + [HiveSQL](hivesql/README.md)
          + [Spark SQL](spark-sql/README.md)
        + Workspace estimator

          + [Overview](../workspace-estimator/overview.md)
          + [Getting started](../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../interactive-assessment-application/overview.md)
          + [Installation guide](../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../support/glossary.md)
          + [Contact us](../support/contact-us.md)
    * Guides

      * [Teradata](../../guides/teradata.md)
      * [Databricks](../../guides/databricks.md)
      * [SQL Server](../../guides/sqlserver.md)
      * [Amazon Redshift](../../guides/redshift.md)
      * [Oracle](../../guides/oracle.md)
      * [Azure Synapse](../../guides/azuresynapse.md)
15. [Queries](../../../guides/overview-queries.md)
16. [Listings](../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../guides/overview-alerts.md)
25. [Security](../../../guides/overview-secure.md)
26. [Data Governance](../../../guides/overview-govern.md)
27. [Privacy](../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../guides/overview-performance.md)
33. [Cost & Billing](../../../guides/overview-cost.md)

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[Snowpark Migration Accelerator](../README.md)Translation referenceSQL embedded code

# Snowpark Migration Accelerator: SQL Embedded code[¶](#snowpark-migration-accelerator-sql-embedded-code "Link to this heading")

Note

Currently, SMA only supports the [***pyspark.sql***](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.sql.html) function.

SMA can transform SQL code that is embedded within Python or Scala files. It processes embedded SQL code in the following file extensions:

* Python source code files (with .py extension)
* Scala source code files (with .scala extension)
* Jupyter Notebook files (with .ipynb extension)
* Databricks source files (with .python or .scala extensions)
* Databricks Notebook archive files (with .dbc extension)

## Embedded SQL Code transformation Samples[¶](#embedded-sql-code-transformation-samples "Link to this heading")

### Supported Case[¶](#supported-case "Link to this heading")

* Using the [*spark.sql*](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.sql.html) function in Python to execute SQL queries:

```
# Original in Spark
spark.sql("""MERGE INTO people_target pt
USING people_source ps
ON (pt.person_id1 = ps.person_id2)
WHEN NOT MATCHED BY SOURCE THEN DELETE""")
```

Copy

```
# SMA transformation
spark.sql("""MERGE INTO people_target pt
USING (
   SELECT
      pt.person_id1
   FROM
      people_target pt
      LEFT JOIN
         people_source ps
         ON pt.person_id1 = ps.person_id2
   WHERE
      ps.person_id2 IS NULL
) s_src
ON pt.person_id1 = s_src.person_id1
WHEN MATCHED THEN
   DELETE;""")
```

Copy

## Unsupported Cases[¶](#unsupported-cases "Link to this heading")

When SMA encounters code that it cannot convert, it generates an Error, Warning, and Issue (EWI) message in the output code. For more details about these messages, see [EWI](#unsupported-cases-and-ewi-messages).

The following scenarios are not currently supported:

* When working with SQL code, you can incorporate string variables in the following way:

```
query = "SELECT COUNT(COUNTRIES) FROM SALES"
dfSales = spark.sql(query)
```

Copy

```
query = "SELECT COUNT(COUNTRIES) FROM SALES" 
#EWI: SPRKPY1077 => SQL embedded code cannot be processed. 
dfSales = spark.sql(query)
```

Copy

* Combining strings to build SQL code using simple concatenation:

```
base = "SELECT "
criteria_1 = " COUNT(*) "
criteria_2 = " * "
fromClause = " FROM COUNTRIES"

df1 = spark.sql(bas + criteria_1 + fromClause)
df2 = spark.sql(bas + criteria_2 + fromClause)
```

Copy

```
base = "SELECT "
criteria_1 = " COUNT(*) "
criteria_2 = " * "
fromClause = " FROM COUNTRIES"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.

df1 = spark.sql(bas + criteria_1 + fromClause)
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
df2 = spark.sql(bas + criteria_2 + fromClause)
```

Copy

* Using string interpolation to dynamically generate SQL statements:

```
# Old Style interpolation
UStbl = "SALES_US"
salesUS = spark.sql("SELECT * FROM %s" % (UStbl))

# Using format function
COLtbl = "COL_SALES WHERE YEAR(saleDate) > 2023"
salesCol = spark.sql("SELECT * FROM {}".format(COLtbl))

# New Style
UKTbl = " UK_SALES_JUN_18" 
salesUk = spark.sql(f"SELECT * FROM {UKTbl}")
```

Copy

```
# Old Style interpolation
UStbl = "SALES_US"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
salesUS = spark.sql("SELECT * FROM %s" % (UStbl))

# Using format function
COLtbl = "COL_SALES WHERE YEAR(saleDate) > 2023"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
salesCol = spark.sql("SELECT * FROM {}".format(COLtbl))

# New Style
UKTbl = " UK_SALES_JUN_18"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
salesUk = spark.sql(f"SELECT * FROM {UKTbl}")
```

Copy

* Using functions that generate SQL queries dynamically:

```
def ByMonth(month):
    query = f"SELECT * LOGS WHERE MONTH(access_date) = {month}"
    return spark.sql(query)
```

Copy

```
def ByMonth(month):
query = f"SELECT * LOGS WHERE MONTH(access_date) = {month}"
    #EWI: SPRKPY1077 => SQL embedded code cannot be processed.
    return spark.sql(query)
```

Copy

## Unsupported Cases and EWI messages[¶](#unsupported-cases-and-ewi-messages "Link to this heading")

* When analyzing Scala code, the error code SPRKSCL1173 indicates unsupported embedded SQL statements.

```
/*Scala*/
 class SparkSqlExample {
    def main(spark: SparkSession) : Unit = {
    /*EWI: SPRKSCL1173 => SQL embedded code cannot be processed.*/
    spark.sql("CREATE VIEW IF EXISTS My View AS Select * From my Table WHERE date < current_date() ")
    }
```

Copy

* When Python code contains unsupported embedded SQL statements, the error code SPRKPY1077 will be displayed.

```
# Python Output 
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
b = spark.sql("CREATE VIEW IF EXISTS My View AS Select * From my Table WHERE date < current_date() ")
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

1. [Embedded SQL Code transformation Samples](#embedded-sql-code-transformation-samples)
2. [Unsupported Cases](#unsupported-cases)
3. [Unsupported Cases and EWI messages](#unsupported-cases-and-ewi-messages)