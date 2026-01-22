---
auto_generated: true
description: A subdivision of the SELECT statement done in IBM DB2.
last_scraped: '2026-01-14T16:53:09.315353+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/db2/db2-select-statement
title: SnowConvert AI - IBM DB2 - SELECT STATEMENT | Snowflake Documentation
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

              * [FROM Clause](db2-from-clause.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[IBM DB2](README.md)SELECT

# SnowConvert AI - IBM DB2 - SELECT STATEMENT[¶](#snowconvert-ai-ibm-db2-select-statement "Link to this heading")

## Description[¶](#description "Link to this heading")

> A subdivision of the SELECT statement done in IBM DB2.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=queries-fullselect) to navigate to the IBM DB2 documentation page for this syntax.

## Grammar Syntax[¶](#grammar-syntax "Link to this heading")

![image](../../../../_images/select_statement_overview.png)

## From Clause[¶](#from-clause "Link to this heading")

All information about this part of the syntax is specified on the [from-clause page](db2-from-clause).

## Where Clause[¶](#where-clause "Link to this heading")

> The WHERE clause specifies an intermediate result table that consists of those rows of R for which the search-condition is true. R is the result of the FROM clause of the subselect.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-where-clause) to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax[¶](#id1 "Link to this heading")

![image](../../../../_images/where_clause_syntax.png)

SuccessPlaceholder

All the grammar specified in this where clause of DB2 is ANSI compliant, equivalent to Snowflake, and is therefore translated as is by SnowConvert AI.

## Group By Clause[¶](#group-by-clause "Link to this heading")

> The GROUP BY clause specifies an intermediate result table that consists of a grouping of the rows of R. R is the result of the previous clause of the subselect.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-group-by-clause) to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax[¶](#id2 "Link to this heading")

![image](../../../../_images/group_by_clause_syntax.png)

### No explicit column reference[¶](#no-explicit-column-reference "Link to this heading")

> The following expressions, which do not contain an explicit column reference, can be used in a grouping-expression to identify a column of R:
>
> * ROW CHANGE TIMESTAMP FOR table-designator
> * ROW CHANGE TOKEN FOR table-designator
> * RID\_BIT or RID scalar function

ROW CHANGE Expressions and RID/RID\_BIT scalar functions are not supported in Snowflake.

#### Sample Source Patterns

##### IBM DB2

```
select * from product group by ROW CHANGE TIMESTAMP FOR product;
```

Copy

##### Snowflake

```
select * from
 product
--!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - GROUP BY ROW CHANGE TIMESTAMP FOR NOT SUPPORTED IN SNOWFLAKE ***/!!!
--group by ROW CHANGE TIMESTAMP FOR product
                                         ;
```

Copy

##### IBM DB2

```
    select * from product group by RID();
```

Copy

##### Snowflake

```
select * from
 product
--!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - GROUP BY scalar function RID NOT SUPPORTED IN SNOWFLAKE ***/!!!
--group by RID()
              ;
```

Copy

#### Related EWIs

1. [SSC-EWI-0021](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0021)

## Fetch Clause

### Description

> Sets a maximum number of rows to be retrieved.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-fetch-clause) to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax

![image](../../../../_images/fetch_clause_syntax.png)

### Sample Source Patterns

#### Fetch without row count

##### IBM DB2

```
 SELECT * FROM Product FETCH First Row ONLY;
/* or */
SELECT * FROM Product FETCH First Rows ONLY;
/* or */
SELECT * FROM Product FETCH Next Row ONLY;
/* or */
SELECT * FROM Product FETCH Next Rows ONLY;
```

Copy

###### Snowflake

```
SELECT * FROM
   Product
FETCH NEXT 1 ROW ONLY;
```

Copy

## Offset Clause

### Description

> Sets the number of rows to skip.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-offset-clause) to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax

![image](../../../../_images/offset_clause_syntax_1.png)

![image](../../../../_images/offset_clause_syntax_2.png)

### Sample Source Patterns

#### Offset row-count

##### IBM DB2

```
 SELECT * FROM Product OFFSET 3 ROW;
/* or */
SELECT * FROM Product OFFSET 3 ROWS;
```

Copy

##### Snowflake

```
SELECT * FROM
   Product
LIMIT NULL
OFFSET 3;
```

Copy

#### Limit X,Y

##### IBM DB2

```
SELECT * FROM Product LIMIT 3,2;
```

Copy

##### Snowflake

```
SELECT * FROM
   Product
OFFSET 3 ROWS
FETCH NEXT 2 ROWS ONLY;
```

Copy

## Order by Clause

