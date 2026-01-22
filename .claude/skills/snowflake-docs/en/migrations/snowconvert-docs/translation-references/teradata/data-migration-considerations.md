---
auto_generated: true
description: This section describe important consideration when migration data from
  Teradata to Snowflake.
last_scraped: '2026-01-14T16:53:43.494555+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/data-migration-considerations
title: SnowConvert AI - Teradata - Data Migration Considerations | Snowflake Documentation
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
          + [Teradata](README.md)

            - [Data Migration Considerations](data-migration-considerations.md)
            - [Session Modes in Teradata](session-modes.md)
            - [Sql Translation Reference](sql-translation-reference/README.md)
            - [SQL to JavaScript (Procedures)](teradata-to-javascript-translation-reference.md)")
            - [SQL to Snowflake Scripting (Procedures)](teradata-to-snowflake-scripting-translation-reference.md)")
            - [Scripts To Python](scripts-to-python/README.md)
            - [Scripts to Snowflake SQL](scripts-to-snowflake-sql-translation-reference/README.md)
            - ETL And BI Repointing

              - [Power BI Teradata Repointing](etl-bi-repointing/power-bi-teradata-repointing.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Teradata](README.md)Data Migration Considerations

# SnowConvert AI - Teradata - Data Migration Considerations[¶](#snowconvert-ai-teradata-data-migration-considerations "Link to this heading")

This section describe important consideration when migration data from Teradata to Snowflake.

Note

Consider that this is a work in progress.

When migrating data from Teradata to Snowflake, it is crucial to consider the functional differences between the databases. This page showcases the best suggestions for migrating data.

Review the following information:

## UNION ALL Data Migration[¶](#union-all-data-migration "Link to this heading")

Data migration considerations for UNION ALL.

UNION ALL is a SQL operator that allows the combination of multiple resultsets. The syntax is the following:

```
 query_expression_1 UNION [ ALL ] query_expression_2
```

Copy

For more information, please review the following [Teradata](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Manipulation-Language/Set-Operators/UNION-Operator/UNION-Operator-Syntax) documentation.

### Column Size differences[¶](#column-size-differences "Link to this heading")

Even though the operator is translated into the same operator in Snowflake, there could be detailed differences in functional equivalence. For example, the union of different columns which have different column sizes. Teradata does truncate the values when the first SELECT statement contains less space in the columns.

#### Teradata behavior[¶](#teradata-behavior "Link to this heading")

Note

**Same behavior in ANSI and TERA session modes.**

For this example, the following input will show the Teradata behavior.

##### Teradata setup data[¶](#teradata-setup-data "Link to this heading")

```
 CREATE TABLE table1
(
col1 VARCHAR(20)
);

INSERT INTO table1 VALUES('value 1 abcdefghijk');
INSERT INTO table1 VALUES('value 2 abcdefghijk');

CREATE TABLE table2
(
col1 VARCHAR(10)
);

INSERT INTO table2 VALUES('t2 row 1 a');
INSERT INTO table2 VALUES('t2 row 2 a');
INSERT INTO table2 VALUES('t2 row 3 a');
```

Copy

##### Snowflake setup data[¶](#snowflake-setup-data "Link to this heading")

```
 CREATE OR REPLACE TABLE table1
(
col1 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table1
VALUES ('value 1 abcdefghijk');

INSERT INTO table1
VALUES ('value 2 abcdefghijk');

CREATE OR REPLACE TABLE table2
(
col1 VARCHAR(10)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table2
VALUES ('t2 row 1 a');

INSERT INTO table2
VALUES ('t2 row 2 a');

INSERT INTO table2
VALUES ('t2 row 3 a');
```

Copy

#### **Case 1 - one single column: UNION ALL for a column varchar (20) over a column varchar (10)**[¶](#case-1-one-single-column-union-all-for-a-column-varchar-20-over-a-column-varchar-10 "Link to this heading")

SuccessPlaceholder

For this case, the functional equivalence is the same

##### Teradata input[¶](#teradata-input "Link to this heading")

```
 SELECT col1 FROM table1
UNION ALL
SELECT col1 FROM table2;
```

Copy

##### Teradata output[¶](#teradata-output "Link to this heading")

```
value 1 abcdefghijk
t2 row 3 a
value 2 abcdefghijk
t2 row 1 a
t2 row 2 a
```

Copy

