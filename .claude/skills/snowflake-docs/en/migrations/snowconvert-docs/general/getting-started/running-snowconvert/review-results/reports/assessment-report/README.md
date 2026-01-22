---
auto_generated: true
description: The purpose of this document is to provide guidance for users to understand
  the summary results from the SnowConvert AI conversion tools. It will guide through
  the different metrics returned and how t
last_scraped: '2026-01-14T16:52:19.785936+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/review-results/reports/assessment-report/README
title: SnowConvert AI - Assessment Report | Snowflake Documentation
---

1. [Overview](../../../../../../../../guides/README.md)
2. [Snowflake Horizon Catalog](../../../../../../../../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../../../../../../../guides/overview-connecting.md)
6. [Virtual warehouses](../../../../../../../../user-guide/warehouses.md)
7. [Databases, Tables, & Views](../../../../../../../../guides/overview-db.md)
8. [Data types](../../../../../../../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../../../../../../../../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../../../../../../../../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../../../../../../../../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../../../../../../../guides/overview-loading-data.md)
    - [Dynamic Tables](../../../../../../../../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../../../../../../../../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../../../../../../../../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../../../../../../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../../../../../../../../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../../../../../../README.md)

    * Tools

      * [SnowConvert AI](../../../../../../overview.md)

        + General

          + [About](../../../../../about.md)
          + [Getting Started](../../../../README.md)

            - [System Requirements](../../../../system-requirements.md)
            - [Best Practices](../../../../best-practices.md)
            - [Download And Access](../../../../download-and-access.md)
            - [Code Extraction](../../../../code-extraction/README.md)
            - [Running Snowconvert AI](../../../README.md)

              * [Supported Languages](../../../supported-languages/README.md)
              * [Validation](../../../validation/README.md)
              * [Conversion](../../../conversion/README.md)
              * [Review Results](../../README.md)

                + [SnowConvert AI Scopes](../../snowconvert-scopes.md)
                + [Output Code](../../output-code.md)
                + [Reports](../README.md)

                  - [Renaming Report](../renaming-reports.md)
                  - [Elements Report](../elements-report.md)
                  - [Functions Usage Report](../functions-usage-report.md)
                  - [Embedded Code Units Report](../embedded-code-units-report.md)
                  - [Assessment Report](README.md)

                    * [Object Conversion Summary](object-conversion-summary.md)
                    * [Scripts Files](scripts-files.md)
                    * [File And Object Level Breakdown SQL Files](file-and-object-level-breakdown-sql-files.md)
                    * [File And Object Level Breakdown SQL Identified Objects](file-and-object-level-breakdown-sql-identified-objects.md)
                    * [Schemas](schemas.md)
                    * [Databases And Schemas](databases-and-schemas.md)
                    * [Overall Conversion Summary](overall-conversion-summary.md)
                    * [Code Completeness Score](code-completeness-score.md)
                    * [SQL Conversion Summary](sql-conversion-summary.md)
                    * [Scripts Identified Objects](scripts-identified-objects.md)
                    * [Scripts Line Conversion Summary](scripts-line-conversion-summary.md)
                  - [Object References Report](../object-references-report.md)
                  - [Top Level Code Units Report](../top-level-code-units-report.md)
                  - [Missing Objects Report](../missing-objects-report.md)
                  - [Issues Report](../issues-report.md)
                  - [ETL Replatform Issues Report](../etl-replatform-issues-report.md)
                  - [ETL Replatform Component Summary Report](../etl-replatform-report.md)
                  - [TypeMappings Report](../type-mappings-report.md)
            - [Training And Support](../../../../training-and-support.md)
          + [Terms And Conditions](../../../../../terms-and-conditions/README.md)
          + [Release Notes](../../../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../../../user-guide/snowconvert/README.md)
            + [Project Creation](../../../../../user-guide/project-creation.md)
            + [Extraction](../../../../../user-guide/extraction.md)
            + [Deployment](../../../../../user-guide/deployment.md)
            + [Data Migration](../../../../../user-guide/data-migration.md)
            + [Data Validation](../../../../../user-guide/data-validation.md)
            + [Power BI Repointing](../../../../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../../../technical-documentation/README.md)
          + [Contact Us](../../../../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../../../../translation-references/general/README.md)
          + [Teradata](../../../../../../translation-references/teradata/README.md)
          + [Oracle](../../../../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../../../../translation-references/hive/README.md)
          + [Redshift](../../../../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../../../../translation-references/postgres/README.md)
          + [BigQuery](../../../../../../translation-references/bigquery/README.md)
          + [Vertica](../../../../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../../../../translation-references/db2/README.md)
          + [SSIS](../../../../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../../../../data-validation-cli/index.md)
        + [AI Verification](../../../../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../../../../sma-docs/README.md)
    * Guides

      * [Teradata](../../../../../../../guides/teradata.md)
      * [Databricks](../../../../../../../guides/databricks.md)
      * [SQL Server](../../../../../../../guides/sqlserver.md)
      * [Amazon Redshift](../../../../../../../guides/redshift.md)
      * [Oracle](../../../../../../../guides/oracle.md)
      * [Azure Synapse](../../../../../../../guides/azuresynapse.md)
