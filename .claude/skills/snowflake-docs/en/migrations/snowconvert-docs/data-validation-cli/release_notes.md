---
auto_generated: true
description: 'New Command: column-partitioning-helper - Interactive helper to partition
  wide tables by columns for more efficient validation of tables with many columns'
last_scraped: '2026-01-14T16:52:14.482868+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/release_notes
title: Release Notes - Snowflake Data Validation CLI | Snowflake Documentation
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
        + [Migration Assistant](../migration-assistant/README.md)
        + [Data Validation CLI](index.md)

          - [Quick reference](CLI_QUICK_REFERENCE.md)
          - [Usage Guide](CLI_USAGE_GUIDE.md)
          - [Configuration Examples](CONFIGURATION_EXAMPLES.md)
          - [Release Notes](release_notes.md)
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

[Guides](../../../guides/README.md)[Migrations](../../README.md)Tools[SnowConvert AI](../overview.md)[Data Validation CLI](index.md)Release Notes

# Release Notes - Snowflake Data Validation CLI[¶](#release-notes-snowflake-data-validation-cli "Link to this heading")

## Version 1.0.2 (December 2025)[¶](#version-1-0-2-december-2025 "Link to this heading")

### What’s New[¶](#what-s-new "Link to this heading")

* **New Command:** `column-partitioning-helper` - Interactive helper to partition wide tables by columns for more efficient validation of tables with many columns

### Changes[¶](#changes "Link to this heading")

* **Command Renamed:** `table-partitioning-helper` has been renamed to `row-partitioning-helper` for improved clarity on its purpose

---

## Version 1.0.1 (December 2025)[¶](#version-1-0-1-december-2025 "Link to this heading")

### What’s New[¶](#id1 "Link to this heading")

This release introduces an enhancement to improve the CLI user experience whenaccessing help documentation.

### Example[¶](#example "Link to this heading")

```
# These commands no longer create log files
sdv --help
sdv sqlserver --help
sdv sqlserver run-validation --help

# These commands still create log files normally
sdv sqlserver run-validation --data-validation-config-file config.yaml
```

Copy

---

## Documentation[¶](#documentation "Link to this heading")

For complete information about using the Snowflake Data Validation CLI, refer to:

* **[Documentation Index](index)** - Start here for navigation to all documentation
* **[CLI Usage Guide](CLI_USAGE_GUIDE)** - Comprehensive CLI documentation
* **[Quick Reference Guide](CLI_QUICK_REFERENCE)** - Fast lookup reference
* **[Configuration Examples](CONFIGURATION_EXAMPLES)** - Ready-to-use configuration examples
* **[SQL Server Commands](sqlserver_commands)** - SQL Server specific commands
* **[Teradata Commands](teradata_commands)** - Teradata specific commands
* **[Redshift Commands](redshift_commands)** - Redshift specific commands

---

## Support[¶](#support "Link to this heading")

If you encounter any issues or have questions:

* **Email:** [snowconvert-support@snowflake.com](mailto:snowconvert-support%40snowflake.com)
* **Documentation:** [Full Documentation](https://github.com/snowflakedb/migrations-data-validation)
* **Issues:** [GitHub Issues](https://github.com/snowflakedb/migrations-data-validation/issues)

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [Version 1.0.2 (December 2025)](#version-1-0-2-december-2025)
2. [Version 1.0.1 (December 2025)](#version-1-0-1-december-2025)
3. [Documentation](#documentation)
4. [Support](#support)