##### Snowflake input[¶](#snowflake-input "Link to this heading")

```
 SELECT
col1 FROM
table1
UNION ALL
SELECT
col1 FROM
table2;
```

Copy

##### Snowflake output[¶](#snowflake-output "Link to this heading")

```
value 1 abcdefghijk
t2 row 3 a
value 2 abcdefghijk
t2 row 1 a
t2 row 2 a
```

Copy

#### **Case 2 - one single column: UNION ALL for a column varchar (10) over a column varchar (20)**[¶](#case-2-one-single-column-union-all-for-a-column-varchar-10-over-a-column-varchar-20 "Link to this heading")

Danger

In this case, the function equivalence is not the same.

The following case does not show functional equivalence in Snowflake. The column values should be truncated as in the Teradata sample.

##### Teradata input[¶](#id1 "Link to this heading")

```
 SELECT col1 FROM table2
UNION ALL
SELECT col1 FROM table1;
```

Copy

##### Teradata output[¶](#id2 "Link to this heading")

```
t2 row 3 a
value 1 ab --> truncated
t2 row 1 a
t2 row 2 a
value 2 ab --> truncated
```

Copy

##### Snowflake input[¶](#id3 "Link to this heading")

```
 SELECT
col1 FROM
table2
UNION ALL
SELECT
col1 FROM
table1;
```

Copy

##### Snowflake output[¶](#id4 "Link to this heading")

```
t2 row 3 a
value 1 abcdefghijk --> NOT truncated
t2 row 1 a
t2 row 2 a
value 2 abcdefghijk --> NOT truncated
```

Copy

**Workaround to get the same functionality**