15. [Queries](../../../../../../../../guides/overview-queries.md)
16. [Listings](../../../../../../../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../../../../../../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../../../../../../../guides/overview-ai-features.md)
21. [Snowflake Postgres](../../../../../../../../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](../../../../../../../../guides/overview-alerts.md)
25. [Security](../../../../../../../../guides/overview-secure.md)
26. [Data Governance](../../../../../../../../guides/overview-govern.md)
27. [Privacy](../../../../../../../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../../../../../../../guides/overview-manage.md)
30. [Business continuity & data recovery](../../../../../../../../user-guide/replication-intro.md)
32. [Performance optimization](../../../../../../../../guides/overview-performance.md)
33. [Cost & Billing](../../../../../../../../guides/overview-cost.md)

[Guides](../../../../../../../../guides/README.md)[Migrations](../../../../../../../README.md)Tools[SnowConvert AI](../../../../../../overview.md)General[Getting Started](../../../../README.md)[Running Snowconvert AI](../../../README.md)[Review Results](../../README.md)[Reports](../README.md)Assessment Report

# SnowConvert AI - Assessment Report[¶](#snowconvert-ai-assessment-report "Link to this heading")

## General Summary[¶](#general-summary "Link to this heading")

The purpose of this document is to provide guidance for users to understand the summary results from the SnowConvert AI conversion tools. It will guide through the different metrics returned and how these metrics can be used to determine the automation level achieved, and the amount of manual effort needed to make the output code into functionally equivalent Snowflake code.

![image](../../../../../../../../_images/image%28210%29.png)

Most of the concepts presented in this document are already explained on the Report’s main page. But here is some other helpful information about the most important information of the image above.

* **Total Parsing Errors**: The number of times that the conversion tool found text fragments that could not be recognized as syntactically correct elements for the source language under conversion. A parsing error could have a little or large impact. It is important to determine the number of LOC affected by parsing errors and how much they represent of the total workload. Sometimes parsing errors can occur due to encoding issues or because the workload needs some preparation.
* **Code Conversion Rate**: The conversion rate is the percentage of the total source code that was successfully converted by SnowConvert AI into functionally equivalent Snowflake code. Every time that the tool identifies not supported elements, *i.e,* fragments in the input source code that were not converted into Snowflake, this will affect the conversion rate.
* **Identified Objects**: The count of all the Top Level DDL Objects ( Table, View, Procedure, etc.. ) that the SnowConvert AI identified. If there were a parsing error on an object, it wouldn’t be an Identified Object.   
  Example: The [first objects](../../../../../technical-documentation/issues-and-troubleshooting/functional-difference/README) from line #1 to line #6. There is evidently a parsing error, so the SnowConvert AI cannot identify that as an object.

### Conversion rate modes[¶](#conversion-rate-modes "Link to this heading")

