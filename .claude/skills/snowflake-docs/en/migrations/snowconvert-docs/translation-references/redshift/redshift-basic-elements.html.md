---
auto_generated: true
description: Names and identifiers translation for Redshift
last_scraped: '2026-01-14T16:56:59.460596+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/redshift-basic-elements.html
title: SnowConvert AI - Redshift - Basic elements | Snowflake Documentation
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
          + [Redshift](README.md)

            - [Basic Elements](redshift-basic-elements.md)

              * [Literals](redshift-basic-elements-literals.md)
            - [Expressions](redshift-expressions.md)
            - [Conditions](redshift-conditions.md)
            - [Data types](redshift-data-types.md)
            - [SQL Statements](redshift-sql-statements.md)
            - [Functions](redshift-functions.md)
            - [System Catalog Tables](redshift-system-catalog.md)
            - ETL And BI Repointing

              - [Power BI Redshift Repointing](etl-bi-repointing/power-bi-redshift-repointing.md)
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

[Guides](../../../../guides/README.md)[Migrations](../../../README.md)Tools[SnowConvert AI](../../overview.md)Translation References[Redshift](README.md)Basic Elements

# SnowConvert AI - Redshift - Basic elements[¶](#snowconvert-ai-redshift-basic-elements "Link to this heading")

## Names and identifiers[¶](#names-and-identifiers "Link to this heading")

Names and identifiers translation for Redshift

### Description [¶](#description "Link to this heading")