In this case, the size of the column of the `table2` is 10 and the `table1` is 20. So, the size of the first column in the query should be the element to complete the `LEFT()` function used here. Review more information about the Snowflake LEFT function [HERE](https://docs.snowflake.com/en/sql-reference/functions/left).

##### Snowflake input[¶](#id5 "Link to this heading")

```
 SELECT col1 FROM table2 -- size (10)
UNION ALL
SELECT LEFT(col1, 10) AS col1 FROM table1;
```

Copy

##### Snowflake output[¶](#id6 "Link to this heading")

```
t2 row 1 a
t2 row 2 a
t2 row 3 a
value 1 ab
value 2 ab
```

Copy

#### **Case 3 - multiple columns - same size by table: UNION ALL for columns varchar (20) over columns varchar (10)**[¶](#case-3-multiple-columns-same-size-by-table-union-all-for-columns-varchar-20-over-columns-varchar-10 "Link to this heading")

For this case, it is required to set up new data as follows:

##### Teradata setup data[¶](#id7 "Link to this heading")

```
 CREATE TABLE table3
(
col1 VARCHAR(20),
col2 VARCHAR(20)
);

INSERT INTO table3 VALUES('value 1 abcdefghijk', 'value 1 abcdefghijk');
INSERT INTO table3 VALUES('value 2 abcdefghijk', 'value 2 abcdefghijk');

CREATE TABLE table4
(
col1 VARCHAR(10),
col2 VARCHAR(10)
);

INSERT INTO table4 VALUES('t2 row 1 a', 't2 row 1 b');
INSERT INTO table4 VALUES('t2 row 2 a', 't2 row 2 b');
INSERT INTO table4 VALUES('t2 row 3 a', 't2 row 3 b');
```

Copy

##### Snowflake setup data[¶](#id8 "Link to this heading")

```
 CREATE OR REPLACE TABLE table3
(
col1 VARCHAR(20),
col2 VARCHAR(20)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table3
VALUES ('value 1 abcdefghijk', 'value 1 abcdefghijk');

INSERT INTO table3
VALUES ('value 2 abcdefghijk', 'value 2 abcdefghijk');

CREATE OR REPLACE TABLE table4
(
col1 VARCHAR(10),
col2 VARCHAR(10)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table4
VALUES ('t2 row 1 a', 't2 row 1 b');

INSERT INTO table4
VALUES ('t2 row 2 a', 't2 row 2 b');

INSERT INTO table4
VALUES ('t2 row 3 a', 't2 row 3 b');
```

Copy

Once the new tables and data are created, the following query can be evaluated.

Note

For this case, the functional equivalence is the same

##### Teradata input[¶](#id9 "Link to this heading")

```
 select col1, col2 from table3
union all
select col1, col2 from table4;
```

Copy

##### Teradata output[¶](#id10 "Link to this heading")

| col1 | col2 |
| --- | --- |
| value 1 abcdefghijk | value 1 abcdefghijk |
| t2 row 3 a | t2 row 3 b |
| value 2 abcdefghijk | value 2 abcdefghijk |
| t2 row 1 a | t2 row 1 b |
| t2 row 2 a | t2 row 2 b |

##### Snowflake input[¶](#id11 "Link to this heading")

```
 SELECT
col1, col2 FROM
table3
UNION ALL
SELECT
col1, col2 FROM
table4;
```

Copy

##### Snowflake output[¶](#id12 "Link to this heading")

| col1 | col2 |
| --- | --- |
| value 1 abcdefghijk | value 1 abcdefghijk |
| value 2 abcdefghijk | value 2 abcdefghijk |
| t2 row 1 a | t2 row 1 b |
| t2 row 2 a | t2 row 2 b |
| t2 row 3 a | t2 row 3 b |

#### Case 4 - multiple columns - same size by table: UNION ALL for columns varchar (10) over columns varchar (20)[¶](#case-4-multiple-columns-same-size-by-table-union-all-for-columns-varchar-10-over-columns-varchar-20 "Link to this heading")

Warning

In this case, the function equivalence is not the same.

##### Teradata input[¶](#id13 "Link to this heading")

```
 select col1, col2 from table4
union all
select col1, col2 from table3;
```

Copy

##### Teradata output[¶](#id14 "Link to this heading")

| col1 | col2 |
| --- | --- |
| t2 row 3 a | t2 row 3 b |
| value 1 ab | value 1 ab |
| t2 row 1 a | t2 row 1 b |
| t2 row 2 a | t2 row 2 b |
| value 2 ab | value 2 ab |

##### Snowflake input[¶](#id15 "Link to this heading")

```
 SELECT
col1, col2 FROM
table4
UNION ALL
SELECT
col1, col2 FROM
table3;
```

Copy

##### Snowflake output[¶](#id16 "Link to this heading")

| col1 | col2 |
| --- | --- |
| t2 row 1 a | t2 row 1 b |
| t2 row 2 a | t2 row 2 b |
| t2 row 3 a | t2 row 3 b |
| value 1 abcdefghijk | value 1 abcdefghijk |
| value 2 abcdefghijk | value 2 abcdefghijk |

**Workaround to get the same functionality**

Apply the column size to the second `SELECT` on the columns to get the same functionality.

##### Snowflake input[¶](#id17 "Link to this heading")

```
 SELECT col1, col2 FROM table4 -- size (10)
UNION ALL
SELECT LEFT(col1, 10) AS col1, LEFT(col2, 10) AS col2 FROM table3;
```

Copy

##### Snowflake output[¶](#id18 "Link to this heading")

| col1 | col2 |
| --- | --- |
| t2 row 1 a | t2 row 1 b |
| t2 row 2 a | t2 row 2 b |
| t2 row 3 a | t2 row 3 b |
| value 1 ab | value 1 ab |
| value 2 ab | value 2 ab |

#### Case 5 - multiple columns - different sizes by table: UNION ALL for columns varchar (10) over columns varchar (20)[¶](#case-5-multiple-columns-different-sizes-by-table-union-all-for-columns-varchar-10-over-columns-varchar-20 "Link to this heading")

For this case, it is required to set up new data as follows:

##### Teradata setup data[¶](#id19 "Link to this heading")

```
 CREATE TABLE table5
(
col1 VARCHAR(20),
col2 VARCHAR(12)
);

INSERT INTO table5 VALUES('value 1 abcdefghijk', 'value 1 abcdefghijk');
INSERT INTO table5 VALUES('value 2 abcdefghijk', 'value 2 abcdefghijk');

CREATE TABLE table6
(
col1 VARCHAR(10),
col2 VARCHAR(5)
);

INSERT INTO table6 VALUES('t2 row 1 a', 't2 row 1 b');
INSERT INTO table6 VALUES('t2 row 2 a', 't2 row 2 b');
INSERT INTO table6 VALUES('t2 row 3 a', 't2 row 3 b');
```

Copy

##### Snowflake setup data[¶](#id20 "Link to this heading")

```
 CREATE OR REPLACE TABLE table5
(
col1 VARCHAR(20),
col2 VARCHAR(12)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table5
VALUES ('value 1 abcdefghijk', 'value 1 abcd');

INSERT INTO table5
VALUES ('value 2 abcdefghijk', 'value 2 abcd');

CREATE OR REPLACE TABLE table6
(
col1 VARCHAR(10),
col2 VARCHAR(5)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "10/14/2024" }}'
;

INSERT INTO table6
VALUES ('t2 row 1 a', 't2 1b');

INSERT INTO table6
VALUES ('t2 row 2 a', 't2 2b');

INSERT INTO table6
VALUES ('t2 row 3 a', 't2 3b');
```

Copy

Once the new tables and data are created, the following query can be evaluated.

Note

For this case, the functional equivalence is the same

##### Teradata input[¶](#id21 "Link to this heading")

```
 select col1, col2 from table5
union all
select col1, col2 from table6;
```

Copy

##### Teradata output[¶](#id22 "Link to this heading")

| col1 | col2 |
| --- | --- |
| value 1 abcdefghijk | value 1 abcd |
| t2 row 3 a | t2 3b |
| value 2 abcdefghijk | value 2 abcd |
| t2 row 1 a | t2 1b |
| t2 row 2 a | t2 2b |

##### Snowflake input[¶](#id23 "Link to this heading")

```
 SELECT
col1, col2 FROM
table5
UNION ALL
SELECT
col1, col2 FROM
table6;
```

Copy

##### Snowflake output[¶](#id24 "Link to this heading")

| col1 | col2 |
| --- | --- |
| value 1 abcdefghijk | value 1 abcd |
| value 2 abcdefghijk | value 2 abcd |
| t2 row 1 a | t2 1b |
| t2 row 2 a | t2 2b |
| t2 row 3 a | t2 3b |

#### Case 6 - multiple columns - different sizes by table: UNION ALL for columns varchar (20), varchar(10) over columns varchar (10), varchar(5)[¶](#case-6-multiple-columns-different-sizes-by-table-union-all-for-columns-varchar-20-varchar-10-over-columns-varchar-10-varchar-5 "Link to this heading")

Warning

In this case, the function equivalence is not the same.

##### Teradata input[¶](#id25 "Link to this heading")

```
 select col1, col2 from table6
union all
select col1, col2 from table5;
```

Copy

##### Teradata output[¶](#id26 "Link to this heading")

| col1 | col2 |
| --- | --- |
| t2 row 3 a | t2 3b |
| **value 1 ab** | **value** |
| t2 row 1 a | t2 1b |
| t2 row 2 a | t2 2b |
| **value 2 ab** | **value** |

##### Snowflake input[¶](#id27 "Link to this heading")

```
 SELECT
col1, col2 FROM
table6
UNION ALL
SELECT
col1, col2 FROM
table5;
```

Copy

##### Snowflake output[¶](#id28 "Link to this heading")

| col1 | col2 |
| --- | --- |
| t2 row 1 a | t2 1b |
| t2 row 2 a | t2 2b |
| t2 row 3 a | t2 3b |
| **value 1 abcdefghijk** | **value 1 abcd** |
| **value 2 abcdefghijk** | **value 2 abcd** |

**Workaround to get the same functionality**

The column with the smallest size from the first `SELECT` is used to determine the size of the columns from the second `SELECT`.

##### Snowflake input[¶](#id29 "Link to this heading")

```
 SELECT
col1, col2 FROM
table6
UNION ALL
SELECT
LEFT(col1, 5) as col1, LEFT(col2, 5) AS col2 FROM
table5;
```

Copy

##### Snowflake output[¶](#id30 "Link to this heading")

| col1 | col2 |
| --- | --- |
| t2 row 3 a | t2 3b |
| **value 1 ab** | **value** |
| t2 row 1 a | t2 1b |
| t2 row 2 a | t2 2b |
| **value 2 ab** | **value** |

#### Case 7 - multiple columns *expression* - different sizes by table: UNION ALL for columns varchar (20), varchar(20) over columns varchar (10), varchar(10)[¶](#case-7-multiple-columns-expression-different-sizes-by-table-union-all-for-columns-varchar-20-varchar-20-over-columns-varchar-10-varchar-10 "Link to this heading")

Use the data set up [here](#case-3-multiple-columns-same-size-by-table-union-all-for-columns-varchar-20-over-columns-varchar-10). Once the new tables and data are created, the following query can be evaluated.

Note

For this case, the functional equivalence is the same

##### Teradata input[¶](#id31 "Link to this heading")

```
 select col1 || col2 from table3
union all
select col1 || col2 from table4;
```

Copy

##### Teradata output[¶](#id32 "Link to this heading")

| col1 || col2 |
| --- |
| value 1 abcdefghijkvalue 1 abcdefghijk |
| t2 row 3 at2 row 3 b |
| value 2 abcdefghijkvalue 2 abcdefghijk |
| t2 row 1 at2 row 1 b |
| t2 row 2 at2 row 2 b |

##### Snowflake input[¶](#id33 "Link to this heading")

```
 SELECT
col1 || col2 FROM
table3
UNION ALL
SELECT
col1 || col2 FROM
table4;
```

Copy

##### Snowflake output[¶](#id34 "Link to this heading")

| col1 || col2 |
| --- |
| value 1 abcdefghijkvalue 1 abcdefghijk |
| value 2 abcdefghijkvalue 2 abcdefghijk |
| t2 row 1 at2 row 1 b |
| t2 row 2 at2 row 2 b |
| t2 row 3 at2 row 3 b |

#### Case 8 - multiple columns *expression* - different sizes by table: UNION ALL for columns varchar (20), varchar(20) over columns varchar (10), varchar(10)[¶](#case-8-multiple-columns-expression-different-sizes-by-table-union-all-for-columns-varchar-20-varchar-20-over-columns-varchar-10-varchar-10 "Link to this heading")

Warning

This case has functional differences.

##### Teradata input[¶](#id35 "Link to this heading")

```
 select col1 || col2 from table4
union all
select col1 || col2 from table3;
```

Copy

##### Teradata output[¶](#id36 "Link to this heading")

| col1 || col2 |
| --- |
| t2 row 1 at2 row 1 b |
| t2 row 2 at2 row 2 b |
| t2 row 3 at2 row 3 b |
| value 1 abcdefghijkv |
| value 2 abcdefghijkv |

##### Snowflake input[¶](#id37 "Link to this heading")

```
 SELECT
col1 || col2 FROM
table4
UNION ALL
SELECT
col1 || col2 FROM
table3;
```

Copy

##### Snowflake output[¶](#id38 "Link to this heading")

| col1 || col2 |
| --- |
| t2 row 1 at2 row 1 b |
| t2 row 2 at2 row 2 b |
| t2 row 3 at2 row 3 b |
| value 1 abcdefghijkvalue 1 abcdefghijk |
| value 2 abcdefghijkvalue 2 abcdefghijk |

**Workaround to get the same functionality**

The sum of the column sizes of the less big column should be used in the `LEFT` function. For example, the less big column is varchar(10), so the limit of the `LEFT` function should be 20 (10 + 10).

Warning

The sum of the first `SELECT` if this is less big, it would be used for the truncation of the values.

##### Snowflake input[¶](#id39 "Link to this heading")

```
 SELECT
col1 || col2 FROM
table4
UNION ALL
SELECT
LEFT(col1 || col2, 20) FROM
table3;
```

Copy

##### Snowflake output[¶](#id40 "Link to this heading")

| col1 || col2 |
| --- |
| t2 row 1 at2 row 1 b |
| t2 row 2 at2 row 2 b |
| t2 row 3 at2 row 3 b |
| value 1 abcdefghijkv |
| value 2 abcdefghijkv |

#### Other considerations about column size differences[¶](#other-considerations-about-column-size-differences "Link to this heading")

* `CHAR` and `VARCHAR` behave the same.
* Number columns may behave differently. The numbers cannot be truncated, so there is an overflow in the Teradata environment. So, this is not applied to these data types. Review the following example:

```
-- Teradata number sample 
CREATE TABLE table11
(
col1 NUMBER(2)
);

INSERT INTO table11 VALUES(10);
INSERT INTO table11 VALUES(10);

CREATE TABLE table12
(
col1 NUMBER(1)
);

INSERT INTO table12 VALUES(1);
INSERT INTO table12 VALUES(1);
INSERT INTO table12 VALUES(1);

-- ERROR!  Overflow occurred when computing an expression involving table11.col1
SELECT col1 FROM table12
UNION ALL
SELECT col1 FROM table11;
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

1. [UNION ALL Data Migration](#union-all-data-migration)