As mentioned before, when an element is marked as not supported (due to parsing errors or because there is no support for it in Snowflake) the conversion rate will be punished. How much of the conversion rate is punished for each not-supported element depends on the unit of code selected, two units are available: characters or lines.

#### Conversion rate using code characters[¶](#conversion-rate-using-code-characters "Link to this heading")

When characters of code are selected, the total amount of characters in the input source will represent the overall units to convert. So, if there are 100 characters total and there is only one not-supported element with 10 characters, the conversion rate will be **90%**. The conversion rate using characters is more precise because only the characters belonging to the not-supported elements are punished but, it is harder to manually calculate and understand.

#### Conversion rate using lines of code[¶](#conversion-rate-using-lines-of-code "Link to this heading")

When lines of code are chosen (default option), the number of lines of code in the input source code will represent the overall units to convert, and lines containing not-supported elements will be **entirely** considered as not-supported units of code. So, if the same input code with those 100 characters is split into 5 lines of code, and the not-supported element is in just one line, then the conversion rate will be **80%**; the **entire line** containing the not-supported element is considered not supported as well. The conversion rate using lines is easier to follow however, it is less accurate because entire lines of code containing not-supported elements are punished (even if there are other supported elements in that same line).

The next example shows how the conversion rate is calculated using both metrics.

### Conversion rate example[¶](#conversion-rate-example "Link to this heading")

**Input source code**

```
--Comment123
CREATE TABLE Table1(
 Prefix_Employee_Name CHAR(25),
 !ERROR_Col,
 Prefix_Employee_Sal DECIMAL(8))
```

Copy

The above code has exactly 100 code characters because whitespaces and line breaks are not considered code characters. The comment above `Table1` belongs to the table and is part of those 100 characters. This is the output code that SnowConvert AI generates for this input.

**Output source code**

```
--Comment123
CREATE OR REPLACE TABLE Table1 (
 Prefix_Employee_Name CHAR(25)
--                              ,
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '4' COLUMN '2' OF THE SOURCE CODE STARTING AT '!'. EXPECTED 'Column Definition' GRAMMAR. LAST MATCHING TOKEN WAS ',' ON LINE '3' COLUMN '31'. FAILED TOKEN WAS '!' ON LINE '4' COLUMN '2'. CODE '15'. **
-- !ERROR_Col
           ,
 Prefix_Employee_Sal DECIMAL(8))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;
```

Copy

The second column of the table has a parsing error and therefore this is a not-supported element. Let’s take a look a how the conversion rate is punished using the two units available.

#### Conversion rate using code characters[¶](#id1 "Link to this heading")

Here is the breakdown of the characters in the input code

```
--Comment123 /*12 code characters*/
CREATE TABLE Table1( /*18 code characters*/
 Prefix_Employee_Name CHAR(25), /*29 code characters*/
 !ERROR_Col, /*11 code characters*/
 Prefix_Employee_Sal DECIMAL(8)) /*30 code characters*/
```

Copy

* Total amount of code characters: 100
* Code characters in not-supported elements: 10
* **Result: 90.00%**

Note

Notice there are 11 characters in the 4th line but only 10 are marked as not supported. This is because of how the parsing recovery mechanism works. When the parser encounters an error, it will consider all the following characters, until the next delimiter character, in this case the comma (‘,’), as part of the error. That means that the amount of not-supported characters in any input code can greatly depend on the type of parsing errors. In some cases, the parser will be able to recover close to where the actual error is, but sadly in other cases, a lot of code can be swallowed by the error.

#### Conversion rate using lines of code[¶](#id2 "Link to this heading")

The conversion rate using lines of code as units is much simpler to calculate.

* Total amount of lines of code: 5
* Lines of code with not-supported elements: 1
* **Result: 80%**

#### LOC conversion rate depends on how the code is formatted[¶](#loc-conversion-rate-depends-on-how-the-code-is-formatted "Link to this heading")

When using lines of code as the unit, the conversion rate will greatly depend on how the input code is formatted. For example, the following two code samples are equivalent but in the first case all the code is put into the same line and in the second case the code is split into 5 lines of code

