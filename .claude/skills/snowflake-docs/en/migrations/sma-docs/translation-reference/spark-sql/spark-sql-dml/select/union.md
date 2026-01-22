---
auto_generated: true
description: 'Merges two subqueries into a single query. Databricks SQL provides three
  set operators that allow you to combine queries:'
last_scraped: '2026-01-14T16:51:55.523956+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/translation-reference/spark-sql/spark-sql-dml/select/union
title: 'Snowpark Migration Accelerator:  Union | Snowflake Documentation'
---

1. [Overview](../../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../../guides/overview-db.md)
8. [Data types](../../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../../../README.md)

        + General

          + [Introduction](../../../../general/introduction.md)
          + [Getting started](../../../../general/getting-started/README.md)
          + [Conversion software terms of use](../../../../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../../../../general/release-notes/README.md)
          + [Roadmap](../../../../general/roadmap.md)
        + User guide

          + [Overview](../../../../user-guide/overview.md)
          + [Before using the SMA](../../../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../../../user-guide/project-overview/README.md)
          + [Technical discovery](../../../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../../../user-guide/chatbot.md)
          + [Assessment](../../../../user-guide/assessment/README.md)
          + [Conversion](../../../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../../../../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../../../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../../../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../../../use-cases/conversion-walkthrough.md)
          + [Migration lab](../../../../use-cases/migration-lab/README.md)
          + [Sample project](../../../../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../../../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../../../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../../../../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../../../issue-analysis/approach.md)
          + [Issue code categorization](../../../../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../../../../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../../../../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../../../../issue-analysis/workarounds.md)
          + [Deploying the output code](../../../../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../../../translation-reference-overview.md)
          + [SIT tagging](../../../sit-tagging/README.md)
          + [SQL embedded code](../../../sql-embedded-code.md)
          + [HiveSQL](../../../hivesql/README.md)
          + [Spark SQL](../../README.md)

            - [Spark SQL DDL](../../spark-sql-ddl/README.md)
            - [Spark SQL DML](../README.md)

              * [MERGE](../merge.md)
              * [SELECT](README.md)

                + [DISTINCT](distinct.md)
                + [VALUES](values.md)
                + [JOIN](join.md)
                + [WHERE](where.md)
                + [GROUP BY](group-by.md)
                + [UNION](union.md)
            - [Spark SQL data types](../../spark-sql-data-types.md)
            - [Supported functions](../../supported-functions.md)
        + Workspace estimator

          + [Overview](../../../../workspace-estimator/overview.md)
          + [Getting started](../../../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../../../interactive-assessment-application/overview.md)
          + [Installation guide](../../../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../../../support/glossary.md)
          + [Contact us](../../../../support/contact-us.md)
    * Guides

      * [Teradata](../../../../../guides/teradata.md)
      * [Databricks](../../../../../guides/databricks.md)
      * [SQL Server](../../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../../guides/redshift.md)
      * [Oracle](../../../../../guides/oracle.md)
      * [Azure Synapse](../../../../../guides/azuresynapse.md)
15. [Queries](../../../../../../guides/overview-queries.md)
16. [Listings](../../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../../guides/overview-alerts.md)
25. [Security](../../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../../guides/overview-cost.md)

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[Snowpark Migration Accelerator](../../../../README.md)Translation reference[Spark SQL](../../README.md)[Spark SQL DML](../README.md)[SELECT](README.md)UNION

# Snowpark Migration Accelerator: Union[¶](#snowpark-migration-accelerator-union "Link to this heading")

## Description[¶](#description "Link to this heading")

Merges two subqueries into a single query. Databricks SQL provides three set operators that allow you to combine queries:

* `EXCEPT` - Retrieves all rows from the first query that do not appear in the second query
* `INTERSECT` - Returns only the rows that appear in both queries
* `UNION` - Combines the results of two or more queries into a single result set

[Databricks SQL Language Reference UNION](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-setops.html)

