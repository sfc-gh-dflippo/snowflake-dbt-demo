---
auto_generated: true
description: A subquery is a query within another query. Subqueries in a FROM or WHERE
  clause are used to provide data that will be used to limit or compare/evaluate the
  data returned by the containing query. (Sno
last_scraped: '2026-01-14T16:51:10.878619+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/general/subqueries
title: SnowConvert AI - ANSI SQL - Subqueries | Snowflake Documentation
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

          + [General](README.md)

            - [Built-in Functions](built-in-functions.md)
            - [Subqueries](subqueries.md)
          + [Teradata](../teradata/README.md)
          + [Oracle](../oracle/README.md)
          + [SQL Server-Azure Synapse](../transact/README.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[General](README.md)Subqueries

# SnowConvert AI - ANSI SQL - Subqueries[¶](#snowconvert-ai-ansi-sql-subqueries "Link to this heading")

## Description[¶](#description "Link to this heading")

> A subquery is a query within another query. Subqueries in a [FROM](https://docs.snowflake.com/en/sql-reference/constructs/from) or [WHERE](https://docs.snowflake.com/en/sql-reference/constructs/where) clause are used to provide data that will be used to limit or compare/evaluate the data returned by the containing query. ([Snowflake subqueries documentation](https://docs.snowflake.com/en/user-guide/querying-subqueries)).

Subqueries can be correlated/uncorrelated as well as scalar/non-scalar.

**Correlated subqueries** reference columns from the outer query. In Snowflake, correlated subqueries execute for each row in the query. On the other hand, **Uncorrelated subqueries** do not reference the outer query and are executed once for the entire query.

**Scalar subqueries** return a single value as result, otherwise the subquery is **non-scalar.**

The following patterns are based on these categories.

## Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

### Setup data[¶](#setup-data "Link to this heading")

#### Teradata[¶](#teradata "Link to this heading")

```
CREATE TABLE tableA
(
    col1 INTEGER,
    col2 VARCHAR(20)
);

CREATE TABLE tableB
(
    col3 INTEGER,
    col4 VARCHAR(20)
);

INSERT INTO tableA VALUES (50, 'Hey');
INSERT INTO tableA VALUES (20, 'Example');

INSERT INTO tableB VALUES (50, 'Hey');
INSERT INTO tableB VALUES (20, 'Bye');
```

Copy

#### *Snowflake*[¶](#snowflake "Link to this heading")

```
CREATE OR REPLACE TABLE tableA
(
    col1 INTEGER,
    col2 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "12/02/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE tableB
(
    col3 INTEGER,
    col4 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "12/02/2024",  "domain": "test" }}'
;

INSERT INTO tableA
VALUES (50, 'Hey');

INSERT INTO tableA
VALUES (20, 'Example');

INSERT INTO tableB
VALUES (50, 'Hey');

INSERT INTO tableB
VALUES (20, 'Bye');
```

Copy

### Correlated Scalar subqueries[¶](#correlated-scalar-subqueries "Link to this heading")

Snowflake evaluates correlated subqueries **at compile time** to determine if they are scalar and therefore valid in the context were a single return value is expected. To solve this, the ANY\_VALUE aggregate function is added to the returned column when the result is not an aggregate function. This allows the compiler to determine a single value return is expected. Since scalar subqueries are expected to return a single value the function ANY\_VALUE will not change the result, it will just return the original value as is.

#### *Teradata*[¶](#id1 "Link to this heading")

```
SELECT col2
FROM tableA
WHERE col1 = (SELECT col3 FROM tableB WHERE col2 = col4);
```

Copy

#### Results[¶](#results "Link to this heading")

```
+------+
| col2 |
+------+
| Hey  |
+------+
```

Copy

#### *Snowflake*[¶](#id2 "Link to this heading")

```
SELECT
    col2
FROM
    tableA
WHERE col1 =
             --** SSC-FDM-0002 - CORRELATED SUBQUERIES MAY HAVE SOME FUNCTIONAL DIFFERENCES. **
             (
                 SELECT
                     ANY_VALUE(col3) FROM
                     tableB
                 WHERE
                     RTRIM( col2) = RTRIM(col4));
```

Copy

#### Results[¶](#id3 "Link to this heading")

```
+------+
| col2 |
+------+
| Hey  |
+------+
```

Copy

### Uncorrelated Scalar subqueries[¶](#uncorrelated-scalar-subqueries "Link to this heading")

Snowflake fully supports uncorrelated scalar subqueries.

#### *Teradata*[¶](#id4 "Link to this heading")

```
SELECT col2, (SELECT AVG(col3) FROM tableB) AS avgTableB
FROM tableA
WHERE col1 = (SELECT MAX(col3) FROM tableB);
```

Copy

#### Results[¶](#id5 "Link to this heading")

```
+------+-----------+
| col2 | avgTableB |
+------+-----------+
| Hey  | 35        |
+------+-----------+
```

Copy

#### *Snowflake*[¶](#id6 "Link to this heading")

```
SELECT
    col2,
    (
                 SELECT
                     AVG(col3) FROM
                     tableB
    ) AS avgTableB
            FROM
    tableA
            WHERE col1 = (
                 SELECT
                     MAX(col3) FROM
                     tableB
    );
```

Copy

#### Results[¶](#id7 "Link to this heading")

```
+------+-----------+
| col2 | avgTableB |
+------+-----------+
| Hey  | 35.000000 |
+------+-----------+
```

Copy

### Non-scalar subqueries[¶](#non-scalar-subqueries "Link to this heading")

Non-scalar subqueries specified inside subquery operators (ANY/ALL/IN/EXISTS) are supported.

Non-scalar subqueries used as derived tables are also supported.

#### *Teradata*[¶](#id8 "Link to this heading")

```
SELECT col2
FROM tableA
WHERE col1 IN (SELECT col3 FROM tableB);

SELECT col2
FROM tableA
WHERE col1 >= ALL(SELECT col3 FROM tableB);

SELECT col2, myDerivedTable.col4
FROM tableA, (SELECT * FROM tableB) AS myDerivedTable
WHERE col1 = myDerivedTable.col3;
```

Copy

#### Result[¶](#result "Link to this heading")

```
+---------+
| col2    |
+---------+
| Example |
+---------+
| Hey     |
+---------+

+---------+
| col2    |
+---------+
| Hey     |
+---------+

+---------+------+
| col2    | col4 |
+---------+------+
| Example | Bye  |
+---------+------+
| Hey     | Hey  |
+---------+------+
```

Copy

#### *Snowflake*[¶](#id9 "Link to this heading")

```
SELECT
    col2
            FROM
    tableA
            WHERE col1 IN (
                 SELECT
                     col3 FROM
                     tableB
    );

                     SELECT
    col2
            FROM
    tableA
            WHERE col1 >= ALL(
                 SELECT
                     col3 FROM
                     tableB
    );
                    SELECT
    col2,
    myDerivedTable.col4
            FROM
    tableA, (
                 SELECT
                     * FROM
                     tableB
    ) AS myDerivedTable
            WHERE col1 = myDerivedTable.col3;
```

Copy

#### Results[¶](#id10 "Link to this heading")

```
+---------+
| col2    |
+---------+
| Example |
+---------+
| Hey     |
+---------+

+---------+
| col2    |
+---------+
| Hey     |
+---------+

+---------+------+
| col2    | col4 |
+---------+------+
| Example | Bye  |
+---------+------+
| Hey     | Hey  |
+---------+------+
```

Copy

## Known Issues[¶](#known-issues "Link to this heading")

**1. Subqueries with FETCH first that are not uncorrelated scalar**

Oracle allows using the FETCH clause in subqueries, Snowflake only allows using this clause if the subquery is uncorrelated scalar, otherwise an exception will be generated.

SnowConvert AI will mark any inalid usage of FETCH in subqueries with [SSC-EWI-0108](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0108)

Oracle:

```
-- Correlated scalar
SELECT col2
FROM tableA
WHERE col2 = (SELECT col4 FROM tableB WHERE col3 = col1 FETCH FIRST ROW ONLY);

-- Uncorrelated scalar
SELECT col2
FROM tableA
WHERE col2 = (SELECT col4 FROM tableB FETCH FIRST ROW ONLY);
```

Copy

Snowflake:

```
-- Correlated scalar
SELECT col2
FROM
    tableA
    WHERE col2 =
                 --** SSC-FDM-0002 - CORRELATED SUBQUERIES MAY HAVE SOME FUNCTIONAL DIFFERENCES. **
                 !!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!! (SELECT
                         ANY_VALUE( col4) FROM
                         tableB
                     WHERE col3 = col1
                     FETCH FIRST 1 ROW ONLY);
 
 -- Uncorrelated scalar
SELECT col2
FROM
    tableA
    WHERE col2 = (SELECT col4 FROM
                         tableB
                     FETCH FIRST 1 ROW ONLY);
```

Copy

## Related EWIs[¶](#related-ewis "Link to this heading")

1. [SSC-FDM-0002](../../general/technical-documentation/issues-and-troubleshooting/functional-difference/generalFDM.html#ssc-fdm-0002): Correlated subquery may have functional differences
2. [SSC-EWI-0108](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0108): The following subquery matches at least one of the patterns considered invalid and may produce compilation errors

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
2. [Sample Source Patterns](#sample-source-patterns)
3. [Known Issues](#known-issues)
4. [Related EWIs](#related-ewis)