```
SELECT col1, !error_col FROM table1;
```
```none
SELECT
   col1,
   !error_col
 FROM
    table1;
```

Copy

Notice that the second column that is being referenced in the SELECT has an error because it starts with an invalid character. In the first case, since the whole code is in the same line, the conversion rate will be 0%. But in the second case, since the code is split, only one line of code is punished and therefore the conversion rate will be 80%.

### Conversion rate differences[¶](#conversion-rate-differences "Link to this heading")

There could be differences in the conversion results on the same migration between different operative systems.

This occurs because most of the time, Microsoft Windows uses CRLF line-breaking in their files. This format uses the characters `\r\n`, but UNIX OS only `\n`(LF).   
Due to that format difference, when our code processor is reading the input files, it will count the CRLF format as two characters and just one in LF files. These counting differences generate different results in the conversion rates, specifically, in string expressions present in your code.

To avoid this problem, you can use Visual Studio Code or similar tools to change the line-breaking format.

## File and Object-Level Breakdown[¶](#file-and-object-level-breakdown "Link to this heading")

### SQL - Files[¶](#sql-files "Link to this heading")

| File | Conversion Rate | Lines of Code | Total Object Quantity | Parsing Errors |
| --- | --- | --- | --- | --- |
| SQL | 42% | 20 | 2 | 3 |

In this section, you’ll get the overall assessment summary information for all the SQL Files

* **Code Conversion Rate**: This is an estimation of the conversion rate based on the characters of the given SQL Files.
* **Line of Code**: The count for the lines of code of the given SQL Files.
* **Total Object Quantity**: The count of total identified objects of the given SQL Files.
* **Parsing Errors**: The count of total parsing errors of the given SQL Files.

Warning

The Unrecognized objects will be counted also a parsing errors of the SQL Files section

Warning

The Code conversion rate may differ from Identified conversion rate because this is also considering the unrecognized objects.

### SQL - Identified Objects[¶](#sql-identified-objects "Link to this heading")

| Object | Conversion Rate | Lines of Code | Total Object Quantity | Parsing Errors |
| --- | --- | --- | --- | --- |
| Tables | 67% | 5 | 1 | 1 |
| Views | 57% | 7 | 1 | 1 |
| Procedures | - | 0 | 0 | 0 |
| Functions | N/A | N/A | N/A | N/A |

Note

If N/A is listed in the table above, it means that the object type is not supported in Snowflake, most likely due to architectural reasons. These objects are commented out in the generated code, and they do not punish the conversion rate.

Note

If the Conversion Rate field has a “-”, it means that the current set of files you have migrated didn’t contain any instance of the specified object.

In this section, you’ll get the assessment information for all the identified objects divided by the DDL objects like Tables, Views, Procedures, etc.

Warning

If there is a code where the parser couldn’t handle it, the entire object will be accounted as *Unrecognized Object,* and therefore it wouldn’t show here

* **Code Conversion Rate**: This is an estimation of the conversion rate based on the characters for the identified objects like Table, View, Procedure, etc.
* **Line of Code**: The count for the lines of code of each type of identified object.
* **Total Object Quantity**: The count for each type of identified object.
* **Parsing Errors**: The count for the parsing errors that occurred inside each type of identified object.

Example: For the 2 tables that we have in the [source code](../../../../../technical-documentation/issues-and-troubleshooting/functional-difference/README), one is an unrecognized object and one is succesfully identified. The conversion rate of that table of 5 lines of code is 75% due to 1 parsing error.

## Issues Breakdown[¶](#issues-breakdown "Link to this heading")

![Issues Breakdown table](../../../../../../../../_images/image%28291%29.png)

In this page, you will get the number of unique issues and the list of issues ordered by severity in descendant sort.‌

For example, for the given source code, we have 2 critical issues related to parsing errors and one medium severity issue related to the *Not supported function.*

Note

Only errors with Medium/High/Critical severity will affected the current conversion rate. Warnings are just informative.

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

1. [General Summary](#general-summary)
2. [File and Object-Level Breakdown](#file-and-object-level-breakdown)
3. [Issues Breakdown](#issues-breakdown)