> Names identify database objects, including tables and columns, as well as users and passwords. The terms *name* and *identifier* can be used interchangeably. There are two types of identifiers, standard identifiers and quoted or delimited identifiers. Identifiers must consist of only UTF-8 printable characters. ASCII letters in standard and delimited identifiers are case-insensitive and are folded to lowercase in the database. ([Redshift SQL Language reference Names and identifiers](https://docs.aws.amazon.com/redshift/latest/dg/r_names.html)).

### Standard identifiers [¶](#standard-identifiers "Link to this heading")

Standard SQL identifiers adhere to a set of rules and must:

* Begin with an ASCII single-byte alphabetic character or underscore character, or a UTF-8 multibyte character two to four bytes long.
* Subsequent characters can be ASCII single-byte alphanumeric characters, underscores, or dollar signs, or UTF-8 multibyte characters two to four bytes long.
* Be between 1 and 127 bytes in length, not including quotation marks for delimited identifiers.
* Contain no quotation marks and no spaces.
* Not be a reserved SQL keyword. ([Redshift SQL Language reference Standard identifiers](https://docs.aws.amazon.com/redshift/latest/dg/r_names.html#r_names-standard-identifiers))

Note

This syntax is fully supported by Snowflake.

### Special characters identifiers [¶](#special-characters-identifiers "Link to this heading")

In Redshift, there is support for using some special characters as part of the name of the identifier. These could be used in any part of an identifier. For this reason, to emulate this behavior, replace these unsupported special characters with a new value valid in Snowflake.

* The **#** character is replaced by a **\_H\_**.

Note

In Redshift, if you specify a table name that begins with **‘# ‘**, the table is created as a temporary table.

#### Sample Source Patterns[¶](#sample-source-patterns "Link to this heading")

##### Input Code:[¶](#input-code "Link to this heading")

##### Redshift[¶](#redshift "Link to this heading")

```
 CREATE TABLE #TABLE_NAME
(
    COL#1 int,
    "col2#" int
);

INSERT INTO #TABLE_NAME(COL#1, "col2#") VALUES (1,20),(2,21),(3,22);

SELECT col#1, "col2#" as col# FROM #TABLE_NAME;
```

Copy

##### Output Code:[¶](#output-code "Link to this heading")

##### Snowflake[¶](#snowflake "Link to this heading")

```
 CREATE TEMP TABLE _H_TABLE_NAME
(
	COL_H_1 int,
	"col2#" int
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/04/2025",  "domain": "test" }}';

INSERT INTO _H_TABLE_NAME (COL_H_1, "col2#") VALUES (1,20),(2,21),(3,22);

SELECT
	col_H_1,
	"col2#" as col_H_
FROM
	_H_TABLE_NAME;
```

Copy

### Delimited identifiers [¶](#delimited-identifiers "Link to this heading")

> Delimited identifiers (**also known as quoted identifiers**) begin and end with double quotation marks (“). If you use a delimited identifier, you must use the double quotation marks for every reference to that object. The identifier can contain any standard UTF-8 printable characters other than the double quotation mark itself. Therefore, you can create column or table names that include otherwise illegal characters, such as spaces or the percent symbol. ([Redshift SQL Language reference Delimited identifiers](https://docs.aws.amazon.com/redshift/latest/dg/r_names.html#r_names-delimited-identifiers)).

In Redshift, identifiers can be enclosed in quotes and are [not case-sensitive by default](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_case_sensitive_identifier.html). However, in Snowflake, they are [case-sensitive by default](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_case_sensitive_identifier.html). For this reason, to emulate this behavior, we are removing the quotes from all identifiers that are **enclosed in quotes, are not reserved keywords in Snowflake, and contain alphanumeric characters**. [**Reserved** **keywords**](#reserved-keywords) in Snowflake will always be enclosed in double quotes and defined in lowercase.

Warning

This change could impact the desired behavior if the [`enable_case_sensitive_identifier`](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_case_sensitive_identifier.html) flag is set to true in your configuration. Future updates will allow users to define the desired transformation for these identifiers.

#### Sample Source Patterns[¶](#id1 "Link to this heading")

For this scenario, please keep in mind that “LATERAL” and “INCREMENT” are reserved words in Snowflake, while “LOCAL” is not a reserved word.

##### Input Code:[¶](#id2 "Link to this heading")

##### Redshift[¶](#id3 "Link to this heading")

```
 CREATE TABLE lateral
(
    INCREMENT int,
    "local" int
);

INSERT INTO lateral(INCREMENT, "local") VALUES (1,20),(2,21),(3,22);

SELECT lateral.INCREMENT, "local" FROM LATERAL;
```

Copy

##### Result[¶](#result "Link to this heading")

| increment | local |
| --- | --- |
| 1 | 20 |
| 2 | 21 |
| 3 | 22 |

##### Output Code:[¶](#id4 "Link to this heading")

##### Snowflake[¶](#id5 "Link to this heading")

```
 CREATE TABLE "lateral"
(
    "increment" int,
    local int
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "12/10/2024",  "domain": "test" }}';

INSERT INTO "lateral" ("increment", local) VALUES (1,20),(2,21),(3,22);

SELECT
    "lateral"."increment",
    local
FROM
    "lateral";
```

Copy

##### Result[¶](#id6 "Link to this heading")

| increment | LOCAL |
| --- | --- |
| 1 | 20 |
| 2 | 21 |
| 3 | 22 |

### Quoted identifiers in Functions[¶](#quoted-identifiers-in-functions "Link to this heading")

In Redshift, function names can be enclosed in quotes and are [not case-sensitive by default](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_case_sensitive_identifier.html). However, in Snowflake, functions may cause issues if they are in quotes and written in lowercase. For this reason, in Snowflake, any function name enclosed in quotes will always be transformed to uppercase and the quotation marks will be removed.

#### Sample Source Patterns[¶](#id7 "Link to this heading")

##### Input Code:[¶](#id8 "Link to this heading")

##### Redshift[¶](#id9 "Link to this heading")

```
 SELECT "getdate"();
```

Copy

##### Result[¶](#id10 "Link to this heading")

| “GETDATE”() |
| --- |
| 2024-11-21 22:08:53.000000 |

##### Output Code:[¶](#id11 "Link to this heading")

##### Snowflake[¶](#id12 "Link to this heading")

```
 SELECT GETDATE();
```

Copy

##### Result[¶](#id13 "Link to this heading")

| “GETDATE”() |
| --- |
| 2024-11-21 22:08:53.000 +0000 |

#### Recommendations[¶](#recommendations "Link to this heading")

> To work around this limitation, Snowflake provides the [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](https://docs.snowflake.com/en/sql-reference/parameters.html#label-quoted-identifiers-ignore-case) session parameter, which causes Snowflake to treat lowercase letters in double-quoted identifiers as uppercase when creating and finding objects.
>
> ([Snowflake SQL Language Reference Identifier requirements](https://docs.snowflake.com/en/sql-reference/identifiers-syntax#migrating-from-databases-that-treat-double-quoted-identifiers-as-case-insensitive)).

## Reserved Keywords[¶](#reserved-keywords "Link to this heading")

Reserved keywords translation for Redshift

### Description[¶](#id14 "Link to this heading")

In Redshift you can use some of the [Snowflake reserved keywords](https://docs.snowflake.com/en/sql-reference/reserved-keywords) as column names, table names, etc. For this reason, it is necessary that these words are enclosed in double quotes in order to be able to use them.

Note

Please be aware that in Snowflake when these names are enclosed in double quotes, they are **case-sensitive**. For this reason It is important to emphasize that when a reserved keyword is used in Snowflake it is always transformed with double quotes and in lowercase. For more information please refer to [Snowflake identifiers documentation.](https://docs.snowflake.com/en/sql-reference/identifiers-syntax#label-delimited-identifier)

### Sample Source Patterns[¶](#id15 "Link to this heading")

#### Input Code:[¶](#id16 "Link to this heading")

##### Redshift[¶](#id17 "Link to this heading")

```
 CREATE TABLE alter
(
    alter INT
);

CREATE TABLE CONNECT
(
    CONNECT INT
);

DROP TABLE alter;
DROP TABLE CONNECT;
```

Copy

##### Output Code:[¶](#id18 "Link to this heading")

##### Snowflake[¶](#id19 "Link to this heading")

```
 CREATE TABLE "alter"
(
    "alter" INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';

CREATE TABLE "connect"
(
    "connect" INT
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';

DROP TABLE "alter";
DROP TABLE "connect";
```

Copy

### Related EWIs[¶](#related-ewis "Link to this heading")

No related EWIs.

### Known Issues [¶](#known-issues "Link to this heading")

No issues were found.

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

1. [Names and identifiers](#names-and-identifiers)
2. [Reserved Keywords](#reserved-keywords)