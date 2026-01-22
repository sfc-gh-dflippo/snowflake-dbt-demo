---
auto_generated: true
description: The SnowConvert AI Migration Assistant uses the Snowflake Cortex REST
  API, which incurs compute costs based on the number of tokens processed. You can
  view current rates in the Snowflake Service Consu
last_scraped: '2026-01-14T16:53:00.565751+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/migration-assistant/billing
title: SnowConvert AI - Migration Assistant - Billing | Snowflake Documentation
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

      * [SnowConvert AI](../overview.md)

        + General

          + [About](../general/about.md)
          + [Getting Started](../general/getting-started/README.md)
          + [Terms And Conditions](../general/terms-and-conditions/README.md)
          + [Release Notes](../general/release-notes/release-notes/README.md)
          + User Guide

            + [SnowConvert AI](../general/user-guide/snowconvert/README.md)
            + [Project Creation](../general/user-guide/project-creation.md)
            + [Extraction](../general/user-guide/extraction.md)
            + [Deployment](../general/user-guide/deployment.md)
            + [Data Migration](../general/user-guide/data-migration.md)
            + [Data Validation](../general/user-guide/data-validation.md)
            + [Power BI Repointing](../general/user-guide/power-bi-repointing-general.md)
            + [ETL Migration](../general/user-guide/etl-migration-replatform.md)
          + [Technical Documentation](../general/technical-documentation/README.md)
          + [Contact Us](../general/contact-us.md)
          + Others

            + [Using SnowConvert AI In A Ubuntu Docker Image](../general/others/using-snowconvert-in-a-ubuntu-docker-image.md)
          + [Frequently Asked Questions (FAQ)](../general/frequently-asked-questions-faq.md)")
        + Translation References

          + [General](../translation-references/general/README.md)
          + [Teradata](../translation-references/teradata/README.md)
          + [Oracle](../translation-references/oracle/README.md)
          + [SQL Server-Azure Synapse](../translation-references/transact/README.md)
          + [Sybase IQ](../translation-references/sybase/README.md)
          + [Hive-Spark-Databricks SQL](../translation-references/hive/README.md)
          + [Redshift](../translation-references/redshift/README.md)
          + [PostgreSQL-Greenplum-Netezza](../translation-references/postgres/README.md)
          + [BigQuery](../translation-references/bigquery/README.md)
          + [Vertica](../translation-references/vertica/README.md)
          + [IBM DB2](../translation-references/db2/README.md)
          + [SSIS](../translation-references/ssis/README.md)
        + [Migration Assistant](README.md)

          - [Getting Started](getting-started.md)
          - [Troubleshooting](troubleshooting.md)
          - [Billing](billing.md)
          - [Legal Notices](legal-notices.md)
        + [Data Validation CLI](../data-validation-cli/index.md)
        + [AI Verification](../snowconvert-ai-verification.md)
      * [Snowpark Migration Accelerator](../../sma-docs/README.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Migration Assistant](README.md)Billing

# SnowConvert AI - Migration Assistant - Billing[¶](#snowconvert-ai-migration-assistant-billing "Link to this heading")

The SnowConvert AI Migration Assistant uses the [Snowflake Cortex REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api), which incurs compute costs based on the number of tokens processed. You can view current rates in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf), and get more information on how to monitor LLM usage and costs in your account in the [Snowflake documentation for using Large Language Models](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#cost-considerations).

It’s not possible to precisely estimate the cost of a given interaction with the Migration Assistant because each response is custom-generated based on the code object you’re working on. A reasonable estimate for a common, one-cycle interaction to resolve an EWI is 3500 tokens. At current rates of 2.55 credits per million tokens, this results in 0.0089 credits used, at a cost of ~$0.027 for [Enterprise Edition in AWS, US East (Northern Virginia)](https://www.snowflake.com/en/pricing-options/). This is only an estimate, and it is possible for interactions to use significantly more tokens than this, especially if they involve multiple rounds of conversation with the LLM.

Since SnowConvert AI Migration Assistant is using Snowflake Cortex REST API, the only way to get the required information to estimate the costs of the requests executed is by consulting the [CORTEX\_ACCOUNT\_USAGE\_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/cortex_functions_usage_history) view by running the following query:

```
 SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY WHERE warehouse_id = 0 ORDER BY start_time DESC;
```

Copy

The provided query isolates requests made by the SnowConvert AI Migration Assistant by filtering for calls that did not use a virtual warehouse. This condition is effective because Cortex REST API calls are processed without a warehouse, allowing us to distinguish them from standard SQL-based queries.

Warning

**Limitation**: This query cannot distinguish between REST API calls made by the SnowConvert AI Migration Assistant and any other REST API calls executed by the same user. Consequently, if a user utilizes the Cortex REST API for other purposes, it will be impossible to isolate and attribute consumption specifically to this tool.

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