---
auto_generated: true
description: ''
last_scraped: '2026-01-14T16:52:04.083339+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/running-snowconvert/conversion/teradata-conversion-settings
title: SnowConvert AI - Teradata Conversion Settings | Snowflake Documentation
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

      * [SnowConvert AI](../../../../overview.md)

        + General

          + [About](../../../about.md)
          + [Getting Started](../../README.md)

            - [System Requirements](../../system-requirements.md)
            - [Best Practices](../../best-practices.md)
            - [Download And Access](../../download-and-access.md)
            - [Code Extraction](../../code-extraction/README.md)
            - [Running Snowconvert AI](../README.md)

              * [Supported Languages](../supported-languages/README.md)
              * [Validation](../validation/README.md)
              * [Conversion](README.md)

                + [SQL Server Conversion Settings](sql-server-conversion-settings.md)
                + [General Conversion Settings](general-conversion-settings.md)
                + [Converting Subfolders](converting-subfolders.md)
                + [Oracle Conversion Settings](oracle-conversion-settings.md)
                + [Teradata Conversion Settings](teradata-conversion-settings.md)
                + [Preview Features Settings](preview-conversion-settings.md)
              * [Review Results](../review-results/README.md)
            - [Training And Support](../../training-and-support.md)
          + [Terms And Conditions](../../../terms-and-conditions/README.md)
          + [Release Notes](../../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../../user-guide/snowconvert/README.md)
            + [Project Creation](../../../user-guide/project-creation.md)
            + [Extraction](../../../user-guide/extraction.md)
            + [Deployment](../../../user-guide/deployment.md)
            + [Data Migration](../../../user-guide/data-migration.md)
            + [Data Validation](../../../user-guide/data-validation.md)
            + [Power BI Repointing](../../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../../../technical-documentation/README.md)
          + [Contact Us](../../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../../translation-references/general/README.md)
          + [Teradata](../../../../translation-references/teradata/README.md)
          + [Oracle](../../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../../translation-references/hive/README.md)
          + [Redshift](../../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../../translation-references/postgres/README.md)
          + [BigQuery](../../../../translation-references/bigquery/README.md)
          + [Vertica](../../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../../translation-references/db2/README.md)
          + [SSIS](../../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../../data-validation-cli/index.md)
        + [AI Verification](../../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../../sma-docs/README.md)
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

[Guides](../../../../../../guides/README.md)[Migrations](../../../../../README.md)Tools[SnowConvert AI](../../../../overview.md)General[Getting Started](../../README.md)[Running Snowconvert AI](../README.md)[Conversion](README.md)Teradata Conversion Settings

# SnowConvert AI - Teradata Conversion Settings[¶](#snowconvert-ai-teradata-conversion-settings "Link to this heading")

## General Conversion Settings[¶](#general-conversion-settings "Link to this heading")

### General Result Settings[¶](#general-result-settings "Link to this heading")

![General Result Settings sub-page](../../../../../../_images/image%28531%29.png)

1. **Comment objects with missing dependencies:** Flag to indicate if the user wants to comment on nodes that have missing dependencies.
2. **Disable EWI comments generation (errors, warnings and issues):** Flag to indicate whether EWIs comments (Errors, Warnings, and Issues) will not be generated on the converted code. The default is false
3. **Generate XML-tags for SQL statements in Stored Procedures:** Flag to indicate whether the SQL statements SELECT, INSERT, CREATE, DELETE, UPDATE, DROP, MERGE in Stored Procedures will be tagged on the converted code. This feature is used for easy statement identification on the migrated code. Wrapping these statements within these XML-like tags allows for other programs to quickly find and extract them. The decorated code looks like this:

   ```
   //<SQL_DELETE
   EXEC(DELETE FROM SB_EDP_SANDBOX_LAB.PUBLIC.USER_LIST,[])
   //SQL_DELETE!>
   ```

   Copy
4. **Separate Period Data-type definitions and usages into begin and end Data-Time fields:** This flag is used to indicate that the tool should migrate any use of the PERIOD datatype as two separate DATETIME fields that will hold the original period begin and end values, anytime a period field or function is migrated using this flag SSC-EWI-TD0053 will be added to warn about this change.

   Input Code:

   ```
   CREATE TABLE myTable(
      col1 PERIOD(DATE),
      col2 VARCHAR(50),
      col3 PERIOD(TIMESTAMP)
   );
   ```

   Copy

   Output Code:

   ```
   CREATE OR REPLACE TABLE myTable (
      col1 VARCHAR(24) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!,
      col2 VARCHAR(50),
      col3 VARCHAR(58) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
   ;
   ```

   Copy
5. **Set encoding of the input files:** Check [General Conversion Settings](general-conversion-settings) for more details.
6. **Use COLLATE for Case Specification**: This flag indicates whether to use COLLATE or UPPER to preserve Case Specification functionality, e.g. CASESPECIFIC or NOT CASESPECIFIC. By default, it is turned off, meaning that the UPPER function will be used to emulate case insensitivity (NOT CASESPECIFIC). To learn more about how Case Specification is handled by SnowConvert AI check here.

Note

To review the Settings that apply to all supported languages, go to the following [article](general-conversion-settings).

### Session Mode Settings[¶](#session-mode-settings "Link to this heading")

This settings sub-page is used to indicate the Session Mode of the input code.

![Session Mode Settings sub-page](../../../../../../_images/image%28532%29.png)

SnowConvert AI handles Teradata code in both TERA and ANSI modes. Currently, this is limited to the default case specification of character data and how it affects comparisons. By default, the Session Mode is TERA.

