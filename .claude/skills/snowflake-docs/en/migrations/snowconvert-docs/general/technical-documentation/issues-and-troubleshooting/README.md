---
auto_generated: true
description: SnowConvert AI produces messages in the converted code that highlight
  areas requiring additional work to ensure the code functions correctly in Snowflake.
last_scraped: '2026-01-14T16:52:34.994976+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/general/technical-documentation/issues-and-troubleshooting/README
title: SnowConvert AI - Understanding Converted Code | Snowflake Documentation
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

      * [SnowConvert AI](../../../overview.md)

        + General

          + [About](../../about.md)
          + [Getting Started](../../getting-started/README.md)
          + [Terms And Conditions](../../terms-and-conditions/README.md)
          + [Release Notes](../../release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../../user-guide/snowconvert/README.md)
            + [Project Creation](../../user-guide/project-creation.md)
            + [Extraction](../../user-guide/extraction.md)
            + [Deployment](../../user-guide/deployment.md)
            + [Data Migration](../../user-guide/data-migration.md)
            + [Data Validation](../../user-guide/data-validation.md)
            + [Power BI Repointing](../../user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../../user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../README.md)

            - [Considerations](../considerations/README.md)
            - [Issues And Troubleshooting](README.md)

              * [Conversion Issues](conversion-issues/README.md)
              * [Functional Difference](functional-difference/README.md)
              * [Out Of Scope](out-of-scope/README.md)
              * [Performance Review](performance-review/README.md)
            - Function References

              - [SnowConvert AI Udfs](../function-references/snowconvert-udfs.md)
              - [Teradata](../function-references/teradata/README.md)
              - [Oracle](../function-references/oracle/README.md)
              - [Shared](../function-references/shared/README.md)
              - [SQL Server](../function-references/sql-server/README.md)
          + [Contact Us](../../contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../../others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../../frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../../../translation-references/general/README.md)
          + [Teradata](../../../translation-references/teradata/README.md)
          + [Oracle](../../../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../../../translation-references/transact/README.md)
          + [Sybase IQ](../../../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../../../translation-references/hive/README.md)
          + [Redshift](../../../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../../../translation-references/postgres/README.md)
          + [BigQuery](../../../translation-references/bigquery/README.md)
          + [Vertica](../../../translation-references/vertica/README.md)
          + [IBM DB2](../../../translation-references/db2/README.md)
          + [SSIS](../../../translation-references/ssis/README.md)
        + [Migration Assistant](../../../migration-assistant/README.md)
        + [Data Validation CLI](../../../data-validation-cli/index.md)
        + [AI Verification](../../../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../../../sma-docs/README.md)
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

[Guides](../../../../../guides/README.md)[Migrations](../../../../README.md)Tools[SnowConvert AI](../../../overview.md)General[Technical Documentation](../README.md)Issues And Troubleshooting

# SnowConvert AI - Understanding Converted Code[¶](#snowconvert-ai-understanding-converted-code "Link to this heading")

## Definitions[¶](#definitions "Link to this heading")

SnowConvert AI produces messages in the converted code that highlight areas requiring additional work to ensure the code functions correctly in Snowflake.

### EWI (Errors, Warnings and Issues)[¶](#ewi-errors-warnings-and-issues "Link to this heading")

When SnowConvert AI cannot completely convert a code segment, it generates an Error, Warning, and Issue (EWI) message. Each EWI negatively affects the conversion rate of a code unit. Here are the common reasons why SnowConvert AI might not fully convert code:

* The required conversion rule has not been created yet
* Required dependent code is missing for the conversion rule to work
* An equivalent statement is not available in Snowflake, or a User-Defined Function (UDF) has not been developed to provide the needed functionality

SnowConvert AI adds a `!!!RESOLVE EWI!!!` marker before each EWI (Error, Warning, and Issue) message. This marker causes compilation to fail, ensuring that developers address these issues before deploying the converted code.

The SnowConvert AI team categorizes EWIs (Errors, Warnings, and Issues) into four severity levels based on the average effort required to fix the code:

* Low
* Medium
* High
* Critical

### FDM (Functional Difference Messages)[¶](#fdm-functional-difference-messages "Link to this heading")