Set operators enable you to combine multiple queries into a single result. For more details, see [Snowflake SQL Language Reference UNION](https://docs.snowflake.com/en/sql-reference/operators-query).

### Syntax[¶](#syntax "Link to this heading")

```
subquery1 { { UNION [ ALL | DISTINCT ] |
              INTERSECT [ ALL | DISTINCT ] |
              EXCEPT [ ALL | DISTINCT ] } subquery2 } [...] }
```

Copy

```
[ ( ] <query> [ ) ] { INTERSECT | { MINUS | EXCEPT } | UNION [ ALL ] } [ ( ] <query> [ ) ]
[ ORDER BY ... ]
[ LIMIT ... ]
```

Copy

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### Setup data[¶](#setup-data "Link to this heading")

#### Databricks[¶](#databricks "Link to this heading")

```
CREATE TEMPORARY VIEW number1(c) AS VALUES (3), (1), (2), (2), (3), (4);

CREATE TEMPORARY VIEW number2(c) AS VALUES (5), (1), (1), (2);
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
CREATE TEMPORARY TABLE number1(c int);
INSERT INTO number1 VALUES (3), (1), (2), (2), (3), (4);

CREATE TEMPORARY TABLE number2(c int);
INSERT INTO number2 VALUES (5), (1), (1), (2);
```

Copy

### Pattern code[¶](#pattern-code "Link to this heading")

#### Databricks[¶](#id1 "Link to this heading")

```
-- EXCEPT (MINUS) Operator:
SELECT c FROM number1 EXCEPT SELECT c FROM number2;

SELECT c FROM number1 MINUS SELECT c FROM number2;

-- EXCEPT ALL (MINUS ALL) Operator:
SELECT c FROM number1 EXCEPT ALL (SELECT c FROM number2);

SELECT c FROM number1 MINUS ALL (SELECT c FROM number2);

-- INTERSECT Operator:
(SELECT c FROM number1) INTERSECT (SELECT c FROM number2);

-- INTERSECT DISTINCT Operator:
(SELECT c FROM number1) INTERSECT DISTINCT (SELECT c FROM number2);

-- INTERSECT ALL Operator:
(SELECT c FROM number1) INTERSECT ALL (SELECT c FROM number2);

-- UNION Operator:
(SELECT c FROM number1) UNION (SELECT c FROM number2);

-- UNION DISTINCT Operator:
(SELECT c FROM number1) UNION DISTINCT (SELECT c FROM number2);

-- UNION ALL Operator:
SELECT c FROM number1 UNION ALL (SELECT c FROM number2);
```

Copy

**EXCEPT (MINUS) Operator:** The EXCEPT operator, also known as MINUS, removes rows from the first query that appear in the result set of the second query. It returns only unique rows from the first query that do not exist in the second query.

| c |
| --- |
| 3 |
| 4 |

**EXCEPT ALL (MINUS ALL) Operator: Removes Duplicate Records**

| c |
| --- |
| 3 |
| 3 |
| 4 |

**INTERSECT Operator:** Returns only the rows that appear in both result sets, eliminating duplicates. It compares the results of two or more SELECT statements and returns only the matching records. Returns only the rows that appear in both result sets, eliminating duplicates.

| c |
| --- |
| 1 |
| 2 |

**INTERSECT DISTINCT Operator:** Returns only unique rows that appear in both result sets, eliminating any duplicates. Returns only unique rows that appear in both queries, eliminating any duplicates from the result set.

| c |
| --- |
| 1 |
| 2 |

**INTERSECT ALL Operator:** Returns all matching rows from multiple queries, including duplicates. Unlike the standard INTERSECT operator, which removes duplicates, INTERSECT ALL preserves duplicate rows in the final result set. Returns all rows that appear in both result sets, including duplicates. Unlike INTERSECT, which removes duplicates, INTERSECT ALL preserves duplicate rows based on their frequency in both sets.

| c |
| --- |
| 1 |
| 2 |
| 2 |

**UNION Operator:** The UNION operator combines the results of two or more SELECT statements into a single result set. It removes duplicate rows from the combined result set by default. The UNION operator combines the results of two or more SELECT statements into a single result set. It removes duplicate rows from the combined results.

| c |
| --- |
| 1 |
| 3 |
| 5 |
| 4 |
| 2 |

**UNION DISTINCT Operator:** The UNION DISTINCT operator combines two or more result sets and removes any duplicate rows from the final output. It returns only unique rows from all the combined queries. The UNION DISTINCT operator combines rows from two or more queries while removing any duplicate rows from the final result set.

| c |
| --- |
| 1 |
| 3 |
| 5 |
| 4 |
| 2 |

**UNION ALL Operator:** The UNION ALL operator combines rows from two or more queries without removing duplicate records. Unlike the UNION operator, UNION ALL retains all rows, including duplicates, making it faster to execute since it doesn’t need to perform duplicate checking. This operator combines the results of two or more SELECT statements and includes all rows, including duplicates. Unlike UNION, which removes duplicate rows, UNION ALL retains all rows from all SELECT statements.

| c |
| --- |
| 3 |
| 1 |
| 2 |
| 2 |
| 3 |
| 4 |
| 5 |
| 1 |
| 1 |
| 2 |

#### Snowflake[¶](#id2 "Link to this heading")

```
-- EXCEPT (MINUS) Operator
SELECT c FROM number1 EXCEPT SELECT c FROM number2;

SELECT c FROM number1 MINUS SELECT c FROM number2;

-- EXCEPT ALL (MINUS ALL) Operator:
SELECT number1.c FROM number1 
LEFT JOIN number2 
    ON number1.c = number2.c
WHERE number2.c IS NULL;
-- ** MSC-WARMING - MSC-S000# - EXCEPT ALL IS TRANSFORMED TO A LEFT JOIN. **

SELECT number1.c FROM number1 
LEFT JOIN number2 
    ON number1.c = number2.c
WHERE number2.c IS NULL;
-- ** MSC-WARMING - MSC-S000# - MINUS ALL IS TRANSFORMED TO A LEFT JOIN. **

-- INTERSECT Operator:
(SELECT c FROM number1) INTERSECT (SELECT c FROM number2);

-- INTERSECT DISTINCT Operator:
(SELECT c FROM number1) INTERSECT (SELECT c FROM number2);

-- INTERSECT ALL Operator:
SELECT DISTINCT number1.c FROM number1 
INNER JOIN number2 
    ON number1.c = number2.c;
-- ** MSC-WARMING - MSC-S000# - INTERSECT ALL IS TRANSFORMED TO A INNER JOIN. **

-- UNION Operator:
(SELECT c FROM number1) UNION (SELECT c FROM number2);

-- UNION DISTINCT Operator:
(SELECT c FROM number1) UNION DISTINCT (SELECT c FROM number2);

-- UNION ALL Operator:
SELECT c FROM number1 UNION ALL (SELECT c FROM number2);
```

Copy

**EXCEPT (MINUS) Operator: Removes Duplicate Records**

The EXCEPT operator, also known as MINUS, compares two queries and returns only the unique records from the first query that do not appear in the second query. It eliminates duplicate rows from the result set.

| c |
| --- |
| 3 |
| 4 |

**EXCEPT ALL (MINUS ALL) Operator: Removes Duplicate Rows**

| c |
| --- |
| 3 |
| 3 |
| 4 |

**INTERSECT Operator:**

| c |
| --- |
| 1 |
| 2 |

**INTERSECT DISTINCT Operator:**

| c |
| --- |
| 1 |
| 2 |

**INTERSECT ALL Operator:**

| c |
| --- |
| 1 |
| 2 |
| 2 |

**UNION Operator:**

| c |
| --- |
| 1 |
| 3 |
| 5 |
| 4 |
| 2 |

**UNION DISTINCT Operator:**

| c |
| --- |
| 1 |
| 3 |
| 5 |
| 4 |
| 2 |

**UNION ALL Operator:**

| c |
| --- |
| 3 |
| 1 |
| 2 |
| 2 |
| 3 |
| 4 |
| 5 |
| 1 |
| 1 |
| 2 |

### Known Issues[¶](#known-issues "Link to this heading")

No related EWIs

### Related EWIs[¶](#related-ewis "Link to this heading")

* MSC-S000#: A SET operator with the ALL keyword is converted into a JOIN operation.

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

1. [Description](#description)
2. [Sample Source Patterns](#sample-source-patterns)