You can learn more about how SnowConvert AI handles and converts code depending on the session mode, check here.

## DB Objects Names Settings[¶](#db-objects-names-settings "Link to this heading")

![DB Objects Names Settings page](../../../../../../_images/image%28407%29.png)

1. **Schema:** The string value specifies the custom schema name to apply. If not specified, the original database name will be used. Example: DB1.**myCustomSchema**.Table1.
2. **Database:** The string value specifies the custom database name to apply. Example: **MyCustomDB**.PUBLIC.Table1.
3. **Default:** None of the above settings will be used in the object names.

## Prepare Code Settings[¶](#prepare-code-settings "Link to this heading")

![Prepare Code Settings page](../../../../../../_images/image%28408%29.png)

### **Description**[¶](#description "Link to this heading")

**Prepare my code:** Flag to indicate whether the input code should be processed before parsing and transformation. This can be useful to improve the parsing process. By default, it’s set to FALSE.

Splits the input code top-level objects into multiple files. The containing folders would be organized as follows:

```
└───A new folder named ''[input_folder_name]_Processed''
    └───Top-level object type
        └───Schema name
```

Copy

### **Example**[¶](#example "Link to this heading")

#### **Input**[¶](#input "Link to this heading")

```
├───in
│       DDL_Macros.sql
│       DDL_Procedures.sql
│       DDL_Tables.sql
```

Copy

#### **Output**[¶](#output "Link to this heading")

Assume that the name of the files is the name of the top-level objects in the input files.

```
├───in_Processed
    ├───macro
    │   └───MY_DATABASE
    │           MY_FIRST_MACRO.sql
    │           ANOTHER_MACRO.sql
    │
    ├───procedure
    │   └───MY_DATABASE
    │           A_PROCEDURE.sql
    │           ANOTHER_PROCEDURE.sql
    │           YET_ANOTHER_PROCEDURE.sql
    │
    └───table
        └───MY_DATABASE
                MY_TABLE.sql
                ADDITIONAL_TABLE.sql
                THIRD_TABLE.sql
```

Copy

Inside the “schema name” folder, there should be as many files as top-level objects in the input code. Also, it is possible to have copies of some files when multiple same-type top-level objects have the same name. In this case, the file names will be enumerated in ascending order.

![](../../../../../../_images/image%28541%29.png)

Only files with the “.sql”, “.ddl” and “.dml” extensions will be considered for splitting. Other kinds of files like “.bteq” scripts will be copied into the preprocessed folder and will be categorized depending on the script extension but they won’t be modified by the Split Task.

### Requirements [¶](#requirements "Link to this heading")

To identify top-level objects, a tag must be included in a comment before their declaration. Our [Extraction](../../code-extraction/teradata) scripts generate these tags.

The tag should follow the next format:

```
<sc-top_level_object_type>top_level_object_name</sc-top_level_object_type>
```

Copy

You can follow the next example:

```
/* <sc-table> MY_DATABASE.MY_TABLE</sc-table> */
CREATE TABLE "MY_DATABASE"."MY_TABLE" (
    "MY_COLUMN" INTEGER
) ;
```

Copy

## Format Conversion Settings[¶](#format-conversion-settings "Link to this heading")

![Format Conversion Settings page](../../../../../../_images/image%28409%29.png)

1. **Character to Number default scale:** An integer value for the CHARACTER to Approximate Number transformation (Default: 10).
2. **Default TIMESTAMP format:** String value for the TIMESTAMP format (Default: “YYYY/MM/DD HH:MI:SS.FF6”).
3. **Default DATE format:** String value for the DATE format (Default: “YYYY/MM/DD”).
4. **Source TIMEZONE:** String value for the TIMEZONE format (Default: “GMT-5”).
5. **Default TIME format:** String value for the TIME format (Default: “HH:MI:SS.FF6”).

## Target Language for BTEQ, Procedures/Macros[¶](#target-language-for-bteq-procedures-macros "Link to this heading")

![BTEQ Target Language Settings page](../../../../../../_images/image%28410%29.png)

Specifies the target language to convert Bteq and Mload script files. Currently supported values are **SnowScript** and **Python**. The default value is set to **Python**.

![Procedures/Macros Target Language Settings page](../../../../../../_images/image%28411%29.png)

String value specifying the target language to convert Stored procedures and Macros. Currently supported are: **SnowScript** and **JavaScript**. The default value is set to **SnowScript**.

**Reset Settings:** The reset settings option appears on every page. If you’ve made changes, you can reset SnowConvert AI to its original default settings.

## Table translation[¶](#table-translation "Link to this heading")

Used to specify the type of tables that SnowConvert AI will output for table transformations, currently:

1. Snowflake-native tables
2. [Iceberg tables in Snowflake Horizon Catalog](../../../../translation-references/teradata/sql-translation-reference/Iceberg-tables-transformations)

Default is Snowflake-native tables.

The selected table type will be generated unless the source table is considered not compatible, the following criteria is applied for incompatible tables generation:

| Table type | Not compatible tables |
| --- | --- |
| Iceberg tables in Snowflake Horizon Catalog | Temporary tables (VOLATILE) |

Any table not compatible with the specified table type will not be affected by the setting and transformed to its default table type.

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

1. [General Conversion Settings](#general-conversion-settings)
2. [DB Objects Names Settings](#db-objects-names-settings)
3. [Prepare Code Settings](#prepare-code-settings)
4. [Format Conversion Settings](#format-conversion-settings)
5. [Target Language for BTEQ, Procedures/Macros](#target-language-for-bteq-procedures-macros)
6. [Table translation](#table-translation)