### Description

> The ORDER BY clause specifies an ordering of the rows of the result table.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=subselect-order-by-clause) to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax

![image](../../../../_images/order_by_clause_syntax_1.png)

![image](../../../../_images/order_by_clause_syntax_2.png)

### Sample Source Patterns

The only paths of ORDER BY in Db2 that are not supported in Snowflake are those when it is used with ORDER OF and INPUT SEQUENCE; hence, if these are present, the clause will be marked with an EWI.

#### IBM DB2 Not Supported Examples

```
Select * from ORDERBYTest ORDER BY ORDER OF TableDesignator;
Select * from ORDERBYTest ORDER BY INPUT SEQUENCE;
```

Copy

##### Snowflake

```
Select * from
   ORDERBYTest
!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - ORDER BY ORDER OF NOT SUPPORTED IN SNOWFLAKE ***/!!!
ORDER BY ORDER OF TableDesignator;


Select * from
   ORDERBYTest
!!!RESOLVE EWI!!! /*** SSC-EWI-0021 - ORDER BY INPUT SEQUENCE NOT SUPPORTED IN SNOWFLAKE ***/!!!
ORDER BY INPUT SEQUENCE;
```

Copy

### Related EWIs

1. [SSC-EWI-0021](../../general/technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI.html#ssc-ewi-0021): NODE NOT SUPPORTED

## Values Clause

### Description

> Derives a result table by specifying the actual values, using expressions or row expressions, for each column of a row in the result table. hin

Note

The VALUES clause is not supported in Snowflake. For this reason, it is translated to a SELECT statement, as shown in the examples below.

### Grammar Syntax[¶](#id23 "Link to this heading")

![image](../../../../_images/values_clause_syntax.png)

### Sample Source Patterns[¶](#id24 "Link to this heading")

The Values clause is not supported in Snowflake. For this reason, the values clause is translated to a select query.

#### IBM DB2[¶](#id25 "Link to this heading")

```
VALUES 1, 2, 3
```

Copy

|  |
| --- |
| 1 |
| 2 |
| 3 |

##### Snowflake[¶](#id26 "Link to this heading")

```
SELECT 1, 2, 3
```

Copy

|  |  |  |
| --- | --- | --- |
| 1 | 2 | 3 |

For the values with multiple rows, a Union is used:

##### IBM DB2[¶](#id27 "Link to this heading")

```
VALUES (1, 1, 1),
    (2, 2, 2), 
    (3, 3, 3)
```

Copy

|  |  |  |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

##### Snowflake[¶](#id28 "Link to this heading")

```
SELECT
   1, 1, 1
UNION
SELECT
   2, 2, 2
UNION
SELECT
   3, 3, 3
```

Copy

|  |  |  |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

## Removed Clauses[¶](#removed-clauses "Link to this heading")

### Description[¶](#id29 "Link to this heading")

The following clauses are removed since they are not applicable in Snowflake:

* FOR READ ONLY
* Update Clause
* Optimize for Clause
* Concurrent access resolution Clause
* Isolation Clause

### Sample Source Patterns[¶](#id30 "Link to this heading")

#### IBM DB2[¶](#id31 "Link to this heading")

```
-- For Read Only
SELECT
   *
FROM
   Table1
FOR READ ONLY;


-- Update Clause
SELECT
   *
FROM
   Table1
FOR UPDATE OF
   COL1,
   COL2;


--Optimize For Clause
SELECT
   *
FROM
   Table1
OPTIMIZE FOR 2 ROWS;


-- Concurrent access resolution Clause
SELECT
   *
FROM
   Table1
WAIT FOR OUTCOME;


-- Isolation Clause
SELECT
   *
FROM
   Table1
WITH RR USE AND KEEP EXCLUSIVE LOCKS;
```

Copy

##### Snowflake[¶](#id32 "Link to this heading")

```
-- For Read Only
SELECT
   *
FROM
   Table1;


-- Update Clause
SELECT
   *
FROM
   Table1;


--Optimize For Clause
SELECT
   *
FROM
   Table1;


-- Concurrent access resolution Clause
SELECT
   *
FROM
   Table1;


-- Isolation Clause
SELECT
   *
FROM
   Table1;
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

1. [Description](#description)
2. [Grammar Syntax](#grammar-syntax)
3. [From Clause](#from-clause)
4. [Where Clause](#where-clause)
5. [Group By Clause](#group-by-clause)
6. [Fetch Clause](#)
7. [Offset Clause](#)
8. [Order by Clause](#)
9. [Values Clause](#)
10. [Removed Clauses](#removed-clauses)