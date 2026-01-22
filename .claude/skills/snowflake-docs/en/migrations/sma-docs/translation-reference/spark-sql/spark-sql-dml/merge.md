---
auto_generated: true
description: The MERGE statement combines data from one or more source tables with
  a target table, allowing you to perform updates and inserts in a single operation.
  Based on conditions you define, it determines w
last_scraped: '2026-01-14T16:51:53.958334+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/sma-docs/translation-reference/spark-sql/spark-sql-dml/merge
title: 'Snowpark Migration Accelerator:  Merge | Snowflake Documentation'
---

1. [Overview](../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../guides/overview-db.md)
8. [Data types](../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../snowconvert-docs/overview.md)
      * [Snowpark Migration Accelerator](../../../README.md)

        + General

          + [Introduction](../../../general/introduction.md)
          + [Getting started](../../../general/getting-started/README.md)
          + [Conversion software terms of use](../../../general/conversion-software-terms-of-use/README.md)
          + [Release notes](../../../general/release-notes/README.md)
          + [Roadmap](../../../general/roadmap.md)
        + User guide

          + [Overview](../../../user-guide/overview.md)
          + [Before using the SMA](../../../user-guide/before-using-the-sma/README.md)
          + [Project overview](../../../user-guide/project-overview/README.md)
          + [Technical discovery](../../../user-guide/project-overview/optional-technical-discovery.md)
          + [AI assistant](../../../user-guide/chatbot.md)
          + [Assessment](../../../user-guide/assessment/README.md)
          + [Conversion](../../../user-guide/conversion/README.md)
          + [Using the SMA CLI](../../../user-guide/using-the-sma-cli/README.md)
        + Use cases

          + Snowflake VS Code extension

            + [SMA checkpoints walkthrough](../../../use-cases/sma-checkpoints-walkthrough/README.md)
            + [SMA EWI Assistant walkthrough](../../../use-cases/sma-ewi-assistant-walkthrough/README.md)
          + [Assessment walkthrough](../../../use-cases/assessment-walkthrough/README.md)
          + [Conversion walkthrough](../../../use-cases/conversion-walkthrough.md)
          + [Migration lab](../../../use-cases/migration-lab/README.md)
          + [Sample project](../../../use-cases/sample-project.md)
          + [Using SMA in an Ubuntu Docker image](../../../use-cases/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [SMA CLI walkthrough](../../../use-cases/sma-cli-walkthrough.md)
          + [Snowpark Connect](../../../use-cases/snowpark-connect/README.md)
        + Issue analysis

          + [Approach](../../../issue-analysis/approach.md)
          + [Issue code categorization](../../../issue-analysis/issue-code-categorization.md)
          + [Issue codes by source](../../../issue-analysis/issue-codes-by-source/README.md)
          + [Troubleshooting the output code](../../../issue-analysis/troubleshooting-the-output-code/README.md)
          + [Workarounds](../../../issue-analysis/workarounds.md)
          + [Deploying the output code](../../../issue-analysis/deploying-the-output-code.md)
        + Translation reference

          + [Translation reference overview](../../translation-reference-overview.md)
          + [SIT tagging](../../sit-tagging/README.md)
          + [SQL embedded code](../../sql-embedded-code.md)
          + [HiveSQL](../../hivesql/README.md)
          + [Spark SQL](../README.md)

            - [Spark SQL DDL](../spark-sql-ddl/README.md)
            - [Spark SQL DML](README.md)

              * [MERGE](merge.md)
              * [SELECT](select/README.md)
            - [Spark SQL data types](../spark-sql-data-types.md)
            - [Supported functions](../supported-functions.md)
        + Workspace estimator

          + [Overview](../../../workspace-estimator/overview.md)
          + [Getting started](../../../workspace-estimator/getting-started.md)
        + Interactive assessment application

          + [Overview](../../../interactive-assessment-application/overview.md)
          + [Installation guide](../../../interactive-assessment-application/installation-guide.md)
        + Support

          + [General troubleshooting](../../../support/general-troubleshooting/README.md)
          + [Frequently asked questions](../../../support/frequently-asked-questions-faq/README.md)
          + [Glossary](../../../support/glossary.md)
          + [Contact us](../../../support/contact-us.md)
    * Guides

      * [Teradata](../../../../guides/teradata.md)
      * [Databricks](../../../../guides/databricks.md)
      * [SQL Server](../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../guides/redshift.md)
      * [Oracle](../../../../guides/oracle.md)
      * [Azure Synapse](../../../../guides/azuresynapse.md)
15. [Queries](../../../../../guides/overview-queries.md)
16. [Listings](../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../guides/overview-alerts.md)
25. [Security](../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../guides/overview-cost.md)

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[Snowpark Migration Accelerator](../../../README.md)Translation reference[Spark SQL](../README.md)[Spark SQL DML](README.md)MERGE

# Snowpark Migration Accelerator: Merge[¶](#snowpark-migration-accelerator-merge "Link to this heading")

## Description[¶](#description "Link to this heading")

The `MERGE` statement combines data from one or more source tables with a target table, allowing you to perform updates and inserts in a single operation. Based on conditions you define, it determines whether to update existing rows or insert new ones in the target table. This makes it more efficient than using separate `INSERT`, `UPDATE`, and `DELETE` statements. The `MERGE` statement always produces consistent results when run multiple times with the same data.

In Spark, you can find the MERGE syntax in the [Spark documentation](https://docs.databricks.com/en/sql/language-manual/delta-merge-into.html).

```
MERGE INTO target_table_name [target_alias]
   USING source_table_reference [source_alias]
   ON merge_condition
   { WHEN MATCHED [ AND matched_condition ] THEN matched_action |
     WHEN NOT MATCHED [BY TARGET] [ AND not_matched_condition ] THEN not_matched_action |
     WHEN NOT MATCHED BY SOURCE [ AND not_matched_by_source_condition ] THEN not_matched_by_source_action } [...]

matched_action
 { DELETE |
   UPDATE SET * |
   UPDATE SET { column = { expr | DEFAULT } } [, ...] }

not_matched_action
 { INSERT * |
   INSERT (column1 [, ...] ) VALUES ( expr | DEFAULT ] [, ...] )

not_matched_by_source_action
 { DELETE |
   UPDATE SET { column = { expr | DEFAULT } } [, ...] }
```

Copy

In Snowflake, the MERGE statement follows this syntax (For additional details, refer to the [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/merge)):

```
MERGE INTO <target_table> USING <source> ON <join_expr> { matchedClause | notMatchedClause } [ ... ]

matchedClause ::=
  WHEN MATCHED [ AND <case_predicate> ] THEN { UPDATE SET <col_name> = <expr> [ , <col_name2> = <expr2> ... ] | DELETE } [ ... ]
  
notMatchedClause ::=
   WHEN NOT MATCHED [ AND <case_predicate> ] THEN INSERT [ ( <col_name> [ , ... ] ) ] VALUES ( <expr> [ , ... ] )
```

Copy

The key distinction is that Snowflake lacks a direct equivalent to the `WHEN NOT MATCHED BY SOURCE` clause. A workaround solution is required to achieve similar functionality in Snowflake.

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### Sample auxiliary data[¶](#sample-auxiliary-data "Link to this heading")

Note

The following code examples have been executed to help you better understand how they work:

```
CREATE OR REPLACE people_source ( 
  person_id  INTEGER NOT NULL PRIMARY KEY, 
  first_name STRING NOT NULL, 
  last_name  STRING NOT NULL, 
  title      STRING NOT NULL,
);

CREATE OR REPLACE TABLE people_target ( 
  person_id  INTEGER NOT NULL PRIMARY KEY, 
  first_name STRING NOT NULL, 
  last_name  STRING NOT NULL, 
  title      STRING NOT NULL DEFAULT 'NONE'
);


INSERT INTO people_target VALUES (1, 'John', 'Smith', 'Mr');
INSERT INTO people_target VALUES (2, 'alice', 'jones', 'Mrs');
INSERT INTO people_source VALUES (2, 'Alice', 'Jones', 'Mrs.');
INSERT INTO people_source VALUES (3, 'Jane', 'Doe', 'Miss');
INSERT INTO people_source VALUES (4, 'Dave', 'Brown', 'Mr');
```

Copy

```
CREATE OR REPLACE TABLE people_source (
    person_id  INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    title VARCHAR(10) NOT NULL
);

CREATE OR REPLACE TABLE people_target (
    person_id  INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    title VARCHAR(10) NOT NULL DEFAULT 'NONE'
);


INSERT INTO people_target VALUES (1, 'John', 'Smith', 'Mr');
INSERT INTO people_target VALUES (2, 'alice', 'jones', 'Mrs');
INSERT INTO people_source VALUES (2, 'Alice', 'Jones', 'Mrs.');
INSERT INTO people_source VALUES (3, 'Jane', 'Doe', 'Miss');
INSERT INTO people_source VALUES (4, 'Dave', 'Brown', 'Mr');
```

Copy

### MERGE Statement - Insert and Update Case[¶](#merge-statement-insert-and-update-case "Link to this heading")

#### Spark[¶](#spark "Link to this heading")

```
MERGE INTO people_target pt 
USING people_source ps 
ON    (pt.person_id = ps.person_id) 
WHEN MATCHED THEN UPDATE 
  SET pt.first_name = ps.first_name, 
      pt.last_name = ps.last_name, 
      pt.title = DEFAULT 
WHEN NOT MATCHED THEN INSERT 
  (pt.person_id, pt.first_name, pt.last_name, pt.title) 
  VALUES (ps.person_id, ps.first_name, ps.last_name, ps.title);


SELECT * FROM people_target;
```

Copy

```
PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
---------+----------+---------+-----+
        1|John      |Smith    |Mr   |
        2|Alice     |Jones    |NONE |
        3|Jane      |Doe      |Miss |
        4|Dave      |Brown    |Mr   |
```

Copy

#### Snowflake[¶](#snowflake "Link to this heading")

```
MERGE INTO people_target2 pt 
USING people_source ps 
ON    (pt.person_id = ps.person_id) 
WHEN MATCHED THEN UPDATE 
  SET pt.first_name = ps.first_name, 
      pt.last_name = ps.last_name, 
      pt.title = DEFAULT 
WHEN NOT MATCHED THEN INSERT 
  (pt.person_id, pt.first_name, pt.last_name, pt.title) 
  VALUES (ps.person_id, ps.first_name, ps.last_name, ps.title);


SELECT * FROM PUBLIC.people_target ORDER BY person_id;
```

Copy

```
PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
---------+----------+---------+-----+
        1|John      |Smith    |Mr   |
        2|Alice     |Jones    |NONE |
        3|Jane      |Doe      |Miss |
        4|Dave      |Brown    |Mr   |
```

Copy

The `INSERT` and `UPDATE` operations work the same way in Snowflake. In both SQL dialects, you can use `DEFAULT` as an expression to set a column to its default value.

Spark allows insert and update operations without explicitly listing the columns. When columns are not specified, the operation affects all columns in the table. For this to work correctly, the source and destination tables must have identical column structures. If the column structures don’t match, you will receive a parsing error.

```
UPDATE SET *
-- This is equivalent to UPDATE SET col1 = source.col1 [, col2 = source.col2 ...]

INSERT * 
-- This command copies all columns from the source table to the target table, matching columns by name. It is the same as explicitly listing all columns in both the INSERT and VALUES clauses.

Since Snowflake doesn't support these options, the migration process will instead list all columns from the target table.

### MERGE Statement - Delete Case

 
```{code} sql
:force:
MERGE INTO people_target pt 
USING people_source ps 
ON    (pt.person_id = ps.person_id)
WHEN MATCHED AND pt.person_id < 3 THEN DELETE
WHEN NOT MATCHED BY TARGET THEN INSERT *;

SELECT * FROM people_target;
```

Copy

```
PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
---------+----------+---------+-----+
        1|John      |Smith    |Mr   |
        3|Jane      |Doe      |Miss |
        4|Dave      |Brown    |Mr   |
```

Copy

#### Snowflake[¶](#id1 "Link to this heading")

```
MERGE INTO people_target pt 
USING people_source ps 
ON    (pt.person_id = ps.person_id)
WHEN MATCHED AND pt.person_id < 3 THEN DELETE
WHEN NOT MATCHED THEN INSERT 
  (pt.person_id, pt.first_name, pt.last_name, pt.title) 
  VALUES (ps.person_id, ps.first_name, ps.last_name, ps.title);


SELECT * FROM people_target;
```

Copy

```
PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
---------+----------+---------+-----+
        1|John      |Smith    |Mr   |
        3|Jane      |Doe      |Miss |
        4|Dave      |Brown    |Mr   |
```

Copy

The `DELETE` action in Snowflake works the same way as in other databases. You can also add additional conditions to the `MATCHED` and `NOT MATCHED` clauses.

`WHEN NOT MATCHED BY TARGET` and `WHEN NOT MATCHED` are equivalent clauses that can be used interchangeably in SQL merge statements.

### MERGE Statement - WHEN NOT MATCHED BY SOURCE[¶](#merge-statement-when-not-matched-by-source "Link to this heading")

`WHEN NOT MATCHED BY SOURCE` clauses are triggered when a row in the target table has no matching rows in the source table. This occurs when both the `merge_condition` and the optional `not_match_by_source_condition` evaluate to true. For more details, see the [Spark documentation](https://docs.databricks.com/en/sql/language-manual/delta-merge-into.html).

Snowflake does not support this clause directly. To handle this limitation, you can use the following workaround for both `DELETE` and `UPDATE` actions.

```
MERGE INTO people_target pt 
USING people_source ps 
ON pt.person_id = ps.person_id
WHEN NOT MATCHED BY SOURCE THEN DELETE;


SELECT * FROM people_target;
```

Copy

```
PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
---------+----------+---------+-----+
        2|Alice     |Jones    |NONE |
```

Copy

#### Snowflake[¶](#id2 "Link to this heading")

```
MERGE INTO people_target pt 
USING (
    SELECT 
        pt.person_id 
    FROM
        people_target pt LEFT 
    JOIN people_source ps ON pt.person_id = ps.person_id
    WHERE 
        ps.person_id is null
) s_src
    ON s_src.person_id = pt.person_id
WHEN MATCHED THEN DELETE;

SELECT * FROM people_target;
```

Copy

```
PERSON_ID|FIRST_NAME|LAST_NAME|TITLE|
---------+----------+---------+-----+
        2|Alice     |Jones    |NONE |
```

Copy

The `DELETE` action in Snowflake works the same way as in other databases. You can also add additional conditions to the `MATCHED` and `NOT MATCHED` clauses.

## Known issues[¶](#known-issues "Link to this heading")

### 1. MERGE is very similar in both languages[¶](#merge-is-very-similar-in-both-languages "Link to this heading")

While Apache Spark offers additional features, you can achieve similar functionality in Snowflake using alternative approaches, as demonstrated in the previous examples.

## Related EWIs[¶](#related-ewis "Link to this heading")

No related Errors, Warnings, and Issues (EWIs) found.

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
3. [Known issues](#known-issues)
4. [Related EWIs](#related-ewis)