When converting code from legacy platforms (such as Teradata, Oracle, or SQL Server) to Snowflake, it’s important to understand that these systems have different features and capabilities. Due to these differences, automatic conversion may not provide complete functional equivalence, and manual intervention is often necessary to address these gaps.

A Functional Difference Message (FDM) appears when SnowConvert AI successfully converts code that compiles correctly but may not function exactly like the original source code. This can happen when Snowflake doesn’t support certain features from the source platform. Resolving these differences often requires business decisions or architectural changes beyond simple code conversion. Since FDMs are added as comments to working code, they don’t affect the code’s ability to compile.

### PRF (Performance Review)[¶](#prf-performance-review "Link to this heading")

These warning messages are added to the converted code to inform users that although the code has been correctly translated, it may not perform optimally in certain situations. To achieve the best performance in Snowflake, some code modifications may be necessary.

### OOS (Out Of Scope)[¶](#oos-out-of-scope "Link to this heading")

As explained in the [conversion scope page](../../getting-started/running-snowconvert/review-results/snowconvert-scopes.html#conversion-scope) and the out of scope messages section, certain code units cannot be automatically converted. SnowConvert AI will generate messages to inform users when a code unit has not been converted.

---

## New Codes Format[¶](#new-codes-format "Link to this heading")

We have updated the format of Error, Warning, and Issue (EWI) messages to be more user-friendly. The new format makes it easier to identify both the message type and the programming language it relates to. Below, we’ll explain these changes with examples.

### General[¶](#general "Link to this heading")

General Errors, Warnings, and Issues (EWIs) that do not correspond to any specific programming language supported by SnowConvert AI will no longer use the code 1000. Instead, these EWIs will be identified by the absence of a language-specific abbreviation.

#### Example[¶](#example "Link to this heading")

| New Code | Old Code |
| --- | --- |
| SSC-EWI-0001 | MSCEWI1001 |

### Teradata[¶](#teradata "Link to this heading")

Teradata Errors, Warnings, and Issues (EWIs) previously used codes starting with 2000. Now, these codes will begin with ‘TD’ followed by the numeric portion.

#### Example[¶](#id1 "Link to this heading")

| New Code | Old Code |
| --- | --- |
| SSC-EWI-TD0001 | MSCEWI2001 |

### Oracle[¶](#oracle "Link to this heading")

Oracle Errors, Warnings, and Issues (EWIs) previously used codes starting with 3000. Now, these codes will begin with ‘OR’ followed by the numeric portion of the code.

#### Example[¶](#id2 "Link to this heading")

| New Code | Old Code |
| --- | --- |
| SSC-EWI-OR0012 | MSCEWI3012 |

### SQL Server[¶](#sql-server "Link to this heading")

SQL Server Errors, Warnings, and Issues (EWIs) codes have been updated. Previously, these codes started with 2000. Now, they begin with ‘TS’ followed by a numeric value.

#### Example[¶](#id3 "Link to this heading")

| New Code | Old Code |
| --- | --- |
| SSC-EWI-TS0003 | MSCEWI4003 |

## Changed Category To FDM[¶](#changed-category-to-fdm "Link to this heading")

| Dialect | New code | Old code |
| --- | --- | --- |
| General | SSC-FDM-0001 | MSCINF0001 |
| General | SSC-FDM-0002 | MSCINF0002 |
| General | SSC-FDM-0003 | MSCINF0003 |
| General | SSC-FDM-0004 | MSC-GP0001 |
| General | SSC-FDM-0005 | MSCEWI1096 |
| General | SSC-FDM-0006 | MSCEWI1066 |
| General | SSC-FDM-0007 | MSCEWI1050 |
| General | SSC-FDM-0008 | MSCEWI1093 |
| General | SSC-FDM-0009 | MSCCP0002 |
| General | SSC-FDM-0010 | MSCEWI1044 |
| General | SSC-FDM-0011 | MSCEWI1045 |
| General | SSC-FDM-0012 | MSCEWI1097 |
| General | SSC-FDM-0013 | MSCEWI1008 |
| General | SSC-FDM-0014 | MSCEWI1035 |
| General | SSC-FDM-0015 | MSCEWI1064 |
| General | SSC-FDM-0016 | MSCEWI1076 |
| General | SSC-FDM-0022 | MSCEWI1072 |
| General | SSC-FDM-0023 | SSC-EWI-0049 |
| General | SSC-FDM-0024 | MSCEWI1058 |
| General | SSC-FDM-0026 | MSCEWI1028 |
| General | SSC-FDM-0029 | SSC-EWI-0068 |
| Teradata | SSC-FDM-TD0001 | MSCEWI2013 |
| Teradata | SSC-FDM-TD0002 | MSCEWI2014 |
| Teradata | SSC-FDM-TD0003 | MSCEWI2073 |
| Teradata | SSC-FDM-TD0004 | MSCEWI2074 |
| Teradata | SSC-FDM-TD0005 | MSCEWI2058 |
| Teradata | SSC-FDM-TD0006 | MSCEWI2045 |
| Teradata | SSC-FDM-TD0007 | MSCEWI2018 |
| Teradata | SSC-FDM-TD0008 | MSCEWI2080 |
| Teradata | SSC-FDM-TD0009 | MSCEWI2019 |
| Teradata | SSC-FDM-TD0010 | MSCEWI2042 |
| Teradata | SSC-FDM-TD0011 | MSCEWI2064 |
| Teradata | SSC-FDM-TD0012 | MSCEWI2004 |
| Teradata | SSC-FDM-TD0013 | MSCEWI2075 |
| Teradata | SSC-FDM-TD0014 | MSCEWI2023 |
| Teradata | SSC-FDM-TD0015 | MSCEWI2020 |
| Teradata | SSC-FDM-TD0016 | MSCEWI2021 |
| Teradata | SSC-FDM-TD0018 | MSCEWI2063 |
| Teradata | SSC-FDM-TD0019 | MSCEWI2084 |
| Teradata | SSC-FDM-TD0020 | MSCEWI2062 |
| Teradata | SSC-FDM-TD0021 | MSCEWI2030 |
| Teradata | SSC-FDM-TD0022 | MSCEWI2086 |
| Teradata | SSC-FDM-TD0025 | MSCEWI2054 |
| Teradata | SSC-FDM-TD0026 | SSC-EWI-TD0087 |
| Teradata | SSC-FDM-TD0027 | MSCEWI2061 |
| Teradata | SSC-FDM-TD0028 | MSCEWI2060 |
| Teradata | SSC-FDM-TD0029 | SSC-EWI-TD0055 |
| Teradata | SSC-FDM-TD0030 | SSC-EWI-TD0070 |
| Oracle | SSC-FDM-OR0001 | MSCINF0004 |
| Oracle | SSC-FDM-OR0002 | MSCEWI3068 |
| Oracle | SSC-FDM-OR0003 | MSCEWI3038 |
| Oracle | SSC-FDM-OR0004 | MSCEWI3022 |
| Oracle | SSC-FDM-OR0005 | MSCEWI3025 |
| Oracle | SSC-FDM-OR0006 | MSCEWI3041 |
| Oracle | SSC-FDM-OR0007 | MSCEWI3056 |
| Oracle | SSC-FDM-OR0008 | MSCEWI3071 |
| Oracle | SSC-FDM-OR0009 | MSCEWI3086 |
| Oracle | SSC-FDM-OR0010 | MSCEWI3093 |
| Oracle | SSC-FDM-OR0011 | MSCEWI3066 |
| Oracle | SSC-FDM-OR0012 | MSCEWI3131 |
| Oracle | SSC-FDM-OR0013 | MSCEWI3039 |
| Oracle | SSC-FDM-OR0014 | MSCEWI3002 |
| Oracle | SSC-FDM-OR0015 | MSCEWI3091 |
| Oracle | SSC-FDM-OR0016 | MSCEWI3132 |
| Oracle | SSC-FDM-OR0017 | MSCEWI3017 |
| Oracle | SSC-FDM-OR0018 | MSCEWI3134 |
| Oracle | SSC-FDM-OR0019 | MSCEWI3086 |
| Oracle | SSC-FDM-OR0020 | MSCEWI3051 |
| Oracle | SSC-FDM-OR0021 | MSCEWI3102 |
| Oracle | SSC-FDM-OR0022 | MSCEWI3100 |
| Oracle | SSC-FDM-OR0023 | MSCEWI3099 |
| Oracle | SSC-FDM-OR0024 | MSCEWI3114 |
| Oracle | SSC-FDM-OR0025 | MSCEWI3021 |
| Oracle | SSC-FDM-OR0026 | MSCEWI1065 |
| Oracle | SSC-FDM-OR0025 | MSCEWI3098 |
| Oracle | SSC-FDM-OR0028 | MSCEWI3031 |
| Oracle | SSC-FDM-OR0029 | MSCEWI3059 |
| Oracle | SSC-FDM-OR0030 | MSCEWI3094 |
| Oracle | SSC-FDM-OR0031 | MSCEWI3113 |
| Oracle | SSC-FDM-OR0037 | MSCEWI3004 |
| Oracle | SSC-FDM-OR0038 | SSC-EWI-OR0128 |
| Oracle | SSC-FDM-OR0040 | SSC-EWI-OR0062 |
| Oracle | SSC-FDM-OR0043 | SSC-EWI-OR0005 |
| Oracle | SSC-FDM-OR0044 | SSC-EWI-OR0089 |
| Oracle | SSC-EWI-OR0039 | SSC-FDM-OR0013 |
| Oracle | SSC-FDM-OR0045 | SSC-EWI-OR0006 |
| SQL Server | SSC-FDM-TS0001 | MSCEWI4005 |
| SQL Server | SSC-FDM-TS0002 | MSCEWI4004 |
| SQL Server | SSC-FDM-TS0003 | MSCEWI4064 |
| SQL Server | SSC-FDM-TS0004 | MSCEWI4022 |
| SQL Server | SSC-FDM-TS0005 | MSCEWI4074 |
| SQL Server | SSC-FDM-TS0006 | MSCEWI4066 |
| SQL Server | SSC-FDM-TS0007 | MSCEWI4066 |
| SQL Server | SSC-FDM-TS0008 | MSCEWI4065 |
| SQL Server | SSC-FDM-TS0009 | MSCEWI4003 |
| SQL Server | SSC-FDM-TS0010 | MSCEWI4069 |
| SQL Server | SSC-FDM-TS0011 | MSCEWI1088 |
| SQL Server | SSC-FDM-TS0017 | SSC-EWI-TS0071 |
| SQL Server | SSC-FDM-TS0020 | SSC-EWI-TS0055 |

| Dialect | New code | Old code |
| --- | --- | --- |
| General | SSC-FDM-0001 | MSCINF0001 |
| General | SSC-FDM-0002 | MSCINF0002 |
| General | SSC-FDM-0003 | MSCINF0003 |
| General | SSC-FDM-0004 | MSC-GP0001 |
| General | SSC-FDM-0005 | MSCEWI1096 |
| General | SSC-FDM-0006 | MSCEWI1066 |
| General | SSC-FDM-0007 | MSCEWI1050 |
| General | SSC-FDM-OR0039 | MSCEWI1057 |
| General | SSC-FDM-0008 | MSCEWI1093 |
| General | SSC-FDM-0009 | MSCCP0002 |
| General | SSC-FDM-0010 | MSCEWI1044 |
| General | SSC-FDM-0011 | MSCEWI1045 |
| General | SSC-FDM-0012 | MSCEWI1097 |
| General | SSC-FDM-0013 | MSCEWI1008 |
| General | SSC-FDM-0014 | MSCEWI1035 |
| General | SSC-FDM-0015 | MSCEWI1064 |
| General | SSC-FDM-0016 | MSCEWI1076 |
| General | SSC-FDM-0022 | MSCEWI1072 |
| General | SSC-FDM-0024 | MSCEWI1058 |
| General | SSC-FDM-0026 | MSCEWI1028 |
| Teradata | SSC-FDM-TD0001 | MSCEWI2013 |
| Teradata | SSC-FDM-TD0002 | MSCEWI2014 |
| Teradata | SSC-FDM-TD0003 | MSCEWI2073 |
| Teradata | SSC-FDM-TD0004 | MSCEWI2074 |
| Teradata | SSC-FDM-TD0005 | MSCEWI2058 |
| Teradata | SSC-FDM-TD0006 | MSCEWI2045 |
| Teradata | SSC-FDM-TD0007 | MSCEWI2018 |
| Teradata | SSC-FDM-TD0008 | MSCEWI2080 |
| Teradata | SSC-FDM-TD0009 | MSCEWI2019 |
| Teradata | SSC-FDM-TD0010 | MSCEWI2042 |
| Teradata | SSC-FDM-TD0011 | MSCEWI2064 |
| Teradata | SSC-FDM-TD0012 | MSCEWI2004 |
| Teradata | SSC-FDM-TD0013 | MSCEWI2075 |
| Teradata | SSC-FDM-TD0014 | MSCEWI2023 |
| Teradata | SSC-FDM-TD0015 | MSCEWI2020 |
| Teradata | SSC-FDM-TD0016 | MSCEWI2021 |
| Teradata | SSC-FDM-TD0018 | MSCEWI2063 |
| Teradata | SSC-FDM-TD0019 | MSCEWI2084 |
| Teradata | SSC-FDM-TD0020 | MSCEWI2062 |
| Teradata | SSC-FDM-TD0021 | MSCEWI2030 |
| Teradata | SSC-FDM-TD0022 | MSCEWI2086 |
| Teradata | SSC-FDM-TD0025 | MSCEWI2054 |
| Teradata | SSC-FDM-TD0027 | MSCEWI2061 |
| Teradata | SSC-FDM-TD0028 | MSCEWI2060 |
| Oracle | SSC-FDM-OR0001 | MSCINF0004 |
| Oracle | SSC-FDM-OR0002 | MSCEWI3068 |
| Oracle | SSC-FDM-OR0003 | MSCEWI3038 |
| Oracle | SSC-FDM-OR0004 | MSCEWI3022 |
| Oracle | SSC-FDM-OR0005 | MSCEWI3025 |
| Oracle | SSC-FDM-OR0006 | MSCEWI3041 |
| Oracle | SSC-FDM-OR0007 | MSCEWI3056 |
| Oracle | SSC-FDM-OR0008 | MSCEWI3071 |
| Oracle | SSC-FDM-OR0009 | MSCEWI3086 |
| Oracle | SSC-FDM-OR0010 | MSCEWI3093 |
| Oracle | SSC-FDM-OR0011 | MSCEWI3066 |
| Oracle | SSC-FDM-OR0012 | MSCEWI3131 |
| Oracle | SSC-FDM-OR0013 | MSCEWI3039 |
| Oracle | SSC-FDM-OR0014 | MSCEWI3002 |
| Oracle | SSC-FDM-OR0015 | MSCEWI3091 |
| Oracle | SSC-FDM-OR0016 | MSCEWI3132 |
| Oracle | SSC-FDM-OR0017 | MSCEWI3017 |
| Oracle | SSC-FDM-OR0018 | MSCEWI3134 |
| Oracle | SSC-FDM-OR0019 | MSCEWI3086 |
| Oracle | SSC-FDM-OR0020 | MSCEWI3051 |
| Oracle | SSC-FDM-OR0021 | MSCEWI3102 |
| Oracle | SSC-FDM-OR0022 | MSCEWI3100 |
| Oracle | SSC-FDM-OR0023 | MSCEWI3099 |
| Oracle | SSC-FDM-OR0024 | MSCEWI3114 |
| Oracle | SSC-FDM-OR0025 | MSCEWI3021 |
| Oracle | SSC-FDM-OR0026 | MSCEWI1065 |
| Oracle | SSC-FDM-OR0025 | MSCEWI3098 |
| Oracle | SSC-FDM-OR0027 | MSCEWI3029 |
| Oracle | SSC-FDM-OR0028 | MSCEWI3031 |
| Oracle | SSC-FDM-OR0029 | MSCEWI3059 |
| Oracle | SSC-FDM-OR0030 | MSCEWI3094 |
| Oracle | SSC-FDM-OR0031 | MSCEWI3113 |
| Oracle | SSC-FDM-OR0038 | SSC-EWI-OR0128 |
| Oracle | SSC-FDM-OR0041 | MSCEWI307 |
| Oracle | SSC-FDM-OR0040 | SSC-EWI-OR0062 |
| SQL Server | SSC-FDM-TS0001 | MSCEWI4005 |
| SQL Server | SSC-FDM-TS0002 | MSCEWI4004 |
| SQL Server | SSC-FDM-TS0003 | MSCEWI4064 |
| SQL Server | SSC-FDM-TS0004 | MSCEWI4022 |
| SQL Server | SSC-FDM-TS0005 | MSCEWI4074 |
| SQL Server | SSC-FDM-TS0006 | MSCEWI4066 |
| SQL Server | SSC-FDM-TS0007 | MSCEWI4066 |
| SQL Server | SSC-FDM-TS0008 | MSCEWI4065 |
| SQL Server | SSC-FDM-TS0009 | MSCEWI4003 |
| SQL Server | SSC-FDM-TS0010 | MSCEWI4069 |
| SQL Server | SSC-FDM-TS0011 | MSCEWI1088 |
| SQL Server | SSC-FDM-TS0017 | SSC-EWI-TS0071 |
| SQL Server | SSC-FDM-TS0020 | SSC-EWI-TS0055 |

## Changed Category To PRF[¶](#changed-category-to-prf "Link to this heading")

| Dialect | New code | Old code |
| --- | --- | --- |
| General | SSC-PRF-0001 | MSCCP0005 |
| General | SSC-PRF-0002 | MSCCP0007 |
| General | SSC-PRF-0003 | MSCCP0006 |
| General | SSC-PRF-0004 | MSCCP0003 |
| General | SSC-PRF-0005 | MSCCP0010 |
| General | SSC-PRF-0006 | MSCCP0011 |
| Teradata | SSC-PRF-TD0001 | MSCEWI2008 |
| SQL Server | SSC-PRF-TS0001 | MSCEWI4007 |

## Deprecated EWIs[¶](#deprecated-ewis "Link to this heading")

| Dialect | Code |
| --- | --- |
| General | MSCEWI1008 |
| General | MSCEWI1016 |
| General | MSCEWI1017 |
| General | MSCEWI1019 |
| General | MSCEWI1029 |
| General | MSCEWI1055 |
| General | MSCEWI1037 |
| General | MSCEWI1042 |
| General | MSCEWI1043 |
| General | MSCEWI1048 |
| General | MSCEWI1059 |
| General | MSCEWI1069 |
| General | MSCEWI1074 |
| General | MSCEWI1079 |
| General | MSCEWI1081 |
| General | MSCEWI1082 |
| General | MSCEWI1083 |
| General | MSCEWI1085 |
| General | MSCEWI1087 |
| General | MSCEWI1089 |
| General | MSCEWI1090 |
| General | MSCEWI1091 |
| General | MSCEWI1097 |
| General | MSCEWI1098 |
| General | MSCEWI1099 |
| General | MSCEWI1108 |
| General | MSCINF0001 |
| General | MSCINF0002 |
| General | MSCINF0003 |
| Teradata | MSCEWI2002 |
| Teradata | MSCEWI2006 |
| Teradata | MSCEWI2007 |
| Teradata | MSCEWI2016 |
| Teradata | MSCEWI2018 |
| Teradata | MSCEWI2026 |
| Teradata | MSCEWI2028 |
| Teradata | MSCEWI2032 |
| Teradata | MSCEWI2033 |
| Teradata | MSCEWI2038 |
| Teradata | MSCEWI2044 |
| Teradata | MSCEWI2047 |
| Teradata | MSCEWI2050 |
| Teradata | MSCEWI2056 |
| Teradata | MSCEWI2065 |
| Teradata | MSCEWI2078 |
| Teradata | MSCEWI2081 |
| Teradata | MSCEWI2085 |
| Teradata | MSCEWI2088 |
| Teradata | MSCEWI2089 |
| Teradata | MSCEWI2090 |
| Oracle | MSCEWI3003 |
| Oracle | MSCEWI3007 |
| Oracle | MSCEWI3015 |
| Oracle | MSCEWI3019 |
| Oracle | MSCEWI3024 |
| Oracle | MSCEWI3027 |
| Oracle | MSCEWI3028 |
| Oracle | MSCEWI3037 |
| Oracle | MSCEWI3043 |
| Oracle | MSCEWI3044 |
| Oracle | MSCEWI3054 |
| Oracle | MSCEWI3058 |
| Oracle | MSCEWI3061 |
| Oracle | MSCEWI3063 |
| Oracle | MSCEWI3064 |
| Oracle | MSCEWI3065 |
| Oracle | MSCEWI3077 |
| Oracle | MSCEWI3083 |
| Oracle | MSCEWI3084 |
| Oracle | MSCEWI3085 |
| Oracle | MSCEWI3088 |
| Oracle | MSCEWI3096 |
| Oracle | MSCEWI3117 |
| Oracle | MSCEWI3119 |
| Oracle | MSCEWI3122 |
| Oracle | MSCEWI3125 |
| Oracle | SSC-EWI-OR0130 |
| SQL Server | MSCEWI4002 |
| SQL Server | MSCEWI4006 |
| SQL Server | MSCEWI4008 |
| SQL Server | MSCEWI4011 |
| SQL Server | MSCEWI4012 |
| SQL Server | MSCEWI4014 |
| SQL Server | MSCEWI4018 |
| SQL Server | MSCEWI4019 |
| SQL Server | MSCEWI4020 |
| SQL Server | MSCEWI4026 |
| SQL Server | MSCEWI4028 |
| SQL Server | MSCEWI4030 |
| SQL Server | MSCEWI4040 |
| SQL Server | MSCEWI4042 |
| SQL Server | MSCEWI4050 |
| SQL Server | MSCEWI4052 |
| SQL Server | MSCEWI4054 |
| SQL Server | MSCEWI4056 |
| SQL Server | MSCEWI4068 |
| SQL Server | SSC-EWI-TS0048 |

| Dialect | New code | Old code |
| --- | --- | --- |
| General | SSC-FDM-0001 | MSCINF0001 |
| General | SSC-FDM-0002 | MSCINF0002 |
| General | SSC-FDM-0003 | MSCINF0003 |
| General | SSC-FDM-0004 | MSC-GP0001 |
| General | SSC-FDM-0005 | MSCEWI1096 |
| General | SSC-FDM-0006 | MSCEWI1066 |
| General | SSC-FDM-0007 | MSCEWI1050 |
| General | SSC-FDM-OR0039 | MSCEWI1057 |
| General | SSC-FDM-0008 | MSCEWI1093 |
| General | SSC-FDM-0009 | MSCCP0002 |
| General | SSC-FDM-0010 | MSCEWI1044 |
| General | SSC-FDM-0011 | MSCEWI1045 |
| General | SSC-FDM-0012 | MSCEWI1097 |
| General | SSC-FDM-0013 | MSCEWI1008 |
| General | SSC-FDM-0014 | MSCEWI1035 |
| General | SSC-FDM-0015 | MSCEWI1064 |
| General | SSC-FDM-0016 | MSCEWI1076 |
| General | SSC-FDM-0022 | MSCEWI1072 |
| General | SSC-FDM-0023 | SSC-EWI-0049 |
| General | SSC-FDM-0024 | MSCEWI1058 |
| General | SSC-FDM-0026 | MSCEWI1028 |
| General | SSC-FDM-0029 | SSC-EWI-0068 |
| Teradata | SSC-FDM-TD0001 | MSCEWI2013 |
| Teradata | SSC-FDM-TD0002 | MSCEWI2014 |
| Teradata | SSC-FDM-TD0003 | MSCEWI2073 |
| Teradata | SSC-FDM-TD0004 | MSCEWI2074 |
| Teradata | SSC-FDM-TD0005 | MSCEWI2058 |
| Teradata | SSC-FDM-TD0006 | MSCEWI2045 |
| Teradata | SSC-FDM-TD0007 | MSCEWI2018 |
| Teradata | SSC-FDM-TD0008 | MSCEWI2080 |
| Teradata | SSC-FDM-TD0009 | MSCEWI2019 |
| Teradata | SSC-FDM-TD0010 | MSCEWI2042 |
| Teradata | SSC-FDM-TD0011 | MSCEWI2064 |
| Teradata | SSC-FDM-TD0013 | MSCEWI2075 |
| Teradata | SSC-FDM-TD0014 | MSCEWI2023 |
| Teradata | SSC-FDM-TD0016 | MSCEWI2021 |
| Teradata | SSC-FDM-TD0019 | MSCEWI2084 |
| Teradata | SSC-FDM-TD0020 | MSCEWI2062 |
| Teradata | SSC-FDM-TD0021 | MSCEWI2030 |
| Teradata | SSC-FDM-TD0022 | MSCEWI2086 |
| Teradata | SSC-FDM-TD0025 | MSCEWI2054 |
| Oracle | SSC-FDM-OR0001 | MSCINF0004 |
| Oracle | SSC-FDM-OR0004 | MSCEWI3022 |
| Oracle | SSC-FDM-OR0005 | MSCEWI3025 |
| Oracle | SSC-FDM-OR0006 | MSCEWI3041 |
| Oracle | SSC-FDM-OR0007 | MSCEWI3056 |
| Oracle | SSC-FDM-OR0009 | MSCEWI3086 |
| Oracle | SSC-FDM-OR0010 | MSCEWI3093 |
| Oracle | SSC-FDM-OR0011 | MSCEWI3066 |
| Oracle | SSC-FDM-OR0012 | MSCEWI3131 |
| Oracle | SSC-FDM-OR0013 | MSCEWI3039 |
| Oracle | SSC-FDM-OR0014 | MSCEWI3002 |
| Oracle | SSC-FDM-OR0015 | MSCEWI3091 |
| Oracle | SSC-FDM-OR0016 | MSCEWI3132 |
| Oracle | SSC-FDM-OR0017 | MSCEWI3017 |
| Oracle | SSC-FDM-OR0018 | MSCEWI3134 |
| Oracle | SSC-FDM-OR0019 | MSCEWI3086 |
| Oracle | SSC-FDM-OR0020 | MSCEWI3051 |
| Oracle | SSC-FDM-OR0021 | MSCEWI3102 |
| Oracle | SSC-FDM-OR0022 | MSCEWI3100 |
| Oracle | SSC-FDM-OR0023 | MSCEWI3099 |
| Oracle | SSC-FDM-OR0024 | MSCEWI3114 |
| Oracle | SSC-FDM-OR0025 | MSCEWI3021 |
| Oracle | SSC-FDM-OR0026 | MSCEWI1065 |
| Oracle | SSC-FDM-OR0025 | MSCEWI3098 |
| Oracle | SSC-FDM-OR0027 | MSCEWI3029 |
| Oracle | SSC-FDM-OR0029 | MSCEWI3059 |
| Oracle | SSC-FDM-OR0030 | MSCEWI3094 |
| Oracle | SSC-FDM-OR0031 | MSCEWI3113 |
| Oracle | SSC-FDM-OR0037 | MSCEWI3004 |
| Oracle | SSC-FDM-OR0041 | MSCEWI307 |
| Oracle | SSC-FDM-OR0040 | SSC-EWI-OR0062 |
| SQL Server | SSC-FDM-TS0001 | MSCEWI4005 |
| SQL Server | SSC-FDM-TS0002 | MSCEWI4004 |
| SQL Server | SSC-FDM-TS0003 | MSCEWI4064 |
| SQL Server | SSC-FDM-TS0004 | MSCEWI4022 |
| SQL Server | SSC-FDM-TS0005 | MSCEWI4074 |
| SQL Server | SSC-FDM-TS0006 | MSCEWI4066 |
| SQL Server | SSC-FDM-TS0007 | MSCEWI4066 |
| SQL Server | SSC-FDM-TS0008 | MSCEWI4065 |
| SQL Server | SSC-FDM-TS0009 | MSCEWI4003 |
| SQL Server | SSC-FDM-TS0010 | MSCEWI4069 |
| SQL Server | SSC-FDM-TS0011 | MSCEWI1088 |
| SQL Server | SSC-FDM-TS0017 | SSC-EWI-TS0071 |
| SQL Server | SSC-FDM-TS0019 | SSC-EWI-TS0047 |
| SQL Server | SSC-FDM-TS0020 | SSC-EWI-TS0055 |
| SQL Server | SSC-FDM-TS0021 | SSC-EWI-TS0056 |
| SQL Server | SSC-FDM-TS0022 | SSC-EWI-TS0057 |
| SQL Server | SSC-FDM-TS0023 | SSC-EWI-TS0073 |

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

1. [Definitions](#definitions)
2. [New Codes Format](#new-codes-format)
3. [Changed Category To FDM](#changed-category-to-fdm)
4. [Changed Category To PRF](#changed-category-to-prf)
5. [Deprecated EWIs](#deprecated-ewis)